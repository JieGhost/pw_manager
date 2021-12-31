from abc import ABC, abstractmethod
from typing import List

from storage.model import LoginModel, UserModel

# TODO: we can potentially add namespace param for different login providers.
class Storage(ABC):
    @abstractmethod
    def Set(self, user: UserModel, login: LoginModel) -> None:
        pass

    @abstractmethod
    def Get(self, user_id: str, domain: str) -> LoginModel:
        pass

    @abstractmethod
    def List(self, user_id: str) -> List[str]:
        pass
