from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from sys import platform
from time import sleep
import numpy as np
import pickle

class SeleniumScraper():
    def __init__(self, url, driverPath='drivers/chromedriverLinux64', wait_time='default'):
        self.driverPath = driverPath if platform != "darwin" else 'drivers/chromedriverMac64'
        self.base_url = url
        self.wait_time = wait_time if wait_time != 'default' else abs(
            np.random.normal(7, 2, size=(1,)).item())

    def session(func):
        def wrapper(self, *args):
            options = Options()
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = Chrome(service=Service(self.driverPath),options=options)
            self.wait = WebDriverWait(self.driver, self.wait_time)
            self.driver.maximize_window()
            self.driver.get(f'{self.base_url}/login?')
            self.signIn()
            data = func(self, *args)
            self.driver.quit()
            return data
        return wrapper

    def login(self, username, password):
        def wrapper():
            self.driver.find_element(By.ID, "username").send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.XPATH, '//*[@class="btn__primary--large from__button--floating"]').click()
            sleep(3)
            self.save_cookie()
        self.signIn = wrapper

    def save_cookie(self, path='cookies.pkl'):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path='cookies.pkl'):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             self.driver.add_cookie(cookie) 

    def get_elem(self, xpath, driver=None):
        driver = driver if driver != None else self.driver
        try:
            elem = driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            elem = None
        return elem

    def get_elem_text(self, xpath, driver=None):
        driver = driver if driver != None else self.driver
        try:
            elem = driver.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            elem = None
        return elem

    def get_elems(self, parent_items, xpaths, parent_name):
        items = {}
        for index, item in enumerate(parent_items):
            elems = {}
            for elem in xpaths:
                elems.update(
                    {elem: self.get_elem_text(xpaths[elem], driver=item)})
            items.update({f"{parent_name}_{index+1}": elems})
        return items

    def get_elem_item(self, parent, item_index):
        try:
            item = parent[item_index].text
        except IndexError:
            item = None
        return item

    def handle_redirected(func):
        def wrapper(self, user):
            self.load_cookie()
            self.driver.get(user)
            self.load_cookie()
            # Check if the url was redirected
            user_url = user if user[-1]=='/' else user+'/'
            if self.driver.current_url == user_url:
                profile = func(self, user)
            else:
                try:
                    self.driver.find_element_by_css_selector('.main__sign-in-link').click()
                    self.signIn()
                    profile = func(self, user)
                except:
                    profile = func(self, user)
            return profile
        return wrapper

    @handle_redirected
    def get_profile(self, user):
        # clicking buttons
        try:
            # wait for element to be clickable
            more_tab = self.get_elem('//*[contains(text(), "more experience")]')
            more_tab.click()
            other_tab = self.get_elem('//*[@id="ember512"]/div/span/button')
            other_tab.click()
        except AttributeError:
            pass

        # get main variables
        exps = self.driver.find_elements(
            By.XPATH, '//*[@class="pv-entity__position-group-pager pv-profile-section__list-item ember-view"]')
        schools = self.driver.find_elements(
            By.XPATH, '//*[@class="pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view"]')
        licenses = self.driver.find_elements(
            By.XPATH, '//*[@class="pv-profile-section__sortable-item pv-certification-entity ember-view"]')
        volunteer = self.driver.find_elements(
            By.XPATH, '//*[@class="pv-profile-section__list-item pv-volunteering-entity pv-profile-section__card-item ember-view"]')
        skills = self.driver.find_elements(
            By.XPATH, '//span[@class="pv-skill-category-entity__name-text t-16 t-black t-bold"]')

        exps_xpaths = {
            'exp_positions': './/h3[@class="t-16 t-black t-bold"]',
            'exp_companies': './/p[@class="pv-entity__secondary-title t-14 t-black t-normal"]',
            'exp_years': './/span[text()="Dates Employed"]//following::span[1]',
            'exp_durations': './/span[text()="Employment Duration"]/following::span[1]'
        }

        schools_xpaths = {
            'school_names': './/h3[@class="pv-entity__school-name t-16 t-black t-bold"]',
            'degree_name': './/span[text()="Degree Name"]//following::span[1]',
            'study_field': './/span[text()="Field Of Study"]//following::span[1]',
            'grade': './/span[text()="Grade"]//following::span[1]',
            'school_years': './/span[text()="Dates attended or expected graduation"]//following::span[1]',
            'activities': './/span[text()="Activities and Societies:"]//following::span[1]'
        }

        licenses_xpaths = {
            'licenses': './/h3[@class="t-16 t-bold"]',
            'issue_date': './/span[text()="Issued date and, if applicable, expiration date of the certification or license"]//following::span[1]',
            'issue_authority': './/span[text()="Issuing authority"]//following::span[1]'
        }

        profile = {
            # left header
            'name': self.get_elem_text('//*[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]'),
            'job_title': self.get_elem_text('//*[@class="text-body-medium break-words"]'),
            'small_bio': self.get_elem_text('//*[@class="text-body-small t-black--light break-words pt1"]'),
            'loc': self.get_elem_text('//*[@class="text-body-small inline t-black--light break-words"]'),

            # right header
            'cur_comp': self.get_elem_text('//*[@aria-label="Current company"]'),
            'educ': self.get_elem_text('//*[@aria-label="Education"]'),

            # experiences
            'experiences': self.get_elems(exps, exps_xpaths, 'company'),

            # schools
            'schools': self.get_elems(schools, schools_xpaths, 'university'),

            # licenses
            'licenses': self.get_elems(licenses, licenses_xpaths, "license"),

            # about
            'about': self.get_elem_text('//*[@class="pv-profile-section pv-about-section artdeco-card p5 mt4 ember-view"]'),
            'skills': self.get_elem_item(skills, 0), 

            # the html of the entire page
            "profile_html":self.driver.page_source
        }
        return profile

    @session
    def scrape_profiles(self, users):
        profiles = []
        for user in users:
            profile = self.get_profile(user)
            profiles.append(profile)
        return profiles
