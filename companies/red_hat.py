from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def red_hat(driver):
    page_url = 'https://careers-redhat.icims.com/jobs/search?'
    page_title = 'Red Hat Jobs'
    driver.get(page_url)
    # assert page_title in driver.title, \
    #     "'{}' not found, check url".format(page_title)

    # move driver to iframe with form
    driver.switch_to_frame(driver.find_element_by_name('icims_content_iframe'))

    # select desired form inputs
    elem = driver.find_element_by_name('searchKeyword')  # Keyword
    elem.send_keys('python')
    driver.find_element_by_xpath(  # Category
        "//select[@name='searchCategory']/option[@value='17505']").click()
    driver.find_element_by_xpath(  # Location
        "//select[@name='searchLocation']/option[@value='12781-12817-Raleigh']"
        ).click()
    elem.send_keys(Keys.RETURN)

    # grab list of listing urls
    urls = []
    while True:
        # grab anchor tag for each job listing
        elems = driver.find_elements_by_xpath(
            "//table[@class='iCIMS_JobsTable iCIMS_Table']/tbody/tr/td[\
            @itemprop='title']/a")

        # append url from each anchor tag to url list
        for el in elems:
            urls.append(el.get_attribute('href'))

        # check for a next button and click
        try:
            driver.find_element_by_xpath(
                "//div[@class='iCIMS_JobsTablePaging iCIMS_Table']/div/div[\
                @class='iCIMS_TableCell']/a/img[@alt='Next']"
                ).click()
        except NoSuchElementException:
            break

    for url in urls:
        print(url)
