import boto3
from botocore.exceptions import ClientError
from qa_core.qa_core_settings import QaCoreSettings


class S3client:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=QaCoreSettings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=QaCoreSettings.AWS_SECRET_ACCESS_KEY,
        )

    def file_exist(self, bucket, prefix):
        """
        Метод проверки на существование файла в хранилище
        :param bucket: Название s3 хранилища
        :param prefix: Префикс имени файла
        :return: True or False
        """
        try:
            self.s3_client.head_object(Bucket=bucket, Key=prefix)
        except ClientError:
            # Not found
            return False
        return True

    def upload_file(self, file_name, bucket, object_name):
        """
        Метод загрузки файла в s3 хранилище
        :param file_name: Префикс имени файла
        :param bucket: Название s3 хранилища
        :param object_name: Название объекта в хранилище
        """
        self.s3_client.upload_file(file_name, bucket, object_name)

    def download_file(self, bucket, file_name, object_name):
        """
        Метод скачивания файла из s3 хранилища
        :param bucket: Название s3 хранилища
        :param file_name: Префикс имени файла
        :param object_name: Название объекта в хранилище
        """
        self.s3_client.download_file(bucket, file_name, object_name)

    # Метод удаления одного файла из хранилища по префиксу изображения
    def delete_file(self, bucket, file_path):
        self.s3_client.delete_object(Bucket=bucket, Key=file_path)
