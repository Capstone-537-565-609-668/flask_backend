import matplotlib.pyplot as plt
import fiona
import pandas as pd
import geopandas


def convert_to_shape_csv(polygons):
    gdf = geopandas.GeoDataFrame(geometry=polygons)

    gdf.to_csv("my_file_csv.csv")

    gdf.to_file("my_file_shape.shp")
