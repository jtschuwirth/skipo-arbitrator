import requests
import json
from base64 import b64encode
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class SkipoApiClient:
    def __init__(self, base_url, api_key, private_key_path):
        self.base_url = base_url
        self.api_key = api_key
        self.secret = self.load_private_key(private_key_path)

    def load_private_key(self, path):
        with open(Path(path), 'rb') as key_file:
            private_key = load_pem_private_key(
                key_file.read(),
                password=None,
            )
        return private_key

    @staticmethod
    def sort_object_keys(obj):
        return {key: obj[key] for key in sorted(obj)}

    def sign_message(self, message):
        signature = self.secret.sign(
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return b64encode(signature).decode('utf-8')

    def request(self, method, path, body=None, params=None, timeout=None):
        if body is None:
            body = {}
        sorted_body = json.dumps(
            self.sort_object_keys(body), separators=(',', ':'))
        message = f"{method} {path} {sorted_body}"
        signature = self.sign_message(message)
        headers = {
            "X-API-KEY": self.api_key,
            "X-SIGNATURE": signature
        }
        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            params=params,
            headers=headers,
            timeout=timeout,
            json=body
        )
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.RequestException as error:
            print(f"Error: {error.response.text}")
            return None