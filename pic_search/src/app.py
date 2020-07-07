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
from encoder.encode import Img2Vec
from indexer.index import milvus_client
from indexer.tools import connect_mysql
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_PATH
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


@app.route('/addImages', methods=['POST'])
def do_insert_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \

        add_argument('Size', type=int). \
        add_argument('Table', type=str). \
        parse_args()
    file_id = request.files.get('FileId', "")
    file_image = request.files.get('FileImage', "")

    size = args['Size']
    table_name = args['Table']
    if file_id:
        ids = str(file_id.read().decode("utf-8")).strip().split(",")
        ids = ids[:-1]

    else:
        ids = args['Id'].split(",")
        image = args['Image'].split(",")
    # ids = args['Id'].split(",")
    # image = args['Image'].split(",")
    try:
        init_conn()
        status, info = do_insert(index_client, conn, cursor, img_to_vec, ids, image, size, table_name)
        return "{0},{1}".format(status, info)
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/deleteImages', methods=['POST'])
def do_delete_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Table', type=str). \
        add_argument('Id', type=str). \
        parse_args()

    table_name = args['Table']
    file_id = request.files.get('FileId', "")

    if file_id:
        ids = str(file_id.read().decode("utf-8")).strip().split(",")
        ids = ids[:-1]
    else:
        ids = args['Id'].split(",")

    try:
        init_conn()
        status, info = do_delete(index_client, conn, cursor, ids, table_name)
        return "{0},{1}".format(status, info), 200
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/countImages', methods=['POST'])
def do_count_images_api():
    try:
        args = reqparse.RequestParser(). \
            add_argument('Table', type=str). \
            parse_args()
        table_name = args['Table']
        init_conn()
        rows = do_count(table_name)
        return "{}".format(rows), 200
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/getSimilarImages', methods=['POST'])
def do_search_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Table', type=str). \
        add_argument('Image', type=str). \
        add_argument('FileId', type=str). \
        add_argument('FileImage', type=str). \
        parse_args()

    file_id = request.files.get('FileId', "")
    file_image = request.files.get('FileImage', "")
    table_name = args['Table']

    if file_id:
        ids = str(file_id.read().decode("utf-8")).strip().split(",")
        ids = ids[:-1]

    else:
        ids = args['Id'].split(",")
        image = args['Image'].split(",")
    # ids = args['Id'].split(",")
    # image = args['Image'].split(",")
    try:
        init_conn()

        result = do_search(index_client, conn, cursor, img_to_vec, image, table_name)

        # with open("results_0630.txt","w") as f:
        #    f.write(str(ids).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')
        #    f.write("\n")
        #    for i in result:
        #        f.write(str(i).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')

        return "{0},{1}".format(ids, result), 200

    except Exception as e:
        return "Error with {}".format(e), 400


if __name__ == "__main__":

    app.run(host="0.0.0.0",port=5000)

