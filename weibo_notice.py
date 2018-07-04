from pushover import push
from weibo_spy import get_profile_page
import re
from datetime import datetime
from datetime import timedelta

# 将指定用户的微博更新通过pushover推送到手机

# 该方式有bug，方便定义提醒间隔  可先判断是否一个小时内发的  再判断是否 1-n小时内发送的；
def notice_me_old(filter):
    an_hour_ago = (datetime.now() - timedelta(hours=1)).strftime("%m月%d日%H:%M")
    soup = get_profile_page(user_id, filter)
    nearest_one = soup.find_all(id=re.compile('^M_.*?'))[0]
    # print(nearest_one.get_text())
    print(nearest_one.find('span', class_="ct").get_text())
    rep_time = ''
    for i in nearest_one.find('span', class_="ct").get_text().split()[:2]:
        rep_time += i
    print(rep_time)
    print(an_hour_ago)
    print(datetime.now())
    if rep_time > an_hour_ago:
        push('微博更新提醒', msg=nearest_one.get_text())
    print('Done!')


def notice_me(user_id, filter):
    soup = get_profile_page(user_id, filter)
    # 定位微博正文的div
    profiles = soup.find_all(id=re.compile('^M_.*?'))
    nearest_one = profiles[0]
    # 排除第一条是置顶微博的情况
    if profiles[0].find_all('span', class_='kt'):
        nearest_one = profiles[1]
    print(datetime.now())
    if '分钟' in nearest_one.find('span', class_="ct").get_text():
        try:
            push('微博更新提醒', msg=nearest_one.get_text())
            print('Send success!!')
        except Exception as e:
            print('Send failed!!')


if __name__ == '__main__':
    # user_id = '1904769205'  # zhihu
    user_id = '1662316853'
    notice_me(user_id, 0)  # 用cron每小时自动运行一次
