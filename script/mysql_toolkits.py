import pymysql


TABLE_NAME = 'images'


def conect_mysql():
	try:
		conn = pymysql.connect(host="127.0.0.1",user="root",port=3306,password="123456",database="mysql", local_infile=True)
		return conn
	except:
		return "connect mysql faild"


def create_table(conn,cursor):
	sql = "create table if not exists " + TABLE_NAME + "(milvus_id int, images_id varchar(30), index ix_milvus (milvus_id), index ix_images (images_id));"
	try:
		cursor.execute(sql)
		print("create table")
	except:
		conn.rollback()
		print("create table faild")


#将图片id和其对应的milvus_id批量存入mysql中
def load_data_to_mysql(conn, cursor, fname):
	sql = "load data local infile '" + fname + "' into table " + TABLE_NAME + " fields terminated by ',';"
	try:
		cursor.execute(sql)
		conn.commit()
	except:
		conn.rollback()
		print("load data faild")


#对image_id创建索引
# def build_index(conn, cursor):
# 	sql = "create index "




#通过图片对应的id删除库中的数据
def delete_data(conn, cursor, image_id):
	sql = "delete from " + TABLE_NAME + " where images_id = '" + image_id + "';"
	try:
		cursor.execute(sql)
		conn.commit()
	except:
		conn.rollback()
		print("delete data faild")


#通过milvus返回的id查找对应的图片
def search_by_milvus_ids(conn, cursor, ids):
	str_ids = [str(_id) for _id in ids]
	str_ids = ",".join(str_ids)
	sql = "select images_id from " + TABLE_NAME + " where milvus_id in (" + str_ids + ") order by field (milvus_id," + str_ids + ");"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		return results
	except:
		conn.rollback()
		print("search faild")


#判断库中是否已经存在该图片的id
def search_by_image_id(conn, cursor, image_id):
	sql = "select images_id from " + TABLE_NAME + " where images_id = '" + image_id + "';"
	try:
		cursor.execute(sql)
		results = cursor.fetchall()
		if len(results):
			return True
		else:
			return False
	except:
		conn.rollback()
		print("judge faild")



# def main():
	# conn = conect_mysql()
	# cursor = conn.cursor()
	# ids = [2474546,3454556,1454556]
	# results = search_images(conn, cursor, ids)
	# print(results)
	# fname = 'test.csv'
	# load_data_to_mysql(conn, cursor, fname)
	# image_id = 'a3nr4t4g'
	# delete_data(conn, cursor, image_id)
	# create_table(conn,cursor)



# main()



# 关闭数据库连接
# conn.close()