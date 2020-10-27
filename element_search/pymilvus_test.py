# -*- coding:utf-8 -*-
# @author :adolf
from milvus import Milvus, DataType

client = Milvus(host='localhost', port='9783')

collection_name = 'test01'

collection_param = {
    "fields": [
        {"name": "A", "type": DataType.INT32},
        {"name": "B", "type": DataType.INT32},
        {"name": "C", "type": DataType.INT64},
        {"name": "Vec", "type": DataType.FLOAT_VECTOR, "params": {"dim": 128}}
    ],
    "segment_row_limit": 4096,
    "auto_id": True
}
