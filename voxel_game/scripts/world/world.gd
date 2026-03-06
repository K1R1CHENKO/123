extends Node3D
class_name VoxelWorld

const VIEW_DISTANCE := 3

var generator := WorldGenerator.new(2025)
var chunks: Dictionary = {}
var blocks: Dictionary = {}
var player: Node3D
var save_system := SaveSystem.new()

func _process(_delta: float) -> void:
	if player:
		ensure_chunks_around(player.global_position)

func world_to_chunk(pos: Vector3i) -> Vector2i:
	return Vector2i(floori(float(pos.x) / Chunk.CHUNK_SIZE), floori(float(pos.z) / Chunk.CHUNK_SIZE))

func get_block(pos: Vector3i) -> int:
	if pos.y < 0 or pos.y >= Chunk.CHUNK_HEIGHT:
		return BlockRegistry.AIR
	if blocks.has(pos):
		return blocks[pos]
	return generator.get_block(pos.x, pos.y, pos.z)

func set_block(pos: Vector3i, block_id: int) -> void:
	if pos.y < 0 or pos.y >= Chunk.CHUNK_HEIGHT:
		return
	blocks[pos] = block_id
	_refresh_chunk_and_neighbors(pos)

func remove_block(pos: Vector3i) -> int:
	var old := get_block(pos)
	set_block(pos, BlockRegistry.AIR)
	return old

func get_surface_height(x: int, z: int) -> int:
	for y in range(Chunk.CHUNK_HEIGHT - 1, 0, -1):
		if get_block(Vector3i(x, y, z)) != BlockRegistry.AIR:
			return y
	return 1

func ensure_chunks_around(world_pos: Vector3) -> void:
	var center := world_to_chunk(Vector3i(world_pos.x, 0, world_pos.z))
	var needed := {}
	for dx in range(-VIEW_DISTANCE, VIEW_DISTANCE + 1):
		for dz in range(-VIEW_DISTANCE, VIEW_DISTANCE + 1):
			var cc := Vector2i(center.x + dx, center.y + dz)
			needed[cc] = true
			if not chunks.has(cc):
				_load_chunk(cc)
	for cc in chunks.keys():
		if not needed.has(cc):
			_unload_chunk(cc)

func _load_chunk(coord: Vector2i) -> void:
	var chunk := Chunk.new()
	chunk.chunk_coord = coord
	chunk.world = self
	chunk.position = Vector3(coord.x * Chunk.CHUNK_SIZE, 0, coord.y * Chunk.CHUNK_SIZE)
	add_child(chunk)
	chunks[coord] = chunk
	_generate_trees_for_chunk(coord)
	chunk.rebuild_mesh()

func _generate_trees_for_chunk(coord: Vector2i) -> void:
	var origin := Vector3i(coord.x * Chunk.CHUNK_SIZE, 0, coord.y * Chunk.CHUNK_SIZE)
	for p in generator.get_tree_positions(origin, Chunk.CHUNK_SIZE):
		if get_block(p) != BlockRegistry.AIR:
			continue
		for i in 4:
			blocks[Vector3i(p.x, p.y + i, p.z)] = BlockRegistry.LOG
		for lx in range(-2, 3):
			for ly in range(2, 5):
				for lz in range(-2, 3):
					var leaf_pos := Vector3i(p.x + lx, p.y + ly, p.z + lz)
					if abs(lx) + abs(lz) <= 3 and get_block(leaf_pos) == BlockRegistry.AIR:
						blocks[leaf_pos] = BlockRegistry.LEAVES

func _unload_chunk(coord: Vector2i) -> void:
	var chunk: Chunk = chunks[coord]
	chunk.queue_free()
	chunks.erase(coord)

func _refresh_chunk_and_neighbors(pos: Vector3i) -> void:
	var base := world_to_chunk(pos)
	for x in range(-1, 2):
		for z in range(-1, 2):
			var cc := Vector2i(base.x + x, base.y + z)
			if chunks.has(cc):
				(chunks[cc] as Chunk).rebuild_mesh()

func load_world() -> void:
	blocks = save_system.load_blocks()

func save_world() -> void:
	save_system.save_blocks(blocks)
