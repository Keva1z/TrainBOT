import colorama
from colorama import Fore, Back
from datetime import datetime

colorama.init(autoreset=True)

bot_name = 'PairTraining_Bot'

class logger():
    class telegram():
        def log_command(username: str, command: str) -> None:
            """_summary_

            Args:
                username (str): name of telegram user
                command (str): command to log
            """
            
            print()
            pref = "USER"
            if username == bot_name:
                pref = 'BOT'
            
            print(Back.BLACK + (Fore.YELLOW + f"({datetime.now().strftime('%H:%M:%S')})"+ Fore.RED + "[" + pref +"] " + Fore.CYAN + username + Fore.WHITE + " : " + command + " "))
            print()
            
    class database():
        def log(message: str) -> None:
            print(Back.BLACK + (Fore.YELLOW + f"({datetime.now().strftime('%H:%M:%S')})"+ Fore.RED + "[DATABASE] " + Fore.GREEN + message + " "))
            
    
    class daily_reset():
        def log(message: str) -> None:
            print()
            print(Back.BLACK + (Fore.YELLOW + f"({datetime.now().strftime('%H:%M:%S')})"+ Fore.LIGHTCYAN_EX + "[Daily Reset] " + Fore.LIGHTYELLOW_EX + message + " "))
