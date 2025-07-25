from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from pathlib import Path
import os

class SeleniumJobScraper:
    def __init__(self, headless: bool = True):
        chromedriver_path = Path("chromedriver").resolve()
        opts = Options()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")

        # ✅ Use dedicated Chrome user data directory to avoid conflict
        user_data_dir = Path("./chrome_user_data").resolve()
        opts.add_argument(f"--user-data-dir={user_data_dir}")

        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=opts)

    def fetch_detail(
        self, url: str, timeout: int = 30
    ) -> tuple[str | None, str | None]:
        d = self.driver

        try:
            d.set_page_load_timeout(timeout + 40)  
            d.get(url)
            print(">>> Navigated to:", url)
            time.sleep(1)
        except TimeoutException:
            print(f"⏰ Page load timeout: {url}")
            return None, None
        except Exception as e:
            print(f"❌ Exception during d.get(): {e}")
            return None, None

        # ───── description ─────
        try:
            see_more = WebDriverWait(d, timeout).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@aria-label='Click to see more description' or "
                    "contains(@class,'jobs-description__footer-button')]"
                ))
            )
            d.execute_script("arguments[0].click();", see_more)
        except TimeoutException:
            pass  # not fatal

        try:
            WebDriverWait(d, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))
            )
            description = d.find_element(
                By.CLASS_NAME, "show-more-less-html__markup"
            ).text.strip()
        except Exception:
            description = ""       

        # ───── apply link ─────
        apply_link = ""
        try:
            APPLY_LOCATOR = (
                By.XPATH,
                "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/"
                "div/div/div/div[6]/div/div/div/button",
            )
            btn = WebDriverWait(d, timeout).until(
                EC.element_to_be_clickable(APPLY_LOCATOR)
            )
            original_window = d.current_window_handle
            original_url = d.current_url
            d.execute_script("arguments[0].click();", btn)
            time.sleep(2)

            new_tabs = [w for w in d.window_handles if w != original_window]
            if new_tabs:
                d.switch_to.window(new_tabs[0])
                apply_link = d.current_url
                d.close()
                d.switch_to.window(original_window)
            else:
                if d.current_url != original_url:
                    apply_link = d.current_url
                elif d.find_elements(
                    By.CSS_SELECTOR,
                    "div.jobs-easy-apply-modal, div[role='dialog'][data-test-modal='easy-apply']",
                ):
                    apply_link = "Easy Apply (modal)"
        except Exception as e:
            ts = int(time.time())

        return description, apply_link


    def close(self):
        self.driver.quit()
