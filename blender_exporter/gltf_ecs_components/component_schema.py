"""
Handles parsing to/from the json schema for a component
"""
from typing import TypedDict, Optional


class ComponentSchemaType(TypedDict):
    """What type of component"""

    const: str


class ComponentSchemaProperties(TypedDict):
    """Properties contained in the component"""

    type: ComponentSchemaType


class ComponentSchema(TypedDict):
    """The bare minimum definition/metadata about a schema"""

    properties: ComponentSchemaProperties
    title: Optional[str]
    description: Optional[str]


def get_id(schema: ComponentSchema) -> str:
    """Returns the ID of the schema"""
    return schema["properties"]["type"]["const"]


def get_title(schema: ComponentSchema) -> str:
    """Returns the title of the schema if present, if not
    returns the ID"""
    title = schema.get("title")
    if title is not None:
        return title
    return get_id(schema)


def get_description(schema: ComponentSchema) -> str:
    """Returns a description to use for the schema"""
    description = schema.get("description")
    if description is not None:
        return description
    return ""
