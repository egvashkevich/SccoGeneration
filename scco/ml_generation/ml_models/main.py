import generation

import make_prompts


client = make_prompts.SystemPromptData()
client.company_name = 'Интеллект'
client.channel_name = 'Репетитор'
client.services = [
    'Английский (до уровня C2 и подготовка к экзаменам SAT, IELTS)',
    'Математика (олимпиадная и школьная программа)',
    'Физика (олимпиадная, школьная и вузовская программы)',
    'Испанский (до уровня B2)',
]
client.specific = [
    "Специалисты с 10 летним стажем",
    "Опыт работы с детьми всех возрастов",
]


model = generation.GenerateGateWrapper()
info = generation.MLRequestInfo()

info.current_message = "Подскажите хорошего репетиора по математике. Дочь не успевает за школьной программой. 9 класс. Физико-математическое направление"

ans = model.generate_offer_text(info, client)
print(ans.main_text)
