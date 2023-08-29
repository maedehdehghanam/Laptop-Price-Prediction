from getopt import getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import sys
import datetime
import re
import requests


def extract(feed_file, start_url, count):
    feed = open(feed_file, 'x', encoding='utf-8')
    link_file = f'./get_link_microsoft.txt'
    feed2 = open(link_file, 'x', encoding='utf-8')
    # Options for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Start the driver.
    print('starting the driver')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 3)

    print('loading the page')
    driver.get(start_url)

    cards_per_page = 24
    count -= 1
    count = max(count, 1)
    max_retries = 20
    current_retires = 0
    i = 1
    while i <= count // cards_per_page + 1:
        expected_card_count = i * cards_per_page
        print('waiting for total of', expected_card_count)

        try:
            wait.until(ec.presence_of_element_located(
                (By.CSS_SELECTOR, f'.cards > .jsx-2514672dc9197d80:nth-child({expected_card_count})')))
            current_retires = 0
        except TimeoutException:
            print('timeout exception')
            i -= 1
            current_retires += 1
            if current_retires == max_retries:
                print('maximum retries reached')
                # Close the feed file and quit the driver
                feed.close()
                driver.quit()
                break

        print('scrolling down')
        driver.execute_script('window.scrollBy(0, 1000)')
        i += 1

    elements = driver.find_elements(By.CSS_SELECTOR, '.jsx-2514672dc9197d80 > a')
    for e in elements:
        match = re.search(r"/([a-f0-9-]+)/", e.get_attribute('href'))
        url = "https://api.torob.com/v4/base-product/details-log-click/?prk=" + match.group(1)

        response = requests.get(url)

        if response.status_code == 200:  # Successful response
            data = response.json()  # Parse the JSON response

            # Extract "min_price" and "attributes" from the JSON data
            min_price = data.get("min_price", "")
            attributes = data.get("attributes", "")

            # Print the extracted values
            feed2.write(e.get_attribute('href'))
            feed2.write('\n')
            feed.write(str(min_price))
            feed.write(str(attributes))
            feed.write('\n')

        else:
            print("Error:", response.status_code)
    feed.close()
    driver.quit()


now = datetime.datetime.now().timetuple()
feed_file = f'./data_microsoft.txt'
start_url = "https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9" \
            "-laptop/b/13/microsoft-%D9%85%D8%A7%DB%8C%DA%A9%D8%B1%D9%88%D8%B3%D8%A7%D9%81%D8%AA/ "
count = 24

opts, _ = getopt(sys.argv[1:], 'o:l:c:', ["output=", "start_url=", "count="])
for opt, arg in opts:
    if opt in ('-o', '--output'):
        feed_file = arg
    elif opt in ('-l', '--start_url'):
        start_url = arg
    elif opt in ('-c', '--count'):
        count = int(arg)

extract(feed_file=feed_file, start_url=start_url, count=count)

