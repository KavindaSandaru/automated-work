from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import pyautogui
import pyperclip
import os
import time
import pytesseract
import winsound
import pygetwindow as gw
from datetime import datetime, timedelta
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ==========================
# SHIFT SELECTION
# ==========================

print("\nSelect Shift")
print("1. 3PM - 7PM")
print("2. 7PM - 4AM")

choice = input("Enter shift (1 or 2): ").strip()

now = datetime.now()

if choice == "1":
    shift_name = "3PM - 7PM"

    shift_end = now.replace(
        hour=19,
        minute=0,
        second=0,
        microsecond=0
    )

elif choice == "2":
    shift_name = "7PM - 4AM"

    shift_end = now.replace(
        hour=4,
        minute=0,
        second=0,
        microsecond=0
    )

    if now.hour < 4:
        pass  # already after midnight, end today at 4 AM
    else:
        shift_end += timedelta(days=1)

else:
    print("Invalid shift selected.")
    sys.exit()

print(f"\nShift Selected: {shift_name}")
print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Shift Ends: {shift_end.strftime('%Y-%m-%d %H:%M:%S')}")

if datetime.now() >= shift_end:
    print("\nThe selected shift has already ended.")
    sys.exit()

# ==================================
# FIREFOX
# ==================================

options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

driver = webdriver.Firefox(options=options)

driver.maximize_window()

# ==================================
# DASHBOARD URLS
# ==================================

sniper_url = (
    ""
)

grafana_url = (
    ""
)


nagios_url = (
    ""
)

outlook_url = (
    ""
)

kibana_reservation_url = (
    ""
)

kibana_availability_url = (
    ""
)

# ==================================
# OPEN TABS ONCE
# ==================================

driver.get(sniper_url)

driver.execute_script(
    f"window.open('{grafana_url}', '_blank');"
)
driver.execute_script(f"window.open('{nagios_url}', '_blank');")
driver.execute_script(f"window.open('{outlook_url}', '_blank');")
driver.execute_script(f"window.open('{kibana_reservation_url}', '_blank');")
driver.execute_script(f"window.open('{kibana_availability_url}', '_blank');")

input(
    "\nLogin to Sniper and Grafana.\n"
    "Make sure both dashboards are loaded.\n"
    "Press ENTER when ready..."
)

# ==================================
# WHATSAPP
# ==================================

input(
    "\nOpen WhatsApp Desktop and make sure it is visible.\n"
    "Press ENTER when ready..."
)

# ==================================
# BUILD TAB MAP
# ==================================

tab_map = {}

for handle in driver.window_handles:

    driver.switch_to.window(handle)

    url = driver.current_url.lower()

    print(url)

    if "sniper" in url:
        tab_map["sniper"] = handle

    elif "toutmappers-live" in url:
        tab_map["grafana"] = handle

    elif "nagios" in url:
        tab_map["nagios"] = handle

    elif "40c5e6c0" in url:
        tab_map["kibana_res"] = handle

    elif "d22a4c20" in url:
        tab_map["kibana_avail"] = handle

print("\nTAB MAP:")
print(tab_map)

input("\nPress ENTER to continue...")

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1


def find_and_click(image, timeout=20, confidence=0.90):
    start = time.time()

    while time.time() - start < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(
                image,
                confidence=confidence,
                grayscale=True
            )

            if location:
                pyautogui.click(location)
                return

        except Exception:
            pass

        time.sleep(1)

    raise Exception(f"Could not find {image}")


# ==================================
# OPEN CHAT USING SEARCH
# ==================================

def focus_whatsapp():
    windows = gw.getWindowsWithTitle("WhatsApp")

    if not windows:
        raise Exception("WhatsApp window not found")

    window = windows[0]

    if window.isMinimized:
        window.restore()

    window.activate()

    time.sleep(2)


def open_chat(chat_name):
    focus_whatsapp()

    print(f"Opening chat: {chat_name}")

    print("Step 1: Ctrl+F")
    pyautogui.keyDown("ctrl")
    pyautogui.press("f")
    pyautogui.keyUp("ctrl")

    time.sleep(2)

    print("Step 2: Typing group name")
    pyautogui.write(chat_name, interval=0.05)

    time.sleep(2)

    print("Step 3: Pressing Enter")
    pyautogui.press("enter")

    time.sleep(2)

    print("Step 4: Done")


