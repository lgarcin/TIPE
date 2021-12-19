extends KinematicBody2D
class_name Particle

var velocity: Vector2
var pbest: Vector2
var pbest_obj: float

func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	velocity = move_and_slide(velocity)

#func _process(delta):
#	pass
