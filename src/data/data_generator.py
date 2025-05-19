import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Constants
TOTAL_EMPLOYEES = 5000
CURRENT_DATE = datetime(2025, 5, 1)  # Setting current date as May 1, 2025

# Define department-specific attrition rates
DEPT_ATTRITION_RATES = {
    'Sales': 0.225,  # 20-25%
    'Collections': 0.20,  # 18-22%
    'Credit Analysis': 0.17,
    'Operations': 0.12,
    'Finance': 0.10,  # 8-12% for corporate functions
    'IT': 0.15,
    'Customer Service': 0.15,
    'HR': 0.10  # 8-12% for corporate functions
}

# Define job roles by department
JOB_ROLES = {
    'Sales': ['Account Executive', 'Sales Manager', 'Branch Sales Lead', 'Regional Sales Director', 'VP Sales'],
    'Credit Analysis': ['Credit Analyst', 'Senior Credit Analyst', 'Credit Manager', 'Risk Analyst', 'Credit Director'],
    'Collections': ['Collection Officer', 'Collection Supervisor', 'Collection Manager', 'Recovery Specialist'],
    'Operations': ['Operations Staff', 'Operations Supervisor', 'Branch Operations Manager', 'Regional Operations Director'],
    'Finance': ['Finance Staff', 'Financial Analyst', 'Accounting Manager', 'Finance Manager', 'CFO'],
    'IT': ['IT Support', 'Software Developer', 'System Analyst', 'IT Project Manager', 'IT Director', 'CTO'],
    'Customer Service': ['Customer Service Rep', 'Customer Service Supervisor', 'Customer Experience Manager'],
    'HR': ['HR Staff', 'HR Specialist', 'Recruitment Officer', 'Training Specialist', 'HR Manager', 'HR Director']
}

# Map job roles to job levels
JOB_LEVEL_MAP = {
    # Level 1 roles (entry)
    'Account Executive': 1,
    'Credit Analyst': 1,
    'Collection Officer': 1,
    'Operations Staff': 1,
    'Finance Staff': 1,
    'IT Support': 1,
    'Software Developer': 1,
    'Customer Service Rep': 1,
    'HR Staff': 1,
    'HR Specialist': 1,
    'Recruitment Officer': 1,
    
    # Level 2 roles
    'Senior Credit Analyst': 2,
    'Recovery Specialist': 2,
    'Financial Analyst': 2,
    'System Analyst': 2,
    'Training Specialist': 2,
    
    # Level 3 roles (supervisory)
    'Sales Manager': 3,
    'Collection Supervisor': 3,
    'Operations Supervisor': 3,
    'Customer Service Supervisor': 3,
    
    # Level 4 roles (management)
    'Branch Sales Lead': 4,
    'Credit Manager': 4,
    'Collection Manager': 4,
    'Branch Operations Manager': 4,
    'Accounting Manager': 4,
    'Finance Manager': 4,
    'IT Project Manager': 4,
    'Customer Experience Manager': 4,
    'HR Manager': 4,
    
    # Level 5 roles (director)
    'Regional Sales Director': 5,
    'Credit Director': 5,
    'Regional Operations Director': 5,
    'IT Director': 5,
    'HR Director': 5,
    'Risk Analyst': 5,
    
    # Level 6 roles (executive)
    'VP Sales': 6,
    'CFO': 6,
    'CTO': 6
}

# Salary ranges by job level (in IDR millions)
SALARY_RANGES = {
    1: (3, 7),      # Entry level
    2: (6, 12),     # Junior
    3: (10, 20),    # Supervisory
    4: (18, 35),    # Management
    5: (30, 60),    # Director
    6: (50, 100)    # Executive
}

# Define region distribution
REGIONS = ['Java', 'Sumatra', 'Kalimantan', 'Sulawesi', 'Bali & NT']
REGION_DIST = [0.6, 0.2, 0.1, 0.05, 0.05]  # Weighted distribution toward Java

