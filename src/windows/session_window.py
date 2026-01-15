from .base_window import WindowStrategy
from utils.ForwardDecay import ForwardDecay

class SessionWindow(WindowStrategy):
    def __init__(self, gap_size_sec, lambda_=0.01, cleanup_interval=1.0):
        """
        Session Window: Prunes keys that have been inactive for > gap_size_sec.
        """
        self.gap_size = gap_size_sec
        self.lambda_ = lambda_
        self.cleanup_interval = cleanup_interval
        
        self.fd = ForwardDecay(lambda_=self.lambda_)
        self.last_active = {} # Map[item_id] -> last_timestamp
        self.next_cleanup = None

    def process(self, item_id, timestamp):
        if self.next_cleanup is None:
            self.fd._ensure_t0(timestamp)
            self.next_cleanup = timestamp + self.cleanup_interval

        # Update Session Activity
        self.fd.update(item_id, timestamp)
        self.last_active[item_id] = timestamp
        
        result = None

        # Periodic Cleanup (Check for Session Timeouts)
        if timestamp >= self.next_cleanup:
            # Identify keys active longer than the gap
            expired_keys = [
                k for k, last_ts in self.last_active.items() 
                if (timestamp - last_ts) > self.gap_size
            ]
            
            # Prune
            for k in expired_keys:
                del self.last_active[k]
                if k in self.fd.decayed_counts:
                    del self.fd.decayed_counts[k]
            
            # Report
            result = {
                "window_type": "Session",
                "current_time": timestamp,
                "keys_stored": self.fd.get_memory_usage(),
                "meta": f"Pruned {len(expired_keys)} sessions"
            }
            
            while timestamp >= self.next_cleanup:
                self.next_cleanup += self.cleanup_interval
                
        return result