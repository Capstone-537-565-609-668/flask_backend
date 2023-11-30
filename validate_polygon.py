import csv

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Polygon
from shapely.validation import explain_validity, make_valid
from shapely.wkt import loads


def correct_invalid_geometry(geometry):
    if not geometry.is_valid:

        return make_valid(geometry)
    else:
        return geometry

def number_of_invalid(shp):
    count = 0
    for i in shp.index:
        if shp['validity'][i] != 'Valid Geometry':
            count+=1
    return count

def validate_polygon(shp):
    # Set a buffer distance to handle overlaps
    buffer_distance = 0.00000001  # Adjust this value based on your data and precision needs
    # geoseries = gpd.GeoSeries(pols)
    # shp = gpd.GeoDataFrame(geoseries, columns=['geometry'])
    
    
    shp['geometry'] = shp['geometry'].apply(correct_invalid_geometry)
    multi_polygons = shp[shp['geometry'].geom_type == 'MultiPolygon']
    shp = shp[shp['geometry'].geom_type == 'Polygon']
    if not len(multi_polygons)==0:
        multi_polygons = multi_polygons.explode(index_parts=True)
        shp = pd.concat([shp, multi_polygons], ignore_index=True)
        return validate_polygon(shp)
    
  

    for i, row1 in shp.iterrows():
        for j, row2 in shp.iterrows():
            if i < j:
                geometry1 = row1['geometry']
                geometry2 = row2['geometry']
                print(geometry1.geom_type, geometry2.geom_type)
                # Check for overlaps within the buffer distance
                if geometry1.buffer(buffer_distance).intersects(geometry2) :
                    # Remove overlapping part from geometry2
                    diff_geometry = geometry2.difference(geometry1)

                    # Update the DataFrame with the modified geometry
                    shp.at[j, 'geometry'] = diff_geometry
    shp['geometry'] = shp['geometry'].apply(correct_invalid_geometry)

    multi_polygons = shp[shp['geometry'].geom_type == 'MultiPolygon']
    shp = shp[shp['geometry'].geom_type == 'Polygon']
   

    if not len(multi_polygons)==0:
        multi_polygons = multi_polygons.explode(index_parts=True)
        shp = pd.concat([shp, multi_polygons], ignore_index=True)
        return validate_polygon(shp)
    
    # return shp['geometry'].tolist()
    # multi_polygons = multi_polygons.explode(index_parts=True)

    # Concatenate the exploded MultiPolygons back to the original GeoDataFrame
    # shp = pd.concat([shp, multi_polygons], ignore_index=True)
    # Iterate over the DataFrame to perform operations

    return shp['geometry'].tolist()