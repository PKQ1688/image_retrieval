import logging
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, search_vectors
from indexer.tools import connect_mysql, search_by_milvus_ids
import time


def do_search(index_client, conn, cursor, img_to_vec, img_list):
    vectors_img = img_to_vec(img_list)

    status, ids_milvus = search_vectors(index_client, DEFAULT_TABLE, vectors_img)

    re_ids_img = []
    for ids in ids_milvus:
        vids = [x.id for x in ids]
        re_ids = search_by_milvus_ids(conn, cursor, vids)
        re_ids_img.append(re_ids)
    return re_ids_img
