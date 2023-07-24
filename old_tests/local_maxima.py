# -*- coding: utf-8 -*-
"""
Binarisation works with nsbatwm.threshold_otsu to get the points 
with the highest intensities

Whole cell body binarisation works best with nsbatwm.threshol_otsu
~more unbiased
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import napari
import czifile

import napari_segment_blobs_and_things_with_membranes as nsbatwm
from skimage import data, measure, exposure, img_as_ubyte, filters
import pyclesperanto_prototype as cle

from nuclei_segmentation import load_file

data_folder = Path("Data")
files = ["cover slip 35 image 3.czi",
        "coverslip 33 image 1.czi"]

from file in files:
    nuclei = load_file(file, 0)
    protein = load_file(file, 1)
    
    viewer = napari.Viewer()
    CH1 = viewer.add_image(nuclei, name='CH1')
    CH2 = viewer.add_image(protein, name='CH2')
    
    preprocessed = filters.gaussian(protein, sigma=1, preserve_range=True)
    
    local_maxima_image = cle.detect_maxima_box(preprocessed)
    all_labeled = cle.label_spots(local_maxima_image)
    binary_image = nsbatwm.threshold_li(preprocessed)
    
    plt.imshow(binary_image)
    
    final_spots = cle.exclude_labels_with_map_values_out_of_range(
        binary_image,
        all_labeled,
        minimum_value_range=1,
        maximum_value_range=1)
    
    points = np.argwhere(final_spots)
    
    fig, ax = plt.subplots(1, 1, figsize=(8,8))
    ax.plot(points[:, 0],points[:, 1],'w+', markersize=10)
    ax.imshow(protein)
    
    points_layer = viewer.add_points(points, size=4, face_color='lime')
