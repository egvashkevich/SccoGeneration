import os
import pandas as pd

from ChatAccessManager import ChatAccessManager
from LLM_Manager import LLM_Manager
from SimpleBaseLine import SimpleBaseline

CSV_PATH = os.environ.get('CSV_PATH')


if __name__ == "__main__":
    manager = ChatAccessManager()
    manager.update_token()
    print()
    model_manager = LLM_Manager()

    path_to_csv = CSV_PATH
    data = pd.read_csv(path_to_csv)
    data.head()

    message_id = 10
    message = data.iloc[13]['Message']

    baseline = SimpleBaseline()
    baseline.need_generate_cp(message)
