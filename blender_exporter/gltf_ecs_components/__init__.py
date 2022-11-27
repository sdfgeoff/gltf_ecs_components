"""
All the blender setup for the addon: registering UI's etc
"""
import logging

import bpy

from .utils import jdict
from .component_finder import get_components
from .component_schema import get_title, get_description
from .operators import AddEcsComponent, RemoveEcsComponent, has_component

logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG")

bl_info = {
    "name": "GLTF ECS Components",
    "blender": (3, 3, 0),
    "category": "Game",
}


class EcsComponentsPanel(bpy.types.Panel):  # pylint: disable=R0903
    """The panel in which buttons that add/remove components are shown"""

    bl_idname = "OBJECT_PT_ecs_components_panel"
    bl_label = "Ecs Components"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"

    def draw(self, context):
        """Create the UI for the panel"""
        row = self.layout.row()
        row.operator("object.add_ecs_component")
        row.operator("object.remove_ecs_component")

        # I would like to do this, but it still brings up the UI
        # and I don't know how to get it to show the UI when clicking
        # the generic add ones, but remove it when clicking a specific add
        # button.....
        #
        # for component in get_components():
        #     if not has_component(context.object, component):
        #         op = row.operator(
        #             "object.add_ecs_component", text=get_title(component), icon="ADD"
        #         )
        #         op.property_to_add = get_id(component)  # type: ignore
        #     else:
        #         op = row.operator(
        #             "object.remove_ecs_component",
        #             text=get_title(component),
        #             icon="REMOVE",
        #         )
        #         op.property_to_add = get_id(component)  # type: ignore
        for component in get_components():
            if has_component(context.object, component):
                col = self.layout.column(align=True)

                col.row().label(text=get_title(component))

                row = col.box().row()
                description = get_description(component)
                if description:
                    row.label(text=description)


def register():
    """Blender needs to know about all our classes and UI panels
    so that it can draw/store things"""
    logger.info(jdict(event="registering_gltf_ecs_components_addon", state="start"))

    bpy.utils.register_class(AddEcsComponent)
    bpy.utils.register_class(RemoveEcsComponent)
    bpy.utils.register_class(EcsComponentsPanel)

    logger.debug(jdict(event="registering_gltf_ecs_components_addon", state="end"))


def unregister():
    """When closing blender or uninstalling the addon we should leave
    things nice and clean...."""
    logger.info(jdict(event="unregistering_gltf_ecs_components_addon", state="start"))

    bpy.utils.unregister_class(AddEcsComponent)
    bpy.utils.unregister_class(RemoveEcsComponent)
    bpy.utils.unregister_class(EcsComponentsPanel)

    logger.debug(jdict(event="unregistering_gltf_ecs_components_addon", state="end"))
