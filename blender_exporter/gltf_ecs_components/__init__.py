"""
All the blender setup for the addon: registering UI's etc
"""
import logging

from . import component_finder
from .utils import jdict


logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG")

bl_info = {
    "name": "GLTF ECS Components",
    "blender": (3, 3, 0),
    "category": "Game",
}


def register():
    """Blender needs to know about all our classes and UI panels
    so that it can draw/store things"""
    logger.info(jdict(event="registering_gltf_ecs_components_addon", state="start"))

    print(component_finder.get_components())

    logger.debug(jdict(event="registering_gltf_ecs_components_addon", state="end"))


def unregister():
    """When closing blender or uninstalling the addon we should leave
    things nice and clean...."""
    logger.info(jdict(event="unregistering_gltf_ecs_components_addon", state="start"))
    logger.debug(jdict(event="unregistering_gltf_ecs_components_addon", state="end"))
