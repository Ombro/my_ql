# 天气推送脚本
import requests
import json
import datetime
from utils import utils_notify

appID = "wx48ba0057a632e0d0"
appSecret = "1aeb7c97444291b70a059e643bd11d29"
openIdList = [
    "oxtrZ6G0zoTb_CgecWnExwpkUczo",
    "oxtrZ6N8kQkrlFU1lsXBNm-OZYeI",
]

def get_weather_json(url):
    resp = requests.get(url)
    data = json.loads(resp.text)
    city = data['cityInfo']['city']
    weather=data['data']['forecast']
    return city, weather

def cal_aqi(aqi_str):
    rank = {
        50 : "优",
        100 : "良好",
        150 : "轻度污染",
        200 : "中度污染",
        300 : "重度污染",
        999999 : "严重污染",
    }
    aqi = int(aqi_str)
    for val, str in rank.items():
        if aqi <= val:
            return str

def format_msg_body(city, weather):
    info = {}
    cur_hour = datetime.datetime.now().hour
    print("当前小时:", cur_hour)
    cur_day = 1
    city_info = city + "今天天气情况:"
    if cur_hour >= 20:
        cur_day = 2
        city_info = city + "明天天气情况:"

    content = weather[cur_day-1]
    msg_body = {
        "template_id": "R5bAiVELkb9GB6EJg_OMhuUiuN6gZgVpz3egEzQdc6Q",
        "url": "http://weather.cma.cn/web/weather/59287.html",
        "data": {
            "city": {
                "value": city_info,
                "color": "#173177"
            },
            "date": {
                "value": content['ymd'] + ' ' + content ['week'],
                "color": "#173177"
            },
            "temperature": {
                "value": content['high'] + ' ' + content['low'],
                "color": "#173177"
            },
            "wind": {
                "value": content['fx'] + ':' + content['fl'],
                "color": "#173177"
            },
            "weather_type": {
                "value": content['type'],
                "color": "#173177"
            },
            "AQI": {
                "value": '空气质量:' + cal_aqi(content['aqi']),
                "color": "#173177"
            },
            "tips": {
                "value": content['notice'],
                "color": "#173177"
            },
        }
    }
    return msg_body

def get_weather_msg_body():
    url ='http://t.weather.sojson.com/api/weather/city/101280102'
    city, weather = get_weather_json(url) 
    msg_body = format_msg_body(city, weather)
    print(msg_body)
    return msg_body

if __name__ == '__main__':
    msg_body = get_weather_msg_body()
    notify = utils_notify.Notify()
    notify.notify(msg_body)
