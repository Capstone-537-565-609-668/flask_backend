import csv

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.validation import explain_validity, make_valid


def number_of_invalid(shp):
    shp['validity'] = shp.apply(
        lambda row: explain_validity(row.geometry), axis=1)
    count = 0
    for i in shp.index:
        if shp['validity'][i] != 'Valid Geometry':
            count += 1
    return count


def correct_invalid_geometry(geometry):
    if not geometry.is_valid:
        return make_valid(geometry)
    else:
        return geometry


def overlap_correction(shp, buffer_distance=0.00000001):
    # Simplify geometries
    shp['geometry'] = shp['geometry'].apply(
        lambda geom: geom.simplify(tolerance=buffer_distance))

    # Iterate over pairs of Polygons to check for overlaps
    for i, row1 in shp.iterrows():
        for j, row2 in shp.iterrows():
            if i < j:
                geometry1 = row1['geometry']
                geometry2 = row2['geometry']

                # Check for overlaps within the buffer distance
                if (
                    geometry1.geom_type == 'Polygon'
                    and geometry2.geom_type == 'Polygon' and geometry1.buffer(buffer_distance).intersects(geometry2)

                ):
                    # Remove overlapping part from geometry2
                    diff_geometry = geometry2.difference(geometry1)

                    # Update the DataFrame with the modified geometry
                    shp.at[j, 'geometry'] = diff_geometry

    # Apply correction to invalid geometries again
    # shp['geometry'] = shp['geometry'].apply(correct_invalid_geometry)
    return shp


def validate_polygon(shp, card):
    def validate_only(shp):

        shp['geometry'] = shp['geometry'].apply(correct_invalid_geometry)

        multi_polygons = shp[shp['geometry'].geom_type == 'MultiPolygon']

        # if not multi_polygons.empty:
        multi_polygons = multi_polygons.explode(index_parts=True)
        shp = pd.concat([shp, multi_polygons], ignore_index=True)
        shp = shp[shp['geometry'].geom_type == 'Polygon']
        # Recursive call to process MultiPolygons
        # return validate_geometry(shp)
        return shp
    shp = validate_only(shp)
    if (card < 1000):
        shp = overlap_correction(shp)
        shp = validate_only(shp)
    return shp['geometry'].tolist()


# Example usage:
# df = gpd.read_file("your_shapefile.shp")
# validated_df = validate_geometry(df.copy())
# corrected_geometries = overlap_correction(validated_df.copy())
