from pyomo.environ import *

model = AbstractModel()
model.vertices = Set()
model.edges = Set(model.vertices * model.vertices)
model.flows = Var(model.edges, within=NonNegativeReals, bounds=(0, 1))
