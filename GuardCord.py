import time

from colorama import *
from helpers.sessions import Sessions

init(convert=True)

class GuardCord:
    def start():
        if Sessions.get() is not None:
            print(f"{Fore.GREEN}[SUCCESS]{Fore.WHITE} Authorization is valid, Starting GuardCord.")
            
            sessions: dict[str] = Sessions.get()
            
            for session in sessions["user_sessions"]:
                print(session)
            
        else:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Authorization is invalid, Please replace it.")
            time.sleep(6); exit(code=None)
            
        
if __name__ == "__main__":
    GuardCord.start()