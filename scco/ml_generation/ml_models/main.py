import generation

# example
model = generation.GenerateGateWrapper()
info = generation.MlClientInfo()
info.current_message = "Добрый день, мне нужен разработчик на Питоне, \
    для разработки сайта под интернет-магазин"

ans = model.generate_offer_text(info)
print(ans.main_text)
