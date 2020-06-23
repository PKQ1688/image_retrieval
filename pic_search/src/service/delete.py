import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, delete_vectors
from indexer.tools import connect_mysql, search_by_image_id, delete_data


def do_delete(index_client, conn, cursor, ids_images):
    info = []
    ids_milvus_list = []
    for ids in ids_images:
        ids_milvus = search_by_image_id(conn, cursor, ids)
        if not ids_milvus:
            info.append(ids)
        else:
            ids_milvus_list.append(ids_milvus[0])

    ids_milvus = list(map(int, ids_milvus_list))
    # print("ids_images:", ids_images, "----ids_milvus:", ids_milvus)
    status = delete_vectors(index_client, DEFAULT_TABLE, ids_milvus)
    # print("delete_vectors:", status)
    if status:
        delete_data(conn, cursor, ids_images)

    return status, info

