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
API_URL = "https://rpwtools.onrender.com/api"
user_token = None
user_data = None

# --- GLOBAL VARIABLES FOR AUTO SHARE ---
success_count = 0
lock = asyncio.Lock()

def clear():
    """Clears the terminal screen completely."""
    os.system('clear')

def normalize_facebook_url(url):
    """Normalize Facebook URL to facebook.com/username format."""
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
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0.2{RESET}")
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
        
        # Color-coded plan display
        user_plan = user_data['plan']
        if user_plan == 'max':
            if user_data.get('planExpiry'):
                plan_display = f"{M}[ \033[45m{W}MAX{RESET}{M} ]{RESET}"
            else:
                plan_display = f"{M}[ \033[45m{W}MAX LIFETIME{RESET}{M} ]{RESET}"
        else:  # free
            plan_display = f"{W}[ \033[47m\033[30mFREE{RESET}{W} ]{RESET}"
        
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN':<13} {W}➤{RESET} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {W}[{RESET}•{W}]{RESET} {Y}{'PLAN EXPIRY IN':<13} {W}➤{RESET} {Y}{user_data['planExpiry']}{RESET}")
        
        # Show cookie count
        cookie_count = user_data.get('cookieCount', 0)
        print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOTAL COOKIES':<13} {W}➤{RESET} {C}{cookie_count}{RESET}")
    
    print(LINE)