# Define departure reasons by category
VOLUNTARY_REASONS = [
    'Better Opportunity', 
    'Work-Life Balance', 
    'Career Growth', 
    'Relocation', 
    'Education', 
    'Personal Reasons',
    'Retirement'
]

INVOLUNTARY_REASONS = [
    'Performance Issue', 
    'Reorganization', 
    'Contract End', 
    'Policy Violation',
    'Misconduct'
]

def generate_employee_base(n=TOTAL_EMPLOYEES):
    """Generate base employee demographic data"""

    data = []

    for i in range(1, n+1):
        employee = {
            'EmployeeID': f'EMP{i:05d}',
            'Gender': np.random.choice(['Male', 'Female'], p=[0.55, 0.45]),  # Indonesian workforce has slightly more males
            'Education': np.random.choice(
                ['High School', 'Diploma', 'Bachelor\'s', 'Master\'s'],
                p=[0.25, 0.15, 0.55, 0.05]  # Education distribution in Indonesia
            ),
            'MaritalStatus': np.random.choice(
                ['Single', 'Married', 'Divorced'],
                p=[0.35, 0.6, 0.05]  # Marital status distribution
            ),
            'Department': np.random.choice(
                list(DEPT_ATTRITION_RATES.keys()),
                p=[0.25, 0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]  # Department distribution
            ),
            'Region': np.random.choice(REGIONS, p=REGION_DIST)
        }

        # Set job role based on department
        employee['JobRole'] = np.random.choice(JOB_ROLES[employee['Department']])

        # Set job level based on job role
        employee['JobLevel'] = JOB_LEVEL_MAP[employee['JobRole']]

        # Set branch type (HQ is only in Java)
        if employee['Region'] == 'Java' and random.random() < 0.15:  # 15% chance of HQ if in Java
            employee['BranchType'] = 'HQ'
        else:
            employee['BranchType'] = np.random.choice(
                ['Large Branch', 'Medium Branch', 'Small Branch'],
                p=[0.2, 0.3, 0.5]  # Non-HQ branch distribution
            )

        # Set remote work status
        if employee['BranchType'] == 'HQ':
            # HQ has more hybrid options
            employee['IsRemote'] = np.random.choice(['Yes', 'No', 'Hybrid'], p=[0.05, 0.6, 0.35])
        else:
            # Other branches have less remote options
            employee['IsRemote'] = np.random.choice(['Yes', 'No', 'Hybrid'], p=[0.03, 0.8, 0.17])

        # Set commute distance
        if employee['IsRemote'] == 'Yes':
            employee['CommuteDistance'] = 0
        elif employee['IsRemote'] == 'Hybrid':
            employee['CommuteDistance'] = np.random.randint(1, 30)
        else:  # No remote work
            employee['CommuteDistance'] = np.random.randint(1, 50)

        # Set age based on job level
        employee['Age'] = max(20, min(60, int(
            np.random.normal(
                25 + 5 * employee['JobLevel'],
                3
            )
        )))
        
        data.append(employee)

    return pd.DataFrame(data)

