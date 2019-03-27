import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import binary_erosion, disk

n = 1024
r = 500
cx, cy = n / 2, n / 2
img = np.zeros((n, n), dtype=bool)
x, y = np.ogrid[-cx:n - cx, -cy:n - cy]
img[x * y <= 0] = True

for _ in range(200):
    img = np.logical_or(np.logical_and((np.random.random((n, n)) < .1), img), binary_erosion(img, disk(1)))
plt.imshow(binary_erosion(img, disk(1)), cmap='Greys')
plt.show()
