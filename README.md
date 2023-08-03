# Example_01
 
A set of scripts which use the napari plugin [napari-segment-blobs-and-things-with-membranes](https://github.com/haesleinhuepf/napari-segment-blobs-and-things-with-membranes) to segment nuclei and cells from fluoresence microscopy images with high intensity in the nuclei and bodies then visualise the results in the napari viewer.
## Pre-requisites
Create a new conda/mamba environment and install [devbio-napari](https://github.com/haesleinhuepf/devbio-napari#installation) using mamba (already on OnDemand).
```
mamba create --name devbio-napari-env python=3.9 devbio-napari -c conda-forge -c pytorch
```

Afterwards, activate the environment.
```
conda activate devbio-napari-env
```

Then navigate to the repo and run the desired scripts from the command line.
## Images
<img src="https://github.com/vanessadao31/Example_01/assets/138872234/c7727328-80eb-4bc5-81d7-6ece3fb0d208" width="300">
<img src="https://github.com/vanessadao31/Example_01/assets/138872234/13b0ee2e-04a3-49a9-93b7-665be4a05984" width="300">

Two channel datasets visualised in napari with enhanced contrast. 

## Nuceli Segmentation
Performs Voronoi-Otsu-Labelling, a workflow which combines Gaussian blur, spot detection, thresholding and binary watershed, to label nuclei as well as output the number of nuclei detected and their centroids. See [nsbatwm implementation](https://github.com/haesleinhuepf/napari-segment-blobs-and-things-with-membranes/blob/main/napari_segment_blobs_and_things_with_membranes/__init__.py)
## Local Maxima
Local maxima detection with [plyclesperanto-prototype's](https://github.com/clEsperanto/pyclesperanto_prototype) `detect_maxima_box` and li thresholding.

Clustering the points according to nearest neighbour with nuclei centroids as the origins of the clusters. 
## Protein Segmentation
Requires a nuclei marker such as DAPI. Similar to nuclei segmentation but uses a binary mask from the protein channel to perform watershed from nuclei centroids.
<img src="https://github.com/vanessadao31/Example_01/assets/138872234/0c94776e-e045-4802-8a14-eabb41b3ac67" width="600">

Outputs a summary .csv fie with number of nuclei detected, number of protein blobs detected and number of nuclei associated with a protein blob.
A labels layer will be produced identifying which, and how many, nuclei are within a protein blob.
## Using Your Own Data
As of right now, only works with two channcel .czi data with the nuclei in channel 1 and the protein in channel 2. Save the data in the `Data` folder then run the desired script.
