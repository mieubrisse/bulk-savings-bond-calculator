from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv
import sys
import os
import shutil

# Timeout in seconds to wait for any given action to complete
_WEB_TIMEOUT = 15
_TREASURY_URL = "https://www.treasurydirect.gov/BC/SBCPrice"

def submit_bond(browser, value, issue_date):
    wait = WebDriverWait(browser, 10)  # Wait up to 10 seconds if needed

    # Wait for the issue date input field to be available
    issue_date_elem = wait.until(expected_conditions.presence_of_element_located((By.NAME, "IssueDate")))
    issue_date_elem.clear()
    issue_date_elem.send_keys(issue_date)

    # Wait for the dropdown and select the bond value
    denomination_dropdown = wait.until(expected_conditions.presence_of_element_located((By.NAME, "Denomination")))
    Select(denomination_dropdown).select_by_value(value)

    # Wait for the add button and click it
    add_button = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "btnAdd.x")))
    add_button.click()

    # Wait for the page reload before continuing
    wait.until(expected_conditions.staleness_of(add_button))  # Ensure previous page is gone

# Locate installed Chrome and ChromeDriver
chromedriver_path = shutil.which("chromedriver")

if not chromedriver_path:
    raise Exception("No Chromedriver found!")

service = Service(chromedriver_path)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(service=service, options=options)

browser.maximize_window()
browser.implicitly_wait(_WEB_TIMEOUT)
browser.get(_TREASURY_URL)

# Determine input source: file or STDIN
if len(sys.argv) > 1:
    input_filepath = sys.argv[1]
    if not os.path.exists(input_filepath):
        print(f"Error: File '{input_filepath}' does not exist.")
        sys.exit(1)
    input_source = open(input_filepath, newline='', encoding='utf-8')
else:
    print("Reading input from STDIN...")
    input_source = sys.stdin

# Process CSV
csv_reader = csv.reader(input_source)
for row in csv_reader:
    if len(row) != 2:
        print(f"Skipping invalid row: {row}")
        continue
    submit_bond(browser, row[0], row[1])

# Locate table containing output values
try:
    # NOTE: for some reason this (frustratingly) doesn't work in Docker; it just can't find the element
    # Super weird, but it's not worth spending more time on
    table = WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "ta1"))
    )
except TimeoutException:
    print("Error: Table did not load within the timeout period; dumping page source:")

    # Dump the page source for debugging
    print(browser.page_source)

    browser.quit()
    sys.exit(1)

rows = table.find_elements(By.TAG_NAME, "tr")

# Extract values from the second row (index 1)
columns = rows[1].find_elements(By.TAG_NAME, "td")

# Assign values with labels
labels = ["Total Price", "Total Value", "Total Interest", "YTD Interest"]
for label, value in zip(labels, columns):
    print(f"{label}: {value.text}")

# Close file if it was opened from a path
if input_source is not sys.stdin:
    input_source.close()