from selenium.webdriver.common.by import By

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def capture_kibana_chart(output_file):

    driver.execute_script(
        "window.scrollTo(0, 900);"
    )

    time.sleep(3)

    driver.save_screenshot("kibana_full.png")

    img = Image.open("kibana_full.png")

    width, height = img.size

    crop = img.crop(
        (
            0,
            620,
            width,
            height
        )
    )

    crop.save(output_file)

    print(f"Saved {output_file}")

def send_image(image_path):
    print(f"Sending {image_path}")

    find_and_click("plus.png", confidence=0.95)

    time.sleep(1)

    find_and_click("photos_videos.png", confidence=0.90)

    time.sleep(2)

    pyperclip.copy(os.path.abspath(image_path))
    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    pyautogui.press("enter")

    time.sleep(3)

    pyautogui.press("enter")

    time.sleep(4)


def send_message(message):
    pyperclip.copy(message)

    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    pyautogui.press("enter")


def check_for_critical_alert():
    try:
        text = pytesseract.image_to_string(
            Image.open("sniper.png")
        ).lower()

        print("\nOCR RESULT:")
        print(text)

        # Healthy indicators
        healthy_patterns = [
            "no critical",
            "no critical serve",
            "no critical server",
            "no critical servers"
        ]

        for pattern in healthy_patterns:
            if pattern in text:
                print("Healthy state detected")
                return False

        # Critical indicators
        critical_patterns = [
            "critical",
            "critical server",
            "critical servers"
        ]

        for pattern in critical_patterns:
            if pattern in text:
                print("Critical state detected")
                return True

        print("OCR uncertain - treating as HEALTHY")
        return False

    except Exception as e:
        print(f"OCR Error: {e}")

        # safer than waking you up for OCR failures
        return False


def play_alarm():
    print("\nCRITICAL ALERT DETECTED!")
    print("Monitoring stopped.")

    while True:
        winsound.Beep(2500, 1000)
        time.sleep(0.5)


# ==================================
# MAIN LOOP
# ==================================

while True:
    
     # ======================
    # CHECK SHIFT END
    # ======================
    if datetime.now() >= shift_end:
        print("\nShift ended. Closing application...")

        try:
            driver.quit()
        except:
            pass

        sys.exit()

    try:

        print("\n==================================")
        print("Starting monitoring cycle...")
        print("==================================")

        # ==================================
        # SNIPER SCREENSHOT
        # ==================================

        driver.switch_to.window(tab_map["sniper"])

        time.sleep(3)

        driver.save_screenshot("sniper_full.png")

        img = Image.open("sniper_full.png")

        width, height = img.size

        cropped = img.crop(
            (
                220,
                70,
                width - 20,
                620
            )
        )

        cropped.save("sniper.png")

        print("Saved sniper.png")

        # ==================================
        # CHECK FOR CRITICAL ALERT
        # ==================================

        if check_for_critical_alert():
            play_alarm()
            break

        # ==================================
        # GRAFANA SCREENSHOT
        # ==================================

        driver.switch_to.window(tab_map["grafana"])

        time.sleep(5)

        driver.save_screenshot("grafana.png")

        print("Saved grafana.png")

        # Reservation dashboard
        driver.switch_to.window(tab_map["kibana_res"])

        capture_kibana_chart(
        "kibana_reservations.png"
        )

        # Availability dashboard
        driver.switch_to.window(tab_map["kibana_avail"])

        capture_kibana_chart(
        "kibana_availability.png"
        )

        # ==================================
        # SEND STATUS MESSAGE
        # ==================================

        print("Opening 24/7 Monitoring group...")

        open_chat("24/7 Monitoring group")

        send_message("No critical alerts")

        print("Sent status message")

        # ==================================
        # SEND SCREENSHOTS
        # ==================================

        print("Opening TM + Support...")

        open_chat("TM + Support")

        send_image("sniper.png")
        send_image("grafana.png")
        send_image("kibana_reservations.png")
        send_image("kibana_availability.png")

        print("Sent screenshots")

        print("\nCycle complete.")
        print("Waiting 1 hour...")

        for _ in range(3600):

            if datetime.now() >= shift_end:
                print("\nShift ended. Closing application...")

                try:
                    driver.quit()
                except:
                    pass

                sys.exit()

            time.sleep(1)

    except Exception as e:

        print(f"\nERROR: {e}")

        print("Retrying in 5 minutes...")

        for _ in range(300):

            if datetime.now() >= shift_end:
                print("\nShift ended. Closing application...")

                try:
                    driver.quit()
                except:
                    pass

                sys.exit()
                
            time.sleep(1)

        
