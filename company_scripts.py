from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def print_result(info):
    """Takes in a dictionary with keys for 'company', 'title', 'url',
    and 'description' and prints them neatly to the terminal"""

    for key in ['company', 'title', 'url', 'description']:
        assert key in info.keys(), \
            "The key '{}' is not in the dictionary".format(key)
        assert isinstance(info[key], str), \
            "The value at '{}' is not a string".format(key)

    print('{} - {}'.format(info['company'], info['title']))
    print(info['url'])
    print(info['description'])


def red_hat(driver):
    page_url = 'https://careers-redhat.icims.com/jobs/search?mobile=false&width=900&height=500&bga=true&needsRedirect=false&jan1offset=-300&jun1offset=-240'
    page_title = 'Red Hat Jobs'
    driver.get(page_url)
    # assert page_title in driver.title, \
    #     "'{}' not found, check url".format(page_title)
    driver.switch_to_frame(driver.find_element_by_name('icims_content_iframe'))
    elem = driver.find_element_by_name('searchKeyword')
    elem.send_keys('python')
    driver.find_element_by_xpath(
        "//select[@name='searchCategory']/option[@value='17505']").click()
    driver.find_element_by_xpath(
        "//select[@name='searchLocation']/option[@value='12781-12817-Raleigh']"
        ).click()
    elem.send_keys(Keys.RETURN)

    elems = driver.find_elements_by_xpath(
        "//table[@class='iCIMS_JobsTable iCIMS_Table']/tbody/tr/td[@itemprop='title']/a")
    for el in elems:
        print(el.get_attribute('href'))

def main():
    driver = webdriver.Firefox()

    red_hat(driver)

    driver.close()
    # print_result({'company': 'comp',
    #               'title': 'title',
    #               'url': 'url.com',
    #               'description': 'things and stuff'})


if __name__ == "__main__":
    main()
