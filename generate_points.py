from utils import clip
import math
import random
from generate_polygon import generate_polygon


def generate_points(card, xsize, ysize, show_grid=False):
    # card=100
    gridCols = math.ceil(math.sqrt(card))
    # 5*5=> 25 cells. Need to distribute card into these cells
    gridRows = math.ceil(math.sqrt(card))
    # vertices_bounds=[3,10]
    # xsize=1000
    # ysize=1000
    if card > (gridCols*gridRows):
        raise Exception("Cannot generate non-overlapping polygons")
    mapping = dict()  # key: rowNum, value:[colNum]
    generated_polygon_centers = 0
    while generated_polygon_centers != card:
        xval = random.randint(0, gridRows-1)
        yval = random.randint(0, gridCols-1)
        if not mapping.get(xval):
            mapping[xval] = [yval]
            generated_polygon_centers += 1
        else:
            if (not (yval in mapping[xval])):
                mapping[xval].append(yval)
                generated_polygon_centers += 1

    """
    1. Distribute polygons to cells: {key: (row, col) => we can estimate the center of the cell => rowNum*size+colNum*size}
      - Estimate size of the cell: (500/5, 500/5)
      - vetices bound input
    2. Generate a polygon in these cells
  """

    shapes = []

    for key in mapping.keys():
        for value in mapping[key]:
            centerx = (clip((xsize/(2*gridCols))+value*(xsize/gridCols), 0, xsize),
                       clip((ysize/(2*gridRows))+(key)*(ysize/(gridRows)), 0, ysize))
            #  centerx=((value+1)*(xsize/gridCols), (key+1)*(ysize/gridRows))
            #  print(centerx)
            #  print(avg_radius)

            # We can do parallel execution in this loop

            shapes.append(generate_polygon(center=centerx,
                                           avg_radius=random.randint(
                                               20, max(21, int(xsize/(2*gridCols)))),
                                           irregularity=clip(
                                               random.random(), 0, 0),
                                           spikiness=clip(
                                               random.random(), 0, 0),
                                           num_vertices=1))

    return shapes
