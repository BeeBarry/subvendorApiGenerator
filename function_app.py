import azure.functions as func
import datetime
import json
import logging
import traceback
import base64
from parser import generate_openapi_spec

app = func.FunctionApp()

@app.route(route="setSchema", auth_level=func.AuthLevel.ANONYMOUS)
def setSchema(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)
    else:
        for key, encoded_content in req_body.items():
            try:
                decoded_bytes = base64.b64decode(encoded_content)
                decoded_hcl = decoded_bytes.decode('utf-8')
                
                spec = generate_openapi_spec(decoded_hcl)
                return func.HttpResponse(
                    json.dumps(spec, indent=2),
                    status_code=200,
                    mimetype="application/json"
                )
            except UnicodeDecodeError as e:
                logging.error(f"Base64 decoding failed for {key}: {str(e)}")
                return func.HttpResponse(f"Invalid base64 encoding in {key}", status_code=400)
            except Exception as e:
                logging.error(f"Processing failed for {key}: {str(e)}")
                logging.error(traceback.format_exc())
                return func.HttpResponse(f"Error processing {key}: {str(e)}", status_code=400)            

    return func.HttpResponse(
        status_code=200
    )

