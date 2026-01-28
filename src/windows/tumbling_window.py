from .base_window import WindowStrategy
from utils.ForwardDecay import ForwardDecay
class TumblingWindow(WindowStrategy):
    def __init__(self, window_size_sec, lambda_=0.01):
        self.window_size = window_size_sec
        self.lambda_ = lambda_
        
        self.fd = None
        self.window_start = None
        self.window_end = None

    def _reset_window(self, start_time):
        self.window_start = start_time
        self.window_end = start_time + self.window_size
        # reset to a newinsatnce
        self.fd = ForwardDecay(lambda_=self.lambda_, t0=self.window_start)

    def process(self, item_id, timestamp):
        if self.window_start is None:
            self._reset_window(timestamp)

        result = None

        if timestamp >= self.window_end:
            #  measure the system before reset
            keys_in_memory = self.fd.get_memory_usage()
            top_k = self.fd.top_k(5, self.window_end)
            
            result = {
                "window_start": self.window_start,
                "window_end": self.window_end,
                "keys_stored": keys_in_memory,  
                "top_heavy_hitters": top_k
            }
            
            #  advance window
            while timestamp >= self.window_end:
                self.window_start += self.window_size
                self.window_end += self.window_size
            
            #  hard reset
            self.fd = ForwardDecay(lambda_=self.lambda_, t0=self.window_start)


        if timestamp >= self.window_start:
            self.fd.update(item_id, timestamp)
            
        return result