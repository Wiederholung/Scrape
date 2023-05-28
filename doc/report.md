# 大数据应用课程报告：JavaScript 逆向爬虫程序设计

## 爬虫程序设计

### 目标

调用网站数据接口，获取电影详情页信息。

<img src="https://web.metattri.com/i/2023/05/28/6473050758982.png" alt="image-20230528153846167" style="zoom:67%;" />

### 分析

1. 该电影网站的数据通过 [Ajax](https://en.wikipedia.org/wiki/Ajax_(programming)) 加载，电影详情页数据接口 (URL)
   的返回值 (JSON) 包含指定电影的全部信息，与电影详情页对应，如上图的右侧所示。该接口有如下结构：

   > <font size=5><font color=#5b9bd5>https</font>://<font color=#ffc000>spa6.scrape.center</font><font color=#70ad47>
   > /api/movie/{encrypt_id}</font>/<font color=#ed7d31>?token={token}</font></font>
   >
   > - <font color=#5b9bd5>**protocol:** https</font>
   > - <font color=#ffc000>**host:** spa6.scrape.center</font>
   > - <font color=#70ad47>**path:**</font> `encrypt_id` 代表经过**加密**的电影唯一标识符（下称电影的原始唯一标识符为电影
       id）
   > - <font color=#ed7d31>**query:**</font> URL 设有过期策略，这意味着 `token` 具有**时效性**

2. 网站还使用了电影列表的数据接口，该接口的返回值同样是 JSON 格式，包含了指定电影数量和偏移量的**电影 id** 和电影摘要等数据。
   例如 <font color=#ed7d31>query = ?limit=**2**&offset=0&token=NTU...x</font> 的返回值如下：

    ```JSON
    {
    "count": 101,
    "results": [
      {
        "id": 1,
        "name": "霸王别姬",
        "alias": "Farewell My Concubine",
        "cover": "https://p0.meituan.net/movie/ce4da3e03e655b5b88ed31b5cd7896cf62472.jpg@464w_644h_1e_1c",
        "categories": ["剧情", "爱情"],
        "published_at": "1993-07-26",
        "minute": 171,
        "score": 9.5,
        "regions": ["中国内地", "中国香港"]
      },
      {
        "id": 2,
        "name": "这个杀手不太冷",
        "alias": "Léon",
        "cover": "https://p1.meituan.net/movie/6bea9af4524dfbd0b668eaa7e187c3df767253.jpg@464w_644h_1e_1c",
        "categories": ["剧情", "动作", "犯罪"],
        "published_at": "1994-09-14",
        "minute": 110,
        "score": 9.5,
        "regions": ["法国"]
      }
    ]
    }
    ```

   该接口 (URL) 结构如下：

   > <font size=5><font color=#5b9bd5>https</font>://<font color=#ffc000>spa6.scrape.center</font><font color=#70ad47>/api/movie</font>/<font color=#ed7d31>?limit={limit}&offset={offset}&token={token}</font></font>
   >
   > <font color=#ed7d31>**query**</font> 字段有三个参数，分别是：
   >   - `limit`: 列表中电影数量
   >   - `offset`: 偏移量
   >   - `token`: 列表页 token

3. 该网站对 JavaScript 代码进行了[**混淆**](https://en.wikipedia.org/wiki/Obfuscation_(software))

**因此，我们需要根据 JavaScript 代码逆向解析出 `encrypt_id` 和 `token` 的生成方法（TODO节已给出），并实现，然后再调用数据接口获取电影详情页信息。**

### 实现

以下内容采用 notebook 的形式展示。

#### 准备工作

##### 导入依赖库并禁用 SSL 警告

```python
import base64
import hashlib
import random
import time
from typing import List, Any

import requests
import urllib3

urllib3.disable_warnings()
```

##### 定义常量

- INDEX_URL：电影列表 URL

    - `limit`：电影数量
    - `offset`：偏移量
    - `token`：列表页 token
- DETAIL_URL：电影详情 URL
    - `encrypt_id`：电影 id（加密后）
    - `token`：详情页 token
- SECRET：密钥（对应 TODO）

```python
INDEX_URL = 'https://spa6.scrape.center/api/movie?limit={limit}&offset={offset}&token={token}'
DETAIL_URL = 'https://spa6.scrape.center/api/movie/{encrypt_id}?token={token}'
SECRET = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'
```

#### 获取 token

- 参数：<font color=#70ad47>path</font> (e.g. **/api/movie**)
- 返回：token（base64 编码后的字符串）

```python
def get_token(args: List[Any]):
    # 获取时间戳
    timestamp = str(int(time.time()))
    # 将时间戳加入参数列表
    args.append(timestamp)
    sign1 = ','.join(args)
    print('1. 拼接 path 和时间戳：\t\t', sign1)
    # 将参数列表转为字符串并进行SHA1加密
    sign2 = hashlib.sha1(sign1.encode('utf-8')).hexdigest()
    print('2. 对上一步结果进行 SHA1 加密：\t', sign2)
    # 将加密后的字符串和时间戳拼接并进行base64编码
    sign3 = sign2 + ',' + timestamp
    print('3. 拼接加密后的字符串和时间戳：\t', sign3)
    token = base64.b64encode(sign3.encode('utf-8')).decode('utf-8')
    print('4. 对上一步结果进行 base64 编码：', token, '\n')
    return token


get_token(args=['/api/movie'])
```

    1. 拼接 path 和时间戳：		 /api/movie,1685265861
    2. 对上一步结果进行 SHA1 加密：	 5203a412bc9595544c1a98aa342a2987072fafbf
    3. 拼接加密后的字符串和时间戳：	 5203a412bc9595544c1a98aa342a2987072fafbf,1685265861
    4. 对上一步结果进行 base64 编码： NTIwM2E0MTJiYzk1OTU1NDRjMWE5OGFhMzQyYTI5ODcwNzJmYWZiZiwxNjg1MjY1ODYx 

    'NTIwM2E0MTJiYzk1OTU1NDRjMWE5OGFhMzQyYTI5ODcwNzJmYWZiZiwxNjg1MjY1ODYx'

#### 获取电影列表

- 参数：无
- 返回：JSON 格式的电影列表

##### 方法

1. 获取 token
2. 构造 URL：limit=10, offset=0, token=token
3. 获取 URL 的 response ，提取电影总数
4. 根据电影总数构造新的 URL：limit=mov_count, offset=0, token=token
5. 接收新的 URL 的 response ，提取 JSON 格式的电影列表
6. 返回电影列表

```python
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


get_mov_list()
```

#### 获取电影详情

- 参数：电影 id
- 返回：JSON 格式的电影详情

##### 方法

1. 将电影 id 与密钥 SECRET 拼接后进行 base64 编码，得到加密后的电影 id
2. 根据 path '/api/movie/{encrypt_id}' 获取 token
3. 根据加密 id 和 token 构造新的 URL
4. 接收新的 URL 的 response ，提取 JSON 格式的电影详情
5. 返回电影详情

```python
def get_mov_detail(mov_id):
    # 对电影id进行加密
    encrypt_id = base64.b64encode((SECRET + str(mov_id)).encode('utf-8')).decode('utf-8')
    # 构造URL
    url = DETAIL_URL.format(encrypt_id=encrypt_id, token=get_token(args=[f'/api/movie/{encrypt_id}']))
    # 获取电影详情
    return requests.get(url, verify=False).json()


get_mov_detail(random.randint(1, 100))
```

#### 获取所有电影详情

- 参数：JSON 格式的电影列表
- 返回：JSON 格式的列表中的所有电影详情

##### 方法

遍历电影列表，调用 get_mov_detail()，获取每部电影的详情，最后返回所有电影详情

```python
def get_all_mov_detail(mov_list):
    # 获取所有电影详情
    all_mov_detail = [get_mov_detail(mov['id']) for mov in mov_list['results']]
    # 打印获取电影详情的数量
    print(f'已成功获取 {len(all_mov_detail)} 部电影详情')
    return all_mov_detail


get_all_mov_detail(get_mov_list())
```
