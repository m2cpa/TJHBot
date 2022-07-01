'''
Created on 2022/07/01

@author: m2(@m2cpa)
'''

import tjh_bot.util.TimeUtil as TimeUtil


class NoticeModel:
    '''
    classdocs
    '''

    # 日付
    @property
    def notice_date(self):
        return self.__notice_date

    @notice_date.setter
    def notice_date(self, notice_date):
        self.__notice_date = TimeUtil.to_eight_date(notice_date.strip())

    # 地区
    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, area):
        self.__area = area.strip()

    # 年次
    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, grade):
        self.__grade = grade.strip()

    # 記事種類
    @property
    def notice_type(self):
        return self.__notice_type

    @notice_type.setter
    def notice_type(self, notice_type):
        self.__notice_type = notice_type.strip()

    # 記事タイトル
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title.strip()

    # URL
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url.strip()

    ################################################
    # オブジェクト情報の表示を定義する
    ################################################
    def __repr__(self):
        '''
        titleが空ならば空を返す
        title以外が全て空でも空を返す
        それ以外の場合、★期間情報★\n【地区】【年次】【記事種類】タイトル の書式で返す
        '''
        ret = ""
        if self.__title:
            ret = ret + "★" + self.notice_date + "★\n"
            if self.__area:
                ret = ret + "【" + self.__area + "】"
            if self.__grade:
                ret = ret + "【" + self.__grade + "】"
            if self.__notice_type:
                ret = ret + "【" + self.__notice_type + "】"
            if ret:
                ret = ret + self.__title

        return ret

    ################################################
    # オブジェクト比較のロジックを定義する
    ################################################
    def __eq__(self, other):
        # otherの型が違う場合は NotImplemented を返却する
        if not isinstance(other, NoticeModel):
            return NotImplemented

        if(self.notice_date == other.notice_date
            and self.area == other.area
            and self.grade == other.grade
            and self.notice_type == other.notice_type
            and self.title == other.title
            and self.url == other.url):
            return True

        return False

    ################################################
    # コンストラクタ
    ################################################
    def __init__(self):
        self.__notice_date = ""
        self.__area = ""
        self.__grade = ""
        self.__notice_type = ""
        self.__title = ""
        self.__url = ""
