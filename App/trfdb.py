import pymysql
from datetime import datetime

now = datetime.now()

##create table sql code
# create table test
# (trf_id smallint unsigned not null auto_increment primary key,
# trf_limit varchar(20) not null,
# trf_accuracy varchar(20) not null,
# now varchar(100) not null)

def insertdb(split_labels):
    # db connect
    con = pymysql.connect(host='localhost', user='root', password='root',
                          db='trfdb', charset='utf8')
    cur = con.cursor()  # sql문 대신 실행해주고 결과 반환해줄 커서 객체 생성

    # sql code
    sql = "INSERT INTO trftable (trf_limit, trf_accuracy, now) VALUES (%s, %s, %s)"
    vals = (split_labels[0], split_labels[1], now)

    cur.execute(sql, vals)
    con.commit()
    con.close()
