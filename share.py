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
import uuid

# --- NEON COLOR PALETTE ---
R = '\033[1;31m'   # Red (Bold)
G = '\033[1;32m'   # Green (Bold)
C = '\033[1;36m'   # Cyan (Bold)
Y = '\033[1;33m'   # Yellow (Bold)
M = '\033[1;35m'   # Magenta (Bold)
B = '\033[1;34m'   # Blue (Bold)
W = '\033[1;37m'   # White (Bold)
BG_R = '\033[41m'  # Red Background
BG_G = '\033[42m'  # Green Background
BG_C = '\033[46m'  # Cyan Background
BG_M = '\033[45m'  # Magenta Background
BG_Y = '\033[43m'  # Yellow Background
BG_B = '\033[44m'  # Blue Background
BG_W = '\033[47m'  # White Background
BLACK = '\033[30m' # Black text
RESET = '\033[0m'  # Reset

# --- UI CONSTANTS ---
LINE = f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

# --- API CONFIGURATION ---
API_URL = "https://rpwtools.onrender.com/api"
user_token = None
user_data = None

# --- GLOBAL VARIABLES ---
success_count = 0
success_count_v2 = 0
pages_created_count = 0
lock = asyncio.Lock()
lock_v2 = asyncio.Lock()
global_pause_event = asyncio.Event()
global_pause_event.set()
eaag_tokens = []

# --- PAGE NAME GENERATORS ---
PAGE_NAME_PREFIXES = ["The", "Amazing", "Best", "Super", "Ultra", "Pro", "Elite", "Prime", "Top", "Royal", "Golden", "Silver", "Diamond", "Crystal", "Magic", "Digital", "Smart", "Fast", "Quick", "Easy", "Fresh", "New", "Modern", "Classic", "Premium", "Luxury", "Expert", "Master", "Power", "Max"]
PAGE_NAME_WORDS = ["Shop", "Store", "Market", "Hub", "Zone", "Center", "Place", "Spot", "World", "Planet", "Galaxy", "Universe", "Kingdom", "Empire", "Nation", "Land", "City", "Town", "Village", "House", "Home", "Room", "Space", "Studio", "Lab", "Factory", "Works", "Co", "Inc", "Group", "Team", "Squad", "Crew", "Club", "Society", "Community", "Network", "Connect", "Link", "Bridge", "Tech", "Digital", "Online", "Web", "Net", "Cloud", "Data", "Info", "Media", "News", "Blog", "Channel", "Stream", "Cast", "Show", "Live", "Now", "Today", "Daily", "Weekly"]
PAGE_NAME_SUFFIXES = ["Official", "PH", "USA", "Global", "International", "Worldwide", "Online", "24/7", "Express", "Direct", "Plus", "Pro", "VIP", "Premium", "Gold", "Platinum", "Elite", "Supreme", "Ultimate", "Extreme", "2024", "2025", "New", "Fresh", "Hot", "Trending", "Viral", "Popular", "Famous", "Best"]
PAGE_CATEGORIES = [{"id": "2214", "name": "Public Figure"}, {"id": "2200", "name": "Community"}, {"id": "1601", "name": "Business"}, {"id": "2612", "name": "Entertainment"}, {"id": "2500", "name": "Brand"}, {"id": "2301", "name": "Local Business"}, {"id": "2707", "name": "Musician/Band"}, {"id": "2600", "name": "TV Show"}, {"id": "2603", "name": "Movie"}, {"id": "2606", "name": "Sports Team"}, {"id": "2611", "name": "Artist"}, {"id": "2700", "name": "Comedian"}, {"id": "1900", "name": "Product/Service"}, {"id": "2201", "name": "Organization"}, {"id": "2210", "name": "Personal Blog"}]

def clear():
    os.system('clear')

def normalize_facebook_url(url):
    if not url:
        return url
    url = url.strip()
    url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
    url = re.sub(r'^(www\.|m\.)', '', url, flags=re.IGNORECASE)
    if not url.startswith('facebook.com'):
        if '/' not in url:
            url = f'facebook.com/{url}'
    return url

