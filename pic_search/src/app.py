import os
import logging
from service.insert import do_insert
from service.search import do_search
from service.count import do_count
from service.delete import do_delete_images, do_delete_table
from flask_cors import CORS
from flask import Flask, request, send_file, jsonify
from flask_restful import reqparse
from werkzeug.utils import secure_filename
from encoder.encode import Img2Vec
from indexer.index import milvus_client
from indexer.tools import connect_mysql
from indexer.logs import write_log
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

img_to_vec = Img2Vec(model_path="./src/model/vgg_triplet.pth")
index_client = milvus_client()

print("test service!")


def init_conn():
    conn = connect_mysql()
    cursor = conn.cursor()
    return conn, cursor


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
    print(args['Id'])

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
        index_client, conn, cursor = init_conn()
        status, info = do_insert(index_client, conn, cursor, img_to_vec, ids, image, size, table_name)
        return "{0},{1}".format(status, info)
    except Exception as e:
        write_log(e, 1)
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
        index_client, conn, cursor = init_conn()
        status, info = do_delete_images(index_client, conn, cursor, ids, table_name)
        return "{0},{1}".format(status, info), 200
    except Exception as e:
        write_log(e, 1)
        return "Error with {}".format(e), 400


@app.route('/countImages', methods=['POST'])
def do_count_images_api():
    args = reqparse.RequestParser(). \
        add_argument('Table', type=str). \
        parse_args()
    table_name = args['Table']

    print("table_name", table_name)
    try:
        index_client, conn, cursor = init_conn()
        rows_milvus, rows_mysql = do_count(index_client, conn, cursor, table_name)
        return "{0},{1}".format(rows_milvus, rows_mysql), 200
    except Exception as e:
        write_log(e, 1)
        return "Error with {}".format(e), 400


@app.route('/deleteTable', methods=['POST'])
def do_delete_table_api():
    args = reqparse.RequestParser(). \
        add_argument('Table', type=str). \
        parse_args()
    try:
        index_client, conn, cursor = init_conn()
        table_name = args['Table']
        status = do_delete_table(index_client, conn, cursor, table_name)
        return "{}".format(status)
    except Exception as e:
        write_log(e, 1)
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

    if file_image:
        image = str(file_image.read().decode("utf-8")).strip().split(",")
        image = image[:-1]
    else:
        image = args['Image'].split(",")

    try:
        conn, cursor = init_conn()
        result, distance = do_search(index_client, conn, cursor, img_to_vec, image, table_name)
        print("----------------search_results:", result)

        # Python 字典类型转换为 JSON 对象
        result_dic = {"code": 0, "msg": "success"}
        data = []
        for i in range(len(ids)):
            id_dis = []
            for j in range(len(result[i])):
                id_sim = {
                    "id": result[i][j],
                    "similarity": distance[i][j]
                }
                id_dis.append(id_sim)
            re_sim = {
                "id": ids[i],
                "similarImages": id_dis
            }
            data.append(re_sim)

        result_dic["data"] = data
        # with open("results_0630.txt","w") as f:
        #    f.write(str(ids).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')
        #    f.write("\n")
        #    for i in result:
        #        f.write(str(i).replace('[','').replace(']','').replace('\'','').replace('‘','')+'\n')

        # return "{0},{1}".format(ids, result), 200
        return result_dic, 200

    except Exception as e:
        write_log(e, 1)
        return "Error with {}".format(e), 400


if __name__ == "__main__":
    app.run(threaded=True, host="0.0.0.0", port=5000, debug=True)
