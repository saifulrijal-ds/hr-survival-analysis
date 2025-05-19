# BFI Finance HR Dataset Data Dictionary

## Overview
This data dictionary describes the synthetic HR dataset generated for BFI Finance. The dataset contains comprehensive employee information including demographics, employment history, performance metrics, career progression, compensation data, and departure details for 5,000 employees.

## Variables

### Employee Demographics

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| EmployeeID | String | Unique employee identifier | Format: "EMP#####" (e.g., "EMP00001") |
| Gender | String | Employee gender | "Male", "Female" |
| Age | Integer | Employee age in years | 20-60, normally distributed based on job level |
| Education | String | Highest education level | "High School", "Diploma", "Bachelor's", "Master's" |
| MaritalStatus | String | Employee marital status | "Single", "Married", "Divorced" |
| Department | String | Department name | "Sales", "Collections", "Credit Analysis", "Operations", "Finance", "IT", "Customer Service", "HR" |
| JobRole | String | Specific job title | Various roles by department (see department-specific job roles in code) |
| JobLevel | Integer | Hierarchical level | 1 (Entry) to 6 (Executive) |
| Region | String | Geographic region in Indonesia | "Java", "Sumatra", "Kalimantan", "Sulawesi", "Bali & NT" |
| BranchType | String | Type of branch | "HQ", "Large Branch", "Medium Branch", "Small Branch" |
| IsRemote | String | Remote work status | "Yes", "No", "Hybrid" |
| CommuteDistance | Integer | Commute distance in km | 0-50 (0 for fully remote employees) |

### Employment History

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| HireDate | Date | Date of hire | 1995-01-01 to current date (format: YYYY-MM-DD) |
| Tenure | Integer | Tenure in months | Calculated from hire date to current date or termination date |
| EmploymentStatus | String | Current employment status | "Current", "Former" |
| AttritionFlag | String | Indicates if employee has left | "Yes", "No" |
| TerminationDate | Date | Date of termination if applicable | Format: YYYY-MM-DD, null for current employees |

### Performance Metrics

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| PerformanceRating | Integer | Annual performance rating | 1 (Low) to 5 (Excellent) |
| EngagementScore | Integer | Employee engagement score | 1-100 |
| WorkLifeBalanceRating | Integer | Work-life balance rating | 1 (Poor) to 5 (Excellent) |
| JobSatisfaction | Integer | Job satisfaction rating | 1 (Low) to 5 (High) |
| RelationshipWithManager | Integer | Quality of relationship with manager | 1 (Poor) to 5 (Excellent) |
| TrainingHoursLastYear | Integer | Training hours in previous year | 0-100 |
| HighPotentialFlag | String | High potential employee indicator | "Yes", "No" |

### Career Progression

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| NumberOfPromotions | Integer | Number of promotions received | 0 to (JobLevel-1) |
| YearsSinceLastPromotion | Integer | Years since last promotion | 0 to tenure in years (equals tenure if no promotions) |
| YearsInCurrentRole | Integer | Years in current role | 0 to tenure in years |
| YearsWithCurrentManager | Integer | Years with current manager | 0 to tenure in years |
| MonthsSinceLastSalaryChange | Integer | Months since last salary change | 0 to tenure in months |

### Compensation Data

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| MonthlyIncome | Float | Monthly income in IDR millions | Range varies by job level: <br>Level 1: 3-7 <br>Level 2: 6-12 <br>Level 3: 10-20 <br>Level 4: 18-35 <br>Level 5: 30-60 <br>Level 6: 50-100 <br>(Adjusted based on department, performance, tenure, promotions) |
| PercentSalaryHikeLastYear | Float | Percentage salary increase in previous year | 0-25% |
| OvertimeHours | Integer | Overtime hours worked per month | 0-60 |

### Attrition Details (For Former Employees)

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| TurnoverCategory | String | Type of turnover | "Voluntary", "Involuntary", null for current employees |
| DepartureReason | String | Specific reason for departure | Voluntary: "Better Opportunity", "Work-Life Balance", "Career Growth", "Relocation", "Education", "Personal Reasons", "Retirement" <br><br>Involuntary: "Performance Issue", "Reorganization", "Contract End", "Policy Violation", "Misconduct" <br><br>null for current employees |
| FunctionalTurnover | String | Whether turnover was beneficial for company | "Yes" (beneficial), "No" (harmful), null for current employees |

## Notes

1. Attrition probabilities vary by department:
   - Sales: 22.5%
   - Collections: 20.0%
   - Credit Analysis: 17.0%
   - Operations: 12.0%
   - Finance: 10.0%
   - IT: 15.0%
   - Customer Service: 15.0%
   - HR: 10.0%

2. Attrition patterns follow specific lifecycle patterns:
   - Onboarding phase (0-3 months): Higher attrition, especially in Sales and Collections
   - Integration phase (4-12 months): Gradual decline in attrition risk
   - First career assessment (12-18 months): Rising attrition risk
   - Mid-career phase (2-5 years): Department-specific patterns
   - Established phase (5+ years): Generally lower attrition with exceptions

3. The dataset deliberately models realistic HR patterns including:
   - Performance-based departure patterns
   - Department-specific attrition trends
   - Tenure-based career progression
   - Job level appropriate education requirements
   - Correlation between performance, compensation, and turnover
