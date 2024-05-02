import sys

from ml_generation.broker.broker import Broker
from ml_generation.broker.rmq_broker import RmqBroker

from ml_generation.steps.co_gen import CoGen
from ml_generation.steps.preproc import Preproc

from ml_models.co_gen.api import GenerateGateWrapper as CoMlModel
from ml_generation.dummy_ml_model import DummyMlModel


def main():
    print("Creating RmqBroker...")
    broker: Broker = RmqBroker()
    print("RmqBroker created")

    print("Creating Preproc...")
    preproc = Preproc(broker)
    print("Preproc created")

    print("Creating CoGen...")
    # ml_model = CoMlModel()  # TODO: enable when ml is ready
    ml_model = DummyMlModel()
    co_gen = CoGen(broker, ml_model)
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
