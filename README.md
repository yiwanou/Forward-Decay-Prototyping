# Forward Decay Prototyping: Windowed Extensions

This repository contains a reproducible implementation of the **Forward Decay** algorithm (Cormode et al., 2009) and a prototype of **Windowed Forward Decay** strategies to address the infinite memory problem in streaming systems.

## 🎯 Purpose
The original Forward Decay algorithm is computationally efficient ($O(1)$ updates) but suffers from unbounded memory growth in infinite streams because it never physically deletes keys (it only decays their weight). 

**This prototype implements and compares four "Garbage Collection" strategies** (Windows) on top of the Forward Decay core:
1.  **Tumbling Window (Time-Based)**: Eagerly resets memory every $T$ seconds.
2.  **Sliding Window (Time-Based)**: Lazily prunes keys older than $T$ seconds.
3.  **Threshold Window (Count-Based)**: Resets memory after $N$ updates.
4.  **Session Window (Gap-Based)**: Prunes keys inactive for $G$ seconds.

## 📂 Project Structure
```text
├── docker-compose.yml       # Infrastructure (Kafka + Zookeeper)
├── run_experiment.py        # Orchestrator script (Runs Python logic)
├── src/
│   ├── app.py               # Stream Processor (Quix Streams)
│   ├── collector.py         # Data Collector (Saves to CSV)
│   ├── utils/
│   │   └── ForwardDecay.py  # Core Mathematical Implementation
│   └── windows/             # Window Strategy Implementations
│       ├── tumbling_window.py
│       ├── sliding_window.py
│       ├── threshold_window.py
│       └── session_window.py
├── generator/
│   └── traffic_generator.py # Synthetic Traffic (Phased Concept Drift)
├── evaluation/
│   └── plot_comparison.py   # Visualization Script
└── data/                    # Output folder (CSV results + PNG graphs)