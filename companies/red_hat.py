from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sqlalchemy.orm.exc import MultipleResultsFound

from time import time
from datetime import datetime

from app import db
from models import Listing, Company


def current_time():
    return datetime.fromtimestamp(time()).now().strftime('%Y-%m-%d %H:%M:%S')


def wait_for_element(driver, xpath):
    wait = WebDriverWait(driver, 10)
    try:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    finally:
        pass
    return elem


def get_frame(driver, url):
    driver.get(url)
    elem = wait_for_element(driver, "//iframe[@name='icims_content_iframe']")
    driver.switch_to_frame(elem)
    return driver


def fill_form(driver, kw, loc, dpt):
    # move driver to iframe with form
    # driver.switch_to_frame(driver.find_element_by_name('icims_content_iframe'))

    # select desired form inputs
    elem = driver.find_element_by_name('searchKeyword')  # Keyword
    elem.clear()
    elem.send_keys(kw)
    driver.find_element_by_xpath(  # Category
        "//select[@name='searchCategory']/option[@value={}]".format(dpt)
        ).click()
    driver.find_element_by_xpath(  # Location
        "//select[@name='searchLocation']/option[@value='{}']".format(loc)
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
            }


def exists(listing):
    try:
        q = db.session.query(Listing).filter(
            Listing.title == listing['title'],
            Listing.company == listing['company']).one_or_none()
        if q:
            q.seen_now()
            print("Updating last_seen for {} - {}"
                  .format(listing['company'], listing['title']))
            return q
        else:
            return q
    except MultipleResultsFound:
        print("Found multiple results for {} - {}"
              .format(listing['company'], listing['title']))


def db_entry(listing):
    entry = Listing(
        url=listing['url'],
        company=listing['company'],
        title=listing['title'])
    db.session.add(entry)
    db.session.commit()


def red_hat(driver):
    rh = db.session.query(Company).filter(Company.name == "Red Hat")[0]
    # page_url = 'https://careers-redhat.icims.com/jobs/search'
    driver = get_frame(driver, rh.careers_url)
    all_urls = []
    for kw in rh.keywords:
        for loc in rh.locations:
            for dpt in rh.departments:
                driver = fill_form(driver, kw, loc, dpt)
                urls = get_listing_urls(driver)
                all_urls += urls
    listings = []
    for url in all_urls:
        driver = get_frame(driver, url)
        listing = get_content(driver)
        listing['url'] = url
        if not exists(listing):
            db_entry(listing)
        listings.append(listing)

    # print(listings)
