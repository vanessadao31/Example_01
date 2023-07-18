# -*- coding: utf-8 -*-
"""
Finding which cells express protein signal and which do not
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import napari
import czifile
import time

from skimage.morphology import local_maxima
from skimage import data, measure, exposure, filters

import napari_segment_blobs_and_things_with_membranes as nsbatwm
import pyclesperanto_prototype as cle

from sklearn.cluster import KMeans
from skimage.segmentation import watershed

from k_initialise import my_voronoi_otsu_labeling, load_file, make_points

data_folder = Path("Data")
files = ["cover slip 35 image 3.czi",
        "coverslip 33 image 1.czi"]
num_channels = 2

nuclei = load_file(files[1], 0)
protein = load_file(files[1], 1)

# viewer = napari.Viewer()
# CH1 = viewer.add_image(nuclei, name='CH1')
# CH2 = viewer.add_image(protein, name='CH2')

sigma_spot_detection = 18 # lower number, more segmentation
sigma_outline = 10 # higher number, more gaussian blur applied
segmented_nuclei, number_nuclei, centroids = my_voronoi_otsu_labeling(nuclei, 
                                                 spot_sigma=sigma_spot_detection,
                                                 outline_sigma=sigma_outline)
# nuclei_labels = viewer.add_labels(segmented_nuclei)

points = make_points(protein, 'otsu')

reflect = [[0, 1], 
           [1, 0]]
reflected_points = np.matmul(points, reflect)
    
kmeans = KMeans(n_clusters=number_nuclei, init=centroids, max_iter=1).fit(reflected_points)
protein_labels = kmeans.labels_

features = {'cluster': protein_labels/protein_labels.max()}
# points_layer = viewer.add_points(points, features=features, size=5, face_color='cluster', face_colormap='prism')

test = np.zeros((1024, 1024))

for i in range(len(protein_labels)):
    test[reflected_points[i]] = protein_labels[i]

# maximum_distance = 15 # pixels

# # draw a parametric map of cell counts
# count_map = cle.proximal_other_labels_count_map(segmented_nuclei, test,
#                                                 maximum_distance=maximum_distance)

plt.imshow(test)