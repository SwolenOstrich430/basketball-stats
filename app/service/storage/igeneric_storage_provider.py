from abc import abstractmethod
from app.service.storage.istorage_provider import IStorageProvider
from app.service.config.iconfig_provider import IConfigProvider

class IGenericStorageProvider(IStorageProvider):
    
    @abstractmethod
    def upload_file(bucket_identifier: str, file_name: str) -> bool: 
        pass 

    @abstractmethod
    def download_file(bucket_identifier: str, file_name: str) -> str: 
        pass 

    @abstractmethod
    def file_exists(bucket_identifier: str, file_name: str) -> bool: 
        pass 

    @abstractmethod
    def _get_bucket_name(self, bucket_identifier: str) -> str:
        pass

    @abstractmethod
    def _get_provider(self) -> IStorageProvider:
        pass 
    
    @abstractmethod
    def _set_config_provider(self) -> IConfigProvider:
        pass 

    @abstractmethod
    def _get_config_provider(self) -> IConfigProvider:
        pass 