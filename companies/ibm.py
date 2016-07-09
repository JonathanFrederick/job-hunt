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


def ibm(driver):
    ibm = db.session.query(Company).filter(Company.name == "IBM")[0]
    driver.get(ibm.careers_url)


    return driver
