from Levenshtein import distance
import re

#default: all possible punctuation
def split_by_regex(text, regex):
    normalize_text = re.sub(regex, '', text)
    return normalize_text.split(' ')

class DictOccurrenceManager:
    def __init__(self, dictionary : set):
        self.dictionary = dictionary
        self.punctuation_regex = '[^\w\s]'

    # Time ~ len(message)
    def check_exact_occurrence(self, message):
        splitted_message = split_by_regex(message, self.punctuation_regex)
        for word in splitted_message:
            if len(word)==0: #split can return empty word between spaces
                continue
            if word in self.dictionary:
                return True
        return False

    # error == k <=> Levenshtein dist == k
    # Time ~ O(D*n^2), where n is average len(word), D = len(dict)
    def check_occurrence_with_errors(self, message, errors_num): # <= errors_num errors
        splitted_message = split_by_regex(message, self.punctuation_regex)
        for word in splitted_message:
            if len(word) < errors_num:
                continue
            for dict_word in self.dictionary:
                if distance(dict_word, word) <= errors_num:
                    return True
        return False
        

t = DictOccurrenceManager(['Вакансия', 'Яблоко'])
print(t.check_occurrence_with_errors('Вакансииииииии !!!!', 2))
