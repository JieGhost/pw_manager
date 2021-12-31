from typing import List

from google.cloud import datastore

from storage.model import LoginModel, UserModel
from storage.storage import Storage


class DatastoreStorage(Storage):
    def __init__(self, json_path: str = None) -> None:
        super().__init__()
        if json_path != None:
            self._client = datastore.Client.from_service_account_json(
                json_path)
        else:
            self._client = datastore.Client()
        self._user_kind = 'User'
        self._login_kind = 'Login'

    def Set(self, user: UserModel, login: LoginModel) -> None:
        user_key = self._client.key(self._user_kind, user.id)
        if self._client.get(key=user_key) == None:
            user_entry = datastore.Entity(key=user_key)
            user_entry['email'] = user.email
            self._client.put(user_entry)

        login_key = self._client.key(
            self._login_kind, login.domain, parent=user_key)
        login_entry = datastore.Entity(key=login_key)
        login_entry['domain'] = login.domain
        login_entry['username'] = login.username
        login_entry['encrypted_password'] = login.encrypted_password
        self._client.put(login_entry)

    def Get(self, user_id: str, domain: str) -> LoginModel:
        user_key = self._client.key(self._user_kind, user_id)
        login_key = self._client.key(self._login_kind, domain, parent=user_key)
        login_entry = self._client.get(key=login_key)
        if login_entry is None:
            raise KeyError('domain {} not found'.format(domain.decode()))
        login = LoginModel(domain=login_entry['domain'],
                           username=login_entry['username'],
                           encrypted_password=login_entry['encrypted_password'])
        return login

    def List(self, user_id: str) -> List[str]:
        domains = list()
        user_key = self._client.key(self._user_kind, user_id)
        query = self._client.query(kind=self._login_kind, ancestor=user_key)
        query_iter = query.fetch()
        for entry in query_iter:
            domains.append(entry['domain'])
        return domains
