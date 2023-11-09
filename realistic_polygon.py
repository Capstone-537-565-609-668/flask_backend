from generate_set import generate_sets
from shapely.geometry import Polygon
import os
import pymongo
import certifi
from dotenv import load_dotenv
load_dotenv()

'''
    1. parks
    2. lakes
    3. sport

'''


def analyze_polygon_data(type_param, xsize, ysize, card):
    client = pymongo.MongoClient(
        os.getenv("DB_URI"), tlsCAFile=certifi.where())
    db = client[os.getenv("MONGO_DBNAME")]
    collection = db[os.getenv("MONGO_COLLECTION")]

    # Find documents of the specified type in the collection
    query = {"type": type_param}
    documents = collection.find(query)

    # Initialize lists to store results for multiple polygons of the specified type
    vertices_list = []

    irregularity_coeff_list = []
    spikiness_score_list = []
    average_radius_list = []

    for data in documents:
        # Number of vertices
        num_vertices = data["num_vertices"]
        vertices_list.append(num_vertices)

        # Irregularity coefficient
        irregularity_coeff = data["irregularity_coeff"]
        irregularity_coeff_list.append(irregularity_coeff)

        # Spikiness score
        spikiness_score = data["spikiness_score"]
        spikiness_score_list.append(spikiness_score)

        # Calculate the average radius
        average_radius = data["average_radius"]
        average_radius_list.append(average_radius)

    # Calculate the minimum and maximum vertices, irregularity, spikiness, and average radius
    min_vertices = min(vertices_list)
    max_vertices = max(vertices_list)
    avg_irregularity = sum(irregularity_coeff_list) / \
        len(irregularity_coeff_list)
    avg_spikiness = sum(spikiness_score_list) / len(spikiness_score_list)
    avg_radius = sum(average_radius_list) / len(average_radius_list)

    # Close the MongoDB connection
    client.close()
    return generate_sets(card, xsize, ysize, [min_vertices, max_vertices], show_grid=True, irregularity_clip=avg_irregularity, spikiness_clip=avg_spikiness)
    # return {
    #     "min_vertices": min_vertices,
    #     "max_vertices": max_vertices,
    #     "average_irregularity": avg_irregularity,
    #     "average_spikiness": avg_spikiness,
    #     "average_radius": avg_radius
    # }

# Usage example:
# type_to_analyze = "lakes"
# results = analyze_polygon_data(type_to_analyze, 500, 500, 10)
# print("Results for type:", type_to_analyze)
# print("Minimum Vertices:", results["min_vertices"])
# print("Maximum Vertices:", results["max_vertices"])
# print("Average Irregularity:", results["average_irregularity"])
# print("Average Spikiness:", results["average_spikiness"])
# print("Average Radius:", results["average_radius"])
