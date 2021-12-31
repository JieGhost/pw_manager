"""Defines various data models."""

class UserModel:
    def __init__(self, id: str, email: str) -> None:
        self._id = id
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email


# TODO: Add a wrapped key field:
# Randomly generated encryption key wrapped with user root key (master key)
class LoginModel:
    def __init__(self, domain: str, username: str, encrypted_password: bytes) -> None:
        self._domain = domain
        self._username = username
        self._encrypted_password = encrypted_password
    
    @property
    def domain(self) -> str:
        return self._domain
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def encrypted_password(self) -> bytes:
        return self._encrypted_password