from datetime import datetime, timedelta

from interfaces.retry_interface import RetryStrategy

class ExponentialBackoffStrategy(RetryStrategy):

    def next_retry(self, attempt_count: int):
        delay = 2 ** attempt_count

        return datetime.utcnow() + timedelta(seconds=delay)
