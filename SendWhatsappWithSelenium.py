import pathlib
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = 'path/to/chromedriver'

# Function to send a message using the browser session with Selenium
def send_message(phone_no, message):
    script_directory = pathlib.Path().absolute()
    service = Service(ChromeDriverManager().install())
    if platform.system() == "Windows":
        user_data_dir = f"user-data-dir={script_directory}\\userdata"
    else: 
        user_data_dir = f"user-data-dir={script_directory}/userdata"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(user_data_dir) # Use saved session data
    driver = webdriver.Chrome(service=service, options=options)
   
    try:
        # Directly interact with the page to send the message
        # Open chat with the given phone number using WhatsApp Web's direct URL scheme
        url = f'https://web.whatsapp.com/send?phone={phone_no}&text={message}'
        print(url)
        driver.get(url)
        
        # Wait until the send button is present
        try:
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-tab="11"]'))
            )
        except TimeoutException:
            print("Page did not load properly or element was not found.")
            driver.quit()
            return

        send_button = driver.find_element(By.XPATH, '//button[@data-tab="11"]')
        send_button.click()
        
        time.sleep(5)  # Wait to ensure the message is sent

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    driver.quit()

# Example usage to send a message
# send_message('+918450937773', 'Hello, this is a test message!')