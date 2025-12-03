import os
import sys
import time

# ANSI Color Codes
R = '\033[1;31m'  # Red
G = '\033[1;32m'  # Green
Y = '\033[1;33m'  # Yellow
B = '\033[1;34m'  # Blue
C = '\033[1;36m'  # Cyan
W = '\033[1;37m'  # White
RESET = '\033[0m' # Reset

def clear_screen():
    os.system('clear')

def print_slow(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.001)
    print()

def banner():
    clear_screen()
    # Ascii Art
    print(f"{R}  ____  ____   {W}AUTO SHARER")
    print(f"{R} |  _ \|  _ \  {W}VERSION 1.0.0")
    print(f"{R} | |_) | |_) | {W}FB AUTO SHARER")
    print(f"{R} |  _ <|  _ <  {W}2025")
    print(f"{R} |_| \_\_| \_\ {W}MO-4")
    print(f"{RESET}")
    
    # Updated Box with thick brackets 【 】 and Yellow /
    print(f"{W}  【 {Y}DEVELOPER {W}】 {Y}/ {W}【 {G}KEN DRICK {W}】")
    print(f"{W}  【 {Y}GITHUB    {W}】 {Y}/ {W}【 {G}RYO GRAHHH {W}】")
    print(f"{W}  【 {Y}FACEBOOK  {W}】 {Y}/ {W}【 {B}facebook.com/ryoevisu {W}】")
    print(f"{RESET}")
    print(f"{R}  ========================================={RESET}")

def main():
    banner()
    print("")
    # Menu Options using thick brackets
    print(f"{W}  【01】 {G}FILE CLONING")
    print(f"{W}  【02】 {G}COOKIE TO TOKEN")
    print(f"{W}  【03】 {G}CONTACT AUTHOR")
    print(f"{W}  【00】 {R}EXIT PROGRAM")
    print("")
    print(f"{R}  ========================================={RESET}")
    
    choice = input(f"{W}  【?】 SELECT OPTION : {G}")

    if choice == '1':
        print(f"\n{Y}  [!] COMING SOON...{RESET}")
    elif choice == '2':
        # Cookie to Token Logic
        print(f"\n{Y}  [!] LOAD KAZUXAPI...{RESET}")
        time.sleep(1)
        os.system("xdg-open https://kazuxapi.vercel.app/")
    elif choice == '3':
        os.system("xdg-open https://facebook.com/ryoevisu")
    elif choice == '0':
        sys.exit()
    else:
        print(f"\n{R}  [!] INVALID OPTION{RESET}")

if __name__ == "__main__":
    main(PROGRAMOGRAM
