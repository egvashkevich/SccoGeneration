import json
import pika
import sys

def process_customer_data(customer_data):
    
    print("Данные получены:")
    print(f"Customer ID: {customer_data['customer_id']}")
    print(f"Company Name: {customer_data['company_name']}")
    print(f"Contact Info: {', '.join(customer_data['contact_info'])}")
    print(f"Black List: {', '.join(customer_data['black_list'])}")
    print(f"Tags: {', '.join(customer_data['tags'])}")
    print(f"Specific Features: {', '.join(customer_data['specific_features'])}")

    print("\nServices Provided:")
    for service in customer_data['services']:
        print(f"Service Name: {service['service_name']}")
        print(f"Service Description: {service['service_desc']}")
    print("\n")

def process_request_data(json_input):
    try:
        # Декодирование строки JSON в словарь
        data = json.loads(json_input)
        
        # Передача данных в функцию обработки
        process_customer_data(data)
    except json.JSONDecodeError as e:
        print(f"An error occurred while decoding JSON: {e}")
    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
# Пример JSON строки
    json_input = '''
    {
            "customer_id": "customer_3",
            "contact_info": ["telegram", "whatsup"],
            "company_name": "MIPT",
            "black_list": [
                "forbidden1",
                "forbidden2"
            ],
            "tags": [
                "backend",
                "java"
            ],
            "specific_features": [
                "some customer comment 1",
                "some customer comment 2"
            ],
            "services": [
                {
                    "service_name": "(1) First service",
                    "service_desc": "First service description. Very long description."
                },
                {
                    "service_name": "(2) Second service",
                    "service_desc": "Second service description. Very long description."
                },
                {
                    "service_name": "(3) Third service",
                    "service_desc": "Third service description. Very long description."
                }
            ]
    }
    '''
    raise Exception()
    # Вызов функции с примером JSON строки
    process_request_data(json_input)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)

