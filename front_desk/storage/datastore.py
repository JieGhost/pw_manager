from typing import List

from google.cloud import datastore

from storage.storage import Storage


class DatastoreStorage(Storage):
    def __init__(self, json_path: str = None) -> None:
        super().__init__()
        if json_path != None:
            self._client = datastore.Client.from_service_account_json(json_path)
        else:
            self._client = datastore.Client()
        self._kind = 'Entry'

    def Get(self, domain: bytes) -> bytes:
        key = self._client.key(self._kind, domain.decode())
        entity = self._client.get(key=key)
        if entity is None:
            raise KeyError('domain {} not found'.format(domain.decode()))
        return entity['encrypted_password']

    def Set(self, domain: bytes, encrypted_password: bytes) -> None:
        key = self._client.key(self._kind, domain.decode())
        entry = datastore.Entity(key=key)
        entry['domain'] = domain
        entry['encrypted_password'] = encrypted_password
        self._client.put(entry)

    def List(self) -> List[bytes]:
        domains = list()
        query = self._client.query(kind=self._kind)
        query_iter = query.fetch()
        for entity in query_iter:
            domains.append(entity['domain'])
        return domains
