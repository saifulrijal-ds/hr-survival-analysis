import os
import yaml
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.data.data_generator import generate_hr_dataset

def generate_statistics_report(df):
    """Generate a Markdown report with summary statistics for the dataset"""
    
    # Overall stats
    total_employees = len(df)
    current_employees = sum(df['EmploymentStatus'] == 'Current')
    former_employees = sum(df['EmploymentStatus'] == 'Former')
    attrition_rate = former_employees / total_employees * 100
    
    # Attrition by department
    dept_stats = []
    for dept in df['Department'].unique():
        dept_employees = sum(df['Department'] == dept)
        dept_attrition = sum((df['Department'] == dept) & (df['AttritionFlag'] == 'Yes'))
        dept_rate = dept_attrition / dept_employees * 100
        dept_stats.append(f"  {dept}: {dept_rate:.1f}% ({dept_attrition}/{dept_employees})")
    
    # Tenure stats
    tenure_mean = df['Tenure'].mean()
    tenure_median = df['Tenure'].median()
    tenure_min = df['Tenure'].min()
    tenure_max = df['Tenure'].max()
    
    # Turnover categories
    voluntary = sum(df['TurnoverCategory'] == 'Voluntary')
    involuntary = sum(df['TurnoverCategory'] == 'Involuntary')
    
    # Departure reasons
    reasons_count = df['DepartureReason'].value_counts().head(5)
    reason_stats = []
    for reason, count in reasons_count.items():
        if reason is not None:
            reason_stats.append(f"  {reason}: {count} ({count/former_employees*100:.1f}% of departures)")
    
    # Create Markdown report
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown = f"""# BFI Finance HR Dataset Summary

Generated: {now}

## Overall Statistics
- **Total Employees**: {total_employees}
- **Current Employees**: {current_employees} ({current_employees/total_employees*100:.1f}%)
- **Former Employees**: {former_employees} ({former_employees/total_employees*100:.1f}%)
- **Overall Attrition Rate**: {attrition_rate:.1f}%

## Attrition by Department
{chr(10).join(dept_stats)}

## Tenure Statistics (months)
- **Mean**: {tenure_mean:.1f}
- **Median**: {tenure_median:.1f}
- **Min**: {tenure_min}
- **Max**: {tenure_max}

## Turnover Categories
- **Voluntary**: {voluntary} ({voluntary/former_employees*100:.1f}% of departures)
- **Involuntary**: {involuntary} ({involuntary/former_employees*100:.1f}% of departures)

## Top Departure Reasons
{chr(10).join(reason_stats)}
"""
    
    return markdown

def main():
    # Load parameters
    with open("params.yaml", "r") as params_file:
        params = yaml.safe_load(params_file)
    
    data_params = params["data_generation"]
    
    # Create output directories if they don't exist
    output_dir = data_params["output_dir"]
    report_dir = "reports/data_generation"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    # Generate the dataset
    sample_size = data_params["sample_size"]
    hr_data = generate_hr_dataset(sample_size)
    
    # Print summary to console (for logs)
    from src.data.data_generator import print_dataset_stats
    print_dataset_stats(hr_data)
    
    # Save to CSV
    output_path = os.path.join(output_dir, data_params["output_file"])
    hr_data.to_csv(output_path, index=False)
    print(f"\nDataset saved to {output_path}")
    
    # Create and save the Markdown report
    report = generate_statistics_report(hr_data)
    report_path = os.path.join(report_dir, "dataset_statistics.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Statistics report generated at {report_path}")

if __name__ == "__main__":
    main()