from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time


class AliScraper():

    def __init__(self):
        '''
        Initializing firefox webdriver with maximized window.
        '''
    
        print(f'[PROCESS]: Initializing web driver for firefox.')
        self.driver = webdriver.Firefox()
        print(f'[INFO]: Started Firefox in a new window.')
        print(f'[PROCESS]: Maximizing firefox window.')
        self.driver.maximize_window()
        print(f'[INFO]: Firefox window maximized.')

    def request_url(self, url):
        '''
        Request the specified URL. The request here is explicit so the browser will not 
        execute the further commands untill page finished loading.
        '''
        print(f'[PROCESS]: Requesting desired URL = {url}.')
        self.driver.get(url)
        print(f'[INFO]: Request completed.')

        print(f'[PROCESS]: Verifing the URL.')
        
        if self.matches_current_url(url):
            print(f'[INFO]: Request successfully completed')
            print(f'[INFO]: Displayed URL is = {self.get_current_url()}')
            return True
        else:
            print(f'[ERROR]: Could not fetch the given URL.')
            print(f'[LOG]: Displayed URL is = {self.get_current_url()}')
            return False

    def is_login_url(self):
        '''
        Checks if current URL is for loign page.
        '''

        current_url = self.get_current_url()
        if 'login' in current_url:
            print(f'[INFO]: Hit the login page.')
            return True
        else:
            print(f'[INFO]: No match for login page')
            print(f'[INFO]: Displayed URL is = {self.get_current_url()}')
            return False

    def matches_current_url(self, url):
        '''
        Checks if given URL matches the current URL.
        '''

        current_url = self.get_current_url()
        if current_url == url:
            print(f'[INFO]: Current URL perfectly matches: {url}')
            return True
        else:
            print(f'[INFO]: No match for given URL: {url}')
            print(f'[INFO]: Displayed URL is = {self.get_current_url()}')
            return False
    
    def in_current_url(self, str_check):
        '''
        Checks if given string is present in the current URL.
        '''

        current_url = self.get_current_url()
        if str_check in current_url:
            print(f'[INFO]: Current URL contains: {str_check}')
            return True
        else:
            print(f'[INFO]: No match for given string {str_check}')
            print(f'[INFO]: Displayed URL is = {self.get_current_url()}')
            return False
    
    def get_current_url(self):
        '''
        Retrieves the current URL.
        '''

        return(self.driver.current_url)

    def aexp_login(self, login_id, login_pass):
        '''
        AliExpress Specific login.
        Caveat: Can't distinguish between successful login and and unsuccessful one, So no return statement.
        '''
        print(f'[INFO]: Executing the Login sequence.')

        print(f'[PROCESS]: Getting the login box element.')
        # Another method of finding elements: mucho_cheese = driver.find_elements_by_css_selector("#cheese li")
        login_box_element = self.driver.find_element(By.ID, "fm-login-id")
        print(f'[INFO]: Found login box.')
        print(f'[PROCESS]: Getting the password box element.')
        password_box_element = self.driver.find_element(By.ID, "fm-login-password")
        print(f'[INFO]: Found password box.')
        print(f'[PROCESS]: Getting the login button element.')
        login_button_element = self.driver.find_element_by_css_selector(".fm-button")
        print(f'[INFO]: Found login button.')

        print(f'[PROCESS]: Typing login ID.')
        login_box_element.send_keys(login_id)
        print(f'[INFO]: Login ID typed successfully.')
        print(f'[PROCESS]: Typing Password.')
        # Enter password and perform "ENTER" keyboard action
        # No need to locate the login button and press it.
        password_box_element.send_keys(login_pass + Keys.ENTER)
        print(f'[INFO]: Password typed successfully.')
        print(f'[PROCESS]: Logging In.')
        login_button_element.click()
        print(f'[INFO]: Logged In successfully.')

        print(f'[MESSAGE]: The browser would redirect to the page you have previously requested.')
        # return(driver)
    
    def wait_for_css_element(self, css_selector: str, timeout = None):
        '''
        Waits untill the elements of given css selector loads.
        '''
        # Default time out = 20 seconds.
        if timeout == None:
            timeout = 20

        print(f'[PROCESS]: Waiting for \'{css_selector}\' elements to load.')
        # Caution: The element selector argument is a tuple.
        WebDriverWait(self.driver, timeout=timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        print(f'[INFO]: Wait is over, Either timeout or elements are loaded.')

    def extract_group_links(self):
        '''
        This function extracts group links from an AliExpress store.
        Returns: Links to the subgroups.
        '''

        print(f'[PROCESS]: Executing Extraction function.')

        pause_time = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # Record the starting time
        start = datetime.datetime.now()

        print(f'[PROCESS]: Scrolling to the bottom of the page')
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait to load page
            time.sleep(pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height: # which means end of page
                break
            # update the last height
            last_height = new_height

        print(f'[INFO]: Scrolled to the bottom of the page.')

        # Record the end time, then calculate and print the total time
        end = datetime.datetime.now()
        delta = end-start
        print("[INFO] Total time taken to scroll till the end {}".format(delta))


        # Extract sub-group-item class elements
        print(f'[PROCESS]: Extracting link elements within sub-group-item class.')
        sub_gp_element_list = self.driver.find_elements_by_css_selector(".sub-group-item a")
        print(f'[INFO]: Extracted link elements successfully.')

        # Extract all anchor tags
        # link_tags = driver.find_elements_by_tag_name('a')

        print(f'[PROCESS]: Extracting link text from link elements.')
        # Create an emply list to hold all the urls for the sub groups
        sub_gp_links = []

        # Extract the urls of only the images from each of the tag WebElements
        for tag in sub_gp_element_list:
            sub_gp_links.append(tag.get_attribute('href'))
        print(f'[INFO]: Extracted link text from link elements successfully.')

        print(f'[PROCESS]: Printing Extracted links.')
        for link in sub_gp_links:
            print(link)
        print(f'[INFO]: Print successful.')

        return(sub_gp_links)
    
    # def extract_product_info(self):


def main() -> None:
    '''
    Driver code.
    '''
    store_url = 'https://wavgat.aliexpress.com/store/all-wholesale-products/1962508.html?spm=a2g0o.store_home.pcShopHead_12386176.99'
    log_in_id = 'your_login_id'
    log_in_pass = 'your_login_password'
    ffx_driver = AliScraper()
    ffx_driver.request_url(store_url)

    if ffx_driver.is_login_url():
        # Auto-login
        ffx_driver.aexp_login(log_in_id, log_in_pass)
        # Wait for page to load, Default timeout 20 sec.
        ffx_driver.wait_for_css_element(".sub-group-item a")
        # Check for the redirected URL
        if ffx_driver.matches_current_url(store_url):
            # Extract Group links
            ffx_driver.extract_group_links()

    elif ffx_driver.matches_current_url(store_url):
        ffx_driver.extract_group_links()

    else:
        print(f'Bad URL.')
        print(f'Displayed URL is : {ffx_driver.get_current_url()}')


if __name__ == "__main__":
    main()
