import MySQLdb


class SqlUtils(object):
    def __init__(self):
        pass

    def get_conn(self):
        #获取MySQL连接
        try:
            conn = MySQLdb.connect(
                db="user_grade",
                host="127.0.0.1",
                user='root',
                password='',
                charset='utf8'
            )
        except:
            pass
        return conn

    def sql_test(self):
        conns = self.get_conn()
        print(conns)



if __name__ == '__main__':
    client = SqlUtils()
    client.sql_test()