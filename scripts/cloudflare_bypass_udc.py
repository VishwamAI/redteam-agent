import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_undetected_webdriver():
    try:
        # Set up undetected Chrome options for headless mode
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-first-run")
        options.add_argument("--user-data-dir=/tmp")

        # Initialize undetected Chrome driver
        driver = uc.Chrome(options=options)
        return driver

    except Exception as e:
        print(f"Error initializing undetected WebDriver: {e}")
        return None


def main():
    driver = initialize_undetected_webdriver()
    if driver:
        try:
            # Navigate to the picoCTF practice page
            driver.get("https://play.picoctf.org/practice")

            # Wait for the Cloudflare challenge to be bypassed
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "challenge-success-text"))
            )

            # Interact with the page as needed
            # Example: Print the page title
            print(driver.title)

            # Additional interaction: Print the page source
            print(driver.page_source)

        finally:
            # Close the browser
            driver.quit()


if __name__ == "__main__":
    main()
