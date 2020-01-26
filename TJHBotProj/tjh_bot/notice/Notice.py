'''
Created on 2020/01/14

@author: m2(@m2cpa)
'''

from bs4 import BeautifulSoup
import re
import requests
import tjh_bot.util.DBUtil as DBUtil

URL_JFAEL = "http://www.jfael.or.jp/ja/"

NOTICE_REGEX_STR = "ja_info_all|ja_info_tokyo"  # 全国or東京の画像があるものを抜き出す
TAG_NAME_TD = "td"      # タグ名は大文字小文字を区別するので注意
TAG_NAME_IMG = "img"    # タグ名は大文字小文字を区別するので注意
ATTRI_NAME_SRC = "src"  # 属性名は大文字小文字を区別するので注意


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
    return requests.get(URL_JFAEL).text


################################################
# 通知情報を抜き出したリストを作成する
################################################
def __create_notice_list(row_data):
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
            ret_list.append(body)
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
