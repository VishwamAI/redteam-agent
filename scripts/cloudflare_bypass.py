from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import os

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
service = Service("/usr/local/bin/chromedriver")

# Use Xvfb to run Chrome in a virtual display environment
xvfb_command = [
    "xvfb-run",
    "--auto-servernum",
    "--server-args=-screen 0 1920x1080x24",
    "chromedriver",
]
xvfb_process = subprocess.Popen(
    xvfb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

# Set the DISPLAY environment variable to use the Xvfb display
os.environ["DISPLAY"] = ":99"

driver = None
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to the picoCTF practice page
    driver.get("https://play.picoctf.org/practice")

    # Take a screenshot before waiting for the Cloudflare challenge to be bypassed
    driver.save_screenshot("/home/ubuntu/screenshots/before_wait.png")

    # Increase the wait time for the Cloudflare challenge to be bypassed
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[text()='picoGym Practice Challenges']")
        )
    )

    # Interact with the page as needed
    # Example: Print the page title
    print(driver.title)

    # Additional interaction: Print the page source
    print(driver.page_source)

finally:
    # Close the browser if it was successfully created
    if driver:
        driver.quit()
    # Terminate the Xvfb process
    xvfb_process.terminate()
