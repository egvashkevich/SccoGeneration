from typing import List

from importlib.resources import files

from ml_models.co_gen.gigachat_gate import GigaChatAPIManager
import ml_models.co_gen.make_prompts as make_prompts
import configparser as configparser


# class MLRequestInfo:
#     current_message: str
#     previous_messages: List[str]
#     sender_attitude: List[str]


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
        return [UserMessageWrapper.handle_message(message) for message in messages]


class GenerateGateWrapper:
    def __init__(self):
        config_path = str(
            files("ml_models").joinpath(
                "co_gen/configs/params.ini"
            )
        )
        self.gate = GigaChatAPIManager(config_path)

    def set_params(self, prompt_info):
        config = configparser.ConfigParser()
        config_path = str(
            files("ml_models").joinpath(
                "co_gen/configs/prompts.ini"
            )
        )
        config.read(config_path)

        system_content = make_prompts.make_system_prompt(prompt_info)
        print(system_content)

        self.system_prompts = [
            {
                'role': 'system',
                'content': system_content
            }
        ]

    def generate_offer_text(self, request_info) -> dict:
        client = make_prompts.SystemPromptData()
        client.company_name = request_info["company_name"]
        # TODO: for every message channel is separate (channel_ids)
        # TODO: rename client to customer
        client.channel_name = "???"
        # TODO: parse services (see crud data)
        client.services = [
            'Английский (до уровня C2 и подготовка к экзаменам SAT, IELTS)',
            'Математика (олимпиадная и школьная программа)',
            'Физика (олимпиадная, школьная и вузовская программы)',
            'Испанский (до уровня B2)',
        ]
        # TODO: parse tags and specific_features from crud
        client.specific = [
            "Специалисты с 10 летним стажем",
            "Опыт работы с детьми всех возрастов",
        ]

        self.set_params(client)
        messages = self.system_prompts + \
            [UserMessageWrapper.handle_message(request_info.current_message)]
        response = self.gate.generate_request(messages)
        text_response = response.json()['choices'][0]['message']['content']

        result = {
            "main_text": text_response,
        }

        return result
