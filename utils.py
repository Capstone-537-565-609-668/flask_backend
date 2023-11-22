import math
import random
from typing import List
from shapely.geometry import Polygon
from download_csv import convert_to_shape_csv
import geopandas
import json
import ast
'''
  Time : O(1)
  Space : O(1)
'''


def clip(value, lower, upper):
    """
    Given an interval, values outside the interval are clipped to the interval edges.
    """
    return min(upper, max(value, lower))


'''
  Time : O(N)
  Space : O(N)

  where N is the steps / vertices
'''


def random_angle_steps(steps: int, irregularity: float) -> List[float]:
    """Generates the division of a circumference in random angles.

    Args:
        steps (int): number of vertices
            the number of angles to generate.
        irregularity (float):
            variance of the spacing of the angles between consecutive vertices.
    Returns:
        List[float]: the list of the random angles.
    """
    # generate n angle steps
    angles = []
    lower = (2 * math.pi / steps) - irregularity
    upper = (2 * math.pi / steps) + irregularity
    cumsum = 0
    for i in range(steps):
        angle = random.uniform(lower, upper)
        angles.append(angle)
        cumsum += angle

    # normalize the steps so that point 0 and point n+1 are the same
    cumsum /= (2 * math.pi)
    for i in range(steps):
        angles[i] /= cumsum
    return angles


def convert_for_visualize(polygons):
    poly = []
    for i in polygons:
        p1 = Polygon(i)
        poly.append(p1)

    for_vis = poly[:15]
    dataset_descriptor = convert_to_shape_csv(poly)
    json_visualization_data = geopandas.GeoDataFrame(
        geometry=for_vis).to_json()
    # dump json_visualization_data to outputs/dataset_descriptor.json
    with open(f"outputs/{dataset_descriptor}/visualization_data.json", "w") as f:
        json.dump(json_visualization_data, f)

    return dataset_descriptor, json_visualization_data


def string_to_tuple(coord_string):
    try:
        # Using ast.literal_eval to safely evaluate the string as a literal
        coord_tuple = ast.literal_eval(coord_string)

        # Checking if the result is a tuple of two floats
        if isinstance(coord_tuple, tuple) and len(coord_tuple) == 2 and all(isinstance(x, float) for x in coord_tuple):
            return coord_tuple
        else:
            raise ValueError("Invalid input: Not a tuple of two floats")
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        return None
