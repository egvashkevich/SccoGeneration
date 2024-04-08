import inspect  # cleandoc
import textwrap  # dedent
import json


def json_get_or_panic(json_dict, key, db_query: any = "not passed"):
    if key not in json_dict:
        raise RuntimeError(
            inspect.cleandoc(f"""
Missing "{key}".
db_query content: {json.dumps(db_query, indent=2)}
json_dict content: {json.dumps(json_dict, indent=2)}
            """)
        )
    return json_dict[key]
