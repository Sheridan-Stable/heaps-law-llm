import os
import pickle
from tqdm import tqdm  # For progress bar
import argparse

import math
from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt

# ----------------------------
# Plotting Strategy Classes
# ----------------------------

# Define the base class for the plotting strategy
class PlotStrategy:
    def plot(self, data, label):
        raise NotImplementedError("Subclasses must implement the plot method.")

    def save_plot(self, filename):
        plot_directory = 'plot'
        if not os.path.exists(plot_directory):
            os.makedirs(plot_directory)
        plt.savefig(f'{plot_directory}/{filename}')
        plt.clf()  # Clear the figure after saving to avoid overlap

class LogLogPlotStrategy(PlotStrategy):
    def calculate_r_squared(self, y, fit_y):
        residuals = y - fit_y
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        return r_squared

    def plot(self, data, label):
        log_x = np.log10([pair[0] for pair in data])
        log_y = np.log10([pair[1] for pair in data])

        # Perform a linear fit to the log-log data.
        coefficients = np.polyfit(log_x, log_y, 1)
        beta, log_alpha = coefficients
        alpha = 10 ** log_alpha

        # Calculate fitted values
        fit_y = np.polyval(coefficients, log_x)
        r_squared = self.calculate_r_squared(log_y, fit_y)

        # Plot the log-log data points and the fitted line.
        plt.scatter(log_x, log_y, label=f'{label} Data Points')
        plt.plot(log_x, fit_y, label=f'{label} Fit: α={alpha:.3f}, β={beta:.3f}, $R^2$={r_squared:.3f}', linewidth=2)

class SimplePlotStrategy(PlotStrategy):

    def calculate_r_squared(self, y, fit_y):
        residuals = y - fit_y
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        return r_squared

    def plot(self, data, label):
        x = np.array([pair[0] for pair in data])
        y = np.array([pair[1] for pair in data])

        # Define the power-law function.
        def power_law(x, alpha, beta):
            return alpha * np.power(x, beta)

        # Fit the power-law function to the data.
        params, _ = curve_fit(power_law, x, y, p0=[1, 1])
        alpha, beta = params

        # Calculate the fitted values and R^2
        fit_y = power_law(x, alpha, beta)
        r_squared = self.calculate_r_squared(y, fit_y)

        # Plot the data points.
        plt.scatter(x, y, label=f'{label} Data Points')

        # Plot the fitted curve.
        plt.plot(x, fit_y, label=f'{label} Fit: α={alpha:.3f}, β={beta:.3f}, $R^2$={r_squared:.3f}', linewidth=2)

# Define the context that uses the strategy
class HeapsLawAnalyzer:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def perform_plot(self, data, label):
        if not self.strategy:
            raise ValueError("Strategy not set")
        self.strategy.plot(data, label)

    def finalize_plot(self, title):
        if isinstance(self.strategy, LogLogPlotStrategy):
            plt.xlabel('log10(Total Words)')
            plt.ylabel('log10(Unique Words)')
            plt.title(title)
        elif isinstance(self.strategy, SimplePlotStrategy):
            plt.xlabel('Total Words')
            plt.ylabel('Unique Words')
            plt.title(title)
        else:
            plt.title(title)
        plt.legend()
        self.strategy.save_plot(title)

# ----------------------------
# Utility Functions
# ----------------------------

def load_aggregated_data(pickle_file):
    """
    Load aggregated data from a pickle file.
    """
    if not os.path.exists(pickle_file):
        print(f"Error: Pickle file '{pickle_file}' does not exist.")
        return None

    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        return data
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return None

def list_available_plots(aggregated_data):
    """
    List all available plots based on the aggregated data.
    """
    available_plots = []
    print(aggregated_data.items())
    for dataset, models in aggregated_data.items():
        for model_name, model_sizes in models.items():
            for model_size, prompt_types in model_sizes.items():
                for prompt_type, types in prompt_types.items():
                    for type_, data_arrays in types.items():
                        label = f"{dataset} - {model_name} - {model_size} - {prompt_type} - {type_}"
                        available_plots.append(label)
    return available_plots

