from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import csv
import sys

# Timeout in seconds to wait for any given action to complete
_WEB_TIMEOUT = 15

_TREASURY_URL = "https://www.treasurydirect.gov/BC/SBCPrice"

def submit_bond(browser, value, issue_date):
    issue_date_elem = browser.find_element(by=By.NAME, value="IssueDate")
    issue_date_elem.clear()
    issue_date_elem.send_keys(issue_date)
    Select(browser.find_element(by=By.NAME, value="Denomination")).select_by_value(value)
    browser.find_element(by=By.NAME, value="btnAdd.x").click()

browser = webdriver.Chrome()
browser.maximize_window()
browser.implicitly_wait(_WEB_TIMEOUT)
browser.get(_TREASURY_URL)

if not sys.argv[1]:
    print("Error: Provide a CSV containing tuples of (bond value, bond issue date) where issue date is in 'MMYYYY' format")
    sys.exit(1)
input_filepath = sys.argv[1]

with open(input_filepath) as fp:
    csv_reader = csv.reader(fp)
    for row in csv_reader:
        submit_bond(browser, row[0], row[1])

browser.find_element(by=By.NAME, value="btnAll.x").click()

print("Done!")
