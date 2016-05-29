import os
from indeed import IndeedClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

FIRST_NAME = input('Enter your first name: ')
LAST_NAME = input('Enter your last name: ')
EMAIL_ADDRESS = input('Enter your email address: ')
JOB_DESCRIPTION = input('Enter a job title: ')
JOB_LOCATION = input('Enter a location: ')
RESUME = input('Enter the filename of your resume: ')

driver = webdriver.Firefox()


def indeed_parameters(what, where):
    """Use Indeed API to obtain job application links.
    :param q: job description
    :param l: job location; searches entire U.S. when left blank
    :param sort: sort results by relevance or date
    :param sr: direct hire only or include staffing agencies
    :param limit: number of results, 0-25
    :param fromage: number of days to search
    :param start: index of beginning search result
    :param userip: ip of client (required)
    :param useragent: user agent of client (required)
    """
    params = {'q': what,
              'l': where,
              'sort': 'date',
              'sr': 'directhire',
              'limit': 25,
              'fromage': 365,
              'start': 0,
              'userip': "1.2.3.4",
              'useragent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, \
                            like Gecko) Chrome/48.0.2564.82 Safari/537.36"
              }
    return params


def indeed_urls(parameters):
    """Use Indeed publisher ID in order to gain access to the API. With
    parameters from indeed_paramters(), return a list of job application links."""
    client = IndeedClient('7458209865285883')
    response = client.search(**parameters)
    urls = [str(links['url']) for links in response['results']]
    return urls


def find_apply_button(button_name):
    """Searches page for the apply now button and clicks it if it exists."""
    driver.find_element_by_class_name(button_name).click()


def switch_frames(frame_name):
    """The job application is inside a nested frame. In order to navigate to
    the application, each frame must be selected."""
    wait = WebDriverWait(driver, 10)
    frame = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, frame_name)))
    driver.switch_to.frame(frame)
    wait.until(EC.frame_to_be_available_and_switch_to_it(0))


def fill_application(cv):
    """There are two application types: one that requires a full name and one
    that requires a first and last name. A try/except is used to identify which
    is used."""
    job_title = driver.find_element_by_class_name("jobtitle").text
    company = driver.find_element_by_class_name("jobcompany").text
    print("Applying for: {} at {}".format(job_title, company))
    try:
        driver.find_element_by_id('applicant.name').send_keys("{} {}" .format(FIRST_NAME, LAST_NAME))
        driver.find_element_by_id('applicant.email').send_keys(EMAIL_ADDRESS)
        driver.find_element_by_id('resume').send_keys(os.path.abspath(cv))
    except (NoSuchElementException, ElementNotVisibleException):
        driver.find_element_by_id('applicant.firstName').send_keys(FIRST_NAME)
        driver.find_element_by_id('applicant.lastName').send_keys(LAST_NAME)
        driver.find_element_by_id('applicant.email').send_keys(EMAIL_ADDRESS)
        driver.find_element_by_id('resume').send_keys(os.path.abspath(cv))


def apply_or_continue():
    """There are two types of apply methods: one applies after
    clicking the apply button, and the other applies after clicking the
    continue button and answering some questions. A try/except is used
    again here to identify which is used."""
    try:
        driver.find_element_by_id('apply').click()
        driver.implicitly_wait(1)
        print('Application Successful.')
    except (NoSuchElementException, ElementNotVisibleException):
        driver.find_element_by_link_text('Continue').click()
        driver.implicitly_wait(1)
        for radio_button in driver.find_elements_by_xpath('//*[@type="radio" and @value="0"]'):
            radio_button.click()
        driver.find_element_by_id('apply').click()
        driver.implicitly_wait(1)
        print('Application Successful.')
    finally:
        driver.switch_to.window(driver.window_handles[0])


def main():
    user_parameters = indeed_parameters(JOB_DESCRIPTION, JOB_LOCATION)
    count = 0
    while count < 2:
        for url in indeed_urls(user_parameters):
            driver.get(url)
            try:
                find_apply_button('indeed-apply-button')
                switch_frames('iframe[name$=modal-iframe]')
                fill_application(RESUME)
                apply_or_continue()
            except (NoSuchElementException, ElementNotVisibleException):
                pass
        user_parameters['start'] += 25
        count += 1
