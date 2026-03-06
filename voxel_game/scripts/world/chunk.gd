extends Node3D
class_name Chunk

const CHUNK_SIZE := 16
const CHUNK_HEIGHT := 64

var chunk_coord: Vector2i
var world: VoxelWorld

var _mesh_instance := MeshInstance3D.new()
var _static_body := StaticBody3D.new()
var _collision_shape := CollisionShape3D.new()

const FACES = [
	{"dir": Vector3i(1, 0, 0), "v": [Vector3(1,0,0), Vector3(1,1,0), Vector3(1,1,1), Vector3(1,0,1)]},
	{"dir": Vector3i(-1, 0, 0), "v": [Vector3(0,0,1), Vector3(0,1,1), Vector3(0,1,0), Vector3(0,0,0)]},
	{"dir": Vector3i(0, 1, 0), "v": [Vector3(0,1,1), Vector3(1,1,1), Vector3(1,1,0), Vector3(0,1,0)]},
	{"dir": Vector3i(0, -1, 0), "v": [Vector3(0,0,0), Vector3(1,0,0), Vector3(1,0,1), Vector3(0,0,1)]},
	{"dir": Vector3i(0, 0, 1), "v": [Vector3(1,0,1), Vector3(1,1,1), Vector3(0,1,1), Vector3(0,0,1)]},
	{"dir": Vector3i(0, 0, -1), "v": [Vector3(0,0,0), Vector3(0,1,0), Vector3(1,1,0), Vector3(1,0,0)]}
]

func _ready() -> void:
	add_child(_mesh_instance)
	add_child(_static_body)
	_static_body.add_child(_collision_shape)
	_mesh_instance.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON

func rebuild_mesh() -> void:
	var vertices := PackedVector3Array()
	var colors := PackedColorArray()
	var normals := PackedVector3Array()
	var indices := PackedInt32Array()
	var idx := 0
	for lx in CHUNK_SIZE:
		for ly in CHUNK_HEIGHT:
			for lz in CHUNK_SIZE:
				var gx := chunk_coord.x * CHUNK_SIZE + lx
				var gz := chunk_coord.y * CHUNK_SIZE + lz
				var pos := Vector3i(gx, ly, gz)
				var block := world.get_block(pos)
				if block == BlockRegistry.AIR:
					continue
				for face in FACES:
					var neighbor := pos + face.dir
					if BlockRegistry.is_solid(world.get_block(neighbor)):
						continue
					var light_boost := BlockRegistry.light(block) / 16.0
					var c := BlockRegistry.color(block).lightened(light_boost)
					for v in face.v:
						vertices.append(Vector3(lx, ly, lz) + v)
						colors.append(c)
						normals.append(Vector3(face.dir))
					indices.append_array([idx, idx + 1, idx + 2, idx, idx + 2, idx + 3])
					idx += 4
	var mesh := ArrayMesh.new()
	if vertices.size() > 0:
		var arrays := []
		arrays.resize(Mesh.ARRAY_MAX)
		arrays[Mesh.ARRAY_VERTEX] = vertices
		arrays[Mesh.ARRAY_COLOR] = colors
		arrays[Mesh.ARRAY_NORMAL] = normals
		arrays[Mesh.ARRAY_INDEX] = indices
		mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
		var material := StandardMaterial3D.new()
		material.vertex_color_use_as_albedo = true
		material.roughness = 1.0
		mesh.surface_set_material(0, material)
	_mesh_instance.mesh = mesh
	if vertices.size() > 0:
		_collision_shape.shape = mesh.create_trimesh_shape()
	else:
		_collision_shape.shape = null
