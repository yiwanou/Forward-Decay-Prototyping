import pandas as pd
import matplotlib.pyplot as plt
import os

def plot():
    file_path = "data/comparison_results.csv"
    if not os.path.exists(file_path):
        print("No data file found.")
        return

    df = pd.read_csv(file_path)
    
    # Filter out rows with 0 throughput (startup artifacts)
    df = df[df['throughput'] > 0]
    
    # Prepare data for boxplot
    algos = df['algorithm'].unique()
    data = [df[df['algorithm'] == algo]['throughput'] for algo in algos]
    
    plt.figure(figsize=(10, 6))
    
    # Create Boxplot
    # The box shows the Interquartile Range (IQR). The orange line is Median.
    plt.boxplot(data, labels=algos, patch_artist=True, 
                boxprops=dict(facecolor="lightblue", color="blue"),
                medianprops=dict(color="red", linewidth=2))

    plt.title("Stability Analysis: Throughput Distribution by Strategy")
    plt.ylabel("Throughput (Events/Sec)")
    plt.xlabel("Window Strategy")
    plt.grid(True, linestyle='--', alpha=0.3)
    
    output_path = "data/throughput_distribution.png"
    plt.savefig(output_path, dpi=300)
    print(f"[Success] Boxplot saved to {output_path}")

if __name__ == "__main__":
    plot()