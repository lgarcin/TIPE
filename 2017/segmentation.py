from skimage.segmentation import slic
from skimage.data import astronaut

img = astronaut()
segments = slic(img, n_segments=100, compactness=1)

from skimage.io import imshow, show

imshow(segments)
show()
imshow(img)
show()
