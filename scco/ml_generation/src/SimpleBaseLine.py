from ModelPromptsWrapper import ModelPromptsWrapper
from LLM_Manager import (
    categories,
    positive_answers,
)


class SimpleBaseline:
    def __init__(self):
        reduction_prompts = [{
            'role': 'system',
            'content': 'Выдели из сообщений главное'
        }]
        self.reduction_model = ModelPromptsWrapper(
            reduction_prompts,
            temperature=2,
            top_p=0.05,
            max_tokens=128
        )

        classify_prompts = [{
            'role': 'system',
            'content': f"Нужна ли отправителю одна из данных услуг: {'; '.join(categories)}, \
            Отвечай на русском языке в формате (Да/Нет)"
        }]
        self.classify_model = ModelPromptsWrapper(
            classify_prompts,
            temperature=0.5,
            top_p=0.05,
        )

    def need_generate_cp(self, message):
        red_ans = self.reduction_model.generate_answer(message)
        classif_ans = self.classify_model.generate_answer(message)
        return classif_ans in positive_answers
