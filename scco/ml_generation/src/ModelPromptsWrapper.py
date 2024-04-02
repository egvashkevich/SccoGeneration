from LLM_Manager import (
    LLM_Manager,
    add_user_message,
    extract_str_from_answer,
)


class ModelPromptsWrapper(LLM_Manager):
    def __init__(
            self,
            prompts=None,
            temperature=1,
            top_p=0.1,
            max_tokens=256,
            repetition_penalty=1):
        # TODO: принимать параметры наследника одной переменной мб
        super().__init__(temperature, top_p, max_tokens, repetition_penalty)
        if prompts is None:
            self.prompts = []
        else:
            self.prompts = prompts

    def generate_answer(self, message):
        prompts = add_user_message(self.prompts, message)
        ans = self.generate_request(prompts)
        return extract_str_from_answer(ans)
