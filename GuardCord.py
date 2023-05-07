import os
import time
import asyncio

from colorama import *
from helpers.time import Time
from helpers.menus import Menus
from helpers.discord import Discord
from helpers.sessions import Sessions
from helpers.database import Database

init(convert=True)
Database.create_table()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class GuardCord:
    def __init__(self, hash_ids: list[str]):
        self.known_sessions: list[str] = []
        self.backup_codes: list[str] = []
        
        for hash_id in hash_ids:
            self.known_sessions.append(hash_id)
            print(f"{Fore.GREEN}[CACHED SESSION]{Fore.WHITE} {hash_id} has been added to known sessions.")
            
            time.sleep(2);clear_console()

    def start(self):
        password = str(input(f"{Fore.GREEN}[INPUT]{Fore.WHITE} Discord Password: "))
        nonce: str = Discord.send_code_to_email(password=password)
        
        if nonce != None:
            clear_console(); print(f"{Fore.GREEN}[SUCCESS]{Fore.WHITE} A code has been sent to your email, Please enter it below.")
            code = str(input(f"{Fore.GREEN}[INPUT]{Fore.WHITE} Discord Code: ")); result = Discord.get_codes(code=code, nonce=nonce)
            print(result)
            
            time.sleep(3); clear_console()
            
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
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Invalid password, Please try again.")
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
                            self.known_sessions.append(session["id_hash"])
                            
                            operating_system: str = session["client_info"]["os"]
                            platform: str = session["client_info"]["platform"]
                            location: str = session["client_info"]["location"]
                            readable_time: str = Time.to_human_time(session["approx_last_used_time"])
                            
                            menu_result: int = Menus.yes_or_no(f"{Fore.RED}[DEVICE] {operating_system.upper()}\n[PLATFORM] {platform}\n[LOCATION] {location}\n[TIME] {readable_time}\n")
                            
                            if menu_result == True:
                                session_id: str = session["id_hash"]
                                Database.add_session(session["id_hash"], operating_system, platform)
                                
                                print(f"{Fore.GREEN}[SESSION]{Fore.WHITE} Session ({session_id}) been added to the known sessions list.")
                            else:
                                print("we need to do our stuff to log them out...")
                                
                    await asyncio.sleep(4)
                else:
                    print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
                    time.sleep(6); exit(code=None)
                    
            except Exception as e:
                print(e)
                      
if __name__ == "__main__":
    GuardCord_Instance: object = GuardCord(hash_ids=Database.get_sessions())
    GuardCord_Instance.start(); asyncio.run(GuardCord_Instance.listen())