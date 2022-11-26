all: typecheck fmt lint

typecheck:
	mypy ./gltf_ecs_components

lint:
	flake8 ./gltf_ecs_components
	pylint ./gltf_ecs_components --disable=I1101

fmt:
	black ./gltf_ecs_components
