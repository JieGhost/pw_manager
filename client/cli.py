import argparse
import base64
import os
from typing import List

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from localfile import LocalFileStorage
from remote import RemoteStorage
from storage import Storage


def InitArgParser():
    parser = argparse.ArgumentParser(
        description='Weclome to password manager.')
    parser.add_argument('command', choices=['init', 'add', 'get', 'list'],
                        help='a command to run')
    parser.add_argument('--saltfilepath',
                        default=os.path.join(os.path.dirname(
                            __file__), '../data/salt'),
                        help='the path to the salt file')
    parser.add_argument('--local_mode', action='store_true',
                        help='wether to store the password locally')
    parser.add_argument('--remote_server', default='https://passwordmanager-335804.uk.r.appspot.com',
                        help='the address of the remote server')
    parser.add_argument('--datafilepath',
                        default=os.path.join(os.path.dirname(
                            __file__), '../data/raw_data'),
                        help='the path to the raw data file')
    parser.add_argument(
        '--rootkey', default='not_working_key', help='the root pass key')
    parser.add_argument(
        '--domain', help='the domain where the password is associated with')
    parser.add_argument('--password', help='the password to be stored')
    return parser


def InitPasswordManager(salt_file: str):
    salt = os.urandom(16)
    with open(salt_file, 'wb') as fp:
        fp.write(salt)


def GetSalt(salt_file: str) -> bytes:
    with open(salt_file, 'rb') as fp:
        salt = fp.read()
    return salt


class PasswordManager(object):
    def __init__(self, root_key: bytes, salt: bytes, storage: Storage) -> None:
        super().__init__()

        self._root_key = root_key
        self._salt = salt
        self._storage = storage

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=390000,
        )
        self._encryption_key = base64.urlsafe_b64encode(
            kdf.derive(self._root_key))
        self._f = Fernet(self._encryption_key)

    def RetrievePassword(self, domain: str) -> str:
        encrypted_password = self._storage.Get(domain)
        return self._f.decrypt(encrypted_password.encode()).decode()

    def StorePassword(self, domain: str, password: str) -> None:
        self._storage.Set(domain, self._f.encrypt(password.encode()).decode())

    def ListDomains(self) -> List[str]:
        return self._storage.List()


def main():
    parser = InitArgParser()
    args = parser.parse_args()
    if args.command == 'init':
        InitPasswordManager(args.saltfilepath)
        return

    if args.local_mode:
        storage = LocalFileStorage(args.datafilepath)
    else:
        storage = RemoteStorage(args.remote_server)

    pwm = PasswordManager(args.rootkey.encode(),
                          GetSalt(args.saltfilepath), storage)
    if args.command == 'add':
        pwm.StorePassword(args.domain, args.password)
    elif args.command == 'get':
        print(pwm.RetrievePassword(args.domain))
    elif args.command == 'list':
        print('\n'.join(pwm.ListDomains()))


if __name__ == '__main__':
    main()
