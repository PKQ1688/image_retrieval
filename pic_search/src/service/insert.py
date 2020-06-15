import logging
from common.config import DEFAULT_TABLE, FILE_NAME
from indexer.index import milvus_client, create_table, insert_vectors, create_index, has_table
from indexer.tools import connect_mysql, create_table_mysql, search_by_image_id, load_data_to_mysql
import datetime
from encoder.encode import img_to_vec
import pymysql
import time


def img_to_vectors(conn, cursor, ids_image, img):
    vectors_img = []
    end_ids_image = []
    for i in range(len(img)):
        try:
            has_id = search_by_image_id(conn, cursor, ids_image[i])
            if has_id:
                print("The id of image has exists:", ids_image[i])
                continue
            vec = img_to_vec(img[i])
            vectors_img.append(vec)
            end_ids_image.append(ids_image[i])
        except:
            print("The image has wrong data:", ids_image[i])
            continue
    return vectors_img, end_ids_image


def get_ids_file(ids_milvus, ids_image):
    with open(FILE_NAME,'w') as f:
        for i in range(len(ids_image)):
            line = str(ids_milvus[i]) + "," + ids_image[i] + '\n'
            f.write(line)


def init_table(index_client, conn, cursor):
    status, ok = has_table(index_client, DEFAULT_TABLE)
    if not ok:
        print("create table.")
        create_table(index_client, DEFAULT_TABLE)
        create_index(index_client, DEFAULT_TABLE)
        create_table_mysql(conn, cursor)


def do_insert(ids_image, img):
    conn = connect_mysql()
    cursor = conn.cursor()

    index_client = milvus_client()
    init_table(index_client, conn, cursor)
    vectors_img, end_ids_image = img_to_vectors(conn, cursor, ids_image, img)
    print(len(vectors_img),end_ids_image)

    try:
        status, ids_milvus = insert_vectors(index_client, DEFAULT_TABLE, vectors_img)
        print("insert_milvus:", status, ids_milvus)
        get_ids_file(ids_milvus, end_ids_image)
        load_data_to_mysql(conn, cursor)
        return status
    except Exception as e:
        logging.error(e)
        return "Fail with error {}".format(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
        if index_client:
            index_client.disconnect()