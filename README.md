
# FORCE_GRID_SPATIAL_DATA_AGGREGATION



## Description

"The FORCE_GRID_SPATIAL_DATA_AGGREGATION contains functions to aggregate geospatial data to a lower resolution Grid. We use the functionalities to aggregate raster or vector data of different environmental indicators to the FORCE Grid (https://force-eo.readthedocs.io/en/latest/howto/datacube.html) at 10m resolution to facilitate usage in Sentinel-2 based machine learning models. Aggregation functions include e.g. Mean, Standard Deviation and Sum. 

Additionally, some functionality for high resolution raster transformation is included. For our projects, we for example transform high resolution canopy height rasters to green volume (applying some rules based transformations) and into binary canopy rasters (using a specified threshold value). These are then upscaled to the FORCE Grid." 


## Getting Started

### Dependencies

* GDAL, Geopandas, Geowombat, xarray
* Anaconda [download](https://www.anaconda.com/download) 
* developed on Windows

### Installation

* Install GDAL Binaries:
```python I'm A tab
conda install -c conda-forge gdal
```
**Hint**: If you encounter issues while installing GDAL, we recommend creating a separate environment specifically for installing GDAL to avoid conflicts. This can help streamline the installation process and resolve any compatibility issues that may arise.

* Verify GDAL Version:
After installing GDAL, verify the version to ensure compatibility
```python I'm A tab
gdalinfo --version
```
For Example the output is:
```python I'm A tab
GDAL_3.8.4
```
* Create Conda Environment:
Create a virtual Conda environment with the required Python version and requirements file:
```python I'm A tab
conda create --name gwenv python=3.8 cython numpy
conda activate gwenv
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
cd ../environment
pip install -r requirements.txt
```
* installing Python GDAL Package:
Ensure that the Python GDAL package version matches the installed GDAL binaries version:
```python I'm A tab
(gwenv) pip install GDAL==3.8.4
```
* Install Geowombat Library:
Install Geowombat from GitHub and update it:
```python I'm A tab
(gwenv) pip install git+https://github.com/jgrss/geowombat
(gwenv) pip install --upgrade git+https://github.com/jgrss/geowombat
```
* To activate your library in Jupyter Notebook or spyder, follow these steps:
```python I'm A tab
pip install ipykernel
python -m ipykernel install --user --name gwenv --display-name "Python (gwenv)"
```



## Authors

 
 - [Sebastian Lehmler](https://github.com/LUP-LuftbildUmweltPlanung)
 - [Shadi Ghantous](https://github.com/LUP-LuftbildUmweltPlanung)


## Reference

* [GeoWombat documentation](https://geowombat.readthedocs.io/en/latest/).
* [FORCE Framework] (https://force-eo.readthedocs.io/en/latest/index.html)
* [Geopandas](https://geopandas.org/en/stable/)




