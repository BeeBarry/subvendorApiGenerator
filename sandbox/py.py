import logging
import os
import json
import traceback
import base64
import sys
import hcl2

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from parser import generate_openapi_schema, sanitize_schema_name

file_path = './test.json'

def decodeHcl(encoded_content):
    decoded_bytes = base64.b64decode(encoded_content)
    return decoded_bytes.decode('utf-8')

with open(file_path, 'r') as file:
    data = json.load(file)

    specs = {}
    contents = data.get("contents", {})
    for key, encoded_content in contents.items():
        try:
            decoded_hcl = decodeHcl(encoded_content) 
            dict = hcl2.loads(decoded_hcl)
            obj={}

            # TODO: error handling
            for item in dict["variable"]:
                for k, v in item.items():
                    obj[k] = v

            spec = generate_openapi_schema(obj)
            schemaName = sanitize_schema_name(key)

            specs[schemaName] = spec
        except UnicodeDecodeError as e:
            logging.error(f"Base64 decoding failed for {key}: {str(e)}")
        except Exception as e:
            logging.error(f"Processing failed for {key}: {str(e)}")
            logging.error(traceback.format_exc())

    print(json.dumps(specs, indent=2))

    # api_spec = {
    #     "openapi": "3.0.0", 
    #     "info": {
    #         "title": "Request Subscription API",
    #         "version": "not-implemented"
    #     },
    #     "paths": {
    #         "/requestSubscription": {
    #             "post": {
    #                 "summary": "Request a subscription",
    #                 "requestBody": {
    #                     "content": {
    #                         "application/json": {
    #                             "schema": specs
    #                         }
    #                     }
    #                 },
    #                 "responses": {
    #                     "201": {
    #                         "description": "Subscription requested successfully"
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }
    # print(api_spec)
