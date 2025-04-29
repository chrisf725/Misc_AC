import pyautogui
import pygetwindow as gw
from pynput import mouse
import time
from PIL import Image
import keyboard
import threading

pyautogui.FAILSAFE = True

# Get the window
try:
    window = gw.getWindowsWithTitle('Miscrits')[0]
    print(f"Window width: {window.width}")
    print(f"Window height: {window.height}")
except IndexError:
    print('Window not found')
    exit()

window.activate()

plat_train_response = input("Do you want to platinum train? (yes/no/y/n): ").strip().lower()

if plat_train_response not in ["yes", "y", "no", "n"]:
    print("Invalid input. Please restart the script and enter 'yes', 'no', 'y', or 'n'.")
    exit()

plat_train = plat_train_response == "yes" or plat_train_response == "y"
print(f"Platinum train: {plat_train}")

bypass_rare_response = input("Do you want to ignore rare crits? (yes/no/y/n): ").strip().lower()
if bypass_rare_response not in ["yes", "y", "no", "n"]:
    print("Invalid input. Please restart the script and enter 'yes', 'no', 'y', or 'n'.")
    exit()

bypass_rare = bypass_rare_response == "yes" or bypass_rare_response == "y"
print(f"Ignore rare crits: {bypass_rare}")

# Store coordinates of search object
click_coordinates = []

def smart_sleep(total_time, interval=0.1):
    elapsed = 0
    while elapsed < total_time:
        # If paused, keep waiting (in short increments)
        while paused:
            time.sleep(interval)
        time.sleep(interval)
        elapsed += interval

paused = False
def toggle_pause():
    global paused
    while True:
        if keyboard.is_pressed('p'):
            paused = not paused
            state = "Paused" if paused else "Resumed"
            print(f"{state}...")
            time.sleep(0.5)
        time.sleep(0.1)

pause_thread = threading.Thread(target=toggle_pause, daemon=True)
pause_thread.start()

exit_flag = False
def check_exit():
    global exit_flag
    while not exit_flag:
        if keyboard.is_pressed('q'):
            exit_flag = True
            print("Exiting... 3")
            exit()
            break
        time.sleep(0.1)

exit_thread = threading.Thread(target=check_exit, daemon=True)
exit_thread.start()

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

def click_action(x, y, time_delay):
    pyautogui.mouseDown(window.left + x, window.top + y)
    time.sleep(0.01)
    pyautogui.mouseUp()
    # time.sleep(time_delay)
    smart_sleep(time_delay)

def get_pixel_color(x, y):
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel((x, y))
    del screenshot  # Free up memory
    return pixel_color

def is_blue_pixel(color, blue_threshold=150, other_max=130):
    r, g, b = color
    return b > blue_threshold and r <= other_max and g <= other_max

def is_cyan_pixel(color, cyan_threshold=155, other_max=170):
    r, g, b = color
    return r <= other_max and g > cyan_threshold and b > cyan_threshold

def is_yellow_pixel(color, yellow_threshold=150, other_max=100):
    r, g, b = color
    return r > yellow_threshold and g > yellow_threshold and b <= other_max

def is_dark_grey_pixel(color, target=(46, 57, 69), tolerance=10):
    r, g, b = color
    tr, tg, tb = target
    return abs(r - tr) <= tolerance and abs(g - tg) <= tolerance and abs(b - tb) <= tolerance

print("Right click on the object you want to search for")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

# time.sleep(3)
smart_sleep(3)
print(f"Click coordinates: {click_coordinates}")

