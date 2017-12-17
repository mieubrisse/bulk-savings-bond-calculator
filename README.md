# Bulk Savings Bond Value Calculator

Very simple Python script for querying [the US Treasury savings bond calculator website](https://www.treasurydirect.gov/BC/SBCPrice) in bulk.

## Getting Started

1. Use Python 3+
2. `brew install chromedriver` to install headless Chrome driver
3. `pip install selenium` to install the Python bindings for the headless driver
4. Build a CSV file of bond information of the form `FACE_VALUE,ISSUE_DATE` where ISSUE_DATE is in MMYYYY format (e.g. `50,051992` for a $50 bond issued in May, 1992)
5. Run `chromedriver` to start the driver
5. `python calculate.py $YOUR_CSV_FILE` to submit all bond information to the website
6. Switch to the new Chrome process started by the script for information about each bond and totals
