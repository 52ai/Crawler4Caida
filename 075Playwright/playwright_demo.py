# coding:utf-8

"""
create on Jan 21, 2022 By Wayne YU
Function:

Test playwright

This are two mode of Playwright, synchronous(like Selenium) and asynchronous(like Pyppeteer)

"""

from playwright.sync_api import sync_playwright
import time

star_time = time.time()

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.baidu.com')
        # print(page.content())
        page.screenshot(path=f'screenshot-{browser_type.name}.png')
        print(page.title())
        browser.close()

# import asyncio
# from playwright.async_api import async_playwright
#
#
# async def main():
#     async with async_playwright() as p:
#         for browser_type in [p.chromium, p.firefox, p.webkit]:
#             browser = await browser_type.launch(headless=False)
#             page = await browser.new_page(headless=False)
#             await page.goto('http://www.mryu.top')
#             await page.screenshot(path=f'screenshot-asyn-{browser_type.name}.png')
#             print(await page.title())
#             await browser.close()
# asyncio.run(main())

print("time consuming:", (time.time() - star_time))