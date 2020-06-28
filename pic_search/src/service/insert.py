import logging
from common.config import DEFAULT_TABLE, FILE_NAME
from indexer.index import milvus_client, create_table, insert_vectors, create_index, has_table
from indexer.tools import connect_mysql, create_table_mysql, search_by_image_id, load_data_to_mysql
import datetime
from encoder.encode import Img2Vec
import time


def img_to_vectors(conn, cursor, img_to_vec, ids_image, img):
    vectors_img = []
    img_list = []
    ids_img = []
    info = []

    for i in range(len(ids_image)):
        has_id = search_by_image_id(conn, cursor, ids_image[i])
        if has_id:
            print("The id of image has exists:", ids_image[i])
            info.append(ids_image[i])
            continue
        else:
            img_list.append(img[i])
            ids_img.append(ids_image[i])

    vectors_img = img_to_vec(img_list)
    return vectors_img, ids_img, info


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


def do_insert(index_client, conn, cursor, img_to_vec, ids_image, img):
    try:
        init_table(index_client, conn, cursor)
        vectors_img, ids_img, info = img_to_vectors(conn, cursor, img_to_vec, ids_image, img)
        log.info(vectors_img)
        # print(len(vectors_img),len(ids_img))
        status, ids_milvus = insert_vectors(index_client, DEFAULT_TABLE, vectors_img)

        get_ids_file(ids_milvus, ids_img)
        load_data_to_mysql(conn, cursor)

        return status, info
    except Exception as e:
        return None, "Error with {}".format(e)