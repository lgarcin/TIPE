import numpy as np

graph = {
    'vertices': range(4),
    'edges': {
        (0, 1): (0, 1),
        (1, 3): (1, 0),
        (0, 2): (1, 0),
        (2, 3): (0, 1),
        (2, 1): (0, 0)
    },
    'source': 0,
    'sink': 3
}

N = len(graph['edges'])
C = np.zeros((N, N))
for i, e in enumerate(graph['edges']):
    C[i, i] = graph['edges'][e][0]
b = np.zeros((N, 1))
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
f = np.zeros((P, 1))
f[graph['source']] = 1
f[graph['sink']] = -1

Q = np.bmat([[C, A.T], [A, np.zeros((P, P))]])
c = np.bmat([[-b], [f]])
flow_selfish = (np.linalg.pinv(Q) * c)[:N]
time_selfish = sum(C * flow_selfish + b)
Q = np.bmat([[2 * C, A.T], [A, np.zeros((P, P))]])
flow_social = (np.linalg.pinv(Q) * c)[:N]
time_social = sum(C * flow_social + b)
print(time_selfish/time_social)