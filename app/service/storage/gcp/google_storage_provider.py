from google.cloud import storage
from pathlib import Path

from app.service.storage.istorage_provider import IStorageProvider

class GoogleStorageProvider(IStorageProvider):
    def __init__(self):
        self._set_client()
    
    def upload_file(self, bucket_name: str, storage_path: str):
        blob = self._get_blob(bucket_name, storage_path)
        blob.upload_from_file_name(storage_path)
        
        assert blob.exists()
    
    def download_file(
        self, 
        bucket_name: str, 
        storage_path: str,
        local_path: str
    ):
        assert self.file_exists(bucket_name, storage_path)
        blob = self._get_blob(bucket_name, storage_path)
        blob.download_to_filename(local_path)
        
        _local_path = Path(local_path)
        assert _local_path.exists()

    def bucket_exists(self, bucket_name: str) -> bool:
        return self._get_bucket(bucket_name).exists()
    
    def file_exists(self, bucket_name: str, file_name: str) -> bool:
        return super().file_exists(file_name)
    
    def _get_blob(self, bucket_name: str, file_name: str):
        bucket = self._get_bucket(bucket_name)
        assert bucket.exists()

        return bucket.blob(file_name)
    
    def _get_bucket(self, bucket_name: str) -> storage.Bucket:
        return self._get_client().get_bucket(bucket_name)

    def _set_client(self) -> storage.Client:
        self.client = storage.Client()
    
    def _get_client(self) -> storage.Client:
        return self.client