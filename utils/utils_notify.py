# 微信测试号推送脚本

import requests
import json

class Notify():
    def __init__(self):
        self.__appID = "wx48ba0057a632e0d0"
        self.__appSecret = "1aeb7c97444291b70a059e643bd11d29"
        self.__openIdList = [
            "oxtrZ6G0zoTb_CgecWnExwpkUczo",
            "oxtrZ6N8kQkrlFU1lsXBNm-OZYeI",
        ]

    def __get_access_token(self):
        # 获取access token的url
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
            .format(self.__appID, self.__appSecret)
        response = requests.get(url).json()
        access_token = response.get('access_token')
        return access_token

    def __send_msg(self, access_token, msg_body):
        for openId in self.__openIdList:
            msg_body['touser'] = openId
            url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
            print(requests.post(url, json.dumps(msg_body)).text)

    def notify(self, msg_body):
        # 1.获取access_token
        access_token = self.__get_access_token()
        # 2.发送模板消息
        self.__send_msg(access_token, msg_body)
