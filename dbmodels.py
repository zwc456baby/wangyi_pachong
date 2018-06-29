import sqlite3

#------------------- 修改表名，修改表中数据条目 ---------------------------------
db_table_name = 'comment_info_db'
db_items = {'music_id':'TEXT','music_name':'TEXT','user':'TEXT','comment_id':'TEXT','comment':'TEXT','zan':'TEXT','http_url':'TEXT'}

#----------------------------------------------------


create_sqdb_cmd = 'create table '+db_table_name+' (id INT PRIMARY KEY'
for db_key_item in db_items:
	create_sqdb_cmd += ','
	create_sqdb_cmd += db_key_item
	create_sqdb_cmd += ' '
	create_sqdb_cmd += db_items[db_key_item]

create_sqdb_cmd += ')'


check_sqdb_exists = "SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name ='%s'"%(db_table_name,)
#将创建数据表的命令改成 for循环动态添加
#create_sqdb_cmd = 'create table '+db_table_name+' (id INT PRIMARY KEY,id_ TEXT,music_name TEXT,user TEXT,comment TEXT,zan TEXT)'

#print(create_sqdb_cmd)

insert_sqdb_cmd = "INSERT INTO "+db_table_name+' ('
index = 0
for db_key_item in db_items:
	if(index != 0):
		insert_sqdb_cmd += ','
	insert_sqdb_cmd += db_key_item
	index += 1
insert_sqdb_cmd += ') VALUES ('
for index_tmp in range(index):
	if(index_tmp != 0):
		insert_sqdb_cmd += ','
	insert_sqdb_cmd += "'%s'"
insert_sqdb_cmd += ')'

#print(insert_sqdb_cmd)
# 插入数据到表中,将插入数据的命令改成动态
#insert_sqdb_cmd = "INSERT INTO "+db_table_name+" (id_,music_name,user,comment,zan) VALUES ('%s','%s','%s','%s','%s')"

#查询表中所有数据
select_all_data = "SELECT * FROM "+db_table_name

def __get_connect_and_cursor():
	db_connect = sqlite3.connect(db_table_name)
	db_cursor = db_connect.cursor()
	__check_and_create_tab()
	return db_connect,db_cursor

def __close_db(db_connect,db_cursor):
	db_cursor.close()
	db_connect.close()

def __check_and_create_tab():
	db_connect = sqlite3.connect(db_table_name)
	db_cursor = db_connect.cursor()

	check_status = db_cursor.execute(check_sqdb_exists)
	tab_fetchall = check_status.fetchall()
	tab_len = len(tab_fetchall)

	if(tab_len == 0 or tab_fetchall[0][0] == 0):
		#print(tab_len)
		#print(tab_fetchall)
		#print(tab_fetchall[0][0])
		#print('创建表')
		db_cursor.execute(create_sqdb_cmd)
	else:
		pass

	db_connect.commit()
	__close_db(db_connect,db_cursor)


def save_item(comment,zan,music_id = 'None',comment_id = 'None',music = 'None',user = "None",http_url = ''):

	db_connect,db_cursor = __get_connect_and_cursor()
	try:
		insert_cmd = insert_sqdb_cmd % (music_id,music,user,comment_id,comment,zan,http_url)
		insert_statu = db_cursor.execute(insert_cmd)
		#print(insert_statu.fetchall())

		db_connect.commit()
	except Exception as e:
		pass
	finally:
		__close_db(db_connect,db_cursor)




def print_all_data():
	db_connect,db_cursor = __get_connect_and_cursor()
	try:
		#遍历查询获取数据
		select_status = db_cursor.execute(select_all_data)
		one_data = select_status.fetchone()
		index = 0
		while one_data != None:
			#print(one_data)
			index += 1
			one_data = select_status.fetchone()
		print('data length:'+str(index))
	except Exception as e:
		print('print db data error')
	finally:
		__close_db(db_connect,db_cursor)
