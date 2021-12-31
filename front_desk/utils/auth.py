"""Provides auth related methods."""

from typing import Any, Mapping
from google.auth.transport import requests
from google.oauth2 import id_token

# TODO: Define parsed object and use google auth library.

class AuthManager:
    def __init__(self, project_id: str) -> None:
        self._project_id = project_id
        self._auth_header = 'Authorization'
        self._auth_type = 'Bearer'
    
    def _extract_token(self, request_headers) -> str:
        if self._auth_header not in request_headers:
            raise KeyError('Expect "{}" in the request header'.format(self._auth_header))
        token_type, token = request_headers.get(self._auth_header).split(None, 1)
        if token_type != self._auth_type:
            raise TypeError('Expect token type: {}; got {}'.format(self._auth_type, token_type))
        return token
    
    def _verify_token(self, raw_token: str) -> Mapping[str, Any]:
        request = requests.Request()
        # TODO: add more verification
        return id_token.verify_firebase_token(raw_token, request)
        
    def ExtractAndVerifyToken(self, request_headers):
       raw_token = self._extract_token(request_headers)
       return self._verify_token(raw_token)