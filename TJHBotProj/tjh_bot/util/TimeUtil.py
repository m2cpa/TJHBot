'''
Created on 2020/01/24

@author: m2(@m2cpa)
'''

import pytz
import datetime

TIME_FORMAT_YYMMDDHHMM = "%Y/%m/%d %H:%M"
TIME_FORMAT_YYMMDD = "%Y/%m/%d"

TIME_ZONE_JST_STR = 'Asia/Tokyo'
jst = pytz.timezone(TIME_ZONE_JST_STR)  # タイムゾーンを日本に指定する


################################################
# タイムスタンプを指定されたフォーマットで取得する
################################################
def __convert_date_str(date, format_str):
    ret = date.strftime(format_str)
    return ret


################################################
# 現時点のタイムスタンプを指定されたフォーマットで取得する
################################################
def get_now_str(format_str):
    now = datetime.datetime.now(jst)
    ret = __convert_date_str(now, format_str)
    return ret


################################################
# 翌日のタイムスタンプを指定されたフォーマットで取得する
################################################
def get_next_day_str(format_str):
    now = datetime.datetime.now(jst)
    next_day = now + datetime.timedelta(days=1)
    ret = __convert_date_str(next_day, format_str)
    return ret


################################################
# １週間後のタイムスタンプを指定されたフォーマットで取得する
################################################
def get_next_week_str(format_str):
    now = datetime.datetime.now(jst)
    next_week = now + datetime.timedelta(weeks=1)
    ret = __convert_date_str(next_week, format_str)
    return ret


################################################
# ６桁や７桁の日付を８桁の日付に変換する（フォーマットはYY/MM/DD）
################################################
def to_eight_date(date_str, delimiter="/"):
    ret = ""
    if date_str:
        date_str_list = []
        param = date_str.split(delimiter)
        if len(param) == 3:
            date_str_list.append(param[0].zfill(4))
            date_str_list.append(param[1].zfill(2))
            date_str_list.append(param[2].zfill(2))
            ret = delimiter.join(date_str_list)
    return ret
