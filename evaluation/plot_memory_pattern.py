import pandas as pd
import matplotlib.pyplot as plt
import os

def plot():
    file_path = "data/comparison_results.csv"
    if not os.path.exists(file_path):
        print("No data file found.")
        return

    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_numeric(df['timestamp'])
    df = df.sort_values("timestamp")
    df['rel_time'] = df['timestamp'] - df['timestamp'].min()
    
    # Filter only Time-Based Windows
    target_algos = ["TUMBLING", "SLIDING"]
    df = df[df['algorithm'].isin(target_algos)]
    
    plt.figure(figsize=(10, 5))
    
    colors = {"TUMBLING": "#d62728", "SLIDING": "#1f77b4"}
    styles = {"TUMBLING": "--", "SLIDING": "-"}
    
    for algo in target_algos:
        subset = df[df['algorithm'] == algo]
        plt.plot(subset['rel_time'], subset['keys_in_memory'], 
                 label=algo, color=colors.get(algo, "black"), 
                 linestyle=styles.get(algo, "-"), linewidth=2.5)

    plt.title("Memory Pattern Comparison: Sawtooth (Tumbling) vs. Plateau (Sliding)")
    plt.xlabel("Simulation Time (s)")
    plt.ylabel("Keys in Memory")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    output_path = "data/memory_pattern_zoom.png"
    plt.savefig(output_path, dpi=300)
    print(f"[Success] Zoomed Memory plot saved to {output_path}")

if __name__ == "__main__":
    plot()