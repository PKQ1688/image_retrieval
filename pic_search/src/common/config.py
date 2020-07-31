import os
from milvus import Milvus, IndexType, MetricType, Status

MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", 19530)
VECTOR_DIMENSION = os.getenv("VECTOR_DIMENSION", 512)
METRIC_TYPE = os.getenv("METRIC_TYPE", MetricType.IP)
TOP_K = os.getenv("TOP_K", 20)

DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "milvus_image")
# DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "milvus_image_1")

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PWD = os.getenv("MYSQL_PWD", "123456")
MYSQL_DB = os.getenv("MYSQL_DB", "mysql")
