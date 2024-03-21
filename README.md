
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

* Using conda, install GDAL in "base" environment by:
```python I'm A tab
conda install -c conda-forge gdal==3.4.3
```
* Create Conda Environment:
Create a virtual Conda environment with the required Python version and requirements file:
```python I'm A tab
conda create --name gwenv python=3.8
conda activate gwenv
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
cd ../environment
pip install -r requirements.txt
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




