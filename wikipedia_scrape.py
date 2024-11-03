# import the necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import os
import pandas as pd

#  Create undetectable driver instance
Service = Service(r'C:\Program Files\WebDrivers\chromedriver.exe')
Options = webdriver.ChromeOptions()
Options.add_argument("--headless=new")
Options.add_argument("start-maximized")
Options.add_experimental_option("excludeSwitches", ["enable-automation"])
Options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=Service, options=Options)
url = (
    f'https://en.wikipedia.org/wiki/'
    f'List_of_U.S._state_and_territory_abbreviations'
)
wait = WebDriverWait(driver, 30)


def open_browser(url: str) -> None:
    """
    A function that is responsible for opening the web browser
    """
    driver.get(url)


def main(a: int, b: int) -> None:
    """
    Function responsible for the scraping scraping web data and storing
    the data as a csv file.

    Args:
        a: Intenger
        The integer value from which the random wait time will begin
        from

        B: Integer
        The integer value of which the random wait time could end from

    Return:
        None
    """
    open_browser(url)
    time.sleep(random.randint(a, b))

    state_codes_df = table_scrape()

    dirname = os.path.dirname(__file__)
    filename = 'state_codes.csv'
    file = os.path.join(dirname, filename)
    state_codes_df.to_csv(file)


def table_scrape() -> pd.DataFrame:
    """
    Function responsible for obtaining web data from a table and
    storing that web table as a pandas dataframe oject

    Returns: Dataframe
    Returns a dataframe of the information scraped from the table on
    the webpage.
    """
    name_of_region = driver.find_elements(
        By.XPATH,
        f'//table[@class="wikitable sortable jquery-tablesorter"]'
        f'/tbody/tr/td[1]/a'
    )

    try:
        region_status = driver.find_elements(
            By.XPATH,
            f'//table[@class="wikitable sortable jquery-tablesorter"]'
            f'/tbody/tr/td[2]'
        )
    except ValueError:
        region_status = driver.find_elements(
            By.XPATH,
            f'//table[@class="wikitable sortable jquery-tablesorter"]'
            f'/tbody/tr/td[2]/a'
        )

    state_code = driver.find_elements(
        By.XPATH,
        f'//table[@class="wikitable sortable jquery-tablesorter"]'
        f'/tbody/tr/td[4]'
    )

    # Use list comprehension to store the text attributes of each
    # webElement.
    name_of_region = [region.text for region in name_of_region]
    region_status = [status.text for status in region_status]
    state_code = [code.text for code in state_code]

    # Remove the 'U.S. Armed Forces because from the source, the column
    # and row combinaton showed to have two values.
    name_of_region.remove('U.S. Armed Forces')

    dct = {
        'region': name_of_region,
        'status': region_status,
        'code': state_code
    }

    df = pd.DataFrame(dct)

    return df


if __name__ == "__main__":
    main(3, 5)
    time.sleep(10)
    driver.close()
