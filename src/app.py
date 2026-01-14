import os
import sys
import json
import time
from quixstreams import Application
from windows.tumbling_window import TumblingWindow
from windows.sliding_window import SlidingWindow

# CONFIGURATION
WINDOW_SIZE = 5
DECAY_LAMBDA = 0.1

def main():
    # 1. Select Algorithm
    algo_type = os.getenv("WINDOW_ALGO", "TUMBLING").upper()
    print(f"[App] Starting Processor with Algorithm: {algo_type}")

    if algo_type == "SLIDING":
        strategy = SlidingWindow(window_size_sec=WINDOW_SIZE, lambda_=DECAY_LAMBDA, cleanup_interval=0.5)
    else:
        strategy = TumblingWindow(window_size_sec=WINDOW_SIZE, lambda_=DECAY_LAMBDA)

    app = Application(
        broker_address="kafka:29092",
        consumer_group=f"fwd-{algo_type.lower()}-group",
        auto_offset_reset="earliest"
    )

    # 2. RETRY LOGIC for Topic Discovery
    # This prevents the crash when the generator creates the topic 
    # at the exact same millisecond the processor tries to read it.
    input_topic = None
    output_topic = None

    while input_topic is None:
        try:
            print("[App] Attempting to connect to topics...")
            input_topic = app.topic("traffic_stream", value_deserializer="json")
            output_topic = app.topic("window_results", value_serializer="json")
            print("[App] Topics found/created successfully.")
        except Exception as e:
            print(f"[App] Topic error: {e}. Retrying in 3s...")
            time.sleep(3)

    sdf = app.dataframe(input_topic)

    def process_wrapper(row):
        ts = row["timestamp"]
        item = row["item_id"]
        
        raw_result = strategy.process(item, ts)
        
        if raw_result:
            return {
                "algorithm": algo_type,
                "timestamp": raw_result.get("window_end", raw_result.get("current_time")),
                "keys_in_memory": raw_result["keys_stored"],
                "meta": raw_result
            }
        return None

    sdf = sdf.apply(process_wrapper)
    sdf = sdf.filter(lambda x: x is not None)
    
    # Debug print
    sdf = sdf.update(lambda row: print(f"[{row['algorithm']}] Time: {row['timestamp']:.1f} | Mem: {row['keys_in_memory']}"))
    
    sdf = sdf.to_topic(output_topic)
    app.run(sdf)

if __name__ == "__main__":
    main()