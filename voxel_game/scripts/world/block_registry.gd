extends RefCounted
class_name BlockRegistry

const AIR := 0
const GRASS := 1
const DIRT := 2
const STONE := 3
const LOG := 4
const LEAVES := 5
const COAL_ORE := 6
const TORCH := 7
const PLANK := 8

static var _blocks := {
	AIR: {"name": "Air", "solid": false, "color": Color(0, 0, 0, 0), "light": 0},
	GRASS: {"name": "Grass", "solid": true, "color": Color(0.30, 0.8, 0.25), "light": 0},
	DIRT: {"name": "Dirt", "solid": true, "color": Color(0.45, 0.28, 0.13), "light": 0},
	STONE: {"name": "Stone", "solid": true, "color": Color(0.5, 0.5, 0.52), "light": 0},
	LOG: {"name": "Log", "solid": true, "color": Color(0.42, 0.27, 0.12), "light": 0},
	LEAVES: {"name": "Leaves", "solid": true, "color": Color(0.19, 0.52, 0.18, 0.85), "light": 0},
	COAL_ORE: {"name": "Coal Ore", "solid": true, "color": Color(0.15, 0.15, 0.15), "light": 0},
	TORCH: {"name": "Torch", "solid": true, "color": Color(0.95, 0.75, 0.2), "light": 12},
	PLANK: {"name": "Plank", "solid": true, "color": Color(0.72, 0.52, 0.28), "light": 0}
}

static func get_block_data(block_id: int) -> Dictionary:
	return _blocks.get(block_id, _blocks[AIR])

static func is_solid(block_id: int) -> bool:
	return get_block_data(block_id).get("solid", false)

static func color(block_id: int) -> Color:
	return get_block_data(block_id).get("color", Color.WHITE)

static func light(block_id: int) -> int:
	return get_block_data(block_id).get("light", 0)

static func all_placeable() -> Array[int]:
	return [GRASS, DIRT, STONE, LOG, LEAVES, COAL_ORE, TORCH, PLANK]
