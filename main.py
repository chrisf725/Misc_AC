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

# pyautogui.moveTo(window.left + 459, window.top + 279)

# plat_train_response = input("Do you want to platinum train? (yes/no/y/n): ").strip().lower()

# if plat_train_response not in ["yes", "y", "no", "n"]:
#     print("Invalid input. Please restart the script and enter 'yes', 'no', 'y', or 'n'.")
#     exit()

# plat_train = plat_train_response == "yes" or plat_train_response == "y"
# print(f"Platinum train: {plat_train}")

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

print("Right click on the object you want to search for")
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

        for coord in click_coordinates:
            # Move the mouse to the search object and click
            pyautogui.moveTo(window.left + coord[0], window.top + coord[1])
            time.sleep(1)
            pyautogui.mouseDown(window.left + coord[0], window.top + coord[1])
            time.sleep(0.01)
            pyautogui.mouseUp()
            print(f"Clicked at ({coord[0]}, {coord[1]})")

            time.sleep(4)

            # Define the region to check for the color of the enemy rarity
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
                result_color_2 = get_pixel_color(window.left + 459, window.top + 279)

                # pyautogui.moveTo(window.left + 272, window.top + 122)
                # Continue script if crit is common
                # End script if crit is rare and above
                if color == (98, 98, 98): # Grey
                    print(result_color_2)
                    time.sleep(1)
                    pyautogui.mouseDown(window.left + 328, window.top + 621)
                    time.sleep(0.01)
                    pyautogui.mouseUp()
                    time.sleep(1)
                    # pyautogui.moveTo(window.left + 459, window.top + 279)
                    # time.sleep(1)
                    
                    if result_color_2 == (255, 255, 255) and result_color == (107, 138, 19): 
                        time.sleep(1)
                        # Click continue on results screen
                        pyautogui.mouseDown(window.left + 574, window.top + 591)
                        time.sleep(0.01)
                        pyautogui.mouseUp()
                        exit()
                        break
                    if result_color_2 == (94, 108, 126):
                        time.sleep(1)
                        # Click continue on results screen
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