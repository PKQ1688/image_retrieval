import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, count_collection
from indexer.tools import count_table
from indexer.logs import write_log

def do_count(index_client, conn, cursor, table_name):
    if not table_name:
        table_name = DEFAULT_TABLE

    write_log("doing count, table_name:" + table_name)
    print("doing count, table_name:", table_name)
    num_milvus = count_collection(index_client, table_name)
    num_mysql = count_table(conn, cursor, table_name)
    return num_milvus, num_mysql
