from abc import ABC, abstractmethod
from typing import List


class Storage(ABC):
    @abstractmethod
    def Get(self, domain: bytes) -> bytes:
        pass

    @abstractmethod
    def Set(self, domain: bytes, encrypted_password: bytes) -> None:
        pass

    @abstractmethod
    def List(self) -> List[bytes]:
        pass
