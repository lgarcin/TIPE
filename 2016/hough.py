# -*- coding: utf-8 -*-
'''
Transformée de Hough pour la détection de segments de droites
'''

from skimage.transform import hough_line
from skimage import data
from skimage import exposure, feature

import numpy as np
import matplotlib.pyplot as plt

# Chargement ou construction d'une image
image = data.checkerboard()
# image = np.zeros((200, 200))
# image[40:160, 40:160] = 255
# image[70:130, 70:130] = 0

# Détection des contours
edges = feature.canny(image, 2, 1, 25)

# Calcul de la transformée de Hough
h, theta, d = hough_line(edges, theta=np.linspace(-np.pi, np.pi, 200))

plt.figure()

# Affichage de l'image initiale
plt.subplot(221)
plt.imshow(image)
plt.title('Image initiale')

# Affichage des contours
plt.gray()
plt.subplot(222)
plt.imshow(edges)
plt.title('Contours')

# Affichage de la transformée de Hough
plt.subplot(223)
plt.imshow(exposure.equalize_hist(h * 1.), extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]],
           aspect=1. / 3.)
plt.title('Transformée de Hough')
plt.xlabel('Angles (degrés)')
plt.ylabel('Distance (pixels)')

# Détection des maxima locaux de la transformée de Hough
lm = feature.peak_local_max(h, min_distance=20, threshold_rel=.5)

# Affichage de l'image puis des droites détectées
plt.subplot(224)
plt.imshow(image)
axes = plt.gcf().gca()
dist = np.sqrt(image.shape[0] ** 2 + image.shape[1] ** 2)
for m in lm:
    t, r = theta[m[1]], d[m[0]]
    M1 = [r * np.cos(t) - dist * np.sin(t), r * np.cos(t) + dist * np.sin(t)]
    M2 = [r * np.sin(t) + dist * np.cos(t), r * np.sin(t) - dist * np.cos(t)]
    line = plt.Line2D(M1, M2)
    axes.add_artist(line)
plt.title('Droites détectées')

plt.show()
