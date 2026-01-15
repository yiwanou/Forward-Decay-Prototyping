import subprocess
import time
import os
import signal
import sys

def run():
    print("==============================================")
    print("   FORWARD DECAY PROTOTYPE ORCHESTRATOR")
    print("==============================================")
    
    processes = []
    
    # 1. Start Data Collector
    print("[1/3] Starting Collector...")
    p_col = subprocess.Popen([sys.executable, "src/collector.py"])
    processes.append(p_col)
    
    # 2. Start Processors (All 4 types in parallel)
    algos = ["TUMBLING", "SLIDING", "THRESHOLD", "SESSION"]
    for algo in algos:
        print(f"[2/3] Launching {algo} Processor...")
        p = subprocess.Popen([sys.executable, "src/app.py", "--algo", algo])
        processes.append(p)

    # 3. Start Traffic Generator
    print("[3/3] Launching Traffic Generator (Phased Traffic)...")
    time.sleep(2) # Give processors time to connect
    p_gen = subprocess.Popen([sys.executable, "generator/traffic_generator.py"])
    processes.append(p_gen)

    print("\n--- EXPERIMENT RUNNING ---")
    print("Leave this running for ~45 seconds to see phase changes.")
    print("Press Ctrl+C to stop and generate the graph.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping all processes...")
        # Kill all subprocesses
        for p in processes:
            p.terminate()
        
        print("Generating Final Plot...")
        subprocess.run([sys.executable, "evaluation/plot_comparison.py"])
        print("Done. Check data/final_comparison.png")

if __name__ == "__main__":
    run()