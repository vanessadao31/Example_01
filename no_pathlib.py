# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:32:09 2023

@author: daov1
"""

from pathlib import Path
import napari
from napari_skimage_regionprops import regionprops_table
import czifile

from functions import my_voronoi_otsu_labeling

def load_file_test(file, channel):
    filename = data_folder / file
    image = czifile.imread(filename)
    return image[0, 0, channel, 0, 0, :, :, 0]

data_folder = Path.cwd() / Path("Data")
files = ["cover slip 35 image 3.czi", "coverslip 33 image 1.czi"]
num_channels = 2

for file in files:
    nuclei = load_file_test(file, 0)
    protein = load_file_test(file, 1)
    
    viewer = napari.Viewer()
    CH1 = viewer.add_image(nuclei, name='CH1')
    CH2 = viewer.add_image(protein, name='CH2')
    
    # using napari segment blobs and things with membranes
    sigma_spot_detection = 18 # lower number, more segmentation
    sigma_outline = 10 # higher number, more gaussian blur applied
    segmented_nuclei, number_nuclei, centroids = my_voronoi_otsu_labeling(nuclei, 
                                                     spot_sigma=sigma_spot_detection,
                                                     outline_sigma=sigma_outline
                                                     )
    nuclei_labels = viewer.add_labels(segmented_nuclei)
    
    # region properties
    regionprops_table(
        viewer.layers[0].data,
        viewer.layers[2].data,
        intensity=True,
        napari_viewer=viewer,
        )
    napari.run()
