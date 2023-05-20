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
    timestamp = str(int(time.time()))
    args.append(timestamp)
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')


def get_mov_list():
    token = get_token(args=['/api/movie'])
    url = INDEX_URL.format(limit=10, offset=0, token=token)
    mov_count = requests.get(url, verify=False).json()['count']

    url = INDEX_URL.format(limit=mov_count, offset=0, token=token)
    mov_list = requests.get(url, verify=False).json()

    return mov_list


def get_mov_detail(mov_id):
    encrypt_id = base64.b64encode((SECRET + str(mov_id)).encode('utf-8')).decode('utf-8')
    url = DETAIL_URL.format(id=encrypt_id, token=get_token(args=[f'/api/movie/{encrypt_id}']))

    return requests.get(url, verify=False).json()


def get_all_mov_detail(mov_list):
    all_mov_detail = [get_mov_detail(mov['id']) for mov in mov_list['results']]

    print(f'已成功获取 {len(all_mov_detail)} 部电影详情')
    return all_mov_detail


if __name__ == '__main__':
    # 生成1-100的随机数
    mov = get_mov_detail(mov_id=random.randint(1, 100))
    for key, value in mov.items():
        print(key + ": ", value)

    # m_list = get_mov_list()
    # with open('mov_list.json', 'w', encoding='utf-8') as f:
    #     json.dump(m_list, f, ensure_ascii=False, indent=2)
    #
    # all_m_detail = get_all_mov_detail(m_list)
    # with open('all_mov_detail.json', 'w', encoding='utf-8') as f:
    #     json.dump(all_m_detail, f, ensure_ascii=False, indent=2)
