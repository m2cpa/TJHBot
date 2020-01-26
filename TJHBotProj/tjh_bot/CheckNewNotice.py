'''
Created on 2020/01/14

@author: m2(@m2cpa)
'''
import tjh_bot.notice.Notice as Notice
import tjh_bot.util.TweetUtil as TweetUtil
import tjh_bot.util.TimeUtil as TimeUtil

MESSAGE_BASE_EXIST_NOTICE = \
    "【実務補習所　通知確認】\n" + \
    "　前回確認時から{date}までに新しい通知が{count}件あります。"

MESSAGE_BASE_NOT_EXIST_EVENT = \
    "【実務補習所　通知確認】\n" + \
    "　前回確認時から{date}までに新しい通知はありません。"

################################################
# 更新された通知情報をツイートする
################################################
if __name__ == '__main__':
    # 更新された通知情報を取得する
    tweet_notices = Notice.create_notice_list()

    # ツイートする
    date_str = TimeUtil.get_now_str(TimeUtil.TIME_FORMAT_YYMMDDHHMM)
    TweetUtil.tweet(
        tweet_notices,
        MESSAGE_BASE_EXIST_NOTICE.format(
            date=date_str,
            count=len(tweet_notices)),
        MESSAGE_BASE_NOT_EXIST_EVENT.format(date=date_str))
