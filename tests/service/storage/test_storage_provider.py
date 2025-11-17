import pytest 
from flask import Flask 
from app.service.storage.storage_provider import StorageProvider
from app.service.config.config_provider import ConfigProvider

class TestStorageProvider():

    def setup_method(self):
        self.subject = StorageProvider()
    
    def test_get_bucket_throws_file_not_found_exception_if_supplied_bucket_prefix_isnt_defined(self, mocker):
        with pytest.raises(KeyError) as _:
            config_provider = ConfigProvider()
    
            mocker.patch.object(
                config_provider,
                '_get_config', 
                return_value={"one": 2}
            )

            mocker.patch.object(
                self.subject,
                '_get_config_provider',
                return_value=config_provider
            )
            
            self.subject._get_bucket_name("addfdsfjklasd")

    def test_get_bucket_throws_file_not_found_exception_if_supplied_bucket_prefix_returns_an_empty_string(self, mocker):
        with pytest.raises(KeyError) as _:
            config_provider = ConfigProvider()
    
            mocker.patch.object(
                config_provider,
                '_get_config', 
                return_value={"one": ""}
            )

            mocker.patch.object(
                self.subject,
                '_get_config_provider',
                return_value=config_provider
            )
            
            self.subject._get_bucket_name("one")