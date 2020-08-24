import logging as log
from common.config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB
import pymysql
from indexer.logs import write_log
import os


def connect_mysql():
    try:
        # conn = pymysql.connect(host="127.0.0.1",user="root",port=3306,password="123456",database="mysql", local_infile=True)
        conn = pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,port=MYSQL_PORT,password=MYSQL_PWD,database=MYSQL_DB, local_infile=True)
        return conn
    except Exception as e:
        print("MYSQL ERROR: connect failed", e)
        write_log(e,1)


def create_table_mysql(conn,cursor, table_name):
    sql = "create table if not exists " + table_name + "(milvus_id bigint, images_id varchar(256), index ix_milvus (milvus_id), index ix_images (images_id));"
    try:
        cursor.execute(sql)
        print("MYSQL create table.")
    except Exception as e:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)


def search_by_milvus_ids(conn, cursor, ids, table_name):
    str_ids = str(ids)
    str_ids = str(str_ids).replace('[','').replace(']','')
    sql = "select images_id from " + table_name + " where milvus_id in (" + str_ids + ") order by field (milvus_id," + str_ids + ");"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        results = [res[0] for res in results]
        print("MYSQL search by milvus id.")
        return results
    except Exception as e:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)


def search_by_image_id(conn, cursor, image_id, table_name):
    sql = "select milvus_id from " + table_name + " where images_id = '" + image_id + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print("MYSQL search by image id.")
        if len(results):
            results = [res[0] for res in results]
            return results
        else:
            return None
    except Exception as e:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)


def load_data_to_mysql(conn, cursor, table_name, file_name):
    sql = "load data local infile '" + file_name + "' into table " + table_name + " fields terminated by ',';"
    try:
        cursor.execute(sql)
        conn.commit()
        print("MYSQL load table.")
    except Exception as e:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)
    finally:
        if os.path.exists(file_name):
            with open(file_name) as f:
                line = f.readlines()
                print("-----------MySQL insert info--------len:" + str(len(line)) + "------" + str(line))
                write_log("-----------MySQL insert info--------len:" + str(len(line)) + "------" + str(line))
            os.remove(file_name)


def delete_data(conn, cursor, image_id, table_name):
    str_ids = [str(_id) for _id in image_id]
    str_ids = str(str_ids).replace('[','').replace(']','')
    sql = "delete from " + table_name + " where images_id in (" + str_ids + ");"
    try:
        cursor.execute(sql)
        conn.commit()
        print("MYSQL delete data.")
    except Exception as e:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)


def delete_table(conn, cursor, table_name):
    sql = "drop table if exists " + table_name + ";"
    try:
        cursor.execute(sql)
        print("MYSQL delete table.")
    except:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)


def delete_all_data(conn, cursor, table_name):
    sql = 'delete from ' + table_name + ';'
    try:
        cursor.execute(sql)
        conn.commit()
        print("MYSQL delete all data.")
    except:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)


def count_table(conn, cursor, table_name):
    sql = "select count(milvus_id) from " + table_name + ";"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print("MYSQL count table.")
        return results[0][0]
    except Exception as e:
        print("MYSQL ERROR:", sql, e)
        write_log(e,1)