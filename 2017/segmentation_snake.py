from skimage.draw import circle_perimeter
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.data import camera
import numpy as np
import matplotlib.pyplot as plt

img = camera()
lx, ly = img.shape
img = gaussian(img, 3)

s = np.linspace(0, 2 * np.pi, 100)
init = np.array([np.cos(s) * (lx / 2.) + lx / 2., np.sin(s) * (ly / 2.) + ly / 2.]).T

snake = active_contour(img, init, w_edge=10, w_line=0, alpha=0.1, beta=.001)
plt.plot(snake[:, 0], snake[:, 1])
plt.imshow(img, cmap='gray')
plt.show()
