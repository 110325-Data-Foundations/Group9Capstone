# Function calculates the standardized pay annually
def calculate_standardized_salary(annual_salary, hourly_rate, typical_hours):
    # Check if annual salary exists and is valid
    if annual_salary is not None and annual_salary > 0:
        return float(annual_salary)
    
    # Check if hourly rate exists and is valid
    if hourly_rate is not None and hourly_rate > 0:
        hours = typical_hours if (typical_hours is not None and typical_hours > 0) else 40
        
        return float(hourly_rate * hours * 52)
    
    return 0.0
# calculates the coefficient of variation (standard deviation divided by mean, then multiply by 100 for %)
# What we are looking for is the score is lower means more consistent pay, higher is more inconsistent pay
def calculate_cv(mean, std_dev):
    if mean == 0:
        return 0.0
    return (std_dev / mean) * 100