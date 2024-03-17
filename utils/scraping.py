import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tempfile import mkdtemp
from enums import Category
from typing import Optional


def scrap_toad_and_toad(search_query: str, category: Optional[str]):

    print("Category: ", category)

    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'

    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    results = []
    driver = None
    try:
        start_time = time.time()  # Start timing
        driver = webdriver.Chrome(service=service,
                                  options=options
                                  )

        # Navigate to the page
        driver.get('https://www.trollandtoad.com')
        navigation_time = time.time()
        print(
            f"Navigation to page took: {navigation_time - start_time:.2f} seconds")

        # Wait for the search bar to be ready and perform a search
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-words")))
        search_bar.clear()
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)
        search_time = time.time()
        print(
            f"Search execution took: {search_time - navigation_time:.2f} seconds")

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".row.mt-1.list-view")))
        results_load_time = time.time()
        print(
            f"Loading search results took: {results_load_time - search_time:.2f} seconds")

        # Extracting information from the products
        product_divs = driver.find_elements(By.CSS_SELECTOR, ".product-col")

        for div in product_divs[:5]:
            try:
                # Extract the card image URL
                card_image_url = div.find_element(
                    By.CSS_SELECTOR, "img.productImage").get_attribute('src')
            except:
                card_image_url = None

            try:
                # Extract the title and link of the product
                title_element = div.find_element(
                    By.CSS_SELECTOR, ".prod-title a")
                title = title_element.text.strip()
                link = title_element.get_attribute('href')
            except:
                title = "No title found"
                link = "No link found"

            buying_options_table = div.find_element(
                By.CSS_SELECTOR, ".buying-options-table")

            all_sellers_info = []

            seller_rows = buying_options_table.find_elements(
                By.CSS_SELECTOR, "div.row")[1:]

            for row in seller_rows:
                seller_img_alt = row.find_element(
                    By.CSS_SELECTOR, "div.col-3.text-center.p-1 img").get_attribute("alt")

                seller_img_url = row.find_element(
                    By.CSS_SELECTOR, "div.col-3.text-center.p-1 img").get_attribute("src"
                                                                                    )
                condition = row.find_element(
                    By.CSS_SELECTOR, "div.col-3.text-center.p-1 + div").text
                # This might need adjustment to accurately capture selected/default quantity
                quantity = row.find_element(
                    By.CSS_SELECTOR, "div.box-quantity select").get_attribute("value")
                price = row.find_element(
                    By.CSS_SELECTOR, "div.col-2.text-center.p-1").text

                seller_info = {
                    "seller": {
                        "name": seller_img_alt,
                        "image": seller_img_url
                    },
                    "condition": condition,
                    "quantity": quantity,
                    "price": price
                }

                all_sellers_info.append(seller_info)
            results.append({
                'title': title,
                'link': link,
                'card_image_url': card_image_url,
                'sellers_info': all_sellers_info
            })

        scraping_end_time = time.time()
        print(
            f"Scraping content took: {scraping_end_time - results_load_time:.2f} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

    total_time = time.time() - start_time
    print(f"Total scraping process took: {total_time:.2f} seconds")
    return results
