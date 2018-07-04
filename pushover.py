# pushover API：https://api.pushover.net/1/messages.json

import requests

# 推送消息至手机

# pushover的token和user
token = 'xx'
user = 'xx'


def push(title, msg, url='', timestamp=''):
    api = 'https://api.pushover.net/1/messages.json'
    data = {
        'token': token,
        'user': user,
        'title': title,
        'message': msg,
        'url': url,
    }
    return requests.post(api, data)


if __name__ == '__main__':
    response = push('test', 'hello', 'weibo.com')
    print(response.status_code)
    print(response.content)
    print(response.json())
