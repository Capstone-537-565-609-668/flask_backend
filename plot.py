# card,xsize,ysize,vertices_bounds,show_grid=True,irregularity_clip=0.8, spikiness_clip=0.8
# error handling when card > canvas size
# when tested with generate_sets(200000,50000,50000,[3,7],False) : its taking more than 3m 12secs and it did not draw the canvas
# we have to parallise it


# First plot is with card vs time keeping the range for number of vertices const
# Breaking condition : card > (gridCols*gridRows):
import matplotlib.pyplot as plt
import time
from generate_set import generate_sets


def PLOT():

    cardi = []
    time_1 = []
    for i in range(10, 7000, 25):
        start_time = time.time()
        generate_sets(i, 10000, 10000, [3, 7], False)
        end_time = time.time()
        cardi.append(i)
        time_1.append(end_time - start_time)

    # x , y
    plt.plot(cardi, time_1, label='cardinality')
    plt.xlabel("Cardinality / Vertices")
    plt.ylabel("Time (in secs)")

    # Second plot is with vertices vs time keeping the cardinality const
    verti = []
    time_2 = []

    for i in range(10, 5000, 25):
        start_time = time.time()
        generate_sets(64, 10000, 10000, [i, i], False)
        end_time = time.time()
        verti.append(i)
        time_2.append(end_time - start_time)

    # x , y
    plt.plot(verti, time_2, label='Vertices')
    plt.legend()

    plt.show()
