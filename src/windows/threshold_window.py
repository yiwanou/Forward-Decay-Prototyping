from .base_window import WindowStrategy
from utils.ForwardDecay import ForwardDecay

class ThresholdWindow(WindowStrategy):
    def __init__(self, threshold_count, lambda_=0.01):
        """
        Threshold Window: Resets the entire state after N updates.
        """
        self.threshold = threshold_count
        self.lambda_ = lambda_
        self.count = 0
        self.fd = ForwardDecay(lambda_=self.lambda_)

    def process(self, item_id, timestamp):
        # initialize
        self.fd._ensure_t0(timestamp)

        # update
        self.fd.update(item_id, timestamp)
        self.count += 1
        
        result = None

        # checkt threshold
        if self.count >= self.threshold:
            keys_in_memory = self.fd.get_memory_usage()
            
            result = {
                "window_type": "Threshold",
                "current_time": timestamp,
                "keys_stored": keys_in_memory,
                "meta": f"Reset at {self.count} items"
            }
            
            #  reset
            self.fd = ForwardDecay(lambda_=self.lambda_)
            self.fd._ensure_t0(timestamp)
            self.count = 0
            
        return result