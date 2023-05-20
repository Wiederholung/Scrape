import base64
import hashlib
import random
import time
from typing import List, Any

import requests
import urllib3

INDEX_URL = 'https://spa6.scrape.center/api/movie?limit={limit}&offset={offset}&token={token}'
DETAIL_URL = 'https://spa6.scrape.center/api/movie/{id}?token={token}'
SECRET = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'

# 去除SSL验证警告
urllib3.disable_warnings()


def get_token(args: List[Any]):
    # 获取时间戳
    timestamp = str(int(time.time()))
    # 将时间戳加入参数列表
    args.append(timestamp)
    # 将参数列表转为字符串并进行SHA1加密
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    # 将加密后的字符串和时间戳拼接并进行base64编码
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')


def get_mov_list():
    # 获取token
    token = get_token(args=['/api/movie'])
    # 构造URL
    url = INDEX_URL.format(limit=10, offset=0, token=token)
    # 获取电影总数
    mov_count = requests.get(url, verify=False).json()['count']
    # 根据电影总数构造新的URL
    url = INDEX_URL.format(limit=mov_count, offset=0, token=token)
    # 获取电影列表
    mov_list = requests.get(url, verify=False).json()
    return mov_list


def get_mov_detail(mov_id):
    # 对电影ID进行加密
    encrypt_id = base64.b64encode((SECRET + str(mov_id)).encode('utf-8')).decode('utf-8')
    # 构造URL
    url = DETAIL_URL.format(id=encrypt_id, token=get_token(args=[f'/api/movie/{encrypt_id}']))
    # 获取电影详情
    return requests.get(url, verify=False).json()


def get_all_mov_detail(mov_list):
    # 获取所有电影详情
    all_mov_detail = [get_mov_detail(mov['id']) for mov in mov_list['results']]
    # 打印获取电影详情的数量
    print(f'已成功获取 {len(all_mov_detail)} 部电影详情')
    return all_mov_detail


if __name__ == '__main__':
    # 生成1-100的随机数
    m_info = get_mov_detail(mov_id=random.randint(1, 100))
    # 打印电影详情
    for key, value in m_info.items():
        print(key + ": ", value)

    # m_list = get_mov_list()
    # with open('mov_list.json', 'w', encoding='utf-8') as f:
    #     json.dump(m_list, f, ensure_ascii=False, indent=2)
    #
    # all_m_detail = get_all_mov_detail(m_list)
    # with open('all_mov_detail.json', 'w', encoding='utf-8') as f:
    #     json.dump(all_m_detail, f, ensure_ascii=False, indent=2)
