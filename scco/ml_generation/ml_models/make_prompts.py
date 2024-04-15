import typing
import configparser


class SystemPromptData:
    company_name: str
    channel_name: str
    services: list
    specific: list


pos_to_insert_in_system = {
    'company_name': '[COMPANY]',
    'channel_name': '[CHANNEL]',
    'services': '[SERVICES]',
    'specific': '[SPECIFIC]'
}


def make_system_prompt(system_prompt_info: SystemPromptData, path_to_conf='configs/prompts.ini'):
    config = configparser.ConfigParser()
    config.read(path_to_conf)

    basic = config['PROMPTS']['basic_system']

    basic = basic.replace(
        pos_to_insert_in_system['company_name'], system_prompt_info.company_name)
    basic = basic.replace(
        pos_to_insert_in_system['channel_name'], system_prompt_info.channel_name)
    basic = basic.replace(pos_to_insert_in_system['services'], ', '.join(
        system_prompt_info.services))
    basic = basic.replace(pos_to_insert_in_system['specific'], ', '.join(
        system_prompt_info.specific))

    return basic
