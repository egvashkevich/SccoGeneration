from typing import List


class UserMessageWrapper:
    @staticmethod
    def handle_message(message: str):
        return {
            "role": "user",
            "content": message
        }

    @staticmethod
    def handle_messages(messages: List[str]):
        print("Start pack messages", flush=True)
        res = [UserMessageWrapper.handle_message(message) for message in messages]
        print("End pack messages", flush=True)
        return res
