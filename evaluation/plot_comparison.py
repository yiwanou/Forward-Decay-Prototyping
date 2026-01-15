import pandas as pd
import matplotlib.pyplot as plt
import os

def plot():
    file_path = "data/comparison_results.csv"
    if not os.path.exists(file_path):
        print("No data file found.")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception:
        print("CSV is empty or invalid.")
        return

    if df.empty:
        print("Dataframe is empty.")
        return

    # Clean and Sort
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df = df.dropna().sort_values("timestamp")
    
    # Normalize time (Relative start from 0)
    df['rel_time'] = df['timestamp'] - df['timestamp'].min()
    
    plt.figure(figsize=(12, 6))
    
    # Styles for each algo
    styles = {
        "TUMBLING": {"color": "#d62728", "style": "--", "label": "Tumbling (Time)"},
        "SLIDING":  {"color": "#1f77b4", "style": "-",  "label": "Sliding (Lazy)"},
        "THRESHOLD":{"color": "#2ca02c", "style": ":",  "label": "Threshold (Count)"},
        "SESSION":  {"color": "#9467bd", "style": "-.", "label": "Session (Gap)"}
    }

    # Plot each algorithm found in the CSV
    for algo in df['algorithm'].unique():
        subset = df[df['algorithm'] == algo]
        style = styles.get(algo, {"color": "black", "style": "-", "label": algo})
        
        plt.plot(subset['rel_time'], subset['keys_in_memory'], 
                 label=style["label"], 
                 color=style["color"], 
                 linestyle=style["style"], 
                 linewidth=2,
                 alpha=0.8)

    plt.xlabel("Simulation Time (s)")
    plt.ylabel("Keys in Memory")
    plt.title("Memory Efficiency: Windowed Forward Decay Comparison")
    plt.grid(True, which="both", linestyle='--', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    output_path = "data/final_comparison.png"
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot()