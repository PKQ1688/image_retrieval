import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, count_table


def do_count():
    index_client = milvus_client()
    num = count_table(index_client, DEFAULT_TABLE)
    return num