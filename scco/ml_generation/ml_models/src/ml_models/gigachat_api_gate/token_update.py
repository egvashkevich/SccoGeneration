import os
import base64
import requests
import uuid

from importlib.resources import files
from dotenv import load_dotenv

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def load_local_env():
    dotenv_path = str(files("ml_models").joinpath(
        "gigachat_api_gate/api_token.secret.env"
    ))
    load_dotenv(dotenv_path)


class ChatAccessManager:
    def __init__(self):
        self.set_credentials()

    def set_credentials(self):
        '''
            set client_id and secret
            (usually from environment)
        '''
        print("Start construct access manager", flush=True)

        print("Load env variables (GIGACHAT_API)", flush=True)
        load_local_env()
        self.scope = os.environ.get('GIGACHAT_API_SCOPE')
        self.client_id = os.environ.get('GIGACHAT_API_CLIENT_ID')
        self.secret = os.environ.get('GIGACHAT_API_CLIENT_SECRET')

        credentials = f'{self.client_id}:{self.secret}'
        self.encoded_credentials = base64.b64encode(
            credentials.encode('utf-8')).decode('utf-8')

        self.access_token = None
        print("End build access manager", flush=True)

    def update_token(self):
        '''
            update access token
        '''
        rq_uid = str(uuid.uuid4())

        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': rq_uid,
            'Authorization': f'Basic {self.encoded_credentials}'
        }

        payload = {
            'scope': self.scope
        }
        print("Try get token update response", flush=True)
        try:
            response = requests.post(
                url, headers=headers, data=payload, verify=False)
            self.access_token = response.json()['access_token']
            return response
        except requests.RequestException as e:
            print('ERROR IN TOKEN UPDATING')
            print(f'Error: {str(e)}')
            raise e
