# -*- coding: utf-8 -*-
"""
Trying to segment protein expressions into cells
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import napari

from skimage import data, measure, exposure, filters
from skimage.segmentation import watershed

import napari_segment_blobs_and_things_with_membranes as nsbatwm
import pyclesperanto_prototype as cle

from k_initialise import load_file, my_voronoi_otsu_labeling

data_folder = Path("Data")
files = ["cover slip 35 image 3.czi",
        "coverslip 33 image 1.czi"]

num_channels = 2

nuclei = load_file(files[1], 0)
protein = load_file(files[1], 1)

def two_channel_segmentor(nuclei, protein, spot_sigma: float = 2, outline_sigma: float = 2) -> "napari.types.LabelsData":
    image = np.asarray(nuclei)

    # blur and detect local maxima
    blurred_spots = filters.gaussian(image, spot_sigma)
    spot_centroids = local_maxima(blurred_spots)
    
    # blur and threshold
    blurred_outline = filters.gaussian(protein, outline_sigma)
    threshold = filters.threshold_triangle(blurred_outline)
    binary_otsu = blurred_outline >= threshold
    
    # determine local maxima within the thresholded area
    remaining_spots = spot_centroids * binary_otsu
    
    # start from remaining spots and flood binary image with labels
    labeled_spots, number = measure.label(remaining_spots, return_num=True)
    labels = watershed(binary_otsu, labeled_spots, mask=binary_otsu)
    
    return labels

for file in files: 
    nuclei = load_file(file, 0)
    protein = load_file(file, 1)
    
    viewer = napari.Viewer()
    CH1 = viewer.add_image(nuclei, name='CH1')
    CH2 = viewer.add_image(protein, name='CH2')
    
    # using napari segment blobs and things with membranes
    segmented_protein= two_channel_segmentor(nuclei, protein, 
                                                     spot_sigma=22,
                                                     outline_sigma=7)
    
    segmented_nuclei, number_nuclei, centroids = my_voronoi_otsu_labeling(nuclei, 
                                                         spot_sigma=18,
                                                         outline_sigma=10)
    nuclei_labels = viewer.add_labels(segmented_nuclei)
    protein_labels = viewer.add_labels(segmented_protein)

    maximum_distance = 75 # pixels
    
    count_map = cle.proximal_other_labels_count_map(segmented_nuclei, segmented_protein, maximum_distance = maximum_distance)
    
    pos_nuclei = cle.exclude_labels_with_map_values_out_of_range(
        count_map, segmented_nuclei, minimum_value_range=1)
    cle.imshow(pos_nuclei, labels=True)
    
    pos_nuclei_labels = viewer.add_labels(pos_nuclei, name='positive_nuclei')
    
    # print out results
    print('\nFile name:', file)
    print('Number of nuclei: ', segmented_nuclei.max() + 1)
    print('Number of protein blobs: ', segmented_protein.max() + 1)
    print('Number of "cells with protein expression": ', pos_nuclei.max() +1)