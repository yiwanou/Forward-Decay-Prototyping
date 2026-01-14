import math
from collections import defaultdict

class ForwardDecay:
    def __init__(self, lambda_=0.01, t0=None):
        self.lambda_ = lambda_
        self.t0 = t0
        self.decayed_counts = defaultdict(float)

    def _ensure_t0(self, timestamp):
        if self.t0 is None:
            self.t0 = timestamp

    def update(self, item_id, timestamp):
        self._ensure_t0(timestamp)
        d = math.exp(-self.lambda_ * (timestamp - self.t0))
        self.decayed_counts[item_id] += d

    def query(self, item_id, current_time):
        if item_id not in self.decayed_counts or self.t0 is None:
            return 0.0
        multiplier = math.exp(self.lambda_ * (current_time - self.t0))
        return self.decayed_counts[item_id] * multiplier

    def total_frequency(self, current_time):
        if self.t0 is None: return 0.0
        multiplier = math.exp(self.lambda_ * (current_time - self.t0))
        return sum(v * multiplier for v in self.decayed_counts.values())

    def top_k(self, k, current_time):
        if self.t0 is None: return []
        multiplier = math.exp(self.lambda_ * (current_time - self.t0))
        scored = [(item, value * multiplier) for item, value in self.decayed_counts.items()]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    def get_memory_usage(self):
        """Returns the number of keys currently stored (Memory Proxy)."""
        return len(self.decayed_counts)