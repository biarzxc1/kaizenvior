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
BG_G = '\033[42m'  # Green Background
BG_C = '\033[46m'  # Cyan Background
BG_M = '\033[45m'  # Magenta Background
BG_Y = '\033[43m'  # Yellow Background
BG_B = '\033[44m'  # Blue Background
RESET = '\033[0m' # Reset

# --- UI CONSTANTS ---
LINE = f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

# --- API CONFIGURATION ---
API_URL = "https://rpwtools.onrender.com/api"  # Render server URL
TOKEN_API_URL = "https://kazuxapi.vercel.app"  # Token converter API
user_token = None
user_data = None

# --- GLOBAL VARIABLES FOR AUTO SHARE (PAGE & NORM ACC) ---
success_count = 0
lock = asyncio.Lock()
global_pause_event = asyncio.Event()
global_pause_event.set()  # Initially not paused

# --- GLOBAL VARIABLES FOR AUTO SHARE V2 (NORM ACC) ---
success_count_v2 = 0
lock_v2 = asyncio.Lock()

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
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0{RESET}")
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
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PAIRED ACC':<13} {W}➤{RESET} {C}{account_count}{RESET}")
    
    print(LINE)

def show_menu():
    """Prints the Menu Options with colored background numbers."""
    if not user_token:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}LOGIN{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}REGISTER{RESET}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R}EXIT{RESET}")
    elif user_data and user_data.get('isAdmin'):
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}AUTO SHARE              — PAGE & NORM{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}AUTO SHARE V2           — NORM ACCOUNTS{RESET}")
        print(f" {W}[{RESET}{BG_M}{W}03{RESET}{BG_M}{Y}/{RESET}{BG_M}{W}C{RESET}{W}]{RESET} {M}COOKIE TO TOKEN         — CONVERT{RESET}")
        print(f" {W}[{RESET}{BG_Y}{W}04{RESET}{BG_Y}{Y}/{RESET}{BG_Y}{W}D{RESET}{W}]{RESET} {Y}MANAGE COOKIE & TOKEN   — DATABASE{RESET}")
        print(f" {W}[{RESET}{BG_B}{W}05{RESET}{BG_B}{Y}/{RESET}{BG_B}{W}E{RESET}{W}]{RESET} {B}MY STATS                — STATISTICS{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}06{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}F{RESET}{W}]{RESET} {C}AUTO CREATE PAGES       — FROM DATABASE{RESET}")
        print(f" {W}[{RESET}{BG_M}{W}07{RESET}{BG_M}{Y}/{RESET}{BG_M}{W}G{RESET}{W}]{RESET} {M}ADMIN PANEL             — MANAGEMENT{RESET}")
        print(f" {W}[{RESET}{BG_G}{W}08{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}H{RESET}{W}]{RESET} {G}UPDATE TOOL             — LATEST VERSION{RESET}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R}LOGOUT{RESET}")
    else:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}AUTO SHARE              — PAGE & NORM{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}AUTO SHARE V2           — NORM ACCOUNTS{RESET}")
        print(f" {W}[{RESET}{BG_M}{W}03{RESET}{BG_M}{Y}/{RESET}{BG_M}{W}C{RESET}{W}]{RESET} {M}COOKIE TO TOKEN         — CONVERT{RESET}")
        print(f" {W}[{RESET}{BG_Y}{W}04{RESET}{BG_Y}{Y}/{RESET}{BG_Y}{W}D{RESET}{W}]{RESET} {Y}MANAGE COOKIE & TOKEN   — DATABASE{RESET}")
        print(f" {W}[{RESET}{BG_B}{W}05{RESET}{BG_B}{Y}/{RESET}{BG_B}{W}E{RESET}{W}]{RESET} {B}MY STATS                — STATISTICS{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}06{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}F{RESET}{W}]{RESET} {C}AUTO CREATE PAGES       — FROM DATABASE{RESET}")
        print(f" {W}[{RESET}{BG_G}{W}07{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}G{RESET}{W}]{RESET} {G}UPDATE TOOL             — LATEST VERSION{RESET}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R}LOGOUT{RESET}")
    
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

