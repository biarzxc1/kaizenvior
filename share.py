import os
import sys
import time
import json
import urllib.request
import urllib.parse
import aiohttp
import asyncio
import datetime
import requests
import re
import random

# --- NEON COLOR PALETTE ---
R = '\033[1;31m'   # Red (Bold)
G = '\033[1;32m'   # Green (Bold)
C = '\033[1;36m'   # Cyan (Bold)
Y = '\033[1;33m'   # Yellow (Bold)
M = '\033[1;35m'   # Magenta (Bold)
B = '\033[1;34m'   # Blue (Bold)
W = '\033[1;37m'   # White (Bold)
BG_R = '\033[41m'  # Red Background
RESET = '\033[0m' # Reset

# --- UI CONSTANTS ---
LINE = f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

# --- API CONFIGURATION ---
API_URL = "https://rpwtools.onrender.com/api"  # Render server URL
user_token = None
user_data = None

# --- GLOBAL VARIABLES FOR AUTO SHARE V1 (PAGE & NORM ACC) ---
success_count = 0
lock = asyncio.Lock()
global_pause_event = asyncio.Event()
global_pause_event.set()  # Initially not paused

# --- GLOBAL VARIABLES FOR AUTO SHARE V2 (NORM ACC) ---
success_count_v2 = 0
lock_v2 = asyncio.Lock()
eaag_tokens = []

def clear():
    """Clears the terminal screen completely."""
    os.system('clear')

def normalize_facebook_url(url):
    """
    Normalize Facebook URL to facebook.com/username format.
    Removes https://, www., m., and standardizes to facebook.com
    """
    if not url:
        return url
    
    url = url.strip()
    url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
    url = re.sub(r'^(www\.|m\.)', '', url, flags=re.IGNORECASE)
    
    if not url.startswith('facebook.com'):
        if '/' not in url:
            url = f'facebook.com/{url}'
    
    return url

def banner_header():
    """Prints the static top part (Banner + Info)."""
    print(f"""{C}
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    {RESET}""")

    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'GITHUB':<13} {W}➤{RESET} {G}RYO GRAHHH{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}2.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    
    tool_name = f"{R}[ {BG_R}{W}RPWTOOLS{RESET}{R} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL\'S NAME':<13} {W}➤{RESET} {tool_name}")
    
    if user_data:
        print(LINE)
        username_display = user_data['username'].upper()
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'USERNAME':<13} {W}➤{RESET} {G}{username_display}{RESET}")
        
        fb_link = user_data.get('facebook', 'N/A')
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}{fb_link}{RESET}")
        
        country_display = user_data.get('country', 'N/A').upper()
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COUNTRY':<13} {W}➤{RESET} {G}{country_display}{RESET}")
        
        # Color-coded plan display with background colors
        user_plan = user_data['plan']
        if user_plan == 'max':
            plan_display = f"{M}[ \033[45m{W}MAX{RESET}{M} ]{RESET}"  # Magenta background
        elif user_plan == 'vip':
            plan_display = f"{G}[ \033[42m{W}VIP{RESET}{G} ]{RESET}"  # Green background
        else:  # free
            plan_display = f"{W}[ \033[47m\033[30mFREE{RESET}{W} ]{RESET}"  # White background with black text
        
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN':<13} {W}➤{RESET} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN EXPIRY IN':<13} {W}➤{RESET} {Y}{user_data['planExpiry']}{RESET}")
        
        # Show paired accounts count
        account_count = user_data.get('accountCount', 0)
        all_cookies = user_data.get('allCookies', 0)
        all_tokens = user_data.get('allTokens', 0)
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PAIRED ACC':<13} {W}➤{RESET} {C}{account_count}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ALL COOKIES':<13} {W}➤{RESET} {C}{all_cookies}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ALL TOKENS':<13} {W}➤{RESET} {C}{all_tokens}{RESET}")
    
    print(LINE)

def show_menu():
    """Prints the Menu Options."""
    def key(n, c): return f"{W}[{W}{n}{Y}/{W}{c}{W}]{RESET}"

    if not user_token:
        print(f" {key('01', 'A')} {G}LOGIN{RESET}")
        print(f" {key('02', 'B')} {G}REGISTER{RESET}")
        print(f" {key('00', 'X')} {R}EXIT{RESET}")
    elif user_data and user_data.get('isAdmin'):
        print(f" {key('01', 'A')} {G}START AUTO SHARE (PAGE & NORM ACC){RESET}")
        print(f" {key('02', 'B')} {C}START AUTO SHARE V2 (NORM ACC){RESET}")
        print(f" {key('03', 'C')} {G}COOKIE TO TOKEN{RESET}") 
        print(f" {key('04', 'D')} {G}MANAGE COOKIE & TOKEN{RESET}")
        print(f" {key('05', 'E')} {G}MY STATS{RESET}")
        print(f" {key('06', 'F')} {M}ADMIN PANEL{RESET}")
        print(f" {key('07', 'G')} {G}UPDATE TOOL{RESET}")
        print(f" {key('00', 'X')} {R}LOGOUT{RESET}")
    else:
        print(f" {key('01', 'A')} {G}START AUTO SHARE (PAGE & NORM ACC){RESET}")
        print(f" {key('02', 'B')} {C}START AUTO SHARE V2 (NORM ACC){RESET}")
        print(f" {key('03', 'C')} {G}COOKIE TO TOKEN{RESET}") 
        print(f" {key('04', 'D')} {G}MANAGE COOKIE & TOKEN{RESET}")
        print(f" {key('05', 'E')} {G}MY STATS{RESET}")
        print(f" {key('06', 'F')} {G}UPDATE TOOL{RESET}")
        print(f" {key('00', 'X')} {R}LOGOUT{RESET}")
    
    print(LINE)

def refresh_screen():
    """Instantly wipes screen and repaints the UI base."""
    clear()
    banner_header()
    show_menu()

