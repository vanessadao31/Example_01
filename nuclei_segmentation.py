# -*- coding: utf-8 -*-
"""
First attempt: Trying voronoi-otsu labelling
"""
from pathlib import Path
import numpy as np
import napari
from napari_skimage_regionprops import regionprops_table

from functions import load_file, my_voronoi_otsu_labeling

data_folder = Path.cwd() / Path("Data")
num_channels = 2

for file_path in data_folder.glob("*.czi"):

    specific_folder = data_folder / Path(f"{file_path.stem}")
    specific_folder.mkdir(exist_ok=True)
    
    nuclei = load_file(data_folder, file_path, 0)
    pores = load_file(data_folder, file_path, 1)
    
    # using napari segment blobs and things with membranes
    sigma_spot_detection = 18 # lower number, more segmentation
    sigma_outline = 10 # higher number, more gaussian blur applied
    segmented_nuclei, number_nuclei, centroids = my_voronoi_otsu_labeling(nuclei, 
                                                     spot_sigma=sigma_spot_detection,
                                                     outline_sigma=sigma_outline
                                                     )
    
    segmented_nuclei_filename = f"{file_path.stem}_nuclei.csv"
    
    np.savetxt(segmented_nuclei_filename, segmented_nuclei, delimiter=',')
    
    for csv_path in Path.cwd().glob("*.csv"):
        new_path = specific_folder / csv_path.name
        csv_path.replace(new_path)
    

