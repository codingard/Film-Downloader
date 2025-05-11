import json
import time
import undetected_chromedriver as uc
from logger import logger

def get_driver_with_logs():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    return uc.Chrome(options=options)

def extract_m3u8_links(url):
    logger.info("🌐 Launching Chrome and opening the page...")
    driver = get_driver_with_logs()
    driver.get(url)
    time.sleep(10)
    logger.info("📡 Scanning network logs for .m3u8 links...")
    logs = driver.get_log("performance")
    m3u8_links = []
    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
            if message["method"] == "Network.requestWillBeSent":
                req_url = message["params"]["request"]["url"]
                if ".m3u8" in req_url and req_url not in m3u8_links:
                    m3u8_links.append(req_url)
        except Exception:
            continue
    driver.quit()
    return m3u8_links
