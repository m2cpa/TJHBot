'''
Created on 2020/01/24

@author: m2(@m2cpa)
'''
import os
import csv
import tjh_bot.event.EventModel
import tjh_bot.util.TimeUtil as TimeUtil

CSV_COLUMN_AREA = 0
CSV_COLUMN_GRADE = 1
CSV_COLUMN_START_DATE = 2
CSV_COLUMN_START_TIME = 4
CSV_COLUMN_END_DATE = 5
CSV_COLUMN_END_TIME = 7
CSV_COLUMN_CLASSNAME = 8
CSV_COLUMN_GROUP = 9
CSV_COLUMN_SUBJECT = 12

SHCEDULE_FILE_PATH = os.path.dirname(__file__) + "/../../data/schedule.csv"


################################################
# イベントモデルを作成する
################################################
def __create_event(params):
    ret = None
    if params:
        ret = tjh_bot.event.EventModel.EventModel()
        ret.area = params[CSV_COLUMN_AREA]
        ret.grade = params[CSV_COLUMN_GRADE]
        ret.start_date = params[CSV_COLUMN_START_DATE]
        ret.start_time = params[CSV_COLUMN_START_TIME]
        ret.end_date = params[CSV_COLUMN_END_DATE]
        ret.end_time = params[CSV_COLUMN_END_TIME]
        ret.classname = params[CSV_COLUMN_CLASSNAME]
        ret.group = params[CSV_COLUMN_GROUP]
        ret.subject = params[CSV_COLUMN_SUBJECT]

    return ret


################################################
# 全てのイベントを取得する
################################################
def __create_all_event_list():
    ret_list = []
    with open(SHCEDULE_FILE_PATH, encoding="UTF-8") as f:
        reader = csv.reader(f)
        for row in reader:
            event = __create_event(row)
            ret_list.append(event)

    return ret_list


################################################
# イベントオブジェクトを返却用リストに追加する
################################################
def __append_event_list(ret_list, event):
    if event not in ret_list:
        ret_list.append(event)
    else:
        index = ret_list.index(event)
        ret = ret_list[index]
        if ret.group:
            ret.group = ret.group + "・"
        ret.group = ret.group + event.group


################################################
# 終了日を指定してイベントを取得する
################################################
def __search_end_event_list(end_date, type_list):
    ret_list = []
    events = __create_all_event_list()
    for event in events:
        if event.end_date == end_date and event.type in type_list:
            __append_event_list(ret_list, event)

    return ret_list


################################################
# 開始日を指定してイベントを取得する
################################################
def __search_start_event_list(start_date, type_list):
    ret_list = []
    events = __create_all_event_list()
    for event in events:
        if event.start_date == start_date and event.type in type_list:
            __append_event_list(ret_list, event)

    return ret_list


################################################
# 今日開始のイベントを取得する
################################################
def create_today_start_event_list(type_list):
    today_str = TimeUtil.get_now_str(TimeUtil.TIME_FORMAT_YYMMDD)
    return __search_start_event_list(today_str, type_list)


################################################
# 翌日開始のイベントを取得する
################################################
def create_next_day_start_event_list(type_list):
    next_day_str = TimeUtil.get_next_day_str(TimeUtil.TIME_FORMAT_YYMMDD)
    return __search_start_event_list(next_day_str, type_list)


################################################
# 翌日終了のイベントを取得する
################################################
def create_next_day_end_event_list(type_list):
    next_day_str = TimeUtil.get_next_day_str(TimeUtil.TIME_FORMAT_YYMMDD)
    ret_list = __search_end_event_list(next_day_str, type_list)
    for event in ret_list:
        event.previous_day_flag = True
    return ret_list


################################################
# １週間後に終了のイベントを取得する
################################################
def create_next_week_end_event_list(type_list):
    next_week_str = TimeUtil.get_next_week_str(TimeUtil.TIME_FORMAT_YYMMDD)
    ret_list = __search_end_event_list(next_week_str, type_list)
    for event in ret_list:
        event.previous_week_flag = True
    return ret_list