def select_progress_display():
    """Let user choose progress display mode"""
    refresh_screen()
    print(f" {C}[SHARING PROGRESS DISPLAY]{RESET}")
    print(LINE)
    print(f" {Y}Choose how you want to see sharing progress:{RESET}")
    print(LINE)
    print(f" {W}[{RESET}{BG_G}{W}1{RESET}{W}]{RESET} {G}SUCCESS COUNTER (1/100){RESET}")
    print(f"     {Y}• Best for smaller screens (mobile){RESET}")
    print(f"     {Y}• Shows only success count{RESET}")
    print(f"     {Y}• Minimal display, stays in one place{RESET}")
    print(f"     {Y}• No spam, just countdown style{RESET}")
    print(LINE)
    print(f" {W}[{RESET}{BG_C}{W}2{RESET}{W}]{RESET} {C}DETAILED LOGS{RESET}")
    print(f"     {Y}• Best for larger screens (desktop){RESET}")
    print(f"     {Y}• Shows success, time, page ID, total{RESET}")
    print(f"     {Y}• Full process information{RESET}")
    print(f"     {Y}• Scrolling log display{RESET}")
    print(LINE)
    
    while True:
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE (1 or 2) {W}➤{RESET} ").strip()
        
        if choice == '1':
            return 'minimal'
        elif choice == '2':
            return 'detailed'
        else:
            print(f" {R}[!] Invalid choice. Please enter 1 or 2{RESET}")
            time.sleep(1)
            sys.stdout.write("\033[F\033[K")  # Move up and clear line
            sys.stdout.flush()

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
    else:
        print(f" {R}[ERROR] Failed to delete accounts{RESET}")
    
    print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def cookie_to_token_tool():
    """Cookie to token converter with cooldown check and spam prevention"""
    nice_loader("LAUNCHING")

    # Track converted cookies to prevent spam
    converted_cookies = {}

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
        
        print(f" {G}[!] COOKIE TO TOKEN CONVERTER{RESET}")
        print(LINE)
        print(f" {Y}⚠ WARNING: Do not spam the same cookie multiple times!{RESET}")
        print(f" {Y}⚠ Spamming can cause your account to be locked or suspended!{RESET}")
        print(LINE)
        print(f" {C}[!] Enter cookie to convert (Leave empty to back){RESET}")
        
        prompt = f" {W}[{W}➤{W}]{RESET} {C}COOKIE {W}➤{RESET} "
        
        try:
            cookie = input(prompt)
        except KeyboardInterrupt:
            return

        if not cookie.strip():
            return

        # Check if this cookie was recently converted (within last 5 minutes)
        cookie_hash = str(hash(cookie.strip()))[:16]
        current_time = time.time()
        
        if cookie_hash in converted_cookies:
            last_convert_time = converted_cookies[cookie_hash]
            time_diff = current_time - last_convert_time
            
            if time_diff < 300:  # 5 minutes = 300 seconds
                remaining = int(300 - time_diff)
                refresh_screen()
                print(f" {R}[SPAM PROTECTION]{RESET}")
                print(LINE)
                print(f" {Y}This cookie was recently converted!{RESET}")
                print(f" {Y}Please wait {R}{remaining}s{Y} before converting again.{RESET}")
                print(LINE)
                print(f" {C}This prevents account suspension from spam requests.{RESET}")
                print(LINE)
                input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
                continue

        refresh_screen() 
        nice_loader("EXTRACTING") 

        try:
            encoded_cookie = urllib.parse.quote(cookie.strip())
            url = f"{TOKEN_API_URL}/{encoded_cookie}"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read().decode('utf-8')
                json_data = json.loads(data)
                
            if json_data.get("success"):
                # Mark this cookie as converted
                converted_cookies[cookie_hash] = current_time
                
                print(f" {G}[SUCCESS] TOKENS GENERATED:{RESET}")
                print(LINE)
                
                tokens = json_data.get("tokens", {})
                
                # Show only EAAAAU token prominently
                eaaaau_token = tokens.get("EAAAAU")
                if eaaaau_token:
                    print(f" {G}✓ EAAAAU (RECOMMENDED FOR AUTO SHARE):{RESET}")
                    print(f" {W}{eaaaau_token}{RESET}")
                    print(LINE)
                
                # Show other tokens in collapsed format
                print(f" {C}[OTHER AVAILABLE TOKENS]{RESET}")
                for app_name, token in tokens.items():
                    if app_name != "EAAAAU":
                        if token:
                            print(f" {Y}{app_name}: {W}{token[:30]}...{RESET}")
                        else:
                            print(f" {Y}{app_name}: {R}No Token Found{RESET}")
                print(LINE)
                
                api_request("POST", "/cookie/convert")
            else:
                error = json_data.get("error", "Unknown Error")
                print(f" {R}[FAILED] {error}{RESET}")
                print(LINE)
                
        except Exception as e:
            print(f" {R}[ERROR] {str(e)}{RESET}")
            print(LINE)

        print(f" {Y}[TIP] Press ENTER to convert another cookie or leave empty to go back{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def update_tool_logic():
    """Simulates an update and restarts the script."""
    print(f" {G}[!] CHECKING FOR UPDATES...{RESET}")
    nice_loader("CHECKING")
    
    print(f" {G}[!] NEW VERSION FOUND! DOWNLOADING...{RESET}")
    nice_loader("UPDATING")
    
    print(f" {G}[!] UPDATE COMPLETE. RESTARTING...{RESET}")
    time.sleep(1)
    
    os.execv(sys.executable, ['python'] + sys.argv)

# ============ AUTO CREATE PAGE FUNCTIONS ============

def create_facebook_page_api(access_token, page_name):
    """
    Create a Facebook page using the Graph API
    
    Args:
        access_token (str): EAAAAU access token
        page_name (str): Full name of page to create
    
    Returns:
        dict: Response containing success status, message, and page_id/uid
    """
    import uuid
    
    # Generate unique client trace ID
    client_trace_id = str(uuid.uuid4())
    
    # Prepare POST data
    post_data = {
        'method': 'post',
        'pretty': 'false',
        'format': 'json',
        'server_timestamps': 'true',
        'locale': 'en_US',
        'purpose': 'fetch',
        'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'fb_api_caller_class': 'graphservice',
        'client_doc_id': '11994080423068421059028841356',
        'variables': json.dumps({
            "params": {
                "params": json.dumps({
                    "params": json.dumps({
                        "client_input_params": {
                            "cp_upsell_declined": 0,
                            "category_ids": ["2214"],
                            "profile_plus_id": "0",
                            "page_id": "0"
                        },
                        "server_params": {
                            "INTERNAL__latency_qpl_instance_id": 40168896100127,
                            "screen": "category",
                            "referrer": "pages_tab_launch_point",
                            "name": page_name,
                            "creation_source": "android",
                            "INTERNAL__latency_qpl_marker_id": 36707139,
                            "variant": 5
                        }
                    })
                }),
                "bloks_versioning_id": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec",
                "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"
            },
            "scale": "1.5",
            "nt_context": {
                "styles_id": "e6c6f61b7a86cdf3fa2eaaffa982fbd1",
                "using_white_navbar": True,
                "pixel_ratio": 1.5,
                "is_push_on": True,
                "bloks_version": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec"
            }
        }),
        'fb_api_analytics_tags': '["GraphServices"]',
        'client_trace_id': client_trace_id
    }
    
    # Prepare headers
    headers = {
        'x-fb-request-analytics-tags': '{"network_tags":{"product":"350685531728","purpose":"fetch","request_category":"graphql","retry_attempt":"0"},"application_tags":"graphservice"}',
        'x-fb-ta-logging-ids': f'graphql:{client_trace_id}',
        'x-fb-rmd': 'state=URL_ELIGIBLE',
        'x-fb-sim-hni': '31016',
        'x-fb-net-hni': '31016',
        'authorization': f'OAuth {access_token}',
        'x-graphql-request-purpose': 'fetch',
        'user-agent': '[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;FBDM/{density=1.5,width=720,height=1244};FBLC/en_US;FBRV/0;FBCR/T-Mobile;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-N976N;FBSV/7.1.2;FBOP/1;FBCA/x86:armeabi-v7a;]',
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-connection-type': 'WIFI',
        'x-fb-background-state': '1',
        'x-fb-friendly-name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'x-graphql-client-library': 'graphservice',
        'x-fb-privacy-context': '3643298472347298',
        'x-fb-device-group': '3543',
        'x-tigon-is-retry': 'False',
        'priority': 'u=3,i',
        'x-fb-http-engine': 'Liger',
        'x-fb-client-ip': 'True',
        'x-fb-server-cluster': 'True'
    }
    
    url = "https://graph.facebook.com/graphql"
    
    try:
        # Make the request
        response = requests.post(
            url,
            data=post_data,
            headers=headers,
            timeout=30,
            verify=True
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        response_json = response.json()
        
        # Check for success
        if 'data' in response_json and response_json['data']:
            success_res = response_json['data'].get('fb_bloks_action', {}).get('root_action', {}).get('action', {}).get('action_bundle', {}).get('bloks_bundle_action', '')
            
            if 'Cannot create Page: You have created too many Pages in a short time' in str(success_res):
                return {
                    'success': False,
                    'message': "Cannot create Page: You have created too many Pages in a short time"
                }
            else:
                # Try to extract page ID/UID from response
                page_id = None
                try:
                    # Look for page ID in the response
                    response_str = json.dumps(response_json)
                    if 'page_id' in response_str:
                        import re
                        page_id_match = re.search(r'"page_id["\s:]+(\d+)"', response_str)
                        if page_id_match:
                            page_id = page_id_match.group(1)
                except:
                    pass
                
                return {
                    'success': True,
                    'message': "Page created successfully!",
                    'page_id': page_id,
                    'response': response_json
                }
        else:
            return {
                'success': False,
                'message': f"Unexpected response format"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f"Request error: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'message': f"JSON decode error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        }

def auto_create_pages():
    """Auto create Facebook pages using tokens from database with cooldown"""
    refresh_screen()
    print(f" {G}[!] LOADING PAIRED ACCOUNTS...{RESET}")
    nice_loader("LOADING")
    
    # Get accounts from database
    status, response = api_request("GET", "/user/accounts")
    
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load accounts from database{RESET}")
        print(f" {Y}[TIP] Use option 4 to add paired accounts first{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    accounts = response.get('accounts', [])
    
    if not accounts:
        print(f" {R}[ERROR] No accounts stored in database{RESET}")
        print(f" {Y}[TIP] Add paired accounts first (Cookie + Token){RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {G}[AUTO CREATE FACEBOOK PAGES]{RESET}")
    print(LINE)
    print(f" {Y}Available Accounts: {C}{len(accounts)}{RESET}")
    print(LINE)
    
    # Display accounts
    for i, acc in enumerate(accounts, 1):
        letter = chr(64 + i) if i <= 26 else str(i)
        print(f" {W}[{RESET}{BG_C}{W}{i:02d}{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}{letter}{RESET}{W}]{RESET} {M}{acc['name']}{RESET} {W}({C}UID: {acc['uid']}{W}){RESET}")
    
    print(LINE)
    print(f" {Y}[!] Each page creation has a 5-minute cooldown{RESET}")
    print(LINE)
    
    # Select account
    acc_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT ACCOUNT (0 to cancel) {W}➤{RESET} ").strip().upper()
    
    if not acc_choice or acc_choice == '0':
        return
    
    # Handle both number and letter selection
    selected_acc = None
    try:
        if acc_choice.isdigit():
            acc_index = int(acc_choice) - 1
            if 0 <= acc_index < len(accounts):
                selected_acc = accounts[acc_index]
        elif len(acc_choice) == 1 and acc_choice.isalpha():
            acc_index = ord(acc_choice) - 65
            if 0 <= acc_index < len(accounts):
                selected_acc = accounts[acc_index]
    except:
        pass
    
    if not selected_acc:
        print(f" {R}[ERROR] Invalid selection{RESET}")
        time.sleep(1)
        return
    
    # Ask for page name mode
    refresh_screen()
    print(f" {C}[PAGE NAME MODE]{RESET}")
    print(LINE)
    print(f" {W}[{RESET}{BG_G}{W}1{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}Auto-generate page names{RESET}")
    print(f" {W}[{RESET}{BG_C}{W}2{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}Enter page names manually{RESET}")
    print(LINE)
    
    mode_choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip().upper()
    
    auto_generate = mode_choice in ['1', 'A']
    
    # Track last creation time for cooldown
    last_creation_time = 0
    pages_created = 0
    
    # For auto-generated names
    import random
    import string
    
    def generate_page_name():
        """Generate a random page name"""
        prefixes = ["Business", "Store", "Shop", "Official", "Brand", "Company", "Enterprise", "Corp"]
        suffixes = ["Page", "Hub", "Center", "Online", "Digital", "Group", "Team", "Pro"]
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        return f"{random.choice(prefixes)} {random_str} {random.choice(suffixes)}"
    
    while True:
        refresh_screen()
        print(f" {G}[AUTO CREATE PAGE] - Account: {M}{selected_acc['name']}{RESET}")
        print(LINE)
        print(f" {Y}Pages Created This Session: {G}{pages_created}{RESET}")
        print(LINE)
        
        # Check cooldown
        current_time = time.time()
        time_since_last = current_time - last_creation_time
        
        if last_creation_time > 0 and time_since_last < 300:  # 5 minutes = 300 seconds
            remaining = int(300 - time_since_last)
            
            print(f" {Y}[COOLDOWN ACTIVE]{RESET}")
            print(LINE)
            print(f" {R}Please wait before creating another page{RESET}")
            print(LINE)
            
            # Countdown display
            for i in range(remaining, 0, -1):
                mins, secs = divmod(i, 60)
                timer = f"{mins:02d}:{secs:02d}"
                sys.stdout.write(f"\r {C}[Creating page again in {timer}]{RESET} {W}Please wait...{RESET}")
                sys.stdout.flush()
                time.sleep(1)
            
            sys.stdout.write(f"\r{' ' * 70}\r")
            sys.stdout.flush()
            
            refresh_screen()
            print(f" {G}[AUTO CREATE PAGE] - Account: {M}{selected_acc['name']}{RESET}")
            print(LINE)
            print(f" {Y}Pages Created This Session: {G}{pages_created}{RESET}")
            print(LINE)
        
        # Get page name based on mode
        if auto_generate:
            page_name = generate_page_name()
            print(f" {G}[AUTO-GENERATED PAGE NAME]{RESET}")
            print(LINE)
            print(f" {Y}Page Name: {C}{page_name}{RESET}")
            print(LINE)
            print(f" {Y}Press ENTER to create this page or type 'exit' to stop{RESET}")
            
            user_input = input(f" {W}[{W}➤{W}]{RESET} ").strip().lower()
            
            if user_input == 'exit':
                break
        else:
            print(f" {C}[!] Enter page name (leave empty to exit){RESET}")
            page_name = input(f" {W}[{W}➤{W}]{RESET} {C}PAGE NAME {W}➤{RESET} ").strip()
            
            if not page_name:
                break
        
        # Create page
        refresh_screen()
        print(f" {G}[!] CREATING FACEBOOK PAGE...{RESET}")
        nice_loader("CREATING")
        
        result = create_facebook_page_api(selected_acc['token'], page_name)
        
        refresh_screen()
        
        if result['success']:
            pages_created += 1
            last_creation_time = time.time()
            
            print(f" {G}[SUCCESS] {result['message']}{RESET}")
            print(LINE)
            print(f" {Y}Page Name: {G}{page_name}{RESET}")
            
            if result.get('page_id'):
                print(f" {Y}Page UID: {C}{result['page_id']}{RESET}")
            
            print(f" {Y}Total Created: {G}{pages_created}{RESET}")
            print(LINE)
            print(f" {C}[!] You can create another page in 5 minutes{RESET}")
            print(LINE)
        else:
            print(f" {R}[FAILED] {result['message']}{RESET}")
            print(LINE)
            
            if "too many Pages" in result['message']:
                print(f" {Y}[!] Facebook has limited your page creation{RESET}")
                print(f" {Y}[!] Please wait and try again later{RESET}")
                print(LINE)
        
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

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
            print(f"      Paired Accounts: {C}{user.get('accountCount', 0)}{RESET}")
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

def get_eaaaau_token_from_cookie(cookie):
    """Get EAAAAU token from cookie using API."""
    try:
        encoded_cookie = urllib.parse.quote(cookie.strip())
        url = f"{TOKEN_API_URL}/{encoded_cookie}"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode('utf-8')
            json_data = json.loads(data)
            
        if json_data.get("success"):
            tokens = json_data.get("tokens", {})
            return tokens.get("EAAAAU")
        return None
    except:
        return None

def create_facebook_page(access_token, page_name):
    """
    Create a Facebook page using the Graph API with EAAAU token
    
    Args:
        access_token (str): EAAAU access token
        page_name (str): Name of page to create
    
    Returns:
        dict: Response containing success status and page_id
    """
    import uuid
    
    # Generate unique client trace ID
    client_trace_id = str(uuid.uuid4())
    
    # Prepare POST data
    post_data = {
        'method': 'post',
        'pretty': 'false',
        'format': 'json',
        'server_timestamps': 'true',
        'locale': 'en_US',
        'purpose': 'fetch',
        'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'fb_api_caller_class': 'graphservice',
        'client_doc_id': '11994080423068421059028841356',
        'variables': json.dumps({
            "params": {
                "params": json.dumps({
                    "params": json.dumps({
                        "client_input_params": {
                            "cp_upsell_declined": 0,
                            "category_ids": ["2214"],
                            "profile_plus_id": "0",
                            "page_id": "0"
                        },
                        "server_params": {
                            "INTERNAL__latency_qpl_instance_id": 40168896100127,
                            "screen": "category",
                            "referrer": "pages_tab_launch_point",
                            "name": page_name,
                            "creation_source": "android",
                            "INTERNAL__latency_qpl_marker_id": 36707139,
                            "variant": 5
                        }
                    })
                }),
                "bloks_versioning_id": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec",
                "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"
            },
            "scale": "1.5",
            "nt_context": {
                "styles_id": "e6c6f61b7a86cdf3fa2eaaffa982fbd1",
                "using_white_navbar": True,
                "pixel_ratio": 1.5,
                "is_push_on": True,
                "bloks_version": "c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec"
            }
        }),
        'fb_api_analytics_tags': '["GraphServices"]',
        'client_trace_id': client_trace_id
    }
    
    # Prepare headers
    headers = {
        'x-fb-request-analytics-tags': '{"network_tags":{"product":"350685531728","purpose":"fetch","request_category":"graphql","retry_attempt":"0"},"application_tags":"graphservice"}',
        'x-fb-ta-logging-ids': f'graphql:{client_trace_id}',
        'x-fb-rmd': 'state=URL_ELIGIBLE',
        'x-fb-sim-hni': '31016',
        'x-fb-net-hni': '31016',
        'authorization': f'OAuth {access_token}',
        'x-graphql-request-purpose': 'fetch',
        'user-agent': '[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;FBDM/{density=1.5,width=720,height=1244};FBLC/en_US;FBRV/0;FBCR/T-Mobile;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-N976N;FBSV/7.1.2;FBOP/1;FBCA/x86:armeabi-v7a;]',
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-connection-type': 'WIFI',
        'x-fb-background-state': '1',
        'x-fb-friendly-name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'x-graphql-client-library': 'graphservice',
        'x-fb-privacy-context': '3643298472347298',
        'x-fb-device-group': '3543',
        'x-tigon-is-retry': 'False',
        'priority': 'u=3,i',
        'x-fb-http-engine': 'Liger',
        'x-fb-client-ip': 'True',
        'x-fb-server-cluster': 'True'
    }
    
    url = "https://graph.facebook.com/graphql"
    
    try:
        response = requests.post(url, data=post_data, headers=headers, timeout=30, verify=True)
        response.raise_for_status()
        response_json = response.json()
        
        if 'data' in response_json and response_json['data']:
            success_res = response_json['data'].get('fb_bloks_action', {}).get('root_action', {}).get('action', {}).get('action_bundle', {}).get('bloks_bundle_action', '')
            
            if 'Cannot create Page: You have created too many Pages in a short time' in str(success_res):
                return {
                    'success': False,
                    'message': 'Cannot create Page: You have created too many Pages in a short time'
                }
            else:
                # Try to extract page ID from response
                page_id = None
                try:
                    # Look for page ID in the response
                    response_str = json.dumps(response_json)
                    # Try to find page ID pattern
                    import re
                    page_id_match = re.search(r'"page_id["\s:]+(\d+)', response_str)
                    if page_id_match:
                        page_id = page_id_match.group(1)
                except:
                    pass
                
                return {
                    'success': True,
                    'message': 'Page created successfully!',
                    'page_id': page_id
                }
        else:
            return {
                'success': False,
                'message': f'Unexpected response format'
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }

def auto_create_pages():
    """Auto create Facebook pages using tokens from database with 5-minute cooldown."""
    refresh_screen()
    print(f" {G}[!] LOADING PAIRED ACCOUNTS...{RESET}")
    nice_loader("LOADING")
    
    # Get accounts from database
    status, response = api_request("GET", "/user/accounts")
    
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load accounts from database{RESET}")
        print(f" {Y}[TIP] Use option 4 to add paired accounts first{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    accounts = response.get('accounts', [])
    
    if not accounts:
        print(f" {R}[ERROR] No accounts found in database{RESET}")
        print(f" {Y}[TIP] Add paired accounts first using option 4{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {G}[AUTO CREATE PAGES]{RESET}")
    print(LINE)
    print(f" {Y}Found {G}{len(accounts)}{Y} account(s) in database{RESET}")
    print(LINE)
    
    # Display accounts
    for i, acc in enumerate(accounts, 1):
        print(f" {W}[{i}]{RESET} {M}{acc['name']}{RESET} {W}({C}UID: {acc['uid']}{W}){RESET}")
    
    print(LINE)
    print(f" {C}[!] SELECT ACCOUNT TO USE FOR PAGE CREATION{RESET}")
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT ACCOUNT NUMBER {W}➤{RESET} ").strip()
    
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(accounts):
        print(f" {R}[ERROR] Invalid selection{RESET}")
        time.sleep(1)
        return
    
    selected_account = accounts[int(choice) - 1]
    
    refresh_screen()
    print(f" {G}[AUTO CREATE PAGES]{RESET}")
    print(LINE)
    print(f" {Y}Selected Account: {M}{selected_account['name']}{RESET}")
    print(f" {Y}UID: {C}{selected_account['uid']}{RESET}")
    print(LINE)
    
    # Get number of pages to create
    print(f" {C}[!] HOW MANY PAGES DO YOU WANT TO CREATE?{RESET}")
    print(LINE)
    
    count_input = input(f" {W}[{W}➤{W}]{RESET} {C}NUMBER OF PAGES {W}➤{RESET} ").strip()
    
    if not count_input.isdigit() or int(count_input) < 1:
        print(f" {R}[ERROR] Invalid number{RESET}")
        time.sleep(1)
        return
    
    page_count = int(count_input)
    
    refresh_screen()
    print(f" {G}[AUTO CREATE PAGES]{RESET}")
    print(LINE)
    print(f" {Y}Account: {M}{selected_account['name']}{RESET}")
    print(f" {Y}Pages to Create: {G}{page_count}{RESET}")
    print(f" {Y}Cooldown: {R}5 minutes between each page{RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {Y}Start creating pages? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        return
    
    # Get the token
    token = selected_account['token']
    
    # Create pages
    created_pages = []
    failed_pages = []
    
    for i in range(1, page_count + 1):
        refresh_screen()
        print(f" {G}[AUTO CREATE PAGES]{RESET}")
        print(LINE)
        print(f" {Y}Progress: {G}{i}/{page_count}{RESET}")
        print(LINE)
        
        # Get page name
        page_name = input(f" {W}[{W}➤{W}]{RESET} {C}PAGE NAME #{i} {W}➤{RESET} ").strip()
        
        if not page_name:
            print(f" {R}[ERROR] Page name cannot be empty{RESET}")
            failed_pages.append({'page_number': i, 'reason': 'Empty name'})
            time.sleep(1)
            continue
        
        # Create the page
        refresh_screen()
        print(f" {G}[!] CREATING PAGE #{i}: {page_name}...{RESET}")
        nice_loader("CREATING")
        
        result = create_facebook_page(token, page_name)
        
        if result['success']:
            page_id = result.get('page_id', 'Unknown')
            created_pages.append({
                'number': i,
                'name': page_name,
                'page_id': page_id
            })
            
            refresh_screen()
            print(f" {G}[SUCCESS] Page #{i} created!{RESET}")
            print(LINE)
            print(f" {Y}Name: {M}{page_name}{RESET}")
            print(f" {Y}Page ID: {C}{page_id}{RESET}")
            print(LINE)
        else:
            failed_pages.append({
                'number': i,
                'name': page_name,
                'reason': result['message']
            })
            
            refresh_screen()
            print(f" {R}[FAILED] Page #{i} creation failed!{RESET}")
            print(LINE)
            print(f" {Y}Name: {M}{page_name}{RESET}")
            print(f" {R}Reason: {result['message']}{RESET}")
            print(LINE)
        
        # If not the last page, show countdown
        if i < page_count:
            print(f" {Y}[COOLDOWN] Next page creation in 5 minutes...{RESET}")
            print(LINE)
            
            # 5 minute countdown (300 seconds)
            for remaining in range(300, 0, -1):
                mins, secs = divmod(remaining, 60)
                timer = f"{mins:02d}:{secs:02d}"
                
                sys.stdout.write(f"\r {C}[CREATING PAGE AGAIN IN {timer}]{RESET} {W}Cooldown active...{RESET}")
                sys.stdout.flush()
                time.sleep(1)
            
            sys.stdout.write(f"\r{' ' * 80}\r")
            sys.stdout.flush()
    
    # Show final summary
    refresh_screen()
    print(f" {G}[AUTO CREATE PAGES - SUMMARY]{RESET}")
    print(LINE)
    print(f" {Y}Total Pages: {G}{page_count}{RESET}")
    print(f" {Y}Successfully Created: {G}{len(created_pages)}{RESET}")
    print(f" {Y}Failed: {R}{len(failed_pages)}{RESET}")
    print(LINE)
    
    if created_pages:
        print(f" {G}[CREATED PAGES]{RESET}")
        for page in created_pages:
            print(f" {W}[{page['number']}]{RESET} {M}{page['name']}{RESET} {W}({C}ID: {page['page_id']}{W}){RESET}")
        print(LINE)
    
    if failed_pages:
        print(f" {R}[FAILED PAGES]{RESET}")
        for page in failed_pages:
            print(f" {W}[{page['number']}]{RESET} {M}{page.get('name', 'N/A')}{RESET}")
            print(f"      Reason: {R}{page['reason']}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ POST ID EXTRACTION ============

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

# ============ AUTO SHARE FUNCTIONS (PAGE & NORM ACC) ============

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

async def share_loop(session, tk, ck, post, page_id, target=None, display_mode='detailed'):
    """
    Continuous sharing loop for a single page with display mode support.
    ZERO DELAY - Maximum speed with synchronized pause handling.
    """
    global success_count, global_pause_event
    
    current_published_status = 0
    consecutive_block_count = 0 
    page_count = 0  # Track count per page
    
    while True:
        # Check if target reached for this page
        if target and page_count >= target:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            if display_mode == 'minimal':
                sys.stdout.write(f"\r {G}[TARGET REACHED {page_count}/{target}]{RESET}                                          \n")
                sys.stdout.flush()
            else:
                print(f" {G}[TARGET REACHED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {Y}Completed: {page_count}/{target}{RESET}")
            break
        
        try:
            await global_pause_event.wait()
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")

            is_success, result = await share_single_post(session, tk, ck, post, current_published_status)
            
            if is_success:
                async with lock:
                    success_count += 1
                    current_success_count = success_count
                
                page_count += 1
                consecutive_block_count = 0 
                
                if display_mode == 'minimal':
                    # Minimal display - stay in one place
                    if target:
                        sys.stdout.write(f"\r {G}[SUCCESS SHARES {page_count}/{target}]{RESET} {W}|{RESET} {Y}Total: {current_success_count}{RESET}            ")
                    else:
                        sys.stdout.write(f"\r {G}[SUCCESS SHARES {current_success_count}]{RESET} {W}|{RESET} {C}Keep sharing...{RESET}            ")
                    sys.stdout.flush()
                else:
                    # Detailed display - full logs
                    if target:
                        print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {Y}Count: {page_count}/{target}{RESET} {W}|{RESET} {C}Total: {current_success_count}{RESET}")
                    else:
                        print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {Y}Total: {current_success_count}{RESET}")
                
                # ZERO DELAY - Continue immediately
                continue

            else:
                consecutive_block_count += 1
                error_message = result 
                
                if consecutive_block_count == 1:
                    next_published_status = 1 if current_published_status == 0 else 0
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[RETRY]{RESET} {W}|{RESET} {C}Switching status...{RESET}                         ")
                        sys.stdout.flush()
                    else:
                        print(f" {Y}[RETRY]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {Y}Switching status...{RESET}")
                    
                    current_published_status = next_published_status
                    continue
                
                elif consecutive_block_count == 2:
                    current_published_status = 0
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {R}[BLOCKED]{RESET} {W}|{RESET} {Y}Global pause triggered...{RESET}                    \n")
                        sys.stdout.flush()
                        time.sleep(2)
                    else:
                        print(f" {R}[BLOCKED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}Triggering global pause for all accounts{RESET}")
                    
                    api_request("POST", "/share/set-global-pause", {"minutes": 30})
                    
                    global_pause_event.clear()
                    
                    await show_countdown(1800)
                    
                    global_pause_event.set()
                    consecutive_block_count = 0
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {G}[RESUMED]{RESET} {W}|{RESET} {C}All accounts resumed{RESET}                        ")
                        sys.stdout.flush()
                    else:
                        print(f" {G}[RESUMED]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {G}All accounts resumed{RESET}")
                    continue

                if display_mode != 'minimal':
                    print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}{error_message[:30]}{RESET}")
                
                await asyncio.sleep(5)

        except Exception as e:
            if display_mode != 'minimal':
                print(f" {R}[EXCEPTION]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}{str(e)[:40]}{RESET}")
            await asyncio.sleep(30)
                    
                    global_pause_event.set()
                    consecutive_block_count = 0
                    print(f" {G}[RESUMED]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {G}All accounts resumed{RESET}")
                    continue

                print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}{error_message[:30]}{RESET}")
                await asyncio.sleep(5)

        except Exception as e:
            print(f" {R}[EXCEPTION]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{page_id}{RESET} {W}|{RESET} {R}{str(e)[:40]}{RESET}")
            await asyncio.sleep(30)

async def auto_share_page_mode(link):
    """PAGE & NORM ACC MODE - Uses paired accounts from database OR manual cookie input."""
    global success_count, global_pause_event
    
    refresh_screen()
    print(f" {G}[!] INITIALIZING AUTO SHARE (PAGE & NORM ACC MODE)...{RESET}")
    nice_loader("LOADING")
    
    async with aiohttp.ClientSession() as session:
        # Try to extract post ID directly first
        post = extract_post_id_from_link(link)
        
        # If extraction failed or looks like a full URL, try API method
        if not post.isdigit():
            refresh_screen()
            print(f" {G}[!] EXTRACTING POST ID FROM LINK...{RESET}")
            nice_loader("EXTRACTING")
            
            post = await getid(session, link)
            if not post:
                print(f" {R}[ERROR] Failed to get post ID{RESET}")
                input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
                return
        
        refresh_screen()
        print(f" {G}[SUCCESS] Post ID: {post}{RESET}")
        print(LINE)
        
        # Ask user if they want to use database accounts or enter manually
        print(f" {C}[!] CHOOSE INPUT METHOD:{RESET}")
        print(LINE)
        print(f" {W}[{RESET}{BG_G}{W}1{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}Use paired accounts from database{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}2{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}Enter cookies manually (auto-convert to tokens){RESET}")
        print(LINE)
        
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip().upper()
        
        accounts_data = []
        
        if choice in ['1', 'A']:
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
        
        elif choice in ['2', 'B']:
            refresh_screen()
            print(f" {C}[!] MANUAL COOKIE INPUT{RESET}")
            print(LINE)
            print(f" {Y}⚠ WARNING: Do not spam cookies!{RESET}")
            print(f" {Y}⚠ Each cookie will be auto-converted to EAAAAU token{RESET}")
            print(LINE)
            
            cookie_count = 0
            converted_cookies_hashes = {}
            
            while True:
                refresh_screen()
                print(f" {C}[MANUAL COOKIE INPUT] - {cookie_count} cookies added{RESET}")
                print(LINE)
                print(f" {Y}Enter cookies one by one.{RESET}")
                print(f" {Y}Type 'done' when finished or 'cancel' to abort.{RESET}")
                print(LINE)
                
                cookie_input = input(f" {W}[{W}➤{W}]{RESET} {C}COOKIE #{cookie_count + 1} {W}➤{RESET} ").strip()
                
                if cookie_input.lower() == 'done':
                    break
                elif cookie_input.lower() == 'cancel':
                    accounts_data = []
                    break
                elif not cookie_input:
                    continue
                
                # Check for spam (same cookie entered multiple times)
                cookie_hash = str(hash(cookie_input))[:16]
                if cookie_hash in converted_cookies_hashes:
                    refresh_screen()
                    print(f" {R}[SPAM DETECTED]{RESET}")
                    print(LINE)
                    print(f" {Y}This cookie was already entered!{RESET}")
                    print(f" {Y}Please use different cookies to avoid account suspension.{RESET}")
                    print(LINE)
                    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
                    continue
                
                # Convert cookie to EAAAAU token
                refresh_screen()
                print(f" {G}[!] CONVERTING COOKIE #{cookie_count + 1} TO TOKEN...{RESET}")
                nice_loader("CONVERTING")
                
                eaaaau_token = get_eaaaau_token_from_cookie(cookie_input)
                
                if eaaaau_token:
                    # Get account info
                    name, uid = await get_facebook_account_info(session, eaaaau_token)
                    
                    accounts_data.append({
                        'cookie': cookie_input,
                        'token': eaaaau_token,
                        'name': name,
                        'uid': uid
                    })
                    
                    converted_cookies_hashes[cookie_hash] = True
                    cookie_count += 1
                    
                    refresh_screen()
                    print(f" {G}[SUCCESS] Cookie #{cookie_count} converted!{RESET}")
                    print(LINE)
                    print(f" {Y}Name: {M}{name}{RESET}")
                    print(f" {Y}UID: {C}{uid}{RESET}")
                    print(LINE)
                    time.sleep(1.5)
                else:
                    refresh_screen()
                    print(f" {R}[FAILED] Could not convert cookie #{cookie_count + 1}{RESET}")
                    print(LINE)
                    print(f" {Y}Make sure the cookie is valid and try again.{RESET}")
                    print(LINE)
                    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
            
            if not accounts_data:
                refresh_screen()
                print(f" {Y}[!] NO COOKIES ADDED{RESET}")
                input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
                return
        
        else:
            print(f" {R}[ERROR] Invalid choice{RESET}")
            time.sleep(1)
            return
        
        refresh_screen()
        print(f" {G}[SUCCESS] Loaded {len(accounts_data)} accounts{RESET}")
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
        
        # Ask for target share count
        refresh_screen()
        print(f" {C}[TARGET SHARE COUNT]{RESET}")
        print(LINE)
        print(f" {Y}How many shares per page do you want?{RESET}")
        print(f" {Y}Leave empty for unlimited (continuous sharing){RESET}")
        print(LINE)
        
        target_input = input(f" {W}[{W}➤{W}]{RESET} {C}TARGET (empty for unlimited) {W}➤{RESET} ").strip()
        
        target_count = None
        if target_input:
            try:
                target_count = int(target_input)
                if target_count <= 0:
                    print(f" {R}[ERROR] Target must be greater than 0{RESET}")
                    time.sleep(1)
                    return
            except:
                print(f" {R}[ERROR] Invalid target number{RESET}")
                time.sleep(1)
                return
        
        # Select display mode
        display_mode = select_progress_display()
        
        refresh_screen()
        print(f" {M}[SHARE CONFIGURATION]{RESET}")
        print(LINE)
        print(f" {Y}Mode: {G}PAGE & NORM ACC{RESET}")
        print(f" {Y}Total Page Tokens: {G}{total_pages}{RESET}")
        print(f" {Y}Share Speed: {G}MAXIMUM (ZERO DELAYS){RESET}")
        print(f" {Y}Independent Threads: {G}{len(list_pages)}{RESET}")
        if target_count:
            print(f" {Y}Target Per Page: {C}{target_count} shares{RESET}")
            print(f" {Y}Expected Total: {M}{len(list_pages) * target_count} shares{RESET}")
        else:
            print(f" {Y}Target Per Page: {G}UNLIMITED{RESET}")
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
                page["page_id"],
                target_count,  # Pass target to share_loop
                display_mode   # Pass display mode
            ))
            tasks.append(task)
        
        print(f" {G}[STARTED] Running {len(tasks)} parallel share threads at MAXIMUM SPEED (ZERO DELAYS)...{RESET}")
        print(LINE)
        
        await asyncio.gather(*tasks)

def start_auto_share():
    """Entry point for auto share feature (PAGE & NORM ACC)."""
    refresh_screen()
    
    # Display warning message
    print(f" {R}[!] IMPORTANT WARNING{RESET}")
    print(LINE)
    print(f" {Y}⚠ This method is NOT RECOMMENDED for video FB posts!{RESET}")
    print(f" {Y}⚠ Fast sharing can quickly limit both pages and normal accounts!{RESET}")
    print(LINE)
    print(f" {C}[!] PLEASE READ CAREFULLY:{RESET}")
    print(f" {W}• Make sure your post is set to PUBLIC{RESET}")
    print(f" {W}• Video posts may get limited faster{RESET}")
    print(f" {W}• This uses MAXIMUM SPEED (zero delays){RESET}")
    print(f" {W}• Both page and normal accounts can be affected{RESET}")
    print(LINE)
    
    # Delay to let user read
    for i in range(5, 0, -1):
        sys.stdout.write(f"\r {Y}[CONTINUE IN {i} SECONDS]{RESET} {W}Reading time...{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write(f"\r{' ' * 60}\r")
    sys.stdout.flush()
    
    # Ask for confirmation
    print(f" {Y}[CONFIRMATION REQUIRED]{RESET}")
    print(LINE)
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R}Are you sure you want to proceed? (YES/NO) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        refresh_screen()
        print(f" {Y}[!] AUTO SHARE CANCELLED{RESET}")
        print(LINE)
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
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
    print(f" {G}[!] ENTER POST LINK OR ID (Leave empty to back){RESET}")
    
    prompt = f" {W}[{W}➤{W}]{RESET} {C}POST LINK/ID {W}➤{RESET} "
    
    try:
        link = input(prompt)
    except KeyboardInterrupt:
        return
    
    if not link.strip():
        return
    
    try:
        asyncio.run(auto_share_page_mode(link))
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

def cookie_to_eaag_v2(cookie):
    """Convert cookie to EAAG token using business.facebook.com method."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36',
        'referer': 'https://www.facebook.com/',
        'host': 'business.facebook.com',
        'origin': 'https://business.facebook.com',
        'upgrade-insecure-requests': '1',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'content-type': 'text/html; charset=utf-8',
        'cookie': cookie
    }
    
    try:
        response = requests.get('https://business.facebook.com/business_locations', headers=headers, timeout=10)
        eaag_match = re.search(r'(EAAG\w+)', response.text)
        if eaag_match:
            return eaag_match.group(1)
    except:
        pass
    return None

async def share_with_eaag_v2(session, cookie, token, post_id):
    """Share a post using EAAG token with proper headers."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'accept-encoding': 'gzip, deflate',
        'host': 'b-graph.facebook.com',
        'cookie': cookie
    }
    
    try:
        url = f'https://b-graph.facebook.com/me/feed?link=https://mbasic.facebook.com/{post_id}&published=0&access_token={token}'
        async with session.post(url, headers=headers) as response:
            json_data = await response.json()
            
            if 'id' in json_data:
                return True, json_data.get('id', 'N/A')
            else:
                error_msg = json_data.get('error', {}).get('message', 'Unknown error')
                return False, error_msg
    except Exception as e:
        return False, str(e)

async def renew_eaag_token_v2(cookie):
    """Renew EAAG token for a cookie."""
    return cookie_to_eaag_v2(cookie)

async def share_loop_v2(session, cookie, token, post_id, account_name, display_mode='detailed'):
    """
    Continuous sharing loop for NORM ACC mode with ZERO DELAYS, token renewal, and display modes.
    """
    global success_count_v2
    
    last_token_renewal = time.time()
    current_token = token
    failed_consecutive = 0
    
    while True:
        try:
            # Auto-renew token every 5 minutes (300 seconds)
            if time.time() - last_token_renewal >= 300:
                new_token = await renew_eaag_token_v2(cookie)
                
                if new_token:
                    current_token = new_token
                    last_token_renewal = time.time()
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[TOKEN RENEWED]{RESET} {W}|{RESET} {B}{account_name}{RESET}                              ")
                        sys.stdout.flush()
                        time.sleep(1)
                    else:
                        now = datetime.datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f" {Y}[RENEWED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {C}Token renewed{RESET}")
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            is_success, result = await share_with_eaag_v2(session, cookie, current_token, post_id)
            
            if is_success:
                # Use lock properly to update counter
                async with lock_v2:
                    success_count_v2 += 1
                    current_count = success_count_v2
                
                failed_consecutive = 0
                
                if display_mode == 'minimal':
                    # Minimal display - stay in one place
                    sys.stdout.write(f"\r {G}[SUCCESS SHARES {current_count}]{RESET} {W}|{RESET} {C}{account_name[:15]}{RESET}            ")
                    sys.stdout.flush()
                else:
                    # Detailed display - full logs
                    print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {Y}Total: {current_count}{RESET}")
                
                # ZERO DELAY - Continue immediately
            else:
                failed_consecutive += 1
                error_message = result
                
                # If failed 3 times consecutively, try to renew token
                if failed_consecutive >= 3:
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[RENEWING TOKEN...]{RESET} {W}|{RESET} {B}{account_name}{RESET}                          ")
                        sys.stdout.flush()
                    else:
                        print(f" {Y}[RENEWING]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {Y}Attempting token renewal...{RESET}")
                    
                    new_token = await renew_eaag_token_v2(cookie)
                    
                    if new_token:
                        current_token = new_token
                        last_token_renewal = time.time()
                        failed_consecutive = 0
                        
                        if display_mode == 'minimal':
                            sys.stdout.write(f"\r {G}[TOKEN RENEWED]{RESET} {W}|{RESET} {B}{account_name}{RESET}                            ")
                            sys.stdout.flush()
                            time.sleep(1)
                        else:
                            print(f" {G}[RENEWED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {G}Token renewed successfully{RESET}")
                    else:
                        if display_mode != 'minimal':
                            print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                        await asyncio.sleep(10)
                else:
                    if display_mode != 'minimal':
                        print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                    await asyncio.sleep(5)
        
        except asyncio.CancelledError:
            # Handle task cancellation gracefully
            break
        except KeyboardInterrupt:
            # Handle user interruption
            break
        except Exception as e:
            error_msg = str(e)
            # Avoid printing the full exception object
            if "asyncio" not in error_msg.lower() and "event" not in error_msg.lower():
                if display_mode != 'minimal':
                    print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {B}{account_name}{RESET} {W}|{RESET} {R}{error_msg[:40]}{RESET}")
            await asyncio.sleep(30)

