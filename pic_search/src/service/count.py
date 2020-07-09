import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, count_table
from indexer.logs import write_log

def do_count(table_name):
    if not table_name:
        table_name = DEFAULT_TABLE

    write_log("doing count, table_name:" + table_name)
    print("doing count, table_name:", table_name)
    index_client = milvus_client()
    num = count_table(index_client, table_name)
    return num
