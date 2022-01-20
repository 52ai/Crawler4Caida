from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    iphone_12_pro_max = p.devices['iPhone 12 Pro Max']
    browser = p.webkit.launch(headless=False)
    context = browser.new_context(
        **iphone_12_pro_max,
        locale='zh-CN',
        geolocation={'longitude': 116.39014, 'latitude': 39.913904},
        permissions=['geolocation']
    )
    page = context.new_page()
    page.goto('https://amap.com')
    page.wait_for_load_state(state='networkidle')
    page.screenshot(path='location-iphone.png')
    browser.close()