async def auto_share_v2_main(link_or_id, selected_cookies):
    """Main auto share V2 function using selected database cookies with EAAG tokens."""
    global success_count_v2
    success_count_v2 = 0
    
    refresh_screen()
    print(f" {C}[!] CONVERTING SELECTED COOKIES TO EAAG TOKENS...{RESET}")
    nice_loader("CONVERTING")
    
    eaag_tokens = []
    
    # Convert selected cookies to EAAG tokens
    for acc in selected_cookies:
        token = cookie_to_eaag_v2(acc['cookie'])
        if token:
            eaag_tokens.append({
                'cookie': acc['cookie'],
                'token': token,
                'name': acc['name'],
                'uid': acc['uid']
            })
            print(f" {G}✓{RESET} {Y}{acc['name']}{RESET} {W}({C}UID: {acc['uid']}{W}){RESET}")
        else:
            print(f" {R}✗{RESET} {Y}{acc['name']}{RESET} {R}Failed to extract EAAG token{RESET}")
    
    if not eaag_tokens:
        print(f" {R}[ERROR] No valid EAAG tokens extracted!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Extract post ID
    post_id = extract_post_id_from_link(link_or_id)
    
    # Select display mode
    display_mode = select_progress_display()
    
    refresh_screen()
    print(f" {G}[SUCCESS] Extracted {len(eaag_tokens)} EAAG tokens{RESET}")
    print(LINE)
    print(f" {Y}Post ID: {G}{post_id}{RESET}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        print(f" {M}[SHARE V2 CONFIGURATION]{RESET}")
        print(LINE)
        print(f" {Y}Mode: {C}NORM ACC (EAAG Tokens){RESET}")
        print(f" {Y}Total Accounts: {G}{len(eaag_tokens)}{RESET}")
        print(f" {Y}Share Speed: {G}MAXIMUM (ZERO DELAYS){RESET}")
        print(f" {Y}Token Renewal: {C}Auto every 5 minutes{RESET}")
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
                acc['name'],
                display_mode  # Pass display mode
            ))
            tasks.append(task)
        
        print(f" {G}[STARTED] Running {len(tasks)} parallel share threads at MAXIMUM SPEED (ZERO DELAYS)...{RESET}")
        print(LINE)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            # Cancel all tasks on exception
            for task in tasks:
                if not task.done():
                    task.cancel()
            # Wait for all tasks to complete cancellation
            await asyncio.gather(*tasks, return_exceptions=True)

