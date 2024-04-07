import os
from typing import List
from token_update import ChatAccessManager
from gigachat_gate import GigaChatAPIManager

import configparser

class MlClientInfo:
    current_message: str
    previous_messages: List[str]
    sender_attitude: List[str]

class OfferInfo:
    def __init__(self, text):
        self.main_text = text
    main_text: str

class UserMessageWrapper:
    @staticmethod
    def handle_message(message: str):
        return {
          "role": "user",
            "content": message
        }

    @staticmethod
    def handle_messages(messages: List[str]):
        return [handle_message(message) for message in messages]

class GenerateGateWrapper:
    def __init__(self):
        self.gate = GigaChatAPIManager('configs/params.ini')

        config = configparser.ConfigParser()
        config.read('configs/prompts.ini')

        self.system_prompts = [
                {
                    'role':'system',
                    'content':config['PROMPTS']['SYSTEM']
                }
        ]

    def generate_offer_text(self, client_info: MlClientInfo) -> OfferInfo:
        messages = self.system_prompts + [UserMessageWrapper.handle_message(client_info.current_message)]
        response = self.gate.generate_request(messages)
        text_response = response.json()['choices'][0]['message']['content']
        return OfferInfo(text_response)
