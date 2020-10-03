from MySQLdb import connect
from MySQLdb.cursors import DictCursor
from django.db import models

def fetchlist():
    conn = getconnection()
    cursor = conn.cursor(DictCursor)

    sql = '''
          select no,
                 name,
                 message,
                 date_format(reg_time, '%Y-%m-%d %p %h:%i:%s') as reg_date
            from guestbook
        order by no desc
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    # 자원 정리
    cursor.close()
    conn.close()

    return results


def insert(name, password, message):
    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
        insert
          into guestbook
        values (null, %s, %s, %s, now())
    '''
    cursor.execute(sql, (name, password, message))
    conn.commit()

    # 자원 정리
    cursor.close()
    conn.close()


def delete(no, password):
    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
        delete
          from guestbook
         where no=%s and password=password(%s)
    '''
    result = cursor.execute(sql, (no, password))
    conn.commit()

    # 자원 정리
    cursor.close()
    conn.close()

    return result

def getconnection():
    return connect(user="mysite", password="mysite", host="localhost", db="mysite", charset="utf8")