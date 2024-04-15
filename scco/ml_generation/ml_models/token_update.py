import os
import base64
import requests
import uuid
from dotenv import load_dotenv

def load_local_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


class ChatAccessManager:
    def __init__(self):
        self.set_credentials()
    def set_credentials(self):
        '''
            set client_id and secret
            (usually from environment)
        '''
        load_local_env()
        self.scope = os.environ.get('GIGACHAT_API_SCOPE') # физ/юр лицо
        self.client_id = os.environ.get('GIGACHAT_API_CLIENT_ID')
        self.secret = os.environ.get('GIGACHAT_API_CLIENT_SECRET')
        
        credentials = f'{self.client_id}:{self.secret}'
        self.encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')        

        self.access_token = None

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
            'scope':self.scope
        }
    
        try:
            response = requests.post(url, headers=headers, data=payload, verify = False)
            self.access_token = response.json()['access_token']
            return response
        except requests.RequestException as e:
            print('ERROR IN UPDATER')
            print(f'Error: {str(e)}')
            return -1
