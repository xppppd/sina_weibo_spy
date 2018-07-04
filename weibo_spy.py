#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import time
import csv

cookie = {
    "Cookie": "cookie"  # 填入从浏览器获取的cookie
}


# weibo.cn内容方便爬取
# https://weibo.cn/xxxxxxxxx/info   个人资料页面
# https://weibo.cn/xxxxxxxxx/profile?page=2   微博列表   page 页码
# https://weibo.cn/xxxxxxxxx/profile?filter=1  原创微博   ----0：全波  1：原创  2：带图


# https://weibo.cn/comment/GiFBC0GwS   评论页面   GiFBC0GwS是对应微博id  post

def check_cookie():
    try:
        url = 'https://weibo.cn/'
        html = requests.get(url, cookies=cookie).content
        soup = BeautifulSoup(html, "lxml")
        if '"http://weibo.cn/reg/index"' in str(soup):
            print('cookie已失效!')
            return False
        else:
            return True
    except:
        print('请检查网络！')
        return False


# 获取个人资料页面 把基本信息存入字典并返回
def get_user_info(user_id):
    user_info = {}
    try:
        url = 'https://weibo.cn/{id}/info'.format(id=user_id)
        html = requests.get(url, cookies=cookie).content
        soup = BeautifulSoup(html, "lxml")
        # 获取包含基本信息的标签内容
        s = str(soup.find_all(class_='c')[3])
        # 用正则过滤出需要的内容
        data_list = re.compile('>(.*?)<br/').findall(s)
        for data in data_list[:-1]:
            slice = data.split(':', 1)
            if len(slice) != 2:
                slice = data.split('：', 1)
            user_info[slice[0]] = slice[1]
        user_info['id'] = user_id
    except Exception as e:
        print("Error: ", e)
    return user_info


# 按页数获取微博页面
def get_profile_page(user_id, filter=0, page=1):
    url = 'https://weibo.cn/{id}/profile?page={n}&filter={f}'.format(id=user_id, n=page, f=filter)
    try:
        html = requests.get(url, cookies=cookie).content
        return BeautifulSoup(html, "lxml")
    except:
        print('数据获取失败，请检查网络!')
        return None


# 爬取目标用户的全部微博并返回 ,Filter参数  0 全部微博 1 原创 2 带图
def get_msgs(user_id, Filter=0):
    msg_list = []
    soup = get_profile_page(user_id, Filter)
    # 通过定位元素位置，找到微博总数那一栏，并用正则得到数字
    if soup:
        try:
            total = int(re.findall('\d+', soup.find(class_='tip2').get_text().split()[0])[0])
            # 确定页数
            page_num = int(re.findall('\d+', str(soup.find('input', attrs={'name': 'mp'})))[0])
            for i in range(1, page_num + 1):
                soup = get_profile_page(user_id, Filter, i)
                for line in soup.find_all(id=re.compile('^M_.*?')):
                    msg_list.append(line.get_text())
                time.sleep(1)
            print('Done!')
            return msg_list
        except:
            print('cookid或代码已失效！')
    else:
        return None


# 获取关注列表 https://weibo.cn/id/follow?page=
def get_follow(user_id):
    followe_list = []
    follower = {}
    url = 'https://weibo.cn/{}/follow?page={}'.format(user_id, 1)
    html = requests.get(url, cookies=cookie).content
    soup = BeautifulSoup(html, 'lxml')
    page_num = int(re.findall('\d+', str(soup.find('input', attrs={'name': 'mp'})))[0])
    # print(page_num)
    for i in range(page_num - 1):
        table_list = soup.find_all('table')
        for con in table_list:
            split_str = str(con).split('>')
            nikename = con.select('tr a')[1].text
            id = re.compile('uid=(\d+)&').findall(str(con))[0]
            fans_num = re.compile('\d+').findall(con.text.split('粉丝')[-1])[0]
            follower['nikename'] = nikename
            follower['id'] = id
            follower['fans_num'] = fans_num
            followe_list.append(follower.copy())
        time.sleep(1)
        url = 'https://weibo.cn/{}/follow?page={}'.format(user_id, i + 2)
        html = requests.get(url, cookies=cookie).content
        soup = BeautifulSoup(html, 'lxml')
    return followe_list


