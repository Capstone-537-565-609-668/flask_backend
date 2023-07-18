import math
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from download_csv import convert_to_shape_csv
from shapely.geometry import Polygon
from utils import clip
from generate_polygon import generate_polygon


'''
  Time : O(N) , where N is number of vertices
  space : O(M)
'''


def generate_sets(card, xsize, ysize, vertices_bounds, show_grid=True, irregularity_clip=0.8, spikiness_clip=0.8):
    # card=100
    gridCols = math.ceil(math.sqrt(card))
    # 5*5=> 25 cells. Need to distribute card into these cells
    gridRows = math.ceil(math.sqrt(card))
    # vertices_bounds=[3,10]
    # xsize=1000
    # ysize=1000
    print(card, gridCols, gridRows, gridCols * gridRows)
    # print("sfwenfwefnweuifhnewj")
    if card > (gridCols*gridRows):
        print("heeeeeerrrrre")
        card = gridCols*gridRows
        # raise Exception("Cannot generate non-overlapping polygons")

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

    black = (0, 0, 0)
    white = (255, 255, 255)
    img = Image.new('RGB', (xsize, ysize), white)
    im_px_access = img.load()
    draw = ImageDraw.Draw(img)

    shapes = []
    # center_bounds=[50, 400]
    avg_radius = 50

    point = 0
    if(show_grid):
        height = ysize
        width = xsize
        image = Image.new(mode='L', size=(height, width), color=255)

        # Draw some line
        y_start = 0
        y_end = image.height
        step_size = int(xsize/gridRows)

        for x in range(0, image.width, step_size):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill=128)

        x_start = 0
        x_end = image.width

        for y in range(0, image.height, step_size):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill=128)

    # if(20 > int(xsize/(2*gridCols))):
    #   raise Exception("Cannot have a decreasing a randInt")

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
                                               random.random(), 0, irregularity_clip),
                                           spikiness=clip(
                                               random.random(), 0, spikiness_clip),
                                           num_vertices=random.randint(vertices_bounds[0], vertices_bounds[1])))
            # print(shapes[point])
            draw.polygon(shapes[point], outline=black, fill=white)
            draw.line(shapes[point] + [shapes[point][0]], width=2, fill=black)

            #  break
            point += 1

    # return image
    pols = []
    for i in shapes:
        # i.append(i[0])
        p1 = Polygon(i)
        pols.append(p1)
    convert_to_shape_csv(pols)
    
    # return img

    # img.show()
