import time

from colorama import *
from helpers.time import Time
from helpers.menus import Menus
from helpers.sessions import Sessions
from helpers.database import Database

init(convert=True)
Database.create_table()

class GuardCord:
    def __init__(self, hash_ids: list[str]):
        self.known_sessions: list[str] = []
        
        for hash_id in hash_ids:
            self.known_sessions.append(hash_id)

    def start(self):
        if Sessions.get() is not None:
            sessions_list: dict[str] = Sessions.get()
            
            for session in sessions_list["user_sessions"]:
                session_id_hash: str = session["id_hash"]
                approx_last_used_time: str = Time.to_human_time(session["approx_last_used_time"])
                
                operating_system: str = session["client_info"]["os"]
                platform: str = session["client_info"]["platform"]
                
                self.known_sessions.append(session_id_hash)
                print(f"{Fore.GREEN}[SESSION]{Fore.WHITE} {operating_system}, {platform} ({approx_last_used_time}) was added to the known sessions list.")
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
            time.sleep(6); exit(code=None)
            
        
if __name__ == "__main__":
    GuardCord_Instance: object = GuardCord(hash_ids=Database.get_sessions())
    GuardCord_Instance.start()