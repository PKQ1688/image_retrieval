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
img_to_vec = Img2Vec(model_path="/data/model/vgg_triplet.pth")


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
    time1 = time.time()
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \
        add_argument('File', type=str). \
        parse_args()
    file = args['File']
    if file:
        print("file:",file)
        with open(file+'_id.txt') as fid:
            ids = fid.read().strip().split(",")
            ids = ids[:-1]
        with open(file+'_base64.txt') as fimg:
            image = fimg.read().strip().split(",")
            image = image[:-1]
        print(ids, len(image))
    else:
        ids = args['Id'].split(",")
        image = args['Image'].split(",")

    try:
        time2 = time.time()
        status, info = do_insert(index_client, conn, cursor, img_to_vec, ids, image)
        time3 = time.time()
        print("------------do_insert_time:", time3-time2)
        print("------------total_insert_time:", time3-time1)
        return "{0},{1}".format(status, info)
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/deleteImages', methods=['GET'])
def do_delete_images_api():
    time1 = time.time()
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        parse_args()
    ids = args['Id'].split(",")
    try:
        status, info = do_delete(index_client, conn, cursor, ids)
        time2 = time.time()
        print("------------total_delete_time:", time2-time1)
        return "{0},{1}".format(status, info), 200
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/countImages', methods=['GET'])
def do_count_images_api():
    try:
        rows = do_count()
        return "{}".format(rows), 200
    except Exception as e:
        return "Error with {}".format(e), 400


@app.route('/getSimilarImages', methods=['GET'])
def do_search_images_api():
    time1 = time.time()
    args = reqparse.RequestParser(). \
        add_argument('Id', type=str). \
        add_argument('Image', type=str). \
        add_argument('File', type=str). \
        parse_args()
    file = args['File']
    if file:
        print("file:",file)
        with open(file+'_id.txt') as fid:
            ids = fid.read().strip().split(",")
            ids = ids[:-1]
        with open(file+'_base64.txt') as fimg:
            image = fimg.read().strip().split(",")
            image = image[:-1]
        print(ids, len(image))
    else:
        ids = args['Id'].split(",")
        image = args['Image'].split(",")
    time2 = time.time()
    # ids = args['Id'].split(",")
    # image = args['Image'].split(",")

    try:
        time3 = time.time()
        init_conn()
        time4 = time.time()
        result = do_search(index_client, conn, cursor, img_to_vec, image)
        time5 = time.time()
        print("\n------------args_time:", time2-time1)
        print("\n------------do_split_time:", time3-time2)
        print("\n------------do_init_time:", time4-time3)
        print("\n------------do_search_time:", time5-time4)
        print("\n------------total_search_time:", time5-time1)

        with open("results.txt","w") as f:
           f.write(str(ids).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')
           f.write("\n")
           for i in result:
               f.write(str(i).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')
        
        return "{0},{1}".format(ids, result)
    except Exception as e:
        return "Error with {}".format(e), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
