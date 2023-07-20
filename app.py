from flask import Flask,render_template, request, jsonify
from generate_set import generate_sets
from generate_polygon import generate_polygon

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
    dataset_id = generate_sets(card, xsize, ysize, vertices_bound, show_grid=False,
                          irregularity_clip=irregularity_clip, spikiness_clip=spikiness_clip)

    # return 200 with dataset_id as json
    return jsonify({'dataset_id': dataset_id})

app.run(debug=True)