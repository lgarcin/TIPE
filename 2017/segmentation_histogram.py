from skimage.exposure import histogram
from skimage.data import camera
from scipy.ndimage.measurements import label
from matplotlib.pyplot import plot, show, axis, savefig, subplot, imshow, figure, axvline, title, xlim, cm
import numpy as np

subplot(121)
axis('off')
img = camera()
imshow(img, cmap='gray')
title('Image')
subplot(122, aspect=.03)
axis('on')
hist, bins = histogram(img)
xlim([min(bins), max(bins)])
plot(bins, hist)
title('Histogramme')
savefig('camera_hist.jpeg', bbox_inches='tight')

figure()
subplot(121)
axis('off')
seg = np.vectorize(lambda x: int(x < 50) + int(x < 140))(img)
imshow(seg)
title('Image segmentée')
subplot(122, aspect=.03)
axis('on')
xlim([min(bins), max(bins)])
plot(bins, hist)
axvline(50, color='r')
axvline(140, color='r')
title("Découpage de l'histogramme")
savefig('camera_seg.jpeg', bbox_inches='tight')

figure()
labeled_array, num_features = label(seg)
print(num_features)
imshow(labeled_array, cmap=cm.jet)
show()
