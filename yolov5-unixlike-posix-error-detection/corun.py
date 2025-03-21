import pyautogui
import time

# Set delay between clicks (in seconds)
delay = 0.005  # Adjust as needed

# Set number of clicks (1 trillion times)
num_clicks = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

print("Auto-clicker starting in 3 seconds... Move your cursor to the desired position.")
time.sleep(3)

clicks_done = 0
while clicks_done < num_clicks:
    pyautogui.click()
    clicks_done += 1
    time.sleep(delay)
    
    # Stop after a key press (optional)
    if pyautogui.position() == (0, 0):  # Move cursor to top-left to stop
        print("Auto-clicker stopped.")
        break
