from abc import ABC, abstractmethod

class DispatcherInterface(ABC):

    @abstractmethod
    async def dispatch(
        self,
        url: str,
        payload: dict,
        signature: str
    ):
        pass
