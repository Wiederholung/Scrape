import json

from playwright.sync_api import sync_playwright

COUNT = 0
TOKEN = ''


def on_response(response):
    global COUNT, TOKEN
    if '/api/movie/' in response.url and response.status == 200:
        # 获取url中的token参数
        TOKEN = response.url.split('=')[-1]
        # response.json()转换为字典
        mov_list = response.json()
        COUNT = mov_list['count']


def scrape_mov_list():
    global COUNT, TOKEN
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 监听response事件
        page.on('response', on_response)

        # 访问网页
        page.goto('https://spa6.scrape.center/')

        # 等待网页加载完成
        page.wait_for_load_state('networkidle')

        # 访问带有参数的网页
        page.goto(f'https://spa6.scrape.center/api/movie/?limit={COUNT}&offset=0&token={TOKEN}')

        # 等待网页加载完成
        page.wait_for_load_state('networkidle')

        # 获取API返回的JSON数据
        mov_list = page.evaluate('() => JSON.parse(document.body.innerText)')

        browser.close()

        return mov_list


if __name__ == '__main__':
    # 运行同步函数
    m_list = scrape_mov_list()
    # 将API返回的JSON数据保存到文件，中文需要指定编码为utf-8
    with open('data/mov_list.json', 'w', encoding='utf-8') as f:
        json.dump(m_list, f, ensure_ascii=False, indent=2)
