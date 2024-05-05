from ml_models.gigachat_api_gate.api import GenerateGateWrapper

from ml_models.gigachat_api_gate.utils import UserMessageWrapper
import configparser as configparser

from overrides import override


def make_system_prompt(request, path_to_conf):
    config = configparser.ConfigParser()
    config.read(path_to_conf)
    basic = config['PROMPTS']['basic_system']
    return basic


class KeyWordsGenerator(GenerateGateWrapper):
    def __init__(self):
        cfg_path = 'white_list_generation/configs'
        super().__init__(cfg_path)

    def _make_key_word_prompt(self, request):
        whitelist_features = []
        for service in request['customer_services']:
            whitelist_features.append(service['service_name'])
            whitelist_features.append(service['service_desc'])
        whitelist_features = ', '.join(whitelist_features)

        return whitelist_features

    @override
    def generate(self, request) -> dict:
        self._set_system_params(request, make_system_prompt)
        features = self._make_key_word_prompt(request)
        messages = self.system_prompts + \
            [UserMessageWrapper.handle_message(features)]
        response = self.gate.generate_request(messages)
        text_response = response.json()['choices'][0]['message']['content']
        result = {
            "whitelist": text_response,
        }
        return result
