""" Blender operators for adding/removing components """
from typing import Any

import bpy
from .component_finder import get_components
from .component_schema import ComponentSchema, get_id, get_title, get_description


BASE_PROPERTY = "ECS_Components_v1"


def get_components_array(obj: bpy.types.Object) -> Any:
    """Returns the array of components in an object"""
    arr = obj.get(BASE_PROPERTY)  # type: ignore
    if arr is not None:
        if isinstance(arr, list):
            return arr
        return arr.to_list()
    return []


def has_component(obj: bpy.types.Object, component: ComponentSchema) -> bool:
    """returns True if the object has the specified component"""
    components = get_components_array(obj)
    candidates = [c for c in components if c["type"] == get_id(component)]
    return len(candidates) > 0


def add_component(obj: bpy.types.Object, component: ComponentSchema) -> None:
    """Adds a component to an object. Does not ensure the component is valid/complete but
    creates it empty"""
    assert not has_component(obj, component)
    components = get_components_array(obj)
    components.append({"type": get_id(component)})
    obj[BASE_PROPERTY] = components  # type: ignore


def remove_component(obj: bpy.types.Object, component: ComponentSchema) -> None:
    """Removes a component from an object"""
    assert has_component(obj, component)
    components = get_components_array(obj)
    components = [c for c in components if c["type"] != get_id(component)]
    obj[BASE_PROPERTY] = components  # type: ignore


def generate_component_to_remove_list(_widget, context):
    """The remove component dialog only shows what components the
    object has present that can be removed. This function
    figures out what functions can be removed from an object"""
    component_types = [("0", "None", "None")]
    for component in get_components():
        if has_component(context.object, component):
            component_types.append(
                (get_id(component), get_title(component), get_description(component))
            )
    return component_types


def generate_component_to_add_list(_widget, context):
    """When adding a ecs component, the list only displays the
    components that do not already exist on the object and ones that
    can be added to this object type"""
    component_types = [("0", "None", "None")]
    for component in get_components():
        if not has_component(context.object, component):
            component_types.append(
                (get_id(component), get_title(component), get_description(component))
            )
    return component_types


class RemoveEcsComponent(bpy.types.Operator):
    """Removes a ecs component from this object - pops up a small
    dialog to select which one."""

    bl_idname = "object.remove_ecs_component"
    bl_label = "Remove Ecs Component"
    bl_options = {"REGISTER", "UNDO"}

    property_to_remove: bpy.props.EnumProperty(  # type: ignore
        name="Remove Component",  # noqa
        description="Select the component you wish to remove",  # noqa
        default=None,
        items=generate_component_to_remove_list,
    )

    def invoke(self, context, _event):
        """Show selection dialog that allows the user to select a compoent
        to remove"""
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """Removes the selected component from the object"""
        selected = self.property_to_remove
        if selected in ("0", ""):
            return {"FINISHED"}

        schema = [c for c in get_components() if get_id(c) == selected][0]
        remove_component(context.object, schema)

        # Redraw UI
        for area in bpy.context.window.screen.areas:  # type: ignore
            if area.type == "PROPERTIES":  # type: ignore
                area.tag_redraw()  # type: ignore

        return {"FINISHED"}


class AddEcsComponent(bpy.types.Operator):
    """Adds a ecs component from this object - pops up a small
    dialog to select which one."""

    bl_idname = "object.add_ecs_component"
    bl_label = "Add Ecs Component"
    bl_options = {"REGISTER", "UNDO"}

    property_to_add: bpy.props.EnumProperty(  # type: ignore
        name="Add Component",  # noqa
        description="Select the component you wish to add",  # noqa
        default=None,
        items=generate_component_to_add_list,
    )

    def invoke(self, context, _event):
        """Display the add-component selector, allowing the user to
        select what component they wish to add"""
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """Adds the currently selected component to the object by invoking
        it's add method"""
        selected = self.property_to_add
        if selected in ("0", ""):
            return {"FINISHED"}

        schema = [c for c in get_components() if get_id(c) == selected][0]
        add_component(context.object, schema)

        # Redraw UI
        for area in bpy.context.window.screen.areas:  # type: ignore
            if area.type == "PROPERTIES":  # type: ignore
                area.tag_redraw()  # type: ignore
        return {"FINISHED"}
