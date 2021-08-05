from selenium import webdriver

OLYMPICS_RESULTS_URL =  'https://olympics.com/tokyo-2020/olympic-games/en/results/taekwondo/olympic-schedule-and-results.htm'

def setup_webdriver(clear_popups=True, headless=True):
    """Returns a chromium driver (looks in PATH to find it by default)

    :param clear_popups: Should cookie and popup windows be closed?
    :type clear_popups: bool

    :param headless: Should the driver be headless?
    :type headless: bool

    :rtype: selenium.webdriver.chrome.webdriver.WebDriver
    :return: driver, chromium web driver object
    """
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = headless
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(OLYMPICS_RESULTS_URL)
    # Give a 10s buffer to let the cookie window load :]
    driver.implicitly_wait(10) 

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

def parse_match_urls(driver, match_xpath='//div[1]/table/tbody/tr[*]'):
    """Returns a list of individual match URLS found on the main olympics URL page: https://olympics.com/tokyo-2020/olympic-games/en/results/taekwondo/olympic-schedule-and-results.htm

    :param driver: The driver object being used
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param match_xpath: The XPath string used to obtain match table elements
    :type match_xpath: str

    :rtype: list[str]
    :return: full_urls, list of fullt formatted URLS for each individual match
    """

    results = driver.find_elements_by_xpath(match_xpath)
    relative_urls = [r.get_attribute("data-url") for r in results]
    relative_urls = [r for r in relative_urls if r]

    BASE_URL = '/'.join(OLYMPICS_RESULTS_URL.split('/')[:-1]) + "/"
    full_urls = [BASE_URL + r for r in relative_urls]

    return full_urls


def parse_contestant_row(contestant_element):

    contestant_vars = {}    
    contestant_vars["fullname"] = contestant_element.find_element_by_xpath('.//*[@class="name"]').text
    contestant_vars["noc"] = contestant_element.find_element_by_xpath('.//*[@class="noc"]').text

    # Parse the table column contents into a python list for easier indexing
    td_list = contestant_element.find_elements_by_xpath('./td')    

    contestant_vars["win_string"] = td_list[2].text
    contestant_vars["score_total"] = td_list[3].text
    contestant_vars["score_round1"] = td_list[4].text
    contestant_vars["score_round2"] = td_list[5].text
    contestant_vars["score_round3"] = td_list[6].text
    
    return contestant_vars


def parse_match_page(driver, URL):
    
    driver.get(URL)
    
    TABLE_RESULTS_XPATH = './/*[@class="table table-result"]'
    CONTESTANT_RESULTS_XPATH = './/*[starts-with(@class,"Res")]'

    results_table_element = driver.find_elements_by_xpath(TABLE_RESULTS_XPATH)[-1]
    contestant_row_elements = results_table_element.find_elements_by_xpath(CONTESTANT_RESULTS_XPATH)

    all_contestant_vars = {}
    for i, contestant_element in enumerate(contestant_row_elements):
        contestant_tag = f"contestant{i+1}"
        parsed_contestant_vars = parse_contestant_row(contestant_element)
        # just append the contestant_tag to the keys, and update the full all_contestant_vars dictionary 
        parsed_contestant_vars = {f'{contestant_tag}_{k}': v for k, v in parsed_contestant_vars.items()}
        all_contestant_vars.update(parsed_contestant_vars)

    return all_contestant_vars