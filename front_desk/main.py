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

from storage.datastore import DatastoreStorage
from storage.storage import Storage

datastore_storage = DatastoreStorage()

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/store', methods=['POST'])
def store():
    """Stores the login information."""
    domain = request.form.get('domain')
    encrypted_password = request.form.get('encrypted_password')

    if not domain or not encrypted_password:
        return 'invalid input: <domain: {}; encrypted_password: {}>'.format(domain, encrypted_password), 400

    try:
        datastore_storage.Set(domain.encode(), encrypted_password.encode())
        return 'success', 200
    except Exception as err:
        return 'fail to store: {}'.format(err), 500


@app.route('/retrieve/<domain>')
def retrieve(domain: str):
    """Retrieves the requested login information."""
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
        domains = datastore_storage.List()
        return '\n'.join(domain.decode() for domain in domains), 200
    except Exception as err:
        return 'fail to list domains: {}'.format(err), 500


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
