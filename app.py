# app.py
from flask import Flask, render_template, jsonify
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
from support_2 import MyPlots
from view_home import Home

app = Flask(__name__)

home = Home(app)

# Function to generate sample contour data
def generate_contour_data():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    return X.tolist(), Y.tolist(), Z.tolist()

def get_data():
    data = pd.read_csv("static\\data\\L3.csv", sep=';')
    data['x'] = (data.Ax + data.Bx)/2
    data['y'] = -0.2*abs(data.Bx - data.Ax)
    X, Y, Z= to_grid((data.x,data.y), data.resistividade)
    Z = np.nan_to_num(Z, nan = -10000000)
    return X, Y, Z.tolist()[::-1]

def to_grid(points, Z):
    X1 = sorted(np.unique(points[0]))
    Y1 = sorted(np.unique(points[1]))
    #Y1 = np.linspace(min(points[1]), max(points[1]), 100).tolist()
    grid_x, grid_y = np.meshgrid(X1,Y1)
    return X1, Y1, griddata(points, Z, (grid_x,grid_y), method='linear')


myplots = MyPlots()
myplots.load_files("static\data\L3.csv")
home.set_data(myplots)
#home.draw()

# Route to serve HTML page

# @app.route('/')
# def index():
#     return render_template('index.html')

# API endpoint to serve contour data
@app.route('/')
def index():
    graph = myplots.return_contour(myplots.data1, cont=myplots.contours, log=True, title='teste')
       
    return render_template('index.html', graph=graph)
# def contour_data():
#     # X, Y, Z = generate_contour_data()
#     X, Y, Z = get_data()
#     return jsonify({'X': X, 'Y': Y, 'Z': Z})

# # API endpoint to serve contour data
# @app.route('/example-data')
# def example_data():
#     X, Y, Z = generate_contour_data()
#     return jsonify({'X': X, 'Y': Y, 'Z': Z})

if __name__ == '__main__':
    app.run(debug=True)
