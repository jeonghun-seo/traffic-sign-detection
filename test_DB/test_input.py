import pymysql
from datetime import datetime

now = datetime.now()

##create table sql code
# create table test
# (trf_id smallint unsigned not null auto_increment primary key,
# trf_type varchar(20) not null,
# trf_speed varchar(20) not null,
# now varchar(100) not null)

def insert(vo):
    # db connect
    con = pymysql.connect(host='localhost', user='root', password='1234',
                          db='testdb', charset='utf8')
    cur = con.cursor()  # sql문 대신 실행해주고 결과 반환해줄 커서 객체 생성

    # 일단 input 받기
    vo.trf_type = input('trf_type 값을 입력하세요: ')
    vo.trf_speed = input('trf_speed 값을 입력하세요: ')
    vo.now = datetime.now()

    # sql code
    sql = "INSERT INTO test (trf_type, trf_speed, now) VALUES (%s, %s, %s)"
    vals = (vo.trf_type, vo.trf_speed, vo.now)

    cur.execute(sql, vals)
    con.commit()
    con.close()


# 테스트용 vo 객체 생성
class Vo:
    def __init__(self):
        self.trf_type = ''
        self.trf_speed = ''
        self.now = None


vo = Vo()
insert(vo)
