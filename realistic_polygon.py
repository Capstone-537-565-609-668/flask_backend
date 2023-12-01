from generate_set import generate_sets
from generate_polygon import generate_polygon
from shapely.geometry import Polygon
import os
import pymongo
import certifi
import ast
from utils import string_to_tuple
import random
from download_csv import convert_to_shape_csv
import geopandas
import json

from dotenv import load_dotenv
load_dotenv()

'''
    1. parks
    2. lakes
    3. sport

'''


def analyze_polygon_data(type_param, card, xsize=500, ysize=500):
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


def generate_realistic_polygons(type_param, card):
    client = pymongo.MongoClient(
        os.getenv("DB_URI"), tlsCAFile=certifi.where())
    db = client[os.getenv("MONGO_DBNAME")]
    collection = db[os.getenv("MONGO_COLLECTION")]

    # Find documents of the specified type in the collection
    query = {"type": type_param}
    documents = collection.find(query)

    # Initialize lists to store results for multiple polygons of the specified type
    vertices_list = []
    centers = []
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

        centers.append(string_to_tuple(data["centroid"]))

    # Close the MongoDB connection
    client.close()
    pols = []

    for i in range(card):
        pols.append(Polygon(generate_polygon(center=random.choice(centers), avg_radius=random.choice(average_radius_list)*10, irregularity=random.choice(
            irregularity_coeff_list), spikiness=random.choice(spikiness_score_list), num_vertices=random.choice(vertices_list))))

    # optional validate
    for_vis = pols[:100]
    print(pols)
    dataset_descriptor = convert_to_shape_csv(
        pols)
    json_visualization_data = geopandas.GeoDataFrame(
        geometry=for_vis).to_json()
    # dump json_visualization_data to outputs/dataset_descriptor.json
    with open(f"outputs/{dataset_descriptor}/visualization_data.json", "w") as f:
        json.dump(json_visualization_data, f)

    return (dataset_descriptor, json_visualization_data)
