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
files = ["cover slip 35 image 3.czi", "coverslip 33 image 1.czi"]
num_channels = 2

for file in files:
    nuclei = load_file(file, 0)
    protein = load_file(file, 1)
        
    viewer = napari.Viewer()
    CH1 = viewer.add_image(nuclei, name='CH1')
    CH2 = viewer.add_image(protein, name='CH2')
        
    sigma_spot_detection = 18 # lower number, more segmentation
    sigma_outline = 10 # higher number, more gaussian blur applied
    segmented_nuclei, number_nuclei, centroids = my_voronoi_otsu_labeling(nuclei, 
                                                         spot_sigma=sigma_spot_detection,
                                                         outline_sigma=sigma_outline)
    nuclei_labels = viewer.add_labels(segmented_nuclei)
    reflected_points = make_points(protein, 'li')
    reflect = [[0, 1], 
               [1, 0]]
    points = np.matmul(reflected_points, reflect)
            
    kmeans = KMeans(n_clusters=number_nuclei, init=centroids, max_iter=1).fit(points)
    protein_labels = kmeans.labels_
        
    features = {'cluster': protein_labels/protein_labels.max()}
    points_layer = viewer.add_points(reflected_points, name='protein_points', features=features, size=5, face_color='cluster', face_colormap='prism')
        
    test = np.zeros((1024, 1024))
        
    for i in range(len(protein_labels)):
        test[points[i, 0], points[i, 1]] = protein_labels[i]
        
    maximum_distance = 50 # pixels
        
    # draw a parametric map of cell counts
    count_map = cle.proximal_other_labels_count_map(segmented_nuclei, test,
                                                        maximum_distance=maximum_distance)
            
    pos_nuclei = cle.exclude_labels_with_map_values_out_of_range(
            count_map, segmented_nuclei, minimum_value_range=1)
    cle.imshow(pos_nuclei, labels=True)
    positive_nuclei = viewer.add_labels(pos_nuclei, name='positive_nuclei')
