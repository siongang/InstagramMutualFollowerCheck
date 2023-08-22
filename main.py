from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import utils
import log
import parse_following
import os
from time import sleep

# INITIALIZATION
driver = webdriver.Chrome()
utils.start_web(driver)

# LOGGING IN
# if user didnt log in before, login.
# if already logged in, then continue with user inputted username
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    log.login(driver)

except TimeoutException:
    print("we are logged in")
    input = input('input username to continue or reset() to log into a different account')
    
    if input == "reset()":
        utils.reset()
        sleep(3)
        utils.start_web(driver)
        log.login(driver)
    else:
        log.username = input
    # need to error trap wrong username input


# AFTER LOGGING IN
print("log in successful")


'''
After logging in, save cookies. Then go to client's following page.
Save the html content of the following page.
Scrape and extract all the users that the client follow.
Check if users follow back.
'''
# save cookies (for login credentials)
utils.save_cookie(driver)


# go to following
driver.get(f"https://www.instagram.com/{log.username}/following/")

# html content for client's following page
client_content = parse_following.save_html_content(driver)
# scroll the following page all the way to load all the accounts
utils.scroll_down(driver, parse_following.html_element)
# html content for client's following page
client_content = parse_following.save_html_content(driver)

# save html content to file
file_path = "html_content.html"
utils.save_file(client_content, file_path)

# list of users that the client follows
following_list = parse_following.find_following_list(client_content)

# dictionary that stores whether follow is mutual or not
mutual_dict = {}

# CHECK IF USER FOLLOWS BACK
# iterate through each user 
# load respective instagram link
# check the user's following data and see if client is in there
# update mutual_dict 
for user in following_list:
    driver.get(f"https://www.instagram.com/{user}/following/")
    temp_html_content = parse_following.save_html_content(driver)
    temp_following_list = parse_following.find_following_list(temp_html_content)

    if parse_following.search_client(user, temp_following_list) is True:
        mutual_dict[user] = True
    else:
        mutual_dict[user] = False


# output
print(mutual_dict)

    
driver.quit()