def show_menu():
    """Prints the Menu Options."""
    if not user_token:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}LOGIN{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}REGISTER{RESET}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R}EXIT{RESET}")
    elif user_data and user_data.get('isAdmin'):
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}AUTO SHARE V1           — NORM ACCOUNTS{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}AUTO SHARE V2           — NORM ACCOUNTS (ALT){RESET}")
        print(f" {W}[{RESET}{BG_Y}{W}03{RESET}{BG_Y}{Y}/{RESET}{BG_Y}{W}C{RESET}{W}]{RESET} {Y}MANAGE COOKIES          — DATABASE{RESET}")
        print(f" {W}[{RESET}{BG_B}{W}04{RESET}{BG_B}{Y}/{RESET}{BG_B}{W}D{RESET}{W}]{RESET} {B}MY STATS                — STATISTICS{RESET}")
        print(f" {W}[{RESET}{BG_M}{W}05{RESET}{BG_M}{Y}/{RESET}{BG_M}{W}E{RESET}{W}]{RESET} {M}ADMIN PANEL             — MANAGEMENT{RESET}")
        print(f" {W}[{RESET}{BG_G}{W}06{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}F{RESET}{W}]{RESET} {G}UPDATE TOOL             — LATEST VERSION{RESET}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R}LOGOUT{RESET}")
    else:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G}AUTO SHARE V1           — NORM ACCOUNTS{RESET}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C}AUTO SHARE V2           — NORM ACCOUNTS (ALT){RESET}")
        print(f" {W}[{RESET}{BG_Y}{W}03{RESET}{BG_Y}{Y}/{RESET}{BG_Y}{W}C{RESET}{W}]{RESET} {Y}MANAGE COOKIES          — DATABASE{RESET}")
        print(f" {W}[{RESET}{BG_B}{W}04{RESET}{BG_B}{Y}/{RESET}{BG_B}{W}D{RESET}{W}]{RESET} {B}MY STATS                — STATISTICS{RESET}")
        print(f" {W}[{RESET}{BG_G}{W}05{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}E{RESET}{W}]{RESET} {G}UPDATE TOOL             — LATEST VERSION{RESET}")
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
    print(LINE)
    print(f" {W}[{RESET}{BG_C}{W}2{RESET}{W}]{RESET} {C}DETAILED LOGS{RESET}")
    print(f"     {Y}• Best for larger screens (desktop){RESET}")
    print(f"     {Y}• Shows success, time, account info{RESET}")
    print(f"     {Y}• Full process information{RESET}")
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
        print(f" {Y}Total Cookies: {C}{user_data.get('cookieCount', 0)}{RESET}")
        
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
        
        plan_color = G if stats['plan'] == 'max' else W
        print(f" {Y}Plan: {plan_color}{stats['plan'].upper()}{RESET}")
        
        if stats.get('planExpiry'):
            print(f" {Y}Plan Expiry In: {W}{stats['planExpiry']}{RESET}")
        
        print(LINE)
        print(f" {C}[STATISTICS]{RESET}")
        print(f" {Y}Total Shares: {G}{stats['totalShares']}{RESET}")
        print(f" {Y}Total Cookies: {C}{stats.get('cookieCount', 0)}{RESET}")
        print(LINE)
        
        share_cd = stats.get('shareCooldown', {})
        
        print(f" {C}[COOLDOWN STATUS]{RESET}")
        
        if share_cd.get('active'):
            print(f" {R}Share Cooldown: {share_cd['remainingSeconds']}s remaining{RESET}")
            print(f" {Y}Available at: {W}{share_cd['availableAt']}{RESET}")
        else:
            print(f" {G}Share: Ready ✓{RESET}")
        
        print(LINE)
    else:
        print(f" {R}[ERROR] {response if isinstance(response, str) else response.get('message', 'Failed to get stats')}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def manage_cookies():
    """Manage cookie database"""
    while True:
        refresh_screen()
        print(f" {G}[MANAGE COOKIES]{RESET}")
        print(LINE)
        print(f" {W}[{W}1{W}]{RESET} {G}VIEW ALL COOKIES{RESET}")
        print(f" {W}[{W}2{W}]{RESET} {G}ADD COOKIE{RESET}")
        print(f" {W}[{W}3{W}]{RESET} {R}DELETE COOKIE{RESET}")
        print(f" {W}[{W}4{W}]{RESET} {R}DELETE ALL COOKIES{RESET}")
        print(f" {W}[{W}0{W}]{RESET} {Y}BACK{RESET}")
        print(LINE)
        
        choice = input(f" {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip()
        
        if choice == '1':
            view_cookies()
        elif choice == '2':
            add_cookie()
        elif choice == '3':
            delete_cookie()
        elif choice == '4':
            delete_all_cookies()
        elif choice == '0':
            return
        else:
            print(f"\n {R}[!] INVALID SELECTION{RESET}")
            time.sleep(0.8)

def view_cookies():
    """View all cookies"""
    refresh_screen()
    print(f" {G}[!] LOADING COOKIES...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status == 200 and response.get('success'):
        cookies = response.get('cookies', [])
        
        refresh_screen()
        print(f" {G}[COOKIES] Total: {len(cookies)}{RESET}")
        print(LINE)
        
        if not cookies:
            print(f" {Y}No cookies stored yet.{RESET}")
        else:
            for i, cookie_data in enumerate(cookies, 1):
                status_color = G if cookie_data['status'] == 'active' else R if cookie_data['status'] == 'restricted' else Y
                status_display = cookie_data['status'].upper()
                
                print(f" {W}[{i:02d}]{RESET} {M}{cookie_data['name']}{RESET} {W}({C}UID: {cookie_data['uid']}{W}){RESET}")
                cookie_preview = cookie_data['cookie'][:50] + "..." if len(cookie_data['cookie']) > 50 else cookie_data['cookie']
                print(f"      Cookie: {C}{cookie_preview}{RESET}")
                print(f"      Added: {Y}{cookie_data['addedAt']}{RESET}")
                print(f"      Status: {status_color}{status_display}{RESET}")
                
                if cookie_data['status'] == 'restricted':
                    print(f"      {R}⚠ WARNING: This account is restricted!{RESET}")
                
                print(LINE)
        
    else:
        print(f" {R}[ERROR] Failed to load cookies{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def add_cookie():
    """Add new cookie"""
    refresh_screen()
    print(f" {G}[ADD COOKIE]{RESET}")
    print(LINE)
    
    # Check if user can add more cookies
    if user_data['plan'] == 'free' and user_data.get('cookieCount', 0) >= 10:
        print(f" {R}[LIMIT REACHED]{RESET}")
        print(LINE)
        print(f" {Y}FREE plan users can only store up to 10 cookies.{RESET}")
        print(f" {Y}You currently have: {R}{user_data.get('cookieCount', 0)}/10{RESET}")
        print(LINE)
        print(f" {G}[UPGRADE TO MAX]{RESET}")
        print(f" {Y}• Unlimited cookies{RESET}")
        print(f" {Y}• No cooldowns{RESET}")
        print(f" {Y}• Rental: 1 month (₱150) or 3 months (₱250){RESET}")
        print(LINE)
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    cookie = input(f" {W}[{W}➤{W}]{RESET} {C}COOKIE {W}➤{RESET} ").strip()
    if not cookie:
        return
    
    refresh_screen()
    print(f" {Y}[!] VALIDATING COOKIE...{RESET}")
    print(f" {C}This may take 10-15 seconds{RESET}")
    print(LINE)
    nice_loader("VALIDATING")
    
    status, response = api_request("POST", "/user/cookies", {
        "cookie": cookie
    })
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(f" {G}[SUCCESS] {response.get('message')}{RESET}")
        print(LINE)
        print(f" {Y}Name: {M}{response.get('name', 'Unknown')}{RESET}")
        print(f" {Y}UID: {C}{response.get('uid', 'Unknown')}{RESET}")
        print(f" {Y}Status: {G if response.get('status') == 'active' else R}{response.get('status', 'unknown').upper()}{RESET}")
        
        # Show restriction warning
        if response.get('restricted'):
            print(LINE)
            print(f" {R}⚠ WARNING: This account is RESTRICTED!{RESET}")
            print(f" {Y}Restricted accounts may not be able to share posts.{RESET}")
        
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
            
            # Show remaining slots for FREE users
            if user_data['plan'] == 'free':
                remaining = 10 - user_data['cookieCount']
                print(LINE)
                print(f" {Y}Remaining Slots: {C}{remaining}/10{RESET}")
        
        print(LINE)
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed to add cookie') if isinstance(response, dict) else 'Failed to add cookie'
        print(f" {R}[ERROR] {error_msg}{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_cookie():
    """Delete a specific cookie"""
    refresh_screen()
    print(f" {G}[!] LOADING COOKIES...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not isinstance(response, dict) or not response.get('success'):
        error_msg = response if isinstance(response, str) else 'Failed to load cookies'
        print(f" {R}[ERROR] {error_msg}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        refresh_screen()
        print(f" {Y}No cookies to delete.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    refresh_screen()
    print(f" {R}[DELETE COOKIE]{RESET}")
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        status_indicator = f"{R}[RESTRICTED]{RESET}" if cookie_data['status'] == 'restricted' else f"{G}[ACTIVE]{RESET}"
        print(f" {W}[{i}]{RESET} {M}{cookie_data['name']}{RESET} {W}({C}UID: {cookie_data['uid']}{W}){RESET} {status_indicator}")
    
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT COOKIE NUMBER (0 to cancel) {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        cookie_index = int(choice) - 1
        if cookie_index < 0 or cookie_index >= len(cookies):
            print(f" {R}[ERROR] Invalid cookie number{RESET}")
            time.sleep(1)
            return
        
        selected_cookie = cookies[cookie_index]
    except:
        print(f" {R}[ERROR] Invalid input{RESET}")
        time.sleep(1)
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/user/cookies/{selected_cookie['id']}")
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(f" {G}[SUCCESS] Cookie deleted!{RESET}")
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
    else:
        error_msg = response if isinstance(response, str) else 'Failed to delete cookie'
        print(f" {R}[ERROR] {error_msg}{RESET}")
    
    print(LINE)
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def delete_all_cookies():
    """Delete all cookies"""
    refresh_screen()
    print(f" {R}[DELETE ALL COOKIES]{RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R}Delete ALL cookies? This cannot be undone! (YES/NO) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", "/user/cookies")
    
    if status == 200 and response.get('success'):
        print(f" {G}[SUCCESS] {response.get('message')}{RESET}")
        if user_data:
            user_data['cookieCount'] = 0
    else:
        print(f" {R}[ERROR] Failed to delete cookies{RESET}")
    
    print(LINE)
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
            plan_color = G if user['plan'] == 'max' else W
            admin_badge = f" {M}[ADMIN]{RESET}" if user.get('isAdmin') else ""
            
            print(f" {W}[{i:02d}]{RESET} {C}{user['username'].upper()}{RESET}{admin_badge}")
            print(f"      Plan: {plan_color}{user['plan'].upper()}{RESET} | Country: {G}{user['country']}{RESET}")
            print(f"      Shares: {Y}{user['totalShares']}{RESET}")
            print(f"      Total Cookies: {C}{user.get('cookieCount', 0)}{RESET}")
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
    print(f" {W}[1]{RESET} {W}FREE{RESET} - 10 cookies max")
    print(f" {W}[2]{RESET} {G}MAX{RESET} - Unlimited cookies (RENTAL)")
    print(LINE)
    
    plan_choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT PLAN NUMBER {W}➤{RESET} ").strip()
    
    plan_map = {'1': 'free', '2': 'max'}
    
    if plan_choice not in plan_map:
        print(f" {R}[ERROR] Invalid plan{RESET}")
        time.sleep(1)
        return
    
    new_plan = plan_map[plan_choice]
    duration = None
    
    if new_plan == 'max':
        refresh_screen()
        print(f" {Y}[MAX PLAN DURATION]{RESET}")
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
        plan_color = G if user['plan'] == 'max' else W
        admin_badge = f" {M}[ADMIN]{RESET}" if user.get('isAdmin') else ""
        
        print(f" {W}[{i:02d}]{RESET} {C}{user['username'].upper()}{RESET}{admin_badge} - {plan_color}{user['plan'].upper()}{RESET}")
    
    print(f" {W}[00]{RESET} {Y}CANCEL{RESET}")
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT USER {W}➤{RESET} ").strip()
    
    if not choice or choice in ['0', '00']:
        return
    
    try:
        user_index = int(choice) - 1
        if user_index < 0 or user_index >= len(users):
            print(f" {R}[ERROR] Invalid selection{RESET}")
            time.sleep(1)
            return
        
        selected_user = users[user_index]
    except:
        print(f" {R}[ERROR] Invalid input{RESET}")
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
        print(f" MAX Users: {G}{stats['planDistribution']['max']}{RESET}")
        print(LINE)
        
        print(f" {C}[ACTIVITY STATISTICS]{RESET}")
        print(f" Total Shares: {G}{stats['totalShares']}{RESET}")
        print(LINE)
        
        print(f" {C}[RECENT USERS]{RESET}")
        for user in stats.get('recentUsers', []):
            plan_color = G if user['plan'] == 'max' else W
            print(f" {C}{user['username'].upper()}{RESET} - {plan_color}{user['plan'].upper()}{RESET} - {G}{user['country']}{RESET}")
        print(LINE)
    else:
        print(f" {R}[ERROR] Failed to load dashboard{RESET}")
        print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

# ============ AUTO SHARE V2 FUNCTIONS (ALTERNATIVE HEADERS) ============

async def share_with_eaag_v2(session, cookie, token, post_id):
    """Share a post using EAAG token with ALTERNATIVE headers (V2)."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
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
        async with session.post(url, headers=headers, timeout=10) as response:
            json_data = await response.json()
            
            if 'id' in json_data:
                return True, json_data.get('id', 'N/A')
            else:
                error_msg = json_data.get('error', {}).get('message', 'Unknown error')
                return False, error_msg
    except Exception as e:
        return False, str(e)

async def share_loop_v2(session, cookie, token, post_id, account_name, account_uid, cookie_id, display_mode='detailed'):
    """
    Continuous sharing loop for V2 mode with ALTERNATIVE HEADERS and ZERO DELAYS.
    """
    global success_count
    
    last_token_renewal = time.time()
    current_token = token
    failed_consecutive = 0
    
    while True:
        try:
            # Auto-renew token every 3 minutes (180 seconds)
            if time.time() - last_token_renewal >= 180:
                new_token = await renew_eaag_token(cookie)
                
                if new_token:
                    current_token = new_token
                    last_token_renewal = time.time()
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[TOKEN RENEWED]{RESET} {W}|{RESET} {B}[UID: {account_uid}]{RESET}                              ")
                        sys.stdout.flush()
                        time.sleep(0.5)
                    else:
                        now = datetime.datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f" {Y}[RENEWED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {C}Token renewed{RESET}")
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            is_success, result = await share_with_eaag_v2(session, cookie, current_token, post_id)
            
            if is_success:
                async with lock:
                    success_count += 1
                    current_count = success_count
                
                failed_consecutive = 0
                
                if display_mode == 'minimal':
                    sys.stdout.write(f"\r {G}[SUCCESS — {current_count}]{RESET} {W}|{RESET} {C}[UID: {account_uid}]{RESET}                    ")
                    sys.stdout.flush()
                else:
                    print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {Y}Total: {current_count}{RESET}")
                
                # ZERO DELAY - Continue immediately
            else:
                failed_consecutive += 1
                error_message = result
                
                # If failed 3 times consecutively, try to renew token
                if failed_consecutive >= 3:
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[RENEWING...]{RESET} {W}|{RESET} {B}[UID: {account_uid}]{RESET}                          ")
                        sys.stdout.flush()
                    else:
                        print(f" {Y}[RENEWING]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {Y}Attempting token renewal...{RESET}")
                    
                    new_token = await renew_eaag_token(cookie)
                    
                    if new_token:
                        current_token = new_token
                        last_token_renewal = time.time()
                        failed_consecutive = 0
                        
                        if display_mode == 'minimal':
                            sys.stdout.write(f"\r {G}[TOKEN RENEWED]{RESET} {W}|{RESET} {B}[UID: {account_uid}]{RESET}                            ")
                            sys.stdout.flush()
                            time.sleep(0.5)
                        else:
                            print(f" {G}[RENEWED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {G}Token renewed successfully{RESET}")
                    else:
                        if display_mode != 'minimal':
                            print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                        await asyncio.sleep(5)  # Brief pause after failed renewal
                else:
                    if display_mode != 'minimal':
                        print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                    # ZERO DELAY - Continue immediately even after errors
        
        except asyncio.CancelledError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_msg = str(e)
            if "asyncio" not in error_msg.lower() and "event" not in error_msg.lower():
                if display_mode != 'minimal':
                    print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_msg[:40]}{RESET}")
            # ZERO DELAY - Continue immediately after exceptions

async def auto_share_main_v2(link_or_id, selected_cookies):
    """Main auto share V2 function using alternative headers."""
    global success_count
    success_count = 0
    
    refresh_screen()
    print(f" {C}[!] CONVERTING SELECTED COOKIES TO EAAG TOKENS...{RESET}")
    nice_loader("CONVERTING")
    
    eaag_tokens = []
    
    # Convert selected cookies to EAAG tokens
    for cookie_data in selected_cookies:
        token = cookie_to_eaag(cookie_data['cookie'])
        if token:
            eaag_tokens.append({
                'id': cookie_data['id'],
                'cookie': cookie_data['cookie'],
                'token': token,
                'name': cookie_data['name'],
                'uid': cookie_data['uid'],
                'status': cookie_data.get('status', 'active')
            })
            status_indicator = f"{R}[RESTRICTED]{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}[ACTIVE]{RESET}"
            print(f" {G}✓{RESET} {Y}{cookie_data['name']}{RESET} {W}({C}UID: {cookie_data['uid']}{W}){RESET} {status_indicator}")
        else:
            print(f" {R}✗{RESET} {Y}{cookie_data['name']}{RESET} {R}Failed to extract EAAG token{RESET}")
    
    if not eaag_tokens:
        print(f" {R}[ERROR] No valid EAAG tokens extracted!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Extract post ID
    async with aiohttp.ClientSession() as session:
        post_id = extract_post_id_from_link(link_or_id)
        
        # If extraction failed or looks like a full URL, try API method
        if not post_id.isdigit():
            refresh_screen()
            print(f" {G}[!] EXTRACTING POST ID FROM LINK...{RESET}")
            nice_loader("EXTRACTING")
            
            post_id = await getid(session, link_or_id)
            if not post_id:
                print(f" {R}[ERROR] Failed to get post ID{RESET}")
                input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
                return
    
    # Select display mode
    display_mode = select_progress_display()
    
    refresh_screen()
    print(f" {G}[SUCCESS] Extracted {len(eaag_tokens)} EAAG tokens{RESET}")
    print(LINE)
    print(f" {Y}Post ID: {G}{post_id}{RESET}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        print(f" {M}[AUTO SHARE V2 CONFIGURATION]{RESET}")
        print(LINE)
        print(f" {Y}Mode: {C}V2 - ALTERNATIVE HEADERS{RESET}")
        print(f" {Y}Total Accounts: {G}{len(eaag_tokens)}{RESET}")
        print(f" {Y}Share Speed: {G}MAXIMUM (ZERO DELAYS){RESET}")
        print(f" {Y}Token Renewal: {C}Auto every 3 minutes{RESET}")
        print(f" {Y}Headers: {C}Windows Desktop (Chrome 107){RESET}")
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
                acc['uid'],
                acc['id'],
                display_mode
            ))
            tasks.append(task)
        
        print(f" {G}[STARTED] Running {len(tasks)} parallel V2 share threads at MAXIMUM SPEED...{RESET}")
        print(LINE)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

def start_auto_share_v2():
    """Entry point for auto share V2 feature."""
    refresh_screen()
    
    # Display informational message
    print(f" {C}[!] AUTO SHARE V2 - ALTERNATIVE HEADERS{RESET}")
    print(LINE)
    print(f" {G}[✓] INFORMATION:{RESET}")
    print(f" {W}• Make sure your post is set to PUBLIC{RESET}")
    print(f" {W}• Uses ALTERNATIVE headers (Windows Desktop){RESET}")
    print(f" {W}• Shares run at MAXIMUM SPEED (zero delays){RESET}")
    print(f" {W}• Tokens auto-renew every 3 minutes{RESET}")
    print(f" {W}• Enhanced cookie validation with restriction detection{RESET}")
    print(f" {W}• Best for accounts that fail with V1{RESET}")
    print(LINE)
    
    # Brief delay to let user read
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r {C}[CONTINUE IN {i} SECONDS]{RESET} {W}Reading time...{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write(f"\r{' ' * 60}\r")
    sys.stdout.flush()
    
    selected_cookies = select_cookies_for_sharing()
    
    if not selected_cookies:
        return
    
    refresh_screen()
    print(f" {C}[AUTO SHARE V2]{RESET}")
    print(LINE)
    
    link_or_id = input(f" {W}[{W}➤{W}]{RESET} {C}POST LINK OR ID {W}➤{RESET} ").strip()
    
    if not link_or_id:
        return
    
    try:
        asyncio.run(auto_share_main_v2(link_or_id, selected_cookies))
    except KeyboardInterrupt:
        refresh_screen()
        print(f" {Y}[!] AUTO SHARE V2 STOPPED BY USER{RESET}")
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

# ============ AUTO SHARE FUNCTIONS ============

def cookie_to_eaag(cookie):
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
        response = requests.get('https://business.facebook.com/business_locations', headers=headers, timeout=15)
        eaag_match = re.search(r'(EAAG\w+)', response.text)
        if eaag_match:
            return eaag_match.group(1)
    except:
        pass
    return None

async def share_with_eaag(session, cookie, token, post_id):
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
        async with session.post(url, headers=headers, timeout=10) as response:
            json_data = await response.json()
            
            if 'id' in json_data:
                return True, json_data.get('id', 'N/A')
            else:
                error_msg = json_data.get('error', {}).get('message', 'Unknown error')
                return False, error_msg
    except Exception as e:
        return False, str(e)

async def renew_eaag_token(cookie):
    """Renew EAAG token for a cookie."""
    return cookie_to_eaag(cookie)

async def share_loop(session, cookie, token, post_id, account_name, account_uid, cookie_id, display_mode='detailed'):
    """
    Continuous sharing loop for NORM ACC mode with ZERO DELAYS and token renewal every 3 minutes.
    """
    global success_count
    
    last_token_renewal = time.time()
    current_token = token
    failed_consecutive = 0
    
    while True:
        try:
            # Auto-renew token every 3 minutes (180 seconds)
            if time.time() - last_token_renewal >= 180:
                new_token = await renew_eaag_token(cookie)
                
                if new_token:
                    current_token = new_token
                    last_token_renewal = time.time()
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[TOKEN RENEWED]{RESET} {W}|{RESET} {B}[UID: {account_uid}]{RESET}                              ")
                        sys.stdout.flush()
                        time.sleep(0.5)
                    else:
                        now = datetime.datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f" {Y}[RENEWED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {C}Token renewed{RESET}")
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            is_success, result = await share_with_eaag(session, cookie, current_token, post_id)
            
            if is_success:
                async with lock:
                    success_count += 1
                    current_count = success_count
                
                failed_consecutive = 0
                
                if display_mode == 'minimal':
                    sys.stdout.write(f"\r {G}[SUCCESS — {current_count}]{RESET} {W}|{RESET} {C}[UID: {account_uid}]{RESET}                    ")
                    sys.stdout.flush()
                else:
                    print(f" {G}[SUCCESS]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {Y}Total: {current_count}{RESET}")
                
                # ZERO DELAY - Continue immediately
            else:
                failed_consecutive += 1
                error_message = result
                
                # If failed 3 times consecutively, try to renew token
                if failed_consecutive >= 3:
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}[RENEWING...]{RESET} {W}|{RESET} {B}[UID: {account_uid}]{RESET}                          ")
                        sys.stdout.flush()
                    else:
                        print(f" {Y}[RENEWING]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {Y}Attempting token renewal...{RESET}")
                    
                    new_token = await renew_eaag_token(cookie)
                    
                    if new_token:
                        current_token = new_token
                        last_token_renewal = time.time()
                        failed_consecutive = 0
                        
                        if display_mode == 'minimal':
                            sys.stdout.write(f"\r {G}[TOKEN RENEWED]{RESET} {W}|{RESET} {B}[UID: {account_uid}]{RESET}                            ")
                            sys.stdout.flush()
                            time.sleep(0.5)
                        else:
                            print(f" {G}[RENEWED]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {G}Token renewed successfully{RESET}")
                    else:
                        if display_mode != 'minimal':
                            print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                        await asyncio.sleep(5)  # Brief pause after failed renewal
                else:
                    if display_mode != 'minimal':
                        print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                    # ZERO DELAY - Continue immediately even after errors
        
        except asyncio.CancelledError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_msg = str(e)
            if "asyncio" not in error_msg.lower() and "event" not in error_msg.lower():
                if display_mode != 'minimal':
                    print(f" {R}[ERROR]{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_msg[:40]}{RESET}")
            # ZERO DELAY - Continue immediately after exceptions

async def auto_share_main(link_or_id, selected_cookies):
    """Main auto share function using selected database cookies with EAAG tokens."""
    global success_count
    success_count = 0
    
    refresh_screen()
    print(f" {C}[!] CONVERTING SELECTED COOKIES TO EAAG TOKENS...{RESET}")
    nice_loader("CONVERTING")
    
    eaag_tokens = []
    
    # Convert selected cookies to EAAG tokens
    for cookie_data in selected_cookies:
        token = cookie_to_eaag(cookie_data['cookie'])
        if token:
            eaag_tokens.append({
                'id': cookie_data['id'],
                'cookie': cookie_data['cookie'],
                'token': token,
                'name': cookie_data['name'],
                'uid': cookie_data['uid'],
                'status': cookie_data.get('status', 'active')
            })
            status_indicator = f"{R}[RESTRICTED]{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}[ACTIVE]{RESET}"
            print(f" {G}✓{RESET} {Y}{cookie_data['name']}{RESET} {W}({C}UID: {cookie_data['uid']}{W}){RESET} {status_indicator}")
        else:
            print(f" {R}✗{RESET} {Y}{cookie_data['name']}{RESET} {R}Failed to extract EAAG token{RESET}")
    
    if not eaag_tokens:
        print(f" {R}[ERROR] No valid EAAG tokens extracted!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Extract post ID
    async with aiohttp.ClientSession() as session:
        post_id = extract_post_id_from_link(link_or_id)
        
        # If extraction failed or looks like a full URL, try API method
        if not post_id.isdigit():
            refresh_screen()
            print(f" {G}[!] EXTRACTING POST ID FROM LINK...{RESET}")
            nice_loader("EXTRACTING")
            
            post_id = await getid(session, link_or_id)
            if not post_id:
                print(f" {R}[ERROR] Failed to get post ID{RESET}")
                input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
                return
    
    # Select display mode
    display_mode = select_progress_display()
    
    refresh_screen()
    print(f" {G}[SUCCESS] Extracted {len(eaag_tokens)} EAAG tokens{RESET}")
    print(LINE)
    print(f" {Y}Post ID: {G}{post_id}{RESET}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        print(f" {M}[AUTO SHARE CONFIGURATION]{RESET}")
        print(LINE)
        print(f" {Y}Mode: {C}NORM ACC (EAAG Tokens){RESET}")
        print(f" {Y}Total Accounts: {G}{len(eaag_tokens)}{RESET}")
        print(f" {Y}Share Speed: {G}MAXIMUM (ZERO DELAYS){RESET}")
        print(f" {Y}Token Renewal: {C}Auto every 3 minutes{RESET}")
        print(f" {Y}Renewal Safety: {G}Detection & Error Handling{RESET}")
        print(LINE)
        print(f" {G}[!] STARTING AUTO SHARE...{RESET}")
        print(f" {Y}[TIP] Press Ctrl+C to stop{RESET}")
        print(LINE)
        
        tasks = []
        for acc in eaag_tokens:
            task = asyncio.create_task(share_loop(
                session,
                acc['cookie'],
                acc['token'],
                post_id,
                acc['name'],
                acc['uid'],
                acc['id'],
                display_mode
            ))
            tasks.append(task)
        
        print(f" {G}[STARTED] Running {len(tasks)} parallel share threads at MAXIMUM SPEED (ZERO DELAYS)...{RESET}")
        print(LINE)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

def select_cookies_for_sharing():
    """Let user select which cookies to use for sharing."""
    refresh_screen()
    print(f" {G}[!] LOADING COOKIES FROM DATABASE...{RESET}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not response.get('success'):
        print(f" {R}[ERROR] Failed to load cookies{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return None
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        print(f" {R}[ERROR] No cookies stored in database{RESET}")
        print(f" {Y}[TIP] Use option 2 to add cookies{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return None
    
    refresh_screen()
    print(f" {C}[SELECT COOKIES FOR AUTO SHARE]{RESET}")
    print(LINE)
    print(f" {W}[{BG_G}{W}ALL{RESET}{W}]{RESET} {G}USE ALL COOKIES{RESET}")
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        letter = chr(64 + i) if i <= 26 else str(i)
        status_indicator = f"{R}[RESTRICTED]{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}[ACTIVE]{RESET}"
        print(f" {W}[{BG_C}{W}{i:02d}{RESET}{Y}/{BG_C}{W}{letter}{RESET}{W}]{RESET} {C}{cookie_data['name']}{RESET} {W}({Y}UID: {cookie_data['uid']}{W}){RESET} {status_indicator}")
    
    print(LINE)
    print(f" {Y}[TIP] Enter numbers separated by commas (e.g., 1,2,3) or type 'ALL'{RESET}")
    print(LINE)
    
    selection = input(f" {W}[{W}➤{W}]{RESET} {C}SELECT {W}➤{RESET} ").strip().upper()
    
    if not selection:
        return None
    
    selected_cookies = []
    
    if selection == 'ALL':
        selected_cookies = cookies
    else:
        try:
            parts = selection.replace(',', ' ').split()
            for part in parts:
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(cookies):
                        selected_cookies.append(cookies[idx])
                elif len(part) == 1 and part.isalpha():
                    idx = ord(part) - 65
                    if 0 <= idx < len(cookies):
                        selected_cookies.append(cookies[idx])
        except:
            print(f" {R}[ERROR] Invalid selection{RESET}")
            time.sleep(1)
            return None
    
    if not selected_cookies:
        print(f" {R}[ERROR] No valid cookies selected{RESET}")
        time.sleep(1)
        return None
    
    # Confirmation
    refresh_screen()
    print(f" {Y}[CONFIRM SELECTION]{RESET}")
    print(LINE)
    print(f" {Y}Selected {G}{len(selected_cookies)}{Y} cookie(s):{RESET}")
    for cookie_data in selected_cookies:
        status_indicator = f"{R}[RESTRICTED]{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}[ACTIVE]{RESET}"
        print(f"   • {C}{cookie_data['name']}{RESET} {W}({Y}UID: {cookie_data['uid']}{W}){RESET} {status_indicator}")
    print(LINE)
    
    # Check for restricted cookies
    restricted_count = sum(1 for c in selected_cookies if c.get('status') == 'restricted')
    if restricted_count > 0:
        print(f" {R}⚠ WARNING: {restricted_count} restricted account(s) detected!{RESET}")
        print(f" {Y}Restricted accounts may not be able to share posts.{RESET}")
        print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {Y}Confirm? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm == 'Y':
        return selected_cookies
    else:
        return None

def start_auto_share():
    """Entry point for auto share feature."""
    refresh_screen()
    
    # Display informational message
    print(f" {C}[!] AUTO SHARE - NORMAL ACCOUNTS{RESET}")
    print(LINE)
    print(f" {G}[✓] INFORMATION:{RESET}")
    print(f" {W}• Make sure your post is set to PUBLIC{RESET}")
    print(f" {W}• This uses EAAG tokens (business.facebook.com method){RESET}")
    print(f" {W}• Shares run at MAXIMUM SPEED (zero delays){RESET}")
    print(f" {W}• Tokens auto-renew every 3 minutes{RESET}")
    print(f" {W}• Enhanced cookie validation with restriction detection{RESET}")
    print(f" {W}• Best for normal accounts{RESET}")
    print(LINE)
    
    # Brief delay to let user read
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r {C}[CONTINUE IN {i} SECONDS]{RESET} {W}Reading time...{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write(f"\r{' ' * 60}\r")
    sys.stdout.flush()
    
    selected_cookies = select_cookies_for_sharing()
    
    if not selected_cookies:
        return
    
    refresh_screen()
    print(f" {C}[AUTO SHARE]{RESET}")
    print(LINE)
    
    link_or_id = input(f" {W}[{W}➤{W}]{RESET} {C}POST LINK OR ID {W}➤{RESET} ").strip()
    
    if not link_or_id:
        return
    
    try:
        asyncio.run(auto_share_main(link_or_id, selected_cookies))
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
                manage_cookies()
            
            elif choice in ['4', '04', 'D']:
                show_user_stats()
            
            elif choice in ['5', '05', 'E']:
                if user_data and user_data.get('isAdmin'):
                    admin_panel()
                else:
                    update_tool_logic()
            
            elif choice in ['6', '06', 'F']:
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
