import os
from typing import Dict, List, Tuple

from storage import Storage


class LocalFileStorage(Storage):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self._file_path = file_path
        self._entries = dict()

    def Get(self, domain: str) -> Tuple[str, str]:
        m = self._LoadFile()
        if domain not in m:
            raise KeyError('domain {} not found'.format(domain))
        return m[domain]

    def Set(self, domain: str, username: str, encrypted_password: str) -> None:
        m = self._LoadFile()
        m[domain] = (username, encrypted_password)
        self._WriteFile(m)

    def List(self) -> List[str]:
        m = self._LoadFile()
        return m.keys()

    def _LoadFile(self) -> Dict[str, Tuple[str, str]]:
        if not os.path.exists(self._file_path):
            return dict()

        with open(self._file_path, 'rb') as fp:
            entries = fp.readlines()

        m = dict()
        for entry in entries:
            if len(entry) == 0:
                continue
            domain, username, encrypted_password = entry.strip().split(b':')
            m[domain.decode()] = (username.decode(), encrypted_password.decode())

        return m

    def _WriteFile(self, m: Dict[str, Tuple[str, str]]) -> None:
        with open(self._file_path, 'wb') as fp:
            for domain, (username, encrypted_password) in m.items():
                fp.write(
                    b':'.join([domain.encode(), username.encode(), encrypted_password.encode()]))
                fp.write(b'\n')
