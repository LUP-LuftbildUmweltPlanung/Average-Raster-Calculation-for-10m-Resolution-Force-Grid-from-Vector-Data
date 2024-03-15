# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:21:34 2024

@author: shadi
"""

import rasterio
from rasterio import features
from rasterio.transform import from_bounds
import geopandas as gpd
import geowombat as gw
import xarray as xr
import os
from osgeo import gdal
import time

chunksize = 64 #chunksize for geowombat export - may need to be decreased for small images to avoid RasterBlockError


def polygons_to_raster(shapefile_path, raster_out_path, raster_resolution= 1.0, nodata_value=0):
    """
    Convert polygons from a shapefile to a raster.

    Parameters:
    shapefile_path (str): Path to the input shapefile.
    raster_out_path (str): Path to save the output raster file.
    raster_resolution (float): Resolution of the output raster in the same units as the shapefile's coordinate system.
    nodata_value (int, optional): Value to assign to cells outside the polygons. Defaults to 0.

    Returns:
    None

    Raises:
    ValueError: If an error occurs during rasterization, consider increasing raster_resolution.
    
    Example:
    # Example usage
    shapefile_path = "Path/to/Input_shapefile"
    raster_out_path = "Path/to/output_tiff_file"
    raster_resolution = 1.0  # as default Resolution of the raster
    
    After successful execution, a raster TIFF file is saved at the specified raster_out_path.
    """
    # Read the shapefile using geopandas
    gdf = gpd.read_file(shapefile_path)

    # Get the bounds of the entire shapefile
    minx, miny, maxx, maxy = gdf.total_bounds

    # Calculate the width and height of the raster
    width = int((maxx - minx) / raster_resolution)
    height = int((maxy - miny) / raster_resolution)

    # Define the transformation
    transform = from_bounds(minx, miny, maxx, maxy, width, height)

    # Create an empty raster array
    raster_array = features.rasterize(
        [(geometry, 1) for geometry in gdf.geometry],
        out_shape=(height, width),
        transform=transform,
        fill=nodata_value,
        all_touched=True,
        dtype=rasterio.uint8
    )

    # Write the raster array to a GeoTIFF file
    with rasterio.open(
            raster_out_path,
            'w',
            driver='GTiff',
            width=width,
            height=height,
            count=1,
            dtype=rasterio.uint8,
            crs=gdf.crs,
            transform=transform
    ) as dst:
        dst.write(raster_array, 1)
        
        
        
######################################### Vegetation Height Processing Functions
def open_veg_damaged_raster(veg_damaged_raster):
    """Opens a vegetation damaged raster, sets values < zero to zero and returns its data and attributes.

    Args:
        veg_damaged_raster (str): Path to the vegetation damaged raster file.

    Returns:
        tuple: A tuple containing the vegetation damaged data, its attributes,
            its bounds in the FORCE CRS, its nodata value, and its resolution.
    """
    with gw.open(veg_damaged_raster, chunks=chunksize) as veg_d:
        veg_d = veg_d.gw.set_nodata(src_nodata=veg_d.attrs['_FillValue'], dst_nodata=-9999) #get original nodata value and replace with new one
        veg_d_attrs = veg_d.attrs #get attributes
        veg_d_nodata = veg_d.attrs['_FillValue'] #get new nodata value
        veg_d_res = veg_d.attrs['res'][0] #get resolution
        veg_d = xr.where((veg_d < 0) & (veg_d != veg_d_nodata), 0, veg_d).assign_attrs(veg_d_attrs) #set veg_h raster < zero to zero and reassign attrs

    # Get bounds of vegetation height raster in FORCE CRS
    with gw.config.update(ref_crs='EPSG:3035'):
        with gw.open(veg_damaged_raster) as veg_d_rep:
            veg_d_rep_bounds = veg_d_rep.gw.bounds

    return veg_d, veg_d_attrs, veg_d_rep_bounds, veg_d_nodata, veg_d_res

######################################### Bounding Box and Aggregation Functions
    
def fit_box(box1, box2):
    """Adjusts the first bounding box until it fits inside the second bounding box.

    Args:
        box1 (tuple): Tuple of coordinates (left, bottom, right, top) for the first bounding box.
        box2 (tuple): Tuple of coordinates (left, bottom, right, top) for the second bounding box.

    Returns:
        tuple: The adjusted bounding box as a tuple of coordinates (left, bottom, right, top).
    """
    step = 10
    left = box1[0]
    bottom = box1[1]
    right = box1[2]
    top = box1[3]

    while left < box2[0]:
        left += step

    while bottom < box2[1]:
        bottom += step

    while right > box2[2]:
        right -= step

    while top > box2[3]:
        top -= step

    return (left, bottom, right, top)

########################################################################
def average_aggregate_raster_10m_force(input_raster, adjusted_bbox):
    """Aggregates a raster to 10m resolution using average resampling.

    Args:
        input_raster (str): Path to the input raster file.
        adjusted_bbox (tuple): The adjusted2 bounding box to use for aggregation.

    Returns:
        tuple: A tuple containing the aggregated raster data and its attributes.
    """
    with gw.config.update(ref_crs='EPSG:3035', ref_res=(10, 10), ref_bounds=adjusted_bbox, nodata=-9999):
        with gw.open(input_raster, resampling='average') as input_aggregated:
            input_aggregated_attrs = input_aggregated.attrs
            return input_aggregated, input_aggregated_attrs
        
######################################### Raster Export Function
def export_raster(export_raster, attrs, dest_path):
    """Exports a raster to a file.

    Args:
        export_raster (xarray.DataArray): The raster data to export.
        attrs (dict): The attributes of the raster data.
        dest_path (str): The path to the destination file.
    """
    start_time = time.time()
    
    export_raster = export_raster.assign_attrs(attrs).astype('float32').chunk(chunks=chunksize)

    export_raster.gw.save(dest_path, 
                          num_workers = 16,
                          nodata = -9999)
    
    # Compress the exported raster using gdal
    print('Compressing raster...')
    compression_start_time = time.time()
    
    ds = gdal.Open(dest_path, gdal.GA_Update)
    filename, file_extension = os.path.splitext(dest_path)
    temp_path = filename + '_temp' + file_extension
    gdal.Translate(temp_path, ds, creationOptions=['COMPRESS=LZW', 'BIGTIFF=YES'])
    ds = None
    
    # Replace original raster with compressed raster
    os.replace(temp_path, dest_path)
    
    compression_end_time = time.time()
    compression_elapsed_time = compression_end_time - compression_start_time
    print(f'Finished compressing raster in {compression_elapsed_time:.2f} seconds ({compression_elapsed_time/60:.2f} minutes).')
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Finished exporting raster in {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes).')

