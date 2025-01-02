import pandas as pd
import sys

# Load the CSV file
file_path = r'C:\Users\danii\Downloads\user.csv'  # Update with your file path
df = pd.read_csv(file_path)

# Generalize 'age' to age ranges, including ages under 20
age_bins = [0, 19, 29, 39, 49, float('inf')]
age_labels = ['0-19', '20-29', '30-39', '40-49', '50+']
df['age'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=True)

# Suppress the last two digits of the 'zip_code'
df['zip_code'] = df['zip_code'].astype(str).str[:3] + '**'

# Generalize 'salary' to salary ranges
salary_bins = [0, 50000, 60000, 70000, 80000, float('inf')]
salary_labels = ['<50K', '50K-60K', '60K-70K', '70K-80K', '80K+']
df['salary'] = pd.cut(df['salary'], bins=salary_bins, labels=salary_labels, right=False)

# Drop direct identifiers like 'user_id' and 'name'
df.drop(columns=['user_id', 'name'], inplace=True)

# Prompt the user for the k value
try:
    k = int(input("Enter the value of k for k-anonymity (e.g., 2): "))
    if k < 1:
        print("k must be a positive integer.")
        sys.exit(1)
except ValueError:
    print("Invalid input. Please enter a positive integer for k.")
    sys.exit(1)

# Prompt the user for quasi-identifiers
available_columns = list(df.columns)
print("\nAvailable columns for quasi-identifiers:")
print(", ".join(available_columns))

quasi_identifiers_input = input("\nEnter the quasi-identifiers as a comma-separated list (e.g., age,gender,zip_code): ")
quasi_identifiers = [qi.strip() for qi in quasi_identifiers_input.split(",")]

# Validate quasi-identifiers
invalid_qis = [qi for qi in quasi_identifiers if qi not in available_columns]
if invalid_qis:
    print(f"The following quasi-identifiers are not valid columns: {', '.join(invalid_qis)}")
    sys.exit(1)

# Function to check for k-anonymity and provide recommendations
def check_k_anonymity(df, quasi_identifiers, k):
    # Group by the quasi-identifiers and consider only observed combinations
    group_sizes = df.groupby(quasi_identifiers, observed=True).size()

    # Filter out groups with count less than k
    less_than_k = group_sizes[group_sizes < k]

    if len(less_than_k) == 0:
        print(f"\nThe dataset is {k}-anonymous.")
        return True, []  # Return an empty list of recommendations
    else:
        print(f"\nThe dataset is NOT {k}-anonymous. {len(less_than_k)} combinations appear less than {k} times.")
        print("Combinations with less than k records:")
        print(less_than_k)

        # Provide recommendations
        print("\nRecommendations to achieve k-anonymity:")
        recommendations = []

        # Suggest removing quasi-identifiers one by one
        for qi in quasi_identifiers:
            temp_qi = [q for q in quasi_identifiers if q != qi]
            temp_group_sizes = df.groupby(temp_qi, observed=True).size()
            if temp_group_sizes.min() >= k:
                recommendations.append(f"- Try removing quasi-identifier '{qi}'.")

        # Suggest generalizing attributes further
        recommendations.append("- Consider further generalizing attributes like 'age' or 'zip_code'.")

        # Suggest changing the k value
        if k > 2:
            recommendations.append(f"- Consider decreasing the k value to {k-1}.")
        else:
            recommendations.append("- Increasing k may not be feasible due to data limitations.")

        # Print recommendations
        for rec in recommendations:
            print(rec)

        return False, recommendations  # Return recommendations

# Check k-anonymity
is_k_anonymous, recommendations = check_k_anonymity(df, quasi_identifiers, k)

# Optional: Apply recommendations
if not is_k_anonymous:
    # Here you can prompt the user to decide whether to apply any recommendations
    apply_changes = input("\nWould you like to apply any recommendations? (yes/no): ").strip().lower()
    if apply_changes == 'yes':
        # For simplicity, let's assume we remove 'gender' if recommended
        if any("gender" in rec for rec in recommendations):
            df.drop(columns=['gender'], inplace=True)
            quasi_identifiers = [qi for qi in quasi_identifiers if qi != 'gender']
            # Re-check k-anonymity
            is_k_anonymous, recommendations = check_k_anonymity(df, quasi_identifiers, k)
            print(f"\nAfter applying recommendations, is the dataset {k}-anonymous? {is_k_anonymous}")
        else:
            print("No applicable recommendations to automatically apply.")
    else:
        print("No changes applied.")

# Output the anonymized data and k-anonymity result
df.to_csv('anonymized_users.csv', index=False)
print("\nAnonymized data saved to 'anonymized_users.csv'.")
