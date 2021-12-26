"""Provides sanity check functions."""

from flask.app import Flask


def SanityCheckDomain(domain: str) -> bool:
    if not domain:
        return False
    if ';' in domain:
        return False
    if '/' in domain:
        return False
    return True

def SanityCheckEncryptedPassword(encrypted_password: str) -> bool:
    if not encrypted_password:
        return False
    if '/' in encrypted_password:
        return False
    return True