from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from utils.email_utils import send_404_report

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.seesight-tours.com/tours")

cards_xpath = '//*[@id="feature_experiences_cards"]/div/a'
product_h1_xpath = '//div[contains(@class,"justify-between")]//h1'

# Store 404 products here
not_found_products = []
coming_soon_products = []

see_more = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//h2[text()='See More']"))
)
see_more.click()

elements = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, cards_xpath))
)

print("Total products:", len(elements))

for i in range(len(elements)):

    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, cards_xpath))
    )

    product = elements[i]
    listing_title = product.find_element(By.XPATH, './/h2').text.strip()
    print("\nListing title:", listing_title)

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", product)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(product)).click()

    try:
        product_page_title = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, product_h1_xpath))
        ).text.strip()
    except TimeoutException:
        print(f"❌ 404 Page Detected: {listing_title}")
        not_found_products.append(listing_title)   # Save 404 product
        driver.back()

        see_more = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//h2[text()='See More']"))
        )
        see_more.click()
        continue

    product_page_url = driver.current_url
    print("Product page URL:", product_page_url)
    print("Product page title:", product_page_title)

    if listing_title == product_page_title:
        print("Title matched ✔")
    else:
        print("Title NOT matched ❌")

    try:
        coming_soon = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, '//p[text()="Coming Soon"]'))
        )
        print(f"⚠️ Product '{listing_title}' is Coming Soon")
        coming_soon_products.append(listing_title)
    except TimeoutException:
        # If element not found, ignore
        pass

    driver.back()

    see_more = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//h2[text()='See More']"))
    )
    see_more.click()

# -------- Final 404 Report --------
# print("\n================= 404 PRODUCTS REPORT =================")
# print(f"Total 404 Products: {len(not_found_products)}")
# for item in not_found_products:
#     print("•", item)
# print("======================================================")

# Send email if there are 404 products or Coming Soon products
if not_found_products or coming_soon_products:
    send_404_report(not_found_products, coming_soon_products)
    print("Report email sent successfully.")
else:
    print("No 404 or Coming Soon products found. No email sent.")

