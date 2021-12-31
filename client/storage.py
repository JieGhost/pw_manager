from abc import ABC, abstractmethod
from typing import List, Tuple


class Storage(ABC):
    @abstractmethod
    def Get(self, domain: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    def Set(self, domain: str, username: str, encrypted_password: str) -> None:
        pass

    @abstractmethod
    def List(self) -> List[str]:
        pass
