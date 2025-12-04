import os
import sys
import subprocess
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

# --- AUTO-INSTALLER SECTION ---
def install_requirements():
    requirements = [
        ("aiohttp", "aiohttp"),
        ("requests", "requests"),
        ("asyncio", "asyncio")
    ]
    needs_install = False
    
    for package, import_name in requirements:
        try:
            __import__(import_name)
        except ImportError:
            needs_install = True
            print(f"【!】 {package} is missing. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                print(f"【✗】 Failed to install {package}")
                sys.exit(1)
    
    if needs_install:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("【✓】 All dependencies installed successfully!")
        time.sleep(1)

install_requirements()

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
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, color=W, delay=0.02):
    """Animated typing effect for text."""
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay + random.uniform(0.002, 0.008))
    print()

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
    banner_text = f"""{C}
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    {RESET}"""
    
    for line in banner_text.split('\n'):
        print(line)
        time.sleep(0.05)

    print(LINE)
    type_print(f" 【•】 {'DEVELOPER':<13} ➤ {G}KEN DRICK{RESET}", W, 0.01)
    type_print(f" 【•】 {'GITHUB':<13} ➤ {G}RYO GRAHHH{RESET}", W, 0.01)
    type_print(f" 【•】 {'VERSION':<13} ➤ {G}1.0.2{RESET}", W, 0.01)
    type_print(f" 【•】 {'FACEBOOK':<13} ➤ {G}facebook.com/ryoevisu{RESET}", W, 0.01)
    
    tool_label = "TOOL'S NAME"
type_print(f" 【•】 {tool_label:<13} ➤ {tool_name}", W, 0.01)
    
    if user_data:
        print(LINE)
        username_display = user_data['username'].upper()
        type_print(f" 【•】 {'USERNAME':<13} ➤ {G}{username_display}{RESET}", W, 0.01)
        
        fb_link = user_data.get('facebook', 'N/A')
        type_print(f" 【•】 {'FACEBOOK':<13} ➤ {G}{fb_link}{RESET}", W, 0.01)
        
        country_display = user_data.get('country', 'N/A').upper()
        type_print(f" 【•】 {'COUNTRY':<13} ➤ {G}{country_display}{RESET}", W, 0.01)
        
        # Color-coded plan display
        user_plan = user_data['plan']
        if user_plan == 'max':
            if user_data.get('planExpiry'):
                plan_display = f"{M}【 \033[45m{W}MAX{RESET}{M} 】{RESET}"
            else:
                plan_display = f"{M}【 \033[45m{W}MAX LIFETIME{RESET}{M} 】{RESET}"
        else:  # free
            plan_display = f"{W}【 \033[47m\033[30mFREE{RESET}{W} 】{RESET}"
        
        type_print(f" 【•】 {'PLAN':<13} ➤ {plan_display}", W, 0.01)
        
        if user_data.get('planExpiry'):
            type_print(f" 【•】 {'PLAN EXPIRY IN':<13} ➤ {Y}{user_data['planExpiry']}{RESET}", W, 0.01)
        
        # Show cookie count
        cookie_count = user_data.get('cookieCount', 0)
        type_print(f" 【•】 {'TOTAL COOKIES':<13} ➤ {C}{cookie_count}{RESET}", W, 0.01)
    
    print(LINE)

def show_menu():
    """Prints the Menu Options with animation."""
    if not user_token:
        type_print(f" 【{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}】 {G}LOGIN{RESET}", W, 0.01)
        type_print(f" 【{BG_C}{W}02{RESET}{BG_C}{Y}/{RESET}{BG_C}{W}B{RESET}】 {C}REGISTER{RESET}", W, 0.01)
        type_print(f" 【{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}】 {R}EXIT{RESET}", W, 0.01)
    elif user_data and user_data.get('isAdmin'):
        type_print(f" 【{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}】 {G}AUTO SHARE              — NORM ACCOUNTS{RESET}", W, 0.01)
        type_print(f" 【{BG_Y}{W}02{RESET}{BG_Y}{Y}/{RESET}{BG_Y}{W}B{RESET}】 {Y}MANAGE COOKIES          — DATABASE{RESET}", W, 0.01)
        type_print(f" 【{BG_B}{W}03{RESET}{BG_B}{Y}/{RESET}{BG_B}{W}C{RESET}】 {B}MY STATS                — STATISTICS{RESET}", W, 0.01)
        type_print(f" 【{BG_M}{W}04{RESET}{BG_M}{Y}/{RESET}{BG_M}{W}D{RESET}】 {M}ADMIN PANEL             — MANAGEMENT{RESET}", W, 0.01)
        type_print(f" 【{BG_G}{W}05{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}E{RESET}】 {G}UPDATE TOOL             — LATEST VERSION{RESET}", W, 0.01)
        type_print(f" 【{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}】 {R}LOGOUT{RESET}", W, 0.01)
    else:
        type_print(f" 【{BG_G}{W}01{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}A{RESET}】 {G}AUTO SHARE              — NORM ACCOUNTS{RESET}", W, 0.01)
        type_print(f" 【{BG_Y}{W}02{RESET}{BG_Y}{Y}/{RESET}{BG_Y}{W}B{RESET}】 {Y}MANAGE COOKIES          — DATABASE{RESET}", W, 0.01)
        type_print(f" 【{BG_B}{W}03{RESET}{BG_B}{Y}/{RESET}{BG_B}{W}C{RESET}】 {B}MY STATS                — STATISTICS{RESET}", W, 0.01)
        type_print(f" 【{BG_G}{W}04{RESET}{BG_G}{Y}/{RESET}{BG_G}{W}D{RESET}】 {G}UPDATE TOOL             — LATEST VERSION{RESET}", W, 0.01)
        type_print(f" 【{BG_R}{W}00{RESET}{BG_R}{Y}/{RESET}{BG_R}{W}X{RESET}】 {R}LOGOUT{RESET}", W, 0.01)
    
    print(LINE)

