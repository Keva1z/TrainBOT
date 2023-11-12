import colorama
from colorama import Fore, Back
from datetime import datetime

colorama.init(autoreset=True)

bot_name = 'PairTraining_Bot'

class logger():
    last = None
    class telegram():
        def log_command(username: str, command: str) -> None:
            """_summary_

            Args:
                username (str): name of telegram user
                command (str): command to log
            """
            
            if logger.last != "telegram" and logger.last != None:
                print()
            
            logger.last = "telegram"  
            pref = "USER"
            if username == bot_name:
                pref = 'BOT'
            
            print(Back.BLACK + (Fore.YELLOW + f"({datetime.now().strftime('%H:%M:%S')})"+ Fore.RED + "[" + pref +"] " + Fore.CYAN + username + Fore.WHITE + " : " + command + " "))
            
    class database():
        def log(message: str) -> None:
            
            if logger.last != "database" and logger.last != None:
                print()
            
            logger.last = "database" 
            print(Back.BLACK + (Fore.YELLOW + f"({datetime.now().strftime('%H:%M:%S')})"+ Fore.RED + "[DATABASE] " + Fore.GREEN + message + " "))
            
    
    class daily_reset():
        def log(message: str) -> None:
            
            if logger.last != "resetter" and logger.last != None:
                print()
            
            logger.last = "resetter"
            print(Back.BLACK + (Fore.YELLOW + f"({datetime.now().strftime('%H:%M:%S')})"+ Fore.LIGHTCYAN_EX + "[Daily Reset] " + Fore.LIGHTYELLOW_EX + message + " "))
