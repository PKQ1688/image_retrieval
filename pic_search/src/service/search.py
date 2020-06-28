import logging as log
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, search_vectors
from indexer.tools import connect_mysql, search_by_milvus_ids, get_vector_by_ids
from encoder.encode import Img2Vec
import time


def do_search(index_client, conn, cursor, img_to_vec, img_list):
    vectors_img = img_to_vec(img_list)

    status, ids_milvus = search_vectors(index_client, DEFAULT_TABLE, vectors_img)

    re_ids_img = []
    for ids in ids_milvus:
        vids = [x.id for x in ids]

        status, vector = get_vector_by_ids(index_client, DEFAULT_TABLE, vids)
        log.info(status, vector)
        re_ids = search_by_milvus_ids(conn, cursor, vids)
        re_ids_img.append(re_ids)
    return re_ids_img