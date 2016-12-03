from skimage import data
from skimage.color import rgb2gray
from matplotlib.pyplot import imshow, show, gray, subplot, title
from numpy.linalg import svd
from numpy import zeros, diag, dot

image = rgb2gray(data.lena())
gray()
u, s, v = svd(image)
S = zeros(image.shape)

sizes = [10, 20, 30, 40, 50, 60, 70]

subplot(2, (len(sizes) + 2) // 2, 1)
title("Image initiale")
imshow(image)
for k in range(len(sizes)):
    S[:sizes[k], :sizes[k]] = diag(s[:sizes[k]])
    image = dot(u, dot(S, v))
    subplot(2, (len(sizes) + 2) // 2, k + 2)
    title(str(sizes[k]) + " valeurs singulières")
    imshow(image)
show()
