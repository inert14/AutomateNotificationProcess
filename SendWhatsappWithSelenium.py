import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = 'path/to/chromedriver'

# Function to send a message using the browser session with Selenium
def send_message(phone_no, message):
    script_directory = pathlib.Path().absolute()
    service = Service()  # Update with the path '/path/to/chromedriver' when hosting
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={script_directory}\\userdata")  # Use saved session data
    driver = webdriver.Chrome(service=service, options=options)
    
    # Directly interact with the page to send the message
    # Open chat with the given phone number using WhatsApp Web's direct URL scheme
    url = f'https://web.whatsapp.com/send?phone={phone_no}&text={message}'
    print(url)
    driver.get(url)

     # Wait until the send button is present
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-tab="11"]'))
        )
    except TimeoutException:
        print("Page did not load properly or element was not found.")
        driver.quit()
        return

    send_button = driver.find_element(By.XPATH, '//button[@data-tab="11"]')
    send_button.click()
    
    time.sleep(5)  # Wait to ensure the message is sent
    driver.quit()

# Run this only the first time to login and save cookies
# login_to_whatsapp()

# Example usage to send a message
# send_message('+918450937773', 'Hello, this is a test message!')