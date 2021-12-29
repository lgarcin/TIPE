extends Node2D


var particle = preload("res://Particle.tscn")
var rng = RandomNumberGenerator.new()
var gbest: Vector2
var gbest_obj: float = INF
var c1 = .1
var c2 = .1
var w = .8

func _ready():
	rng.randomize()
	for i in 10:
		for j in 6:
			var new_particle = particle.instance()
			var pos = Vector2((i+1)*100,j*100)
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
			#particle.velocity=w*particle.velocity+c1*rng.randf()*(particle.pbest-particle.global_position)+c2*rng.randf()*(gbest-particle.global_position)
			particle.velocity=w*particle.velocity+c1*rng.randf()*derivative(particle.global_position)+c2*rng.randf()*(gbest-particle.global_position)


#func _process(delta):
#	pass

func objective_function(v: Vector2):
	return v.distance_to(Vector2(0,300))
	#return abs(v.x)+abs(v.y-300)

func derivative(v: Vector2):
	var dx=objective_function(v+Vector2(1,0))-objective_function(v+Vector2(-1,0))
	var dy=objective_function(v+Vector2(0,1))-objective_function(v+Vector2(0,-1))
	return -100*Vector2(dx,dy)
