from pymysql import Connection

#连接mysql
conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='123456'
)
#测试信息
print(conn.get_server_info())

cursor = conn.cursor()
conn.select_db('choose')
cursor.execute("CREATE TABLE pymysql(name char(10),id int);")
#关闭连接
conn.close()