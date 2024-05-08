from ml_models.co_gen.matcher import Matcher


def parse_word(string, idx):
    end = idx
    while string[end] != ' ':
        end += 1
        if end >= len(string):
            break
    return string[idx:end]


class UserMessageHeuristics:
    def __init__(self):
        self.KEYWORD_MESSAGE_PAD = '. Важные инструменты: '
        self.matcher = Matcher()
        self.buff = dict

    def _handle_message(self, request, message_idx, keyword):
        if message_idx not in self.buff.keys:
            self.buff[message_idx] = True
            request[message_idx] += self.KEYWORD_MESSAGE_PAD
        request['messages'][message_idx] += keyword 
        
        for service in request['customer_services']:
            name, desc = service['service_name'], service['service_desc']
            if self.matcher.count_matches(keyword, name + desc) > 0:
                request['message'][i] += ''

    def __call__(self, request):
        whitelist = request['white_list']
        for i, message in enumerate(request['messages']):
            for keyword in whitelist:
                if self.matcher.count_matches(keyword, message):
                    self._handle_message_with_keyword(request, i, keyword)
