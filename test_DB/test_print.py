import pymysql
#db connect
con = pymysql.connect(host = 'localhost', user = 'root', password = '1234',
                      db = 'testdb', charset = 'utf8')
cur = con.cursor() #sql문 대신 실행해주고 결과 반환해줄 커서 객체 생성

#sql code
sql = 'select * from test'
cur.execute(sql)

#print
for row in cur:
    print(row[0], row[1], row[2], row[3])