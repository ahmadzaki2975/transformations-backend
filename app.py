from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, origins=["http://localhost:3000", "https://transformations-frontend.vercel.app"])

@app.route('/')
def index():
    return 'Transformation API by Ahmad Zaki Akmal'

@app.route('/transform', methods=['POST'])
def transform():
    # receive datas
    data = request.get_json()
    n = data["n"]
    coordinates = data["coordinates"]
    vertices = []
    sides = []
    tx = data["tx"]
    ty = data["ty"]
    sx = data["sx"]
    sy = data["sy"]
    shx = data["shx"]
    shy = data["shy"]
    angle = data["angle"] * np.pi / 180
    transformed_vertices = []

    # print(coordinates)
    # make coordinates np.arrays, covert to float
    for i in range(n):
        temp_x = float(coordinates[i]['x'])
        temp_y = float(coordinates[i]['y'])
        vertices.append([temp_x, temp_y, 1])

    # print(vertices)

    # combine each vertex to the next to create a side, combine the last with the first to form the last side
    for i in range(n):
        if i == n-1:
            sides.append([vertices[i], vertices[0]])
        else:
            sides.append([vertices[i], vertices[i+1]])

    #? plot the polygon
    for i in range(n):
        plt.plot([sides[i][0][0], sides[i][1][0]], [sides[i][0][1], sides[i][1][1]], color="blue", linestyle="dashed")
    
    #? apply transformations
    # translation
    translation_matrix = np.array(
        [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0,  1]
        ]
    )

    # scaling
    scaling_matrix = np.array(
        [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0,  1]
        ]
    )

    # shearing
    shearing_matrix = np.array(
        [
            [1, shx, 0],
            [shy, 1, 0],
            [0,  0,  1]
        ]
    )

    # rotation
    rotation_matrix = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1] 
        ]
    )

    transformation_matrix = translation_matrix @ scaling_matrix @ shearing_matrix @ rotation_matrix

    print(transformation_matrix)

    # apply transformation matrix to each vertex
    for i in range(n):
        transformed_vertices.append(np.dot(transformation_matrix, vertices[i]))

    # combine each vertex to the next to create a side, combine the last with the first to form the last side
    transformed_sides = []
    for i in range(n):
        if i == n-1:
            transformed_sides.append([transformed_vertices[i], transformed_vertices[0]])
        else:
            transformed_sides.append([transformed_vertices[i], transformed_vertices[i+1]])

    #? plot the transformed polygon
    for i in range(n):
        plt.plot([transformed_sides[i][0][0], transformed_sides[i][1][0]], [transformed_sides[i][0][1], transformed_sides[i][1][1]], color="red")

    plt.autoscale()
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.gca().invert_xaxis()
    # plt.gca().invert_yaxis()
    # plt.show()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')


