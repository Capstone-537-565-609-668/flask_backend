import math
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from download_csv import convert_to_shape_csv
from shapely.geometry import Polygon
from utils import clip
from generate_polygon import generate_polygon
import json
import geopandas
'''
  Time : O(N) , where N is number of vertices
  space : O(M)
'''
def generate_sets(card, xsize, ysize, vertices_bounds, show_grid=True, irregularity_clip=0.8, spikiness_clip=0.8):
    gridCols = math.ceil(math.sqrt(card))
    gridRows = math.ceil(math.sqrt(card))
    print(card, gridCols, gridRows, gridCols * gridRows)
    if card > (gridCols*gridRows):
        card = gridCols*gridRows
    mapping = dict()  # key: rowNum, value:[colNum]
    generated_polygon_centers = 0
    while generated_polygon_centers != card:
        xval = random.randint(0, gridRows-1)
        yval = random.randint(0, gridCols-1)
        if not mapping.get(xval):
            mapping[xval] = [yval]
            generated_polygon_centers += 1
        else:
            if(not (yval in mapping[xval])):
                mapping[xval].append(yval)
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

    for key in mapping.keys():
        for value in mapping[key]:
            centerx = (clip((xsize/(2*gridCols))+value*(xsize/gridCols), 0, xsize),
                       clip((ysize/(2*gridRows))+(key)*(ysize/(gridRows)), 0, ysize))

            shapes.append(generate_polygon(center=centerx,
                                           avg_radius=random.randint(
                                               20, max(21, int(xsize/(2*gridCols)))),
                                           irregularity=clip(
                                               random.random(), 0, irregularity_clip),
                                           spikiness=clip(
                                               random.random(), 0, spikiness_clip),
                                           num_vertices=random.randint(vertices_bounds[0], vertices_bounds[1])))
            point += 1

    pols = []
    for i in shapes:
        p1 = Polygon(i)
        pols.append(p1)

    #send 15 polygons for visualization which is json serialized
    for_vis =pols[:15]
    dataset_descriptor=convert_to_shape_csv(pols)
    json_visualization_data = geopandas.GeoDataFrame(geometry=for_vis).to_json()
    # dump json_visualization_data to outputs/dataset_descriptor.json
    with open(f"outputs/{dataset_descriptor}/visualization_data.json", "w") as f:
        json.dump(json_visualization_data, f)
    
    return (dataset_descriptor, json_visualization_data)
    
