extends CharacterBody3D
class_name Mob

var world: VoxelWorld
var target: Node3D
var speed := 3.0
var gravity := 15.0
var wander_target := Vector3.ZERO
var attack_range := 1.4
var attack_timer := 0.0

func _ready() -> void:
	var body := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = Vector3(0.8, 1.6, 0.8)
	body.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.7, 0.2, 0.2)
	body.material_override = mat
	add_child(body)
	var collision := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.height = 1.2
	shape.radius = 0.4
	collision.shape = shape
	add_child(collision)
	_pick_wander_target()

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= gravity * delta
	else:
		velocity.y = 0.0
	attack_timer -= delta
	var dir := Vector3.ZERO
	if target and global_position.distance_to(target.global_position) < 14.0:
		dir = (target.global_position - global_position)
		dir.y = 0
		dir = dir.normalized()
		if global_position.distance_to(target.global_position) < attack_range and attack_timer <= 0.0:
			attack_timer = 1.0
	else:
		if global_position.distance_to(wander_target) < 1.0:
			_pick_wander_target()
		dir = (wander_target - global_position)
		dir.y = 0
		dir = dir.normalized()
	velocity.x = dir.x * speed
	velocity.z = dir.z * speed
	move_and_slide()

func _pick_wander_target() -> void:
	wander_target = global_position + Vector3(randf_range(-6, 6), 0, randf_range(-6, 6))
