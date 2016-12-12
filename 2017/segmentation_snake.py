from skimage.draw import circle_perimeter
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import numpy as np
import matplotlib.pyplot as plt

img = np.zeros((100, 100))
rr, cc = circle_perimeter(35, 45, 25)
img[rr, cc] = 1
img = gaussian(img, 2)

s = np.linspace(0, 2 * np.pi, 100)
init = 50 * np.array([np.cos(s), np.sin(s)]).T + 50

snake = active_contour(img, init, w_edge=0, w_line=1)
plt.plot(snake[:, 0], snake[:, 1])
plt.imshow(img, cmap='gray')
plt.show()
