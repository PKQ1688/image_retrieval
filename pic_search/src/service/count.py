import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, count_table


def do_count():
    try:
        index_client = milvus_client()
        num = count_table(index_client, DEFAULT_TABLE)
        print(num)
        return num
    except Exception as e:
        logging.error(e)
        return "Error with {}".format(e)
    finally:
        if index_client:
            index_client.disconnect()