def attrition_prob_by_tenure(tenure_months, department):
    """
    Calculate attrition probability based on tenure and department
    Implementing the specific lifecycle patterns from requirements
    """
    base_prob = DEPT_ATTRITION_RATES[department] / 12  # Monthly base rate

    # Onboarding Phase (0-3 months)
    if tenure_months <= 3:
        if department in ['Sales', 'Collections']:
            return base_prob * 2.5  # Higher attrition in Sales and Collections
        return base_prob * 1.8
    
    # Integration Phase (4-12 months)
    elif tenure_months <= 12:
        decline_factor = 1 - ((tenure_months - 3) / 9) * 0.5  # Gradual decline
        return base_prob * max(1, decline_factor * 1.8)
    
    # First Career Assessment (12-18 months)
    elif tenure_months <= 18:
        rise_factor = 1 + ((tenure_months - 12) / 6) * 0.8  # Rising risk
        return base_prob * rise_factor
    
    # Mid-career Phase (2-5 years)
    elif tenure_months <= 60:
        if department == 'Sales':
            return base_prob * 1.2  # Stable but higher than average
        elif department in ['Credit Analysis', 'IT']:
            # Peak at 2-3 years
            peak_factor = 1.5 if 24 <= tenure_months <= 36 else 1.2
            return base_prob * peak_factor
        elif department == 'Collections':
            # Continuing decline (burnout)
            return base_prob * (1 - (tenure_months - 18) / 42 * 0.3)
        return base_prob
    
    # Established Phase (5+ years)
    else:
        if any(word in ['Manager', 'Director', 'VP', 'CFO', 'CTO'] for word in JOB_LEVEL_MAP.keys()):
            # Increased risk after 5 years (career ceiling)
            return base_prob * 1.3
        elif department == 'Operations':
            # Stable, low attrition
            return base_prob * 0.7
        return base_prob * 0.9  # Generally lower attrition for long-tenured employees

def generate_employment_history(df):
    """Generate employment history including hire date, termination date, and tenure"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Generate random hire dates between 1995 and current date
    earliest_date = datetime(1995, 1, 1)
    hire_dates = []

    for _ in range(len(df)):
        # Generate a random date between earliest_date and CURRENT_DATE
        days_range = (CURRENT_DATE - earliest_date).days
        random_days = random.randint(0, days_range)
        hire_date = earliest_date + timedelta(days=random_days)

        # Skew towards more recent hires (company growth)
        if random.random() < 0.7:  # 70% chance of more recent hire
            years_ago = random.randint(0, 10)  # Last 10 years
            hire_date = CURRENT_DATE - timedelta(days=365 * years_ago + random.randint(0, 365))

        hire_dates.append(hire_date)

    df['HireDate'] = hire_dates

    # Calculate tenure in months as of current date
    df['Tenure'] = df['HireDate'].apply(lambda x: (CURRENT_DATE - x).days // 30)

    # Determine employment status and attrition flag based on tenure and department
    employment_statuses = []
    attrition_flags = []
    termination_dates = []

    for idx, row in df.iterrows():
        tenure_months = row['Tenure']
        department = row['Department']

        # Calculate attrition probability based on tenure and department
        monthly_attrition_prob = attrition_prob_by_tenure(tenure_months, department)

        # Determine if the employee has left
        has_left = False
        term_date = None

        # For each month of tenure, check if employee left
        for month in range(tenure_months):
            if random.random() < monthly_attrition_prob:
                has_left = True
                # Employee left at this month
                term_date = row['HireDate'] + timedelta(days=month * 30)
                break

        if has_left:
            employment_statuses.append('Former')
            attrition_flags.append('Yes')
            termination_dates.append(term_date)
        else:
            employment_statuses.append('Current')
            attrition_flags.append('No')
            termination_dates.append(None)

    df['EmploymentStatus'] = employment_statuses
    df['AttritionFlag'] = attrition_flags
    df['TerminationDate'] = termination_dates

    # Recalculate tenure based on termination date for former employees
    df['Tenure'] = df.apply(
        lambda row: (CURRENT_DATE - row['HireDate']).days // 30 if row['EmploymentStatus'] == 'Current'
        else (row['TerminationDate'] - row['HireDate']).days // 30,
        axis=1
    )

    return df

def generate_performance_data(df):
    """Generate performance-related data before calculating departure details"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Performance rating (1-5 scale)
    df['PerformanceRating'] = df.apply(
        lambda row: np.random.choice(
            [1, 2, 3, 4, 5],
            p=[0.05, 0.1, 0.3, 0.4, 0.15]  # Normal distribution for performance
        ),
        axis=1
    )

    # Engagement score (1-100)
    df['EngagementScore'] = df.apply(
        lambda row: max(1, min(100, int(
            np.random.normal(
                75,  # Mean
                15   # SD
            )
        ))),
        axis=1
    )

    # Work-life balance, job satisfaction, relationship with manager (1-5)
    for col in ['WorkLifeBalanceRating', 'JobSatisfaction', 'RelationshipWithManager']:
        df[col] = df.apply(
            lambda row: max(1, min(5, int(
                np.random.normal(
                    3.5,  # Mean
                    1     # SD
                )
            ))),
            axis=1
        )

    # Training hours
    df['TrainingHoursLastYear'] = df.apply(
        lambda row: int(
            np.random.normal(
                40,
                20
            ) * (1 + 0.2 * (row['JobLevel'] <= 3))  # More training for junior staff
        ),
        axis=1
    )
    df['TrainingHoursLastYear'] = df['TrainingHoursLastYear'].clip(0, 100)

    # High potential flag
    df['HighPotentialFlag'] = df.apply(
        lambda row: 'Yes' if (
            row['PerformanceRating'] >= 4 and
            row['EngagementScore'] >= 70 and
            random.random() < 0.7  # 70% of high performers are high potential
        ) else 'No',
        axis=1
    )

    return df

