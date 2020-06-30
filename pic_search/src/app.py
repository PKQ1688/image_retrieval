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
        parse_args()
    file_id = request.files.get('FileId', "")
    file_image = request.files.get('FileImage', "")

    if file_id:
        ids = str(file_id.read().decode("utf-8")).strip().split(",")
        ids = ids[:-1]
    else:
        ids = args['Id'].split(",")

    if file_image:
        image = str(file_image.read().decode("utf-8")).strip().split(",")
        image = image[:-1]
    else:
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
    file_id = request.files.get('FileId', "")

    if file_id:
        ids = str(file_id.read().decode("utf-8")).strip().split(",")
        ids = ids[:-1]
    else:
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
    file_id = request.files.get('FileId', "")
    file_image = request.files.get('FileImage', "")

    if file_id:
        ids = str(file_id.read().decode("utf-8")).strip().split(",")
        ids = ids[:-1]
    else:
        ids = args['Id'].split(",")

    if file_image:
        image = str(file_image.read().decode("utf-8")).strip().split(",")
        image = image[:-1]
    else:
        image = args['Image'].split(",")

    try:
        init_conn()
        result = do_search(index_client, conn, cursor, img_to_vec, image)


        # with open("results_0630.txt","w") as f:
        #    f.write(str(ids).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')
        #    f.write("\n")
        #    for i in result:
        #        f.write(str(i).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')

        return "{0},{1}".format(ids, result)
    except Exception as e:
        return "Error with {}".format(e), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)