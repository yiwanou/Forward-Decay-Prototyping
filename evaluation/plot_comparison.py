import matplotlib
# FORCE HEADLESS BACKEND (Crucial for Docker)
matplotlib.use('Agg') 

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_comparison():
    input_file = "data/comparison_results.csv"
    output_dir = "evaluation/plots_comparison"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Debug: Check File Existence
    if not os.path.exists(input_file):
        print(f"[Error] {input_file} not found. The collector has not saved any data yet.")
        return

    # 2. Debug: Read and Print Raw Data
    try:
        # Read without assuming types first to see what's in there
        df = pd.read_csv(input_file)
        print(f"[Debug] Raw CSV has {len(df)} rows.")
        if not df.empty:
            print("[Debug] First 5 rows:")
            print(df.head())
        else:
            print("[Error] CSV file is empty! Waiting for data...")
            return
    except Exception as e:
        print(f"[Error] Could not read CSV: {e}")
        return

    # 3. Clean Data
    # Force types and drop bad rows
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df['keys_in_memory'] = pd.to_numeric(df['keys_in_memory'], errors='coerce')
    df = df.dropna(subset=['timestamp', 'keys_in_memory'])
    df = df.sort_values(by="timestamp")

    if df.empty:
        print("[Error] No valid numeric data found after cleaning. Check CSV format.")
        return

    # Normalize time
    start_time = df['timestamp'].min()
    df['relative_time'] = df['timestamp'] - start_time

    # Split Data
    tumbling = df[df["algorithm"] == "TUMBLING"]
    sliding = df[df["algorithm"] == "SLIDING"]

    print(f"[Debug] Plotting {len(tumbling)} Tumbling points and {len(sliding)} Sliding points.")

    # 4. Plot
    plt.figure(figsize=(12, 6))
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    
    # Plot Sliding (Blue)
    if not sliding.empty:
        plt.plot(sliding["relative_time"], sliding["keys_in_memory"], 
                 label="Sliding Window", color="#1f77b4", linewidth=2)
    
    # Plot Tumbling (Red)
    if not tumbling.empty:
        plt.plot(tumbling["relative_time"], tumbling["keys_in_memory"], 
                 label="Tumbling Window", color="#d62728", linestyle="--", marker="o", markersize=4)

    plt.xlabel("Simulation Time (seconds)")
    plt.ylabel("Keys in Memory")
    plt.title("Comparison: Tumbling vs Sliding Window Memory Usage")
    plt.legend()
    plt.tight_layout()
    
    # Save
    output_path = os.path.join