import matplotlib.pyplot as plt
import pandas as pd
import geopandas
import uuid
import os


def convert_to_shape_csv(polygons):

    # generate a unique uuid for this csv file
    dataset_id = uuid.uuid4()
    gdf = geopandas.GeoDataFrame(geometry=polygons)
    # create a folder with name as dataset_id
    # save the csv file in this folder
    # create a folder
    os.mkdir(f"outputs/{dataset_id}")
    gdf.to_csv(f"outputs/{dataset_id}/my_csv.csv")
    gdf.to_file(f"outputs/{dataset_id}/my_shape_file.shp")

    wkt_filename = f"outputs/{dataset_id}/my_wkt_file.wkt"
    with open(wkt_filename, 'w') as wkt_file:
        # wkt_file.write("WKT\n")
        for geometry in gdf["geometry"]:
            wkt_file.write(f"{geometry.wkt}\n")
    return dataset_id
