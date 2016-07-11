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


def wait_for_element(driver, xpath):
    wait = WebDriverWait(driver, 10)
    try:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    finally:
        pass
    return elem


def fill_form(driver, dep, loc, kw):
    # driver.find_element_by_xpath("//div[@class='powerSearchLink']/a").click
    elem = wait_for_element(driver, "//div[@class='powerSearchLink']/a")
    elem.click()
    return driver

def ibm(driver):
    ibm = db.session.query(Company).filter(Company.name == "IBM")[0]
    driver.get(ibm.careers_url)
    for dep in ibm.departments:
        fill_form(driver, dep, '', '')


    return driver
