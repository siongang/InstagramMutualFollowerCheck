from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import utils

username = None

# logging in to instagram
def login(driver):
    global username
    global password
    global two_auth_code
    global username_input
    global password_input
    
    # username
    username = input("enter username")
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys(username)
    print("Username input successful!")

    # password
    password = input("enter password")
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    print("Password input successful!")

    utils.confirm_button(driver)

    # if verification page opens, go to auth_code()
    # if it doesnt, check if it is still in the login page.
    # if so, try login again
    # if not, webdriver is logged in
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "verificationCode"))
        )
        auth_code(driver)


    except TimeoutException:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            print ("Did not load")
            utils.delete(driver, username_input)
            utils.delete(driver, password_input)
            login(driver)
        except TimeoutException:
            print("logged in")
        

from time import sleep
# backup code for testing: 65731029
def auth_code(driver):
    # two factor authentication // need to figure out if there is authentication or not
    two_auth_code = input("enter code")
    auth_input = driver.find_element(By.NAME, "verificationCode")
    auth_input.send_keys(two_auth_code)
    print("auth input successful!")

    utils.confirm_button(driver)
    sleep(10)
    # check if still in verification page. then redo verification
    # else, continue
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "verificationCode"))
        )
        utils.delete(driver, auth_input)
        auth_code(driver)

    except TimeoutException:
        print("we are logged in")

