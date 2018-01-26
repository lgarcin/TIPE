from numpy import ndarray, where, nonzero, sqrt, zeros, logical_and, linspace, max, argmax, unravel_index
from skimage.draw import line
from skimage.io import imshow, imread
from matplotlib.pyplot import show
from skimage.feature import peak_local_max, canny
from skimage.color import rgb2gray


def triangle_sommets(r, c, distance):
    return (r - 2 * distance, c), (r + distance, c - distance * sqrt(3)), (r + distance, c + distance * sqrt(3))


def display_triangle(im, tr, col):
    rows, cols = im.shape
    rr, cc = line(*map(int, tr[0]), *map(int, tr[1]))
    ind = logical_and.reduce((rr >= 0, rr < rows, cc >= 0, cc < cols))
    rr, cc = rr[ind], cc[ind]
    im[rr, cc] = col
    rr, cc = line(*map(int, tr[1]), *map(int, tr[2]))
    ind = logical_and.reduce((rr >= 0, rr < rows, cc >= 0, cc < cols))
    rr, cc = rr[ind], cc[ind]
    im[rr, cc] = col
    rr, cc = line(*map(int, tr[2]), *map(int, tr[0]))
    ind = logical_and.reduce((rr >= 0, rr < rows, cc >= 0, cc < cols))
    rr, cc = rr[ind], cc[ind]
    im[rr, cc] = col


def triangle_hough(edges, sizes):
    nb_lignes, nb_colonnes = edges.shape
    accumulator = zeros((nb_lignes, nb_colonnes, len(sizes) - 1))
    lx, ly = nonzero(edges)
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            x1, y1 = ly - j, lx - i
            x2, y2 = -x1 / 2 - y1 * sqrt(3) / 2, x1 * sqrt(3) / 2 - y1 / 2
            x3, y3 = -x1 / 2 + y1 * sqrt(3) / 2, -x1 * sqrt(3) / 2 - y1 / 2
            for s in range(len(sizes) - 1):
                a1 = logical_and(sizes[s] <= y1, y1 < sizes[s + 1])
                a2 = logical_and(sizes[s] <= y2, y2 < sizes[s + 1])
                a3 = logical_and(sizes[s] <= y3, y3 < sizes[s + 1])
                b1 = y1 < max(sizes[s], sizes[s + 1])
                b2 = y2 < max(sizes[s], sizes[s + 1])
                b3 = y3 < max(sizes[s], sizes[s + 1])
                accumulator[i, j, s] += sum(logical_and.reduce((a1, b2, b3)))
                accumulator[i, j, s] += sum(logical_and.reduce((a2, b3, b1)))
                accumulator[i, j, s] += sum(logical_and.reduce((a3, b1, b2)))
    return accumulator


def triangle_hough_bis(edges, sizes):
    nb_lignes, nb_colonnes = edges.shape
    accumulator = zeros((nb_lignes, nb_colonnes, len(sizes)))
    for i in range(nb_lignes):
        print(str(i + 1) + " / " + str(nb_colonnes))
        for j in range(nb_colonnes):
            for s in range(len(sizes)):
                tr = triangle_sommets(i, j, sizes[s])
                rr, cc = line(*map(int, tr[0]), *map(int, tr[1]))
                ind = logical_and.reduce((rr >= 0, rr < nb_lignes, cc >= 0, cc < nb_colonnes))
                rr, cc = rr[ind], cc[ind]
                accumulator[i, j, s] += sum(edges[rr, cc])
                rr, cc = line(*map(int, tr[1]), *map(int, tr[2]))
                ind = logical_and.reduce((rr >= 0, rr < nb_lignes, cc >= 0, cc < nb_colonnes))
                rr, cc = rr[ind], cc[ind]
                accumulator[i, j, s] += sum(edges[rr, cc])
                rr, cc = line(*map(int, tr[2]), *map(int, tr[0]))
                ind = logical_and.reduce((rr >= 0, rr < nb_lignes, cc >= 0, cc < nb_colonnes))
                rr, cc = rr[ind], cc[ind]
                accumulator[i, j, s] += sum(edges[rr, cc])
    return accumulator


image = imread('03_034assr12signalisation_pan5.gif')
img = rgb2gray(image)
edges = canny(rgb2gray(img), sigma=1.)

# edges = zeros((100, 200))
# tr = triangle_sommets(60, 130, 15)
# display_triangle(edges, tr, 1)

sizes = linspace(10, 40, 10)
acc = triangle_hough_bis(edges, sizes)
for r, c, ind in peak_local_max(acc, threshold_rel=.9):
    tr = triangle_sommets(r, c, sizes[ind])
    print(r, c, sizes[ind], acc[r, c, ind])
    display_triangle(edges, tr, 128)

imshow(edges)
show()
