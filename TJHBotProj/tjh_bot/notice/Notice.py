'''
Created on 2020/01/14

@author: m2(@m2cpa)
'''

from bs4 import BeautifulSoup
import os
import re
import requests
import tjh_bot.notice.NoticeModel
import tjh_bot.util.DBUtil as DBUtil

#URL_HTTP_JFAEL = "http://www.jfael.or.jp/ja/"
URL_HTTP_JFAEL = "https://jfael.or.jp/institution/"
URL_HTTP = "http"

NOTICE_REGEX_STR = "ja_info_all|ja_info_tokyo"  # 全国or東京の画像があるものを抜き出す
TAG_NAME_ARTICLE = "article"             # タグ名は大文字小文字を区別するので注意
TAG_NAME_DL = "dl"                       # タグ名は大文字小文字を区別するので注意
TAG_NAME_DT = "dt"                       # タグ名は大文字小文字を区別するので注意
TAG_NAME_DD = "dd"                       # タグ名は大文字小文字を区別するので注意
TAG_NAME_SPAN = "span"                   # タグ名は大文字小文字を区別するので注意
TAG_NAME_TD = "td"                       # タグ名は大文字小文字を区別するので注意
TAG_NAME_IMG = "img"                     # タグ名は大文字小文字を区別するので注意
TAG_NAME_A = "a"                         # タグ名は大文字小文字を区別するので注意
ATTRI_NAME_SRC = "src"                   # 属性名は大文字小文字を区別するので注意
ATTRI_NAME_HREF = "href"                 # 属性名は大文字小文字を区別するので注意
ATTRI_NAME_CLASS = "class"               # 属性名は大文字小文字を区別するので注意
ATTRI_VALUE_INFORMATION = "information"  # 属性値は大文字小文字を区別するので注意
ATTRI_VALUE_AREA = "area"                # 属性値は大文字小文字を区別するので注意
ATTRI_VALUE_GRADE = "grade"              # 属性値は大文字小文字を区別するので注意
ATTRI_VALUE_TAG = "tag"                  # 属性値は大文字小文字を区別するので注意

MESSAGE_MAX_LENGTH = 140


################################################
# 前回実行時の通知リストを読み込む
################################################
def __read_old_notice_list():
    return DBUtil.select_all_notice_table(DBUtil.COLUMN_NAME_NOTICE)


################################################
# 前回の通知リストの内容を今回の内容に更新する
################################################
def __update_old_notice_list(notices):
    DBUtil.update_notice_list(notices)


################################################
# 現在のJFAELのWebページを読み込む
################################################
def __read_new_html_data():
    return requests.get(URL_HTTP_JFAEL).text


################################################
# twitterに投稿するメッセージを作成する
################################################
def __create_tweet_message(notice):
    ret = ""

    # twitterの文字数制限に気を付けながら結合する
    # twitterの文字数制限に引っかかった場合、メインメッセージを左から文字数分取得する
    len_message = len(str(notice) + os.linesep + notice.url)
    if len_message <= MESSAGE_MAX_LENGTH:
        ret = str(notice)
    else:
        del_len = MESSAGE_MAX_LENGTH - len_message
        ret = str(notice)[:del_len]

    # urlを付加する
    # ただし絶対参照と相対参照が混ざっているので、絶対参照に統一した上で付加する
    if notice.url:
        url = notice.url
        if URL_HTTP not in url:
            url = URL_HTTP_JFAEL + url
        ret = ret + os.linesep + url
    return ret


################################################
# twitterに投稿するメッセージを作成する
################################################
def __create_tweet_message_old(td_tag, body):
    ret = ""

    # AタグからURLを取得する
    url = ""
    for item in td_tag.find_all(TAG_NAME_A):
        if item:
            url = item.get(ATTRI_NAME_HREF)

    # twitterの文字数制限に気を付けながら結合する
    # twitterの文字数制限に引っかかった場合、メインメッセージを左から文字数分取得する
    len_message = len(body + os.linesep + url)
    if len_message <= MESSAGE_MAX_LENGTH:
        ret = body
    else:
        del_len = MESSAGE_MAX_LENGTH - len_message
        ret = body[:del_len]

    # urlを付加する
    # ただし絶対参照と相対参照が混ざっているので、絶対参照に統一した上で付加する
    if url:
        if URL_HTTP not in url:
            url = URL_HTTP_JFAEL + url
        ret = ret + os.linesep + url
    return ret


