'''
Created on 2020/01/24

@author: m2(@m2cpa)
'''
import sys
import tjh_bot.event.Event as Event
import tjh_bot.event.EventModel as EventModel
import tjh_bot.util.TweetUtil as TweetUtil
import tjh_bot.util.TimeUtil as TimeUtil


DIC_KEY_EVENTS = "events"
DIC_KEY_EXIST_MESSAGE = "exist"
DIC_KEY_NOT_EXIST_MESSAGE = "notexist"

MESSAGE_BASE_EXIST_EVENT = \
    "【{0[title]}】\n" + \
    "　{0[date_jpn]}（{0[date]}）はイベントが{0[count]}件あります。\n" + \
    "　詳細は実務補習所Webサイトをご確認下さい。"

MESSAGE_BASE_NOT_EXIST_EVENT = \
    "【{0[title]}】\n" + \
    "　{0[date_jpn]}（{0[date]}）はイベントはありません。"

MESSAGE_BASE_EXIST_END_EVENT = \
    "【{0[title]}】\n" + \
    "　{0[date_jpn]}（{0[date]}）納期／本番を迎えるイベントが{0[count]}件あります。\n" + \
    "　詳細は実務補習所Webサイトをご確認下さい。"

# パラメータ定義
ARGS_START_EVENT_TODAY = "--start_today"
ARGS_START_EVENT_NEXT_DAY = "--start_nextday"
ARGS_END_EVENT_TODAY = "--end_today"
ARGS_END_EVENT_NEXT_DAY = "--end_nextday"
ARGS_END_EVENT_NEXT_WEEK = "--end_nextweek"

# 開始日時で通知するイベントの定義
TYPE_LIST_START_EVENT = [
    EventModel.TYPE_NAME_DISCUSS,
    EventModel.TYPE_NAME_LECTURE,
    EventModel.TYPE_NAME_SEMINAR,
    EventModel.TYPE_NAME_ELEARNING,
    EventModel.TYPE_NAME_APPLICATION]

# 終了日時で通知するイベントの定義
TYPE_LIST_END_EVENT = [
    EventModel.TYPE_NAME_ELEARNING,
    EventModel.TYPE_NAME_APPLICATION,
    EventModel.TYPE_NAME_REPORT,
    EventModel.TYPE_NAME_EXAM]


################################################
# １週間後が終了日付のイベントをリマインド情報して取得する
################################################
def __create_remind_dic_end_next_week():
    events = Event.create_next_week_end_event_list(TYPE_LIST_END_EVENT)
    format_dic = {
        "title": "１週間後納期／本番のイベント",
        "date_jpn": "１週間後",
        "date": TimeUtil.get_next_week_str(TimeUtil.TIME_FORMAT_YYMMDD),
        "count": len(events)}

    ret_dic = {
        DIC_KEY_EVENTS: events,
        DIC_KEY_EXIST_MESSAGE:
            MESSAGE_BASE_EXIST_END_EVENT.format(format_dic),
        DIC_KEY_NOT_EXIST_MESSAGE: ""}

    return ret_dic


################################################
# 明日が終了日付のイベントをリマインド情報して取得する
################################################
def __create_remind_dic_end_next_day():
    events = Event.create_next_day_end_event_list(TYPE_LIST_END_EVENT)
    format_dic = {
        "title": "明日納期／本番のイベント",
        "date_jpn": "明日",
        "date": TimeUtil.get_next_day_str(TimeUtil.TIME_FORMAT_YYMMDD),
        "count": len(events)}

    ret_dic = {
        DIC_KEY_EVENTS: events,
        DIC_KEY_EXIST_MESSAGE:
            MESSAGE_BASE_EXIST_END_EVENT.format(format_dic),
        DIC_KEY_NOT_EXIST_MESSAGE: ""}

    return ret_dic


################################################
# 今日が終了日付のイベントをリマインド情報して取得する
################################################
def __create_remind_dic_end_today():
    events = Event.create_today_end_event_list(TYPE_LIST_END_EVENT)
    format_dic = {
        "title": "今日納期／本番のイベント",
        "date_jpn": "今日",
        "date": TimeUtil.get_now_str(TimeUtil.TIME_FORMAT_YYMMDD),
        "count": len(events)}

    ret_dic = {
        DIC_KEY_EVENTS: events,
        DIC_KEY_EXIST_MESSAGE:
            MESSAGE_BASE_EXIST_END_EVENT.format(format_dic),
        DIC_KEY_NOT_EXIST_MESSAGE: ""}

    return ret_dic


################################################
# 明日が開始日付のイベントをリマインド情報して取得する
################################################
def __create_remind_dic_start_next_day():
    events = Event.create_next_day_start_event_list(TYPE_LIST_START_EVENT)
    format_dic = {
        "title": "明日のイベント",
        "date_jpn": "明日",
        "date": TimeUtil.get_next_day_str(TimeUtil.TIME_FORMAT_YYMMDD),
        "count": len(events)}

    ret_dic = {
        DIC_KEY_EVENTS: events,
        DIC_KEY_EXIST_MESSAGE:
            MESSAGE_BASE_EXIST_EVENT.format(format_dic),
        DIC_KEY_NOT_EXIST_MESSAGE:
            MESSAGE_BASE_NOT_EXIST_EVENT.format(format_dic)}

    return ret_dic


################################################
# 今日が開始日付のイベントをリマインド情報として取得する
################################################
def __create_remind_dic_start_today():
    events = Event.create_today_start_event_list(TYPE_LIST_START_EVENT)
    format_dic = {
        "title": "本日のイベント",
        "date_jpn": "本日",
        "date": TimeUtil.get_now_str(TimeUtil.TIME_FORMAT_YYMMDD),
        "count": len(events)}

    ret_dic = {
        DIC_KEY_EVENTS: events,
        DIC_KEY_EXIST_MESSAGE:
            MESSAGE_BASE_EXIST_EVENT.format(format_dic),
        DIC_KEY_NOT_EXIST_MESSAGE:
            MESSAGE_BASE_NOT_EXIST_EVENT.format(format_dic)}

    return ret_dic


################################################
# リマインド情報を取得する
################################################
def __create_show_data(param):
    remind_dic = {}

    # 今日が開始日付のイベントをリマインド情報として取得する
    if param == ARGS_START_EVENT_TODAY:
        remind_dic = __create_remind_dic_start_today()

    # 明日が開始日付のイベントをリマインド情報して取得する
    elif param == ARGS_START_EVENT_NEXT_DAY:
        remind_dic = __create_remind_dic_start_next_day()

    # 今日が終了日付のイベントをリマインド情報して取得する
    elif param == ARGS_END_EVENT_TODAY:
        remind_dic = __create_remind_dic_end_today()

    # 明日が終了日付のイベントをリマインド情報して取得する
    elif param == ARGS_END_EVENT_NEXT_DAY:
        remind_dic = __create_remind_dic_end_next_day()

    # １週間後が終了日付のイベントをリマインド情報して取得する
    elif param == ARGS_END_EVENT_NEXT_WEEK:
        remind_dic = __create_remind_dic_end_next_week()

    return remind_dic


################################################
# リマインド情報をイートする
################################################
if __name__ == '__main__':
    if len(sys.argv) == 2:
        remind_dic = __create_show_data(sys.argv[1])
        if remind_dic:
            # ツイートする
            TweetUtil.tweet(
                remind_dic[DIC_KEY_EVENTS],
                remind_dic[DIC_KEY_EXIST_MESSAGE],
                remind_dic[DIC_KEY_NOT_EXIST_MESSAGE])
