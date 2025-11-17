import pytest 
from app.service.storage.storage_provider import StorageProvider
from app.service.config.config_provider import ConfigProvider

class TestStorageProvider():

    def setup_method(self):
        self.subject = StorageProvider()
        self.bucket_identifier = "blop"
        self.bucket_name = "blah"
        self.file_name = "bloop"
        self.local_path = "ham"
    
    def test_upload_file_passes_bucket_and_file_name_to_provider_implementation(self, mocker):
        provider = mocker.Mock()

        mocker.patch.object(
            self.subject, 
            '_get_provider',
            return_value=provider 
        )

        mock_method = mocker.patch.object(
            self.subject, 
            '_get_bucket_name',
            return_value=self.bucket_name 
        )

        self.subject.upload_file(
            self.bucket_identifier,
            self.file_name
        )

        mock_method.assert_called_with(self.bucket_identifier)
        provider.upload_file.assert_called_with(
            self.bucket_name,
            self.file_name
        )

    def test_download_file_passes_bucket_and_file_name_to_provider_implementation(self, mocker):
        provider = mocker.Mock()

        mocker.patch.object(
            self.subject, 
            '_get_provider',
            return_value=provider 
        )

        mock_method = mocker.patch.object(
            self.subject, 
            '_get_bucket_name',
            return_value=self.bucket_name 
        )

        self.subject.download_file(
            self.bucket_identifier,
            self.file_name,
            self.local_path
        )

        mock_method.assert_called_with(self.bucket_identifier)
        provider.download_file.assert_called_with(
            self.bucket_name,
            self.file_name,
            self.local_path
        )

    def test_bucket_exists_passes_bucket_and_file_name_to_provider_implementation(self, mocker):
        provider = mocker.Mock()

        mocker.patch.object(
            self.subject, 
            '_get_provider',
            return_value=provider 
        )

        mock_method = mocker.patch.object(
            self.subject, 
            '_get_bucket_name',
            return_value=self.bucket_name 
        )

        self.subject.bucket_exists(
            self.bucket_identifier
        )

        mock_method.assert_called_with(self.bucket_identifier)
        provider.bucket_exists.assert_called_with(
            self.bucket_name
        )

    def test_download_file_passes_bucket_and_file_name_to_provider_implementation(self, mocker):
        provider = mocker.Mock()

        mocker.patch.object(
            self.subject, 
            '_get_provider',
            return_value=provider 
        )

        mock_method = mocker.patch.object(
            self.subject, 
            '_get_bucket_name',
            return_value=self.bucket_name 
        )

        self.subject.file_exists(
            self.bucket_identifier,
            self.file_name
        )

        mock_method.assert_called_with(self.bucket_identifier)
        provider.file_exists.assert_called_with(
            self.bucket_name,
            self.file_name
        )

    def test_get_bucket_key_error_if_supplied_bucket_prefix_isnt_defined(self, mocker):
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

    def test_get_bucket_throws_key_error_if_supplied_bucket_prefix_returns_an_empty_string(self, mocker):
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