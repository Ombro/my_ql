# 毒鸡汤推送脚本

import requests
import json
import datetime
import math
from utils import utils_notify
from config import config_soul_lists

soul_lists = config_soul_lists.soul_lists
start_time = 1696953600 # 2023-10-11 00:00:00

def get_index():
    now_ts = int(datetime.datetime.now().timestamp())
    diff_ts = now_ts - start_time
    counter = math.floor(diff_ts / 3600 / 12)
    soul_num = len(soul_lists)
    hour2index = counter % soul_num
    return hour2index

# 每个字段不超过20个字
def format_content():
    index = get_index()
    content = soul_lists[index]
    length = 20
    result = [content[i:i+length] for i in range(0, len(content), length)]
    return result

def format_msg_body():
    content_list = format_content()
    length = len(content_list)
    msg_body = {}
    msg_body['template_id'] = "DQzCGZrNVDHKWg7oyUTZcSYkDdLnp5m4N_Mr4jZ87Ds"
    msg_body['data'] = {}
    for i in range(length):
        value = ""
        if i <= length - 1:
            value = content_list[i]

        msg_body['data']['content'+str(i+1)] = {
            "value": value,
        }
    print(msg_body)
    return msg_body

if __name__ == '__main__':
    msg_body = format_msg_body()
    notify = utils_notify.Notify()
    notify.notify(msg_body)
