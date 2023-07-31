# -*- coding: utf-8 -*-
"""
Trying to segment protein expressions into cells
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import napari
import csv

from skimage.morphology import local_maxima
from skimage import data, measure, exposure, filters
from skimage.segmentation import watershed

import napari_segment_blobs_and_things_with_membranes as nsbatwm
import pyclesperanto_prototype as cle
from napari_skimage_regionprops import regionprops_table, add_table, get_table

from nuclei_segmentation import load_file, my_voronoi_otsu_labeling

data_folder = Path("Data")
files = ["cover slip 35 image 3.czi",
        "coverslip 33 image 1.czi"]
columns = ["File", "Number nuclei", "Number blobs", "Number cells with protein"]
num_channels = range(len(files))
total_rows = []

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
    
    row = [file, segmented_nuclei.max() + 1, segmented_protein.max() + 1, pos_nuclei.max() + 1]
    total_rows = np.append(total_rows, row, axis=0)
        
    # visualisation
    outlines = cle.detect_label_edges(pos_nuclei)
    img_with_outlines = cle.maximum_images(nuclei, outlines*nuclei.max())
    cle.imshow(img_with_outlines)
    
    pos_nuclei_labels = viewer.add_labels(pos_nuclei, name='positive_nuclei')
    pos_nuclei_labels.contour = 5
    
    # region properties
    regionprops_table(
        viewer.layers[0].data,
        viewer.layers[2].data,
        intensity=True,
        napari_viewer=viewer,
        )
    
total_rows = np.reshape(total_rows, (-1, len(columns)))    

# saving results
with open("summary_file.csv", mode='w') as summary_file:
    summary_writer = csv.writer(summary_file, delimiter=',')
    summary_writer.writerow(columns)        
    summary_writer.writerows(total_rows)