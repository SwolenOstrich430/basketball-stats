import pytest
from pathlib import Path
import os 

from app.service.storage.gcp.google_storage_provider import GoogleStorageProvider

class TestGoogleStorageProvider():
    
    def setup_method(self):
        self.subject = GoogleStorageProvider()
        self.storage_path = "adsfafd"
        self.bucket_name = "asdf"
        self.local_path = "asdfff"

    def test_upload_file_uploads_file_to_storage_path(self, mocker):
        mock_blob = mocker.Mock()

        mock_method = mocker.patch.object(
            self.subject,
            '_get_blob',
            return_value=mock_blob
        )
        mock_blob.exists.return_value = True

        self.subject.upload_file(self.bucket_name, self.storage_path)

        mock_method.assert_called_with(self.bucket_name, self.storage_path)

        mock_blob.upload_from_file_name.assert_called_with(
            self.storage_path
        )

    def test_upload_file_uploads_file_to_storage_path(self, mocker):
        mock_blob = mocker.Mock()

        mock_method = mocker.patch.object(
            self.subject,
            '_get_blob',
            return_value=mock_blob
        )
        mock_blob.exists.return_value = True

        self.subject.upload_file(self.bucket_name, self.storage_path)

        mock_method.assert_called_with(self.bucket_name, self.storage_path)

        mock_blob.upload_from_file_name.assert_called_with(
            self.storage_path
        )

    def test_upload_file_throws_assertion_error_if_file_does_not_exist_after_upload(
        self, mocker
    ):
        mock_blob = mocker.Mock()

        mocker.patch.object(
            self.subject,
            '_get_blob',
            return_value=mock_blob
        )

        mock_blob.exists.return_value = False

        with pytest.raises(AssertionError) as _:
            self.subject.upload_file(self.bucket_name, self.storage_path)

    def test_download_file_throws_assertion_error_if_file_doesnt_already_exist(
        self,
        mocker
    ):
        
        mock_method = mocker.patch.object(
            self.subject,
            'file_exists',
            return_value=False
        )

        with pytest.raises(AssertionError) as _:
            self.subject.download_file(
                self.bucket_name, self.storage_path, self.local_path
            )
            mock_method.assert_called_with(self.bucket_name, self.storage_path)

    def test_download_file_throws_assertion_error_file_doesnt_exist_after_download(
        self,
        mocker
    ):
        mock_blob = mocker.Mock()

        mock_file_exists = mocker.patch.object(
            self.subject,
            'file_exists',
            return_value=True
        )

        mock_get_blob = mocker.patch.object(
            self.subject,
            '_get_blob',
            return_value=mock_blob
        )

        with pytest.raises(AssertionError) as _:
            self.subject.download_file(
                self.bucket_name, self.storage_path, self.local_path
            )
            mock_file_exists.assert_called_with(
                self.bucket_name, self.storage_path
            )
            mock_get_blob.assert_called_with(
                self.bucket_name, self.storage_path
            )
            mock_blob.download_to_filename.assert_called_with(
                self.local_path
            )

    def test_download_file_does_not_throw_assertion_error_if_file_exists_after_download(
        self,
        mocker
    ):

        
        mock_blob = mocker.Mock()

        mock_file_exists = mocker.patch.object(
            self.subject,
            'file_exists',
            return_value=True
        )

        mock_get_blob = mocker.patch.object(
            self.subject,
            '_get_blob',
            return_value=mock_blob
        )

        try:
            with open(self.local_path, "w") as file:
                file.write(self.local_path)

            self.subject.download_file(
                self.bucket_name, 
                self.storage_path, 
                self.local_path
            )
        finally:
            os.remove(self.local_path)

        mock_file_exists.assert_called_with(
            self.bucket_name, self.storage_path
        )
        mock_get_blob.assert_called_with(
            self.bucket_name, self.storage_path
        )
        mock_blob.download_to_filename.assert_called_with(
            self.local_path
        )

    def test_bucket_exists_returns_true_if_bucket_exists(self, mocker):
        mock_bucket = mocker.Mock()
        mock_bucket.exists.return_value = True 

        mocker.patch.object(
            self.subject,
            '_get_bucket',
            return_value=mock_bucket
        )

        assert self.subject.bucket_exists(self.bucket_name)
    
    def test_bucket_exists_returns_false_if_bucket_exists(self, mocker):
        mock_bucket = mocker.Mock()
        mock_bucket.exists.return_value = False 
        
        mocker.patch.object(
            self.subject,
            '_get_bucket',
            return_value=mock_bucket
        )

        assert not self.subject.bucket_exists(self.bucket_name)
    
    