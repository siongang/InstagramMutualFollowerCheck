from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from lxml import html
import utils
import log


from time import sleep
html_element=None
# program waits for html to render
# returns the div that encapsulates following users to html content 
def save_html_content(driver):
    global html_element
    try:
        print("trying to find aano")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_aano"))
        )
        html_element = driver.find_element(By.CLASS_NAME, "_aano")

        sleep(3)

        html_element_div = html_element.find_element(By.XPATH, ".//div[1]")
        html_content = html_element_div.get_attribute("outerHTML") 
        return(html_content)
    except TimeoutException:
        print("could not find _aano")


# returns a list of the users that the client is following
def find_following_list(html_content):
    tree = html.fromstring(html_content)
    user_list=[]
    users = tree.xpath("//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']")   
    for user in users:
       user_list.append(user.text_content())
    return user_list

# search for username in list
def search_client(username, user_list):
    return username in user_list

