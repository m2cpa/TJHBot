'''
Created on 2020/01/25

@author: m2(@m2cpa)
'''
import os
import psycopg2
import psycopg2.extras

DB_URI = os.environ["DB_URI"]

SQL_SELECT_NOTICE = "SELECT id, notice FROM notice_table ORDER BY id ASC"
SQL_DELETE_NOTICE = "TRUNCATE notice_table"
SQL_INSERT_NOTICE = "INSERT INTO notice_table(id, notice) VALUES(%s, %s)"

COLUMN_NAME_NOTICE = "notice"


################################################
# notice_tableのデータを全件削除する
################################################
def __delete_all_notice_table(cur):
    cur.execute(SQL_DELETE_NOTICE)


################################################
# notice_tableにデータを追加する
################################################
def __insert_notice_table(cur, start_cnt, notices):
    if notices:
        for notice in notices:
            cur.execute(SQL_INSERT_NOTICE, (start_cnt, notice))
            start_cnt += 1


################################################
# DBとのコネクション取得する
################################################
def __get_connection():
    ret = psycopg2.connect(DB_URI, cursor_factory=psycopg2.extras.DictCursor)
    return ret


################################################
# notice_tableの内容を更新する
################################################
def update_notice_list(notices):
    with __get_connection() as connection:
        with connection.cursor() as cursor:
            __delete_all_notice_table(cursor)
            __insert_notice_table(cursor, 1, notices)
            connection.commit()


################################################
# notice_tableの指定したカラムを全件取得する
################################################
def select_all_notice_table(column_name):
    ret_list = []
    if column_name:
        with __get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL_SELECT_NOTICE)
                for row in cursor:
                    ret_list.append(row[column_name])
    return ret_list
