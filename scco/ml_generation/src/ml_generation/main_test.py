import ml_models.co_gen.api as ml_models_api

# TODO: expected API as below

model = ml_models_api.GenerateGateWrapper()

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

