import time

from colorama import *
from helpers.time import Time
from helpers.menus import Menus
from helpers.sessions import Sessions

init(convert=True)

class GuardCord:
    def __init__(self):
        self.known_sessions: list[str] = []
        
    def start(self):
        if Sessions.get() is not None:
            sessions_list: dict[str] = Sessions.get()
            
            for session in sessions_list["user_sessions"]:
                session_id_hash: str = session["id_hash"]
                self.known_sessions.append(session_id_hash)
                
            print(self.known_sessions)
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
            time.sleep(6); exit(code=None)
            
        
if __name__ == "__main__":
    GuardCord_Instance: object = GuardCord()
    GuardCord_Instance.start()