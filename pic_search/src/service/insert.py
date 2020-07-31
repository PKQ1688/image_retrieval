import logging as log
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, create_table, insert_vectors, create_index, has_table
from indexer.tools import connect_mysql, create_table_mysql, search_by_image_id, load_data_to_mysql
import datetime
import time
from indexer.logs import write_log
import uuid
import os

def get_img_ids(conn, cursor, ids_image, img, table_name):
    img_list = []
    ids_img = []
    info = []

    for i in range(len(ids_image)):
        has_id = search_by_image_id(conn, cursor, ids_image[i], table_name)
        if has_id:
            print("The id of image has exists:", ids_image[i])
            info.append(ids_image[i])
            continue
        else:
            img_list.append(img[i])
            ids_img.append(ids_image[i])

    return img_list, ids_img, info


def get_ids_file(ids_milvus, ids_image, file_name):
    with open(file_name,'w') as f:
        for i in range(len(ids_image)):
            line = str(ids_milvus[i]) + "," + ids_image[i] + '\n'
            f.write(line)


def init_table(index_client, conn, cursor, table_name):
    status, ok = has_table(index_client, table_name)
    print("has_table:", status, ok)
    if not ok:
        print("create table.")
        create_table(index_client, table_name)
        create_index(index_client, table_name)
        create_table_mysql(conn, cursor, table_name)


def insert_img(index_client, conn, cursor, img_to_vec, insert_img_list, insert_ids_img, table_name):
    vectors_img = img_to_vec(insert_img_list)
    # print(len(insert_img_list),len(insert_ids_img))
    status, ids_milvus = insert_vectors(index_client, table_name, vectors_img)

    file_name = str(uuid.uuid1()) + ".csv"
    get_ids_file(ids_milvus, insert_ids_img, file_name)
    print("load data to mysql:", file_name)
    load_data_to_mysql(conn, cursor, table_name, file_name)
    return status


def do_insert(index_client, conn, cursor, img_to_vec, ids_image, img, size, table_name):
    if not table_name:
        table_name = DEFAULT_TABLE
    if not size:
        size = 200
    print("table_name:", table_name, ", num of orgin ids:", len(ids_image),", num of orgin img:", len(img))

    if len(ids_image)!= len(img):
        return "The number of pictures is not consistent with the ID number, please check!", None

    init_table(index_client, conn, cursor, table_name)
    img_list, ids_img, info = get_img_ids(conn, cursor, ids_image, img, table_name)
    print("num of the insert images:", len(img_list))
    if not img_list:
        return None, "All the image id exists!"
    try:
        i = 0
        while i+size<len(ids_img):
            insert_img_list = img_list[i:i+size]
            insert_ids_img = ids_img[i:i+size]
            i = i+size
            print("doing insert, size:", size, "the num of insert vectors:", len(insert_img_list))
            status = insert_img(index_client, conn, cursor, img_to_vec, insert_img_list, insert_ids_img, table_name)
        else:
            insert_img_list = img_list[i:len(ids_image)]
            insert_ids_img = ids_img[i:len(ids_image)]
            print("doing insert, size:", size, ",the num of insert vectors:", len(insert_img_list))
            status = insert_img(index_client, conn, cursor, img_to_vec, insert_img_list, insert_ids_img, table_name)

        return status, info
    except Exception as e:
        # log.error(e)
        write_log(e, 1)
        return None, "Error with {}".format(e)
