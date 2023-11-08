
from scipy.spatial import Voronoi
import numpy as np
from shapely.geometry import Polygon
from utils import convert_for_visualize


def generate_voronoi(seed_points, show_diag=False):

    transformed_points = np.array([[i[0][0], i[0][1]] for i in seed_points])

    vor = Voronoi(transformed_points)

    polygons = []
    for region in vor.regions:
        if -1 not in region and len(region) > 0:
            polygon = [vor.vertices[i] for i in region]
            shapely_polygon = Polygon(polygon)
            polygons.append(shapely_polygon)

    descriptor_id, json_visualization_data = convert_for_visualize(polygons)

    return descriptor_id, json_visualization_data
