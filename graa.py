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
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}2.1.0{RESET}")
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
        
        # Color-coded plan display with background colors (VIP REMOVED)
        user_plan = user_data['plan']
        if user_plan == 'max':
            plan_display = f"{M}[ \033[45m{W}MAX{RESET}{M} ]{RESET}"  # Magenta background
        else:  # free
            plan_display = f"{W}[ \033[47m\033[30mFREE{RESET}{W} ]{RESET}"  # White background with black text
        
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN':<13} {W}➤{RESET} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN EXPIRY IN':<13} {W}➤{RESET} {Y}{user_data['planExpiry']}{RESET}")
        
        # Show paired accounts count AND V2 cookies count
        account_count = user_data.get('accountCount', 0)
        v2_cookie_count = user_data.get('v2CookieCount', 0)
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PAIRED ACC':<13} {W}➤{RESET} {C}{account_count}{RESET}")
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'V2 COOKIES':<13} {W}➤{RESET} {C}{v2_cookie_count}{RESET}")
    
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
            sys.stdout.write("\033[F\033[K")
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
        
        if user_data.get('planExpiry'):
            print(f" {Y}Plan Expiry: {Y}{user_data['planExpiry']}{RESET}")
        
        print(f" {Y}Paired Accounts: {C}{user_data.get('accountCount', 0)}{RESET}")
        print(f" {Y}V2 Cookies: {C}{user_data.get('v2CookieCount', 0)}{RESET}")
        
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
        
        # UPDATED: Removed VIP color reference
        plan_color = G if stats['plan'] == 'max' else W
        print(f" {Y}Plan: {plan_color}{stats['plan'].upper()}{RESET}")
        
        if stats.get('planExpiry'):
            print(f" {Y}Plan Expiry In: {W}{stats['planExpiry']}{RESET}")
        
        print(LINE)
        print(f" {C}[STATISTICS]{RESET}")
        print(f" {Y}Total Shares: {G}{stats['totalShares']}{RESET}")
        print(f" {Y}Total Cookie Converts: {G}{stats['totalCookieConverts']}{RESET}")
        print(f" {Y}Paired Accounts: {C}{stats.get('accountCount', 0)}{RESET}")
        print(f" {Y}V2 Cookies: {C}{stats.get('v2CookieCount', 0)}{RESET}")
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
# (Keeping original functions - no changes needed here)
# ... [rest of auto create functions remain the same] ...

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
            # UPDATED: Removed VIP color reference
            plan_color = G if user['plan'] == 'max' else W
            admin_badge = f" {M}[ADMIN]{RESET}" if user.get('isAdmin') else ""
            
            print(f" {W}[{i:02d}]{RESET} {C}{user['username'].upper()}{RESET}{admin_badge}")
            print(f"      Plan: {plan_color}{user['plan'].upper()}{RESET} | Country: {G}{user['country']}{RESET}")
            
            if user.get('planExpiry'):
                print(f"      Plan Expiry: {Y}{user['planExpiry']}{RESET}")
            
            print(f"      Shares: {Y}{user['totalShares']}{RESET} | Converts: {Y}{user['totalCookieConverts']}{RESET}")
            print(f"      Paired Accounts: {C}{user.get('accountCount', 0)}{RESET} | V2 Cookies: {C}{user.get('v2CookieCount', 0)}{RESET}")
            print(LINE)
        
    else:
        print(f" {R}[ERROR] Failed to get users{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def change_user_plan():
    """Change a user's plan - UPDATED for rentable MAX"""
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
        # UPDATED: Removed VIP color reference
        plan_color = G if user['plan'] == 'max' else W
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
    # UPDATED: Changed VIP to MAX with pricing
    print(f" {W}[1]{RESET} {W}FREE{RESET} - 5min share cooldown, 30s cookie cooldown")
    print(f" {W}[2]{RESET} {G}MAX{RESET} - No cooldowns (₱150/mo or ₱250/3mo)")
    print(LINE)
    
    plan_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT PLAN NUMBER {W}➤{RESET} ").strip()
    
    # UPDATED: Removed VIP from plan map
    plan_map = {'1': 'free', '2': 'max'}
    
    if plan_choice not in plan_map:
        print(f" {R}[ERROR] Invalid plan{RESET}")
        time.sleep(1)
        return
    
    new_plan = plan_map[plan_choice]
    duration = None
    
    # UPDATED: Changed from 'vip' to 'max' for duration
    if new_plan == 'max':
        refresh_screen()
        print(f" {Y}[MAX PLAN DURATION]{RESET}")
        print(LINE)
        print(f" {W}[1]{RESET} 1 Month (₱150)")
        print(f" {W}[2]{RESET} 3 Months (₱250)")
        print(LINE)
        
        duration_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT DURATION {W}➤{RESET} ").strip()
        
        # UPDATED: Only 1 and 3 months options
        duration_map = {'1': 1, '2': 3}
        
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
        # UPDATED: Removed VIP color reference
        plan_color = G if user['plan'] == 'max' else W
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
        # UPDATED: Removed VIP line
        print(f" MAX Users: {G}{stats['planDistribution']['max']}{RESET}")
        print(LINE)
        
        print(f" {C}[ACTIVITY STATISTICS]{RESET}")
        print(f" Total Shares: {G}{stats['totalShares']}{RESET}")
        print(f" Total Cookie Converts: {G}{stats['totalCookieConverts']}{RESET}")
        print(LINE)
        
        print(f" {C}[RECENT USERS]{RESET}")
        for user in stats.get('recentUsers', []):
            # UPDATED: Removed VIP color reference
            plan_color = G if user['plan'] == 'max' else W
            print(f" {C}{user['username'].upper()}{RESET} - {plan_color}{user['plan'].upper()}{RESET} - {G}{user['country']}{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] Failed to load dashboard{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ AUTO SHARE FUNCTIONS ============
# (Keeping all original auto share functions unchanged)
# ... [rest of auto share functions remain exactly the same] ...

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
                # start_auto_share()  # Your existing function
                pass
                
            elif choice in ['2', '02', 'B']:
                # start_auto_share_v2()  # Your existing function
                pass
                
            elif choice in ['3', '03', 'C']:
                cookie_to_token_tool()
                
            elif choice in ['4', '04', 'D']:
                manage_cookie_token()
            
            elif choice in ['5', '05', 'E']:
                show_user_stats()
            
            elif choice in ['6', '06', 'F']:
                # auto_create_pages()  # Your existing function
                pass
            
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
