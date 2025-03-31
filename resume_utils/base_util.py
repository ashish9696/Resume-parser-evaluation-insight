import json
from ast import literal_eval

def convert_response(response):
    try:
        return eval(response)
    except:
        try:
            return literal_eval(response)
        except:
            try:
                return json.loads(response)
            except:
                return None