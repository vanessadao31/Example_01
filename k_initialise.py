# -*- coding: utf-8 -*-
"""
Trying to cluster points to parents nuclei using k-means but providng the centre of the centroids
"""

from pathlib import Path
import numpy as np
import napari
# import mathpotlib as plt

from skimage import filters

import napari_segment_blobs_and_things_with_membranes as nsbatwm
import pyclesperanto_prototype as cle

from sklearn.cluster import KMeans
from skimage.segmentation import watershed

from nuclei_segmentation import load_file, my_voronoi_otsu_labeling

data_folder = Path.cwd() / Path("Data")
num_channels = 2

def make_points(image, threshold):
    preprocessed = filters.gaussian(image, sigma=1, preserve_range=True)
    local_maxima_image = cle.detect_maxima_box(preprocessed)
    all_labeled = cle.label_spots(local_maxima_image)

    if threshold == 'li':
        binary_image = nsbatwm.threshold_li(preprocessed)
    else:
        binary_image = nsbatwm.threshold_otsu(preprocessed)

    final_spots = cle.exclude_labels_with_map_values_out_of_range(
        binary_image,
        all_labeled,
        minimum_value_range=1,
        maximum_value_range=1)
    
    points = np.argwhere(final_spots)
    
    return points

for file_path in data_folder.glob("*.czi"):
    nuclei = load_file(data_folder, file_path, 0)
    protein = load_file(data_folder, file_path, 1)
    
    viewer = napari.Viewer()
    CH1 = viewer.add_image(nuclei, name='CH1')
    CH2 = viewer.add_image(protein, name='CH2')
    
    # using napari segment ~blobs and things with membranes
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
    labels = kmeans.labels_

    features = {
        'cluster': labels/labels.max()}
    points_layer = viewer.add_points(reflected_points, features=features, size=5, face_color='cluster', face_colormap='prism')
    napari.run()
    
    # Visualisation
    
    # figure, ax = plt.subplots(1, 1, figsize=(8, 8))
    # ax.invert_yaxis()
    
    # plt.scatter(x=points[:, 0], 
    #             y=points[:, 1],
    #             c=labels,
    #             s=0.2,
    #             cmap='prism')
    # plt.scatter(x=centroids[:, 0], y=centroids[:, 1], s=5, color='w')
    # ax.imshow(protein, cmap='gray')
    
    
