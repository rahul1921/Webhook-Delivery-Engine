from abc import ABC, abstractmethod
from datetime import datetime

class RetryStrategy(ABC):

    @abstractmethod
    def next_retry(self, attempt_count: int) -> datetime:
        pass
