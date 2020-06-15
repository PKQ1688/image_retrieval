import logging
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, search_vectors
from indexer.tools import connect_mysql, search_by_milvus_ids
from encoder.encode import img_to_vec
import time


def do_search(img):
    conn = connect_mysql()
    cursor = conn.cursor()
    index_client = milvus_client()

    try:
        time1 = time.time()
        vectors_img = img_to_vec(img)
        time2 = time.time()
        print("img_to_vec_time:", time2-time1)

        time1 = time.time()
        status, ids_milvus = search_vectors(index_client, DEFAULT_TABLE, [vectors_img])
        time2 = time.time()
        print("milvus_search_time:", time2-time1)

        print("search_milvus", status, len(ids_milvus))
        vids = [x.id for x in ids_milvus[0]]
        print("---------------vids:", len(vids))

        time1 = time.time()
        re_ids_img = search_by_milvus_ids(conn, cursor, vids)
        time2 = time.time()
        print("search_with_mysql_time:", time2-time1)
        print("search_mysql", len(re_ids_img))
        return re_ids_img
    except Exception as e:
        logging.error(e)
        return "Fail with error {}".format(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
        if index_client:
            index_client.disconnect()
