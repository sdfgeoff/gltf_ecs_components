"""
Functions used to find and load component definitions
"""
from typing import List, TypedDict, Tuple
import functools
import logging
import os
import json

import bpy

from .utils import jdict

logger = logging.getLogger(__name__)


class ComponentSchemaType(TypedDict):
    """What type of component"""

    const: str


class ComponentSchemaProperties(TypedDict):
    """Properties contained in the component"""

    type: ComponentSchemaType


class ComponentSchema(TypedDict):
    """The bare minimum definition/metadata about a schema"""

    properties: ComponentSchemaProperties


def get_components() -> List[ComponentSchema]:
    """Returns the components"""
    paths = generate_candidate_paths()
    return load_components(tuple(paths))


@functools.lru_cache()
def load_components(paths: Tuple[str]) -> List[ComponentSchema]:
    """Load components from disk"""
    components = []
    for path in paths:
        components.extend(load_schemas(path))

    # Check for component type collisions
    component_types = [
        component["properties"]["type"]["const"] for component in components
    ]
    if len(set(component_types)) != len(component_types):
        logging.warning(jdict(event="duplicate_component_types", types=component_types))

    return components


def generate_candidate_paths() -> List[str]:
    """Where should we look for component definitions?"""
    paths = []

    bundled_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "components"
    )
    paths.append(bundled_path)

    # Search relative to blend
    try:
        blend_path = bpy.path.abspath("//")
    except AttributeError:
        # Blend file not loaded yet
        pass
    else:
        custom_component_folder = os.path.join(blend_path, "components")
        if os.path.isdir(custom_component_folder):
            paths.append(custom_component_folder)

    return paths


def load_schemas(path: str) -> List[ComponentSchema]:
    """Searches for JSON files in the supplied paths and loads
    them into ComponentSchema. If some do not parse, an error is
    logged and ignored"""
    schemas = []
    for file_name in os.listdir(path):
        if file_name.endswith(".json"):
            fullpath = os.path.join(path, file_name)
            try:
                schemas.append(parse_schema(fullpath))
            except ValueError as err:
                logging.error(
                    jdict(
                        event="failed_loading_component", path=fullpath, error=str(err)
                    )
                )
    return schemas


def parse_schema(path: str) -> ComponentSchema:
    """Loads a schema from disk"""
    logger.debug(jdict(event="loading_component", path=path, state="start"))
    with open(path, encoding="utf-8") as filedata:
        data = json.load(filedata)
    type_data = data.get("properties", {}).get("type", {}).get("const", None)
    if type_data is None:
        raise ValueError("Unable to determine component type")
    logger.debug(
        jdict(event="loading_component", path=path, state="end", type=type_data)
    )
    return data
