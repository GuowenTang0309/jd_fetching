from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time

# 1. Set the user-data-dir path
user_data_dir = Path("./chrome_user_data").resolve()

# 2. Chrome options
opts = Options()
opts.add_argument(f"--user-data-dir={user_data_dir}")
opts.add_argument("--window-size=1280,1000")
# ❌ DO NOT set headless here
# ✅ Optional: use a custom profile directory to avoid conflicts
opts.add_argument("--profile-directory=Default")  

# 3. Launch browser
driver = webdriver.Chrome(options=opts)

# 4. Open LinkedIn login page
driver.get("https://www.linkedin.com/login")

print("👉 Please log in manually in the opened Chrome window.")
print("✅ Once you're logged in and see your homepage, close the window or press Ctrl+C here.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("🔒 Login session saved. You can now reuse this profile in your scraper.")

driver.quit()
