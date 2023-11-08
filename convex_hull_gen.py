import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from utils import convert_for_visualize


def convex_hull_gen(num_points, xsize, ysize):

    try:

        # random_points = np.random.randint(
        #     min_coord, max_coord, size=(num_points, 2))

        min_x = 0
        min_y = 0
        x = np.random.uniform(min_x, xsize, size=(num_points, 1))
        y = np.random.uniform(min_y, ysize, size=(num_points, 1))
        random_points = [(x1[0], y1[0]) for x1, y1 in zip(x,y)]
        hull = ConvexHull(random_points)

        # Access the vertices of the convex hull
        convex_hull_vertices = [random_points[i] for i in hull.vertices]

        # Add the first point at the end to complete the polygon
        convex_hull_vertices.append(convex_hull_vertices[0])

        # Create a valid polygon from the convex hull vertices
        polygon = Polygon(convex_hull_vertices)

        dataset_descriptor, json_visualization_data = convert_for_visualize([
            polygon])

        return dataset_descriptor, json_visualization_data

    except Exception as e:
        print("An error occurred while computing the convex hull:", str(e))
