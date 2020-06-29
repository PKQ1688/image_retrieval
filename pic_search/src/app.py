import os
import logging
from common.config import DEFAULT_TABLE
from service.insert import do_insert
from service.search import do_search
from service.count import do_count
from service.delete import do_delete
from flask_cors import CORS
from flask import Flask, request, send_file, jsonify
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from encoder.encode import Img2Vec
from indexer.index import milvus_client
from indexer.tools import connect_mysql
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

conn = connect_mysql()
cursor = conn.cursor()
index_client = milvus_client()
img_to_vec = Img2Vec(model_path="./src/model/vgg_triplet.pth")


def init_conn():
    global index_client
    global conn
    if index_client and conn:
        return
    if not index_client:
        index_client = milvus_client()
    elif not conn:
        conn = connect_mysql()
        cursor = conn.cursor()


@app.route('/addImages', methods=['GET'])
def do_insert_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \
        add_argument('File', type=str). \
        parse_args()
    ids = args['Id'].split(",")
    image = args['Image'].split(",")
    try:
        init_conn()
        status, info = do_insert(index_client, conn, cursor, img_to_vec, ids, image)
        return "{0},{1}".format(status, info)
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/deleteImages', methods=['GET'])
def do_delete_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        parse_args()
    ids = args['Id'].split(",")
    try:
        init_conn()
        status, info = do_delete(index_client, conn, cursor, ids)
        return "{0},{1}".format(status, info), 200
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/countImages', methods=['GET'])
def do_count_images_api():
    try:
        init_conn()
        rows = do_count()
        return "{}".format(rows), 200
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/getSimilarImages', methods=['GET'])
def do_search_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \
        parse_args()
    ids = args['Id'].split(",")
    image = args['Image'].split(",")
    try:
        init_conn()
        result = do_search(index_client, conn, cursor, img_to_vec, image)
        return "{0},{1}".format(ids, result)
    except Exception as e:
        return "Error with {}".format(e), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
