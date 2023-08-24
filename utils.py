import os
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from time import sleep


def start_web(driver):
    print("start web")
    # set domain to instagram
    driver.get("https://www.instagram.com/")
    # load cookies for login credentials
    add_cookie(driver)
    # load instagram again with cookies
    driver.get("https://www.instagram.com/")


def reset(driver):
     # Specify the path to the cookies.pkl file
    cookies_file_path = 'InstagramMutualFollowerCheck/cookies.pkl'
    # Check if the cookies.pkl file exists
    if os.path.exists(cookies_file_path):
        # Delete the cookies.pkl file
        os.remove(cookies_file_path)
        print("cookies.pkl file deleted.")
    else:
        print("cookies.pkl file does not exist.")
    
    driver.delete_all_cookies()


def confirm_button(driver):
    # confirm button
    try:
        confirm_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_acap"))
        )
        confirm_button.click()
        print("Confirm button clicked")
    except TimeoutException:
        print("Confirm button was not clickable within the timeout.")


# load cookies for login credentials
def add_cookie(driver):
    try:
        if os.path.getsize('InstagramMutualFollowerCheck/cookies.pkl') != 0:
            with open('InstagramMutualFollowerCheck/cookies.pkl', 'rb') as file:
                cookies = pickle.load(file)
                print("Loaded cookies:", cookies)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except:
        with open('InstagramMutualFollowerCheck/cookies.pkl','wb') as file:
            pass



# Save cookies to a file
def save_cookie(driver):
    cookies = driver.get_cookies()
    with open('InstagramMutualFollowerCheck/cookies.pkl', 'wb') as file:
        pickle.dump(cookies, file)

def delete(driver, text):
    text.send_keys(Keys.CONTROL + "a")
    text.send_keys(Keys.DELETE)
        


def save_file(content, file_path):
    # clear file first
    # then write html_content onto it
    with open(file_path, "w", encoding="utf-8"):
        pass  # An empty pass statement to ensure the file is truncate
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"HTML content saved to {file_path}")



# Function to scroll down the page to load more content
def scroll_down(driver, parent_div):
    child_div_list = []
 
    med_div = parent_div.find_element(By.XPATH, ".//div[1]")
 
    prev_len = -1
    sleep(5)
    while True:   
        # Scroll down within the div
        driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", parent_div, 800)

        # Find the current child div elements
        current_child_divs = med_div.find_elements(By.XPATH, ".//div")

        # Append the current child div elements to the list
        child_div_list.extend(current_child_divs)

        # Check if new content has been loaded
        current_len = len(current_child_divs)
        print(current_len)
        
        if current_len == prev_len:
            break  # No more new content

        sleep(2)

        prev_len = current_len
