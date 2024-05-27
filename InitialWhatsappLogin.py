import pathlib
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask

app = Flask(__name__)

def find_element_exists(driver, xpath):
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print("Element found and page loaded successfully.")
        return True
    except TimeoutException:
        print("Page did not load properly or element was not found.")
        driver.quit()
        return False

def click_button(driver, xpath):
    if find_element_exists(driver, xpath):
        login_button = driver.find_element(By.XPATH, xpath)
        time.sleep(5)
        login_button.click()

def initial_login():
    script_directory = pathlib.Path().absolute()
    service = Service(ChromeDriverManager().install())  # Update with the path '/path/to/chromedriver' when hosting
    options = webdriver.ChromeOptions()
    if platform.system() == "Windows":
        user_data_dir = f"user-data-dir={script_directory}\\userdata"
    else:
        user_data_dir = f"user-data-dir={script_directory}/userdata"
    options.add_argument(user_data_dir)  # Save session data
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://web.whatsapp.com')
    
    # Click on "Link with phone number"
    xpath_login_button = '//span[@tabindex="0"]'
    find_element_exists(driver, xpath_login_button)
    click_button(driver, xpath_login_button)

    # Find if phone number input field exists
    xpath_number_input = '//input[@class="selectable-text x1n2onr6 xy9n6vp x1n327nk xh8yej3 x972fbf xcfux6l x1qhh985 xm0m39n xjbqb8w x1uvtmcs x1jchvi3 xss6m8b xexx8yu x4uap5 x18d9i69 xkhd6sd"]'
    find_element_exists(driver, xpath_number_input)

    # Find the input field by ID, name, XPath, or any other locator method
    input_field = driver.find_element(By.XPATH, xpath_number_input) 

    # Clear existing text in the input field (optional)
    time.sleep(5)
    input_field.click()     # Click on the input number field
    driver.execute_script("arguments[0].select();", input_field)    # Select all. When we send number it will overwrite the selected values ie everything.
    # Send new input to the input field
    input_field.send_keys("+918450837773")

    # Click on "Next" buton
    xpath_next_button = '//button[@class="x889kno x1a8lsjc xbbxn1n xxbr6pl x1n2onr6 x1rg5ohu xk50ysn x1f6kntn xyesn5m x1z11no5 xjy5m1g x1mnwbp6 x4pb5v6 x178xt8z xm81vs4 xso031l xy80clv x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x1v8p93f xogb00i x16stqrj x1ftr3km x1hl8ikr xfagghw x9dyr19 x9lcvmn xbtce8p x14v0smp xo8ufso xcjl5na x1k3x3db xuxw1ft xv52azi"]'
    find_element_exists(driver, xpath_next_button)
    click_button(driver, xpath_next_button)

    # Locate the element which provides the code
    time.sleep(5)
    xpath_code = '//div[@aria-details="link-device-phone-number-code-screen-instructions"]'
    element = driver.find_element(By.XPATH, xpath_code)

    # Get the value of the data-link-code attribute
    data_link_code = element.get_attribute("data-link-code")

    # Print the value
    print("data-link-code value:", data_link_code)
    
    time.sleep(45)  # Wait for entering code on phone and login
    
    driver.quit()

@app.route('/')
def home():
    return """
    <h1>Login Page!</h1>
    <p>This is some text that will be displayed below the header.</p>
    """

initial_login()

if __name__ == "__main__":
    app.run()