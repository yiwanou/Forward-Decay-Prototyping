from abc import ABC, abstractmethod

class WindowStrategy(ABC):
    @abstractmethod
    def process(self, item_id, timestamp):
        """
        Process a tuple.
        Returns: Dict of results if window closed, else None.
        """
        pass