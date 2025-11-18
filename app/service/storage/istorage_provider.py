from abc import ABC, abstractmethod
from airflow.hooks.base import BaseHook
from airflow.sdk import Connection
class IStorageProvider(ABC):
    
    @abstractmethod
    def upload_file(
        self, 
        bucket_name: str, 
        storage_path: str,
        file_name: str
    ) -> bool: 
        pass 

    @abstractmethod
    def download_file(
        self, 
        bucket_identifier: str, 
        storage_path: str, 
        local_path: str
    ): 
        pass 

    @abstractmethod
    def bucket_exists(self, bucket_name: str) -> bool:
        pass 

    @abstractmethod
    def file_exists(self, bucket_name: str, file_name: str) -> bool: 
        pass 

    @abstractmethod
    def get_airflow_hook(self) -> BaseHook:
        pass 

    @abstractmethod
    def _get_airflow_connection(self) -> Connection:
        pass 
