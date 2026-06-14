import pyautogui
import pyperclip
import subprocess
import time
import os

# ==========================================
# CONFIG
# ==========================================

CONTACT_NAME = "Imesh"

IMAGE_1 = r"C:\Users\Kavinda\Pictures\grafana.png"
IMAGE_2 = r"C:\Users\Kavinda\Pictures\dashboard.png"

MESSAGE = "No critical alerts"

SEARCH_IMG = "search.png"
ATTACH_IMG = "attach.png"

# ==========================================
# FUNCTIONS
# ==========================================

def wait_for_image(image, timeout=30, confidence=0.8):
    start = time.time()

    while time.time() - start < timeout:
        location = pyautogui.locateCenterOnScreen(
            image,
            confidence=confidence
        )

        if location:
            return location

        time.sleep(1)

    return None


def paste_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


# ==========================================
# OPEN WHATSAPP
# ==========================================

print("Opening WhatsApp...")

try:
    subprocess.Popen("whatsapp:")
except:
    print("Please open WhatsApp Desktop manually.")

time.sleep(8)

# ==========================================
# SEARCH CONTACT
# ==========================================

print("Finding search box...")

search = wait_for_image(SEARCH_IMG)

if not search:
    raise Exception(
        "Could not find search box. "
        "Create search.png screenshot."
    )

pyautogui.click(search)

time.sleep(1)

pyautogui.hotkey("ctrl", "a")
pyautogui.press("backspace")

paste_text(CONTACT_NAME)

time.sleep(2)

pyautogui.press("enter")

print("Opened chat.")

time.sleep(2)

# ==========================================
# SEND FIRST IMAGE
# ==========================================

for image_file in [IMAGE_1, IMAGE_2]:

    attach = wait_for_image(ATTACH_IMG)

    if not attach:
        raise Exception(
            "Could not find attach button. "
            "Create attach.png screenshot."
        )

    pyautogui.click(attach)

    time.sleep(1)

    paste_text(os.path.abspath(image_file))

    pyautogui.press("enter")

    time.sleep(3)

    pyautogui.press("enter")

    print("Sent:", image_file)

    time.sleep(2)

# ==========================================
# SEND MESSAGE
# ==========================================

paste_text(MESSAGE)

time.sleep(1)

pyautogui.press("enter")

print("Message sent.")

print("Completed successfully.")