from ml_models.gigachat_api_gate.api import GenerateGateWrapper

from ml_models.gigachat_api_gate.utils import UserMessageWrapper
import configparser as configparser

from overrides import override

pos_to_insert_in_system = {
    'company_name': '[COMPANY]',
    'channel_name': '[CHANNEL]',
    'services': '[SERVICES]',
    'specific': '[SPECIFIC]',
}


def parse_custormer_services(request: dict):
    res_list = []
    for service in request['customer_services']:
        name, desc = service['service_name'], service['service_desc']
        res_list.append(name + f'({desc})')
    return ', '.join(res_list)


def make_system_prompt(request, path_to_conf):
    config = configparser.ConfigParser()
    config.read(path_to_conf)

    basic = config['PROMPTS']['basic_system']

    basic = basic.replace(
        pos_to_insert_in_system['company_name'], request['company_name'])
    basic = basic.replace(
        pos_to_insert_in_system['channel_name'], request['channel_ids'][0])
    basic = basic.replace(
        pos_to_insert_in_system['services'], parse_custormer_services(request))
    basic = basic.replace(pos_to_insert_in_system['specific'], ', '.join(
        request['specific_features']))

    return basic


class SCCOGenerator(GenerateGateWrapper):
    def __init__(self):
        cfg_path = 'co_gen/configs'
        super().__init__(cfg_path)

    @override
    def generate(self, request) -> dict:
        self._set_system_params(request, make_system_prompt)
        messages = self.system_prompts + \
            UserMessageWrapper.handle_messages(request['messages'])
        # TODO: for every message channel is separate (channel_ids)
        response = self.gate.generate_request(messages)
        text_response = response.json()['choices'][0]['message']['content']
        result = {
            "main_text": text_response,
        }
        return result
