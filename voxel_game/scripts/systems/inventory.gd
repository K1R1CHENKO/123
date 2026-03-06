extends Resource
class_name Inventory

signal changed

var slot_count := 24
var hotbar_size := 8
var slots: Array[Dictionary] = []
var selected_hotbar := 0

func _init() -> void:
	for i in slot_count:
		slots.append({"id": BlockRegistry.AIR, "count": 0})
	var placeable := BlockRegistry.all_placeable()
	for i in placeable.size():
		slots[i] = {"id": placeable[i], "count": 64}

func add_item(block_id: int, count: int = 1) -> void:
	for slot in slots:
		if slot["id"] == block_id and slot["count"] < 99:
			slot["count"] += count
			emit_signal("changed")
			return
	for slot in slots:
		if slot["count"] == 0:
			slot["id"] = block_id
			slot["count"] = count
			emit_signal("changed")
			return

func consume_selected() -> int:
	var slot: Dictionary = slots[selected_hotbar]
	if slot["count"] <= 0:
		return BlockRegistry.AIR
	slot["count"] -= 1
	var id := int(slot["id"])
	if slot["count"] == 0:
		slot["id"] = BlockRegistry.AIR
	emit_signal("changed")
	return id

func selected_block() -> int:
	var slot: Dictionary = slots[selected_hotbar]
	return int(slot["id"]) if slot["count"] > 0 else BlockRegistry.AIR

func scroll_hotbar(direction: int) -> void:
	selected_hotbar = posmod(selected_hotbar + direction, hotbar_size)
	emit_signal("changed")
