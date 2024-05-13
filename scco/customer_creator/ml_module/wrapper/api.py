from typing import List

from importlib.resources import files

import make_prompts as make_prompts
from make_prompts import UserMessageWrapper
import configparser as configparser
from gigachat_gate import GigaChatAPIManager


class GenerateGateWrapper:
    def __init__(self, path_to_cfg, path_to_secrets):
        self.path_to_params_cfg = str(
            path_to_cfg+'/params.ini'
        )
        self.system_prompt_config_path = str(
            path_to_cfg+'/prompts.ini'
        )
        self.gate = GigaChatAPIManager(
            self.path_to_params_cfg, path_to_secrets)

    def _set_system_params(self, request):
        system_content = make_prompts.make_system_prompt(
            request, self.system_prompt_config_path)

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
