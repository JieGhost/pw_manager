from abc import ABC, abstractmethod
from typing import List


class Storage(ABC):
    @abstractmethod
    def Get(self, domain: str) -> str:
        pass

    @abstractmethod
    def Set(self, domain: str, encrypted_password: str) -> None:
        pass

    @abstractmethod
    def List(self) -> List[str]:
        pass
