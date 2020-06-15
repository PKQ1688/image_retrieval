import os
import logging
from common.config import DATA_PATH, DEFAULT_TABLE
from service.insert import do_insert
from service.search import do_search
from service.count import do_count
from service.delete import do_delete
from flask_cors import CORS
from flask import Flask, request, send_file, jsonify
from flask_restful import reqparse
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_PATH
app.config['JSON_SORT_KEYS'] = False
CORS(app)


@app.route('/addImages', methods=['POST'])
def do_insert_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \
        parse_args()
    ids = args['Id'].split(",")
    image = args['Image'].split(",")

    print(ids,image)
    status = do_insert(ids, image)
    return "{}".format(status)


@app.route('/deleteImages', methods=['POST'])
def do_delete_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        parse_args()
    ids = args['Id']
    status = do_delete(ids)
    return "{}".format(status)


@app.route('/countImages', methods=['POST'])
def do_count_images_api():
    rows = do_count()
    return "{}".format(rows), 200


@app.route('/getSimilarImages', methods=['POST'])
def do_search_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \
        parse_args()
    ids = args['Id']
    image = args['Image']
    result = do_search(image)
    return "{0},{1}".format(ids, result)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
