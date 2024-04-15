import os
from typing import List
from token_update import ChatAccessManager
from gigachat_gate import GigaChatAPIManager
import make_prompts
import configparser


class MLRequestInfo:
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

    def set_params(self, prompt_info):
        config = configparser.ConfigParser()
        config.read('configs/prompts.ini')

        system_content = make_prompts.make_system_prompt(prompt_info)
        print(system_content)

        self.system_prompts = [
            {
                'role': 'system',
                'content': system_content
            }
        ]

    def generate_offer_text(self, request_info: MLRequestInfo, cleint_info) -> OfferInfo:
        self.set_params(cleint_info)
        messages = self.system_prompts + \
            [UserMessageWrapper.handle_message(request_info.current_message)]
        response = self.gate.generate_request(messages)
        text_response = response.json()['choices'][0]['message']['content']
        return OfferInfo(text_response)
