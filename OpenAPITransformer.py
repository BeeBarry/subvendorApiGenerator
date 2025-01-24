from lark import Transformer
class OpenAPITransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.components = {"schemas": {}}

    def variable_block(self, children):
        var_name = children["name"]
        var_def = {
            "type": "object",
            "properties": {},
            "description": children.get("description", ""),
        }

        if "type" in children:
            var_def["properties"]["value"] = self._map_type(children["type"])

        if "default" in children:
            var_def["example"] = children["default"]

        self.components["schemas"][var_name] = var_def
        return var_name

    def _map_type(self, tf_type):
        # Map Terraform types to OpenAPI types
        type_mapping = {
            "any": {"oneOf": [
                {"type": "string"},
                {"type": "number"},
                {"type": "boolean"},
                {"type": "object"},
                {"type": "array"}
            ]},
            "string": {"type": "string"},
            "number": {"type": "number"},
            "bool": {"type": "boolean"},
            "list": {
                "type": "array",
                "items": self._map_type(tf_type["element_type"])
            },
            "set": {
                "type": "array",
                "items": self._map_type(tf_type["element_type"]),
                "uniqueItems": True
            },
            "map": {
                "type": "object",
                "additionalProperties": self._map_type(tf_type["element_type"])
            },
            "object": {
                "type": "object",
                "properties": {
                    field["name"]: self._map_type(field["type"])
                    for field in tf_type["fields"]
                }
            },
            "tuple": {
                "type": "array",
                "prefixItems": [
                    self._map_type(t) for t in tf_type["element_types"]
                ]
            },
        }
        return type_mapping.get(tf_type["type"], {"type": "string"})
