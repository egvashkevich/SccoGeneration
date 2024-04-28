import typing
from typing import List
import configparser

from importlib.resources import files

pos_to_insert_in_system = {
    'company_name': '[COMPANY]',
    'channel_name': '[CHANNEL]',
    'services': '[SERVICES]',
    'specific': '[SPECIFIC]'
}


class UserMessageWrapper:
    @staticmethod
    def handle_message(message: str):
        return {
            "role": "user",
            "content": message
        }

    @staticmethod
    def handle_messages(messages: List[str]):
        return [UserMessageWrapper.handle_message(message) for message in messages]


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
    basic = basic.replace(pos_to_insert_in_system['specific'], ', '.join(request['specific_features']))

    return basic
