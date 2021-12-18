import argparse
import base64
import os
from typing import Iterator

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def InitArgParser():
    parser = argparse.ArgumentParser(
        description='Weclome to password manager.')
    parser.add_argument('command', choices=['init', 'add', 'get', 'list'],
                        help='a command to run')
    parser.add_argument('--filepath',
                        default=os.path.join(os.path.dirname(
                            __file__), 'data/raw_data'),
                        help='the path to the raw data file')
    parser.add_argument(
        '--rootkey', default='not_working_key', help='the root pass key')
    parser.add_argument(
        '--domain', help='the domain where the password is associated with')
    parser.add_argument('--password', help='the password to be stored')
    return parser


def InitPasswordManager(data_file: str):
    salt = os.urandom(16)
    with open(data_file, 'wb') as fp:
        fp.write(salt)


class PasswordManager(object):
    def __init__(self, data_file: str, root_key: str) -> None:
        super().__init__()
        self._data_file = data_file
        with open(self._data_file, 'rb') as fp:
            self._salt = fp.readline().strip()
            entries = fp.readlines()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=390000,
        )
        self._encryption_key = base64.urlsafe_b64encode(
            kdf.derive(root_key.encode()))
        self._f = Fernet(self._encryption_key)
        self._domain_pw_dict = dict()
        for domain_pw_entry in entries:
            # import pdb;pdb.set_trace()
            domain, pw = domain_pw_entry.strip().split(b':')
            # pdb.set_trace()
            self._domain_pw_dict[domain] = pw

    def Get(self, domain: str) -> str:
        domain_bytes = domain.encode()
        if (domain_bytes not in self._domain_pw_dict):
            raise KeyError('domain {} not found'.format(domain))

        pw = self._domain_pw_dict[domain_bytes]
        return self._f.decrypt(pw).decode()

    def Set(self, domain: str, pw: str) -> None:
        self._domain_pw_dict[domain.encode()] = self._f.encrypt(pw.encode())

    def Persist(self) -> None:
        with open(self._data_file, 'wb') as fp:
            fp.write(self._salt)
            for domain, pw in self._domain_pw_dict.items():
                fp.write(b'\n')
                fp.write(b':'.join([domain, pw]))

    def List(self) -> Iterator[str]:
        return (d.decode() for d in self._domain_pw_dict.keys())


def main():
    parser = InitArgParser()
    args = parser.parse_args()
    if args.command == 'init':
        InitPasswordManager(args.filepath)
        return

    pwm = PasswordManager(args.filepath, args.rootkey)
    if args.command == 'add':
        pwm.Set(args.domain, args.password)
        pwm.Persist()
    elif args.command == 'get':
        print(pwm.Get(args.domain))
    elif args.command == 'list':
        print('\n'.join(pwm.List()))


if __name__ == '__main__':
    main()
