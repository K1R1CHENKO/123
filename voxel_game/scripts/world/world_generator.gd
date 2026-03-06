extends RefCounted
class_name WorldGenerator

var height_noise := FastNoiseLite.new()
var biome_noise := FastNoiseLite.new()
var cave_noise := FastNoiseLite.new()

func _init(seed_value: int = 1337) -> void:
	height_noise.seed = seed_value
	height_noise.frequency = 0.015
	height_noise.fractal_octaves = 4
	height_noise.fractal_gain = 0.5

	biome_noise.seed = seed_value + 77
	biome_noise.frequency = 0.004

	cave_noise.seed = seed_value + 133
	cave_noise.frequency = 0.03

func get_height(x: int, z: int) -> int:
	var biome_v := biome_noise.get_noise_2d(x, z)
	var base := 28 if biome_v < -0.2 else 34 if biome_v < 0.2 else 42
	var variation := int(height_noise.get_noise_2d(x, z) * 16.0)
	return clampi(base + variation, 8, 60)

func get_block(x: int, y: int, z: int) -> int:
	var h := get_height(x, z)
	if y > h:
		return BlockRegistry.AIR
	if y < h - 4:
		if y < h - 8 and randf() < 0.03:
			return BlockRegistry.COAL_ORE
		var cave_v := cave_noise.get_noise_3d(x, y, z)
		if y > 4 and cave_v > 0.35:
			return BlockRegistry.AIR
		return BlockRegistry.STONE
	if y < h:
		return BlockRegistry.DIRT
	return BlockRegistry.GRASS

func get_tree_positions(chunk_origin: Vector3i, chunk_size: int) -> Array[Vector3i]:
	var trees: Array[Vector3i] = []
	for lx in chunk_size:
		for lz in chunk_size:
			var gx := chunk_origin.x + lx
			var gz := chunk_origin.z + lz
			if hash(Vector2i(gx, gz)) % 97 == 0:
				var h := get_height(gx, gz)
				if h > 20:
					trees.append(Vector3i(gx, h + 1, gz))
	return trees
