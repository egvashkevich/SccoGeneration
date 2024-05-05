from ml_models.gigachat_api_gate.api import GenerateGateWrapper

from ml_models.gigachat_api_gate.make_prompts import UserMessageWrapper
import configparser as configparser

from overrides import override

class SCCOGenerator(GenerateGateWrapper):
    def __init__(self, cfg_path):
        super().__init__(cfg_path)
    @override
    def generate_offer_text(self, request) -> dict:
        print('generate')
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
