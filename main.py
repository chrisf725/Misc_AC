import pyautogui
import pygetwindow as gw
from pynput import mouse
import time
from PIL import Image
import keyboard

# Get the window
try:
    window = gw.getWindowsWithTitle('Miscrits')[0]
    print(f"Window width: {window.width}")
    print(f"Window height: {window.height}")
except IndexError:
    print('Window not found')
    exit()

window.activate()

# Store coordinates of search object
click_coordinates = []


def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.right:
        if window.left <= x <= window.right and window.top <= y <= window.bottom:
            # Calculate relative coordinates
            relative_x = x - window.left
            relative_y = y - window.top
            print(f"Right click at ({relative_x}, {relative_y})")
            # Store coordinates
            click_coordinates.append((relative_x, relative_y))
            # Stop listener after first right click
            return False
        else:
            print("Right click outside the window")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

def get_pixel_color(x, y):
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color

time.sleep(3)
print(f"Click coordinates: {click_coordinates}")

try:
    while True:
        if keyboard.is_pressed('q'):
            print("Exiting...")
            break

        # Check if the coordinates are valid
        for coord in click_coordinates:

            pyautogui.moveTo(window.left + coord[0], window.top + coord[1])
            time.sleep(1)
            pyautogui.mouseDown(window.left + coord[0], window.top + coord[1])
            time.sleep(0.01)
            pyautogui.mouseUp()
            print(f"Clicked at ({coord[0]}, {coord[1]})")

            time.sleep(4)

            # Define the region to check for the color
            # check_x = window.left + 740
            # check_y = window.top + 53
            enemy_rarity_x = int(window.width * 0.633)
            enemy_rarity_y = int(window.height * 0.077)
            check_x = window.left + enemy_rarity_x
            check_y = window.top + enemy_rarity_y

            color = get_pixel_color(check_x, check_y)
            print(f"Color at ({check_x}, {check_y}): {color}")
            pyautogui.moveTo(check_x, check_y)
            time.sleep(1)

            while True:
                if keyboard.is_pressed('q'):
                    print("Exiting...")
                    break

                result_color = get_pixel_color(window.left + 272, window.top + 122)
                # pyautogui.moveTo(window.left + 272, window.top + 122)
                if color == (98, 98, 98): # Grey
                    print("Common")
                    time.sleep(1)
                    pyautogui.mouseDown(window.left + 328, window.top + 621)
                    time.sleep(0.01)
                    pyautogui.mouseUp()
                    
                    if result_color == (107, 138, 19): # Green
                        time.sleep(1)
                        pyautogui.mouseDown(window.left + 574, window.top + 591)
                        time.sleep(0.01)
                        pyautogui.mouseUp()
                        break
                else:
                    print("Not common")
                    break
            break
except KeyboardInterrupt:
    print("Program interrupted by user")




# window.move(0, 0)
# time.sleep(3)
# pyautogui.moveTo(window.left + 100, window.top + 100)

# window.minimize()
# time.sleep(3)
# window.restore()