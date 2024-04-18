import api

# TODO: expected API as below

model = api.GenerateGateWrapper()

info = {
  "customer_id": "customer_1",
  "client_id": "client_1",
  "channel_ids": "client_1",
  "messages": [
    "Good morning.\nMy name is client_1.\nI need Python developers."
  ],
  "attitude": "arrogant",
  "company_name": "Company of customer 1",
  "features": [
    "feature_1",
    "feature_2"
  ],
  "customer_services": [
    {
      "service_name": "customer 1, service 1",
      "service_desc": "description 1"
    },
    {
      "service_name": "customer 1, service 2",
      "service_desc": "description 2"
    }
  ],
}

answer = model.generate_offer_text(info)

print(answer["main_text"])

########################################################################


# import os
# from importlib.resources import files
#
# from io import StringIO
#
# from dotenv import load_dotenv
#
# env_vars_text = files('co_gen_model').joinpath(
#     'api_token.secret.env'
# ).read_text()
#
#
# env_stream = StringIO(env_vars_text)
# load_dotenv(stream=env_stream)
#
# GIGACHAT_API_SCOPE = os.getenv('GIGACHAT_API_SCOPE')
#
#
# print(f"GIGACHAT_API_SCOPE = {GIGACHAT_API_SCOPE}")
#
#
# env_vars_text = files('co_gen_model').joinpath(
#     'configs/params.ini'
# )
#
# package_path = str(files('co_gen_model').joinpath('configs/params.ini'))
# print(f"package_path = {package_path}")

# load_dotenv(stream=env_stream)
