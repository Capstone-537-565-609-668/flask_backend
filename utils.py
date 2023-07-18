import math
import random
from typing import List

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