try:
    while not exit_flag:
        # check_exit()
        if paused:
            time.sleep(0.1)
            continue

        for coord in click_coordinates:
            # Move the mouse to the search object and click
            pyautogui.moveTo(window.left + coord[0], window.top + coord[1])
            # time.sleep(1)
            smart_sleep(1)
            click_action(coord[0], coord[1], 4)
            print(f"Clicked at ({coord[0]}, {coord[1]})")

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
            # time.sleep(1)
            smart_sleep(1)

            if exit_flag:
                print("Exiting... 2")
                break

            while not exit_flag:
                # check_exit()

                result_color = get_pixel_color(window.left + 272, window.top + 122)
                # result_color_2 = get_pixel_color(window.left + 459, window.top + 279)
                result_color_2 = get_pixel_color(window.left + 446, window.top + 276)

                # pyautogui.moveTo(window.left + 272, window.top + 122)
                # Continue script if crit is common
                # End script if crit is rare and above
                if color == (98, 98, 98) or (bypass_rare and is_blue_pixel(color)): # Grey
                    # check_exit()
                    print("XP bar color: ", result_color_2)
                    # time.sleep(1)
                    smart_sleep(1)
                    click_action(328, 621, 2)
                    # pyautogui.moveTo(window.left + 446, window.top + 276)

                    
                    # pyautogui.moveTo(window.left + 459, window.top + 279)
                    # time.sleep(1)
                    
                    # Check if crit is ready to train
                    if is_yellow_pixel(result_color_2): # and result_color == (107, 138, 19): # White and Green
                        # check_exit()
                        # time.sleep(1)
                        smart_sleep(1)
                        # Click continue on results screen
                        click_action(574, 591, 1)

                        # Click crit to train
                        click_action(301, 65, 1)

                        # Training
                        pyautogui.mouseDown(window.left + 646, window.top + 88) # Train button
                        click_action(646, 88, 1)

                        if plat_train:
                            for i in range(2):
                                # Click platinum train
                                click_action(517, 635, 2) # Platinum train button

                            click_action(581, 639, 1) # Continue button

                            # Click continue again
                            click_action(705, 483, 2) # Second continue button

                            result_color_3 = get_pixel_color(window.left + 464, window.top + 108)
                            print("Evolution", result_color_3)
                            # time.sleep(1)
                            smart_sleep(1)

                            # Check if crit evolved
                            if result_color_3 == (107, 138, 19):
                                # Click continue
                                click_action(580, 598, 1) # Continue button

                            # Exit training
                            click_action(928, 58, 2) # Close button

                            result_color_4 = get_pixel_color(window.left + 593, window.top + 195)
                            print("Rank upgrade", result_color_4)
                            # time.sleep(1)
                            smart_sleep(1)

                            # Close rank upgrade screen
                            if result_color_4 == (107, 138, 19):
                                click_action(589, 511, 1) # Close button
                            
                        else:
                            for i in range(2):
                                # Click continue
                                click_action(711, 639, 1) # Continue button

                            # Click continue again
                            click_action(705, 483, 2) # Second continue button

                            result_color_3 = get_pixel_color(window.left + 464, window.top + 108)
                            print("Evolution", result_color_3)
                            # time.sleep(1)
                            smart_sleep(1)

                            # Check if crit evolved
                            if result_color_3 == (107, 138, 19):
                                # Click continue
                                click_action(580, 598, 1) # Continue button

                            # Exit training
                            click_action(928, 58, 2) # Close button

                            result_color_4 = get_pixel_color(window.left + 593, window.top + 195)
                            print("Rank upgrade", result_color_4)
                            # time.sleep(1)
                            smart_sleep(1)

                            # Close rank upgrade screen
                            if result_color_4 == (107, 138, 19):
                                click_action(589, 511, 1) # Close button
                        break
                    # If crit is not ready to train, continue
                    if is_blue_pixel(result_color_2) or is_dark_grey_pixel(result_color_2) or is_cyan_pixel(result_color_2): # result_color_2 == (94, 108, 126): # Grey
                        # check_exit()
                        # time.sleep(1)
                        smart_sleep(1)
                        # Click continue on results screen
                        click_action(574, 591, 0)
                        break
                else:
                    # check_exit()
                    print("Not common")
                    if is_blue_pixel(color):
                        print("Rare crit")
                    break
            break
except KeyboardInterrupt:
    print("Program interrupted by user")
    exit()
# finally:
#     print("Exiting script...")
#     exit()