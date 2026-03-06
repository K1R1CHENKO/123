extends RefCounted
class_name CraftingSystem

signal crafted(message: String)

var recipes := [
	{"in": {BlockRegistry.LOG: 1}, "out": {"id": BlockRegistry.PLANK, "count": 4}, "name": "Planks"},
	{"in": {BlockRegistry.PLANK: 2}, "out": {"id": BlockRegistry.TORCH, "count": 2}, "name": "Torches"}
]

func craft_first_available(inventory: Inventory) -> void:
	for recipe in recipes:
		if _has_items(inventory, recipe["in"]):
			_consume_items(inventory, recipe["in"])
			inventory.add_item(recipe["out"]["id"], recipe["out"]["count"])
			emit_signal("crafted", "Crafted %s x%d" % [recipe["name"], recipe["out"]["count"]])
			return
	emit_signal("crafted", "No matching recipe")

func _has_items(inventory: Inventory, required: Dictionary) -> bool:
	for req_id in required.keys():
		var need: int = required[req_id]
		var have := 0
		for slot in inventory.slots:
			if slot["id"] == req_id:
				have += int(slot["count"])
		if have < need:
			return false
	return true

func _consume_items(inventory: Inventory, required: Dictionary) -> void:
	for req_id in required.keys():
		var remaining: int = required[req_id]
		for slot in inventory.slots:
			if slot["id"] != req_id or remaining <= 0:
				continue
			var take := mini(remaining, int(slot["count"]))
			slot["count"] -= take
			remaining -= take
			if slot["count"] <= 0:
				slot["id"] = BlockRegistry.AIR
	inventory.emit_signal("changed")
