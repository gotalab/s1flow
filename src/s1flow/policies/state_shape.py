"""The shape of the states a policy was evaluated on: a small JSON Schema every evaluated state fits.
A loaded policy compares the app's states with it, so a state that changed shape is noticed."""

from __future__ import annotations

from typing import Any

from ..client.state import Image

JSONSchema = dict[str, Any]  # a JSON Schema document is free-form by definition



def schema_of(values: list[Any]) -> JSONSchema:
    """A small JSON Schema that every value fits: types, object keys always present, list items."""
    kinds = {_kind(v) for v in values}
    if len(kinds) > 1:
        return {"anyOf": [schema_of([v for v in values if _kind(v) == k]) for k in sorted(kinds)]}
    kind = kinds.pop() if kinds else "null"
    if kind == "object":
        keys = sorted({k for v in values for k in v})
        required = [k for k in keys if all(k in v for v in values)]
        return {"type": "object", "properties": {k: schema_of([v[k] for v in values if k in v]) for k in keys}, "required": required, "additionalProperties": False}
    if kind == "array":
        items = [x for v in values for x in v]
        return {"type": "array", "items": schema_of(items)} if items else {"type": "array"}
    return {"type": kind}


def _kind(v: Any) -> str:
    if isinstance(v, Image):
        return "image"
    if isinstance(v, dict):
        return "image" if v.get("type") == "image" else "object"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, (int, float)):
        return "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "array"
    return "null" if v is None else type(v).__name__


def mismatch(schema: JSONSchema, value: Any, at: str = "state") -> list[str]:
    """Where `value` does not fit `schema` (empty when it fits)."""
    if "anyOf" in schema:
        tries = [mismatch(s, value, at) for s in schema["anyOf"]]
        return [] if any(not t for t in tries) else min(tries, key=len)
    want = schema.get("type")
    if want == "image":
        return [] if isinstance(value, dict) and value.get("type") == "image" or type(value).__name__ == "Image" else [f"{at}: expected an image"]
    got = _kind(value)
    if want == "integer" and isinstance(value, int) and not isinstance(value, bool):
        return []
    if want is not None and want != got:
        return [f"{at}: expected {want}, got {got}"]
    out: list[str] = []
    if want == "object":
        for k in schema.get("required", []):
            if k not in value:
                out.append(f"{at}.{k}: missing")
        for k, sub in schema.get("properties", {}).items():
            if k in value:
                out += mismatch(sub, value[k], f"{at}.{k}")
        extra = set(value) - set(schema.get("properties", {}))
        additional = schema.get("additionalProperties", True)
        if additional is False:
            out += [f"{at}.{k}: not permitted by the input shape" for k in sorted(extra)]
        elif isinstance(additional, dict):
            for key in sorted(extra):
                out += mismatch(additional, value[key], f"{at}.{key}")
    elif want == "array" and "items" in schema:
        for i, x in enumerate(value):
            out += mismatch(schema["items"], x, f"{at}[{i}]")
    return out


def validate_schema(schema: JSONSchema) -> None:
    """Check the small shape-schema dialect this runtime actually enforces."""
    known = {"type", "properties", "required", "items", "anyOf", "additionalProperties"}
    if set(schema) - known:
        raise ValueError(f"unsupported input shape keywords: {sorted(set(schema) - known)}")
    if "type" in schema and schema["type"] not in {"object", "array", "string", "number", "integer", "boolean", "null", "image"}:
        raise ValueError("unsupported input shape type")
    if "anyOf" in schema and set(schema) != {"anyOf"}:
        raise ValueError("input shape anyOf cannot combine with other keywords")
    if set(schema) & {"properties", "required", "additionalProperties"} and schema.get("type") != "object":
        raise ValueError("object shape keywords require type object")
    if "items" in schema and schema.get("type") != "array":
        raise ValueError("items requires type array")
    if "anyOf" in schema:
        alternatives = schema["anyOf"]
        if not isinstance(alternatives, list) or not alternatives:
            raise ValueError("input shape anyOf requires a nonempty list")
        for alternative in alternatives:
            if not isinstance(alternative, dict):
                raise ValueError("each input shape alternative is an object")
            validate_schema(alternative)
    if "properties" in schema:
        properties = schema["properties"]
        if not isinstance(properties, dict) or not all(isinstance(value, dict) for value in properties.values()):
            raise ValueError("input shape properties must map names to schemas")
        for sub in properties.values():
            validate_schema(sub)
    if "required" in schema and (not isinstance(schema["required"], list) or not all(isinstance(key, str) for key in schema["required"])):
        raise ValueError("input shape required must list property names")
    if "items" in schema:
        if not isinstance(schema["items"], dict):
            raise ValueError("input shape items must be a schema")
        validate_schema(schema["items"])
    if "additionalProperties" in schema:
        additional = schema["additionalProperties"]
        if isinstance(additional, dict):
            validate_schema(additional)
        elif not isinstance(additional, bool):
            raise ValueError("input shape additionalProperties must be a boolean or schema")
