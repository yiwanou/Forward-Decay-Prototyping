import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot():
    file_path = "data/comparison_results.csv"
    if not os.path.exists(file_path):
        print("No data file found.")
        return

    df = pd.read_csv(file_path)
    
    # clean the data
    df['keys_in_memory'] = pd.to_numeric(df['keys_in_memory'], errors='coerce')
    df = df.dropna()

    # calc the statistcs
    stats = df.groupby('algorithm')['keys_in_memory'].agg(['max', 'mean']).reset_index()
    stats.columns = ['algorithm', 'Peak Memory', 'Average Memory']
    
    stats = stats.sort_values('Peak Memory', ascending=False)

    # plot
    plt.figure(figsize=(10, 6))
    
    x = np.arange(len(stats['algorithm']))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, stats['Peak Memory'], width, label='Peak (Worst Case)', color='#d62728', alpha=0.8)
    bars2 = plt.bar(x + width/2, stats['Average Memory'], width, label='Average (Typical)', color='#1f77b4', alpha=0.8)

    plt.xlabel('Window Strategy', fontweight='bold')
    plt.ylabel('Keys in Memory', fontweight='bold')
    plt.title('Resource Constraints: Peak vs. Average Memory Usage', fontsize=12)
    plt.xticks(x, stats['algorithm'])
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
    
    add_labels(bars1)
    add_labels(bars2)

    plt.tight_layout()
    
    output_path = "data/memory_stats_bar.png"
    plt.savefig(output_path, dpi=300)
    print(f"[Success] Stats graph saved to {output_path}")

if __name__ == "__main__":
    plot()