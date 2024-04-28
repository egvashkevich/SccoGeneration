from typing import List

from importlib.resources import files

import ml_models.co_gen.make_prompts as make_prompts
from ml_models.co_gen.make_prompts import UserMessageWrapper
import configparser as configparser
from ml_models.co_gen.gigachat_gate import GigaChatAPIManager


class GenerateGateWrapper:
    def __init__(self):
        self.params_config_path = str(
            files("ml_models").joinpath(
                "co_gen/configs/params.ini"
            )
        )
        self.system_prompt_config_path = str(
            files("ml_models").joinpath(
                'co_gen/configs/prompts.ini'
            ) 
        )
        self.gate = GigaChatAPIManager(self.params_config_path)

    def _set_system_params(self, request):
        system_content = make_prompts.make_system_prompt(request, self.system_prompt_config_path)

        self.system_prompts = [
            {
                'role': 'system',
                'content': system_content
            }
        ]

    def generate_offer_text(self, request) -> dict:
        self._set_system_params(request)
        messages = self.system_prompts + \
            UserMessageWrapper.handle_messages(request['messages'])
        # TODO: for every message channel is separate (channel_ids)
        response = self.gate.generate_request(messages)
        text_response = response.json()['choices'][0]['message']['content']
        result = {
           "main_text": text_response,
        }
        return result
