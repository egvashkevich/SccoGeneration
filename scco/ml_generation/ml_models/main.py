import os
from typing import List

GIGACHAT_API_CLIENT_SECRET = os.environ.get('GIGACHAT_API_CLIENT_SECRET')


class MlClientInfo:
    current_message: str
    previous_messages: List[str]
    sender_attitude: List[str]


class OfferInfo:
    main_text: str


class MLModel:

    def generate_offer_text(self, client_info: MlClientInfo) -> OfferInfo:
        return OfferInfo()
