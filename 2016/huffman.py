from collections import Counter
from heapq import heapify, heappop, heappush


def huffman_tree(occurrences):
    heap = [(occ, id(letter), letter) for (letter, occ) in occurrences.items()]
    heapify(heap)

    while len(heap) >= 2:
        occ1, id1, node1 = heappop(heap)
        occ2, id2, node2 = heappop(heap)
        value = {0: node1, 1: node2}
        heappush(heap, (occ1 + occ2, id(value), value))

    return heappop(heap)[2]


def huffman_dict_aux(d, tree, prefix):
    if len(tree) == 1:
        d[prefix] = tree
    else:
        for node in tree:
            huffman_dict_aux(d, tree[node], prefix + str(node))


def huffman_dict(tree):
    d = {}
    huffman_dict_aux(d, tree, '')
    return d

tree = huffman_tree(Counter("comment allez-vous ? tres bien et vous ?"))
d = huffman_dict(tree)
print(d)
