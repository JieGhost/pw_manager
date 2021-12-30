"""Provides auth related methods."""

# TODO: Define parsed object and use google auth library.

def VerifyAndParseToken(request_headers):
    if 'Authorization' not in request_headers:
        raise KeyError('Expect "Authorization" in the request header')
    token_type, token = request_headers.get('Authorization').split(None, 1)
    if token_type != 'Bearer':
        raise TypeError('Expect token type: {}; got {}'.format('Bearer', token_type))
    return token