def generate_random_page_name():
    style = random.randint(1, 5)
    if style == 1:
        name = f"{random.choice(PAGE_NAME_PREFIXES)} {random.choice(PAGE_NAME_WORDS)} {random.choice(PAGE_NAME_SUFFIXES)}"
    elif style == 2:
        name = f"{random.choice(PAGE_NAME_WORDS)} {random.choice(PAGE_NAME_WORDS)}"
    elif style == 3:
        name = f"{random.choice(PAGE_NAME_PREFIXES)} {random.choice(PAGE_NAME_WORDS)}"
    elif style == 4:
        name = f"{random.choice(PAGE_NAME_WORDS)} {random.choice(PAGE_NAME_SUFFIXES)}"
    else:
        name = f"{random.choice(PAGE_NAME_PREFIXES)} {random.choice(PAGE_NAME_WORDS)} {random.randint(1, 999)}"
    unique_id = ''.join(random.choices('0123456789', k=random.randint(2, 4)))
    if random.random() > 0.5:
        name = f"{name} {unique_id}"
    return name

def get_random_category():
    return random.choice(PAGE_CATEGORIES)

def banner_header():
    print(f"""{C}
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    {RESET}""")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'GITHUB':<13} {W}➤{RESET} {G}RYO GRAHHH{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    tool_name = f"{R}[ {BG_R}{W}RPWTOOLS{RESET}{R} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL\\'S NAME':<13} {W}➤{RESET} {tool_name}")
    
    if user_data:
        print(LINE)
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'USERNAME':<13} {W}➤{RESET} {G}{user_data['username'].upper()}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}{user_data.get('facebook', 'N/A')}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COUNTRY':<13} {W}➤{RESET} {G}{user_data.get('country', 'N/A').upper()}{RESET}")
        
        user_plan = user_data['plan']
        if user_plan == 'max':
            plan_display = f"{M}[ {BG_M}{W}MAX{RESET}{M} ]{RESET}"
        elif user_plan == 'vip':
            plan_display = f"{G}[ {BG_G}{W}VIP{RESET}{G} ]{RESET}"
        else:
            plan_display = f"{W}[ {BG_W}{BLACK}FREE{RESET}{W} ]{RESET}"
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN':<13} {W}➤{RESET} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN EXPIRY IN':<13} {W}➤{RESET} {Y}{user_data['planExpiry']}{RESET}")
        
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PAIRED ACC':<13} {W}➤{RESET} {C}{user_data.get('accountCount', 0)}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ALL COOKIES':<13} {W}➤{RESET} {C}{user_data.get('allCookies', 0)}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ALL TOKENS':<13} {W}➤{RESET} {C}{user_data.get('allTokens', 0)}{RESET}")
    print(LINE)

def menu_item(num, letter, text, color, bg_color, desc=""):
    bracket_display = f"{bg_color}{W}[{num}/{letter}]{RESET}"
    padding = 22 - len(text)
    if padding < 1:
        padding = 1
    if desc:
        return f" {bracket_display} {color}{text}{RESET}{' ' * padding}{W}—{RESET} {W}{desc}{RESET}"
    else:
        return f" {bracket_display} {color}{text}{RESET}"

def show_menu():
    if not user_token:
        print(menu_item("01", "A", "LOGIN", G, BG_G))
        print(menu_item("02", "B", "REGISTER", C, BG_C))
        print(menu_item("00", "X", "EXIT", R, BG_R))
    elif user_data and user_data.get('isAdmin'):
        print(menu_item("01", "A", "AUTO SHARE", G, BG_G, "PAGE & NORM ACCOUNTS"))
        print(menu_item("02", "B", "AUTO SHARE V2", C, BG_C, "NORMAL ACCOUNTS"))
        print(menu_item("03", "C", "AUTO CREATE PAGE", M, BG_M, "FB PAGE CREATOR"))
        print(menu_item("04", "D", "COOKIE TO TOKEN", Y, BG_Y, "CONVERT"))
        print(menu_item("05", "E", "MANAGE ACCOUNTS", B, BG_B, "COOKIE & TOKEN"))
        print(menu_item("06", "F", "MY STATS", C, BG_C, "VIEW STATISTICS"))
        print(menu_item("07", "G", "ADMIN PANEL", M, BG_M, "MANAGE USERS"))
        print(menu_item("08", "H", "UPDATE TOOL", G, BG_G, "CHECK UPDATES"))
        print(menu_item("00", "X", "LOGOUT", R, BG_R))
    else:
        print(menu_item("01", "A", "AUTO SHARE", G, BG_G, "PAGE & NORM ACCOUNTS"))
        print(menu_item("02", "B", "AUTO SHARE V2", C, BG_C, "NORMAL ACCOUNTS"))
        print(menu_item("03", "C", "AUTO CREATE PAGE", M, BG_M, "FB PAGE CREATOR"))
        print(menu_item("04", "D", "COOKIE TO TOKEN", Y, BG_Y, "CONVERT"))
        print(menu_item("05", "E", "MANAGE ACCOUNTS", B, BG_B, "COOKIE & TOKEN"))
        print(menu_item("06", "F", "MY STATS", C, BG_C, "VIEW STATISTICS"))
        print(menu_item("07", "G", "UPDATE TOOL", G, BG_G, "CHECK UPDATES"))
        print(menu_item("00", "X", "LOGOUT", R, BG_R))
    print(LINE)