def get_data_by_label(aggregated_data, label):
    """
    Retrieve data arrays based on the plot label.
    """
    parts = label.split(' - ')
    if len(parts) != 5:
        print(f"Error: Invalid label format '{label}'.")
        return None

    dataset, model_name, model_size, prompt_type, type_ = parts
    data_arrays = aggregated_data.get(dataset, {}).get(model_name, {}).get(model_size, {}).get(prompt_type, {}).get(type_, [])
    return data_arrays

def prompt_user_selection(available_plots):
    """
    Prompt the user to select single or multiple plots.
    Returns a list of selected plot labels.
    """
    print("\nDo you want to plot:")
    print("1. A single dataset/model")
    print("2. Multiple datasets/models on the same plot")
    choice = input("Enter 1 or 2: ").strip()

    while choice not in ['1', '2']:
        print("Invalid input. Please enter 1 or 2.")
        choice = input("Enter 1 or 2: ").strip()

    selected_labels = []

    if choice == '1':
        print("\nAvailable Plots:")
        for idx, plot_label in enumerate(available_plots, 1):
            print(f"{idx}. {plot_label}")

        selection = input("Enter the number of the dataset/model you want to plot: ").strip()

        while not selection.isdigit() or not (1 <= int(selection) <= len(available_plots)):
            print("Invalid selection. Please enter a valid number from the list.")
            selection = input("Enter the number of the dataset/model you want to plot: ").strip()

        selected_labels.append(available_plots[int(selection) - 1])

    elif choice == '2':
        print("\nAvailable Plots:")
        for idx, plot_label in enumerate(available_plots, 1):
            print(f"{idx}. {plot_label}")

        selections = input("Enter the numbers of the datasets/models you want to plot, separated by commas (e.g., 1,3,5): ").strip()
        selection_list = selections.split(',')

        for sel in selection_list:
            sel = sel.strip()
            if sel.isdigit() and 1 <= int(sel) <= len(available_plots):
                selected_labels.append(available_plots[int(sel) - 1])
            else:
                print(f"Warning: '{sel}' is not a valid selection and will be skipped.")

        if not selected_labels:
            print("No valid selections made. Exiting.")
            return []

    # Confirm selections
    print("\nYou have selected the following plot(s):")
    for label in selected_labels:
        print(f"- {label}")

    confirm = input("Do you want to proceed with these selections? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Exiting without plotting.")
        return []

    return selected_labels

def choose_plotting_strategy():
    """
    Prompt the user to choose a plotting strategy.
    Returns the chosen strategy object and the plot title.
    """
    print("\nChoose a plotting strategy:")
    print("1. Log-Log Plot")
    print("2. Simple Plot")
    choice = input("Enter 1 or 2: ").strip()

    while choice not in ['1', '2']:
        print("Invalid input. Please enter 1 or 2.")
        choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        strategy = LogLogPlotStrategy()
        plot_title = "Heaps' Law (Log-Log Plot)"
    else:
        strategy = SimplePlotStrategy()
        plot_title = "Heaps' Law (Simple Plot)"

    return strategy, plot_title

def main():
    # Load aggregated data from Pickle file
    pickle_file = 'final_dataset.pkl'
    aggregated_data = load_aggregated_data(pickle_file)
    if aggregated_data is None:
        return

    # List all available plots
    available_plots = list_available_plots(aggregated_data)
    if not available_plots:
        print("No plots available in the aggregated data.")
        return

    # Prompt user for selection
    selected_labels = prompt_user_selection(available_plots)
    if not selected_labels:
        return

    # Choose plotting strategy
    strategy, plot_title = choose_plotting_strategy()

    # Initialize the analyzer with the chosen strategy
    analyzer = HeapsLawAnalyzer(strategy)
    analyzer.set_strategy(strategy)

    # Plot each selected dataset/model
    for label in selected_labels:
        data_arrays = get_data_by_label(aggregated_data, label)
        if not data_arrays:
            print(f"Warning: No data found for '{label}'. Skipping.")
            continue

        # If multiple data arrays exist under the same label, plot each separately
        for idx, data in enumerate(data_arrays):
            plot_label = f"{label} [{idx+1}]"
            analyzer.perform_plot(data, plot_label)

    # Finalize and save the plot
    analyzer.finalize_plot(plot_title)
    print(f"\nPlot has been saved as '{plot_title}.png' in the 'plot' directory.")

if __name__ == "__main__":
    main()

