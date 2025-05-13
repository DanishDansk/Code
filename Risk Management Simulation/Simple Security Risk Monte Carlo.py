import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to get risk data without dependencies initially
def get_risk_data():
    risks = []
    num_risks = int(input("Enter the number of risks to simulate: "))
    
    for i in range(num_risks):
        print(f"\nEnter details for Risk {i + 1}:")
        
        # Risk ID (now flexible as text or numeric)
        risk_id = input("Risk ID (numeric or text): ")
        
        # Risk Name
        name = input("Risk Name: ")
        
        # Probability validation
        while True:
            try:
                probability = float(input("Probability of Loss Over 1 Year (e.g., 0.4 for 40%): "))
                if 0 <= probability <= 1:
                    break
                print("Probability must be between 0 and 1.")
            except ValueError:
                print("Invalid input. Enter a decimal value between 0 and 1.")
        
        # Bounds validation
        while True:
            try:
                lower_bound = float(input("Lower Bound of 90% Confidence Interval ($): "))
                upper_bound = float(input("Upper Bound of 90% Confidence Interval ($): "))
                if lower_bound >= 0 and upper_bound >= lower_bound:
                    break
                print("Upper bound must be greater than or equal to lower bound, and both must be positive.")
            except ValueError:
                print("Invalid input. Enter numeric values for bounds.")

        # Risk Category
        risk_category = input("Risk Category (e.g., External Threat, Internal Threat): ")

        # Calculate log-normal parameters
        mean_log = np.log(lower_bound) + ((np.log(upper_bound) - np.log(lower_bound)) / 2)
        stddev_log = (np.log(upper_bound) - np.log(lower_bound)) / 3.28971
        
        risks.append({
            "id": risk_id,
            "name": name,
            "probability": probability,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "category": risk_category,
            "mean_log": mean_log,
            "stddev_log": stddev_log,
            "dependent_risk_id": None  # Set initially to None
        })
    
    # Display recap of all entered risks
    print("\nRecap of Entered Risks:")
    for risk in risks:
        print(f"Risk ID: {risk['id']}, Name: {risk['name']}, Probability: {risk['probability']*100:.1f}%, "
              f"Bounds: ${risk['lower_bound']} - ${risk['upper_bound']}, Category: {risk['category']}")
    
    # After all risks are collected, ask for dependencies
    print("\nNow, define dependencies between risks (if any).")
    for risk in risks:
        print(f"\nSetting dependencies for Risk ID: {risk['id']} ({risk['name']})")
        dependent_risk_id = input("Enter the dependent Risk ID if this risk depends on another risk, or leave blank: ")
        
        # Only set if a dependency is entered
        if dependent_risk_id:
            risk["dependent_risk_id"] = dependent_risk_id

    return risks

# Validation function to check if probabilities and means make sense
def validation_checks(simulation_df, expected_frequency):
    num_events = len(simulation_df[simulation_df["Total Loss"] > 0])
    observed_frequency = num_events / len(simulation_df)
    print(f"\nValidation Check:")
    print(f"Observed Event Frequency: {observed_frequency:.2%} (Expected frequency: ~{expected_frequency:.2%})")

# Export results to CSV
def export_to_csv(simulation_df, filename="simulation_results.csv"):
    simulation_df.to_csv(filename, index=False)
    print(f"Results exported to {filename}")

# Visualization function for the heatmap using Seaborn
def plot_heatmap(risks):
    data = pd.DataFrame({
        "Risk": [risk["name"] for risk in risks],
        "Probability": [risk["probability"] for risk in risks],
        "Category": [risk["category"] for risk in risks],
        "Impact": [(risk["lower_bound"] + risk["upper_bound"]) / 2 for risk in risks]
    })
    
    heatmap_data = data.pivot(index="Risk", columns="Category", values="Impact")
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlOrRd", cbar_kws={'label': 'Impact ($)'})
    plt.title("Risk Heatmap by Category and Impact")
    plt.xlabel("Category")
    plt.ylabel("Risk")
    plt.show()

