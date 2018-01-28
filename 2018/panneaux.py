from skimage.feature import canny
from skimage.transform import probabilistic_hough_line, hough_line, hough_line_peaks
from skimage.io import imread, imshow
from matplotlib.pyplot import show, plot, xlim, ylim
from skimage.color import rgb2gray
from numpy import pi, linspace, array, cos, sin

image = imread('03_034assr12signalisation_pan5.gif')
img = rgb2gray(image)
edges = canny(rgb2gray(img), sigma=1.)
imshow(edges)
show()


def plot_hough(angle, precision):
    lines = probabilistic_hough_line(edges,
                                     theta=linspace(angle - precision, angle + precision, 3),
                                     line_gap=0,
                                     line_length=10)
    for line in lines:
        p0, p1 = line
        plot((p0[0], p1[0]), (p0[1], p1[1]))


plot_hough(pi / 2, pi / 20)
plot_hough(pi / 6, pi / 20)
plot_hough(-pi / 6, pi / 20)
plot_hough(pi / 4, pi / 20)
plot_hough(-pi / 4, pi / 20)



imshow(edges)

show()

# hspace, angles, dists = hough_line(edges, theta=linspace(-pi / 2, pi / 2, 1000))
# imshow(hspace)
# show()

# hspace, angles, dists = hough_line_peaks(hspace, angles, dists)
# for i in range(len(hspace)):
#     print(hspace[i], angles[i] * 180 / pi, dists[i])
# imshow(img)
# for _, angle, dist in zip(hspace, angles, dists):
#     y0 = (dist - 0 * cos(angle)) / sin(angle)
#     y1 = (dist - img.shape[1] * cos(angle)) / sin(angle)
#     plot((0, img.shape[1]), (y0, y1), '-r')
# xlim((0, image.shape[1]))
# ylim((image.shape[0], 0))
#
# show()
