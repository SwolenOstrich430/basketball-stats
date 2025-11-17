from abc import ABC, abstractmethod

class IStorageProvider(ABC):
    
    @abstractmethod
    def upload_file(bucket_name: str, file_name: str) -> bool: 
        pass 

    @abstractmethod
    def download_file(bucket_name: str, file_name: str) -> str: 
        pass 

    @abstractmethod
    def file_exists(bucket_name: str, file_name: str) -> bool: 
        pass 
