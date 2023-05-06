import os
import time
import keyboard

from colorama import *

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_text(question: str, pressed_that_was_me: bool):
    clear_console()
    
    if pressed_that_was_me == True:
        print(question)
        print(f"{Fore.GREEN}✔ That was me!{Fore.GREEN}{Fore.WHITE}  ✘ That wasn't me..")
    elif pressed_that_was_me == False:
        print(question)
        print(f"{Fore.WHITE}✔ That was me!{Fore.RED}  ✘ That wasn't me..{Fore.WHITE}")
        
class Menus:
    def yes_or_no(question: str) -> bool:
        pressed_that_was_me: bool = True
        pressed_enter: bool = False

        update_text(question, pressed_that_was_me)
        try:
            while not pressed_enter:
                if keyboard.is_pressed('left'):
                    print(pressed_that_was_me)
                    pressed_that_was_me = True
                    update_text(question, pressed_that_was_me)
                    time.sleep(0.1)
                    
                elif keyboard.is_pressed('right'):
                    pressed_that_was_me = False
                    update_text(question, pressed_that_was_me)
                    time.sleep(0.1)
                    
                elif keyboard.is_pressed('enter'):
                    return pressed_that_was_me
                    
                    
        except Exception as e:
            print(e)