from app.service.storage.igeneric_storage_provider import IGenericStorageProvider
from app.service.storage.istorage_provider import IStorageProvider
from app.service.config.config_provider import ConfigProvider
from app.service.storage.gcp.google_storage_provider import GoogleStorageProvider

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
    
    def download_file(
        self, 
        bucket_identifier: str, 
        storage_path: str, 
        local_path: str
    ):
        return self._get_provider().download_file(
            self._get_bucket_name(bucket_identifier), 
            storage_path,
            local_path
        )
    
    def bucket_exists(self, bucket_identifier: str) -> bool:
        return self._get_provider().bucket_exists(
            self._get_bucket_name(bucket_identifier)
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
    
    # returning this for now: can add actual factory methods 
    # when they're needed 
    def _get_provider(self) -> IStorageProvider:
        return GoogleStorageProvider()

    def _set_config_provider(self): 
        if not hasattr(self, 'config_provider') or \
            not self._get_config_provider:
            self.config_provider = ConfigProvider()
            
    def _get_config_provider(self) -> ConfigProvider:
        return self.config_provider
