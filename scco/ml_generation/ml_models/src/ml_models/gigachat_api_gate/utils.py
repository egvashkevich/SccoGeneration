from typing import List


class UserMessageWrapper:
    @staticmethod
    def handle_message(message: str):
        return {
            "role": "user",
            "content": "Сообщение от потенциального клиента:" + message
        }

    @staticmethod
    def handle_messages(messages: List[str]):
        return [UserMessageWrapper.handle_message(message) for message in messages]
