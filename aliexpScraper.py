from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time


def extract_group_links(driver):
    '''
    This function extracts group links from an AliExpress store.
    '''

    print(f'[PROCESS]: Executing Extraction function.')
    print(f'[INFO]: Inside Extraction function title text says = {driver.title}')

    print(f'[PROCESS]: Waiting for the elements to load.') 
    # Caution: The element selector argument is a tuple.
    WebDriverWait(driver, timeout=20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sub-group-item a"))
    )
    print(f'[INFO]: Wait is over, Either timeout or elements are loaded.')

    pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Record the starting time
    start = datetime.datetime.now()

    print(f'[PROCESS]: Scrolling to the bottom of the page')
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # wait to load page
        time.sleep(pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height: # which means end of page
            break
        # update the last height
        last_height = new_height

    print(f'[INFO]: Scrolled to the bottom of the page.')

    # Record the end time, then calculate and print the total time
    end = datetime.datetime.now()
    delta = end-start
    print("[INFO] Total time taken to scroll till the end {}".format(delta))


    # Extract sub-group tags
    print(f'[PROCESS]: Extracting link elements within sub-group-item class.')
    sub_gp_tags = driver.find_elements_by_css_selector(".sub-group-item a")
    print(f'[INFO]: Extracted link elements successfully.')

    # Extract all anchor tags
    # link_tags = driver.find_elements_by_tag_name('a')

    print(f'[PROCESS]: Extracting link text from link elements.')
    # Create an emply list to hold all the urls for the sub groups
    sub_gp_links = []

    # Extract the urls of only the images from each of the tag WebElements
    for tag in sub_gp_tags:
        sub_gp_links.append(tag.get_attribute('href'))
    print(f'[INFO]: Extracted link text from link elements successfully.')

    print(f'[PROCESS]: Printing Extracted links.')
    for link in sub_gp_links:
        print(link)
    print(f'[INFO]: Print successful.')

    # return(driver)


def aliex_login(driver):
    '''
    This function is used for auto login into aliexpress.
    '''

    login_id = '<your login ID as a string>'
    login_pass = '<your login Password as a string>'
    print(f'[PROCESS]: Executing Login function.')
    print(f'[INFO]: Inside login function title text says = {driver.title}')

    print(f'[PROCESS]: Getting the login box element.')
    # Another method of finding elements: mucho_cheese = driver.find_elements_by_css_selector("#cheese li")
    login_box_element = driver.find_element(By.ID, "fm-login-id")
    print(f'[INFO]: Found login box.')
    print(f'[PROCESS]: Getting the password box element.')
    password_box_element = driver.find_element(By.ID, "fm-login-password")
    print(f'[INFO]: Found password box.')
    print(f'[PROCESS]: Getting the login button element.')
    login_button_element = driver.find_element_by_css_selector(".fm-button")
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

    
def main():

    # AliExpress Landing Page:
    land_link ='https://best.aliexpress.com/?lan=en'


    # Url for AliExpress Store. [Wavgat store here]
    store_front_url = 'https://wavgat.aliexpress.com/store/1962508?spm=a2g0o.cart.0.0.24e93c00fOj6Lo'
    store_all_pro_url = 'https://wavgat.aliexpress.com/store/all-wholesale-products/1962508.html?spm=a2g0o.store_home.pcShopHead_12386176.99'
    # Group links to collect: We have to collect all the links like 
    # that from above link to navigate to grouped data(products list).
    arduino_group_url = 'https://wavgat.aliexpress.com/store/group/Arduino/1962508_511996385.html?spm=2114.12010612.8148362.6.272d581eQA0jIE&origin=n&SortType=orders_desc&g=y'
    amp_group_url = 'https://wavgat.aliexpress.com/store/group/Amplifier-module/1962508_511996399.html?spm=2114.12010615.0.0.5e694362c0Osl0'



    # Initializing web driver for firefox with maximized window.
    print(f'[PROCESS]: Initializing web driver for firefox.')
    driver = webdriver.Firefox()
    print(f'[INFO]: Started Firefox in a new window.')
    print(f'[PROCESS]: Maximizing firefox window.')
    driver.maximize_window()
    print(f'[INFO]: Firefox window maximized.')
    print(f'[PROCESS]: Requesting desired URL.')
    driver.get(store_all_pro_url)
    print(f'[INFO]: Request completed.')
    display_url = driver.current_url
    print(f'[INFO]: Displayed URL is = {display_url}')

    if display_url == store_all_pro_url:
        # Start collecting links.
        print(f'[INFO]: Displayed URL matches the Store URL provided')
        extract_group_links(driver)
    
    elif 'login' in display_url:
        # Login URL Example = https://login.aliexpress.com/
        # First login and then collect links.
        print(f'[INFO]: Hit the login page')
        aliex_login(driver)
        print(f'[INFO]: Title text outside function says = {driver.title}')

        print(f'[PROCESS]: Waiting for the product page.')
        WebDriverWait(driver, timeout=20).until(EC.url_to_be(store_all_pro_url))
        print(f'[INFO]: Wait is over, Either timeout or found desired URL.')

        print(f'[PROCESS]: Checking current URL.')
        if driver.current_url == store_all_pro_url:
            print(f'[INFO]: Currently browsing the products page of the given store.')
            extract_group_links(driver)
        else:
            print(f'[ERROR]: Current URL doesn\'t seem to resemble the desired one.')
            print(f'[LOG]: Display Title = {driver.title}')
            print(f'[LOG]: Current URL = {driver.current_url}')



if __name__ == "__main__":
    main()
