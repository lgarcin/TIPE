from skimage.morphology import binary_opening, disk, square, binary_closing
from skimage.io import imread, imshow
from matplotlib import pyplot as plt
from skimage.color import rgb2gray

image = rgb2gray(imread('empreinte.png'))
print(image)
image = (image > .5)
print(image)
imshow(image, cmap=plt.cm.gray)
plt.show()
im = binary_closing(image, disk(1))
print(im)
imshow(im)
plt.show()
