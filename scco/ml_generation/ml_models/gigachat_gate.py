from token_update import ChatAccessManager
import json
import requests
import configparser

class GigaChatAPIManager:
    def __init__(self, path_to_cfg : str):
        """
            path_to_cfg - конфиг с параметрами модели
        """
        config = configparser.ConfigParser()
        config.read(path_to_cfg)

        self.model_name = config['MODEL']['name']
        self.temperature = float(config['MODEL']['temperature'])
        self.top_p = float(config['MODEL']['top_p'])
        self.max_tokens = int(config['MODEL']['max_tokens'])
        self.repetition_penalty = float(config['MODEL']['repetition_penalty'])

        self.access_manager = ChatAccessManager()
    
    def _try_generate_request(self, messages):
        '''
            messages - list of dict
            there no token updating logic
        '''
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps({
            'model':self.model_name,
            'messages': messages,
            'temperature':self.temperature,
            'top_p':self.top_p,
            'n':1,
            'stream':False,
            'max_tokens':self.max_tokens,
            'repetition_penalty':self.repetition_penalty
        })
        
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': f'Bearer {self.access_manager.access_token}'
        }

        response = requests.request("POST", url, headers = headers, data = payload, verify=False)
        return response

    def generate_request(self, messages):
        self.access_manager.update_token()
        response = self._try_generate_request(messages)
        return response
