import base64
import requests
import uuid
import json

class ChatAccessManager:
    '''
        Access for remote ml server.
    '''

    def __init__(self):
        self.set_credentials()

    def set_credentials(self):
        '''
            set client_id and secret
            (usually from environment)
        '''
        self.client_id = client_id
        self.secret = secret

        credentials = f'{self.client_id}:{self.secret}'
        self.encoded_credentials = base64.b64encode(
            credentials.encode('utf-8')
            ).decode('utf-8')

    def update_token(self, scope=default_scope):
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
            'scope': scope
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                data=payload,
                verify=False
                )
            self.access_token = response.json()['access_token']
            return response
        except requests.RequestException as e:
            print(f'Error: {str(e)}')
            return -1