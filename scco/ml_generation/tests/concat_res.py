import json

for num in range(3, 16):
    with open(f'results/answers/ans{num}.txt', 'r') as f:
        ans = f.read()
    with open('clients_messages/'+f'clients_messages_{num}.txt', 'r', encoding='utf-8') as f:
        d = json.load(f)
        message = d['messages']
    with open(f'results/concated/res{num}.txt', 'w') as f:
        f.write(str(message) + '\n\n' +ans)
    
