import sys

from broker_for_creator.Broker import Broker
from broker_for_creator.RmqBroker import RmqBroker

from steps.insertToDb import InsertToDb

def main():
    print("Customer creator:Creating RmqBroker...")
    broker: Broker = RmqBroker()
    print("RmqBroker created")

    print("Creating insertToDb...")
    InsertToDb = InsertToDb(broker)
    print("InsertToDb created")

    print("Start consuming...")
    broker.start_consuming()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)

