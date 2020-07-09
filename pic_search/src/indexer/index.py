import logging as log
from milvus import Milvus, IndexType, MetricType, Status
from common.config import MILVUS_HOST, MILVUS_PORT, VECTOR_DIMENSION, METRIC_TYPE, TOP_K
from indexer.logs import write_log


def milvus_client():
    try:
        milvus = Milvus()
        milvus.connect(host=MILVUS_HOST, port=MILVUS_PORT)
        return milvus
    except Exception as e:
        write_log(e)


def create_table(client, table_name=None, dimension=VECTOR_DIMENSION,
                 index_file_size=512, metric_type=METRIC_TYPE):
    table_param = {
        'collection_name': table_name,
        'dimension': dimension,
        'index_file_size':index_file_size,
        'metric_type': metric_type
    }
    try:
        status = client.create_collection(table_param)
        return status
    except Exception as e:
        write_log(e)


def insert_vectors(client, table_name, vectors):
    try:
        status, ids = client.insert(collection_name=table_name, records=vectors)
        return status, ids
    except Exception as e:
        write_log(e)


def create_index(client, table_name):
    param = {'nlist': 16384}
    try:
        status = client.create_index(table_name, IndexType.IVF_FLAT, param)
        return status
    except Exception as e:
        write_log(e)


def delete_table(client, table_name):
    try:
        status = client.drop_collection(collection_name=table_name)
        return status
    except Exception as e:
        write_log(e)


def search_vectors(client, table_name, vectors, top_k=TOP_K):
    try:
        search_param = {'nprobe': 16}
        print("_______topk:", top_k)
        status, res = client.search(collection_name=table_name, query_records=vectors, top_k=top_k, params=search_param)
        return status, res
    except Exception as e:
        write_log(e)


def has_table(client, table_name):
    try:
        status = client.has_collection(collection_name=table_name)
        return status
    except Exception as e:
        write_log(e)


def count_table(client, table_name):
    try:
        status, num = client.count_collection(collection_name=table_name)
        return num
    except Exception as e:
        write_log(e)


def delete_vectors(client, table_name, ids):
    try:
        status = client.delete_by_id(table_name, ids)
        return status
    except Exception as e:
        write_log(e)


def get_vector_by_ids(client, table_name, ids):
    try:
        status, vector = client.get_vector_by_id(collection_name=table_name, vector_id=ids)
        return status, vector
    except Exception as e:
        write_log(e)