from skimage.data import camera, moon
from skimage.exposure import cumulative_distribution
from skimage.io import imshow, show
from numpy import vectorize

im_camera = camera()
im_moon = moon()
dist_camera, bins = cumulative_distribution(im_camera)
dist_moon, bins = cumulative_distribution(im_moon)


def rechercher_transformation(dist_source, dist_target):
    nb_source = len(dist_source)
    nb_target = len(dist_target)
    transformation = [0] * nb_source
    i, j = 0, 0
    while i < nb_source and j < nb_target:
        while dist_source[i] < dist_target[j]:
            transformation[i] = j
            i += 1
        j += 1
    return transformation


def appliquer_transformation(image, transformation):
    tr = vectorize(lambda color: transformation[color])
    return tr(image)


def egalisation(image):
    dist_image, bins = cumulative_distribution(image)
    nb = len(dist_image)
    transfo = rechercher_transformation(dist_image, [dist_image[k] / nb for k in range(nb)])
    return appliquer_transformation(image, transfo)


def match(im_source, im_target):
    dist_source, bins = cumulative_distribution(im_source)
    dist_target, bins = cumulative_distribution(im_target)
    transfo = rechercher_transformation(dist_source, dist_target)
    return appliquer_transformation(im_source, transfo)


im_trans = match(im_moon, im_camera)
im_trans = egalisation(im_moon)

imshow(im_trans, cmap='gray')
show()
