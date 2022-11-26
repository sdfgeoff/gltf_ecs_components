
# GLTF ECS Components

## What is this?

Many modern game engines use the [Entity Component System](https://en.wikipedia.org/wiki/Entity_component_system) (ECS) way of defining behaviour and logic. Many modern game engines also use [GLTF](https://en.wikipedia.org/wiki/GlTF) for storing assets - their geometry, animations and materials. One thing that has been lacking is the ability to combine these things. If you wish to assign logic to a particular node in a scene, how do you do so? Do you search through the GLTF scene for particular object names? Do you use suffixes? Or perhaps if your game engine supports it, you look through the "extras" field and define the behaviour there.

This repository aims to create a small standard for how this information is conveyed through GLTF. It does this in two ways:

 1. Defining a standard for how this data is stored
 2. Implementing a blender addon that allows exporting components

Another repository (yet to be developed) will implement the importing of this data into Bevy, as a proof of concept of how this system can work.

## What is this not
This does not define the specifics of any particular components. It does not guarantee interoperability between assets and engines - but it may form the start of some levels of compatibility.

In the future I would love to see a world where collision information (eg friction, collision margins) accompany most GLTF assets, and where many more ad-hoc will transition to GLTF.

# The Spec
The spec is tiny. It goes like this:

1.  A node may contain the field `ECS_Components_v1` in the `extras` field
2. The `ECS_Components_v1` field is a `List` of `ComponentObjects`.
3. A `ComponentObject` must contain the fields:
	1. `type: string` Contains the name/type of the component. If this component represents a box collider, then maybe the value of `type` is `box_collider`. Maybe the value of `type` is `player` or `enemy`
4. A `ComponentObject` may contain any other field required to set up the component in the target system.
5. The `ECS_Components_v1` field must _not_ contain two `CompoentObjects` with the same `type`.

### Design Notes:
This is designed to be easy to parse by a static type system (such as [serde's Enum representation](https://serde.rs/enum-representations.html)), which is why it is an `Array` rather than an `Object`

## Example

### Player Tag:
Here's a cube with a mesh that is tagged with the component `player` 
```json
{
   "nodes" : [
        {
            "extras" : {
                "ECS_Components_v1": [
                    {"type": "player"}
                ]
            },
            "mesh" : 0,
            "name" : "Cube"
        }
    ],
    .... # Rest of GLTF file
}
```

### Player with Health
Maybe our player also has a `health` component:
Here's a cube with a mesh that is tagged with the component `player` 
```json
{
   "nodes" : [
        {
            "extras" : {
                "ECS_Components_v1": [
                    {"type": "player"},
                    {"type": "health", "initial_health": 100, "max_health": 150},
                ]
            },
            "mesh" : 0,
            "name" : "Cube"
        }
    ],
    .... # Rest of GLTF file
}
```

### Duplication of components
Here's an invalid file. It contains two of the same components. Parsers should reject (or at least throw warnings) on encountering this file:
```json
{
   "nodes" : [
        {
            "extras" : {
                "ECS_Components_v1": [
                    {"type": "player"},
                    {"type": "health", "initial_health": 100, "max_health": 150},
                    {"type": "health", "initial_health": 120, "max_health": 180},
                ]
            },
            "mesh" : 0,
            "name" : "Cube"
        }
    ],
    .... # Rest of GLTF file
}
```
Yes, the following is also invalid:
```json
{
   "nodes" : [
        {
            "extras" : {
                "ECS_Components_v1": [
                    {"type": "player"},
                    {"type": "player"},
                ]
            },
            "mesh" : 0,
            "name" : "Cube"
        }
    ],
    .... # Rest of GLTF file
}
```