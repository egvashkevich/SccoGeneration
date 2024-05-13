from typing import List

from importlib.resources import files

import ml_models.gigachat_api_gate.utils as utils
from ml_models.gigachat_api_gate.utils import UserMessageWrapper
import configparser as configparser
from ml_models.gigachat_api_gate.gigachat_gate import GigaChatAPIManager


class GenerateGateWrapper:
    def __init__(self, params_config_path, system_prompt_config_path):

        self.params_config_path = params_config_path
        self.system_prompt_config_path = system_prompt_config_path
        self.gate = GigaChatAPIManager(self.params_config_path)

    def _set_system_params(self, request, make_system_prompt):
        system_content = make_system_prompt(
            request, self.system_prompt_config_path)

        self.system_prompts = [
            {
                'role': 'system',
                'content': system_content
            }
        ]

    def generate(self, request) -> dict:
        """
            You need to override it

            You need to use:
                -self._set_system_params(request, make_prompt_func)
                to set system prompt from configs

                -self.gate.generate_request(...)
                to make GigaChat response from prompt

            You can use:
                - UserMessageWrapper to add user message into prompt
                - .json()['choises'][0]['message']['content'] 
                to extract text from GigaChat response

            Recomendation:
                Please use decorator @override
        """
        pass
