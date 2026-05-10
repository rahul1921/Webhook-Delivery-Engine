from abc import ABC, abstractmethod

class SignerInterface(ABC):

    @abstractmethod
    def sign(self, secret: str, payload: dict) -> str:
        pass
