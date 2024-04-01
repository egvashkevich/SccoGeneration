import base64
import requests
import uuid
import json
from ChatAccessManager import ChatAccessManager


def extract_str_from_answer(ans):
    return ans.json()['choices'][0]['message']['content']


def add_user_message(prompts, message):
    return prompts + [{'role': 'user', 'content': message}]


categories = [
    'Геймдизайн',

    'Ассеты',

    'Создание сценария',

    'Геймификация',
]

positive_answers = ['Yes', 'YES', 'Да', 'ДА']


class LLM_Manager:
    def __init__(
            self,
            temperature=1,
            top_p=0.1,
            max_tokens=256,
            repetition_penalty=1):
        self.access_manager = ChatAccessManager()
        self.model_name = "GigaChat"

        self.temperature = temperature
        self.top_p = 0.1
        self.max_tokens = 256
        self.repetition_penalty = 1

    def generate_request(self, messages):
        self.access_manager.update_token()
        # TODO: делать раз в полчаса (время expired'а токена)
        '''
            messages - list of dict
        '''
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        # TODO: вынести в константы

        payload = json.dumps(
            {
                'model': self.model_name,
                'messages': messages,
                'temperature': self.temperature,
                # чем выше, тем более случайные ответы
                'top_p': self.top_p,  # отвечает за разнообразие
                'n': 1,  # число возвращаемых ответов
                'stream': False,
                'max_tokens': self.max_tokens,  # макс число токенов в ответе
                'repetition_penalty': self.repetition_penalty
                # Штраф за повторы
            }
        )
        # TODO: Абстрагировать параметры от передачи в функцию
        # чтобы упростить настроку под задачу

        # TODO: Добавить историю (few shots по факту)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_manager.access_token}'
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            verify=False
            )

        return response
