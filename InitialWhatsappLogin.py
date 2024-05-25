import pathlib
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask

app = Flask(__name__)

def initial_login():
    script_directory = pathlib.Path().absolute()
    service = Service(ChromeDriverManager().install())  # Update with the path '/path/to/chromedriver' when hosting
    options = webdriver.ChromeOptions()
    if platform.system() == "Windows":
        user_data_dir = f"user-data-dir={script_directory}\\userdata"
    else:
        user_data_dir = f"user-data-dir={script_directory}/userdata"
    options.add_argument(user_data_dir)  # Save session data
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://web.whatsapp.com')
    time.sleep(30)  # Wait for manual QR code scanning and login

    print("Login successful. You can close this browser window.")
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