def refresh_screen():
    clear()
    banner_header()
    show_menu()

def nice_loader(text="PROCESSING"):
    sys.stdout.write("\033[?25l")
    filled, empty, width = "■", "□", 20
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

def get_country_from_ip():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            return response.json().get('country', 'Unknown')
    except:
        pass
    return 'Unknown'

def api_request(method, endpoint, data=None, use_token=True):
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
        return None, "Cannot connect to server."
    except requests.exceptions.Timeout:
        return None, "Request timeout."
    except Exception as e:
        return None, f"Error: {str(e)}"

def login_user():
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
    status, response = api_request("POST", "/auth/login", {"username": username, "password": password}, use_token=False)
    if status == 200 and response.get('success'):
        user_token = response.get('token')
        user_data = response.get('user')
        print(f" {G}[SUCCESS] Login successful!{RESET}")
        print(LINE)
        print(f" {Y}Welcome back, {G}{user_data['username'].upper()}{RESET}")
        print(f" {Y}Plan: {G}{user_data['plan'].upper()}{RESET}")
        if user_data.get('isAdmin'):
            print(f" {M}[ADMIN ACCESS GRANTED]{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] {response if isinstance(response, str) else response.get('message', 'Login failed')}{RESET}")
        print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def register_user():
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
    status, response = api_request("POST", "/auth/register", {"username": username, "password": password, "facebook": facebook, "country": country}, use_token=False)
    if status == 201 and response.get('success'):
        user_token = response.get('token')
        user_data = response.get('user')
        print(f" {G}[SUCCESS] Registration successful!{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] {response if isinstance(response, str) else response.get('message', 'Registration failed')}{RESET}")
        print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def show_user_stats():
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
        print(f" {Y}Plan: {G}{stats['plan'].upper()}{RESET}")
        print(f" {Y}Total Shares: {G}{stats['totalShares']}{RESET}")
        print(f" {Y}Total Cookie Converts: {G}{stats['totalCookieConverts']}{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] Failed to get stats{RESET}")
        print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def manage_cookie_token():
    while True:
        refresh_screen()
        print(f" {G}[MANAGE COOKIE & TOKEN]{RESET}")
        print(LINE)
        print(menu_item("01", "A", "VIEW ALL ACCOUNTS", G, BG_G))
        print(menu_item("02", "B", "ADD ACCOUNT", C, BG_C, "Cookie + Token"))
        print(menu_item("03", "C", "DELETE ACCOUNT", R, BG_R))
        print(menu_item("04", "D", "DELETE ALL", R, BG_R, "ALL ACCOUNTS"))
        print(menu_item("00", "X", "BACK", Y, BG_Y))
        print(LINE)
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip().upper()
        if choice in ['1', '01', 'A']:
            view_accounts()
        elif choice in ['2', '02', 'B']:
            add_account()
        elif choice in ['3', '03', 'C']:
            delete_account()
        elif choice in ['4', '04', 'D']:
            delete_all_accounts()
        elif choice in ['0', '00', 'X']:
            return

