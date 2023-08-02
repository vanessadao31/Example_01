# -*- coding: utf-8 -*-
"""
functions
"""

import matplotlib.pyplot as plt
import numpy as np
import napari
import czifile

from skimage.morphology import local_maxima, local_minima
import napari_segment_blobs_and_things_with_membranes as nsbatwm
from skimage import data, measure, filters
from skimage.segmentation import watershed
import pyclesperanto_prototype as cle

def load_file(folder, file, channel):
    filename = folder / file
    image = czifile.imread(filename)
    return image[0, 0, channel, 0, 0, :, :, 0]

def my_voronoi_otsu_labeling(image:"napari.types.ImageData", spot_sigma: float = 2, outline_sigma: float = 2) -> "napari.types.LabelsData":
    image = np.asarray(image)

    # blur and detect local maxima
    blurred_spots = filters.gaussian(image, spot_sigma)
    spot_centroids = local_maxima(blurred_spots)

    # blur and threshold
    blurred_outline = filters.gaussian(image, outline_sigma)
    threshold = filters.threshold_otsu(blurred_outline)
    binary_otsu = blurred_outline > threshold

    # determine local maxima within the thresholded area
    remaining_spots = spot_centroids * binary_otsu

    # start from remaining spots and flood binary image with labels
    labeled_spots, number = measure.label(remaining_spots, return_num=True)
    labels = watershed(binary_otsu, labeled_spots, mask=binary_otsu)
    
    properties = measure.regionprops_table(labels, properties=('label', 'centroid'))
    centroids = np.stack((properties['centroid-1'], properties['centroid-0']), axis=-1)

    return labels, number, centroids


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
    