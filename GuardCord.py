import time

from colorama import *
from helpers.time import Time
from helpers.menus import Menus
from helpers.sessions import Sessions

init(convert=True)

class GuardCord:
    def start():
        if Sessions.get() is not None:
            sessions: dict[str] = Sessions.get()
            
            for session in sessions["user_sessions"]:
                operating_system: str = session["client_info"]["os"]
                platform: str = session["client_info"]["platform"]
                location: str = session["client_info"]["location"]
                readable_time: str = Time.to_human_time(session["approx_last_used_time"])
                
                menu_result: int = Menus.yes_or_no(f"{Fore.RED}[DEVICE] {operating_system.upper()}\n[PLATFORM] {platform}\n[LOCATION] {location}\n[TIME] {readable_time}\n")
                
            
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
            time.sleep(6); exit(code=None)
            
        
if __name__ == "__main__":
    GuardCord.start()