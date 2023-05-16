import os
import time
import json
import asyncio
import getpass
import subprocess

from colorama import *
from modules.time import Time
from modules.menus import Menus
from modules.config import Fetch
from modules.discord import Discord
from modules.sessions import Sessions
from modules.database import Database
from modules.notifications import Notifications

init(convert=True)
Database.create_table()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class GuardCord:
    def __init__(self, hash_ids: list[str]):
        self.known_sessions: list[str] = []
        self.backup_codes: list[str] = []
        self.password: str = None
        
        for hash_id in hash_ids:
            self.known_sessions.append(hash_id)
            print(f"{Fore.GREEN}[CACHED SESSION]{Fore.WHITE} {hash_id} has been added to known sessions.")
            
            time.sleep(2);clear_console()

    def start(self):
        password = getpass.getpass(f"{Fore.GREEN}[INPUT]{Fore.WHITE} Discord Password: "); self.password = password
        Database.update_password(password)
        
        nonce: str = Discord.send_code_to_email(password=password)
        
        if nonce != None:
            clear_console(); print(f"{Fore.GREEN}[SUCCESS]{Fore.WHITE} A code has been sent to your email, Please enter it below.")
            code = str(input(f"{Fore.GREEN}[INPUT]{Fore.WHITE} Discord Code: ")); result = Discord.get_codes(code=code, nonce=nonce); clear_console()
            
            for backup_code in result["backup_codes"]:
                if backup_code["consumed"] == False:
                    self.backup_codes.append(backup_code["code"])
                    backup_code: str = backup_code["code"]

                    print(f"{Fore.GREEN}[BACKUP CODE]{Fore.WHITE} {backup_code} has been added to the backup codes list.")
                    time.sleep(1); clear_console()
                else:
                    pass
            
            if Sessions.get() is not None:
                sessions_list: dict[str] = Sessions.get(); Database.update_token(Fetch.authorization_token())
                
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
                        time.sleep(1); clear_console()
            else:
                print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
                time.sleep(6); exit(code=None)
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Invalid password or you are Ratelimited, Please try again.")
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
                            
                            Notifications.send(f"Discord - {platform}", "Someone has logged into your account, please check the console.", 4)
                            menu_result: int = Menus.yes_or_no(f"{Fore.RED}[DEVICE] {operating_system.upper()}\n[PLATFORM] {platform}\n[LOCATION] {location}\n[TIME] {readable_time}\n")
                            
                            if menu_result == True:
                                session_id: str = session["id_hash"]
                                Database.add_session(session["id_hash"], operating_system, platform)
                                
                                print(f"{Fore.GREEN}[SESSION]{Fore.WHITE} Session ({session_id}) been added to the known sessions list.")
                            else:
                                response: str = Discord.change_password(self.get_backup_code(), self.password)
                                new_password: str = response["new_password"]; new_token: str = response["new_token"]
                                
                                Database.update_password(new_password); Database.update_token(new_token)
                                
                                with open("config.json", "r+") as jsonFile:
                                    config_data = json.load(jsonFile)
                                    config_data["account"]["authorization_token"] = new_token

                                    jsonFile.seek(0); json.dump(config_data, jsonFile); jsonFile.truncate()
                                    
                                print(f"{Fore.GREEN}[PASSWORD CHANGED]{Fore.WHITE} Password has been changed, Restarting the program...")
                                
                    await asyncio.sleep(4)
                else:
                    print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
                    time.sleep(6); exit(code=None)
                    
            except Exception as e:
                print(e)
                
    def get_backup_code(self) -> str:
        if len(self.backup_codes) == 0:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} No backup codes left, Please generate new ones.")
            time.sleep(6); exit(code=None)
        else:
            backup_code: str = self.backup_codes[0]
            self.backup_codes.remove(backup_code)
            
            return backup_code
                      
if __name__ == "__main__":
    GuardCord_Instance: object = GuardCord(hash_ids=Database.get_sessions())
    GuardCord_Instance.start(); asyncio.run(GuardCord_Instance.listen())