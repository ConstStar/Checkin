'''
ikuuu签到
2020-7-29
by 布吉岛
'''

import requests
import json

# QQ提醒所需
qq = None
cq = None

#发送QQ消息
def sendMsg(msg):
    global qq
    global cq

    if qq == None or cq == None:
        return
    msg = 'ikuuu\n' + msg
    url = f'http://{cq}/send_private_msg?message={msg}&user_id={qq}'
    requests.get(url)

# 登录账号 返回cookie
def login(email, passwd):
    url = 'https://ikuuu.co/auth/login'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', }
    data = f'email={email}&passwd={passwd}&code='
    res = requests.post(url, data=data, headers=headers, allow_redirects=False)
    cookies = res.cookies
    cookie = requests.utils.dict_from_cookiejar(cookies)
    resJson = json.loads(res.text)
    
    if resJson['ret'] != 1:
        msg = resJson['msg']
        raise Exception(f'登录失败 {msg}')
    if len(cookie) == 0:
        raise Exception('登录失败 获取的cookie为空')

    # print(cookie)
    # print(res.text.encode().decode('unicode_escape'))
    return cookie

# 签到
def checkin(cookies):
    url = "https://ikuuu.co/user/checkin"
    headers = {'Content-Type': 'application/x-www-form-urlencoded', }
    res = requests.post(url, cookies=cookies, headers=headers, allow_redirects=False)
    
    if not res.ok:
        raise Exception(f'签到失败 网络异常')

    if len(res.text) == 0:
        raise Exception(f'签到失败 cookie无效')

    return json.loads(res.text)


def main():
    global qq
    global cq

    try:
        email = input('账号：')
        passwd = input('密码：')
        qq = input('QQ：')
        cq = input('CQHTTP：')
        cookie = login(email, passwd)
        res = checkin(cookie)
        msg = res['msg']
        print(msg)
        sendMsg(msg)
    except Exception as ex:
        msg = '出现异常\n账号：{}\n问题：{}'.format(email,ex.__str__())
        sendMsg(msg)
        print(msg)

if __name__ == "__main__":
    main()
