import logging as log
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, search_vectors, get_vector_by_ids
from indexer.tools import connect_mysql, search_by_milvus_ids
import time


def do_search(index_client, conn, cursor, img_to_vec, img_list, table_name):
    if not table_name:
        table_name = DEFAULT_TABLE
    vectors_img = img_to_vec(img_list)
    print("the num of search images:", len(vectors_img))
    print("doing search, table_name:", table_name)
    status, ids_milvus = search_vectors(index_client, table_name, vectors_img)

    # print("distance_array:", ids_milvus.distance_array)
    re_ids_img = []
    for ids in ids_milvus:
        vids = [x.id for x in ids]

        re_ids = search_by_milvus_ids(conn, cursor, vids, table_name)
        re_ids_img.append(re_ids)

    return re_ids_img, ids_milvus.distance_array
