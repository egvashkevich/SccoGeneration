import sys

from ml_generation.rmq_broker import RmqBroker

from ml_generation.steps.co_gen import CoGen
from ml_generation.steps.preproc import Preproc


def main():
    print("Creating RmqBroker...")
    broker = RmqBroker()
    print("RmqBroker created")

    print("Creating Preproc...")
    preproc = Preproc(broker)
    print("Preproc created")

    print("Creating CoGen...")
    co_gen = CoGen(broker)
    print("CoGen created")

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
