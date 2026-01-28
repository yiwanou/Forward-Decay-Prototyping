import json
import csv
import os
from kafka import KafkaConsumer

def main():
    csv_file = "data/comparison_results.csv"
    os.makedirs("data", exist_ok=True)
    

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "timestamp", "keys_in_memory"])

    consumer = KafkaConsumer(
        "window_results",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print(f"[Collector] Writing to {csv_file}...")
    for msg in consumer:
        row = msg.value
        with open(csv_file, 'a', newline='') as f:
            csv.writer(f).writerow([row["algorithm"], row["timestamp"], row["keys_in_memory"]])

if __name__ == "__main__":
    main()