def generate_departure_details(df):
    """Generate departure details for former employees"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    turnover_categories = []
    departure_reasons = []
    functional_turnovers = []

    for idx, row in df.iterrows():
        if row['EmploymentStatus'] == 'Former':
            # Adjust voluntary probability based on performance
            # Lower performers more likely to be involuntary
            voluntary_prob = 0.7  # Base 70% voluntary
            if row['PerformanceRating'] <= 2:
                voluntary_prob = 0.4  # Lower performers more likely involuntary

            is_voluntary = random.random() < voluntary_prob
            turnover_category = 'Voluntary' if is_voluntary else 'Involuntary'

            # Set departure reason based on category
            if is_voluntary:
                # Factor importance by tenure stage
                tenure_years = row['Tenure'] / 12

                if tenure_years <= 2:  # 0-2 years: Compensation
                    weights = [0.4, 0.2, 0.1, 0.1, 0.1, 0.1, 0]  # Weighted toward better opportunity
                elif tenure_years <= 5:  # 2-5 years: Career growth
                    weights = [0.3, 0.1, 0.4, 0.1, 0.1, 0, 0]  # Weighted toward career growth
                else:  # 5+ years: Work-life balance
                    weights = [0.2, 0.4, 0.1, 0.1, 0, 0.1, 0.1]  # Weighted toward work-life balance

                # Adjust weights for key factors
                # If work-life balance rating is low, increase that reason
                if row['WorkLifeBalanceRating'] <= 2:
                    weights[1] += 0.2  # Increase work-life balance weight
                    # Normalize weights
                    weights = [w/sum(weights) for w in weights]

                departure_reason = np.random.choice(VOLUNTARY_REASONS, p=weights)

                # Functional turnover (beneficial/harmful)
                if row['PerformanceRating'] <= 3:
                    functional_turnover = 'Yes'  # Beneficial for low performers to leave
                else:
                    functional_turnover = 'No'  # Harmful for good performers to leave
            else:
                # For involuntary, weight toward performance issues for low performers
                if row['PerformanceRating'] <= 2:
                    weights = [0.6, 0.1, 0.1, 0.1, 0.1]  # Higher weight on performance issues
                else:
                    weights = [0.2, 0.3, 0.2, 0.15, 0.15]  # More varied reasons

                departure_reason = np.random.choice(INVOLUNTARY_REASONS, p=weights)
                functional_turnover = 'Yes'  # Involuntary is typically beneficial (company decision)
        else:
            turnover_category = None
            departure_reason = None
            functional_turnover = None
        
        turnover_categories.append(turnover_category)
        departure_reasons.append(departure_reason)
        functional_turnovers.append(functional_turnover)

    df['TurnoverCategory'] = turnover_categories
    df['DepartureReason'] = departure_reasons
    df['FunctionalTurnover'] = functional_turnovers

    return df

def generate_career_progression(df):
    """Generate career progression data like promotions and roles"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Number of promotions (based on job level and tenure)
    df['NumberOfPromotions'] = df.apply(
        lambda row: min(
            row['JobLevel'] - 1,  # Base on job level
            max(0, row['Tenure'] // 18)  # Cap by tenure (avg promotion every 18 months)
        ),
        axis=1
    )

    # Years since last promotion
    df['YearsSinceLastPromotion'] = df.apply(
        lambda row: 
        min(
            row['Tenure'] // 12,  # Cannot exceed tenure
            random.randint(0, min(5, row['Tenure'] // 12)) if row['NumberOfPromotions'] > 0
                           else row['Tenure'] // 12  # If no promotions, equals tenure
        ),
        axis=1
    )

    # Years in current role
    df['YearsInCurrentRole'] = df.apply(
        lambda row:
        min(
                row['Tenure'] // 12,  # Cannot exceed tenure
                row['YearsSinceLastPromotion']  # If promoted, equals time since promotion
                if row['NumberOfPromotions'] > 0 else row['Tenure'] // 12  # If no promotions, equals tenure
            ),
        axis=1
    )

    # Years with current manager
    df['YearsWithCurrentManager'] = df.apply(
        lambda row: min(
            random.randint(0, max(1, row['Tenure'] // 12)),
            row['Tenure'] // 12  # Cannot exceed tenure
        ),
        axis=1
    )

    # Months since last salary change
    df['MonthsSinceLastSalaryChange'] = df.apply(
        lambda row: min(
            random.randint(0, 24)  # Random months up to 2 years
            if row['YearsSinceLastPromotion'] > 0 or random.random() < 0.7  # Regular salary changes
            else 0,  # Recent promotion often means recent salary change
            row['Tenure']  # Cannot exceed tenure
        ),
        axis=1
    )

    return df

def generate_compensation_data(df):
    """Generate compensation-related data"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Monthly income based on job level, department, and performance
    df['MonthlyIncome'] = df.apply(
        lambda row: (
            # Base range from job level
            random.uniform(
                SALARY_RANGES[row['JobLevel']][0],
                SALARY_RANGES[row['JobLevel']][1]
            ) *
            # Department adjustments
            (1.1 if row['Department'] in ['IT', 'Finance'] else 1.0) *
            # Performance adjustments
            (1 + (row['PerformanceRating'] - 3) * 0.05) *
            # Tenure adjustments
            (1 + min(0.3, row['Tenure'] / 120)) *  # Up to 30% increase for 10 years
            # Promotion adjustments
            (1 + row['NumberOfPromotions'] * 0.05)  # 5% per promotion
        ),
        axis=1
    )

    # Percent salary hike
    df['PercentSalaryHikeLastYear'] = df.apply(
        lambda row:
            # Higher performance = higher hike
            min(25, max(0, (
                np.random.normal(
                    5 + 3 * (row['PerformanceRating'] - 3),  # Base on performance
                    3  # Standard deviation
                ) +
                5 * (row['YearsSinceLastPromotion'] == 0)  # Bonus for recent promotion
            ))),
            axis=1
    )

    # Overtime hours (higher in certain departments)
    df['OvertimeHours'] = df.apply(
        lambda row: int(
            np.random.exponential(
                10 if row['Department'] in ['Sales', 'Collections', 'Operations'] else 5
            )
        ),
        axis=1
    )
    df['OvertimeHours'] = df['OvertimeHours'].clip(0, 60)  # Maximum 60 hours overtime per month

    return df

def adjust_attrition_patterns(df):
    """Fine-tune the performance and engagement scores based on attrition patterns"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Adjust performance and engagement for those who left vs stayed
    for idx, row in df.iterrows():
        if row['AttritionFlag'] == 'Yes':
            if row['TurnoverCategory'] == 'Voluntary':
                # For voluntary leavers:
                if row['DepartureReason'] == 'Better Opportunity':
                    # High performers often leave for better opportunities
                    if random.random() < 0.7:
                        df.at[idx, 'PerformanceRating'] = min(5, df.at[idx, 'PerformanceRating'] + 1)
                    df.at[idx, 'EngagementScore'] = max(10, df.at[idx, 'EngagementScore'] - 20)

                elif row['DepartureReason'] == 'Work-Life Balance':
                    # Lower work-life balance ratings for those who left for this reason
                    df.at[idx, 'WorkLifeBalanceRating'] = max(1, df.at[idx, 'WorkLifeBalanceRating'] - 2)
                    df.at[idx, 'OvertimeHours'] = min(60, df.at[idx, 'OvertimeHours'] + 15)

                elif row['DepartureReason'] == 'Career Growth':
                    # Low promotion opportunities for those who left for career growth
                    df.at[idx, 'YearsSinceLastPromotion'] = min(10, df.at[idx, 'YearsSinceLastPromotion'] + 2)
                    df.at[idx, 'JobSatisfaction'] = max(1, df.at[idx, 'JobSatisfaction'] - 1)

                elif row['DepartureReason'] == 'Relocation':
                    # Relocation is less related to job factors
                    df.at[idx, 'CommuteDistance'] = min(100, df.at[idx, 'CommuteDistance'] + 20)

            elif row['TurnoverCategory'] == 'Involuntary':
                if row['DepartureReason'] == 'Performance Issue':
                    # Lower performance ratings for those let go due to performance
                    df.at[idx, 'PerformanceRating'] = max(1, df.at[idx, 'PerformanceRating'] - 2)
                    df.at[idx, 'EngagementScore'] = max(10, df.at[idx, 'EngagementScore'] - 30)

                elif row['DepartureReason'] == 'Policy Violation' or row['DepartureReason'] == 'Misconduct':
                    # May or may not be related to performance
                    if random.random() < 0.5:
                        df.at[idx, 'PerformanceRating'] = max(1, df.at[idx, 'PerformanceRating'] - 1)

                        return df

def validate_data_consistency(df):
    """Validate and ensure logical consistency between related fields"""

    # Create a copy to avoid modifying the original
    df = df.copy()

    # Fix time-based inconsistencies
    for idx, row in df.iterrows():
        # Ensure YearsInCurrentRole <= Tenure
        if row['YearsInCurrentRole'] * 12 > row['Tenure']:
            df.at[idx, 'YearsInCurrentRole'] = row['Tenure'] // 12

        # Ensure YearsSinceLastPromotion <= Tenure
        if row['YearsSinceLastPromotion'] * 12 > row['Tenure']:
            df.at[idx, 'YearsSinceLastPromotion'] = row['Tenure'] // 12

        # Ensure YearsWithCurrentManager <= Tenure
        if row['YearsWithCurrentManager'] * 12 > row['Tenure']:
            df.at[idx, 'YearsWithCurrentManager'] = row['Tenure'] // 12

        # Ensure MonthsSinceLastSalaryChange <= Tenure
        if row['MonthsSinceLastSalaryChange'] > row['Tenure']:
            df.at[idx, 'MonthsSinceLastSalaryChange'] = row['Tenure']

        # Ensure logical consistency for promotions
        if row['NumberOfPromotions'] > row['JobLevel'] - 1:
            df.at[idx, 'NumberOfPromotions'] = row['JobLevel'] - 1

        # If no promotions, YearsSinceLastPromotion should equal tenure in years
        if row['NumberOfPromotions'] == 0 and row['YearsSinceLastPromotion'] < row['Tenure'] // 12:
            df.at[idx, 'YearsSinceLastPromotion'] = row['Tenure'] // 12

        # If high job level but short tenure, reduce promotions to be realistic
        if row['JobLevel'] >= 4 and row['Tenure'] < 36 and row['NumberOfPromotions'] > 1:
            df.at[idx, 'NumberOfPromotions'] = min(2, row['NumberOfPromotions'])
        
        # Ensure educational requirements for high job levels
        if row['JobLevel'] >= 5 and row['Education'] in ['High School']:
            df.at[idx, 'Education'] = 'Bachelor\'s'

    return df

def generate_hr_dataset(n=TOTAL_EMPLOYEES):
    """Generate the complete HR dataset with all required features"""
    
    print(f"Generating synthetic HR dataset for {n} employees...")
    
    # Generate base demographic data
    print("Generating employee demographics...")
    df = generate_employee_base(n)
    
    # Generate employment history including attrition
    print("Generating employment history...")
    df = generate_employment_history(df)
    
    # Generate performance data
    print("Generating performance metrics...")
    df = generate_performance_data(df)
    
    # Generate career progression data
    print("Generating career progression data...")
    df = generate_career_progression(df)
    
    # Generate compensation data
    print("Generating compensation data...")
    df = generate_compensation_data(df)
    
    # Generate departure details for former employees
    print("Generating departure details...")
    df = generate_departure_details(df)
    
    # Adjust patterns based on attrition
    print("Adjusting attrition patterns...")
    df = adjust_attrition_patterns(df)
    
    # Validate and ensure data consistency
    print("Validating data consistency...")
    df = validate_data_consistency(df)
    
    # Format date columns as strings
    df['HireDate'] = df['HireDate'].dt.strftime('%Y-%m-%d')
    df['TerminationDate'] = df['TerminationDate'].apply(
        lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else None
    )
    
    print("Dataset generation complete!")
    
    return df

def print_dataset_stats(df):
    """Print summary statistics for the dataset"""
    
    print("\n=== BFI Finance HR Dataset Summary ===\n")
    
    # Overall stats
    total_employees = len(df)
    current_employees = sum(df['EmploymentStatus'] == 'Current')
    former_employees = sum(df['EmploymentStatus'] == 'Former')
    attrition_rate = former_employees / total_employees * 100
    
    print(f"Total Employees: {total_employees}")
    print(f"Current Employees: {current_employees} ({current_employees/total_employees*100:.1f}%)")
    print(f"Former Employees: {former_employees} ({former_employees/total_employees*100:.1f}%)")
    print(f"Overall Attrition Rate: {attrition_rate:.1f}%")
    
    # Attrition by department
    print("\nAttrition by Department:")
    for dept in df['Department'].unique():
        dept_employees = sum(df['Department'] == dept)
        dept_attrition = sum((df['Department'] == dept) & (df['AttritionFlag'] == 'Yes'))
        dept_rate = dept_attrition / dept_employees * 100
        print(f"  {dept}: {dept_rate:.1f}% ({dept_attrition}/{dept_employees})")
    
    # Tenure stats
    print("\nTenure Statistics (months):")
    print(f"  Mean: {df['Tenure'].mean():.1f}")
    print(f"  Median: {df['Tenure'].median():.1f}")
    print(f"  Min: {df['Tenure'].min()}")
    print(f"  Max: {df['Tenure'].max()}")
    
    # Turnover categories
    voluntary = sum(df['TurnoverCategory'] == 'Voluntary')
    involuntary = sum(df['TurnoverCategory'] == 'Involuntary')
    print("\nTurnover Categories:")
    print(f"  Voluntary: {voluntary} ({voluntary/former_employees*100:.1f}% of departures)")
    print(f"  Involuntary: {involuntary} ({involuntary/former_employees*100:.1f}% of departures)")
    
    # Departure reasons
    print("\nTop Departure Reasons:")
    reasons_count = df['DepartureReason'].value_counts().head(5)
    for reason, count in reasons_count.items():
        if reason is not None:
            print(f"  {reason}: {count} ({count/former_employees*100:.1f}% of departures)")

if __name__ == "__main__":
    print("This module provides functions for HR data generation.")
    print("It should be run through the DVC pipeline using:")
    print("    dvc repro")
