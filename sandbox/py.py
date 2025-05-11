
import logging
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import json
import base64
import hcl2
from typing import Any
from parser import generate_openapi_schema, sanitize_schema_name

def decodeHcl(encoded_content: str) -> str:
    decoded_bytes = base64.b64decode(encoded_content)
    return decoded_bytes.decode('utf-8')

with open('./test.json', 'r') as file:
    data = json.load(file)
    contents = data.get("contents", {})
    specs = {
        "type": "object",
        "properties": {}
    }

    for key, encoded_content in contents.items():
        decoded_hcl = decodeHcl(encoded_content) 
        dict = hcl2.loads(decoded_hcl)

        for k, v in dict.items():
            obj={}

            # TODO: error handling
            for item in dict["variable"]:
                for k, v in item.items():
                    obj[k] = v

            spec = generate_openapi_schema(obj)
            schemaName = sanitize_schema_name(key)
            specs["properties"][schemaName] = spec

    print(specs)


