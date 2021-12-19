extends Node2D


var particle = preload("res://Particle.tscn")
var rng = RandomNumberGenerator.new()
var gbest: Vector2
var gbest_obj: float = INF
var c1 = .1
var c2 = .2
var w = .8

func _ready():
	rng.randomize()
	for i in 50:
		var new_particle = particle.instance()
		var pos = Vector2(rng.randf_range(0.0, 1000.0), rng.randf_range(0.0, 600.0))
		var obj = objective_function(pos)
		new_particle.global_position = pos
		new_particle.pbest = pos
		new_particle.pbest_obj = obj
		if obj < gbest_obj:
			gbest = pos
			gbest_obj = obj
		add_child(new_particle)

func _physics_process(delta):
	for particle in get_children():
		if particle is Particle:
			var obj = objective_function(particle.global_position)
			if obj < particle.pbest_obj:
				particle.pbest=particle.global_position
				particle.pbest_obj=obj
			if obj<gbest_obj:
				gbest=particle.pbest
				gbest_obj=obj
			particle.velocity=w*particle.velocity+c1*rng.randf()*(particle.pbest-particle.global_position)+c2*rng.randf()*(gbest-particle.global_position)


#func _process(delta):
#	pass

func objective_function(v: Vector2):
	return abs(v.x)+abs(v.y-300)
