import logging as log
from common.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB, FILE_NAME
import pymysql


def connect_mysql():
    try:
        # conn = pymysql.connect(host="127.0.0.1",user="root",port=3306,password="123456",database="mysql", local_infile=True)
        conn = pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,port=MYSQL_PORT,password=MYSQL_PWD,database=MYSQL_DB, local_infile=True)
        return conn
    except Exception as e:
        log.error(e)


def create_table_mysql(conn,cursor, table_name):
    sql = "create table if not exists " + table_name + "(milvus_id bigint, images_id varchar(30), index ix_milvus (milvus_id), index ix_images (images_id));"
    try:
        cursor.execute(sql)
        print("create table")
    except Exception as e:
        log.error(e)


def search_by_milvus_ids(conn, cursor, ids, table_name):
    str_ids = str(ids)
    str_ids = str(str_ids).replace('[','').replace(']','')
    sql = "select images_id from " + table_name + " where milvus_id in (" + str_ids + ") order by field (milvus_id," + str_ids + ");"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        results = [res[0] for res in results]
        return results
    except Exception as e:
        log.error(e)


def search_by_image_id(conn, cursor, image_id, table_name):
    sql = "select milvus_id from " + table_name + " where images_id = '" + image_id + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results):
            results = [res[0] for res in results]
            return results
        else:
            return None
    except Exception as e:
        log.error(e)



def load_data_to_mysql(conn, cursor, table_name):
    sql = "load data local infile '" + FILE_NAME + "' into table " + table_name + " fields terminated by ',';"
    cursor.execute(sql)
    conn.commit()



def delete_data(conn, cursor, image_id, table_name):
    str_ids = [str(_id) for _id in image_id]
    str_ids = str(str_ids).replace('[','').replace(']','')
    sql = "delete from " + table_name + " where images_id in (" + str_ids + ");"
    cursor.execute(sql)
    conn.commit()