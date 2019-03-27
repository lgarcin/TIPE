graphe = [[1, 2], [3, 4], [4], [5], [5], [6, 7], [8], [8], []]


def liste_chemins(graphe, source):
    if not graphe[source]:
        return [[source]]
    return [[source] + l for v in graphe[source] for l in liste_chemins(graphe, v)]


print(liste_chemins(graphe, 0))
