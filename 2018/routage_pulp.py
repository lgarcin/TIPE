from pulp import *

graph = {
    'vertices': {'A', 'B', 'C', 'D'},
    'edges': {
        ('A', 'B'): lambda x: 1,
        ('B', 'D'): lambda x: x,
        ('A', 'C'): lambda x: x,
        ('C', 'D'): lambda x: 1,
        ('C', 'B'): lambda x: 0
    }
}

prob = LpProblem('routage', LpMinimize)

flows = LpVariable.dicts('flows', graph['edges'], lowBound=0, upBound=1, cat='Continuous')
prob += lpSum(graph['edges'][e](flows[e]) for e in graph['edges'])

for v in graph['vertices']:
    prob += lpSum(flows[e] for e in graph['edges'] if e[0] == v) + (1 if v == 'D' else 0) == \
            lpSum(flows[e] for e in graph['edges'] if e[1] == v) + (1 if v == 'A' else 0)

sol = prob.solve()
print(LpStatus[sol])
for e in graph['edges']:
    print(e, value(flows[e]))
