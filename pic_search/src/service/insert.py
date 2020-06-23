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

    time1 = time.time()
    for i in range(len(ids_image)):
        has_id = search_by_image_id(conn, cursor, ids_image[i])
        if has_id:
            print("The id of image has exists:", ids_image[i])
            info.append(ids_image[i])
            continue
        else:
            img_list.append(img[i])
            ids_img.append(ids_image[i])
    time2 = time.time()

    # if len(img_list):
    #     try:
    vectors_img = img_to_vec(img_list)
        # except:
            # print("The imagebase64 has wrong data.")
            # info = "The imagebase6 has wrong data."
    time3 = time.time()
    print("_____insert_mysql_time:", time2 -time1)
    print("_____get_img_vec_time:", time3 -time2)
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
    init_table(index_client, conn, cursor)
    vectors_img, ids_img, info = img_to_vectors(conn, cursor, img_to_vec, ids_image, img)
    print(len(vectors_img),len(ids_img))

    if len(vectors_img):
        time1 = time.time()
        status, ids_milvus = insert_vectors(index_client, DEFAULT_TABLE, vectors_img)
        time2 = time.time()

        print("insert_milvus:", status, ids_milvus)
        get_ids_file(ids_milvus, ids_img)
        load_data_to_mysql(conn, cursor)
        time3 = time.time()
        print("_____insert_milvus_time:", time2 -time1)
        print("_____load_mysql_time:", time3 -time2)
        return status, info
    else:
        return None, info