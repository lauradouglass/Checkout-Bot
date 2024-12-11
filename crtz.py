from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Configure options for headless browsing
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")

# Initialize WebDriver
service = Service('path_to_chromedriver')  
driver = webdriver.Chrome(service=service, options=options)

# Shopify-specific setup
cart_url = "https://www.crtz.xyz/cart"

try:
    driver.get(cart_url)
    time.sleep(1)  # Wait for the page to load

    checkbox = driver.find_element(By.ID, "effectiveAppsAgreeCB")
    checkbox.click()  # Check the box
    time.sleep(0.5)  # Short wait for the action to register

    verify_button = driver.find_element(By.XPATH, "//button[@type='button' and @value='Verifying']")
    verify_button.click()
    time.sleep(1)  # Short wait for verification

    WebDriverWait(driver, 10).until(EC.url_contains("/checkouts"))

    checkout_url = driver.current_url
    print("Checkout URL:", checkout_url)

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("kvng.laura@gmail.com") 
    email_input.send_keys(Keys.RETURN)  # Submit the email field

    verification_code_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identity-verification-code"))
    )

    # Prompt user for the verification code
    verification_code = input("Please enter the verification code sent to your phone: ")

    verification_code_input.send_keys(verification_code)

    pay_now_button = driver.find_element(By.XPATH, "//button[span[text()='Pay now']]")
    pay_now_button.click()

    time.sleep(2)

finally:
    driver.quit()
