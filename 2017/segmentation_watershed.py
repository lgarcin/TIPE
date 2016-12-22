import numpy as np
import matplotlib.pyplot as plt
from skimage import io as io
from skimage import color as color
from skimage import filters as filters
from scipy import ndimage
from skimage import data as data

from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage.measure import regionprops, label

image = color.rgb2gray(data.coins())
image = image < filters.threshold_otsu(image)

distance = ndimage.distance_transform_edt(image)

# Here's one way to measure the number of coins directly
# from the distance map
coin_centres = (distance > 0.8 * distance.max())
print('Number of coins (method 1):', np.max(label(coin_centres)))

# Or you can proceed with the watershed labeling
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
                            labels=image)


markers, num_features = ndimage.label(local_maxi)
labels = watershed(-distance, markers, mask=image)

# ...but then you have to clean up the tiny intersections between coins
regions = regionprops(labels)
regions = [r for r in regions if r.area > 50]

print('Number of coins (method 2):', len(regions) - 1)

fig, axes = plt.subplots(ncols=3, figsize=(8, 2.7))
ax0, ax1, ax2 = axes

ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax0.set_title('Overlapping objects')
ax1.imshow(-distance, cmap=plt.cm.jet, interpolation='nearest')
ax1.set_title('Distances')
ax2.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest')
ax2.set_title('Separated objects')

for ax in axes:
    ax.axis('off')

fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                    right=1)
plt.show()