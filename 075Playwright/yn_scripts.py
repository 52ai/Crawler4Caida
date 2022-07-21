from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to http://www.spbycz.com/
    page.goto("http://www.spbycz.com/")

    # Go to http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html
    page.goto("http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html")

    # Go to http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/
    page.goto("http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/")

    # Go to http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/home
    page.goto("http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/home")

    print(page.content())

    # Click text=云南石屏北银村镇银行服务价目表
    # with page.expect_navigation(url="http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/newsAndNotices/noticeDetail"):
    with page.expect_navigation():
        page.click("text=云南石屏北银村镇银行服务价目表")
    # assert page.url == "http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/redirect/newsAndNotices/noticeDetail"

    # Click text=注：1、政府定价和政府指导价收费依据：发改价【2014】268号，《商业银行服务价格管理办法》（中国银行业监督管理委员会、国家发展和改革委员会2014年第1号令
    page.click("text=注：1、政府定价和政府指导价收费依据：发改价【2014】268号，《商业银行服务价格管理办法》（中国银行业监督管理委员会、国家发展和改革委员会2014年第1号令")

    # Click text=云南石屏北银村镇银行对公函证业务受理公告
    # with page.expect_navigation(url="http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/newsAndNotices/noticeDetail"):
    with page.expect_navigation():
        page.click("text=云南石屏北银村镇银行对公函证业务受理公告")

    # Click text=企业开户服务线上投诉电话
    # with page.expect_navigation(url="http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/newsAndNotices/noticeDetail"):
    with page.expect_navigation():
        page.click("text=企业开户服务线上投诉电话")
    # assert page.url == "http://www.spbycz.com:8898/fpaas_bucket/20213411_prod/h5/41000001-1.0.0.2/html/index.html#/redirect/newsAndNotices/noticeDetail"
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
