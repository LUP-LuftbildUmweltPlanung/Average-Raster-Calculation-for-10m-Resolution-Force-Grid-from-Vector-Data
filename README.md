
# Average-Raster-Calculation-for-10m-Resolution-Force-Grid-from-Vector-Data




## Description

"This repository contains code to rasterize vector shapefiles into raster TIFF files with a 10-meter resolution, aligning them with a Force grid map."
## Getting Started

### Dependencies

* GDAL, Geopandas, Geowombat, xarray
* Anaconda [download](doc:https://www.anaconda.com/download)
* developed on Windows 11

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
python3 -m pip install ipykernel
python3 -m ipykernel gwenv --user
```



## Authors

 
 - [Sebastian Lehmler](https://github.com/LUP-LuftbildUmweltPlanung)
 - [Shadi Ghantous](https://github.com/LUP-LuftbildUmweltPlanung)


## Reference

* [GeoWombat documentation](https://geowombat.readthedocs.io/en/latest/).
* [Geopandas](https://geopandas.org/en/stable/)




