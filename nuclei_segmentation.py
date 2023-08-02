# -*- coding: utf-8 -*-
"""
First attempt: Trying voronoi-otsu labelling
"""
from pathlib import Path
import napari
from napari_skimage_regionprops import regionprops_table

from functions import load_file, my_voronoi_otsu_labeling

data_folder = Path.cwd() / Path("Data")
num_channels = 2

for file_path in data_folder.glob("*.czi"):
    nuclei = load_file(data_folder, file_path, 0)
    protein = load_file(data_folder, file_path, 1)
    
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
    

