from lark import Transformer

class TerraformTransformer(Transformer):
    def string(self, _):
        return "string"

    def number(self, _):
        return "number"

    def bool(self, _):
        return "bool"

    def any(self, _):
        return "any"

    def list_type(self, children):
        return {"type": "list", "element_type": children[0]}

    def set_type(self, children):
        return {"type": "set", "element_type": children[0]}

    def map_type(self, children):
        return {"type": "map", "element_type": children[0]}

    def tuple_type(self, children):
        return {"type": "tuple", "element_types": children}

    def object_type(self, children):
        return {"type": "object", "fields": children}

    def object_field(self, children):
        name = children[0].strip('"')
        type_def = children[2]
        return {"name": name, "type": type_def}

    def variable_block(self, children):
        name = children[0].strip('"')
        attributes = children[1]
        return {"name": name, **attributes}

    def attribute(self, children):
        return children[0]  # Flatten the attribute structure

    def description(self, children):
        return {"description": children[0].strip('"')}

    def type_def(self, children):
        return {"type": children[0]}

    def default(self, children):
        return {"default": children[0]}

    # Handle values
    def value(self, children):
        return children[0]

    def list_value(self, children):
        return children

    def map_value(self, children):
        return dict(children)

    def key_value(self, children):
        key, value = children
        return (key.strip('"'), value)

    def validation(self, children):
        conditions = {}
        for child in children:
            if "condition" in child:
                conditions["condition"] = child["condition"]
            elif "error_message" in child:
                conditions["error_message"] = child["error_message"]
        return {"validation": conditions}

    def validation_condition(self, children):
        key, value = children
        return {key: value}
