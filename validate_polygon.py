import geopandas as gpd
from shapely.validation import explain_validity, make_valid
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import pandas as pd
import csv
import geopandas as gpd
from shapely.wkt import loads


def correct_invalid_geometry(geometry):
    if not geometry.is_valid:

        return make_valid(geometry)
    else:
        return geometry


def validate_polygon(pols):
    geoseries = gpd.GeoSeries(pols)
    shp = gpd.GeoDataFrame(geoseries, columns=['geometry'])
    overlaps = gpd.overlay(shp, shp, how='intersection')

    # Merge the overlapping geometries
    merged = gpd.overlay(shp, overlaps, how='union')
    # Drop duplicate columns and reset index
    merged = merged[shp.columns].reset_index(drop=True)
    shp['geometry'] = merged['geometry'].apply(correct_invalid_geometry)
    multi_polygons = shp[shp['geometry'].geom_type == 'MultiPolygon']
    shp = shp[shp['geometry'].geom_type == 'Polygon']
    if not multi_polygons.empty:
        multi_polygons = multi_polygons.explode(index_parts=True)
        shp = pd.concat([shp, multi_polygons], ignore_index=True)
        return validate_polygon(shp)
    
    return shp['geometry'].tolist()
