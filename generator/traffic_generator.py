import time
import json
import random
from kafka import KafkaProducer

def generate():
    print("[Generator] Connecting to localhost:9092...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    sim_time = 1000.0
    phase_duration = 10 
    
    print("[Generator] Starting Phased Traffic...")
    try:
        while True:
            phase_index = int(sim_time / phase_duration)
            
            start_id = phase_index * 1000
            end_id = start_id + 1000
            
            for _ in range(50):
                user_id = f"user_{random.randint(start_id, end_id)}"
                producer.send("traffic_stream", {"timestamp": sim_time, "item_id": user_id})

            sim_time += 0.2
            time.sleep(0.05) 
            
            if int(sim_time) % 5 == 0:
                print(f"Sim Time: {sim_time:.1f}")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    generate()