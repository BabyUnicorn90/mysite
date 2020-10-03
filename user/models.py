from MySQLdb import connect
from MySQLdb.cursors import DictCursor
from django.db import models

def insert(name, email, password, gender):
    conn = getconnection()
    cursor = conn.cursor()

    sql = '''
            insert
                into user
                values (null, %s, %s,  password(%s), %s, now())
    '''

    cursor.execute(sql, (name, email, password, gender))
    conn.commit()

    cursor.close()
    conn.close()


def get_one_user(email, password):
    conn = getconnection()
    cursor = conn.cursor(DictCursor)

    sql = '''
        select no, name
            from user
        where email=%s
            and password=password(%s)
    '''
    cursor.execute(sql, (email, password))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def fetchonebyno(no):
    conn = getconnection()
    cursor = conn.cursor(DictCursor)

    cursor.execute('select * from user where no=%s', str(no))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

    # sql = '''
    #
    #         update user
    #             set name='%s', gender = '%s'
    #         where no=;
    #
    #         update user
    #             set name='%s', password=password('%s'), gender = '%s'
    #         where no=;
    # '''
    # cursor.execute(sql, (email, password))
    # result = cursor.fetchone()
    #
    # cursor.close()
    # conn.close()
    #
    # return result

no = 1



def update(no, name, password, gender):
    conn = getconnection()
    cursor = conn.cursor()

    if password is None:
        sql = '''
            update user
                set name=%s, gender = %s
            where no=%s
        '''
        cursor.execute(sql, (name, gender, str(no)))
        conn.commit()
    else:
        sql = '''
            update user
                set name=%s, password=password(%s), gender = %s
            where no=%s
        '''
        cursor.execute(sql, (name, password, gender, str(no)))
        conn.commit()

    cursor.close()
    conn.close()


def getconnection():
    return connect(user='mysite', password='mysite', host='localhost', port=3306, db='mysite', charset='utf8')