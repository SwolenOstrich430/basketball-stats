from abc import ABC, abstractmethod
from app.service.storage.istorage_provider import IStorageProvider

class IGenericStorageProvider(IStorageProvider):
    
    @abstractmethod
    def get_provider(self) -> IStorageProvider:
        pass 