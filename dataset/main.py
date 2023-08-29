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


def main():
    data_file = f'./data_dell.txt'
    web_url = "https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88" \
              "%DA%A9-laptop/b/39/dell-%D8%AF%D9%84/ "
    count = 24

    opts, _ = getopt(sys.argv[1:], 'o:l:c:', ["output=", "web_url=", "count="])
    for opt, arg in opts:
        if opt in ('-o', '--output'):
            data_file = arg
        elif opt in ('-l', '--web_url'):
            web_url = arg
        elif opt in ('-c', '--count'):
            count = int(arg)

    extract(data_file=data_file, web_url=web_url, count=count)


def extract(data_file, web_url, count):
    feed = open(data_file, 'x', encoding='utf-8')
    link_file = f'./get_link_dell.txt'
    feed2 = open(link_file, 'x', encoding='utf-8')
    # Options for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Start the driver.
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 3)

    # loading the page
    driver.get(web_url)

    cards_per_page = 24
    count -= 1
    count = max(count, 1)
    max_retries = 20
    current_retires = 0
    i = 1
    while i <= count // cards_per_page + 1:
        expected_card_count = i * cards_per_page
        # print('waiting for total of', expected_card_count)

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


def api(input_file):
    # Replace with the path to your input file
    output_file = "output.txt"  # Replace with the desired output file path
    base_url = "https://api.torob.com/v4/base-product/details-log-click/?prk="

    with open(input_file, "r") as f:
        links = f.read().splitlines()

    results = []

    for link in links:
        match = re.search(r"/([a-f0-9-]+)/", link)
        if match:
            prk = match.group(1)
            url = base_url + prk

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                min_price = data.get("min_price", "")
                attributes = data.get("attributes", "")

                result = f"Link: {link}\nmin_price: {min_price}\nattributes: {attributes}\n"
                results.append(result)

    with open(output_file, "w") as f:
        f.writelines(results)

    print("Extraction complete. Results written to", output_file)


if __name__ == "__main__":
    main()
