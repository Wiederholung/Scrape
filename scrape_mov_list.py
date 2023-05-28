import json
import asyncio
from playwright.async_api import async_playwright

COUNT = 0
TOKEN = ''


async def on_response(response):
    global COUNT, TOKEN
    if '/api/movie/' in response.url and response.status == 200:
        # Get the 'token' parameter from the URL
        TOKEN = response.url.split('=')[-1]
        # Convert the response.json() to a dictionary
        mov_list = await response.json()
        COUNT = mov_list['count']


async def scrape_mov_list():
    global COUNT, TOKEN
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Listen to the 'response' event
        page.on('response', on_response)

        # Access the web page
        await page.goto('https://spa6.scrape.center/')

        # Wait for the web page to load
        await page.wait_for_load_state('networkidle')

        # Access the web page with parameters
        await page.goto(f'https://spa6.scrape.center/api/movie/?limit={COUNT}&offset=0&token={TOKEN}')

        # Wait for the web page to load
        await page.wait_for_load_state('networkidle')

        # Get the JSON data returned by the API
        mov_list = await page.evaluate('() => JSON.parse(document.body.innerText)')

        await browser.close()

        return mov_list


async def main():
    # Run the async function
    m_list = await scrape_mov_list()
    # Save the JSON data returned by the API to a file
    with open('data/mov_list.json', 'w', encoding='utf-8') as f:
        json.dump(m_list, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    asyncio.run(main())
