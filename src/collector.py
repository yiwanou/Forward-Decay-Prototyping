import json
import csv
import os
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

def main():
    print("[Collector] Starting Data Collector...", flush=True)
    
    os.makedirs("data", exist_ok=True)
    csv_file = "data/comparison_results.csv"
    
    # Initialize Header
    if not os.path.isfile(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["algorithm", "timestamp", "keys_in_memory"])

    # Retry Connection
    consumer = None
    while consumer is None:
        try:
            consumer = KafkaConsumer(
                "window_results",
                bootstrap_servers="kafka:29092",
                auto_offset_reset="earliest",
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("[Collector] Connected to Kafka!", flush=True)
        except NoBrokersAvailable:
            print("[Collector] Waiting for Kafka...", flush=True)
            time.sleep(2)

    print(f"[Collector] Listening and writing to {csv_file}...", flush=True)

    # Write Data
    count = 0
    for message in consumer:
        data = message.value
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data["algorithm"], 
                data["timestamp"], 
                data["keys_in_memory"]
            ])
        
        # Log every 10 rows so we know it's working
        count += 1
        if count % 10 == 0:
            print(f"[Collector] Saved {count} data points so far...", flush=True)

if __name__ == "__main__":
    main()