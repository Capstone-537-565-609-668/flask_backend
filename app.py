from flask import Flask,render_template
import random
from generate_set import generate_sets
from generate_polygon import generate_polygon
from PIL import Image,  ImageDraw
import io
import base64
app = Flask(__name__)


@app.route('/')
def hello():

    




    # USER INPUTS
    # card = st.number_input("Enter the number of polygons", 1, 100000, 36)
    # xsize = st.number_input("Enter the xsize", 1, 100000, 500)
    # ysize = st.number_input("Enter the ysize", 1, 100000, 500)
    # vertices_bounds = st.slider("Enter the range of vertices", 3, 10, (3, 7))
    # irregularity_clip = st.slider(
    #     "Enter the range of irregularity", 0.0, 1.0, (0.0, 0.8))
    # spikiness_clip = st.slider(
    #     "Enter the range of spikiness", 0.0, 1.0, (0.0, 0.8))
    # show_grid = st.checkbox("Show Grid", value=True)

    card = 36
    xsize = 500
    ysize = 500
    vertices_bound = (3 , 7)
    irregularity_clip = (0.0, 0.8)
    spikiness_clip = (0.0, 0.8)
    show_grid = True
    

    # Visualize the generated polygons
    Image = generate_sets(card, xsize, ysize, vertices_bound, show_grid,
                          irregularity_clip=irregularity_clip[1], spikiness_clip=spikiness_clip[1])

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
