import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_solution():
    try:
        df = pd.read_csv('xy_data.csv')
    except FileNotFoundError:
        print("xy_data.csv not found")
        return

    # Parameters found by solver.py
    theta_deg = 30.0437
    M = 0.0300
    X = 55.0155

    # Generate Curve
    t_values = np.linspace(6, 60, len(df))
    theta_rad = np.deg2rad(theta_deg)

    x_pred = (t_values * np.cos(theta_rad) - 
              np.exp(M * np.abs(t_values)) * np.sin(0.3 * t_values) * np.sin(theta_rad) + 
              X)
    
    y_pred = (42 + t_values * np.sin(theta_rad) + 
              np.exp(M * np.abs(t_values)) * np.sin(0.3 * t_values) * np.cos(theta_rad))

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1], s=10, color='blue', alpha=0.2, label='Actual Data')
    plt.plot(x_pred, y_pred, color='red', linewidth=2, label='Predicted Curve')
    
    plt.title(f"Curve Fit: Theta={theta_deg}, M={M}, X={X}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('solution_plot.png')
    print("Graph saved as 'solution_plot.png'")

if __name__ == "__main__":
    plot_solution()