import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, delete_vectors
from indexer.tools import connect_mysql, search_by_image_id, delete_data


def do_delete(ids_images):
    conn = connect_mysql()
    cursor = conn.cursor()
    index_client = milvus_client()

    try:
        ids_milvus = search_by_image_id(conn, cursor, ids_images)
        if not ids_milvus:
            return "The image id has not exists."
        ids_milvus = list(map(int, ids_milvus))
        print("ids_images:", ids_images, "----ids_milvus:", ids_milvus[0])
        status = delete_vectors(index_client, DEFAULT_TABLE, ids_milvus)
        print("delete_vectors:", status)
        if status:
            delete_data(conn, cursor, ids_images)
        return status
    except Exception as e:
        logging.error(e)
        return "Error with {}".format(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
        if index_client:
            index_client.disconnect()

