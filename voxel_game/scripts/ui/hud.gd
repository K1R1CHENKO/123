extends Control
class_name HUD

@onready var hotbar_label: Label = $MarginContainer/VBoxContainer/Hotbar
@onready var crafting_label: Label = $MarginContainer/VBoxContainer/Crafting
@onready var info_label: Label = $MarginContainer/VBoxContainer/Info

var inventory: Inventory

func _ready() -> void:
	info_label.text = "LMB break | RMB place | C craft | Wheel select"

func bind_inventory(inv: Inventory) -> void:
	inventory = inv
	inventory.changed.connect(_refresh)
	_refresh()

func bind_crafting(crafting: CraftingSystem) -> void:
	crafting.crafted.connect(_on_crafted)

func _refresh() -> void:
	if inventory == null:
		return
	var lines: Array[String] = []
	for i in inventory.hotbar_size:
		var slot: Dictionary = inventory.slots[i]
		var marker := ">" if i == inventory.selected_hotbar else " "
		var name := BlockRegistry.get_block_data(slot["id"])["name"]
		lines.append("%s[%d] %s x%d" % [marker, i + 1, name, int(slot["count"])])
	hotbar_label.text = "Hotbar\n" + "\n".join(lines)

func _on_crafted(msg: String) -> void:
	crafting_label.text = msg
