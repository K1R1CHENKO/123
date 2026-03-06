extends Node3D

@onready var world: VoxelWorld = $World
@onready var player: PlayerController = $Player
@onready var hud: HUD = $CanvasLayer/HUD
@onready var sun: DirectionalLight3D = $Sun

var time_of_day := 0.2
var day_speed := 0.01

func _ready() -> void:
	player.set_world(world)
	hud.bind_inventory(player.inventory)
	hud.bind_crafting(player.crafting_system)
	world.player = player
	world.load_world()
	world.ensure_chunks_around(player.global_position)
	_spawn_mobs(8)

func _process(delta: float) -> void:
	time_of_day = fmod(time_of_day + delta * day_speed, 1.0)
	var angle := lerp(-30.0, 330.0, time_of_day)
	sun.rotation_degrees = Vector3(angle, -35.0, 0.0)
	sun.light_energy = clampf(sin(time_of_day * TAU) * 1.2 + 0.3, 0.05, 1.2)

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		world.save_world()

func _spawn_mobs(count: int) -> void:
	var mob_scene: PackedScene = preload("res://scenes/mob.tscn")
	for i in count:
		var mob := mob_scene.instantiate() as Mob
		var x := randi_range(-32, 32)
		var z := randi_range(-32, 32)
		var y := world.get_surface_height(x, z) + 2
		mob.global_position = Vector3(x, y, z)
		mob.world = world
		mob.target = player
		add_child(mob)
