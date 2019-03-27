import quadprog as qp
import numpy as np

graph = {
    'vertices': range(4),
    'edges': {
        (0, 1): (1, 1),
        (1, 3): (1, 0),
        (0, 2): (2, 0),
        (2, 3): (1, 1),
        (2, 1): (1, 10)
    },
    'source': 0,
    'sink': 3
}

N = len(graph['edges'])
C = np.zeros((N, N))
for i, e in enumerate(graph['edges']):
    C[i, i] = graph['edges'][e][0]
b = np.zeros((N,))
for i, e in enumerate(graph['edges']):
    b[i] = graph['edges'][e][1]

P = len(graph['vertices'])
A = np.zeros((P, N))
for i in graph['vertices']:
    for j, e in enumerate(graph['edges']):
        if e[0] == i:
            A[i, j] = 1
        if e[1] == i:
            A[i, j] = -1
f = np.zeros((P,))
f[graph['source']] = 1
f[graph['sink']] = -1

print(qp.solve_qp(
    C, -b, np.vstack([A, np.eye(N)]).T, np.hstack([f, np.zeros(N)]), P)[0])
