import pyautogui
import pygetwindow as gw
from pynput import mouse
import time
from PIL import Image
import keyboard

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

# pyautogui.moveTo(window.left + 459, window.top + 279)

plat_train_response = input("Do you want to platinum train? (yes/no/y/n): ").strip().lower()

if plat_train_response not in ["yes", "y", "no", "n"]:
    print("Invalid input. Please restart the script and enter 'yes', 'no', 'y', or 'n'.")
    exit()

plat_train = plat_train_response == "yes" or plat_train_response == "y"
print(f"Platinum train: {plat_train}")

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

plat_train = plat_train_response == "yes" or plat_train_response == "y"
print(f"Platinum train: {plat_train}")

def get_pixel_color(x, y):
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel((x, y))
    del screenshot  # Free up memory
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
                    
                    # Check if crit is ready to train
                    if result_color_2 == (255, 255, 255) and result_color == (107, 138, 19): # White and Green
                        time.sleep(1)
                        # Click continue on results screen
                        pyautogui.mouseDown(window.left + 574, window.top + 591)
                        time.sleep(0.01)
                        pyautogui.mouseUp()
                        time.sleep(1)

                        # Click crit to train
                        pyautogui.mouseDown(window.left + 301, window.top + 65) # Crit in second slot
                        time.sleep(0.01)
                        pyautogui.mouseUp()
                        time.sleep(1)

                        # Training
                        pyautogui.mouseDown(window.left + 646, window.top + 88) # Train button
                        time.sleep(0.01)
                        pyautogui.mouseUp()
                        time.sleep(1)

                        if plat_train:
                            for i in range(2):
                                # Click platinum train
                                pyautogui.mouseDown(window.left + 517, window.top + 635) # Platinum train button
                                time.sleep(0.01)
                                pyautogui.mouseUp()
                                time.sleep(2)

                            pyautogui.mouseDown(window.left + 581, window.top + 639) # Continue button
                            time.sleep(0.01)
                            pyautogui.mouseUp()
                            time.sleep(1)

                            # Click continue again
                            pyautogui.mouseDown(window.left + 705, window.top + 483) # Second continue button
                            time.sleep(0.01)
                            pyautogui.mouseUp()
                            time.sleep(2)

                            result_color_3 = get_pixel_color(window.left + 464, window.top + 108)
                            print("Evolution", result_color_3)
                            time.sleep(1)

                            # Check if crit evolved
                            if result_color_3 == (107, 138, 19):
                                # Click continue
                                pyautogui.mouseDown(window.left + 580, window.top + 598) # Continue button
                                time.sleep(0.01)
                                pyautogui.mouseUp()
                                time.sleep(1)

                            # Exit training
                            pyautogui.mouseDown(window.left + 928, window.top + 58) # Close button
                            time.sleep(0.01)
                            pyautogui.mouseUp()
                            time.sleep(2)

                            result_color_4 = get_pixel_color(window.left + 593, window.top + 195)
                            print("Rank upgrade", result_color_4)
                            time.sleep(1)

                            # Close rank upgrade screen
                            if result_color_4 == (107, 138, 19):
                                pyautogui.mouseDown(window.left + 589, window.top + 511) # Close button
                                time.sleep(0.01)
                                pyautogui.mouseUp()
                                time.sleep(1)
                            
                        else:
                            for i in range(2):
                                # Click continue
                                pyautogui.mouseDown(window.left + 711, window.top + 639) # Continue button
                                time.sleep(0.01)
                                pyautogui.mouseUp()
                                time.sleep(1)

                            # Click continue again
                            pyautogui.mouseDown(window.left + 705, window.top + 483) # Second continue button
                            time.sleep(0.01)
                            pyautogui.mouseUp()
                            time.sleep(2)

                            result_color_3 = get_pixel_color(window.left + 464, window.top + 108)
                            print("Evolution", result_color_3)
                            time.sleep(1)

                            # Check if crit evolved
                            if result_color_3 == (107, 138, 19):
                                # Click continue
                                pyautogui.mouseDown(window.left + 580, window.top + 598) # Continue button
                                time.sleep(0.01)
                                pyautogui.mouseUp()
                                time.sleep(1)

                            # Exit training
                            pyautogui.mouseDown(window.left + 928, window.top + 58) # Close button
                            time.sleep(0.01)
                            pyautogui.mouseUp()
                            time.sleep(2)

                            result_color_4 = get_pixel_color(window.left + 593, window.top + 195)
                            print("Rank upgrade", result_color_4)
                            time.sleep(1)

                            # Close rank upgrade screen
                            if result_color_4 == (107, 138, 19):
                                pyautogui.mouseDown(window.left + 589, window.top + 511) # Close button
                                time.sleep(0.01)
                                pyautogui.mouseUp()
                                time.sleep(1)
                        break
                    # If crit is not ready to train, continue
                    if result_color_2 == (94, 108, 126): # Grey
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