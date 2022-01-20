from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # Go to https://www.google.com.hk/search?q=internet+outage&newwindow=1&tbm=nws&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiQrN7WhcD1AhViKqYKHU3mCuEQpwV6BAgBEBM&biw=1280&bih=720&dpr=1
    page.goto("https://www.google.com.hk/search?q=internet+outage&newwindow=1&tbm=nws&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwiQrN7WhcD1AhViKqYKHU3mCuEQpwV6BAgBEBM&biw=1280&bih=720&dpr=1")

    # Go to https://www.vicksburgpost.com/2022/01/19/att-internet-outages-in-warren-county-due-to-copper-theft/
    page1.goto("https://www.vicksburgpost.com/2022/01/19/att-internet-outages-in-warren-county-due-to-copper-theft/")

    # Go to https://tech-ish.com/2022/01/19/telkom-kenya-services-down/
    page2.goto("https://tech-ish.com/2022/01/19/telkom-kenya-services-down/")

    # Click text=Phone/internet service restored after days-long outage
    with page.expect_popup() as popup_info:
        page.click("text=Phone/internet service restored after days-long outage")
    page4 = popup_info.value

    # Click [aria-label="Search"]
    # with page.expect_navigation(url="https://www.wsaz.com/2022/01/20/phoneinternet-service-restored-after-days-long-outage/"):
    with page.expect_navigation():
        page.click("[aria-label=\"Search\"]")

    # Close page
    page.close()

    # Close page
    page4.close()

    # Close page
    page2.close()

    # Close page
    page1.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
