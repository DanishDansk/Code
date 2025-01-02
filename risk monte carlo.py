import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

# Function to generate delay based on specified distribution and parameters
def generate_delay(distribution, params):
    try:
        if distribution == "normal":
            return np.random.normal(params["mean"], params["std"])
        elif distribution == "uniform":
            return np.random.uniform(params["low"], params["high"])
        elif distribution == "exponential":
            return np.random.exponential(params["scale"])
        elif distribution == "poisson":
            return np.random.poisson(params["lam"])
        elif distribution == "gamma":
            return np.random.gamma(params["shape"], params["scale"])
        elif distribution == "beta":
            return np.random.beta(params["a"], params["b"])
        elif distribution == "lognormal":
            return np.random.lognormal(params["mean"], params["sigma"])
        elif distribution == "weibull":
            return np.random.weibull(params["a"]) * params.get("scale", 1)
        else:
            raise ValueError(f"Unsupported distribution: '{distribution}'.")
    except KeyError as e:
        raise KeyError(f"Missing parameter '{e.args[0]}' for distribution '{distribution}'.") from e
    except Exception as e:
        raise ValueError(f"Error generating delay for distribution '{distribution}': {e}") from e

# Main Monte Carlo function with multiple distribution options and error handling
def run_monte_carlo_multi_dist(
    num_simulations=10000,
    material_config={"distribution": "normal", "params": {"mean": 3.0, "std": 0.5}, "probability": 0.3},
    weather_config={"distribution": "normal", "params": {"mean": 2.0, "std": 0.3}, "probability": 0.25},
    labor_config={"distribution": "normal", "params": {"mean": 1.5, "std": 0.2}, "probability": 0.2}
):
    total_delays = []

    for _ in range(num_simulations):
        total_delay = 0

        if np.random.rand() < material_config["probability"]:
            total_delay += generate_delay(material_config["distribution"], material_config["params"])

        if np.random.rand() < weather_config["probability"]:
            total_delay += generate_delay(weather_config["distribution"], weather_config["params"])

        if np.random.rand() < labor_config["probability"]:
            total_delay += generate_delay(labor_config["distribution"], labor_config["params"])

        total_delays.append(total_delay)

    total_delays = np.array(total_delays)

    # Calculate summary statistics
    average_delay = np.mean(total_delays)
    std_dev_delay = np.std(total_delays)
    delay_90th_percentile = np.percentile(total_delays, 90)
    delay_95th_percentile = np.percentile(total_delays, 95)
    delay_99th_percentile = np.percentile(total_delays, 99)

    within_one_std = np.mean((average_delay - std_dev_delay <= total_delays) & (total_delays <= average_delay + std_dev_delay)) * 100
    within_two_std = np.mean((average_delay - 2 * std_dev_delay <= total_delays) & (total_delays <= average_delay + 2 * std_dev_delay)) * 100
    within_three_std = np.mean((average_delay - 3 * std_dev_delay <= total_delays) & (total_delays <= average_delay + 3 * std_dev_delay)) * 100

    # Plotting with Matplotlib only
    plt.figure(figsize=(14, 8))
    plt.hist(total_delays, bins=20, color="skyblue", edgecolor="black", alpha=0.6)

    plt.axvline(average_delay, color='red', linestyle='--', linewidth=2, label=f"Average: {average_delay:.2f} weeks")
    plt.axvline(delay_90th_percentile, color='green', linestyle='--', linewidth=2, label=f"90th Percentile: {delay_90th_percentile:.2f} weeks")
    plt.axvline(delay_95th_percentile, color='orange', linestyle='--', linewidth=2, label=f"95th Percentile: {delay_95th_percentile:.2f} weeks")
    plt.axvline(delay_99th_percentile, color='purple', linestyle='--', linewidth=2, label=f"99th Percentile: {delay_99th_percentile:.2f} weeks")

    plt.title("Monte Carlo Simulation of Project Delays", fontsize=16)
    plt.xlabel("Total Delay (weeks)", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)

    stats_text = (
        f"Mean Delay: {average_delay:.2f} weeks\n"
        f"Std Dev: {std_dev_delay:.2f} weeks\n"
        f"90th Percentile: {delay_90th_percentile:.2f} weeks\n"
        f"95th Percentile: {delay_95th_percentile:.2f} weeks\n"
        f"99th Percentile: {delay_99th_percentile:.2f} weeks\n"
        f"Empirical Rule Coverage:\n"
        f" - 68% within 1σ: {within_one_std:.2f}%\n"
        f" - 95% within 2σ: {within_two_std:.2f}%\n"
        f" - 99.7% within 3σ: {within_three_std:.2f}%"
    )
    plt.gca().text(0.95, 0.95, stats_text, transform=plt.gca().transAxes, fontsize=10,
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="white"))

    plt.legend()
    plt.show()

    SimulationResults = namedtuple("SimulationResults", [
        "average_delay", "std_dev_delay", "within_one_std", "within_two_std", "within_three_std",
        "percentile_90", "percentile_95", "percentile_99"
    ])
    
    return SimulationResults(
        average_delay, std_dev_delay, within_one_std, within_two_std, within_three_std,
        delay_90th_percentile, delay_95th_percentile, delay_99th_percentile
    )

# Run the simulation without Seaborn
results = run_monte_carlo_multi_dist(
    material_config={"distribution": "normal", "params": {"mean": 3.0, "std": 0.5}, "probability": 0.3},
    weather_config={"distribution": "exponential", "params": {"scale": 2.0}, "probability": 0.25},
    labor_config={"distribution": "uniform", "params": {"low": 1.0, "high": 2.0}, "probability": 0.2}
)
print(results)
