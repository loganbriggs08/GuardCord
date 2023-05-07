import time
import asyncio

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
            print(f"{Fore.GREEN}[CACHED SESSION]{Fore.WHITE} {hash_id} has been added to known sessions.")

    def start(self):
        if Sessions.get() is not None:
            sessions_list: dict[str] = Sessions.get()
            
            for session in sessions_list["user_sessions"]:
                session_id_hash: str = session["id_hash"]
                approx_last_used_time: str = Time.to_human_time(session["approx_last_used_time"])
                
                operating_system: str = session["client_info"]["os"]
                platform: str = session["client_info"]["platform"]
                
                if session_id_hash in self.known_sessions:
                    continue
                else:
                    self.known_sessions.append(session_id_hash)
                    Database.add_session(session_id_hash, operating_system, platform)
                
                print(f"{Fore.GREEN}[SESSION]{Fore.WHITE} {operating_system}, {platform} ({approx_last_used_time}) was added to the known sessions list.")
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
            time.sleep(6); exit(code=None)
            
    async def listen(self):
        while True:
            try:
                if Sessions.get() is not None:
                    sessions_list: dict[str] = Sessions.get()
                    
                    for session in sessions_list["user_sessions"]:
                        if session["id_hash"] in self.known_sessions:
                            pass
                        else:
                            print("New Login detected...")
                            
                    await asyncio.sleep(6)
                else:
                    print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
                    time.sleep(6); exit(code=None)
                    
            except Exception as e:
                print(e)
                
                
if __name__ == "__main__":
    GuardCord_Instance: object = GuardCord(hash_ids=Database.get_sessions())
    GuardCord_Instance.start(); asyncio.run(GuardCord_Instance.listen())