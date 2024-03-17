from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrap_toad_and_toad(search_query: str):
    # Setup the web driver (assuming Chrome and correct chromedriver is installed)
    driver = webdriver.Chrome()

    try:
        # Navigate to the page
        driver.get('https://www.trollandtoad.com')

        # Wait for the search bar to be ready and perform a search
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-words"))
        )
        search_bar.clear()
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".row.mt-1.list-view"))
        )

        # Wait a bit for all elements to load

        product_divs = driver.find_elements(By.CSS_SELECTOR, ".product-col")

        results = []

        for div in product_divs:
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

        # Print or process the results as needed
        for result in results:
            print(result)
            pass

    finally:
        # Clean up by closing the browser window
        driver.quit()