# Monte Carlo simulation function
def run_simulation(risks, num_simulations, truncation_limit=None):
    simulation_results = []

    for _ in range(num_simulations):
        total_loss = 0
        for risk in risks:
            if np.random.rand() <= risk["probability"]:  # Event occurs
                # Generate random loss based on log-normal distribution
                simulated_loss = np.exp(np.random.normal(risk["mean_log"], risk["stddev_log"]))
                # Apply truncation if enabled
                if truncation_limit is not None:
                    simulated_loss = min(simulated_loss, truncation_limit)
                # Add loss to total
                total_loss += simulated_loss
                # Handle dependencies
                if risk["dependent_risk_id"]:
                    dependent_risk = next((r for r in risks if r["id"] == risk["dependent_risk_id"]), None)
                    if dependent_risk:
                        dependent_risk["probability"] += 0.1  # Increase probability of dependent risk

        simulation_results.append(total_loss)

    simulation_df = pd.DataFrame(simulation_results, columns=["Total Loss"])
    return simulation_df

# Scenario analysis
def scenario_analysis(risks, scenario="Normal"):
    for risk in risks:
        if scenario == "High Threat":
            risk["probability"] *= 1.5
        elif scenario == "Under Attack":
            risk["probability"] *= 2.0
    return risks

# Main program execution with input validation
while True:
    try:
        num_simulations = int(input("Enter the number of Monte Carlo simulations to run (e.g., 10000): "))
        break
    except ValueError:
        print("Invalid input. Enter an integer.")

apply_truncation = input("Apply truncation to extreme values? (y/n): ").strip().lower() == 'y'
truncation_limit = None
if apply_truncation:
    while True:
        try:
            truncation_limit = float(input("Enter truncation limit (e.g., 10000000 for $10 million): "))
            if truncation_limit >= 0:
                break
            print("Truncation limit must be positive.")
        except ValueError:
            print("Invalid input. Enter a positive number.")

# Step 1: Get risk data from user
risks = get_risk_data()

# Step 2: Choose scenario (optional)
scenario_choice = input("Choose a scenario (Normal, High Threat, Under Attack): ").strip()
risks = scenario_analysis(risks, scenario_choice)

# Step 3: Run simulation with enhancements
simulation_df = run_simulation(risks, num_simulations, truncation_limit)

# Step 4: Analysis and validation checks
mean_loss = simulation_df["Total Loss"].mean()
median_loss = simulation_df["Total Loss"].median()
percentile_95 = simulation_df["Total Loss"].quantile(0.95)
percentile_99 = simulation_df["Total Loss"].quantile(0.99)

print("\nMonte Carlo Simulation Results:")
print(f"Mean Total Loss: ${mean_loss:,.2f}")
print(f"Median Total Loss: ${median_loss:,.2f}")
print(f"95th Percentile Loss: ${percentile_95:,.2f}")
print(f"99th Percentile Loss: ${percentile_99:,.2f}")

# Validation
expected_frequency = sum(r["probability"] for r in risks) / len(risks)
validation_checks(simulation_df, expected_frequency)

# Export results
export_to_csv(simulation_df)

# Visualizations
plot_heatmap(risks)

# Plot distribution using Matplotlib
plt.figure(figsize=(10, 6))
plt.hist(simulation_df["Total Loss"], bins=50, color="skyblue", edgecolor="black")
plt.axvline(percentile_95, color="red", linestyle="dashed", linewidth=1, label="95th Percentile")
plt.axvline(percentile_99, color="orange", linestyle="dashed", linewidth=1, label="99th Percentile")
plt.axvline(mean_loss, color="green", linestyle="dashed", linewidth=1, label="Mean Loss")
plt.title("Distribution of Total Simulated Losses")
plt.xlabel("Total Loss ($)")
plt.ylabel("Frequency")
plt.legend()
plt.show()
10
