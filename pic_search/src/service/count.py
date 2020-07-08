import logging
import time
from common.config import DEFAULT_TABLE
from indexer.index import milvus_client, count_table
import eventlet

eventlet.monkey_patch()

def do_count(table_name):
    if not table_name:
    	table_name = DEFAULT_TABLE
	
    with eventlet.Timeout(3,False):
	    print("doing count, table_name:", table_name)
	    index_client = milvus_client()
	    num = count_table(index_client, table_name)
	    return num
