# app.py
from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

# Function to generate sample contour data
def generate_contour_data():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    return X.tolist(), Y.tolist(), Z.tolist()

# Route to serve HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to serve contour data
@app.route('/contour-data')
def contour_data():
    X, Y, Z = generate_contour_data()
    return jsonify({'X': X, 'Y': Y, 'Z': Z})

if __name__ == '__main__':
    app.run(debug=True)
