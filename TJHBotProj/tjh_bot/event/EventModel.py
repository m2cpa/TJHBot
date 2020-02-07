'''
Created on 2020/01/24

@author: m2(@m2cpa)
'''
import tjh_bot.util.TimeUtil as TimeUtil

TYPE_NAME_ELEARNING = "Eラン"
TYPE_NAME_EXAM = "考査"
TYPE_NAME_DISCUSS = "ディスカッション"
TYPE_NAME_SEMINAR = "ゼミナール"
TYPE_NAME_REPORT = "課題研究"
TYPE_NAME_LECTURE = "講義"
TYPE_NAME_APPLICATION = "申込"

ALERT_TODAY = "■■■■■■■■■　納期／本番当日です！　■■■■■■■■■"
ALERT_PREVIOUS_DAY = "■■■■■■　納期／本番前日です！　■■■■■■"
ALERT_PREVIOUS_WEEK = "■■■　納期／本番１週間前です！　■■■"


class EventModel:
    '''
    classdocs
    '''
    # イベント種類
    @property
    def type(self):
        return self.__type

    # 地区
    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, area):
        self.__area = area.strip()

        # 地区を利用してイベントタイプを決定する（Eラン、申込）
        if self.__area == TYPE_NAME_ELEARNING:
            self.__type = TYPE_NAME_ELEARNING

        if self.__area == TYPE_NAME_APPLICATION:
            self.__type = TYPE_NAME_APPLICATION

    # 年次
    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, grade):
        self.__grade = grade.strip()

    # 開始日付
    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date):
        self.__start_date = TimeUtil.to_eight_date(start_date.strip())

    # 開始時刻
    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time.strip()

    # 終了日付
    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date):
        self.__end_date = TimeUtil.to_eight_date(end_date.strip())

    # 終了時刻
    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time.strip()

    # クラス
    @property
    def classname(self):
        return self.__classname

    @classname.setter
    def classname(self, classname):
        self.__classname = classname.strip()

    # 班
    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group):
        self.__group = group.replace("班", "").strip()

    # 科目名
    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject.strip()

        # 科目名を利用してイベントタイプを決定する（Eラン以外）
        if not self.__type:
            if TYPE_NAME_DISCUSS in subject:
                self.__type = TYPE_NAME_DISCUSS
            elif TYPE_NAME_EXAM in subject:
                self.__type = TYPE_NAME_EXAM
            elif TYPE_NAME_REPORT in subject:
                self.__type = TYPE_NAME_REPORT
            elif TYPE_NAME_SEMINAR in subject:
                self.__type = TYPE_NAME_SEMINAR
            else:
                self.__type = TYPE_NAME_LECTURE

    # 当日フラグ
    @property
    def today_flag(self):
        return self.__today_flag

    @today_flag.setter
    def today_flag(self, today_flag):
        self.__today_flag = today_flag

    # 前日フラグ
    @property
    def previous_day_flag(self):
        return self.__previous_day_flag

    @previous_day_flag.setter
    def previous_day_flag(self, previous_day_flag):
        self.__previous_day_flag = previous_day_flag

    # １週間前フラグ
    @property
    def previous_week_flag(self):
        return self.__previous_day_flag

    @previous_week_flag.setter
    def previous_week_flag(self, previous_week_flag):
        self.__previous_week_flag = previous_week_flag

    ################################################
    # 期間情報を作成する
    ################################################
    def __create_period_str(self):
        # 納期が迫っている場合に表示する
        # 納期フラグは、Eラン、研究課題、考査、申込について設定される
        previous_message = ""
        if self.__today_flag:
            previous_message = ALERT_TODAY + "\n"
        elif self.__previous_day_flag:
            previous_message = ALERT_PREVIOUS_DAY + "\n"
        elif self.__previous_week_flag:
            previous_message = ALERT_PREVIOUS_WEEK + "\n"

        period = ""
        if self.__start_date:
            period = period + self.__start_date
            if self.__start_time:
                period = period + " " + self.__start_time
        if self.__end_date:
            if self.__start_date != self.__end_date:
                period = period + " ～"
                period = period + " " + self.__end_date
        if self.__end_time:
            if self.__start_date == self.__end_date:
                period = period + " ～"
            period = period + " " + self.__end_time

        else:
            period = period

        ret = ""
        if period:
            ret = previous_message + "★" + period + "★\n"
        return ret

    ################################################
    # オブジェクト情報の表示を定義する
    ################################################
    def __repr__(self):
        '''
        subjectが空ならば空を返す
        subject以外が全て空でも空を返す
        それ以外の場合、★期間情報★\n【地区】【年次】【クラス】【班】科目名 の書式で返す
        '''
        ret = ""
        if self.__subject:
            ret = ret + self.__create_period_str()
            if self.__area:
                ret = ret + "【" + self.__area + "】"
            if self.__grade:
                ret = ret + "【" + self.__grade + "】"
            if self.__classname:
                ret = ret + "【" + self.__classname + "】"
            if self.__group:
                ret = ret + "【" + self.__group + "班】"
            if ret:
                ret = ret + self.__subject

        return ret

    ################################################
    # オブジェクト比較のロジックを定義する
    ################################################
    def __eq__(self, other):
        '''
        オブジェクト比較は班以外の要素が全て等しいかどうかで判定する
        →班が異なり、他の要素が同じオブジェクトはマージするため
        '''
        # otherの型が違う場合は NotImplemented を返却する
        if not isinstance(other, EventModel):
            return NotImplemented

        if(self.type == other.type
            and self.area == other.area
            and self.grade == other.grade
            and self.start_date == other.start_date
            and self.start_time == other.start_time
            and self.end_date == other.end_date
            and self.end_time == other.end_time
            and self.classname == other.classname
            and self.subject == other.subject):
            return True

        return False

    ################################################
    # コンストラクタ
    ################################################
    def __init__(self):
        self.__type = ""
        self.__area = ""
        self.__grade = ""
        self.__start_date = ""
        self.__start_time = ""
        self.__end_date = ""
        self.__end_time = ""
        self.__classname = ""
        self.__group = ""
        self.__subject = ""
        self.__today_flag = False
        self.__previous_day_flag = False
        self.__previous_week_flag = False
