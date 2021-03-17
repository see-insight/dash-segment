import numpy as np
import json
from skimage import io, data
from PIL import Image

from see import GeneticSearch


import dash_canvas
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

from utils import (parse_jsonstring, segmentation_generic,
                   image_with_contour, image_without_contour, image_string_to_PILImage)
from dash_canvas.components import image_upload_zone

import subprocess

import shutil 

# Image to segment and shape parameters
# filename = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Mitochondria%2C_mammalian_lung_-_TEM_%282%29.jpg'
filename = "assets/Snail_resize.jpg"
try:
    img = io.imread(filename, as_gray=True)
except:
    img = data.coins()
height, width = img.shape
canvas_width = 500
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width


app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        dcc.Tabs(
            id='segmentation-tabs',
            value='segmentation-canvas-tab',
            children=[
                dcc.Tab(
                    label='Annotation tool',
                    value='segmentation-canvas-tab',
                    children=[
                        dash_canvas.DashCanvas(
                            id='canvas',
                            width=canvas_width,
                            height=canvas_height,
                            scale=scale,
                            filename=filename,
                            goButtonTitle='Segmentation'
                        ),
                        image_upload_zone('upload-image'),

                ]),
                #dcc.Tab(
                   # label='Ground Truth Image',
                    #value='ground-truth-tab',
                    #children=[
                     #  dcc.Graph(
                      # id='ground-truth',
                       #figure=image_with_contour('assets/Snailcpy_GT.jpg',
                        #                            img > 0, shape=(height, width))
                       #)

                    #]),
                dcc.Tab(
                    label='Segmentation result',
                    value='segmentation-result-tab',
                    children=[
                        dcc.Graph(
                        id='segmentation',
                        figure=image_with_contour(np.ones_like(img),
                                    img > 0, shape=(height, width))
                        ),
                      # dcc.Graph(
                       #id='ground-truth2',
                       #figure=image_with_contour('assets/Snailcpy_GT.jpg',
                        #                            img > 0, shape=(height, width))
                       #)
                    ]),
                dcc.Tab(
                     label='How to use this app',
                     value='segmentation-help-tab',
                     children=[
                        html.Img(id='segmentation-help',
                                 src='assets/segmentation.gif',
                                 width='100%'),
                     ]
                )
            ]
        ),
    ], className="seven columns"),
    html.Div([
	html.Img(src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png', width='30px'),
        html.A(
              id='gh-link',
              children=[
                  'View on GitHub'],
              href="http://github.com/plotly/canvas-portal/"                          			"blob/master/apps/segmentation/app.py",
              style={'color': 'black',
                    'border':'solid 1px black',
                    'float':'left'}
                    ),
        html.H2(children='SEE-Segment Annotation tool'),
        dcc.Markdown('''
                Draw on the picture to annotate each object
                you want to segment, then press the "Segmentation"
                button to trigger the segmentation.
            '''),
        html.Br(),
        html.Label('Segmentation algorithm'),
        dcc.Dropdown(
            id='algorithm',
            options=[
                    {'label': 'Watershed', 'value': 'watershed'},
                    {'label': 'GeneticSearch', 'value': 'genetic_search'},
                    {'label': 'Random Walker', 'value': 'random_walker'},
                    {'label': 'Random Forest', 'value': 'random_forest'}
                ],
                value='watershed'
            ),
        ], className="five columns")],# Div
    className="row")


@app.callback(Output('segmentation', 'figure'),
            [Input('canvas', 'json_data')],
            [State('canvas', 'image_content'),
            State('algorithm', 'value')])
def update_figure_upload(string, image, algorithm):
    print("update figure")
    if string:
        if image is None:
            im = img
            image = img
        else:
            #print("Before PILImage")
            im = image_string_to_PILImage(image)
            im = np.asarray(im)
            #print("After PILImage")
        shape = im.shape[:2]
        #print(f"Before jsonstring - Dirk was here {len(string)}")
        mask = parse_jsonstring(string, shape=shape)
        #print("DIRK WAS HERE")
        #skimage.io.imsave("medial.png", img_as_uint(imgSk))
  
        io.imsave("Snail_GT.jpg", mask)
        #file_copy("Snail_GT.jpg", "assets/Snailcpy_GT.jpg")

        #file_copy function can be removed, the code below can be called----
        #shutil.copyfile("Snail_GT.jpg", "assets/Snailcopy1_GT.jpg") 
      
        
        #import subprocess
        if mask.sum() > 0:

            seg = segmentation_generic(im, mask, mode=algorithm)
            
        else:
        	seg = np.zeros(shape)
        
        return image_with_contour(im, seg, shape=shape)
    else:
        raise PreventUpdate


#This function can be removed and shutil.copfile() can be used in the update_figure_upload function
def file_copy(src, dest):
	#Copy the source to destination
	shutil.copyfile(src, dest) #Update dest filename after each segmentation
	return
    
@app.callback(Output('canvas', 'image_content'),
            [Input('upload-image', 'contents')])
def update_canvas_upload(image_string):
    # The line below causes NoneType Error
    if image_string is None:
        raise PreventUpdate
    else:        
        print("uploading", image_string[:100])
        return image_string


@app.callback(Output('segmentation-tabs', 'value'),
                [Input('canvas', 'json_data')])
def change_focus(string):
    if string:
        return 'segmentation-result-tab'
    return 'segmentation-canvas-tab'



if __name__ == '__main__':
    app.run_server(debug=True)

