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
    
    # Filter only Behavior-Based Windows
    target_algos = ["THRESHOLD", "SESSION"]
    df = df[df['algorithm'].isin(target_algos)]
    
    plt.figure(figsize=(10, 5))
    
    colors = {"THRESHOLD": "#2ca02c", "SESSION": "#9467bd"}
    
    for algo in target_algos:
        subset = df[df['algorithm'] == algo]
        plt.plot(subset['rel_time'], subset['keys_in_memory'], 
                 label=algo, color=colors.get(algo, "black"), linewidth=2)

    plt.title("Semantic Comparison: Count-Based vs. Activity-Based Pruning")
    plt.xlabel("Simulation Time (s)")
    plt.ylabel("Keys in Memory")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    output_path = "data/semantics_comparison.png"
    plt.savefig(output_path, dpi=300)
    print(f"[Success] Semantics plot saved to {output_path}")

if __name__ == "__main__":
    plot()