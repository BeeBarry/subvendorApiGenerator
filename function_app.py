import azure.functions as func
import datetime
import json
import logging
from lark import Lark

app = func.FunctionApp()

# Stolen from Melvin Koh at https://melvinkoh.me/parsing-terraform-for-forms-clr4zq4tu000309juab3r1lf7
type_parser = Lark(r"""
    ?type: "any" -> any
        | "string" -> string
        | "number" -> number
        | "bool" -> bool
        | "object({" [keyval (keyval)*] "})" -> object
        | "list(" [type] ")"  -> list
        | "set(" [type] ")" -> set
        | "map(" [type] ")" -> map
        | "tuple(" [type (type)* ] ")" -> tuple

    keyval: CNAME keyval_separator type [comment]
    ?keyval_separator: "=" | ":"
    ?comment: SH_COMMENT                  

    %import common.SH_COMMENT              
    %import common.CNAME              
    %import common.WS              
    %ignore WS
    """, start='type')

@app.route(route="setSchema", auth_level=func.AuthLevel.ANONYMOUS)
def setSchema(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        processed_data = {}
        for key, value in req_body.items():
            print(key)
            print(value)
            # processed_data[key] = str(value) + "_processed"

    return func.HttpResponse(
         "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
         status_code=200
    )
