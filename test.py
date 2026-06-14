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
driver.set_window_size(1920, 1080)

# ==================================
# DASHBOARD URLS
# ==================================

sniper_url = (
    "your_sniper_url"
)

grafana_url = (
    "your_grafana_url"
)

# ==================================
# OPEN TABS ONCE
# ==================================

driver.get(sniper_url)

driver.execute_script(
    f"window.open('{grafana_url}', '_blank');"
)

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
        print(text[:500])

        print("\nFULL OCR TEXT:")
        print(text)

        # Healthy state
        if "no critical servers" in text:
            return False

        # Explicit critical detection
        if "critical" in text:
            return True

        # OCR uncertain -> treat as alert
        return True

    except Exception as e:
        print(f"OCR Error: {e}")

        # OCR failed -> treat as alert
        return True


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

        driver.switch_to.window(driver.window_handles[0])

        time.sleep(3)

        driver.save_screenshot("sniper_full.png")

        img = Image.open("sniper_full.png")

        cropped = img.crop((225, 75, 1710, 355))

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

        driver.switch_to.window(driver.window_handles[1])

        time.sleep(5)

        driver.save_screenshot("grafana.png")

        print("Saved grafana.png")

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

        
