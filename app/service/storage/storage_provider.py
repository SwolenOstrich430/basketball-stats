from app.service.storage.igeneric_storage_provider import IGenericStorageProvider
from app.service.storage.istorage_provider import IStorageProvider
from app.service.config.config_provider import ConfigProvider

STORAGE_PREFIX = "storage"
BUCKETS_PREFIX = "buckets"
class StorageProvider(IGenericStorageProvider):
    def __init__(self):
        self._set_config_provider()

    def upload_file(self, bucket_identifier: str, file_name: str) -> bool:
        return self._get_provider().upload_file(
            self._get_bucket_name(bucket_identifier), 
            file_name
        )
    
    def download_file(self, bucket_identifier: str, file_name: str) -> str:
        return self._get_provider().download_file(
            self._get_bucket_name(bucket_identifier), 
            file_name
        )
    
    def file_exists(self, bucket_identifier: str, file_name: str) -> bool:
        return self._get_provider().file_exists(
            self._get_bucket_name(bucket_identifier), 
            file_name
        )
    
    def _get_bucket_name(self, bucket_identifier: str) -> str:
        return self._get_config_provider().get(
            STORAGE_PREFIX, BUCKETS_PREFIX, bucket_identifier
        )
        
    def _get_provider(self) -> IStorageProvider:
        StorageProvider()

    def _set_config_provider(self): 
        if not hasattr(self, 'config_provider') or \
            not self._get_config_provider:
            self.config_provider = ConfigProvider()
            
    def _get_config_provider(self) -> ConfigProvider:
        return self.config_provider
