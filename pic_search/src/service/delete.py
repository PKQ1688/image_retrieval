import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, delete_vectors
from indexer.tools import connect_mysql, search_by_image_id, delete_data
import time


def do_delete(index_client, conn, cursor, ids_images, table_name):
    info = []
    ids_milvus_list = []
    if not table_name:
        table_name = DEFAULT_TABLE
    for ids in ids_images:
        ids_milvus = search_by_image_id(conn, cursor, ids, table_name)
        if not ids_milvus:
            info.append(ids)
            print("the ids dose not exists:", ids)
        else:
            ids_milvus_list.append(ids_milvus[0])

    ids_milvus = list(map(int, ids_milvus_list))
    print("doing delete, table_name:", table_name)
    status = delete_vectors(index_client, table_name, ids_milvus)

    if status:
        delete_data(conn, cursor, ids_images, table_name)

    return status, info

