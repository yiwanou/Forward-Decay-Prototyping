from .base_window import WindowStrategy
from utils.ForwardDecay import ForwardDecay

class SlidingWindow(WindowStrategy):
    def __init__(self, window_size_sec, lambda_=0.01, cleanup_interval=1.0):
        """
        Sliding Window: Continuous monitoring with Lazy Pruning (TTL).
        
        Args:
            window_size_sec (int): Keys older than this (TTL) are deleted.
            lambda_ (float): Decay rate.
            cleanup_interval (float): How often (in stream time) to scan for expired keys.
        """
        self.window_size = window_size_sec
        self.cleanup_interval = cleanup_interval
        self.lambda_ = lambda_
        
        # state
        self.fd = ForwardDecay(lambda_=self.lambda_)
        self.last_seen = {}  
        
        self.next_cleanup_time = None

    def _prune_expired_keys(self, current_time):
        """
        Garbage Collection: Scans all keys and deletes those that 
        haven't been seen within the window size.
        """
        expired_keys = []
        
        # identify expired keys
        for item_id, last_ts in self.last_seen.items():
            if current_time - last_ts > self.window_size:
                expired_keys.append(item_id)
        
        # delete them
        for item_id in expired_keys:
            del self.last_seen[item_id]
            if item_id in self.fd.decayed_counts:
                del self.fd.decayed_counts[item_id]
                
        return len(expired_keys)

    def process(self, item_id, timestamp):
        #  initialization
        if self.next_cleanup_time is None:
            self.fd._ensure_t0(timestamp)
            self.next_cleanup_time = timestamp + self.cleanup_interval

        result = None

        #  update State
        self.fd.update(item_id, timestamp)
        self.last_seen[item_id] = timestamp

        #  cleanup
        if timestamp >= self.next_cleanup_time:
            #  prune
            deleted_count = self._prune_expired_keys(timestamp)
            
            keys_in_memory = self.fd.get_memory_usage()
            top_k = self.fd.top_k(5, timestamp)
            
            result = {
                "window_type": "Sliding",
                "current_time": timestamp,
                "keys_stored": keys_in_memory,    
                "keys_pruned": deleted_count,
                "top_heavy_hitters": top_k
            }
            
            # schedule next cleanup
            while timestamp >= self.next_cleanup_time:
                self.next_cleanup_time += self.cleanup_interval
        
        return result