import time
import json
import random
import os
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

def get_producer():
    # Dynamic Broker Address
    broker = os.getenv("KAFKA_BROKER", "localhost:9092")
    print(f"[Generator] Attempting to connect to Kafka at: {broker}")
    
    # RETRY LOGIC: Keep trying until Kafka is ready
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[broker],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            print("[Generator] Successfully connected to Kafka!")
            return producer
        except NoBrokersAvailable:
            print("[Generator] Kafka not ready yet. Retrying in 2 seconds...")
            time.sleep(2)
        except Exception as e:
            print(f"[Generator] Unexpected connection error: {e}. Retrying...")
            time.sleep(2)

def generate_comparison_traffic():
    # 1. Connect with Retry
    producer = get_producer()

    # Simulation Start
    sim_time = 1000.0  # Arbitrary start time
    
    # PHASE CONFIGURATION
    phase_duration = 10 
    
    print("Starting Comparison Traffic Generator...")
    print("Goal: Demonstrate memory cleanup by shifting active user sets.")

    try:
        while True:
            # Determine current phase (New set of 1000 users every 10s)
            phase_index = int(sim_time / phase_duration)
            
            # The "Active" users for this phase are distinct from previous phases
            current_user_range_start = phase_index * 1000
            current_user_range_end = current_user_range_start + 1000
            
            # Generate a batch of events
            for _ in range(50):
                user_id = f"user_{random.randint(current_user_range_start, current_user_range_end)}"
                
                data = {
                    "timestamp": sim_time,
                    "item_id": user_id
                }
                producer.send("traffic_stream", value=data)

            # Advance Simulation Time
            sim_time += 0.2  # Advance 200ms per batch
            time.sleep(0.05) # Throttle generation speed

            if int(sim_time) % 5 == 0:
                print(f"[Generator] Sim Time: {sim_time:.1f} | Active User Range: {current_user_range_start}-{current_user_range_end}")

    except KeyboardInterrupt:
        print("Stopping generator.")

if __name__ == "__main__":
    generate_comparison_traffic()