from django.db import models
from MySQLdb import connect
from MySQLdb.cursors import DictCursor

# Create your models here.
def get_max_group_no():
    conn = getconnection()
    cursor = conn.cursor(DictCursor)
    sql = '''
        select max(g_no) as max from board
    '''
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result



def insert(title, content, max_group_no, user_no):
    if max_group_no is None:
        max_group_no = 0

    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
        insert
          into board
        values (null, %s, %s, %s, now(), %s, %s, %s, %s)
    '''
    cursor.execute(sql, (title, content, 0, max_group_no + 1, 1, 0, user_no))
    conn.commit()

    cursor.close()
    conn.close()

def fetchlist(limit, page=1):
    conn = getconnection()
    cursor = conn.cursor(DictCursor)

    if page is None:
        page = 1

    sql = '''
        SELECT
            A.no,
            A.title,
            A.hit,
            date_format(A.reg_date, "%%Y-%%m-%%d %%H:%%i:%%s") as reg_date,
            A.user_no,
            u.name as user_name,
            A.page,
            A.topcnt
        FROM (
            SELECT
                board.*,
                row_number() over () as row_no,
                ceil(row_number() over () / %s) as page,
                COUNT(*) OVER() AS topcnt
            FROM board
        ) A
        INNER JOIN user u ON u.no = A.user_no
        WHERE A.page = %s
        ORDER BY A.no DESC
    '''
    cursor.execute(sql, [limit, page])
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def fetchlist2():
    conn = getconnection()
    cursor = conn.cursor(DictCursor)

    sql = '''
        SET @rownum:=0;
          select b.no,
                 b.title,
                 b.hit,
                 date_format(b.reg_date, '%Y-%m-%d %H:%i:%s') as reg_date,
                 b.user_no,
                 u.name as user_name,
                 @rownum:=@rownum+1 as row_no
            from board b
            inner join user u on u.no = b.user_no
            order by no desc
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def fetchonebyno(no):
    conn = getconnection()
    cursor = conn.cursor(DictCursor)

    cursor.execute('select * from board where no = %s', [no])
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def delete(no):
    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
        delete
          from board
         where no=%s
    '''
    result = cursor.execute(sql, [no])
    conn.commit()

    # 자원 정리
    cursor.close()
    conn.close()

    return result

def hit(no):
    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
        update board
            set hit = hit + 1
        where no = %s
    '''
    cursor.execute(sql, [str(no)])
    conn.commit()

    cursor.close()
    conn.close()


def update(board_no, title, content):
    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
        update board
            set title=%s, content=%s
        where no=%s
    '''
    cursor.execute(sql, (title, content, str(board_no)))
    conn.commit()

    cursor.close()
    conn.close()

def getconnection():
    return connect(user="mysite", password="mysite", host="localhost", db="mysite", charset="utf8")