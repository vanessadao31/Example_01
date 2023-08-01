# Example_01
 
A set of scripts which use the napari plugin [napari-segment-blobs-and-things-with-membranes](https://github.com/haesleinhuepf/napari-segment-blobs-and-things-with-membranes) to segment nuclei and cells from fluoresence microscopy images with high intensity in the nuclei and bodies then visualise the results in the napari viewer.
## Pre-requisites
Use environment.yml for required packages/plugins.
Or install [devbio-napari](https://github.com/haesleinhuepf/devbio-napari#installation).

## Images
<img src="https://github.com/vanessadao31/Example_01/assets/138872234/c7727328-80eb-4bc5-81d7-6ece3fb0d208" width="300">
<img src="https://github.com/vanessadao31/Example_01/assets/138872234/13b0ee2e-04a3-49a9-93b7-665be4a05984" width="300">
Two channel datasets visualised in napari with enhanced contrast. 

## Nuceli Segmentation
Performs Voronoi-Otsu-Labelling to label nuclei as well as the number of nuclei detected and their centroids. See [nsbatwm implementation](https://github.com/haesleinhuepf/napari-segment-blobs-and-things-with-membranes/blob/main/napari_segment_blobs_and_things_with_membranes/__init__.py)
## Local Maxima
- Robert Haase on local maxima
- Nearest neighbour to nuclei centroids to cluster
## Protein Segmentation
Watershed on binary mask of protein channel
