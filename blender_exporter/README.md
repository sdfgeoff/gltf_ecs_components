# Blender GLTF ECS Component Tool
This is an exporter for ECS components into the GLTF format.

When exporting, be sure to tick the "include custom properties" tickbox.

# Defining Custom Components
A component is defined by a json schema of what should be included 
into the component.

In line with the specification for a `ComponentObject`, each schema
should include the `type` field which should contain a unique identifier
for the component.

## Example Tag Component
The simplest component is a tag component that contains no data:
```python
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "type": {
      "const": "my_custom_component_name"
    }
  }
}
```

## Example Health Component
If you want your component to look like:
```json
{"type": "health", "initial_health": 100, "max_health": 150}
```
Then you would specify this as:
```python
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "type": {
      "const": "health"
    },
    "initial_health": {
      "type": "integer",
      "mininum": 0
    },
    "max_health": {
      "type": "integer",
      "mininum": 0
    }
  }
}
```

You should also add names and descriptions:
```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "title": "Health",
  "description": "Tracks the health of an entity",
  "properties": {
    "type": {
      "const": "health"
    },
    "initial_health": {
      "title": "Initial Health",
      "description": "The health that this entity has at the start of the game",
      "type": "integer",
      "mininum": 0
    },
    "max_health": {
      "title": "Max Health",
      "description": "How much health the entity can attain after regenerating or picking up med-packs",
      "type": "integer",
      "mininum": 0
    }
  }
}
```

These components can be placed either in the addon folder (`gltf_ecs_components/components`) or in a components folder
parallel to or upstream of the blend file. The following paths
will all correctly find the player robot and health components:
```
 - MyProject/
 - MyProject/robot.blend
 - MyProject/player.blend
 - MyProject/levels/level1.blend
 - MyProject/levels/level2.blend
 - MyProject/components/
 - MyProject/components/player_tag.json
 - MyProject/components/robot_tag.json
 - MyProject/components/health.json
```

## Supported Schema Properties

### Planned

- [x] `$comment` Does nothing....

- [ ] `title` Used as label
- [ ] `description` Used as tooltip while hovering
- [ ] `default` Used as default, not necessarily written to the output
- [ ] `boolean`
- [ ] `null`
- [ ] `enum`
- [ ] `const`

- [ ] `Number`
   - [ ] `minimum`
   - [ ] `maximum`
   - [ ] `multipleOf`  *Not Planned*
   - [ ] `exclusiveMinimum`  *Not Planned*
   - [ ] `exclusiveMaximum`  *Not Planned*

- [ ] `Integer`
   - [ ] `minimum`
   - [ ] `maximum`
   - [ ] `multipleOf`  *Not Planned*
   - [ ] `exclusiveMinimum`  *Not Planned*
   - [ ] `exclusiveMaximum`  *Not Planned*

- [ ] `string`
   - [ ] `minLength`  *Not Planned*
   - [ ] `maxLength`  *Not Planned*
   - [ ] `pattern`  *Not Planned*
   - [ ] `format`  *Not Planned*
       - [ ] `date`-time  *Not Planned*
       - [ ] `time`  *Not Planned*
       - [ ] `date`  *Not Planned*
       - [ ] `duration`  *Not Planned*
       - [ ] `email`  *Not Planned*
       - [ ] `idn-email`  *Not Planned*
       - [ ] `ipv4`  *Not Planned*
       - [ ] `ipv6`  *Not Planned*
       - [ ] `uuid`  *Not Planned*
       - [ ] `uri`  *Not Planned*
       - [ ] `uri-reference`  *Not Planned*
       - [ ] `iri`  *Not Planned*
       - [ ] `iri-reference`  *Not Planned*
       - [ ] `uri-template`  *Not Planned*
       - [ ] `json-pointer`  *Not Planned*
       - [ ] `relative-json-pointer`  *Not Planned*
       - [ ] `regex`  *Not Planned*

- [ ] `Object`  *Not Planned*
   - [ ] `properties`  *Not Planned*
   - [ ] `patternProperties`  *Not Planned*
   - [ ] `additionalProperties`  *Not Planned*
   - [ ] `required`  *Not Planned*
   - [ ] `unevaluatedProperties`  *Not Planned*
   - [ ] `propertyNames`  *Not Planned*
       - [ ] `pattern`  *Not Planned*
   - [ ] `minProperties`  *Not Planned*
   - [ ] `maxProperties`  *Not Planned*

- [ ] `array`  *Not Planned*
   - [ ] `items`  *Not Planned*
   - [ ] `prefixItems`  *Not Planned*
   - [ ] `contains`  *Not Planned*
   - [ ] `minContains`  *Not Planned*
   - [ ] `maxContains`  *Not Planned*
   - [ ] `minItems`  *Not Planned*
   - [ ] `maxItems`  *Not Planned*
   - [ ] `uniqueItems`  *Not Planned*

- [ ] multiple types (eg `{"type": ["number", "string"]})  *Not Planned*
- [ ] `deprecated`  *Not Planned*
- [ ] `examples`  *Not Planned*