# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, request
from flask_cors import CORS

from storage.datastore import DatastoreStorage
from utils.auth import AuthManager
from utils.sanity import SanityCheckDomain, SanityCheckEncryptedPassword

trusted_origins = [
    'https://passwordmanager-335804.firebaseapp.com.*',
    # TODO: remove after dev.
    'http://localhost:[0-9]+',
]

gcp_project_id = 'passwordmanager-335804'

datastore_storage = DatastoreStorage()
auth_manager = AuthManager(gcp_project_id)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
CORS(app, origins=trusted_origins)

@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/store', methods=['POST'])
def store():
    """Stores the login information."""
    try:
        auth_id = auth_manager.ExtractAndVerifyToken(request.headers)
    except Exception as err:
        return 'fail to authenticate: {}'.format(err), 401

    domain = request.form.get('domain')
    encrypted_password = request.form.get('encrypted_password')

    if not SanityCheckDomain(domain):
        return 'invalid domain: {}'.format(domain), 400

    if not SanityCheckEncryptedPassword(encrypted_password):
        return 'invalid encrypted password: {}'.format(encrypted_password), 400

    try:
        datastore_storage.Set(domain.encode(), encrypted_password.encode())
        return 'success', 200
    except Exception as err:
        return 'fail to store: {}'.format(err), 500


@app.route('/retrieve/<domain>')
def retrieve(domain: str):
    """Retrieves the requested login information."""
    try:
        auth_id = auth_manager.ExtractAndVerifyToken(request.headers)
    except Exception as err:
        return 'fail to authenticate: {}'.format(err), 401

    try:
        encrypted_password = datastore_storage.Get(domain.encode())
        return encrypted_password.decode(), 200
    except KeyError as err:
        return '{}'.format(err), 400
    except Exception as err:
        return 'fail to retrieve: {}'.format(err), 500


@app.route('/list_domains')
def list_domains():
    """List all the stored domains."""
    try:
        auth_id = auth_manager.ExtractAndVerifyToken(request.headers)
    except Exception as err:
        return 'fail to authenticate: {}'.format(err), 401

    try:
        domains = datastore_storage.List()
        return ';'.join(domain.decode() for domain in domains), 200
    except Exception as err:
        return 'fail to list domains: {}'.format(err), 500


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