def view_accounts():
    refresh_screen()
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
                print(LINE)
    else:
        print(f" {R}[ERROR] Failed to load accounts{RESET}")
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def add_account():
    refresh_screen()
    print(f" {G}[ADD ACCOUNT]{RESET}")
    print(LINE)
    cookie = input(f" {W}[{W}➤{W}]{RESET} {C}COOKIE {W}➤{RESET} ").strip()
    if not cookie:
        return
    token = input(f" {W}[{W}➤{W}]{RESET} {C}TOKEN {W}➤{RESET} ").strip()
    if not token:
        return
    nice_loader("VALIDATING")
    status, response = api_request("POST", "/user/accounts", {"cookie": cookie, "token": token})
    if status == 200 and response.get('success'):
        print(f" {G}[SUCCESS] Account added!{RESET}")
        if user_data:
            user_data['accountCount'] = response.get('totalAccounts', 0)
    else:
        print(f" {R}[ERROR] Failed to add account{RESET}")
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_account():
    refresh_screen()
    nice_loader("LOADING")
    status, response = api_request("GET", "/user/accounts")
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load accounts{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    accounts = response.get('accounts', [])
    if not accounts:
        print(f" {Y}No accounts to delete.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    refresh_screen()
    print(f" {R}[DELETE ACCOUNT]{RESET}")
    print(LINE)
    for i, acc in enumerate(accounts, 1):
        print(f" {W}[{i}]{RESET} {M}{acc['name']}{RESET}")
    print(LINE)
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT NUMBER (0 to cancel) {W}➤{RESET} ").strip()
    if not choice or choice == '0':
        return
    try:
        acc_index = int(choice) - 1
        if 0 <= acc_index < len(accounts):
            nice_loader("DELETING")
            status, response = api_request("DELETE", f"/user/accounts/{accounts[acc_index]['id']}")
            if status == 200 and response.get('success'):
                print(f" {G}[SUCCESS] Account deleted!{RESET}")
    except:
        pass
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_all_accounts():
    refresh_screen()
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R}Delete ALL accounts? (YES/NO) {W}➤{RESET} ").strip().upper()
    if confirm != 'YES':
        return
    nice_loader("DELETING")
    status, response = api_request("DELETE", "/user/accounts")
    if status == 200 and response.get('success'):
        print(f" {G}[SUCCESS] All accounts deleted!{RESET}")
        if user_data:
            user_data['accountCount'] = 0
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def cookie_to_token_tool():
    nice_loader("LAUNCHING")
    while True:
        refresh_screen()
        print(f" {G}[!] ENTER COOKIE TO CONVERT (Leave empty to back){RESET}")
        try:
            cookie = input(f" {W}[{W}➤{W}]{RESET} {C}COOKIE {W}➤{RESET} ")
        except KeyboardInterrupt:
            return
        if not cookie.strip():
            return
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
                print(f" {R}[FAILED] {json_data.get('error', 'Unknown Error')}{RESET}")
        except:
            print(f" {R}[ERROR] Network Connection Failed.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONVERT ANOTHER]{RESET}")

def update_tool_logic():
    print(f" {G}[!] CHECKING FOR UPDATES...{RESET}")
    nice_loader("CHECKING")
    print(f" {G}[!] UPDATE COMPLETE. RESTARTING...{RESET}")
    time.sleep(1)
    os.execv(sys.executable, ['python'] + sys.argv)

def admin_panel():
    while True:
        refresh_screen()
        print(f" {M}[ADMIN PANEL]{RESET}")
        print(LINE)
        print(menu_item("01", "A", "VIEW ALL USERS", G, BG_G))
        print(menu_item("02", "B", "CHANGE USER PLAN", Y, BG_Y))
        print(menu_item("03", "C", "DELETE USER", R, BG_R))
        print(menu_item("00", "X", "BACK", Y, BG_Y))
        print(LINE)
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip().upper()
        if choice in ['1', '01', 'A']:
            view_all_users()
        elif choice in ['2', '02', 'B']:
            change_user_plan()
        elif choice in ['3', '03', 'C']:
            delete_user()
        elif choice in ['0', '00', 'X']:
            return

def view_all_users():
    refresh_screen()
    nice_loader("LOADING")
    status, response = api_request("GET", "/admin/users")
    if status == 200 and response.get('success'):
        users = response.get('users', [])
        refresh_screen()
        print(f" {G}[ALL USERS] Total: {len(users)}{RESET}")
        print(LINE)
        for i, user in enumerate(users, 1):
            print(f" {W}[{i:02d}]{RESET} {C}{user['username'].upper()}{RESET} - {G}{user['plan'].upper()}{RESET}")
        print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def change_user_plan():
    refresh_screen()
    status, response = api_request("GET", "/admin/users")
    if status != 200:
        return
    users = response.get('users', [])
    for i, user in enumerate(users, 1):
        print(f" {W}[{i}]{RESET} {C}{user['username'].upper()}{RESET}")
    print(LINE)
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT USER NUMBER {W}➤{RESET} ").strip()
    if not choice:
        return
    try:
        user_index = int(choice) - 1
        if 0 <= user_index < len(users):
            selected_user = users[user_index]
            print(f"\n {W}[1]{RESET} FREE  {W}[2]{RESET} VIP  {W}[3]{RESET} MAX")
            plan_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT PLAN {W}➤{RESET} ").strip()
            plan_map = {'1': 'free', '2': 'vip', '3': 'max'}
            if plan_choice in plan_map:
                nice_loader("UPDATING")
                api_request("PUT", f"/admin/users/{selected_user['username']}/plan", {"plan": plan_map[plan_choice]})
                print(f" {G}[SUCCESS] Plan updated!{RESET}")
    except:
        pass
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_user():
    refresh_screen()
    status, response = api_request("GET", "/admin/users")
    if status != 200:
        return
    users = response.get('users', [])
    for i, user in enumerate(users, 1):
        print(f" {W}[{i}]{RESET} {C}{user['username'].upper()}{RESET}")
    print(LINE)
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT USER NUMBER {W}➤{RESET} ").strip()
    if not choice:
        return
    try:
        user_index = int(choice) - 1
        if 0 <= user_index < len(users):
            confirm = input(f" {R}Delete this user? (YES/NO) {W}➤{RESET} ").strip().upper()
            if confirm == 'YES':
                nice_loader("DELETING")
                api_request("DELETE", f"/admin/users/{users[user_index]['username']}")
                print(f" {G}[SUCCESS] User deleted!{RESET}")
    except:
        pass
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ AUTO CREATE FB PAGE ============

def create_facebook_page(access_token, page_name, category_id="2214"):
    client_trace_id = str(uuid.uuid4())
    post_data = {
        'method': 'post', 'pretty': 'false', 'format': 'json', 'server_timestamps': 'true', 'locale': 'en_US', 'purpose': 'fetch',
        'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'fb_api_caller_class': 'graphservice', 'client_doc_id': '11994080423068421059028841356',
        'variables': json.dumps({"params": {"params": json.dumps({"params": json.dumps({"client_input_params": {"cp_upsell_declined": 0, "category_ids": [category_id], "profile_plus_id": "0", "page_id": "0"}, "server_params": {"INTERNAL__latency_qpl_instance_id": 40168896100127, "screen": "category", "referrer": "pages_tab_launch_point", "name": page_name, "creation_source": "android", "INTERNAL__latency_qpl_marker_id": 36707139, "variant": 5}})}), "bloks_versioning_id": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec", "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"}, "scale": "1.5", "nt_context": {"styles_id": "e6c6f61b7a86cdf3fa2eaaffa982fbd1", "using_white_navbar": True, "pixel_ratio": 1.5, "is_push_on": True, "bloks_version": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec"}}),
        'fb_api_analytics_tags': '["GraphServices"]', 'client_trace_id': client_trace_id
    }
    headers = {
        'authorization': f'OAuth {access_token}',
        'user-agent': '[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;FBDM/{density=1.5,width=720,height=1244};FBLC/en_US;FBRV/0;FBCR/T-Mobile;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-N976N;FBSV/7.1.2;FBOP/1;FBCA/x86:armeabi-v7a;]',
        'content-type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post("https://graph.facebook.com/graphql", data=post_data, headers=headers, timeout=30)
        response_json = response.json()
        if 'data' in response_json:
            success_res = str(response_json)
            if 'Cannot create Page' in success_res or 'too many Pages' in success_res:
                return {'success': False, 'message': "Rate limited", 'rate_limited': True}
            return {'success': True, 'message': "Page created!"}
        return {'success': False, 'message': "Failed"}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def show_countdown_timer(seconds, message="Next page creation in"):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        sys.stdout.write(f"\r {Y}[WAITING]{RESET} {message}: {G}{mins:02d}:{secs:02d}{RESET} | {C}Press Ctrl+C to stop{RESET}    ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

def auto_create_page_loop(token, account_name):
    global pages_created_count
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            page_name = generate_random_page_name()
            category = get_random_category()
            print(f" {Y}[CREATING]{RESET} | {M}{current_time}{RESET} | {B}{account_name}{RESET}")
            print(f"           | Name: {C}{page_name}{RESET}")
            print(f"           | Category: {C}{category['name']}{RESET}")
            result = create_facebook_page(token, page_name, category['id'])
            if result['success']:
                pages_created_count += 1
                print(f" {G}[SUCCESS]{RESET} | {M}{current_time}{RESET} | {G}Page Created!{RESET} | {Y}Total: {pages_created_count}{RESET}")
                print(LINE)
                show_countdown_timer(300, "Next page creation in")
            elif result.get('rate_limited'):
                print(f" {R}[RATE LIMITED]{RESET} | Waiting 10 minutes...")
                print(LINE)
                show_countdown_timer(600, "Retry in")
            else:
                print(f" {R}[FAILED]{RESET} | {result['message'][:50]}")
                print(LINE)
                time.sleep(30)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f" {R}[ERROR]{RESET} | {str(e)[:50]}")
            time.sleep(60)

def start_auto_create_page():
    global pages_created_count
    pages_created_count = 0
    refresh_screen()
    print(f" {M}[AUTO CREATE FB PAGE]{RESET}")
    print(LINE)
    nice_loader("LOADING")
    status, response = api_request("GET", "/user/accounts")
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load accounts{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    accounts = response.get('accounts', [])
    if not accounts:
        print(f" {R}[ERROR] No accounts stored{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    refresh_screen()
    print(f" {M}[SELECT ACCOUNT]{RESET}")
    print(LINE)
    for i, acc in enumerate(accounts, 1):
        letter = chr(64 + i) if i <= 26 else str(i)
        print(menu_item(f"{i:02d}", letter, acc['name'], C, BG_C, f"UID: {acc['uid']}"))
    print(menu_item("00", "X", "CANCEL", R, BG_R))
    print(LINE)
    selection = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT ACCOUNT {W}➤{RESET} ").strip().upper()
    if not selection or selection in ['0', '00', 'X']:
        return
    selected = None
    try:
        if selection.isdigit():
            idx = int(selection) - 1
            if 0 <= idx < len(accounts):
                selected = accounts[idx]
        elif len(selection) == 1 and selection.isalpha():
            idx = ord(selection) - 65
            if 0 <= idx < len(accounts):
                selected = accounts[idx]
    except:
        pass
    if not selected:
        print(f" {R}[ERROR] Invalid selection{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    refresh_screen()
    print(f" {Y}[CONFIRM]{RESET}")
    print(LINE)
    print(f" Account: {M}{selected['name']}{RESET}")
    print(f" Interval: {G}Every 5 minutes{RESET}")
    print(f" Names: {G}Auto-generated{RESET}")
    print(f" Categories: {G}Auto-selected{RESET}")
    print(LINE)
    confirm = input(f" {W}[{W}➤{W}]{RESET} {Y}Start? (Y/N) {W}➤{RESET} ").strip().upper()
    if confirm != 'Y':
        return
    refresh_screen()
    print(f" {G}[!] STARTING AUTO PAGE CREATION...{RESET}")
    print(f" {Y}[TIP] Press Ctrl+C to stop{RESET}")
    print(LINE)
    try:
        auto_create_page_loop(selected['token'], selected['name'])
    except KeyboardInterrupt:
        refresh_screen()
        print(f" {Y}[!] STOPPED BY USER{RESET}")
        print(f" {G}[!] Total Pages Created: {pages_created_count}{RESET}")
        print(LINE)
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ AUTO SHARE FUNCTIONS ============

def extract_post_id_from_link(link):
    link = link.strip()
    if link.isdigit():
        return link
    link = re.sub(r'^https?://', '', link)
    link = re.sub(r'^(www\.|m\.)', '', link)
    patterns = [r'facebook\.com/.*?/posts/(\d+)', r'facebook\.com/.*?/photos/.*?/(\d+)', r'facebook\.com/permalink\.php\?story_fbid=(\d+)', r'facebook\.com/share/p/([A-Za-z0-9]+)', r'/(\d+)/?$']
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return link

def cookie_to_eaag_token(cookie):
    headers = {'authority': 'business.facebook.com', 'cookie': cookie, 'user-agent': 'Mozilla/5.0'}
    try:
        response = requests.get('https://business.facebook.com/content_management', headers=headers, timeout=10)
        token = response.text.split('EAAG')[1].split('","')[0]
        return f'EAAG{token}'
    except:
        return None

async def getid(session, link):
    extracted_id = extract_post_id_from_link(link)
    if extracted_id.isdigit():
        return extracted_id
    try:
        async with session.post('https://id.traodoisub.com/api.php', data={"link": link}) as response:
            rq = await response.json()
            if 'success' in rq:
                return rq["id"]
    except:
        pass
    return None

async def get_token(session, token, cookie):
    try:
        async with session.get(f'https://graph.facebook.com/me/accounts?access_token={token}') as r:
            rq = await r.json()
            return rq if 'data' in rq else {}
    except:
        return {}

async def share_single_post(session, tk, ck, post, published_value):
    try:
        async with session.get(f'https://graph.facebook.com/me/feed?method=POST&link=https://m.facebook.com/{post}&published={published_value}&access_token={tk}') as response:
            json_data = await response.json()
            if 'id' in json_data:
                return True, json_data.get('id', 'N/A')
            return False, json_data.get('error', {}).get('message', 'Unknown')
    except Exception as e:
        return False, str(e)

async def show_countdown(seconds):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        sys.stdout.write(f"\r {Y}[PAUSED]{RESET} | Resuming in: {G}{mins:02d}:{secs:02d}{RESET} | {C}Ctrl+C to stop{RESET}")
        sys.stdout.flush()
        await asyncio.sleep(1)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

async def share_loop(session, tk, ck, post, page_id):
    global success_count, global_pause_event
    current_published_status = 0
    consecutive_block_count = 0
    while True:
        try:
            await global_pause_event.wait()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            is_success, result = await share_single_post(session, tk, ck, post, current_published_status)
            if is_success:
                async with lock:
                    success_count += 1
                print(f" {G}[SUCCESS]{RESET} | {M}{current_time}{RESET} | {B}{page_id}{RESET} | {Y}Total: {success_count}{RESET}")
                consecutive_block_count = 0
            else:
                consecutive_block_count += 1
                if consecutive_block_count == 1:
                    current_published_status = 1 if current_published_status == 0 else 0
                elif consecutive_block_count >= 2:
                    global_pause_event.clear()
                    await show_countdown(1800)
                    global_pause_event.set()
                    consecutive_block_count = 0
                else:
                    await asyncio.sleep(5)
        except Exception as e:
            await asyncio.sleep(30)

async def auto_share_v1_main(link):
    global success_count, global_pause_event
    success_count = 0
    global_pause_event.set()
    async with aiohttp.ClientSession() as session:
        post = await getid(session, link)
        if not post:
            print(f" {R}[ERROR] Failed to get post ID{RESET}")
            return
        status, response = api_request("GET", "/user/accounts")
        if status != 200:
            print(f" {R}[ERROR] Failed to load accounts{RESET}")
            return
        accounts = response.get('accounts', [])
        if not accounts:
            print(f" {R}[ERROR] No accounts{RESET}")
            return
        list_pages = []
        for acc in accounts:
            token_data = await get_token(session, acc['token'], acc['cookie'])
            if 'data' in token_data:
                for page in token_data['data']:
                    list_pages.append({"tk": page["access_token"], "page_id": page["id"], "ck": acc['cookie']})
        if not list_pages:
            print(f" {R}[ERROR] No pages found{RESET}")
            return
        print(f" {G}[STARTED] Running {len(list_pages)} threads...{RESET}")
        print(LINE)
        tasks = [asyncio.create_task(share_loop(session, p["tk"], p["ck"], post, p["page_id"])) for p in list_pages]
        await asyncio.gather(*tasks)

async def share_with_eaag_v2(session, cookie, token, post_id):
    try:
        url = f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{post_id}&published=0&access_token={token}'
        async with session.post(url) as response:
            json_data = await response.json()
            if 'id' in json_data:
                return True, json_data.get('id')
            return False, json_data.get('error', {}).get('message', 'Unknown')
    except Exception as e:
        return False, str(e)

async def share_loop_v2(session, cookie, token, post_id, account_name):
    global success_count_v2
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            is_success, result = await share_with_eaag_v2(session, cookie, token, post_id)
            if is_success:
                async with lock_v2:
                    success_count_v2 += 1
                print(f" {G}[SUCCESS]{RESET} | {M}{current_time}{RESET} | {B}{account_name}{RESET} | {Y}Total: {success_count_v2}{RESET}")
                await asyncio.sleep(random.uniform(0.5, 0.6))
            else:
                print(f" {R}[ERROR]{RESET} | {M}{current_time}{RESET} | {result[:40]}")
                await asyncio.sleep(5)
        except:
            await asyncio.sleep(30)

async def auto_share_v2_main(link):
    global success_count_v2, eaag_tokens
    success_count_v2 = 0
    eaag_tokens = []
    status, response = api_request("GET", "/user/accounts")
    if status != 200:
        print(f" {R}[ERROR] Failed to load accounts{RESET}")
        return
    accounts = response.get('accounts', [])
    if not accounts:
        print(f" {R}[ERROR] No accounts{RESET}")
        return
    refresh_screen()
    print(f" {C}[SELECT COOKIES]{RESET}")
    print(LINE)
    for i, acc in enumerate(accounts, 1):
        print(f" {W}[{i}]{RESET} {M}{acc['name']}{RESET}")
    print(LINE)
    selection = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT (comma separated or ALL) {W}➤{RESET} ").strip().upper()
    if not selection:
        return
    selected = []
    if selection == 'ALL':
        selected = accounts
    else:
        for s in selection.split(','):
            try:
                idx = int(s.strip()) - 1
                if 0 <= idx < len(accounts):
                    selected.append(accounts[idx])
            except:
                pass
    if not selected:
        return
    print(f" {G}[!] Converting {len(selected)} cookies to EAAG tokens...{RESET}")
    for acc in selected:
        token = cookie_to_eaag_token(acc['cookie'])
        if token:
            eaag_tokens.append({'cookie': acc['cookie'], 'token': token, 'name': acc['name']})
            print(f" {G}✓{RESET} {acc['name']}")
        else:
            print(f" {R}✗{RESET} {acc['name']}")
    if not eaag_tokens:
        print(f" {R}[ERROR] No valid tokens{RESET}")
        return
    async with aiohttp.ClientSession() as session:
        post_id = await getid(session, link)
        if not post_id:
            print(f" {R}[ERROR] Failed to get post ID{RESET}")
            return
        print(f" {G}[STARTED] Running {len(eaag_tokens)} threads...{RESET}")
        print(LINE)
        tasks = [asyncio.create_task(share_loop_v2(session, t['cookie'], t['token'], post_id, t['name'])) for t in eaag_tokens]
        await asyncio.gather(*tasks)

def start_auto_share_v1():
    refresh_screen()
    print(f" {G}[AUTO SHARE - PAGE & NORM ACCOUNTS]{RESET}")
    print(LINE)
    link = input(f" {W}[{W}➤{W}]{RESET} {C}POST LINK/ID {W}➤{RESET} ").strip()
    if not link:
        return
    try:
        asyncio.run(auto_share_v1_main(link))
    except KeyboardInterrupt:
        print(f"\n {Y}[!] STOPPED | Total: {success_count}{RESET}")
        if success_count > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count})
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def start_auto_share_v2():
    refresh_screen()
    print(f" {C}[AUTO SHARE V2 - NORMAL ACCOUNTS]{RESET}")
    print(LINE)
    link = input(f" {W}[{W}➤{W}]{RESET} {C}POST LINK/ID {W}➤{RESET} ").strip()
    if not link:
        return
    try:
        asyncio.run(auto_share_v2_main(link))
    except KeyboardInterrupt:
        print(f"\n {Y}[!] STOPPED | Total: {success_count_v2}{RESET}")
        if success_count_v2 > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count_v2})
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ MAIN ============

def main():
    global user_token, user_data
    while True:
        refresh_screen()
        try:
            choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").upper()
        except KeyboardInterrupt:
            sys.exit()
        refresh_screen()
        if not user_token:
            if choice in ['1', '01', 'A']:
                login_user()
            elif choice in ['2', '02', 'B']:
                register_user()
            elif choice in ['0', '00', 'X']:
                print(f"\n {R}[!] EXITING...{RESET}")
                sys.exit()
        else:
            if choice in ['1', '01', 'A']:
                start_auto_share_v1()
            elif choice in ['2', '02', 'B']:
                start_auto_share_v2()
            elif choice in ['3', '03', 'C']:
                start_auto_create_page()
            elif choice in ['4', '04', 'D']:
                cookie_to_token_tool()
            elif choice in ['5', '05', 'E']:
                manage_cookie_token()
            elif choice in ['6', '06', 'F']:
                show_user_stats()
            elif choice in ['7', '07', 'G']:
                if user_data and user_data.get('isAdmin'):
                    admin_panel()
                else:
                    update_tool_logic()
            elif choice in ['8', '08', 'H']:
                if user_data and user_data.get('isAdmin'):
                    update_tool_logic()
            elif choice in ['0', '00', 'X']:
                print(f"\n {Y}[!] LOGGING OUT...{RESET}")
                user_token = None
                user_data = None
                time.sleep(1)

if __name__ == "__main__":
    main()