def select_cookies_for_v2():
    """Let user select which cookies to use for V2 sharing."""
    refresh_screen()
    print(f" {G}[!] LOADING ACCOUNTS FROM DATABASE...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/accounts")
    
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load accounts{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return None
    
    accounts = response.get('accounts', [])
    
    if not accounts:
        print(f" {R}[ERROR] No accounts stored in database{RESET}")
        print(f" {Y}[TIP] Use option 4 to add paired accounts{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return None
    
    refresh_screen()
    print(f" {C}[SELECT COOKIES FOR AUTO SHARE V2]{RESET}")
    print(LINE)
    print(f" {W}[{BG_G}{W}ALL{RESET}{W}]{RESET} {G}USE ALL ACCOUNTS{RESET}")
    print(LINE)
    
    for i, acc in enumerate(accounts, 1):
        letter = chr(64 + i) if i <= 26 else str(i)
        print(f" {W}[{BG_C}{W}{i:02d}{RESET}{Y}/{BG_C}{W}{letter}{RESET}{W}]{RESET} {C}{acc['name']}{RESET} {W}({Y}UID: {acc['uid']}{W}){RESET}")
    
    print(LINE)
    print(f" {Y}[TIP] Enter numbers separated by commas (e.g., 1,2,3) or type 'ALL'{RESET}")
    print(LINE)
    
    selection = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT {W}➤{RESET} ").strip().upper()
    
    if not selection:
        return None
    
    selected_accounts = []
    
    if selection == 'ALL':
        selected_accounts = accounts
    else:
        try:
            # Handle both numbers and letters
            parts = selection.replace(',', ' ').split()
            for part in parts:
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(accounts):
                        selected_accounts.append(accounts[idx])
                elif len(part) == 1 and part.isalpha():
                    idx = ord(part) - 65
                    if 0 <= idx < len(accounts):
                        selected_accounts.append(accounts[idx])
        except:
            print(f" {R}[ERROR] Invalid selection{RESET}")
            time.sleep(1)
            return None
    
    if not selected_accounts:
        print(f" {R}[ERROR] No valid accounts selected{RESET}")
        time.sleep(1)
        return None
    
    # Confirmation
    refresh_screen()
    print(f" {Y}[CONFIRM SELECTION]{RESET}")
    print(LINE)
    print(f" {Y}Selected {G}{len(selected_accounts)}{Y} account(s):{RESET}")
    for acc in selected_accounts:
        print(f"   • {C}{acc['name']}{RESET} {W}({Y}UID: {acc['uid']}{W}){RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {Y}Confirm? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm == 'Y':
        return selected_accounts
    else:
        return None

def start_auto_share_v2():
    """Entry point for auto share V2 feature (NORM ACC with EAAG tokens)."""
    refresh_screen()
    
    # Display informational message
    print(f" {C}[!] AUTO SHARE V2 - NORMAL ACCOUNTS{RESET}")
    print(LINE)
    print(f" {G}[✓] INFORMATION:{RESET}")
    print(f" {W}• Make sure your post is set to PUBLIC{RESET}")
    print(f" {W}• This uses EAAG tokens (business.facebook.com method){RESET}")
    print(f" {W}• Shares run at MAXIMUM SPEED (zero delays){RESET}")
    print(f" {W}• Tokens auto-renew every 5 minutes{RESET}")
    print(f" {W}• Best for normal accounts without pages{RESET}")
    print(LINE)
    
    # Brief delay to let user read
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r {C}[CONTINUE IN {i} SECONDS]{RESET} {W}Reading time...{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write(f"\r{' ' * 60}\r")
    sys.stdout.flush()
    
    selected_cookies = select_cookies_for_v2()
    
    if not selected_cookies:
        return
    
    refresh_screen()
    print(f" {C}[AUTO SHARE V2 - NORM ACC]{RESET}")
    print(LINE)
    
    link_or_id = input(f" {W}[{W}➤{W}]{RESET} {C}POST LINK OR ID {W}➤{RESET} ").strip()
    
    if not link_or_id:
        return
    
    try:
        asyncio.run(auto_share_v2_main(link_or_id, selected_cookies))
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
                auto_create_pages()
            
            elif choice in ['7', '07', 'G']:
                if user_data and user_data.get('isAdmin'):
                    admin_panel()
                else:
                    update_tool_logic()
            
            elif choice in ['8', '08', 'H']:
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
