from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import time
from datetime import datetime


def current_time():
    return datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')


def wait_for_element(driver, xpath):
    wait = WebDriverWait(driver, 10)
    try:
        elem = wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath))
        )
    finally:
        pass

    return elem


def get_frame(driver, url):
    driver.get(url)
    elem = wait_for_element(driver, "//iframe[@name='icims_content_iframe']")
    driver.switch_to_frame(elem)
    return driver


def fill_form(driver):
    # move driver to iframe with form
    # driver.switch_to_frame(driver.find_element_by_name('icims_content_iframe'))

    # select desired form inputs
    elem = driver.find_element_by_name('searchKeyword')  # Keyword
    elem.send_keys('python')
    driver.find_element_by_xpath(  # Category
        "//select[@name='searchCategory']/option[@value='17505']").click()
    driver.find_element_by_xpath(  # Location
        "//select[@name='searchLocation']/option[@value='12781-12817-Raleigh']"
        ).click()
    elem.send_keys(Keys.RETURN)

    return driver


def get_listing_urls(driver):
    # grab list of listing urls
    urls = []
    while True:
        # grab anchor tag for each job listing
        elems = driver.find_elements_by_xpath(
            "//table[@class='iCIMS_JobsTable iCIMS_Table']/tbody/tr/td[\
            @itemprop='title']/a")

        # append url from each anchor tag to url list
        for el in elems:
            urls.append(el.get_attribute('href')[:-12])

        # check for a next button and click
        try:
            driver.find_element_by_xpath(
                "//div[@class='iCIMS_JobsTablePaging iCIMS_Table']/div/div[\
                @class='iCIMS_TableCell']/a/img[@alt='Next']"
                ).click()
        except NoSuchElementException:
            break

    return urls


def get_content(driver):
    title = wait_for_element(driver, "//h1[@class='iCIMS_Header']").text
    head = driver.find_elements_by_xpath("//dd[@class='iCIMS_JobHeaderData']")
    text_div_str = "//div[@class='iCIMS_InfoMsg iCIMS_InfoMsg_Job']"
    company_desc = driver.find_element_by_xpath(text_div_str + '[1]').text
    job_sum = driver.find_element_by_xpath(text_div_str + '[2]').text
    resps = driver.find_elements_by_xpath(text_div_str + '[3]/div/div/ul/li')
    resps = [r.text for r in resps]
    skills = driver.find_elements_by_xpath(text_div_str + '[4]/div/div/ul/li')
    skills = [s.text for s in skills]
    return {'title': title,
            'company': 'Red Hat',
            'id': head[0].text,
            'post_date': head[3].text,
            'company_desc': company_desc,
            'job_sum': job_sum,
            'responsibilities': resps,
            'skills': skills,
            'time_scraped': current_time()
            }


def red_hat(driver):
    page_url = 'https://careers-redhat.icims.com/jobs/search'
    page_title = 'Red Hat Jobs'
    # driver.get(page_url)
    driver = get_frame(driver, page_url)

    # assert page_title in driver.title, \
    #     "'{}' not found, check url".format(page_title)

    driver = fill_form(driver)
    urls = get_listing_urls(driver)
    listings = []
    for url in urls:
        # print(url)
        driver = get_frame(driver, url)
        listing = get_content(driver)
        listing['url'] = url
        listings.append(listing)

    print(listings)
