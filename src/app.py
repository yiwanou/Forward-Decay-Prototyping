import sys
import os
import argparse
import time
from quixstreams import Application
from windows.tumbling_window import TumblingWindow
from windows.sliding_window import SlidingWindow
from windows.threshold_window import ThresholdWindow
from windows.session_window import SessionWindow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", type=str, required=True, help="TUMBLING, SLIDING, THRESHOLD, SESSION")
    args = parser.parse_args()

    algo_type = args.algo.upper()
    print(f"[Processor] Starting {algo_type} Strategy...")

    DECAY_LAMBDA = 0.1
    
    # initialize strategy
    if algo_type == "TUMBLING":
        strategy = TumblingWindow(window_size_sec=5, lambda_=DECAY_LAMBDA)
    elif algo_type == "SLIDING":
        strategy = SlidingWindow(window_size_sec=5, lambda_=DECAY_LAMBDA, cleanup_interval=0.5)
    elif algo_type == "THRESHOLD":
        strategy = ThresholdWindow(threshold_count=100, lambda_=DECAY_LAMBDA)
    elif algo_type == "SESSION":
        strategy = SessionWindow(gap_size_sec=3, lambda_=DECAY_LAMBDA, cleanup_interval=0.5)
    else:
        print(f"Unknown algorithm: {algo_type}")
        return

    # connect to kafka
    app = Application(
        broker_address="localhost:9092",
        consumer_group=f"fwd-{algo_type.lower()}-group",
        auto_offset_reset="earliest"
    )

    input_topic = app.topic("traffic_stream", value_deserializer="json")
    output_topic = app.topic("window_results", value_serializer="json")

    sdf = app.dataframe(input_topic)

    def process(row):
        # pSrocess event
        res = strategy.process(row["item_id"], row["timestamp"])
        
        if res:
            ts = res.get("current_time")
            if ts is None:
                ts = res.get("window_end")
            if ts is None:
                ts = res.get("timestamp")
            if ts is None:
                ts = row["timestamp"] 
            keys = res.get("keys_stored")
            if keys is None:
                keys = res.get("keys_in_memory", 0)

            return {
                "algorithm": algo_type,
                "timestamp": ts,
                "keys_in_memory": keys
            }
        return None

    sdf = sdf.apply(process)
    sdf = sdf.filter(lambda x: x is not None)
    sdf = sdf.to_topic(output_topic)
    
    app.run(sdf)

if __name__ == "__main__":
    main()