from lark import Transformer
from typing import Any 

class TerraformTransformer(Transformer):
    def string(self, _: list[Any]) -> str:
        return "string"

    def number(self, _: list[Any]) -> str:
        return "number"

    def bool(self, _: list[Any]) -> str:
        return "bool"

    def any(self, _: list[Any]) -> str:
        return "any"

    def list_type(self, children: list[Any]) -> dict[str, Any]:
        return {"type": "list", "element_type": children[0]}

    def set_type(self, children: list[Any]) -> dict[str, Any]:
        return {"type": "set", "element_type": children[0]}

    def map_type(self, children: list[Any]) -> dict[str, Any]:
        return {"type": "map", "element_type": children[0]}

    def tuple_type(self, children: list[Any]) -> dict[str, Any]:
        return {"type": "tuple", "element_types": children}

    def object_type(self, children: list[Any]) -> dict[str, Any]:
        return {"type": "object", "fields": children}

    def object_field(self, children: list[Any]) -> dict[str, Any]:
        name = children[0].strip('"')
        type_def = children[2]
        return {"name": name, "type": type_def}

    def variable_block(self, children: list[Any]) -> dict[str, Any]:
        name = children[0].strip('"')
        attributes = children[1]
        return {"name": name, **attributes}

    def attribute(self, children: list[Any]) -> Any:
        return children[0]  # Flatten the attribute structure

    def description(self, children: list[Any]) -> dict[str, str]:
        return {"description": children[0].strip('"')}

    def type_def(self, children: list[Any]) -> dict[str, Any]:
        return {"type": children[0]}

    def default(self, children: list[Any]) -> dict[str, Any]:
        return {"default": children[0]}

    def value(self, children: list[Any]) -> Any:
        return children[0]

    def list_value(self, children: list[Any]) -> list[Any]:
        return children

    def map_value(self, children: list[tuple[Any, Any]]) -> dict[Any, Any]:
        return dict(children)

    def key_value(self, children: list[Any]) -> tuple[str, Any]:
        key, value = children
        return (key.strip('"'), value)

    def validation(self, children: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        conditions = {}
        for child in children:
            if "condition" in child:
                conditions["condition"] = child["condition"]
            elif "error_message" in child:
                conditions["error_message"] = child["error_message"]
        return {"validation": conditions}

    def validation_condition(self, children: list[Any]) -> dict[str, Any]:
        key, value = children
        return {key: value}
