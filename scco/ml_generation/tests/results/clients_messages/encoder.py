import json
num = 6

with open(f'clients_messages_{num}.txt', 'r', encoding='utf-8') as f:
    d = json.load(f)
    print(d['messages'][0])
