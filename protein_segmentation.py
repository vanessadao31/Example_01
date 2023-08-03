# -*- coding: utf-8 -*-
"""
Trying to segment protein expressions into cells
"""

from pathlib import Path
import numpy as np
import napari
import csv

import napari_segment_blobs_and_things_with_membranes as nsbatwm
import pyclesperanto_prototype as cle
from napari_skimage_regionprops import regionprops_table

from functions import load_file, my_voronoi_otsu_labeling, two_channel_segmentor

data_folder = Path.cwd() / Path("Data")
columns = ["File", "Number nuclei", "Number blobs", "Number cells with protein"]
total_rows = []

for file_path in data_folder.glob("*.czi"):

    specific_folder = data_folder / Path(f"{file_path.stem}")
    specific_folder.mkdir(exist_ok=True)
    
    nuclei = load_file(data_folder, file_path, 0)
    protein = load_file(data_folder, file_path, 1)
    
    # using napari segment blobs and things with membranes
    segmented_protein= two_channel_segmentor(nuclei, protein, 
                                                     spot_sigma=22,
                                                     outline_sigma=7)
    
    segmented_nuclei, number_nuclei, centroids = my_voronoi_otsu_labeling(nuclei, 
                                                         spot_sigma=18,
                                                         outline_sigma=10)

    count_map = cle.proximal_other_labels_count_map(segmented_nuclei, segmented_protein, maximum_distance = 75) # max distance in pixels
    pos_nuclei = cle.exclude_labels_with_map_values_out_of_range(count_map, segmented_nuclei, minimum_value_range=1)

    # Writing csv fies
    
    segmented_nuclei_filename = f"{file_path.stem}_nuclei.csv"
    segmented_protein_filename = f"{file_path.stem}_protein.csv"
    pos_nuclei_filename = f"{file_path.stem}_pos.csv"
    
    np.savetxt(segmented_nuclei_filename, segmented_nuclei, delimiter=',')
    np.savetxt(segmented_protein_filename, segmented_protein, delimiter=',')
    np.savetxt(pos_nuclei_filename, pos_nuclei, delimiter=',')

    for csv_path in Path.cwd().glob("*.csv"):
        new_path = specific_folder / csv_path.name
        csv_path.replace(new_path)
    
        
    # Writing summary file
    
    row = [file_path.stem, segmented_nuclei.max() + 1, segmented_protein.max() + 1, pos_nuclei.max() + 1]
    total_rows = np.append(total_rows, row, axis=0)
    
    
total_rows = np.reshape(total_rows, (-1, len(columns)))    

with open("summary_file.csv", mode='w') as summary_file:
    summary_writer = csv.writer(summary_file, delimiter=',')
    summary_writer.writerow(columns)        
    summary_writer.writerows(total_rows)

