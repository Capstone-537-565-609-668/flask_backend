from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import random
import math
import json
import generate_polygon
import time
import geopandas
from shapely.geometry import Polygon
from download_csv import convert_to_shape_csv
from utils import clip

conf = SparkConf().setAppName("PolygonGeneration")
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


params = {
    "vertices_with_constant_cardinality": [
        # {
        #     "card": 100,
        #     "xsize": 500,
        #     "ysize": 500,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 100,
        #     "xsize": 500,
        #     "ysize": 500,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 100,
        #     "xsize": 500,
        #     "ysize": 500,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 100,
        #     "xsize": 500,
        #     "ysize": 500,
        #     "vertices_bound": [3, 10000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 1000,
        #     "xsize": 1000,
        #     "ysize": 1000,
        #     "vertices_bound": [3, 10000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 10000,
        #     "xsize": 10000,
        #     "ysize": 10000,
        #     "vertices_bound": [3, 10000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 100000,
        #     "xsize": 100000,
        #     "ysize": 100000,
        #     "vertices_bound": [3, 10],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 100000,
        #     "xsize": 100000,
        #     "ysize": 100000,
        #     "vertices_bound": [3, 100],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        # {
        #     "card": 100000,
        #     "xsize": 100000,
        #     "ysize": 100000,
        #     "vertices_bound": [3, 1000],
        #     "irregularity_clip":0.8,
        #     "spikiness_clip":0.8
        # },
        {
            "card": 100000,
            "xsize": 100000,
            "ysize": 100000,
            "vertices_bound": [3, 10000],
            "irregularity_clip":0.8,
            "spikiness_clip":0.8
        }
    ],
    "cardinality_with_constant_vertices": [
        {
            "card": 1000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 10000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 20000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 30000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 40000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        }, {
            "card": 50000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },

        {
            "card": 60000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },

        {
            "card": 70000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 80000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },

        {
            "card": 90000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },

        {
            "card": 100000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 200000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 300000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 400000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 500000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },
        {
            "card": 600000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        },

        {
            "card": 700000,
            "xsize": 10000,
            "ysize": 10000,
            "vertices_bound": [3, 50],
            "irregularity_clip":0.6,
            "spikiness_clip":0.6
        }

    ]



}


for test_title in params.keys():
    result = []
    print(
        f"Starting tests for {test_title} with {len(params[test_title])} test cases")
    with open(f"{test_title}.csv", "w") as f:
        f.write("dataset_id, Tries ,time_taken,card,xsize,ysize,vertices_bound_min,vertices_bound_max,irregularity_clip,spikiness_clip\n")

    for test_case in params[test_title]:
        # run it 3 times
        for i in range(2):
            st = time.time()
            dataset_id, temp = generate_sets_parallel(card=test_case["card"], xsize=test_case["xsize"], ysize=test_case["ysize"], vertices_bounds=test_case[
                                                      "vertices_bound"], show_grid=True, irregularity_clip=test_case["irregularity_clip"], spikiness_clip=test_case["spikiness_clip"])
            end = time.time()
            elapsed_time = end - st
            temp = [dataset_id, i + 1, f"{elapsed_time:.2f}", test_case["card"], test_case["xsize"], test_case["ysize"],
                    test_case["vertices_bound"][0], test_case["vertices_bound"][1], test_case["irregularity_clip"], test_case["spikiness_clip"]]
            with open(f"{test_title}.csv", "a") as f:
                f.write(",".join(list(map(lambda x: str(x), temp))))
                f.write("\n")

        print("Done with test case: ", test_case)

    # with open(f"{test_title}.csv", "w") as f:
    #     f.write("dataset_id, Tries ,time_taken,card,xsize,ysize,vertices_bound_min,vertices_bound_max,irregularity_clip,spikiness_clip\n")
    #     for row in result:
    #         f.write(",".join(list(map(lambda x: str(x), row))))
    #         f.write("\n")
