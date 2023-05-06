from helpers.sessions import Sessions

class GuardCord:
    def start():
        print(Sessions.get())
        
if __name__ == "__main__":
    GuardCord.start()