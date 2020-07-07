import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, count_table


def do_count(table_name=DEFAULT_TABLE):
    index_client = milvus_client()
    num = count_table(index_client, table_name)
    return num