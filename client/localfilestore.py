import os
from typing import Dict, List

from storage import Storage


class LocalFileStorage(Storage):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self._file_path = file_path
        self._entries = dict()

    def Get(self, domain: bytes) -> bytes:
        m = self._LoadFile()
        if domain not in m:
            raise KeyError('domain {} not found'.format(domain.decode()))
        return m[domain]

    def Set(self, domain: bytes, encrypted_password: bytes) -> None:
        m = self._LoadFile()
        m[domain] = encrypted_password
        self._WriteFile(m)

    def List(self) -> List[bytes]:
        m = self._LoadFile()
        return m.keys()

    def _LoadFile(self) -> Dict[bytes, bytes]:
        if not os.path.exists(self._file_path):
            return dict()

        with open(self._file_path, 'rb') as fp:
            entries = fp.readlines()

        m = dict()
        for entry in entries:
            if len(entry) == 0:
                continue
            domain, encrypted_password = entry.strip().split(b':')
            m[domain] = encrypted_password

        return m

    def _WriteFile(self, m: Dict[bytes, bytes]) -> None:
        with open(self._file_path, 'wb') as fp:
            for domain, encrypted_password in m.items():
                fp.write(b':'.join([domain, encrypted_password]))
                fp.write(b'\n')
