import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)

bot_name = 'test_freelanceKEV_bot'

class logger():
    class telegram():
        def log_command(username: str, command: str) -> None:
            """_summary_

            Args:
                username (str): name of telegram user
                command (str): command to log
            """
            
            pref = "USER"
            if username == bot_name:
                pref = 'BOT'
            
            print(Back.BLACK + (Fore.RED + "[" + pref +"] " + Fore.CYAN + username + Fore.WHITE + " : " + command + " "))
    
    class database():
        def log(message: str) -> None:
            print(Back.BLACK + (Fore.RED + "[DATABASE] " + Fore.GREEN + message + " "))