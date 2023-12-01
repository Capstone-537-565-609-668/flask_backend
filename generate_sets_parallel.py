from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import random
import math
import json
from generate_polygon import generate_polygon
import time
import geopandas
from shapely.geometry import Polygon
from download_csv import convert_to_shape_csv
from utils import clip

conf = SparkConf().setAppName("PolygonGeneration")
SparkContext.setSystemProperty('spark.executor.memory', '12g')
sc = SparkContext(conf=conf)
spark = SparkSession(sc)


def generate_sets_parallel(card, xsize, ysize, vertices_bounds, show_grid=True, irregularity_clip=0.8, spikiness_clip=0.8):
    gridCols = math.ceil(math.sqrt(card))
    gridRows = math.ceil(math.sqrt(card))
    # print(card, gridCols, gridRows, gridCols * gridRows)
    if card > (gridCols*gridRows):
        card = gridCols*gridRows
    mapping = dict()  # key: rowNum, value:[colNum]
    generated_polygon_centers = 0
    centers = []
    while generated_polygon_centers != card:
        xval = random.randint(0, gridRows-1)
        yval = random.randint(0, gridCols-1)
        if not mapping.get(xval):
            mapping[xval] = [yval]
            centers.append((xval, yval))
            generated_polygon_centers += 1
        else:
            if (not (yval in mapping[xval])):
                mapping[xval].append(yval)
                centers.append((xval, yval))
                generated_polygon_centers += 1

    '''
    Commenting this line to avoid multiple printing
  '''
    # print(mapping)
    """
    1. Distribute polygons to cells: {key: (row, col) => we can estimate the center of the cell => rowNum*size+colNum*size}
      - Estimate size of the cell: (500/5, 500/5)
      - vetices bound input
    2. Generate a polygon in these cells
  """
    shapes = []
    point = 0
    gen_rdd = sc.parallelize(centers, 4).map(lambda cent: generate_polygon(center=(clip((xsize/(2*gridCols))+cent[1]*(xsize/gridCols), 0, xsize),
                                                                                   clip((ysize/(2*gridRows))+(cent[0])*(ysize/(gridRows)), 0, ysize)), avg_radius=random.randint(20, max(21, int(xsize/(2*gridCols)))), irregularity=clip(random.random(), 0, irregularity_clip), spikiness=clip(random.random(), 0, spikiness_clip), num_vertices=random.randint(vertices_bounds[0], vertices_bounds[1])))
    print(gen_rdd.getNumPartitions())
    gen_rdd = gen_rdd.collect()

    pols = []
    for i in gen_rdd:
        p1 = Polygon(i)
        pols.append(p1)

    # send 15 polygons for visualization which is json serialized
    for_vis = pols[:15]
    dataset_descriptor = convert_to_shape_csv(pols)
    json_visualization_data = geopandas.GeoDataFrame(
        geometry=for_vis).to_json()
    # dump json_visualization_data to outputs/dataset_descriptor.json
    with open(f"outputs/{dataset_descriptor}/visualization_data.json", "w") as f:
        json.dump(json_visualization_data, f)
    # return gen_rdd

    return (dataset_descriptor, json_visualization_data)
