import pandas as pd
import numpy as np
from scipy.optimize import differential_evolution
import sys

def solve():
    print("1. Loading Data...", flush=True)
    try:
        # Load and sort data by x to align geometrically
        df = pd.read_csv('xy_data.csv')
        df_sorted = df.sort_values(by=df.columns[0])
        x_actual = df_sorted.iloc[:, 0].values
        y_actual = df_sorted.iloc[:, 1].values
        print(f"   - Successfully loaded {len(df)} points.", flush=True)
    except FileNotFoundError:
        print("\n ERROR: 'xy_data.csv' not found. Make sure it is in this folder.", flush=True)
        input("Press Enter to exit...")
        return

    # Setup t parameter
    t_values = np.linspace(6, 60, len(df))

    # Define the equations
    def get_predictions(params):
        theta, M, X = params
        theta_rad = np.deg2rad(theta)
        
        x = (t_values * np.cos(theta_rad) - 
             np.exp(M * np.abs(t_values)) * np.sin(0.3 * t_values) * np.sin(theta_rad) + 
             X)
        
        y = (42 + t_values * np.sin(theta_rad) + 
             np.exp(M * np.abs(t_values)) * np.sin(0.3 * t_values) * np.cos(theta_rad))
        return x, y

    # Cost Function
    def loss_function(params):
        x_pred, y_pred = get_predictions(params)
        
        # Align predictions geometrically
        pred_matrix = np.column_stack((x_pred, y_pred))
        pred_sorted = pred_matrix[pred_matrix[:, 0].argsort()]
        
        return np.sum(np.abs(x_actual - pred_sorted[:, 0])) + np.sum(np.abs(y_actual - pred_sorted[:, 1]))

    # Callback to show progress
    def progress_callback(xk, convergence):
        print(f"   - optimizing... (current error: {convergence:.4f})", flush=True)

    # Run Optimization
    print("2. Starting Optimization (this may take 30 seconds)...", flush=True)
    bounds = [(0, 50), (-0.05, 0.05), (0, 100)]
    
    result = differential_evolution(
        loss_function, 
        bounds, 
        strategy='best1bin', 
        tol=0.01, 
        seed=42,
        callback=progress_callback, # Adds the progress updates
        disp=True # Prints final convergence message
    )

    if result.success:
        theta, m, x = result.x
        print("\n" + "="*30)
        print("SOLUTION FOUND")
        print("="*30)
        print(f"Theta: {theta:.4f}")
        print(f"M:     {m:.4f}")
        print(f"X:     {x:.4f}")
        print(f"Loss:  {result.fun:.4f}")
        print("="*30 + "\n")
    else:
        print("Optimization failed.")
    
    input("Press Enter to close...")

if __name__ == "__main__":
    solve()