# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:51:27 2023

@author: daov1
"""

from pathlib import Path
import napari
import csv
import numpy as np

from napari_skimage_regionprops import regionprops_table
from functions import load_file

data_folder = Path.cwd() / Path("Data")

for folder_path in data_folder.glob("cover*"):
    
    if folder_path.is_dir():

        nuclei = load_file(data_folder, folder_path.name+".czi", 0)
        protein = load_file(data_folder, folder_path.name+".czi", 1)
        
        viewer = napari.Viewer()
        CH1 = viewer.add_image(nuclei, name='CH1')
        CH2 = viewer.add_image(protein, name='CH2')
    
        for file_path in folder_path.glob("*_nuclei.csv"):
            flat_segmented_nuclei = np.loadtxt(file_path, delimiter=',')
            segmented_nuclei = flat_segmented_nuclei.reshape(1024, 1024)
            nuclei_labels = viewer.add_labels(segmented_nuclei.astype(int), name='segmented_nuclei')

        for file_path in folder_path.glob("*_protein.csv"):
            flat_segmented_protein = np.loadtxt(file_path, delimiter=',')
            segmented_protein = flat_segmented_protein.reshape(1024, 1024)   
            protein_labels = viewer.add_labels(segmented_protein.astype(int), name='segmented_protein')

            
        for file_path in folder_path.glob("*_pos.csv"):
            flat_pos_nuclei = np.loadtxt(file_path, delimiter=',')
            pos_nuclei = flat_pos_nuclei.reshape(1024, 1024)  
            pos_nuclei_labels = viewer.add_labels(pos_nuclei.astype(int), name='positive_nuclei')
            pos_nuclei_labels.contour = 5
        
            
        # region properties
        regionprops_table(
            viewer.layers[0].data,
            viewer.layers[2].data,
            intensity=True,
            napari_viewer=viewer)
            
        napari.run()