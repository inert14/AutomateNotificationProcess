import pywhatkit as kit
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import schedule
import time

def open_whatsapp_web():
    script_directory = pathlib.Path().absolute()
    service = Service()  # Update with the path '/path/to/chromedriver' when hosting
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={script_directory}\\userdata")  # Use saved session data
    #options.add_argument('--headless')  # Run in headless mode for server environments
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://web.whatsapp.com')
    time.sleep(15)  # Wait for WhatsApp Web to load completely
    driver.quit()

def send_message(phone_number, message):
    open_whatsapp_web()  # Ensure WhatsApp Web is open with session loaded
    kit.sendwhatmsg_instantly(phone_number, message, 30, tab_close=True)

# Schedule the message sending
def schedule_message(phone_number, message, hour, minute):
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(send_message, phone_number, message)

# Example usage
phone_number = '+918450937773'
message = 'Hello, this is a test message!'
hour, minute = 22, 52  # Send message at 10:30

schedule_message(phone_number, message, hour, minute)

while True:
    schedule.run_pending()
    time.sleep(1)