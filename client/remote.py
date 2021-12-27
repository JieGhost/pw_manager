import requests
from typing import List

from storage import Storage


class RemoteStorage(Storage):
    def __init__(self, remote_server: str) -> None:
        super().__init__()
        self._remote_server = remote_server
        self._retrieve_url = '{}/{}'.format(self._remote_server, 'retrieve')
        self._store_url = '{}/{}'.format(self._remote_server, 'store')
        self._list_domains_url = '{}/{}'.format(self._remote_server, 'list_domains')

    def Get(self, domain: str) -> str:
        r = requests.get('{}/{}'.format(self._retrieve_url, domain))
        r.raise_for_status()
        return r.text

    def Set(self, domain: str, encrypted_password: str) -> None:
        data = {'domain': domain, 'encrypted_password': encrypted_password}
        r = requests.post(self._store_url, data=data)
        r.raise_for_status()

    def List(self) -> List[str]:
        r = requests.get(self._list_domains_url)
        r.raise_for_status()
        return r.text.strip().split(';')