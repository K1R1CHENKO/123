extends RefCounted
class_name SaveSystem

const SAVE_PATH := "user://world_save.json"

func save_blocks(blocks: Dictionary) -> void:
	var serial := {}
	for key in blocks.keys():
		var p: Vector3i = key
		serial["%d,%d,%d" % [p.x, p.y, p.z]] = blocks[key]
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(serial))

func load_blocks() -> Dictionary:
	if not FileAccess.file_exists(SAVE_PATH):
		return {}
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return {}
	var raw := file.get_as_text()
	var parsed = JSON.parse_string(raw)
	if typeof(parsed) != TYPE_DICTIONARY:
		return {}
	var blocks := {}
	for key in parsed.keys():
		var parts := (key as String).split(",")
		if parts.size() != 3:
			continue
		blocks[Vector3i(parts[0].to_int(), parts[1].to_int(), parts[2].to_int())] = int(parsed[key])
	return blocks
