import logging
import azure.functions as func
import os
import json
import traceback
import base64

from dataclasses import dataclass
from parser import generate_openapi_schema

@dataclass
class RequestBody:
    version: str
    revision: str
    contents: dict[str, str]

def main(req: func.HttpRequest, outputblob: func.Out[bytes]):
    try:
        data = req.get_json()
        req_body = RequestBody(**data)
        revision = req.route_params.get('revision')
    except ValueError as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)
    except TypeError as e:
        return func.HttpResponse(f"Missing required field: {str(e)}", status_code=400)
    else:
        contents = req_body.contents

        specs = {}
        for key, encoded_content in contents.items():
            try:
                decoded_bytes = base64.b64decode(encoded_content)
                decoded_hcl = decoded_bytes.decode('utf-8')
                
                spec = generate_openapi_schema(decoded_hcl)
                specs[key] = spec
            except UnicodeDecodeError as e:
                logging.error(f"Base64 decoding failed for {key}: {str(e)}")
                return func.HttpResponse(f"Invalid base64 encoding in {key}", status_code=400)
            except Exception as e:
                logging.error(f"Processing failed for {key}: {str(e)}")
                logging.error(traceback.format_exc())
                return func.HttpResponse(f"Error processing {key}: {str(e)}", status_code=400)            

        api_spec = {
            "openapi": "3.0.0", 
            "info": {
                "title": "Request Subscription API",
                "version": revision
            },
            "paths": {
                "/requestSubscription": {
                    "post": {
                        "summary": "Request a subscription",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": specs
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Subscription requested successfully"
                            }
                        }
                    }
                }
            }
        }
        outputblob.set(json.dumps(api_spec))
    
        return func.HttpResponse(
            f"Blob created successfully!",
            status_code=201
        )
