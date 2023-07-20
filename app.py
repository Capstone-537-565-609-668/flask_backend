from flask import Flask,render_template, request, jsonify, send_file, abort
from generate_set import generate_sets
from generate_polygon import generate_polygon
import os
import zipfile
from time import sleep

# Get the parent directory of this script. (Global)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/')
def get_json_data():
    # receive card, xsize, ysize, vertices_bound, irregularity_clip, spikiness_clip, show_grid from request body
    card = request.get_json()['card']
    xsize= request.get_json()['xsize']
    ysize = request.get_json()['ysize']
    vertices_bound= request.get_json()['vertices_bound']
    vertices_bound = tuple(vertices_bound)
    irregularity_clip = request.get_json()['irregularity_clip']
    spikiness_clip = request.get_json()['spikiness_clip']
    # Visualize the generated polygons
    dataset_id, for_visualizer = generate_sets(card, xsize, ysize, vertices_bound, show_grid=False,
                          irregularity_clip=irregularity_clip, spikiness_clip=spikiness_clip)

    # return 200 with dataset_id as json
    return jsonify({'dataset_id': dataset_id, 'for_visualizer': for_visualizer})


# go to outputs/:id and then send the files
# for download

OUTPUTS_DIRECTORY = 'outputs'

def find_folder_by_uuid(uuid):
    folder_path = os.path.join(OUTPUTS_DIRECTORY, uuid)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return folder_path
    return None

@app.route('/get_file/<string:uuid>', methods=['GET'])
def get_folder_by_uuid(uuid):
    folder_path = find_folder_by_uuid(uuid)
    if not folder_path:
        abort(404, f"Folder with UUID '{uuid}' not found.")

    zip_file_path = folder_path + '.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)

    # Send the zip archive to the client and delete it afterwards.
    response=send_file(zip_file_path, as_attachment=True)
    # os.remove(zip_file_path)
    return response
    # try:
    #     return send_file(zip_file_path, as_attachment=True)
    # finally:
    #     os.remove(zip_file_path)

app.run(debug=True)                                                             