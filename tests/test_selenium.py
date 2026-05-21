import subprocess
import sys
import time

# selenium testing imports
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def start_test_server(port: int = 8001):
    # Start the FastAPI app in a subprocess so Selenium can connect to it.
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    timeout = 15
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(f"http://127.0.0.1:{port}/ui", timeout=1)
            return process
        except requests.RequestException:
            time.sleep(0.5)

    process.kill()
    raise RuntimeError("FastAPI server did not start in time")


def stop_test_server(process: subprocess.Popen):
    # Stop the subprocess started for the app.
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def test_selenium_can_submit_ui_form_and_receive_job_id():
    # Use Selenium to open the UI, submit the form, and verify a job_id is returned.
    server_process = start_test_server(port=8001)

    # Configure Selenium to use headless Chrome for testing.
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )

    try:
        driver.get("http://127.0.0.1:8001/ui")

        # Find the form input and button on the page.
        url_input = driver.find_element(By.ID, "url")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        # Enter a URL and submit the form.
        url_input.send_keys("https://example.com/video")
        submit_button.click()

        time.sleep(1)

        # After submission, the page should contain the JSON response including job_id.
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "job_id" in body_text
    finally:
        driver.quit()
        stop_test_server(server_process)
