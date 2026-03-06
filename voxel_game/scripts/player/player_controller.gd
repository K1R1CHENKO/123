extends CharacterBody3D
class_name PlayerController

@export var move_speed := 8.0
@export var jump_velocity := 5.2
@export var gravity := 18.0
@export var mouse_sense := 0.002

@onready var camera: Camera3D = $Camera3D

var world: VoxelWorld
var inventory := Inventory.new()
var crafting_system := CraftingSystem.new()

var _pitch := 0.0

func _ready() -> void:
	_setup_input_actions()
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func set_world(w: VoxelWorld) -> void:
	world = w

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * mouse_sense)
		_pitch = clampf(_pitch - event.relative.y * mouse_sense, -1.55, 1.55)
		camera.rotation.x = _pitch
	if event.is_action_pressed("ui_cancel"):
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			inventory.scroll_hotbar(-1)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			inventory.scroll_hotbar(1)

func _physics_process(delta: float) -> void:
	var input_vec := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var dir := (transform.basis * Vector3(input_vec.x, 0, input_vec.y)).normalized()
	velocity.x = dir.x * move_speed
	velocity.z = dir.z * move_speed
	if not is_on_floor():
		velocity.y -= gravity * delta
	elif Input.is_action_just_pressed("jump"):
		velocity.y = jump_velocity
	if Input.is_action_just_pressed("break_block"):
		_break_block()
	if Input.is_action_just_pressed("place_block"):
		_place_block()
	if Input.is_action_just_pressed("craft"):
		crafting_system.craft_first_available(inventory)
	move_and_slide()

func _break_block() -> void:
	if world == null:
		return
	var hit := _raycast_block()
	if hit.is_empty():
		return
	var pos: Vector3i = hit["position"]
	var removed := world.remove_block(pos)
	if removed != BlockRegistry.AIR:
		inventory.add_item(removed, 1)

func _place_block() -> void:
	if world == null:
		return
	var hit := _raycast_block()
	if hit.is_empty():
		return
	var place_id := inventory.consume_selected()
	if place_id == BlockRegistry.AIR:
		return
	var pos: Vector3i = hit["position"] + hit["normal"]
	if pos.y < 0:
		return
	if Vector3(pos).distance_to(global_position) < 1.5:
		inventory.add_item(place_id, 1)
		return
	world.set_block(pos, place_id)

func _raycast_block() -> Dictionary:
	var from := camera.global_position
	var to := from + -camera.global_transform.basis.z * 7.0
	var q := PhysicsRayQueryParameters3D.create(from, to)
	q.collide_with_areas = false
	q.collide_with_bodies = true
	var result := get_world_3d().direct_space_state.intersect_ray(q)
	if result.is_empty():
		return {}
	var hit_pos: Vector3 = result.position - result.normal * 0.01
	return {
		"position": Vector3i(floor(hit_pos.x), floor(hit_pos.y), floor(hit_pos.z)),
		"normal": Vector3i(result.normal)
	}

func _setup_input_actions() -> void:
	var actions := {
		"move_forward": KEY_W,
		"move_back": KEY_S,
		"move_left": KEY_A,
		"move_right": KEY_D,
		"jump": KEY_SPACE,
		"break_block": MOUSE_BUTTON_LEFT,
		"place_block": MOUSE_BUTTON_RIGHT,
		"craft": KEY_C
	}
	for action in actions.keys():
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		if InputMap.action_get_events(action).is_empty():
			var event
			if action in ["break_block", "place_block"]:
				event = InputEventMouseButton.new()
				event.button_index = actions[action]
			else:
				event = InputEventKey.new()
				event.keycode = actions[action]
			InputMap.action_add_event(action, event)
