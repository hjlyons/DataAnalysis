from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False

def get_driver(URL='https://olympics.com/tokyo-2020/olympic-games/en/results/taekwondo/olympic-schedule-and-results.htm', clear_popups=True):

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    # Give a 10s buffer to let the cookie window load :]
    driver.implicitly_wait(10) 

    if clear_popups:
    # Accept Cookies
    cookie_buttons = driver.find_elements_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
    # Close Pop-Up
    popup_buttons = driver.find_elements_by_xpath('//*[@id="gdfr-initial-screen"]/div[2]/div[3]/a[1]')

    if clear_popups:
        for b in cookie_buttons:
            b.click()
        for b in popup_buttons:
            b.click()

    return driver