################################################
# 通知情報モデルを作成する
################################################
def __create_notice(dl_tag):
    ret = None

    if dl_tag:
        ret = tjh_bot.notice.NoticeModel.NoticeModel()
        for dl_child in dl_tag.children:
            if dl_child.name == TAG_NAME_DT:
                # dtタグの扱い
                ret.notice_date = dl_child.get_text(strip=True)

            if dl_child.name == TAG_NAME_DD:
                # ddタグの扱い
                for dd_child in dl_child.children:
                    if dd_child.name == TAG_NAME_SPAN:
                        a_str = ""
                        cnt = 0
                        for span_child in dd_child.children:
                            child_name = span_child.name
                            if child_name == TAG_NAME_A:
                                if cnt != 0:
                                    a_str = a_str + ", "
                                a_str = a_str + span_child.get_text(strip=True)
                                cnt = cnt + 1

                        class_name = \
                          dd_child.get(ATTRI_NAME_CLASS)[0].split()[0]
                        if class_name == ATTRI_VALUE_AREA:
                            ret.area = a_str
                        elif class_name == ATTRI_VALUE_GRADE:
                            ret.grade = a_str
                        elif class_name == ATTRI_VALUE_TAG:
                            ret.notice_type = a_str

                    elif dd_child.name == TAG_NAME_A:
                        ret.title = dd_child.get_text(strip=True)
                        url = dd_child.get(ATTRI_NAME_HREF)
                        ret.url = url

    return ret


################################################
# 通知情報を抜き出したリストを作成する
################################################
def __create_notice_list(row_data):
    ret_list = []
    soup = BeautifulSoup(row_data, 'html.parser')

    # dlタグを持つ要素を抜き出す
    article_tags = soup.find_all(TAG_NAME_ARTICLE)

    # 解析パート
    # dlタグの子供としてdtタグとddタグがあり、dtタグが日付を、ddタグが詳細な内容を記載している
    # 「お知らせ」に該当する場合、必ずimgタグで全国or東京の画像が表示されている
    # →　tdタグの子供にimgタグがあった場合に取得フラグを立て、
    # →　取得フラグが立っているときのtdタグのbodyがお知らせの本文であると判断する
    for article_tag in article_tags:
        class_value = article_tag.get(ATTRI_NAME_CLASS)
        if class_value is not None and class_value[0] == ATTRI_VALUE_INFORMATION:
            for article_child in article_tag.children:
                if article_child.name == TAG_NAME_DL:
                    notice = __create_notice(article_child)

                    # tweet用のメッセージを作成する
                    tweet_message = __create_tweet_message(notice)
                    if tweet_message not in ret_list:
                        ret_list.append(tweet_message)

    return ret_list

################################################
# 通知情報を抜き出したリストを作成する（削除予定）
################################################
def __create_notice_list_old(row_data):
    ret_list = []
    soup = BeautifulSoup(row_data, 'html.parser')

    # tdタグを持つ要素を抜き出す
    td_tags = soup.find_all(TAG_NAME_TD)

    # 解析パート
    # 「お知らせ」に該当する場合、必ずimgタグで全国or東京の画像が表示されている
    # →　tdタグの子供にimgタグがあった場合に取得フラグを立て、
    # →　取得フラグが立っているときのtdタグのbodyがお知らせの本文であると判断する
    img_flag = ""
    for td_tag in td_tags:
        # tdタグのボディ部を取得し、お知らせかどうかを判断する
        body = td_tag.get_text(strip=True)
        if body and re.search(NOTICE_REGEX_STR, img_flag) is not None:
            # tweet用のメッセージを作成する
            tweet_message = __create_tweet_message(td_tag, body)
            if tweet_message not in ret_list:
                ret_list.append(tweet_message)
            img_flag = ""

        # 子供にimgタグがあり、かつ、全国or東京の画像だった場合にフラグを立てる
        for child in td_tag.children:
            if child.name == TAG_NAME_IMG:
                img_flag = child.get(ATTRI_NAME_SRC)

    return ret_list



################################################
# 前回との差分のリストを作成する
################################################
def __create_diff_list(new_notices, old_notices):
    ret_list = []
    for new_notice in new_notices:
        if new_notice not in old_notices:
            ret_list.append(new_notice)
    return ret_list


################################################
# 通知確認を実施する
################################################
def create_notice_list():
    # 前回の通知を取得する
    old_notices = __read_old_notice_list()

    # JFAELのサイトから通知を取得する
    new_html_data = __read_new_html_data()
    new_notices = __create_notice_list(new_html_data)

    # 両者を比較し差分を取得する
    ret_list = __create_diff_list(new_notices, old_notices)

    # 古い通知リストを新しい通知リストで更新する
    __update_old_notice_list(new_notices)

    return ret_list
