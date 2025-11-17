from abc import ABC, abstractmethod

class IConfigProvider(ABC):

    @abstractmethod
    def get(*keys: str) -> str:
        pass 