def get_fans(user_id):
    fan_list = []
    fans = {}
    url = 'https://weibo.cn/{}/fans?page={}'.format(user_id, 1)
    html = requests.get(url, cookies=cookie).content
    soup = BeautifulSoup(html, 'lxml')
    page_num = int(re.findall('\d+', str(soup.find('input', attrs={'name': 'mp'})))[0])
    # print(page_num)
    for i in range(page_num - 1):
        table_list = soup.find_all('table')
        for con in table_list:
            split_str = str(con).split('>')
            nikename = con.select('tr a')[1].text
            id = re.compile('uid=(\d+)&').findall(str(con))[0]
            fans_num = re.compile('\d+').findall(con.text.split('粉丝')[-1])[0]
            fans['nikename'] = nikename
            fans['id'] = id
            fans['fans_num'] = fans_num
            fan_list.append(fans.copy())
        time.sleep(1)
        url = 'https://weibo.cn/{}/follow?page={}'.format(user_id, i + 2)
        html = requests.get(url, cookies=cookie).content
        soup = BeautifulSoup(html, 'lxml')
    return fan_list


# 获取关注列表 https://weibo.cn/id/follow
# 单页结果test
def get_follow__(user_id):
    followe_list = []
    follower = {}
    url = 'https://weibo.cn/{}/follow?page={}'.format(user_id, 1)
    html = requests.get(url, cookies=cookie).content
    soup = BeautifulSoup(html, 'lxml')
    page_num = int(re.findall('\d+', str(soup.find('input', attrs={'name': 'mp'})))[0])
    print(page_num)
    table_list = soup.find_all('table')
    for con in table_list:
        nikename = con.select('tr a')[1].text
        id = re.compile('uid=(\d+)&').findall(str(con))[0]
        fans_num = re.compile('\d+').findall(con.text.split('粉丝')[-1])[0]
        # split_str = str(con).split('>')
        # nikename = split_str[9].split('<')[0]
        # id = re.compile('uid=(\d+)&').findall(split_str[-6])[0]
        # fans_num = re.compile('\d+').findall(split_str[-7])[0]
        follower['nikename'] = nikename
        follower['id'] = id
        follower['fans_num'] = fans_num
        # print(follower)
        # print(type(follower))
        followe_list.append(follower.copy())
    return followe_list


def save_msgs_to_txt(user_info, msgs):
    with open(user_id + '_msgs.txt', "w") as f:
        for line in msgs:
            f.write(line + '\n')


def save_follows_info_to_csv(info):
    with open(user_id + '_follows_info.csv', "w") as f:
        headers = ['昵称', 'id', '性别', '生日', '简介', '地区', '达人', '认证', '认证信息', '感情状况', '性取向']
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(info)


def save_fans_info_to_csv(info):
    with open(user_id + '_fans_info.csv', "w") as f:
        headers = ['昵称', 'id', '性别', '生日', '简介', '地区', '达人', '认证', '认证信息', '感情状况', '性取向']
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(info)


def main():
    if check_cookie():
        print('running...please wait')
        user_info = get_user_info(user_id)
        msgs = get_msgs(user_id)
        save_msgs_to_txt(user_info, msgs)
        follows_info_list = []
        fans_info_list = []
        follows = get_follow(user_id)
        for follow in follows:
            s = get_user_info(follow['id'])
            print(s)
            follows_info_list.append(s.copy())
            time.sleep(1)
        fans = get_follow(user_id)
        for fan in fans:
            s = get_user_info(fan['id'])
            print(s)
            fans_info_list.append(s.copy())
            time.sleep(1)
        save_fans_info_to_csv(follows_info_list)
        print('Done!')


if __name__ == "__main__":
    user_id = 'id here'  #目标id
    main()
