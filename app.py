from flask import Flask,render_template, request
import random
from generate_set import generate_sets
from generate_polygon import generate_polygon
from PIL import Image,  ImageDraw
import io
import base64
app = Flask(__name__)


@app.route('/')
def get_json_data():
    # receive card, xsize, ysize, vertices_bound, irregularity_clip, spikiness_clip, show_grid from request body
    card = request.get_json()['card']
    xsize= request.get_json()['xsize']
    ysize = request.get_json()['ysize']
    vertices_bound= request.get_json()['vertices_bound']
    vertices_bound = tuple(vertices_bound[0], vertices_bound[1])
    irregularity_clip = request.get_json()['irregularity_clip']
    spikiness_clip = request.get_json()['spikiness_clip']
    
    # card = 36
    # xsize = 500
    # ysize = 500
    # vertices_bound = (3 , 7)
    # irregularity_clip = (0.0, 0.8)
    # spikiness_clip = (0.0, 0.8)
    # show_grid = True
    

    # Visualize the generated polygons
    Image = generate_sets(card, xsize, ysize, vertices_bound, show_grid=False,
                          irregularity_clip=irregularity_clip, spikiness_clip=spikiness_clip)

    # pass this Image to the html template

    # st.image(image=Image, caption='Polygon Generation')

    # Download the generated polygons as CSV
    buffer = io.BytesIO()
    Image.save(buffer, format='PNG')
    buffer.seek(0)

    # Encode the image data as a base64 string
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Render the HTML template with the image data
    return render_template('index.html', image_data=image_data)




# Download the generated polygons as Shapefile
# with open('my_file_shape.shp', 'rb') as f:
#     st.download_button('Download Shapefile', f,
#                        mime='application/octet-stream')
