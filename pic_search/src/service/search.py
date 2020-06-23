import logging
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, search_vectors
from indexer.tools import connect_mysql, search_by_milvus_ids
from encoder.encode import Img2Vec
import time


def do_search(index_client, conn, cursor, img_to_vec, img_list):

    time1 = time.time()
    vectors_img = img_to_vec(img_list)
    time2 = time.time()
    print("img_to_vec_time:", time2-time1)

    time1 = time.time()
    status, ids_milvus = search_vectors(index_client, DEFAULT_TABLE, vectors_img)
    time2 = time.time()
    print("milvus_search_time:", time2-time1)

    re_ids_img = []
    time1 = time.time()
    for ids in ids_milvus:
        vids = [x.id for x in ids]

        re_ids = search_by_milvus_ids(conn, cursor, vids)
        re_ids_img.append(re_ids)
    time2 = time.time()
    print("search_with_mysql_time:", time2-time1)
    print("search_mysql", len(re_ids_img))
    return re_ids_img