def nice_loader(text="PROCESSING"):
    """Improved Progress Bar Loader."""
    sys.stdout.write("\033[?25l")
    
    filled = "■"
    empty = "□"
    width = 20
    
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = filled * i + empty * (width - i)
        color = G if i == width else C
        
        sys.stdout.write(f"\r {W}[{RESET}•{W}]{RESET} {Y}{text:<10} {W}➤{RESET} {color}[{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.04) 
    
    time.sleep(0.3) 
    sys.stdout.write(f"\r{' ' * 65}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")

# ============ API FUNCTIONS ============

def get_country_from_ip():
    """Auto-detect country from IP address"""
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
    except:
        pass
    return 'Unknown'

def api_request(method, endpoint, data=None, use_token=True):
    """Make API request to server"""
    headers = {"Content-Type": "application/json"}
    
    if use_token and user_token:
        headers["Authorization"] = f"Bearer {user_token}"
    
    url = f"{API_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None, "Invalid method"
        
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to server. Make sure server is running."
    except requests.exceptions.Timeout:
        return None, "Request timeout. Server not responding."
    except Exception as e:
        return None, f"Error: {str(e)}"

def login_user():
    """Login user"""
    global user_token, user_data
    
    refresh_screen()
    print(f" {G}[!] LOGIN TO RPWTOOLS{RESET}")
    print(LINE)
    
    username = input(f" {W}[{W}➤{W}]{RESET} {C}USERNAME {W}➤{RESET} ").strip()
    if not username:
        return
    
    password = input(f" {W}[{W}➤{W}]{RESET} {C}PASSWORD {W}➤{RESET} ").strip()
    if not password:
        return
    
    refresh_screen()
    nice_loader("LOGGING IN")
    
    status, response = api_request("POST", "/auth/login", {
        "username": username,
        "password": password
    }, use_token=False)
    
    if status == 200 and response.get('success'):
        user_token = response.get('token')
        user_data = response.get('user')
        
        print(f" {G}[SUCCESS] Login successful!{RESET}")
        print(LINE)
        print(f" {Y}Welcome back, {G}{user_data['username'].upper()}{RESET}")
        print(f" {Y}Plan: {G}{user_data['plan'].upper()}{RESET}")
        print(f" {Y}Paired Accounts: {C}{user_data.get('accountCount', 0)}{RESET}")
        print(f" {Y}All Cookies: {C}{user_data.get('allCookies', 0)}{RESET}")
        print(f" {Y}All Tokens: {C}{user_data.get('allTokens', 0)}{RESET}")
        
        if user_data.get('isAdmin'):
            print(f" {M}[ADMIN ACCESS GRANTED]{RESET}")
        
        print(LINE)
    else:
        print(f" {R}[ERROR] {response if isinstance(response, str) else response.get('message', 'Login failed')}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def register_user():
    """Register new user"""
    global user_token, user_data
    
    refresh_screen()
    print(f" {G}[!] REGISTER NEW ACCOUNT{RESET}")
    print(LINE)
    
    username = input(f" {W}[{W}➤{W}]{RESET} {C}USERNAME {W}➤{RESET} ").strip()
    if not username:
        return
    
    password = input(f" {W}[{W}➤{W}]{RESET} {C}PASSWORD {W}➤{RESET} ").strip()
    if not password:
        return
    
    facebook = input(f" {W}[{W}➤{W}]{RESET} {C}FACEBOOK LINK {W}➤{RESET} ").strip()
    if not facebook:
        return
    
    facebook = normalize_facebook_url(facebook)
    
    refresh_screen()
    print(f" {G}[!] NORMALIZED FACEBOOK URL: {Y}{facebook}{RESET}")
    print(LINE)
    
    print(f" {G}[!] DETECTING YOUR COUNTRY...{RESET}")
    nice_loader("DETECTING")
    
    country = get_country_from_ip()
    
    refresh_screen()
    print(f" {G}[!] DETECTED COUNTRY: {Y}{country}{RESET}")
    print(LINE)
    confirm = input(f" {W}[{W}➤{W}]{RESET} {Y}Is this correct? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm == 'N':
        country = input(f" {W}[{W}➤{W}]{RESET} {C}ENTER YOUR COUNTRY {W}➤{RESET} ").strip()
    
    refresh_screen()
    nice_loader("REGISTERING")
    
    status, response = api_request("POST", "/auth/register", {
        "username": username,
        "password": password,
        "facebook": facebook,
        "country": country
    }, use_token=False)
    
    if status == 201 and response.get('success'):
        user_token = response.get('token')
        user_data = response.get('user')
        
        print(f" {G}[SUCCESS] Registration successful!{RESET}")
        print(LINE)
        print(f" {Y}Welcome, {G}{user_data['username'].upper()}{RESET}")
        print(f" {Y}Plan: {G}{user_data['plan'].upper()}{RESET}")
        print(f" {Y}Country: {G}{user_data['country']}{RESET}")
        print(f" {Y}Facebook: {G}{facebook}{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] {response if isinstance(response, str) else response.get('message', 'Registration failed')}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def show_user_stats():
    """Display user statistics"""
    refresh_screen()
    print(f" {G}[!] LOADING STATS...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/stats")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats')
        
        refresh_screen()
        print(f" {G}[USER STATISTICS]{RESET}")
        print(LINE)
        print(f" {Y}Username: {W}{stats['username'].upper()}{RESET}")
        
        plan_color = G if stats['plan'] == 'max' else Y if stats['plan'] == 'vip' else W
        print(f" {Y}Plan: {plan_color}{stats['plan'].upper()}{RESET}")
        
        if stats.get('planExpiry'):
            print(f" {Y}Plan Expiry In: {W}{stats['planExpiry']}{RESET}")
        
        print(LINE)
        print(f" {C}[STATISTICS]{RESET}")
        print(f" {Y}Total Shares: {G}{stats['totalShares']}{RESET}")
        print(f" {Y}Total Cookie Converts: {G}{stats['totalCookieConverts']}{RESET}")
        print(f" {Y}Paired Accounts: {C}{stats.get('accountCount', 0)}{RESET}")
        print(f" {Y}All Cookies: {C}{stats.get('allCookies', 0)}{RESET}")
        print(f" {Y}All Tokens: {C}{stats.get('allTokens', 0)}{RESET}")
        print(LINE)
        
        global_pause = stats.get('globalPause', {})
        share_cd = stats.get('shareCooldown', {})
        cookie_cd = stats.get('cookieCooldown', {})
        
        print(f" {C}[COOLDOWN STATUS]{RESET}")
        
        if global_pause.get('active'):
            print(f" {R}⚠ GLOBAL PAUSE ACTIVE (All Accounts Blocked) ⚠{RESET}")
            print(f" {R}Remaining: {global_pause['remainingSeconds']}s{RESET}")
            print(f" {Y}Available at: {W}{global_pause['availableAt']}{RESET}")
        else:
            if share_cd.get('active'):
                print(f" {R}Share Cooldown: {share_cd['remainingSeconds']}s remaining{RESET}")
                print(f" {Y}Available at: {W}{share_cd['availableAt']}{RESET}")
            else:
                print(f" {G}Share: Ready ✓{RESET}")
            
            if cookie_cd.get('active'):
                print(f" {R}Cookie Convert Cooldown: {cookie_cd['remainingSeconds']}s remaining{RESET}")
                print(f" {Y}Available at: {W}{cookie_cd['availableAt']}{RESET}")
            else:
                print(f" {G}Cookie Convert: Ready ✓{RESET}")
        
        print(LINE)
    else:
        print(f" {R}[ERROR] {response if isinstance(response, str) else response.get('message', 'Failed to get stats')}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def manage_cookie_token():
    """Manage paired cookie & token accounts"""
    while True:
        refresh_screen()
        print(f" {G}[MANAGE COOKIE & TOKEN]{RESET}")
        print(LINE)
        print(f" {W}[{W}1{W}]{RESET} {G}VIEW ALL ACCOUNTS{RESET}")
        print(f" {W}[{W}2{W}]{RESET} {G}ADD ACCOUNT (Cookie + Token){RESET}")
        print(f" {W}[{W}3{W}]{RESET} {R}DELETE ACCOUNT{RESET}")
        print(f" {W}[{W}4{W}]{RESET} {R}DELETE ALL ACCOUNTS{RESET}")
        print(f" {W}[{W}0{W}]{RESET} {Y}BACK{RESET}")
        print(LINE)
        
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip()
        
        if choice == '1':
            view_accounts()
        elif choice == '2':
            add_account()
        elif choice == '3':
            delete_account()
        elif choice == '4':
            delete_all_accounts()
        elif choice == '0':
            return
        else:
            print(f"\n {R}[!] INVALID SELECTION{RESET}")
            time.sleep(0.8)

def view_accounts():
    """View all paired accounts"""
    refresh_screen()
    print(f" {G}[!] LOADING ACCOUNTS...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/accounts")
    
    if status == 200 and response.get('success'):
        accounts = response.get('accounts', [])
        
        refresh_screen()
        print(f" {G}[PAIRED ACCOUNTS] Total: {len(accounts)}{RESET}")
        print(LINE)
        
        if not accounts:
            print(f" {Y}No accounts stored yet.{RESET}")
        else:
            for i, acc in enumerate(accounts, 1):
                print(f" {W}[{i:02d}]{RESET} {M}{acc['name']}{RESET} {W}({C}UID: {acc['uid']}{W}){RESET}")
                cookie_preview = acc['cookie'][:30] + "..." if len(acc['cookie']) > 30 else acc['cookie']
                token_preview = acc['token'][:30] + "..." if len(acc['token']) > 30 else acc['token']
                print(f"      Cookie: {C}{cookie_preview}{RESET}")
                print(f"      Token: {C}{token_preview}{RESET}")
                print(f"      Added: {Y}{acc['addedAt']}{RESET}")
                print(LINE)
        
    else:
        print(f" {R}[ERROR] Failed to load accounts{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def add_account():
    """Add new paired cookie & token account"""
    refresh_screen()
    print(f" {G}[ADD ACCOUNT]{RESET}")
    print(f" {Y}[TIP] You need to provide both Cookie and Token for the same account.{RESET}")
    print(LINE)
    
    cookie = input(f" {W}[{W}➤{W}]{RESET} {C}COOKIE {W}➤{RESET} ").strip()
    if not cookie:
        return
    
    token = input(f" {W}[{W}➤{W}]{RESET} {C}TOKEN {W}➤{RESET} ").strip()
    if not token:
        return
    
    refresh_screen()
    nice_loader("VALIDATING")
    
    status, response = api_request("POST", "/user/accounts", {
        "cookie": cookie,
        "token": token
    })
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(f" {G}[SUCCESS] {response.get('message')}{RESET}")
        print(LINE)
        print(f" {Y}Name: {M}{response.get('name', 'Unknown')}{RESET}")
        print(f" {Y}UID: {C}{response.get('uid', 'Unknown')}{RESET}")
        print(LINE)
        
        if user_data:
            user_data['accountCount'] = response.get('totalAccounts', 0)
            user_data['allCookies'] = response.get('allCookies', 0)
            user_data['allTokens'] = response.get('allTokens', 0)
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed to add account') if isinstance(response, dict) else 'Failed to add account'
        print(f" {R}[ERROR] {error_msg}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_account():
    """Delete a specific account"""
    refresh_screen()
    print(f" {G}[!] LOADING ACCOUNTS...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/accounts")
    
    if status != 200 or not isinstance(response, dict) or not response.get('success'):
        error_msg = response if isinstance(response, str) else 'Failed to load accounts'
        print(f" {R}[ERROR] {error_msg}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    accounts = response.get('accounts', [])
    
    if not accounts:
        refresh_screen()
        print(f" {Y}No accounts to delete.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {R}[DELETE ACCOUNT]{RESET}")
    print(LINE)
    
    for i, acc in enumerate(accounts, 1):
        print(f" {W}[{i}]{RESET} {M}{acc['name']}{RESET} {W}({C}UID: {acc['uid']}{W}){RESET}")
    
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT ACCOUNT NUMBER (0 to cancel) {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        acc_index = int(choice) - 1
        if acc_index < 0 or acc_index >= len(accounts):
            print(f" {R}[ERROR] Invalid account number{RESET}")
            time.sleep(1)
            return
        
        selected_acc = accounts[acc_index]
    except:
        print(f" {R}[ERROR] Invalid input{RESET}")
        time.sleep(1)
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/user/accounts/{selected_acc['id']}")
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(f" {G}[SUCCESS] Account deleted!{RESET}")
        if user_data:
            user_data['accountCount'] = response.get('totalAccounts', 0)
            user_data['allCookies'] = response.get('allCookies', 0)
            user_data['allTokens'] = response.get('allTokens', 0)
    else:
        error_msg = response if isinstance(response, str) else 'Failed to delete account'
        print(f" {R}[ERROR] {error_msg}{RESET}")
    
    print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_all_accounts():
    """Delete all accounts"""
    refresh_screen()
    print(f" {R}[DELETE ALL ACCOUNTS]{RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R}Delete ALL accounts? This cannot be undone! (YES/NO) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", "/user/accounts")
    
    if status == 200 and response.get('success'):
        print(f" {G}[SUCCESS] {response.get('message')}{RESET}")
        if user_data:
            user_data['accountCount'] = 0
            user_data['allCookies'] = 0
            user_data['allTokens'] = 0
    else:
        print(f" {R}[ERROR] Failed to delete accounts{RESET}")
    
    print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def cookie_to_token_tool():
    """Cookie to token converter with cooldown check"""
    nice_loader("LAUNCHING")

    while True:
        refresh_screen()
        
        status, response = api_request("POST", "/cookie/convert")
        
        if status == 429:
            print(f" {R}[COOLDOWN ACTIVE]{RESET}")
            print(LINE)
            print(f" {Y}Remaining Time: {R}{response.get('remainingSeconds', 0)}s{RESET}")
            print(f" {Y}Available At: {W}{response.get('cooldownEnd', 'N/A')}{RESET}")
            print(LINE)
            input(f"\n {Y}[PRESS ENTER TO GO BACK]{RESET}")
            return
        
        print(f" {G}[!] ENTER COOKIE TO CONVERT (Leave empty to back){RESET}")
        
        prompt = f" {W}[{W}➤{W}]{RESET} {C}COOKIE {W}➤{RESET} "
        
        try:
            cookie = input(prompt)
        except KeyboardInterrupt:
            return

        if not cookie.strip():
            return

        refresh_screen() 
        nice_loader("EXTRACTING") 

        try:
            encoded_cookie = urllib.parse.quote(cookie.strip())
            url = f"https://kazuxapi.vercel.app/{encoded_cookie}"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = response.read().decode('utf-8')
                json_data = json.loads(data)
                
            if json_data.get("success"):
                print(f" {G}[SUCCESS] TOKENS GENERATED:{RESET}")
                print(LINE)
                
                tokens = json_data.get("tokens", {})
                for app_name, token in tokens.items():
                    if token:
                        print(f" {Y}{app_name}:{RESET}")
                        print(f" {W}{token}{RESET}")
                        print(LINE)
                    else:
                        print(f" {Y}{app_name}: {R}No Token Found{RESET}")
                        print(LINE)
                
                api_request("POST", "/cookie/convert")
            else:
                error = json_data.get("error", "Unknown Error")
                print(f" {R}[FAILED] {error}{RESET}")
                print(LINE)
                
        except Exception:
            print(f" {R}[ERROR] Network Connection Failed.{RESET}")
            print(LINE)

        input(f"\n {Y}[PRESS ENTER TO CONVERT ANOTHER]{RESET}")

def update_tool_logic():
    """Simulates an update and restarts the script."""
    print(f" {G}[!] CHECKING FOR UPDATES...{RESET}")
    nice_loader("CHECKING")
    
    print(f" {G}[!] NEW VERSION FOUND! DOWNLOADING...{RESET}")
    nice_loader("UPDATING")
    
    print(f" {G}[!] UPDATE COMPLETE. RESTARTING...{RESET}")
    time.sleep(1)
    
    os.execv(sys.executable, ['python'] + sys.argv)

# ============ ADMIN PANEL FUNCTIONS ============

def admin_panel():
    """Admin panel for managing users"""
    while True:
        refresh_screen()
        print(f" {M}[ADMIN PANEL]{RESET}")
        print(LINE)
        print(f" {W}[{W}1{W}]{RESET} {G}VIEW ALL USERS{RESET}")
        print(f" {W}[{W}2{W}]{RESET} {Y}CHANGE USER PLAN{RESET}")
        print(f" {W}[{W}3{W}]{RESET} {R}DELETE USER{RESET}")
        print(f" {W}[{W}4{W}]{RESET} {C}VIEW ACTIVITY LOGS{RESET}")
        print(f" {W}[{W}5{W}]{RESET} {G}DASHBOARD STATS{RESET}")
        print(f" {W}[{W}0{W}]{RESET} {Y}BACK{RESET}")
        print(LINE)
        
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip()
        
        if choice == '1':
            view_all_users()
        elif choice == '2':
            change_user_plan()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            view_activity_logs()
        elif choice == '5':
            dashboard_stats()
        elif choice == '0':
            return
        else:
            print(f"\n {R}[!] INVALID SELECTION{RESET}")
            time.sleep(0.8)

def view_all_users():
    """View all registered users"""
    refresh_screen()
    print(f" {G}[!] LOADING USERS...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/users")
    
    if status == 200 and response.get('success'):
        users = response.get('users', [])
        
        refresh_screen()
        print(f" {G}[ALL USERS] Total: {len(users)}{RESET}")
        print(LINE)
        
        for i, user in enumerate(users, 1):
            plan_color = G if user['plan'] == 'max' else Y if user['plan'] == 'vip' else W
            admin_badge = f" {M}[ADMIN]{RESET}" if user.get('isAdmin') else ""
            
            print(f" {W}[{i:02d}]{RESET} {C}{user['username'].upper()}{RESET}{admin_badge}")
            print(f"      Plan: {plan_color}{user['plan'].upper()}{RESET} | Country: {G}{user['country']}{RESET}")
            print(f"      Shares: {Y}{user['totalShares']}{RESET} | Converts: {Y}{user['totalCookieConverts']}{RESET}")
            print(f"      Accounts: {C}{user.get('accountCount', 0)}{RESET} | Cookies: {C}{user.get('allCookies', 0)}{RESET} | Tokens: {C}{user.get('allTokens', 0)}{RESET}")
            print(LINE)
        
    else:
        print(f" {R}[ERROR] Failed to get users{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def change_user_plan():
    """Change a user's plan"""
    refresh_screen()
    print(f" {Y}[CHANGE USER PLAN]{RESET}")
    print(LINE)
    
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load users{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    users = response.get('users', [])
    
    print(f" {G}[SELECT USER]{RESET}")
    print(LINE)
    for i, user in enumerate(users, 1):
        plan_color = G if user['plan'] == 'max' else Y if user['plan'] == 'vip' else W
        print(f" {W}[{i}]{RESET} {C}{user['username'].upper()}{RESET} - Plan: {plan_color}{user['plan'].upper()}{RESET}")
    print(LINE)
    
    user_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT USER NUMBER (0 to cancel) {W}➤{RESET} ").strip()
    
    if not user_choice or user_choice == '0':
        return
    
    try:
        user_index = int(user_choice) - 1
        if user_index < 0 or user_index >= len(users):
            print(f" {R}[ERROR] Invalid user number{RESET}")
            time.sleep(1)
            return
        
        selected_user = users[user_index]
    except:
        print(f" {R}[ERROR] Invalid input{RESET}")
        time.sleep(1)
        return
    
    refresh_screen()
    print(f" {Y}[CHANGE PLAN FOR: {selected_user['username'].upper()}]{RESET}")
    print(LINE)
    print(f" {W}[1]{RESET} {W}FREE{RESET} - 5min share cooldown, 30s cookie cooldown")
    print(f" {W}[2]{RESET} {Y}VIP{RESET} - 1min share cooldown, no cookie cooldown (RENTAL)")
    print(f" {W}[3]{RESET} {G}MAX{RESET} - No cooldowns, unlimited")
    print(LINE)
    
    plan_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT PLAN NUMBER {W}➤{RESET} ").strip()
    
    plan_map = {'1': 'free', '2': 'vip', '3': 'max'}
    
    if plan_choice not in plan_map:
        print(f" {R}[ERROR] Invalid plan{RESET}")
        time.sleep(1)
        return
    
    new_plan = plan_map[plan_choice]
    duration = None
    
    if new_plan == 'vip':
        refresh_screen()
        print(f" {Y}[VIP PLAN DURATION]{RESET}")
        print(LINE)
        print(f" {W}[1]{RESET} 1 Month")
        print(f" {W}[2]{RESET} 2 Months")
        print(f" {W}[3]{RESET} 3 Months")
        print(LINE)
        
        duration_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT DURATION {W}➤{RESET} ").strip()
        
        duration_map = {'1': 1, '2': 2, '3': 3}
        
        if duration_choice not in duration_map:
            print(f" {R}[ERROR] Invalid duration{RESET}")
            time.sleep(1)
            return
        
        duration = duration_map[duration_choice]
    
    refresh_screen()
    print(f" {Y}[CONFIRM CHANGE]{RESET}")
    print(LINE)
    print(f" User: {C}{selected_user['username'].upper()}{RESET}")
    print(f" Current Plan: {W}{selected_user['plan'].upper()}{RESET}")
    print(f" New Plan: {G}{new_plan.upper()}{RESET}")
    if duration:
        print(f" Duration: {Y}{duration} month(s){RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {Y}Confirm? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        return
    
    nice_loader("UPDATING")
    
    status, response = api_request("PUT", f"/admin/users/{selected_user['username']}/plan", {
        "plan": new_plan,
        "duration": duration
    })
    
    if status == 200 and response.get('success'):
        print(f" {G}[SUCCESS] Plan updated successfully!{RESET}")
    else:
        print(f" {R}[ERROR] {response.get('message', 'Failed to update plan')}{RESET}")
    
    print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_user():
    """Delete a user account"""
    refresh_screen()
    print(f" {R}[DELETE USER]{RESET}")
    print(LINE)
    
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load users{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    users = response.get('users', [])
    
    if not users:
        print(f" {Y}No users to delete.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    print(f" {G}[SELECT USER TO DELETE]{RESET}")
    print(LINE)
    
    for i, user in enumerate(users, 1):
        plan_color = G if user['plan'] == 'max' else Y if user['plan'] == 'vip' else W
        admin_badge = f" {M}[ADMIN]{RESET}" if user.get('isAdmin') else ""
        
        letter = chr(64 + i)
        key_display = f"{W}[{i:02d}{Y}/{W}{letter}{W}]{RESET}"
        
        print(f" {key_display} {C}{user['username'].upper()}{RESET}{admin_badge} - {plan_color}{user['plan'].upper()}{RESET}")
    
    print(f" {W}[00{Y}/{W}X{W}]{RESET} {Y}CANCEL{RESET}")
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT USER {W}➤{RESET} ").strip().upper()
    
    if not choice or choice in ['0', '00', 'X']:
        return
    
    selected_user = None
    try:
        if choice.isdigit():
            user_index = int(choice) - 1
            if 0 <= user_index < len(users):
                selected_user = users[user_index]
        elif len(choice) == 1 and choice.isalpha():
            user_index = ord(choice) - 65
            if 0 <= user_index < len(users):
                selected_user = users[user_index]
    except:
        pass
    
    if not selected_user:
        print(f" {R}[ERROR] Invalid selection{RESET}")
        time.sleep(1)
        return
    
    refresh_screen()
    print(f" {R}[CONFIRM DELETION]{RESET}")
    print(LINE)
    print(f" User: {C}{selected_user['username'].upper()}{RESET}")
    print(f" Plan: {W}{selected_user['plan'].upper()}{RESET}")
    print(f" Country: {W}{selected_user['country']}{RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R}Delete this user? This cannot be undone! (YES/NO) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/admin/users/{selected_user['username']}")
    
    if status == 200 and response.get('success'):
        print(f" {G}[SUCCESS] User '{selected_user['username']}' deleted successfully!{RESET}")
    else:
        print(f" {R}[ERROR] {response.get('message', 'Failed to delete user')}{RESET}")
    
    print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def view_activity_logs():
    """View recent activity logs"""
    refresh_screen()
    print(f" {G}[!] LOADING ACTIVITY LOGS...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/logs?limit=20")
    
    if status == 200 and response.get('success'):
        logs = response.get('logs', [])
        
        refresh_screen()
        print(f" {C}[ACTIVITY LOGS] Recent 20{RESET}")
        print(LINE)
        
        for log in logs:
            action_color = G if log['action'] == 'login' else Y if log['action'] == 'register' else C
            print(f" {W}[{log['timestamp']}]{RESET}")
            print(f" User: {C}{log['username'].upper()}{RESET} | Action: {action_color}{log['action'].upper()}{RESET}")
            if log.get('details'):
                print(f" Details: {W}{log['details']}{RESET}")
            print(LINE)
    else:
        print(f" {R}[ERROR] Failed to load logs{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def dashboard_stats():
    """Show admin dashboard statistics"""
    refresh_screen()
    print(f" {G}[!] LOADING DASHBOARD...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/dashboard")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats', {})
        
        refresh_screen()
        print(f" {G}[ADMIN DASHBOARD]{RESET}")
        print(LINE)
        
        print(f" {C}[USER STATISTICS]{RESET}")
        print(f" Total Users: {G}{stats['totalUsers']}{RESET}")
        print(f" FREE Users: {W}{stats['planDistribution']['free']}{RESET}")
        print(f" VIP Users: {Y}{stats['planDistribution']['vip']}{RESET}")
        print(f" MAX Users: {G}{stats['planDistribution']['max']}{RESET}")
        print(LINE)
        
        print(f" {C}[ACTIVITY STATISTICS]{RESET}")
        print(f" Total Shares: {G}{stats['totalShares']}{RESET}")
        print(f" Total Cookie Converts: {G}{stats['totalCookieConverts']}{RESET}")
        print(LINE)
        
        print(f" {C}[RECENT USERS]{RESET}")
        for user in stats.get('recentUsers', []):
            plan_color = G if user['plan'] == 'max' else Y if user['plan'] == 'vip' else W
            print(f" {C}{user['username'].upper()}{RESET} - {plan_color}{user['plan'].upper()}{RESET} - {G}{user['country']}{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] Failed to load dashboard{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ AUTO SHARE V1 FUNCTIONS (PAGE & NORM ACC) ============

async def get_facebook_account_info(session, token):
    """Get Facebook account info (UID and name) from token."""
    try:
        url = f"https://graph.facebook.com/me"
        params = {
            'fields': 'id,name',
            'access_token': token
        }
        
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                name = data.get('name', 'Unknown')
                uid = data.get('id', 'Unknown')
                return name, uid
    except:
        pass
    return 'Unknown', 'Unknown'

async def getid(session, link):
    """Get Facebook post ID from link using traodoisub API."""
    try:
        async with session.post('https://id.traodoisub.com/api.php', data={"link": link}) as response:
            rq = await response.json()
            if 'success' in rq:
                return rq["id"]
            else:
                print(f" {R}[ERROR] Incorrect post link! Please re-enter{RESET}")
                return None
    except Exception as e:
        print(f" {R}[ERROR] Failed to get post ID: {e}{RESET}")
        return None

async def get_token(session, token, cookie):
    """Get page tokens from user token with FULL HEADERS."""
    params = {
        'access_token': token
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    try:
        async with session.get('https://graph.facebook.com/me/accounts', params=params, headers=headers) as r:
            rq = await r.json()
            if 'data' in rq:
                return rq
            else:
                print(f" {R}[ERROR] Incorrect Token or Cookie! Error getting pages.{RESET}")
                return {}
    except Exception as e:
        print(f" {R}[ERROR] Failed to get pages: {e}{RESET}")
        return {}

async def share_single_post(session, tk, ck, post, published_value):
    """Share a post once with FULL HEADERS."""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': ck,
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    try:
        async with session.get(f'https://graph.facebook.com/me/feed?method=POST&link=https://m.facebook.com/{post}&published={published_value}&access_token={tk}', headers=headers) as response:
            json_data = await response.json()
            if 'id' in json_data:
                return True, json_data.get('id', 'N/A')
            else:
                return False, json_data.get('error', {}).get('message', 'Unknown error')
    except Exception as e:
        return False, str(e)

async def show_countdown(seconds):
    """Display a countdown timer in MM:SS format."""
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02d}:{secs:02d}"
        
        sys.stdout.write(f"\r {Y}[PAUSED]{RESET} {W}|{RESET} {R}All accounts paused. Resuming in: {timer}{RESET} {W}|{RESET} {C}Press Ctrl+C to stop{RESET}")
        sys.stdout.flush()
        
        await asyncio.sleep(1)
    
    sys.stdout.write("\r" + " " * 100 + "\r")
    sys.stdout.flush()

async def share_loop(session, tk, ck, post, page_id):
    """
    Continuous sharing loop for a single page.
    ZERO DELAY - Maximum speed with synchronized pause handling.
    """
    global success_count, global_pause_event
    
    current_published_status = 0
    consecutive_block_count = 0 
    
    while True:
        try:
            await global_pause_event.wait()
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")

            is_success, result = await share_single_post(session, tk, ck, post, current_published_status)
            
            if is_success:
                async with lock:
                    success_count += 1
                    current_success_count = success_count
                
                consecutive_block_count = 0 
                
                print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {Y}Total: {current_success_count}{RESET}")
                continue

            else:
                consecutive_block_count += 1
                error_message = result 
                
                if consecutive_block_count == 1:
                    next_published_status = 1 if current_published_status == 0 else 0
                    
                    print(f" {Y}[RETRY]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {Y}Switching status...{RESET}")
                    current_published_status = next_published_status
                    continue
                
                elif consecutive_block_count == 2:
                    current_published_status = 0
                    
                    print(f" {R}[BLOCKED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}Triggering global pause for all accounts{RESET}")
                    
                    api_request("POST", "/share/set-global-pause", {"minutes": 30})
                    
                    global_pause_event.clear()
                    
                    await show_countdown(1800)
                    
                    global_pause_event.set()
                    consecutive_block_count = 0
                    print(f" {G}[RESUMED]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {G}All accounts resumed{RESET}")
                    continue

                print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}{error_message[:30]}{RESET}")
                await asyncio.sleep(5)

        except Exception as e:
            print(f" {R}[EXCEPTION]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}{str(e)[:40]}{RESET}")
            await asyncio.sleep(30)

async def auto_share_main(link):
    """Main auto share function with database paired account loading."""
    global success_count, global_pause_event
    success_count = 0
    global_pause_event.set()
    
    refresh_screen()
    print(f" {G}[!] CHECKING COOLDOWN STATUS...{RESET}")
    nice_loader("CHECKING")
    
    status, response = api_request("POST", "/share/start")
    
    if status == 429:
        refresh_screen()
        cooldown_type = response.get('cooldownType', 'unknown')
        
        if cooldown_type == 'global_pause':
            print(f" {R}⚠ GLOBAL PAUSE ACTIVE ⚠{RESET}")
            print(f" {R}All accounts are blocked due to Facebook restrictions{RESET}")
            print(LINE)
            print(f" {Y}This is different from plan cooldown!{RESET}")
            print(f" {Y}All your accounts are paused until the block expires.{RESET}")
            print(LINE)
            print(f" {R}Remaining Time: {response.get('remainingSeconds', 0)}s{RESET}")
            print(f" {Y}Available At: {W}{response.get('cooldownEnd', 'N/A')}{RESET}")
            print(LINE)
        else:
            print(f" {Y}[PLAN COOLDOWN ACTIVE]{RESET}")
            print(LINE)
            print(f" {Y}You must wait before starting another share session.{RESET}")
            print(f" {Y}This is based on your subscription plan.{RESET}")
            print(LINE)
            print(f" {R}Remaining Time: {response.get('remainingSeconds', 0)}s{RESET}")
            print(f" {Y}Available At: {W}{response.get('cooldownEnd', 'N/A')}{RESET}")
            print(LINE)
            print(f" {C}[PLAN INFO]{RESET}")
            print(f" {Y}Your Plan: {W}{user_data['plan'].upper()}{RESET}")
            
            if user_data['plan'] == 'free':
                print(f" {Y}Upgrade to VIP for 1 minute cooldown{RESET}")
                print(f" {Y}Upgrade to MAX for no cooldown{RESET}")
            elif user_data['plan'] == 'vip':
                print(f" {Y}Upgrade to MAX for no cooldown{RESET}")
            
            print(LINE)
        
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {G}[!] INITIALIZING AUTO SHARE...{RESET}")
    nice_loader("LOADING")
    
    async with aiohttp.ClientSession() as session:
        refresh_screen()
        print(f" {G}[!] EXTRACTING POST ID...{RESET}")
        nice_loader("EXTRACTING")
        
        post = await getid(session, link)
        if not post:
            print(f" {R}[ERROR] Failed to get post ID{RESET}")
            input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
            return
        
        refresh_screen()
        print(f" {G}[SUCCESS] Post ID: {post}{RESET}")
        print(LINE)
        
        print(f" {G}[!] LOADING PAIRED ACCOUNTS FROM DATABASE...{RESET}")
        nice_loader("LOADING")
        
        account_status, account_response = api_request("GET", "/user/accounts")
        if account_status != 200 or not account_response.get('success'):
            print(f" {R}[ERROR] Failed to load accounts from database{RESET}")
            print(f" {Y}[TIP] Use option 4 to add paired accounts{RESET}")
            input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
            return
        
        accounts_data = account_response.get('accounts', [])
        if not accounts_data:
            print(f" {R}[ERROR] No paired accounts stored in database{RESET}")
            print(f" {Y}[TIP] Use option 4 to add paired accounts (Cookie + Token){RESET}")
            input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
            return
        
        refresh_screen()
        print(f" {G}[SUCCESS] Loaded {len(accounts_data)} paired accounts from database{RESET}")
        print(LINE)
        
        print(f" {G}[FACEBOOK ACCOUNTS]{RESET}")
        print(LINE)
        for i, acc in enumerate(accounts_data, 1):
            print(f" {W}[{i}]{RESET} {Y}{acc['name']}{RESET} {W}-{RESET} {C}UID: {acc['uid']}{RESET}")
        print(LINE)
        
        print(f" {G}[!] FETCHING PAGE TOKENS...{RESET}")
        nice_loader("FETCHING")
        
        list_pages = []
        total_pages = 0
        for acc in accounts_data:
            token = acc['token']
            cookie = acc['cookie']
            token_data = await get_token(session, token, cookie)
            
            if 'data' in token_data:
                pages_found = 0
                for page in token_data['data']:
                    list_pages.append({
                        "tk": page["access_token"], 
                        "page_id": page["id"],
                        "ck": cookie
                    })
                    pages_found += 1
                total_pages += pages_found
                print(f" {B}[!] Found {R}{pages_found}{RESET} {M}pages from {Y}{acc['name']}{RESET}")
        
        if not list_pages:
            print(f" {R}[ERROR] No Pages found from accounts{RESET}")
            input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
            return
        
        refresh_screen()
        print(f" {M}[SHARE CONFIGURATION]{RESET}")
        print(LINE)
        print(f" {Y}Total Page Tokens: {G}{total_pages}{RESET}")
        print(f" {Y}Share Speed: {G}MAXIMUM (ZERO DELAYS){RESET}")
        print(f" {Y}Independent Threads: {G}{len(list_pages)}{RESET}")
        print(f" {Y}Your Plan: {G}{user_data['plan'].upper()}{RESET}")
        print(f" {Y}Pause Mode: {C}SYNCHRONIZED (All accounts pause together){RESET}")
        print(LINE)
        print(f" {G}[!] STARTING CONTINUOUS SHARING...{RESET}")
        print(f" {Y}[TIP] Press Ctrl+C to stop{RESET}")
        print(LINE)
        
        tasks = []
        for page in list_pages:
            task = asyncio.create_task(share_loop(
                session, 
                page["tk"], 
                page["ck"], 
                post, 
                page["page_id"]
            ))
            tasks.append(task)
        
        print(f" {G}[STARTED] Running {len(tasks)} parallel share threads at MAXIMUM SPEED (ZERO DELAYS)...{RESET}")
        print(LINE)
        
        await asyncio.gather(*tasks)

def start_auto_share():
    """Entry point for auto share feature (PAGE & NORM ACC)."""
    refresh_screen()
    print(f" {G}[!] ENTER POST LINK OR ID (Leave empty to back){RESET}")
    
    prompt = f" {W}[{W}➤{W}]{RESET} {C}POST LINK/ID {W}➤{RESET} "
    
    try:
        link = input(prompt)
    except KeyboardInterrupt:
        return
    
    if not link.strip():
        return
    
    try:
        asyncio.run(auto_share_main(link))
    except KeyboardInterrupt:
        refresh_screen()
        print(f" {Y}[!] AUTO SHARE STOPPED BY USER{RESET}")
        stop_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f" {Y}[!] Stop Time: {stop_time}{RESET}")
        print(f" {G}[!] Total Successful Shares: {success_count}{RESET}")
        print(LINE)
        
        if success_count > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count})
            print(f" {G}[!] Shares recorded to your account{RESET}")
        
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
    except Exception as e:
        refresh_screen()
        print(f" {R}[ERROR] An unexpected error occurred:{RESET}")
        print(f" {R}{str(e)}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ AUTO SHARE V2 FUNCTIONS (NORM ACC) ============

def extract_post_id_from_link(link):
    """Extract post ID from Facebook link or return as-is if already an ID."""
    link = link.strip()
    
    # Check if it's already a numeric ID
    if link.isdigit():
        return link
    
    # Remove protocol and www
    link = re.sub(r'^https?://', '', link)
    link = re.sub(r'^(www\.|m\.)', '', link)
    
    # Try to extract ID from various Facebook URL formats
    patterns = [
        r'facebook\.com/.*?/posts/(\d+)',
        r'facebook\.com/.*?/photos/.*?/(\d+)',
        r'facebook\.com/permalink\.php\?story_fbid=(\d+)',
        r'facebook\.com/story\.php\?story_fbid=(\d+)',
        r'facebook\.com/photo\.php\?fbid=(\d+)',
        r'/(\d+)/?$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    
    return link

def cookie_to_eaag_token(cookie):
    """Convert cookie to EAAG token using business.facebook.com."""
    headers = {
        'authority': 'business.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'referer': 'https://www.facebook.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }
    
    try:
        response = requests.get('https://business.facebook.com/content_management', headers=headers, timeout=10)
        home_business = response.text
        
        token = home_business.split('EAAG')[1].split('","')[0]
        return f'EAAG{token}'
    except:
        return None

async def share_with_eaag_v2(session, cookie, token, post_id):
    """Share a post using EAAG token with delay between 0.5-0.6 seconds."""
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'connection': 'keep-alive',
        'content-length': '0',
        'cookie': cookie,
        'host': 'graph.facebook.com'
    }
    
    try:
        url = f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{post_id}&published=0&access_token={token}'
        async with session.post(url, headers=headers) as response:
            json_data = await response.json()
            
            if 'id' in json_data:
                return True, json_data.get('id', 'N/A')
            else:
                error_msg = json_data.get('error', {}).get('message', 'Unknown error')
                return False, error_msg
    except Exception as e:
        return False, str(e)

async def share_loop_v2(session, cookie, token, post_id, account_index):
    """
    Continuous sharing loop for V2 with 0.5-0.6 second delays.
    """
    global success_count_v2
    
    while True:
        try:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            is_success, result = await share_with_eaag_v2(session, cookie, token, post_id)
            
            if is_success:
                async with lock_v2:
                    success_count_v2 += 1
                    current_success_count = success_count_v2
                
                print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}Account #{account_index}{RESET} {W}|{RESET} {Y}Total: {current_success_count}{RESET}")
                
                # Random delay between 0.5-0.6 seconds
                delay = random.uniform(0.5, 0.6)
                await asyncio.sleep(delay)
            else:
                error_message = result
                print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}Account #{account_index}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                await asyncio.sleep(5)
        
        except Exception as e:
            print(f" {R}[EXCEPTION]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}Account #{account_index}{RESET} {W}|{RESET} {R}{str(e)[:40]}{RESET}")
            await asyncio.sleep(30)

async def auto_share_v2_main(link_or_id):
    """Main auto share V2 function using cookies and EAAG tokens."""
    global success_count_v2, eaag_tokens
    success_count_v2 = 0
    eaag_tokens = []
    
    refresh_screen()
    print(f" {C}[!] LOADING COOKIES FROM FILE...{RESET}")
    
    # Ask for cookie file
    cookie_file = input(f" {W}[{W}➤{W}]{RESET} {C}COOKIE FILE PATH {W}➤{RESET} ").strip()
    
    if not cookie_file or not os.path.exists(cookie_file):
        print(f" {R}[ERROR] Cookie file not found!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Read cookies from file
    try:
        with open(cookie_file, 'r') as f:
            cookies = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f" {R}[ERROR] Failed to read cookie file: {e}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    if not cookies:
        print(f" {R}[ERROR] No cookies found in file!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {G}[SUCCESS] Loaded {len(cookies)} cookies{RESET}")
    print(LINE)
    print(f" {G}[!] CONVERTING COOKIES TO EAAG TOKENS...{RESET}")
    nice_loader("CONVERTING")
    
    # Convert all cookies to EAAG tokens
    for i, cookie in enumerate(cookies, 1):
        token = cookie_to_eaag_token(cookie)
        if token:
            eaag_tokens.append({
                'cookie': cookie,
                'token': token,
                'index': i
            })
            print(f" {G}[{i}/{len(cookies)}]{RESET} Token extracted successfully")
        else:
            print(f" {R}[{i}/{len(cookies)}]{RESET} Failed to extract token")
    
    if not eaag_tokens:
        print(f" {R}[ERROR] No valid EAAG tokens extracted!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {G}[SUCCESS] Extracted {len(eaag_tokens)} EAAG tokens from {len(cookies)} cookies{RESET}")
    print(LINE)
    
    # Extract post ID
    post_id = extract_post_id_from_link(link_or_id)
    print(f" {G}[POST ID] {post_id}{RESET}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        refresh_screen()
        print(f" {M}[SHARE V2 CONFIGURATION]{RESET}")
        print(LINE)
        print(f" {Y}Total Accounts: {G}{len(eaag_tokens)}{RESET}")
        print(f" {Y}Share Speed: {C}0.5-0.6 seconds delay per share{RESET}")
        print(f" {Y}Mode: {C}NORM ACC (EAAG Tokens){RESET}")
        print(f" {Y}Post ID: {G}{post_id}{RESET}")
        print(LINE)
        print(f" {G}[!] STARTING AUTO SHARE V2...{RESET}")
        print(f" {Y}[TIP] Press Ctrl+C to stop{RESET}")
        print(LINE)
        
        tasks = []
        for acc in eaag_tokens:
            task = asyncio.create_task(share_loop_v2(
                session,
                acc['cookie'],
                acc['token'],
                post_id,
                acc['index']
            ))
            tasks.append(task)
        
        print(f" {G}[STARTED] Running {len(tasks)} parallel share threads with 0.5-0.6s delays...{RESET}")
        print(LINE)
        
        await asyncio.gather(*tasks)

def start_auto_share_v2():
    """Entry point for auto share V2 feature (NORM ACC)."""
    refresh_screen()
    print(f" {C}[AUTO SHARE V2 - NORM ACC]{RESET}")
    print(LINE)
    print(f" {Y}This mode uses cookies to extract EAAG tokens{RESET}")
    print(f" {Y}Share delay: 0.5-0.6 seconds per share{RESET}")
    print(LINE)
    
    link_or_id = input(f" {W}[{W}➤{W}]{RESET} {C}POST LINK OR ID {W}➤{RESET} ").strip()
    
    if not link_or_id:
        return
    
    try:
        asyncio.run(auto_share_v2_main(link_or_id))
    except KeyboardInterrupt:
        refresh_screen()
        print(f" {Y}[!] AUTO SHARE V2 STOPPED BY USER{RESET}")
        stop_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f" {Y}[!] Stop Time: {stop_time}{RESET}")
        print(f" {G}[!] Total Successful Shares: {success_count_v2}{RESET}")
        print(LINE)
        
        if success_count_v2 > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count_v2})
            print(f" {G}[!] Shares recorded to your account{RESET}")
        
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
    except Exception as e:
        refresh_screen()
        print(f" {R}[ERROR] An unexpected error occurred:{RESET}")
        print(f" {R}{str(e)}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ MAIN FUNCTION ============

def main():
    global user_token, user_data
    
    while True:
        refresh_screen()
        
        prompt = f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} "
        try:
            choice = input(prompt).upper()
        except KeyboardInterrupt:
            sys.exit()

        refresh_screen()

        if not user_token:
            if choice in ['1', '01', 'A']:
                login_user()
            elif choice in ['2', '02', 'B']:
                register_user()
            elif choice in ['0', '00', 'X']:
                print(f"\n {R}[!] EXITING TOOL...{RESET}")
                sys.exit()
            else:
                print(f"\n {R}[!] INVALID SELECTION{RESET}")
                time.sleep(0.8)
        else:
            if choice in ['1', '01', 'A']:
                start_auto_share()
            
            elif choice in ['2', '02', 'B']:
                start_auto_share_v2()
                
            elif choice in ['3', '03', 'C']:
                cookie_to_token_tool()
                
            elif choice in ['4', '04', 'D']:
                manage_cookie_token()
                
            elif choice in ['5', '05', 'E']:
                show_user_stats()
            
            elif choice in ['6', '06', 'F']:
                if user_data and user_data.get('isAdmin'):
                    admin_panel()
                else:
                    update_tool_logic()
            
            elif choice in ['7', '07', 'G']:
                if user_data and user_data.get('isAdmin'):
                    update_tool_logic()
                else:
                    print(f"\n {R}[!] INVALID SELECTION{RESET}")
                    time.sleep(0.8)
                
            elif choice in ['0', '00', 'X']:
                print(f"\n {Y}[!] LOGGING OUT...{RESET}")
                user_token = None
                user_data = None
                time.sleep(1)
                
            else:
                print(f"\n {R}[!] INVALID SELECTION{RESET}")
                time.sleep(0.8)

if __name__ == "__main__":
    main()
