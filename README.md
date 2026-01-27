# Forward Decay Prototyping

## Project Description

This project addresses the "Infinite Memory" problem found in the original **Forward Decay** algorithm (Cormode et al., 2009).

While Forward Decay is computationally efficient ($O(1)$ updates) for time-decaying data, it mathematically "forgets" old data without physically deleting it. In infinite streams, this leads to **memory bloat**, where millions of near-zero weight items eventually crash the system.

**Our Solution:**
We implemented a **Windowed Forward Decay** prototype that wraps the core algorithm with four distinct "Garbage Collection" strategies (based on *Verwiebe et al., 2023*) to reclaim memory while preserving speed:
1.  **Tumbling Window:** Hard resets every $T$ seconds (Low CPU, "Sawtooth" memory).
2.  **Sliding Window:** Lazily prunes keys inactive for $T$ seconds (Stable memory).
3.  **Threshold Window:** Resets after $N$ items (Volume-based).
4.  **Session Window:** Prunes keys after an inactivity gap (User-behavior based).

## Project Structure

* **`docker-compose.yml`**: Runs the infrastructure (Kafka & Zookeeper).
* **`run_experiment.py`**: The orchestrator script that runs the entire simulation.
* **`src/`**: Contains the Stream Processors and Window implementations.
* **`generator/`**: Generates synthetic "phased" traffic to test memory reclamation.
* **`evaluation/`**: Scripts to generate research-grade plots (Memory vs. Time).

---

## How to Run

This project uses a **Hybrid Architecture**: Kafka runs in Docker, while the Python logic runs locally for real-time control.

### 1. Prerequisites
* **Docker Desktop** (running).
* **Python 3.9+**.
* Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Start Infrastructure
Open a terminal in the project root and start the message broker:
```bash
docker-compose up -d