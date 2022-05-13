# minio_client

from minio import Minio


class minio_client():
    def __init__(self, config: dict):
        self._alias = config['alias']
        self._endpoint = config['endpoint']
        self._access_key = config['access_key']
        self._secret_key = config['secret_key']
        self._secure = True if config['secure'] == 'Y' else False

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def access_key(self) -> str:
        return self._access_key

    @property
    def secret_key(self) -> str:
        return self._secret_key

    @property
    def secure(self) -> bool:
        return self._secure

    def get_client(self) -> Minio:
        client = Minio(endpoint=self._endpoint,
                       access_key=self._access_key,
                       secret_key=self._secret_key,
                       secure=self._secure)
        return client