def refresh_screen():
    """Instantly wipes screen and repaints the UI base."""
    clear()
    banner_header()
    show_menu()

def animated_input(prompt_text="CHOICE", color=C):
    """Animated input with typing effect."""
    sys.stdout.write(f" {W}【{RESET}")
    time.sleep(0.03)
    sys.stdout.write(f"{W}➤{RESET}")
    time.sleep(0.03)
    sys.stdout.write(f"{W}】{RESET} ")
    
    for char in prompt_text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(0.02)
    
    sys.stdout.write(f" {W}➤{RESET} ")
    sys.stdout.flush()
    return input("")

def nice_loader(text="PROCESSING"):
    """Improved Progress Bar Loader with animation."""
    sys.stdout.write("\033[?25l")
    
    filled = "■"
    empty = "□"
    width = 20
    
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = filled * i + empty * (width - i)
        color = G if i == width else C
        
        sys.stdout.write(f"\r {W}【{RESET}•{W}】{RESET} {Y}{text:<10} {W}➤{RESET} {color}【{bar}】 {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(0.04) 
    
    time.sleep(0.3) 
    sys.stdout.write(f"\r{' ' * 65}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")

def select_progress_display():
    """Let user choose progress display mode"""
    refresh_screen()
    type_print(f" {C}【SHARING PROGRESS DISPLAY】{RESET}", C, 0.02)
    print(LINE)
    type_print(f" {Y}Choose how you want to see sharing progress:{RESET}", Y, 0.02)
    print(LINE)
    type_print(f" 【{BG_G}{W}1{RESET}】 {G}SUCCESS COUNTER (1/100){RESET}", W, 0.01)
    type_print(f"     {Y}• Best for smaller screens (mobile){RESET}", Y, 0.01)
    type_print(f"     {Y}• Shows only success count{RESET}", Y, 0.01)
    type_print(f"     {Y}• Minimal display, stays in one place{RESET}", Y, 0.01)
    print(LINE)
    type_print(f" 【{BG_C}{W}2{RESET}】 {C}DETAILED LOGS{RESET}", W, 0.01)
    type_print(f"     {Y}• Best for larger screens (desktop){RESET}", Y, 0.01)
    type_print(f"     {Y}• Shows success, time, account info{RESET}", Y, 0.01)
    type_print(f"     {Y}• Full process information{RESET}", Y, 0.01)
    print(LINE)
    
    while True:
        choice = animated_input("CHOICE (1 or 2)", C).strip()
        
        if choice == '1':
            return 'minimal'
        elif choice == '2':
            return 'detailed'
        else:
            type_print(f" {R}【!】 Invalid choice. Please enter 1 or 2{RESET}", R, 0.02)
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
    type_print(f" {G}【!】 LOGIN TO RPWTOOLS{RESET}", G, 0.02)
    print(LINE)
    
    username = animated_input("USERNAME", C).strip()
    if not username:
        return
    
    password = animated_input("PASSWORD", C).strip()
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
        
        type_print(f" {G}【SUCCESS】 Login successful!{RESET}", G, 0.02)
        print(LINE)
        type_print(f" {Y}Welcome back, {G}{user_data['username'].upper()}{RESET}", Y, 0.02)
        type_print(f" {Y}Plan: {G}{user_data['plan'].upper()}{RESET}", Y, 0.02)
        type_print(f" {Y}Total Cookies: {C}{user_data.get('cookieCount', 0)}{RESET}", Y, 0.02)
        
        if user_data.get('isAdmin'):
            type_print(f" {M}【ADMIN ACCESS GRANTED】{RESET}", M, 0.02)
        
        print(LINE)
    else:
        type_print(f" {R}【ERROR】 {response if isinstance(response, str) else response.get('message', 'Login failed')}{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def register_user():
    """Register new user"""
    global user_token, user_data
    
    refresh_screen()
    type_print(f" {G}【!】 REGISTER NEW ACCOUNT{RESET}", G, 0.02)
    print(LINE)
    
    username = animated_input("USERNAME", C).strip()
    if not username:
        return
    
    password = animated_input("PASSWORD", C).strip()
    if not password:
        return
    
    facebook = animated_input("FACEBOOK LINK", C).strip()
    if not facebook:
        return
    
    facebook = normalize_facebook_url(facebook)
    
    refresh_screen()
    type_print(f" {G}【!】 NORMALIZED FACEBOOK URL: {Y}{facebook}{RESET}", G, 0.02)
    print(LINE)
    
    type_print(f" {G}【!】 DETECTING YOUR COUNTRY...{RESET}", G, 0.02)
    nice_loader("DETECTING")
    
    country = get_country_from_ip()
    
    refresh_screen()
    type_print(f" {G}【!】 DETECTED COUNTRY: {Y}{country}{RESET}", G, 0.02)
    print(LINE)
    confirm = animated_input("Is this correct? (Y/N)", Y).strip().upper()
    
    if confirm == 'N':
        country = animated_input("ENTER YOUR COUNTRY", C).strip()
    
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
        
        type_print(f" {G}【SUCCESS】 Registration successful!{RESET}", G, 0.02)
        print(LINE)
        type_print(f" {Y}Welcome, {G}{user_data['username'].upper()}{RESET}", Y, 0.02)
        type_print(f" {Y}Plan: {G}{user_data['plan'].upper()}{RESET}", Y, 0.02)
        type_print(f" {Y}Country: {G}{user_data['country']}{RESET}", Y, 0.02)
        type_print(f" {Y}Facebook: {G}{facebook}{RESET}", Y, 0.02)
        print(LINE)
    else:
        type_print(f" {R}【ERROR】 {response if isinstance(response, str) else response.get('message', 'Registration failed')}{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def show_user_stats():
    """Display user statistics"""
    refresh_screen()
    type_print(f" {G}【!】 LOADING STATS...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/stats")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats')
        
        refresh_screen()
        type_print(f" {G}【USER STATISTICS】{RESET}", G, 0.02)
        print(LINE)
        type_print(f" {Y}Username: {W}{stats['username'].upper()}{RESET}", Y, 0.01)
        
        plan_color = G if stats['plan'] == 'max' else W
        type_print(f" {Y}Plan: {plan_color}{stats['plan'].upper()}{RESET}", Y, 0.01)
        
        if stats.get('planExpiry'):
            type_print(f" {Y}Plan Expiry In: {W}{stats['planExpiry']}{RESET}", Y, 0.01)
        
        print(LINE)
        type_print(f" {C}【STATISTICS】{RESET}", C, 0.02)
        type_print(f" {Y}Total Shares: {G}{stats['totalShares']}{RESET}", Y, 0.01)
        type_print(f" {Y}Total Cookies: {C}{stats.get('cookieCount', 0)}{RESET}", Y, 0.01)
        print(LINE)
        
        share_cd = stats.get('shareCooldown', {})
        
        type_print(f" {C}【COOLDOWN STATUS】{RESET}", C, 0.02)
        
        if share_cd.get('active'):
            type_print(f" {R}Share Cooldown: {share_cd['remainingSeconds']}s remaining{RESET}", R, 0.01)
            type_print(f" {Y}Available at: {W}{share_cd['availableAt']}{RESET}", Y, 0.01)
        else:
            type_print(f" {G}Share: Ready ✓{RESET}", G, 0.01)
        
        print(LINE)
    else:
        type_print(f" {R}【ERROR】 {response if isinstance(response, str) else response.get('message', 'Failed to get stats')}{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def manage_cookies():
    """Manage cookie database"""
    while True:
        refresh_screen()
        type_print(f" {G}【MANAGE COOKIES】{RESET}", G, 0.02)
        print(LINE)
        type_print(f" 【{W}1{W}】 {G}VIEW ALL COOKIES{RESET}", W, 0.01)
        type_print(f" 【{W}2{W}】 {G}ADD COOKIE{RESET}", W, 0.01)
        type_print(f" 【{W}3{W}】 {R}DELETE COOKIE{RESET}", W, 0.01)
        type_print(f" 【{W}4{W}】 {R}DELETE ALL COOKIES{RESET}", W, 0.01)
        type_print(f" 【{W}0{W}】 {Y}BACK{RESET}", W, 0.01)
        print(LINE)
        
        choice = animated_input("CHOICE", C).strip()
        
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
            type_print(f"\n {R}【!】 INVALID SELECTION{RESET}", R, 0.02)
            time.sleep(0.8)

def view_cookies():
    """View all cookies"""
    refresh_screen()
    type_print(f" {G}【!】 LOADING COOKIES...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status == 200 and response.get('success'):
        cookies = response.get('cookies', [])
        
        refresh_screen()
        type_print(f" {G}【COOKIES】 Total: {len(cookies)}{RESET}", G, 0.02)
        print(LINE)
        
        if not cookies:
            type_print(f" {Y}No cookies stored yet.{RESET}", Y, 0.02)
        else:
            for i, cookie_data in enumerate(cookies, 1):
                status_color = G if cookie_data['status'] == 'active' else R if cookie_data['status'] == 'restricted' else Y
                status_display = cookie_data['status'].upper()
                
                type_print(f" 【{i:02d}】 {M}{cookie_data['name']}{RESET} ({C}UID: {cookie_data['uid']}{RESET})", W, 0.01)
                cookie_preview = cookie_data['cookie'][:50] + "..." if len(cookie_data['cookie']) > 50 else cookie_data['cookie']
                type_print(f"      Cookie: {C}{cookie_preview}{RESET}", W, 0.01)
                type_print(f"      Added: {Y}{cookie_data['addedAt']}{RESET}", W, 0.01)
                type_print(f"      Status: {status_color}{status_display}{RESET}", W, 0.01)
                
                if cookie_data['status'] == 'restricted':
                    type_print(f"      {R}⚠ WARNING: This account is restricted!{RESET}", R, 0.01)
                
                print(LINE)
        
    else:
        type_print(f" {R}【ERROR】 Failed to load cookies{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def add_cookie():
    """Add new cookie"""
    refresh_screen()
    type_print(f" {G}【ADD COOKIE】{RESET}", G, 0.02)
    print(LINE)
    
    # Check if user can add more cookies
    if user_data['plan'] == 'free' and user_data.get('cookieCount', 0) >= 10:
        type_print(f" {R}【LIMIT REACHED】{RESET}", R, 0.02)
        print(LINE)
        type_print(f" {Y}FREE plan users can only store up to 10 cookies.{RESET}", Y, 0.02)
        type_print(f" {Y}You currently have: {R}{user_data.get('cookieCount', 0)}/10{RESET}", Y, 0.02)
        print(LINE)
        type_print(f" {G}【UPGRADE TO MAX】{RESET}", G, 0.02)
        type_print(f" {Y}• Unlimited cookies{RESET}", Y, 0.01)
        type_print(f" {Y}• No cooldowns{RESET}", Y, 0.01)
        type_print(f" {Y}• Rental: 1 month (₱150) or 3 months (₱250){RESET}", Y, 0.01)
        print(LINE)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    cookie = animated_input("COOKIE", C).strip()
    if not cookie:
        return
    
    refresh_screen()
    type_print(f" {Y}【!】 VALIDATING COOKIE...{RESET}", Y, 0.02)
    type_print(f" {C}This may take 10-15 seconds{RESET}", C, 0.02)
    print(LINE)
    nice_loader("VALIDATING")
    
    status, response = api_request("POST", "/user/cookies", {
        "cookie": cookie
    })
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        type_print(f" {G}【SUCCESS】 {response.get('message')}{RESET}", G, 0.02)
        print(LINE)
        type_print(f" {Y}Name: {M}{response.get('name', 'Unknown')}{RESET}", Y, 0.01)
        type_print(f" {Y}UID: {C}{response.get('uid', 'Unknown')}{RESET}", Y, 0.01)
        type_print(f" {Y}Status: {G if response.get('status') == 'active' else R}{response.get('status', 'unknown').upper()}{RESET}", Y, 0.01)
        
        # Show restriction warning
        if response.get('restricted'):
            print(LINE)
            type_print(f" {R}⚠ WARNING: This account is RESTRICTED!{RESET}", R, 0.02)
            type_print(f" {Y}Restricted accounts may not be able to share posts.{RESET}", Y, 0.02)
        
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
            
            # Show remaining slots for FREE users
            if user_data['plan'] == 'free':
                remaining = 10 - user_data['cookieCount']
                print(LINE)
                type_print(f" {Y}Remaining Slots: {C}{remaining}/10{RESET}", Y, 0.01)
        
        print(LINE)
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed to add cookie') if isinstance(response, dict) else 'Failed to add cookie'
        type_print(f" {R}【ERROR】 {error_msg}{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def delete_cookie():
    """Delete a specific cookie"""
    refresh_screen()
    type_print(f" {G}【!】 LOADING COOKIES...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not isinstance(response, dict) or not response.get('success'):
        error_msg = response if isinstance(response, str) else 'Failed to load cookies'
        type_print(f" {R}【ERROR】 {error_msg}{RESET}", R, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        refresh_screen()
        type_print(f" {Y}No cookies to delete.{RESET}", Y, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    refresh_screen()
    type_print(f" {R}【DELETE COOKIE】{RESET}", R, 0.02)
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        status_indicator = f"{R}【RESTRICTED】{RESET}" if cookie_data['status'] == 'restricted' else f"{G}【ACTIVE】{RESET}"
        type_print(f" 【{i}】 {M}{cookie_data['name']}{RESET} ({C}UID: {cookie_data['uid']}{RESET}) {status_indicator}", W, 0.01)
    
    print(LINE)
    
    choice = animated_input("SELECT COOKIE NUMBER (0 to cancel)", C).strip()
    
    if not choice or choice == '0':
        return
    
    try:
        cookie_index = int(choice) - 1
        if cookie_index < 0 or cookie_index >= len(cookies):
            type_print(f" {R}【ERROR】 Invalid cookie number{RESET}", R, 0.02)
            time.sleep(1)
            return
        
        selected_cookie = cookies[cookie_index]
    except:
        type_print(f" {R}【ERROR】 Invalid input{RESET}", R, 0.02)
        time.sleep(1)
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/user/cookies/{selected_cookie['id']}")
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        type_print(f" {G}【SUCCESS】 Cookie deleted!{RESET}", G, 0.02)
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
    else:
        error_msg = response if isinstance(response, str) else 'Failed to delete cookie'
        type_print(f" {R}【ERROR】 {error_msg}{RESET}", R, 0.02)
    
    print(LINE)
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def delete_all_cookies():
    """Delete all cookies"""
    refresh_screen()
    type_print(f" {R}【DELETE ALL COOKIES】{RESET}", R, 0.02)
    print(LINE)
    
    confirm = animated_input("Delete ALL cookies? This cannot be undone! (YES/NO)", R).strip().upper()
    
    if confirm != 'YES':
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", "/user/cookies")
    
    if status == 200 and response.get('success'):
        type_print(f" {G}【SUCCESS】 {response.get('message')}{RESET}", G, 0.02)
        if user_data:
            user_data['cookieCount'] = 0
    else:
        type_print(f" {R}【ERROR】 Failed to delete cookies{RESET}", R, 0.02)
    
    print(LINE)
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def update_tool_logic():
    """Simulates an update and restarts the script."""
    type_print(f" {G}【!】 CHECKING FOR UPDATES...{RESET}", G, 0.02)
    nice_loader("CHECKING")
    
    type_print(f" {G}【!】 NEW VERSION FOUND! DOWNLOADING...{RESET}", G, 0.02)
    nice_loader("UPDATING")
    
    type_print(f" {G}【!】 UPDATE COMPLETE. RESTARTING...{RESET}", G, 0.02)
    time.sleep(1)
    
    os.execv(sys.executable, ['python'] + sys.argv)

# ============ ADMIN PANEL FUNCTIONS ============

def admin_panel():
    """Admin panel for managing users"""
    while True:
        refresh_screen()
        type_print(f" {M}【ADMIN PANEL】{RESET}", M, 0.02)
        print(LINE)
        type_print(f" 【{W}1{W}】 {G}VIEW ALL USERS{RESET}", W, 0.01)
        type_print(f" 【{W}2{W}】 {Y}CHANGE USER PLAN{RESET}", W, 0.01)
        type_print(f" 【{W}3{W}】 {R}DELETE USER{RESET}", W, 0.01)
        type_print(f" 【{W}4{W}】 {C}VIEW ACTIVITY LOGS{RESET}", W, 0.01)
        type_print(f" 【{W}5{W}】 {G}DASHBOARD STATS{RESET}", W, 0.01)
        type_print(f" 【{W}0{W}】 {Y}BACK{RESET}", W, 0.01)
        print(LINE)
        
        choice = animated_input("CHOICE", C).strip()
        
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
            type_print(f"\n {R}【!】 INVALID SELECTION{RESET}", R, 0.02)
            time.sleep(0.8)

def view_all_users():
    """View all registered users"""
    refresh_screen()
    type_print(f" {G}【!】 LOADING USERS...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/users")
    
    if status == 200 and response.get('success'):
        users = response.get('users', [])
        
        refresh_screen()
        type_print(f" {G}【ALL USERS】 Total: {len(users)}{RESET}", G, 0.02)
        print(LINE)
        
        for i, user in enumerate(users, 1):
            plan_color = G if user['plan'] == 'max' else W
            admin_badge = f" {M}【ADMIN】{RESET}" if user.get('isAdmin') else ""
            
            type_print(f" 【{i:02d}】 {C}{user['username'].upper()}{RESET}{admin_badge}", W, 0.01)
            type_print(f"      Plan: {plan_color}{user['plan'].upper()}{RESET} | Country: {G}{user['country']}{RESET}", W, 0.01)
            type_print(f"      Shares: {Y}{user['totalShares']}{RESET}", W, 0.01)
            type_print(f"      Total Cookies: {C}{user.get('cookieCount', 0)}{RESET}", W, 0.01)
            print(LINE)
        
    else:
        type_print(f" {R}【ERROR】 Failed to get users{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def change_user_plan():
    """Change a user's plan"""
    refresh_screen()
    type_print(f" {Y}【CHANGE USER PLAN】{RESET}", Y, 0.02)
    print(LINE)
    
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        type_print(f" {R}【ERROR】 Failed to load users{RESET}", R, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    users = response.get('users', [])
    
    type_print(f" {G}【SELECT USER】{RESET}", G, 0.02)
    print(LINE)
    for i, user in enumerate(users, 1):
        plan_color = G if user['plan'] == 'max' else W
        type_print(f" 【{i}】 {C}{user['username'].upper()}{RESET} - Plan: {plan_color}{user['plan'].upper()}{RESET}", W, 0.01)
    print(LINE)
    
    user_choice = animated_input("SELECT USER NUMBER (0 to cancel)", C).strip()
    
    if not user_choice or user_choice == '0':
        return
    
    try:
        user_index = int(user_choice) - 1
        if user_index < 0 or user_index >= len(users):
            type_print(f" {R}【ERROR】 Invalid user number{RESET}", R, 0.02)
            time.sleep(1)
            return
        
        selected_user = users[user_index]
    except:
        type_print(f" {R}【ERROR】 Invalid input{RESET}", R, 0.02)
        time.sleep(1)
        return
    
    refresh_screen()
    type_print(f" {Y}【CHANGE PLAN FOR: {selected_user['username'].upper()}】{RESET}", Y, 0.02)
    print(LINE)
    type_print(f" 【1】 {W}FREE{RESET} - 10 cookies max", W, 0.01)
    type_print(f" 【2】 {G}MAX{RESET} - Unlimited cookies (RENTAL)", W, 0.01)
    type_print(f" 【3】 {M}MAX LIFETIME{RESET} - Unlimited cookies (PERMANENT)", W, 0.01)
    print(LINE)
    
    plan_choice = animated_input("SELECT PLAN NUMBER", C).strip()
    
    plan_map = {'1': 'free', '2': 'max', '3': 'max'}
    
    if plan_choice not in plan_map:
        type_print(f" {R}【ERROR】 Invalid plan{RESET}", R, 0.02)
        time.sleep(1)
        return
    
    new_plan = plan_map[plan_choice]
    duration = None
    
    if plan_choice == '2':  # MAX RENTAL
        refresh_screen()
        type_print(f" {Y}【MAX PLAN DURATION】{RESET}", Y, 0.02)
        print(LINE)
        type_print(f" 【1】 1 Month", W, 0.01)
        type_print(f" 【2】 2 Months", W, 0.01)
        type_print(f" 【3】 3 Months", W, 0.01)
        print(LINE)
        
        duration_choice = animated_input("SELECT DURATION", C).strip()
        
        duration_map = {'1': 1, '2': 2, '3': 3}
        
        if duration_choice not in duration_map:
            type_print(f" {R}【ERROR】 Invalid duration{RESET}", R, 0.02)
            time.sleep(1)
            return
        
        duration = duration_map[duration_choice]
    # plan_choice == '3' means LIFETIME (duration stays None)
    
    refresh_screen()
    type_print(f" {Y}【CONFIRM CHANGE】{RESET}", Y, 0.02)
    print(LINE)
    type_print(f" User: {C}{selected_user['username'].upper()}{RESET}", Y, 0.01)
    type_print(f" Current Plan: {W}{selected_user['plan'].upper()}{RESET}", Y, 0.01)
    if plan_choice == '3':
        type_print(f" New Plan: {M}MAX LIFETIME{RESET}", Y, 0.01)
    else:
        type_print(f" New Plan: {G}{new_plan.upper()}{RESET}", Y, 0.01)
    if duration:
        type_print(f" Duration: {Y}{duration} month(s){RESET}", Y, 0.01)
    print(LINE)
    
    confirm = animated_input("Confirm? (Y/N)", Y).strip().upper()
    
    if confirm != 'Y':
        return
    
    nice_loader("UPDATING")
    
    status, response = api_request("PUT", f"/admin/users/{selected_user['username']}/plan", {
        "plan": new_plan,
        "duration": duration
    })
    
    if status == 200 and response.get('success'):
        type_print(f" {G}【SUCCESS】 Plan updated successfully!{RESET}", G, 0.02)
    else:
        type_print(f" {R}【ERROR】 {response.get('message', 'Failed to update plan')}{RESET}", R, 0.02)
    
    print(LINE)
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def delete_user():
    """Delete a user account"""
    refresh_screen()
    type_print(f" {R}【DELETE USER】{RESET}", R, 0.02)
    print(LINE)
    
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        type_print(f" {R}【ERROR】 Failed to load users{RESET}", R, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    users = response.get('users', [])
    
    if not users:
        type_print(f" {Y}No users to delete.{RESET}", Y, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    type_print(f" {G}【SELECT USER TO DELETE】{RESET}", G, 0.02)
    print(LINE)
    
    for i, user in enumerate(users, 1):
        plan_color = G if user['plan'] == 'max' else W
        admin_badge = f" {M}【ADMIN】{RESET}" if user.get('isAdmin') else ""
        
        type_print(f" 【{i:02d}】 {C}{user['username'].upper()}{RESET}{admin_badge} - {plan_color}{user['plan'].upper()}{RESET}", W, 0.01)
    
    type_print(f" 【00】 {Y}CANCEL{RESET}", W, 0.01)
    print(LINE)
    
    choice = animated_input("SELECT USER", C).strip()
    
    if not choice or choice in ['0', '00']:
        return
    
    try:
        user_index = int(choice) - 1
        if user_index < 0 or user_index >= len(users):
            type_print(f" {R}【ERROR】 Invalid selection{RESET}", R, 0.02)
            time.sleep(1)
            return
        
        selected_user = users[user_index]
    except:
        type_print(f" {R}【ERROR】 Invalid input{RESET}", R, 0.02)
        time.sleep(1)
        return
    
    refresh_screen()
    type_print(f" {R}【CONFIRM DELETION】{RESET}", R, 0.02)
    print(LINE)
    type_print(f" User: {C}{selected_user['username'].upper()}{RESET}", Y, 0.01)
    type_print(f" Plan: {W}{selected_user['plan'].upper()}{RESET}", Y, 0.01)
    type_print(f" Country: {W}{selected_user['country']}{RESET}", Y, 0.01)
    print(LINE)
    
    confirm = animated_input("Delete this user? This cannot be undone! (YES/NO)", R).strip().upper()
    
    if confirm != 'YES':
        return
    
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/admin/users/{selected_user['username']}")
    
    if status == 200 and response.get('success'):
        type_print(f" {G}【SUCCESS】 User '{selected_user['username']}' deleted successfully!{RESET}", G, 0.02)
    else:
        type_print(f" {R}【ERROR】 {response.get('message', 'Failed to delete user')}{RESET}", R, 0.02)
    
    print(LINE)
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def view_activity_logs():
    """View recent activity logs"""
    refresh_screen()
    type_print(f" {G}【!】 LOADING ACTIVITY LOGS...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/logs?limit=20")
    
    if status == 200 and response.get('success'):
        logs = response.get('logs', [])
        
        refresh_screen()
        type_print(f" {C}【ACTIVITY LOGS】 Recent 20{RESET}", C, 0.02)
        print(LINE)
        
        for log in logs:
            action_color = G if log['action'] == 'login' else Y if log['action'] == 'register' else C
            type_print(f" 【{log['timestamp']}】", W, 0.01)
            type_print(f" User: {C}{log['username'].upper()}{RESET} | Action: {action_color}{log['action'].upper()}{RESET}", W, 0.01)
            if log.get('details'):
                type_print(f" Details: {W}{log['details']}{RESET}", W, 0.01)
            print(LINE)
    else:
        type_print(f" {R}【ERROR】 Failed to load logs{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

def dashboard_stats():
    """Show admin dashboard statistics"""
    refresh_screen()
    type_print(f" {G}【!】 LOADING DASHBOARD...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/dashboard")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats', {})
        
        refresh_screen()
        type_print(f" {G}【ADMIN DASHBOARD】{RESET}", G, 0.02)
        print(LINE)
        
        type_print(f" {C}【USER STATISTICS】{RESET}", C, 0.02)
        type_print(f" Total Users: {G}{stats['totalUsers']}{RESET}", Y, 0.01)
        type_print(f" FREE Users: {W}{stats['planDistribution']['free']}{RESET}", Y, 0.01)
        type_print(f" MAX Users: {G}{stats['planDistribution']['max']}{RESET}", Y, 0.01)
        print(LINE)
        
        type_print(f" {C}【ACTIVITY STATISTICS】{RESET}", C, 0.02)
        type_print(f" Total Shares: {G}{stats['totalShares']}{RESET}", Y, 0.01)
        print(LINE)
        
        type_print(f" {C}【RECENT USERS】{RESET}", C, 0.02)
        for user in stats.get('recentUsers', []):
            plan_color = G if user['plan'] == 'max' else W
            type_print(f" {C}{user['username'].upper()}{RESET} - {plan_color}{user['plan'].upper()}{RESET} - {G}{user['country']}{RESET}", W, 0.01)
        print(LINE)
    else:
        type_print(f" {R}【ERROR】 Failed to load dashboard{RESET}", R, 0.02)
        print(LINE)
    
    input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

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
                type_print(f" {R}【ERROR】 Incorrect post link! Please re-enter{RESET}", R, 0.02)
                return None
    except Exception as e:
        type_print(f" {R}【ERROR】 Failed to get post ID: {e}{RESET}", R, 0.02)
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
                        sys.stdout.write(f"\r {Y}【TOKEN RENEWED】{RESET} {W}|{RESET} {B}【UID: {account_uid}】{RESET}                              ")
                        sys.stdout.flush()
                        time.sleep(0.5)
                    else:
                        now = datetime.datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f" {Y}【RENEWED】{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {C}Token renewed{RESET}")
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            is_success, result = await share_with_eaag(session, cookie, current_token, post_id)
            
            if is_success:
                async with lock:
                    success_count += 1
                    current_count = success_count
                
                failed_consecutive = 0
                
                if display_mode == 'minimal':
                    sys.stdout.write(f"\r {G}【SUCCESS — {current_count}】{RESET} {W}|{RESET} {C}【UID: {account_uid}】{RESET}                    ")
                    sys.stdout.flush()
                else:
                    print(f" {G}【SUCCESS】{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {Y}Total: {current_count}{RESET}")
                
                # ZERO DELAY - Continue immediately
            else:
                failed_consecutive += 1
                error_message = result
                
                # If failed 3 times consecutively, try to renew token
                if failed_consecutive >= 3:
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {Y}【RENEWING...】{RESET} {W}|{RESET} {B}【UID: {account_uid}】{RESET}                          ")
                        sys.stdout.flush()
                    else:
                        print(f" {Y}【RENEWING】{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {Y}Attempting token renewal...{RESET}")
                    
                    new_token = await renew_eaag_token(cookie)
                    
                    if new_token:
                        current_token = new_token
                        last_token_renewal = time.time()
                        failed_consecutive = 0
                        
                        if display_mode == 'minimal':
                            sys.stdout.write(f"\r {G}【TOKEN RENEWED】{RESET} {W}|{RESET} {B}【UID: {account_uid}】{RESET}                            ")
                            sys.stdout.flush()
                            time.sleep(0.5)
                        else:
                            print(f" {G}【RENEWED】{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {G}Token renewed successfully{RESET}")
                    else:
                        if display_mode != 'minimal':
                            print(f" {R}【ERROR】{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                        await asyncio.sleep(5)  # Brief pause after failed renewal
                else:
                    if display_mode != 'minimal':
                        print(f" {R}【ERROR】{RESET} {W}|{RESET} {M}{current_time}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_message[:40]}{RESET}")
                    # ZERO DELAY - Continue immediately even after errors
        
        except asyncio.CancelledError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_msg = str(e)
            if "asyncio" not in error_msg.lower() and "event" not in error_msg.lower():
                if display_mode != 'minimal':
                    print(f" {R}【ERROR】{RESET} {W}|{RESET} {M}{datetime.datetime.now().strftime('%H:%M:%S')}{RESET} {W}|{RESET} {C}{account_uid}{RESET} {W}|{RESET} {R}{error_msg[:40]}{RESET}")
            # ZERO DELAY - Continue immediately after exceptions

async def auto_share_main(link_or_id, selected_cookies):
    """Main auto share function using selected database cookies with EAAG tokens."""
    global success_count
    success_count = 0
    
    refresh_screen()
    type_print(f" {C}【!】 CONVERTING SELECTED COOKIES TO EAAG TOKENS...{RESET}", C, 0.02)
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
            status_indicator = f"{R}【RESTRICTED】{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}【ACTIVE】{RESET}"
            type_print(f" {G}✓{RESET} {Y}{cookie_data['name']}{RESET} ({C}UID: {cookie_data['uid']}{RESET}) {status_indicator}", W, 0.01)
        else:
            type_print(f" {R}✗{RESET} {Y}{cookie_data['name']}{RESET} {R}Failed to extract EAAG token{RESET}", W, 0.01)
    
    if not eaag_tokens:
        type_print(f" {R}【ERROR】 No valid EAAG tokens extracted!{RESET}", R, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return
    
    # Extract post ID
    async with aiohttp.ClientSession() as session:
        post_id = extract_post_id_from_link(link_or_id)
        
        # If extraction failed or looks like a full URL, try API method
        if not post_id.isdigit():
            refresh_screen()
            type_print(f" {G}【!】 EXTRACTING POST ID FROM LINK...{RESET}", G, 0.02)
            nice_loader("EXTRACTING")
            
            post_id = await getid(session, link_or_id)
            if not post_id:
                type_print(f" {R}【ERROR】 Failed to get post ID{RESET}", R, 0.02)
                input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
                return
    
    # Select display mode
    display_mode = select_progress_display()
    
    refresh_screen()
    type_print(f" {G}【SUCCESS】 Extracted {len(eaag_tokens)} EAAG tokens{RESET}", G, 0.02)
    print(LINE)
    type_print(f" {Y}Post ID: {G}{post_id}{RESET}", Y, 0.01)
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        type_print(f" {M}【AUTO SHARE CONFIGURATION】{RESET}", M, 0.02)
        print(LINE)
        type_print(f" {Y}Mode: {C}NORM ACC (EAAG Tokens){RESET}", Y, 0.01)
        type_print(f" {Y}Total Accounts: {G}{len(eaag_tokens)}{RESET}", Y, 0.01)
        type_print(f" {Y}Share Speed: {G}MAXIMUM (ZERO DELAYS){RESET}", Y, 0.01)
        type_print(f" {Y}Token Renewal: {C}Auto every 3 minutes{RESET}", Y, 0.01)
        type_print(f" {Y}Renewal Safety: {G}Detection & Error Handling{RESET}", Y, 0.01)
        print(LINE)
        type_print(f" {G}【!】 STARTING AUTO SHARE...{RESET}", G, 0.02)
        type_print(f" {Y}【TIP】 Press Ctrl+C to stop{RESET}", Y, 0.02)
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
        
        print(f" {G}【STARTED】 Running {len(tasks)} parallel share threads at MAXIMUM SPEED (ZERO DELAYS)...{RESET}")
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
    type_print(f" {G}【!】 LOADING COOKIES FROM DATABASE...{RESET}", G, 0.02)
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not response.get('success'):
        type_print(f" {R}【ERROR】 Failed to load cookies{RESET}", R, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return None
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        type_print(f" {R}【ERROR】 No cookies stored in database{RESET}", R, 0.02)
        type_print(f" {Y}【TIP】 Use option 2 to add cookies{RESET}", Y, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
        return None
    
    refresh_screen()
    type_print(f" {C}【SELECT COOKIES FOR AUTO SHARE】{RESET}", C, 0.02)
    print(LINE)
    type_print(f" 【{BG_G}{W}ALL{RESET}】 {G}USE ALL COOKIES{RESET}", W, 0.01)
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        letter = chr(64 + i) if i <= 26 else str(i)
        status_indicator = f"{R}【RESTRICTED】{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}【ACTIVE】{RESET}"
        type_print(f" 【{BG_C}{W}{i:02d}{RESET}{Y}/{BG_C}{W}{letter}{RESET}】 {C}{cookie_data['name']}{RESET} ({Y}UID: {cookie_data['uid']}{RESET}) {status_indicator}", W, 0.01)
    
    print(LINE)
    type_print(f" {Y}【TIP】 Enter numbers separated by commas (e.g., 1,2,3) or type 'ALL'{RESET}", Y, 0.02)
    print(LINE)
    
    selection = animated_input("SELECT", C).strip().upper()
    
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
            type_print(f" {R}【ERROR】 Invalid selection{RESET}", R, 0.02)
            time.sleep(1)
            return None
    
    if not selected_cookies:
        type_print(f" {R}【ERROR】 No valid cookies selected{RESET}", R, 0.02)
        time.sleep(1)
        return None
    
    # Confirmation
    refresh_screen()
    type_print(f" {Y}【CONFIRM SELECTION】{RESET}", Y, 0.02)
    print(LINE)
    type_print(f" {Y}Selected {G}{len(selected_cookies)}{Y} cookie(s):{RESET}", Y, 0.02)
    for cookie_data in selected_cookies:
        status_indicator = f"{R}【RESTRICTED】{RESET}" if cookie_data.get('status') == 'restricted' else f"{G}【ACTIVE】{RESET}"
        type_print(f"   • {C}{cookie_data['name']}{RESET} ({Y}UID: {cookie_data['uid']}{RESET}) {status_indicator}", W, 0.01)
    print(LINE)
    
    # Check for restricted cookies
    restricted_count = sum(1 for c in selected_cookies if c.get('status') == 'restricted')
    if restricted_count > 0:
        type_print(f" {R}⚠ WARNING: {restricted_count} restricted account(s) detected!{RESET}", R, 0.02)
        type_print(f" {Y}Restricted accounts may not be able to share posts.{RESET}", Y, 0.02)
        print(LINE)
    
    confirm = animated_input("Confirm? (Y/N)", Y).strip().upper()
    
    if confirm == 'Y':
        return selected_cookies
    else:
        return None

def start_auto_share():
    """Entry point for auto share feature."""
    refresh_screen()
    
    # Display informational message
    type_print(f" {C}【!】 AUTO SHARE - NORMAL ACCOUNTS{RESET}", C, 0.02)
    print(LINE)
    type_print(f" {G}【✓】 INFORMATION:{RESET}", G, 0.02)
    type_print(f" {W}• Make sure your post is set to PUBLIC{RESET}", W, 0.01)
    type_print(f" {W}• This uses EAAG tokens (business.facebook.com method){RESET}", W, 0.01)
    type_print(f" {W}• Shares run at MAXIMUM SPEED (zero delays){RESET}", W, 0.01)
    type_print(f" {W}• Tokens auto-renew every 3 minutes{RESET}", W, 0.01)
    type_print(f" {W}• Enhanced cookie validation with restriction detection{RESET}", W, 0.01)
    type_print(f" {W}• Best for normal accounts{RESET}", W, 0.01)
    print(LINE)
    
    # Brief delay to let user read
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r {C}【CONTINUE IN {i} SECONDS】{RESET} {W}Reading time...{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write(f"\r{' ' * 60}\r")
    sys.stdout.flush()
    
    selected_cookies = select_cookies_for_sharing()
    
    if not selected_cookies:
        return
    
    refresh_screen()
    type_print(f" {C}【AUTO SHARE】{RESET}", C, 0.02)
    print(LINE)
    
    link_or_id = animated_input("POST LINK OR ID", C).strip()
    
    if not link_or_id:
        return
    
    try:
        asyncio.run(auto_share_main(link_or_id, selected_cookies))
    except KeyboardInterrupt:
        refresh_screen()
        type_print(f" {Y}【!】 AUTO SHARE STOPPED BY USER{RESET}", Y, 0.02)
        stop_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        type_print(f" {Y}【!】 Stop Time: {stop_time}{RESET}", Y, 0.02)
        type_print(f" {G}【!】 Total Successful Shares: {success_count}{RESET}", G, 0.02)
        print(LINE)
        
        if success_count > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count})
            type_print(f" {G}【!】 Shares recorded to your account{RESET}", G, 0.02)
        
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")
    except Exception as e:
        refresh_screen()
        type_print(f" {R}【ERROR】 An unexpected error occurred:{RESET}", R, 0.02)
        type_print(f" {R}{str(e)}{RESET}", R, 0.02)
        input(f"\n {Y}【PRESS ENTER TO CONTINUE】{RESET}")

# ============ MAIN FUNCTION ============

def main():
    global user_token, user_data
    
    # Initial loading animation
    clear()
    type_print("【*】 Loading Modules...", W, 0.03)
    time.sleep(0.5)
    
    while True:
        refresh_screen()
        
        try:
            choice = animated_input("CHOICE", C).upper()
        except KeyboardInterrupt:
            sys.exit()

        refresh_screen()

        if not user_token:
            if choice in ['1', '01', 'A']:
                login_user()
            elif choice in ['2', '02', 'B']:
                register_user()
            elif choice in ['0', '00', 'X']:
                type_print(f"\n {R}【!】 EXITING TOOL...{RESET}", R, 0.02)
                sys.exit()
            else:
                type_print(f"\n {R}【!】 INVALID SELECTION{RESET}", R, 0.02)
                time.sleep(0.8)
        else:
            if choice in ['1', '01', 'A']:
                start_auto_share()
                
            elif choice in ['2', '02', 'B']:
                manage_cookies()
            
            elif choice in ['3', '03', 'C']:
                show_user_stats()
            
            elif choice in ['4', '04', 'D']:
                if user_data and user_data.get('isAdmin'):
                    admin_panel()
                else:
                    update_tool_logic()
            
            elif choice in ['5', '05', 'E']:
                if user_data and user_data.get('isAdmin'):
                    update_tool_logic()
                else:
                    type_print(f"\n {R}【!】 INVALID SELECTION{RESET}", R, 0.02)
                    time.sleep(0.8)
                
            elif choice in ['0', '00', 'X']:
                type_print(f"\n {Y}【!】 LOGGING OUT...{RESET}", Y, 0.02)
                user_token = None
                user_data = None
                time.sleep(1)
                
            else:
                type_print(f"\n {R}【!】 INVALID SELECTION{RESET}", R, 0.02)
                time.sleep(0.8)

if __name__ == "__main__":
    main()
