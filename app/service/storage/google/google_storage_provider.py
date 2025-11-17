from app.service.storage.istorage_provider import IStorageProvider

class GoogleStorageProvider(IStorageProvider):
    def __init__(self):
        pass 

    def get_provider(self) -> IStorageProvider:
        return super().get_provider()
    
    def upload_file(bucket_name: str, file_name: str) -> bool:
        return super().upload_file(file_name)
    
    def download_file(bucket_name: str, file_name: str) -> str:
        return super().download_file(file_name)
    
    def file_exists(bucket_name: str, file_name: str) -> bool:
        return super().file_exists(file_name)