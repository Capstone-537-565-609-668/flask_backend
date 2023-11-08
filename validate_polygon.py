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
    shp['geometry'] = shp['geometry'].apply(correct_invalid_geometry)
    multi_polygons = shp[shp['geometry'].geom_type == 'MultiPolygon']
    shp = shp[shp['geometry'].geom_type != 'MultiPolygon']
    multi_polygons = multi_polygons.explode()

    # Concatenate the exploded MultiPolygons back to the original GeoDataFrame
    shp = pd.concat([shp, multi_polygons], ignore_index=True)
    return shp['geometry'].tolist()


