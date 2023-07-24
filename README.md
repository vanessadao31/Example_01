# Example_01
 
A set of scripts which use the napari plugin [napari-segment-blobs-and-things-with-membranes](https://github.com/haesleinhuepf/napari-segment-blobs-and-things-with-membranes) to segment nuclei and cells from fluoresence microscopy images with high intensity in the nuclei and bodies then visualise the results in the napari viewer.

## Images
![IMG1](https://github.com/vanessadao31/Example_01/assets/138872234/c7727328-80eb-4bc5-81d7-6ece3fb0d208)
![IMG2](https://github.com/vanessadao31/Example_01/assets/138872234/13b0ee2e-04a3-49a9-93b7-665be4a05984)
Two channel 2D images

## Nuceli Segmentation
Performs Voronoi-Otsu-Labelling to label nuclei as well as the number of nuclei detected and their centroids. See [nsbatwm implementation](https://github.com/haesleinhuepf/napari-segment-blobs-and-things-with-membranes/blob/main/napari_segment_blobs_and_things_with_membranes/__init__.py)
## Local Maxima

## Body Segmentation
