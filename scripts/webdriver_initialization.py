from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import os

def initialize_webdriver():
    try:
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--user-data-dir=/tmp")

        # Set up the Chrome driver
        service = Service('/usr/local/bin/chromedriver')

        # Use Xvfb to run Chrome in a virtual display environment
        xvfb_command = ["xvfb-run", "--auto-servernum", "--server-args=-screen 0 1920x1080x24", "chromedriver"]
        xvfb_process = subprocess.Popen(xvfb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Set the DISPLAY environment variable to use the Xvfb display
        os.environ["DISPLAY"] = ":99"

        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver, xvfb_process

    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None, None

def main():
    driver, xvfb_process = initialize_webdriver()
    if driver:
        try:
            # Navigate to a website to test the setup
            driver.get("https://www.example.com")

            # Print the page title to confirm successful navigation
            print(driver.title)

        finally:
            # Close the browser
            driver.quit()
            # Terminate the Xvfb process
            xvfb_process.terminate()

if __name__ == "__main__":
    main()
