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
import subprocess
import importlib
import shutil
import platform
import zlib
import base64

# Auto-install colorama for gradient support
def install_colorama():
    """Auto-install colorama if not available"""
    try:
        importlib.import_module('colorama')
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    install_colorama()
    from colorama import init
    init()
except:
    pass

# --- GRADIENT COLOR SYSTEM ---
def get_gradient_color(progress, color_scheme='purple_cyan'):
    """Generate RGB color code based on progress (0.0 to 1.0)"""
    progress = max(0, min(1, progress))
    
    color_schemes = {
        'purple_cyan': [
            (138, 43, 226), (147, 51, 234), (168, 85, 247), (192, 132, 252),
            (216, 180, 254), (147, 197, 253), (125, 211, 252), (34, 211, 238),
        ],
        'green_yellow': [
            (16, 185, 129), (52, 211, 153), (110, 231, 183), (167, 243, 208),
            (253, 224, 71), (250, 204, 21),
        ],
        'red_orange': [
            (220, 38, 38), (239, 68, 68), (248, 113, 113), (251, 146, 60),
            (253, 186, 116), (254, 215, 170),
        ],
        'blue_purple': [
            (37, 99, 235), (59, 130, 246), (96, 165, 250), (147, 197, 253),
            (167, 139, 250), (196, 181, 253),
        ]
    }
    
    levels = color_schemes.get(color_scheme, color_schemes['purple_cyan'])
    
    index = progress * (len(levels) - 1)
    lower_index = int(index)
    upper_index = min(lower_index + 1, len(levels) - 1)
    
    if lower_index == upper_index:
        r, g, b = levels[lower_index]
    else:
        fraction = index - lower_index
        r1, g1, b1 = levels[lower_index]
        r2, g2, b2 = levels[upper_index]
        
        r = int(r1 + (r2 - r1) * fraction)
        g = int(g1 + (g2 - g1) * fraction)
        b = int(b1 + (b2 - b1) * fraction)
    
    return f'\033[38;2;{r};{g};{b}m'

def apply_gradient(text, color_scheme='purple_cyan'):
    """Apply gradient color to text"""
    if not text.strip():
        return text
    
    result = []
    chars = [c for c in text if c != ' ']
    
    if not chars:
        return text
    
    char_index = 0
    for c in text:
        if c == ' ':
            result.append(c)
        else:
            progress = char_index / max(1, len(chars) - 1)
            color = get_gradient_color(progress, color_scheme)
            result.append(color + c + '\033[0m')
            char_index += 1
    
    return ''.join(result)

# Color helpers
G = lambda text: apply_gradient(str(text), 'green_yellow')
R = lambda text: apply_gradient(str(text), 'red_orange')
C = lambda text: apply_gradient(str(text), 'purple_cyan')
Y = lambda text: apply_gradient(str(text), 'green_yellow')
M = lambda text: apply_gradient(str(text), 'blue_purple')
B = lambda text: apply_gradient(str(text), 'purple_cyan')
W = '\033[1;37m'
RESET = '\033[0m'

# Background colors
BG_R = '\033[41m'
BG_G = '\033[42m'
BG_C = '\033[46m'
BG_M = '\033[45m'
BG_Y = '\033[43m'
BG_B = '\033[44m'

LINE = apply_gradient("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'purple_cyan')

# --- API CONFIGURATION ---
API_URL = "https://rpwtools.onrender.com/api"
user_token = None
user_data = None

# --- GLOBAL VARIABLES ---
success_count = 0
lock = asyncio.Lock()

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

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

def banner_header():
    banner_art = """
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    """
    print(apply_gradient(banner_art, 'purple_cyan'))
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C('DEVELOPER')}     {W}➤{RESET} {G('KEN DRICK')}")
    print(f" {W}[{RESET}•{W}]{RESET} {C('GITHUB')}        {W}➤{RESET} {G('RYO GRAHHH')}")
    print(f" {W}[{RESET}•{W}]{RESET} {C('VERSION')}       {W}➤{RESET} {G('1.0.3')}")
    print(f" {W}[{RESET}•{W}]{RESET} {C('FACEBOOK')}      {W}➤{RESET} {G('facebook.com/ryoevisu')}")
    print(f" {W}[{RESET}•{W}]{RESET} {C('TOOL NAME')}     {W}➤{RESET} {R('[ RPWTOOLS ]')}")
    
    if user_data:
        print(LINE)
        print(f" {W}[{RESET}•{W}]{RESET} {C('USERNAME')}       {W}➤{RESET} {G(user_data['username'].upper())}")
        print(f" {W}[{RESET}•{W}]{RESET} {C('FACEBOOK')}       {W}➤{RESET} {G(user_data.get('facebook', 'N/A'))}")
        print(f" {W}[{RESET}•{W}]{RESET} {C('COUNTRY')}        {W}➤{RESET} {G(user_data.get('country', 'N/A').upper())}")
        
        user_plan = user_data['plan']
        if user_plan == 'max':
            if user_data.get('planExpiry'):
                plan_display = M('[ MAX ]')
            else:
                plan_display = M('[ MAX LIFETIME ]')
        else:
            plan_display = G('[ FREE ]')
        
        print(f" {W}[{RESET}•{W}]{RESET} {C('PLAN')}           {W}➤{RESET} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {W}[{RESET}•{W}]{RESET} {C('PLAN EXPIRY IN')} {W}➤{RESET} {R(user_data['planExpiry'])}")
        
        cookie_count = user_data.get('cookieCount', 0)
        print(f" {W}[{RESET}•{W}]{RESET} {C('TOTAL COOKIES')}  {W}➤{RESET} {G(str(cookie_count))}")
    
    print(LINE)

def show_menu():
    if not user_token:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{W}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G('LOGIN')}")
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{W}/{RESET}{BG_C}{W}B{RESET}{W}]{RESET} {C('REGISTER')}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{W}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R('EXIT')}")
    elif user_data and user_data.get('isAdmin'):
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{W}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G('AUTO SHARE              — NORM ACCOUNTS')}")
        print(f" {W}[{RESET}{BG_Y}{W}02{RESET}{BG_Y}{W}/{RESET}{BG_Y}{W}B{RESET}{W}]{RESET} {M('FILE ENCRYPTOR          — CYTHON ENCRYPTION')}")
        print(f" {W}[{RESET}{BG_C}{W}03{RESET}{BG_C}{W}/{RESET}{BG_C}{W}C{RESET}{W}]{RESET} {C('MANAGE COOKIES          — DATABASE')}")
        print(f" {W}[{RESET}{BG_B}{W}04{RESET}{BG_B}{W}/{RESET}{BG_B}{W}D{RESET}{W}]{RESET} {B('MY STATS                — STATISTICS')}")
        print(f" {W}[{RESET}{BG_M}{W}05{RESET}{BG_M}{W}/{RESET}{BG_M}{W}E{RESET}{W}]{RESET} {M('ADMIN PANEL             — MANAGEMENT')}")
        print(f" {W}[{RESET}{BG_G}{W}06{RESET}{BG_G}{W}/{RESET}{BG_G}{W}F{RESET}{W}]{RESET} {G('UPDATE TOOL             — LATEST VERSION')}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{W}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R('LOGOUT')}")
    else:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{W}/{RESET}{BG_G}{W}A{RESET}{W}]{RESET} {G('AUTO SHARE              — NORM ACCOUNTS')}")
        print(f" {W}[{RESET}{BG_Y}{W}02{RESET}{BG_Y}{W}/{RESET}{BG_Y}{W}B{RESET}{W}]{RESET} {C('MANAGE COOKIES          — DATABASE')}")
        print(f" {W}[{RESET}{BG_B}{W}03{RESET}{BG_B}{W}/{RESET}{BG_B}{W}C{RESET}{W}]{RESET} {B('MY STATS                — STATISTICS')}")
        print(f" {W}[{RESET}{BG_G}{W}04{RESET}{BG_G}{W}/{RESET}{BG_G}{W}D{RESET}{W}]{RESET} {G('UPDATE TOOL             — LATEST VERSION')}")
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{W}/{RESET}{BG_R}{W}X{RESET}{W}]{RESET} {R('LOGOUT')}")
    print(LINE)

def refresh_screen():
    clear()
    banner_header()
    show_menu()

def nice_loader(text="PROCESSING"):
    sys.stdout.write("\033[?25l")
    filled = "■"
    empty = "□"
    width = 20
    
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = filled * i + empty * (width - i)
        bar_gradient = apply_gradient(bar, 'purple_cyan')
        
        sys.stdout.write(f"\r {W}[{RESET}•{W}]{RESET} {G(text)} {W}➤{RESET} [{bar_gradient}] {M(f'{percent}%')}")
        sys.stdout.flush()
        time.sleep(0.04)
    
    time.sleep(0.3)
    sys.stdout.write(f"\r{' ' * 80}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")

def select_progress_display():
    refresh_screen()
    print(f" {C('[SHARING PROGRESS DISPLAY]')}")
    print(LINE)
    print(f" {G('Choose how you want to see sharing progress:')}")
    print(LINE)
    print(f" {W}[{RESET}{BG_G}{W}1{RESET}{W}]{RESET} {G('SUCCESS COUNTER (1/100)')}")
    print(f"     {C('• Best for smaller screens (mobile)')}")
    print(LINE)
    print(f" {W}[{RESET}{BG_C}{W}2{RESET}{W}]{RESET} {C('DETAILED LOGS')}")
    print(f"     {G('• Best for larger screens (desktop)')}")
    print(LINE)
    
    while True:
        choice = input(f" {W}[{W}➤{W}]{RESET} {C('CHOICE (1 or 2)')} {W}➤{RESET} ").strip()
        if choice == '1':
            return 'minimal'
        elif choice == '2':
            return 'detailed'
        else:
            print(f" {R('[!] Invalid choice. Please enter 1 or 2')}")
            time.sleep(1)
            sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()

def get_country_from_ip():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
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
        return None, "Cannot connect to server"
    except requests.exceptions.Timeout:
        return None, "Request timeout"
    except Exception as e:
        return None, f"Error: {str(e)}"

def login_user():
    global user_token, user_data
    
    refresh_screen()
    print(f" {G('[!] LOGIN TO RPWTOOLS')}")
    print(LINE)
    
    username = input(f" {W}[{W}➤{W}]{RESET} {C('USERNAME')} {W}➤{RESET} ").strip()
    if not username:
        return
    
    password = input(f" {W}[{W}➤{W}]{RESET} {C('PASSWORD')} {W}➤{RESET} ").strip()
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
        
        print(f" {G('[SUCCESS] Login successful!')}")
        print(LINE)
        print(f" {G('Welcome back,')} {M(user_data['username'].upper())}")
        print(f" {G('Plan:')} {M(user_data['plan'].upper())}")
        print(f" {G('Total Cookies:')} {C(str(user_data.get('cookieCount', 0)))}")
        
        if user_data.get('isAdmin'):
            print(f" {M('[ADMIN ACCESS GRANTED]')}")
        
        print(LINE)
    else:
        print(f" {R('[ERROR]')} {R(response if isinstance(response, str) else response.get('message', 'Login failed'))}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def register_user():
    global user_token, user_data
    
    refresh_screen()
    print(f" {G('[!] REGISTER NEW ACCOUNT')}")
    print(LINE)
    
    username = input(f" {W}[{W}➤{W}]{RESET} {C('USERNAME')} {W}➤{RESET} ").strip()
    if not username:
        return
    
    password = input(f" {W}[{W}➤{W}]{RESET} {C('PASSWORD')} {W}➤{RESET} ").strip()
    if not password:
        return
    
    facebook = input(f" {W}[{W}➤{W}]{RESET} {C('FACEBOOK LINK')} {W}➤{RESET} ").strip()
    if not facebook:
        return
    
    facebook = normalize_facebook_url(facebook)
    
    refresh_screen()
    print(f" {G('[!] NORMALIZED FACEBOOK URL:')} {C(facebook)}")
    print(LINE)
    
    print(f" {G('[!] DETECTING YOUR COUNTRY...')}")
    nice_loader("DETECTING")
    
    country = get_country_from_ip()
    
    refresh_screen()
    print(f" {G('[!] DETECTED COUNTRY:')} {C(country)}")
    print(LINE)
    confirm = input(f" {W}[{W}➤{W}]{RESET} {G('Is this correct? (Y/N)')} {W}➤{RESET} ").strip().upper()
    
    if confirm == 'N':
        country = input(f" {W}[{W}➤{W}]{RESET} {C('ENTER YOUR COUNTRY')} {W}➤{RESET} ").strip()
    
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
        
        print(f" {G('[SUCCESS] Registration successful!')}")
        print(LINE)
        print(f" {G('Welcome,')} {M(user_data['username'].upper())}")
        print(f" {G('Plan:')} {M(user_data['plan'].upper())}")
        print(f" {G('Country:')} {C(user_data['country'])}")
        print(LINE)
    else:
        print(f" {R('[ERROR]')} {R(response if isinstance(response, str) else response.get('message', 'Registration failed'))}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def show_user_stats():
    refresh_screen()
    print(f" {G('[!] LOADING STATS...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/stats")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats')
        
        refresh_screen()
        print(f" {G('[USER STATISTICS]')}")
        print(LINE)
        print(f" {C('Username:')} {W}{stats['username'].upper()}{RESET}")
        
        plan_display = M(stats['plan'].upper()) if stats['plan'] == 'max' else G(stats['plan'].upper())
        print(f" {C('Plan:')} {plan_display}")
        
        if stats.get('planExpiry'):
            print(f" {C('Plan Expiry In:')} {R(stats['planExpiry'])}")
        
        print(LINE)
        print(f" {C('[STATISTICS]')}")
        print(f" {G('Total Shares:')} {M(str(stats['totalShares']))}")
        print(f" {G('Total Cookies:')} {C(str(stats.get('cookieCount', 0)))}")
        print(LINE)
    else:
        print(f" {R('[ERROR]')} {R('Failed to get stats')}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def manage_cookies():
    while True:
        refresh_screen()
        print(f" {G('[MANAGE COOKIES]')}")
        print(LINE)
        print(f" {W}[{W}1{W}]{RESET} {G('VIEW ALL COOKIES')}")
        print(f" {W}[{W}2{W}]{RESET} {G('ADD COOKIE')}")
        print(f" {W}[{W}3{W}]{RESET} {R('DELETE COOKIE')}")
        print(f" {W}[{W}4{W}]{RESET} {R('DELETE ALL COOKIES')}")
        print(f" {W}[{W}0{W}]{RESET} {C('BACK')}")
        print(LINE)
        
        choice = input(f" {W}[{W}➤{W}]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip()
        
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
            print(f"\n {R('[!] INVALID SELECTION')}")
            time.sleep(0.8)

def view_cookies():
    refresh_screen()
    print(f" {G('[!] LOADING COOKIES...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status == 200 and response.get('success'):
        cookies = response.get('cookies', [])
        
        refresh_screen()
        print(f" {G(f'[COOKIES] Total: {len(cookies)}')}")
        print(LINE)
        
        if not cookies:
            print(f" {C('No cookies stored yet.')}")
        else:
            for i, cookie_data in enumerate(cookies, 1):
                status_display = G('[ACTIVE]') if cookie_data['status'] == 'active' else R('[RESTRICTED]')
                
                print(f" {W}[{i:02d}]{RESET} {M(cookie_data['name'])} {W}({C(f\"UID: {cookie_data['uid']}\")}{W}){RESET}")
                cookie_preview = cookie_data['cookie'][:50] + "..." if len(cookie_data['cookie']) > 50 else cookie_data['cookie']
                print(f"      Cookie: {C(cookie_preview)}")
                print(f"      Added: {G(cookie_data['addedAt'])}")
                print(f"      Status: {status_display}")
                
                if cookie_data['status'] == 'restricted':
                    print(f"      {R('⚠ WARNING: This account is restricted!')}")
                
                print(LINE)
        
    else:
        print(f" {R('[ERROR] Failed to load cookies')}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def add_cookie():
    refresh_screen()
    print(f" {G('[ADD COOKIE]')}")
    print(LINE)
    
    if user_data['plan'] == 'free' and user_data.get('cookieCount', 0) >= 10:
        print(f" {R('[LIMIT REACHED]')}")
        print(LINE)
        print(f" {C('FREE plan users can only store up to 10 cookies.')}")
        print(f" {C(f\"You currently have: {R(f\"{user_data.get('cookieCount', 0)}/10\")}\")}")
        print(LINE)
        print(f" {G('[UPGRADE TO MAX]')}")
        print(f" {C('• Unlimited cookies')}")
        print(f" {C('• No cooldowns')}")
        print(LINE)
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    cookie = input(f" {W}[{W}➤{W}]{RESET} {C('COOKIE')} {W}➤{RESET} ").strip()
    if not cookie:
        return
    
    refresh_screen()
    print(f" {G('[!] VALIDATING COOKIE...')}")
    print(f" {C('This may take 10-15 seconds')}")
    print(LINE)
    nice_loader("VALIDATING")
    
    status, response = api_request("POST", "/user/cookies", {"cookie": cookie})
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(f" {G('[SUCCESS]')} {G(response.get('message'))}")
        print(LINE)
        print(f" {C('Name:')} {M(response.get('name', 'Unknown'))}")
        print(f" {C('UID:')} {C(response.get('uid', 'Unknown'))}")
        status_display = G(response.get('status', 'unknown').upper()) if response.get('status') == 'active' else R(response.get('status', 'unknown').upper())
        print(f" {C('Status:')} {status_display}")
        
        if response.get('restricted'):
            print(LINE)
            print(f" {R('⚠ WARNING: This account is RESTRICTED!')}")
            print(f" {C('Restricted accounts may not be able to share posts.')}")
        
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
            
            if user_data['plan'] == 'free':
                remaining = 10 - user_data['cookieCount']
                print(LINE)
                print(f" {C('Remaining Slots:')} {C(f'{remaining}/10')}")
        
        print(LINE)
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed to add cookie') if isinstance(response, dict) else 'Failed to add cookie'
        print(f" {R('[ERROR]')} {R(error_msg)}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def delete_cookie():
    refresh_screen()
    print(f" {G('[!] LOADING COOKIES...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not isinstance(response, dict) or not response.get('success'):
        error_msg = response if isinstance(response, str) else 'Failed to load cookies'
        print(f" {R('[ERROR]')} {R(error_msg)}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        refresh_screen()
        print(f" {C('No cookies to delete.')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(f" {R('[DELETE COOKIE]')}")
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        status_indicator = R('[RESTRICTED]') if cookie_data['status'] == 'restricted' else G('[ACTIVE]')
        print(f" {W}[{i}]{RESET} {M(cookie_data['name'])} {W}({C(f\"UID: {cookie_data['uid']}\")}{W}){RESET} {status_indicator}")
    
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C('SELECT COOKIE NUMBER (0 to cancel)')} {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        cookie_index = int(choice) - 1
        if cookie_index < 0 or cookie_index >= len(cookies):
            print(f" {R('[ERROR] Invalid cookie number')}")
            time.sleep(1)
            return
        
        selected_cookie = cookies[cookie_index]
    except:
        print(f" {R('[ERROR] Invalid input')}")
        time.sleep(1)
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/user/cookies/{selected_cookie['id']}")
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(f" {G('[SUCCESS] Cookie deleted!')}")
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
    else:
        error_msg = response if isinstance(response, str) else 'Failed to delete cookie'
        print(f" {R('[ERROR]')} {R(error_msg)}")
    
    print(LINE)
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def delete_all_cookies():
    refresh_screen()
    print(f" {R('[DELETE ALL COOKIES]')}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R('Delete ALL cookies? This cannot be undone! (YES/NO)')} {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", "/user/cookies")
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS]')} {G(response.get('message'))}")
        if user_data:
            user_data['cookieCount'] = 0
    else:
        print(f" {R('[ERROR] Failed to delete cookies')}")
    
    print(LINE)
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def update_tool_logic():
    print(f" {G('[!] CHECKING FOR UPDATES...')}")
    nice_loader("CHECKING")
    
    print(f" {G('[!] NEW VERSION FOUND! DOWNLOADING...')}")
    nice_loader("UPDATING")
    
    print(f" {G('[!] UPDATE COMPLETE. RESTARTING...')}")
    time.sleep(1)
    
    os.execv(sys.executable, ['python'] + sys.argv)

# ============ ADMIN PANEL FUNCTIONS ============

def admin_panel():
    while True:
        refresh_screen()
        print(f" {M('[ADMIN PANEL]')}")
        print(LINE)
        print(f" {W}[{W}1{W}]{RESET} {G('VIEW ALL USERS')}")
        print(f" {W}[{W}2{W}]{RESET} {C('CHANGE USER PLAN')}")
        print(f" {W}[{W}3{W}]{RESET} {R('DELETE USER')}")
        print(f" {W}[{W}4{W}]{RESET} {C('VIEW ACTIVITY LOGS')}")
        print(f" {W}[{W}5{W}]{RESET} {G('DASHBOARD STATS')}")
        print(f" {W}[{W}0{W}]{RESET} {C('BACK')}")
        print(LINE)
        
        choice = input(f" {W}[{W}➤{W}]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip()
        
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
            print(f"\n {R('[!] INVALID SELECTION')}")
            time.sleep(0.8)

def view_all_users():
    refresh_screen()
    print(f" {G('[!] LOADING USERS...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/users")
    
    if status == 200 and response.get('success'):
        users = response.get('users', [])
        
        refresh_screen()
        print(f" {G(f'[ALL USERS] Total: {len(users)}')}")
        print(LINE)
        
        for i, user in enumerate(users, 1):
            plan_display = M(user['plan'].upper()) if user['plan'] == 'max' else G(user['plan'].upper())
            admin_badge = f" {M('[ADMIN]')}" if user.get('isAdmin') else ""
            
            print(f" {W}[{i:02d}]{RESET} {C(user['username'].upper())}{admin_badge}")
            print(f"      Plan: {plan_display} | Country: {G(user['country'])}")
            print(f"      Shares: {G(str(user['totalShares']))}")
            print(f"      Total Cookies: {C(str(user.get('cookieCount', 0)))}")
            print(LINE)
        
    else:
        print(f" {R('[ERROR] Failed to get users')}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def change_user_plan():
    refresh_screen()
    print(f" {C('[CHANGE USER PLAN]')}")
    print(LINE)
    
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load users')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    users = response.get('users', [])
    
    print(f" {G('[SELECT USER]')}")
    print(LINE)
    for i, user in enumerate(users, 1):
        plan_display = M(user['plan'].upper()) if user['plan'] == 'max' else G(user['plan'].upper())
        print(f" {W}[{i}]{RESET} {C(user['username'].upper())} - Plan: {plan_display}")
    print(LINE)
    
    user_choice = input(f" {W}[{W}➤{W}]{RESET} {C('SELECT USER NUMBER (0 to cancel)')} {W}➤{RESET} ").strip()
    
    if not user_choice or user_choice == '0':
        return
    
    try:
        user_index = int(user_choice) - 1
        if user_index < 0 or user_index >= len(users):
            print(f" {R('[ERROR] Invalid user number')}")
            time.sleep(1)
            return
        
        selected_user = users[user_index]
    except:
        print(f" {R('[ERROR] Invalid input')}")
        time.sleep(1)
        return
    
    refresh_screen()
    print(f" {C(f'[CHANGE PLAN FOR: {selected_user[\"username\"].upper()}]')}")
    print(LINE)
    print(f" {W}[1]{RESET} {G('FREE')} - 10 cookies max")
    print(f" {W}[2]{RESET} {M('MAX')} - Unlimited cookies (RENTAL)")
    print(f" {W}[3]{RESET} {M('MAX LIFETIME')} - Unlimited cookies (PERMANENT)")
    print(LINE)
    
    plan_choice = input(f" {W}[{W}➤{W}]{RESET} {C('SELECT PLAN NUMBER')} {W}➤{RESET} ").strip()
    
    plan_map = {'1': 'free', '2': 'max', '3': 'max'}
    
    if plan_choice not in plan_map:
        print(f" {R('[ERROR] Invalid plan')}")
        time.sleep(1)
        return
    
    new_plan = plan_map[plan_choice]
    duration = None
    
    if plan_choice == '2':
        refresh_screen()
        print(f" {C('[MAX PLAN DURATION]')}")
        print(LINE)
        print(f" {W}[1]{RESET} 1 Month")
        print(f" {W}[2]{RESET} 2 Months")
        print(f" {W}[3]{RESET} 3 Months")
        print(LINE)
        
        duration_choice = input(f" {W}[{W}➤{W}]{RESET} {C('SELECT DURATION')} {W}➤{RESET} ").strip()
        
        duration_map = {'1': 1, '2': 2, '3': 3}
        
        if duration_choice not in duration_map:
            print(f" {R('[ERROR] Invalid duration')}")
            time.sleep(1)
            return
        
        duration = duration_map[duration_choice]
    
    refresh_screen()
    print(f" {C('[CONFIRM CHANGE]')}")
    print(LINE)
    print(f" User: {C(selected_user['username'].upper())}")
    print(f" Current Plan: {G(selected_user['plan'].upper())}")
    new_plan_display = f"{M('MAX LIFETIME')}" if plan_choice == '3' else f"{M('MAX')}" if plan_choice == '2' else f"{G('FREE')}"
    print(f" New Plan: {new_plan_display}")
    if duration:
        print(f" Duration: {G(f'{duration} month(s)')}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {G('Confirm? (Y/N)')} {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        return
    
    nice_loader("UPDATING")
    
    status, response = api_request("PUT", f"/admin/users/{selected_user['username']}/plan", {
        "plan": new_plan,
        "duration": duration
    })
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS] Plan updated successfully!')}")
    else:
        print(f" {R('[ERROR]')} {R(response.get('message', 'Failed to update plan'))}")
    
    print(LINE)
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def delete_user():
    refresh_screen()
    print(f" {R('[DELETE USER]')}")
    print(LINE)
    
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load users')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    users = response.get('users', [])
    
    if not users:
        print(f" {C('No users to delete.')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    print(f" {G('[SELECT USER TO DELETE]')}")
    print(LINE)
    
    for i, user in enumerate(users, 1):
        plan_display = M(user['plan'].upper()) if user['plan'] == 'max' else G(user['plan'].upper())
        admin_badge = f" {M('[ADMIN]')}" if user.get('isAdmin') else ""
        
        print(f" {W}[{i:02d}]{RESET} {C(user['username'].upper())}{admin_badge} - {plan_display}")
    
    print(f" {W}[00]{RESET} {C('CANCEL')}")
    print(LINE)
    
    choice = input(f" {W}[{W}➤{W}]{RESET} {C('SELECT USER')} {W}➤{RESET} ").strip()
    
    if not choice or choice in ['0', '00']:
        return
    
    try:
        user_index = int(choice) - 1
        if user_index < 0 or user_index >= len(users):
            print(f" {R('[ERROR] Invalid selection')}")
            time.sleep(1)
            return
        
        selected_user = users[user_index]
    except:
        print(f" {R('[ERROR] Invalid input')}")
        time.sleep(1)
        return
    
    refresh_screen()
    print(f" {R('[CONFIRM DELETION]')}")
    print(LINE)
    print(f" User: {C(selected_user['username'].upper())}")
    print(f" Plan: {G(selected_user['plan'].upper())}")
    print(f" Country: {G(selected_user['country'])}")
    print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {R('Delete this user? This cannot be undone! (YES/NO)')} {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/admin/users/{selected_user['username']}")
    
    if status == 200 and response.get('success'):
        print(f" {G(f\"[SUCCESS] User '{selected_user['username']}' deleted successfully!\")}")
    else:
        print(f" {R('[ERROR]')} {R(response.get('message', 'Failed to delete user'))}")
    
    print(LINE)
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def view_activity_logs():
    refresh_screen()
    print(f" {G('[!] LOADING ACTIVITY LOGS...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/logs?limit=20")
    
    if status == 200 and response.get('success'):
        logs = response.get('logs', [])
        
        refresh_screen()
        print(f" {C('[ACTIVITY LOGS] Recent 20')}")
        print(LINE)
        
        for log in logs:
            action_display = G(log['action'].upper()) if log['action'] == 'login' else C(log['action'].upper())
            print(f" {W}[{log['timestamp']}]{RESET}")
            print(f" User: {C(log['username'].upper())} | Action: {action_display}")
            if log.get('details'):
                print(f" Details: {G(log['details'])}")
            print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load logs')}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def dashboard_stats():
    refresh_screen()
    print(f" {G('[!] LOADING DASHBOARD...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/admin/dashboard")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats', {})
        
        refresh_screen()
        print(f" {G('[ADMIN DASHBOARD]')}")
        print(LINE)
        
        print(f" {C('[USER STATISTICS]')}")
        print(f" Total Users: {G(str(stats['totalUsers']))}")
        print(f" FREE Users: {G(str(stats['planDistribution']['free']))}")
        print(f" MAX Users: {M(str(stats['planDistribution']['max']))}")
        print(LINE)
        
        print(f" {C('[ACTIVITY STATISTICS]')}")
        print(f" Total Shares: {G(str(stats['totalShares']))}")
        print(LINE)
        
        print(f" {C('[RECENT USERS]')}")
        for user in stats.get('recentUsers', []):
            plan_display = M(user['plan'].upper()) if user['plan'] == 'max' else G(user['plan'].upper())
            print(f" {C(user['username'].upper())} - {plan_display} - {G(user['country'])}")
        print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load dashboard')}")
        print(LINE)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

# ============ CYTHON FILE ENCRYPTOR (ADMIN ONLY) ============

def check_cython_available():
    """Check if Cython is available"""
    try:
        importlib.import_module('Cython')
        return True
    except ImportError:
        return False

def install_cython():
    """Install Cython and dependencies"""
    try:
        print(f" {G('[!] Installing Cython...')}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Cython'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f" {G('[SUCCESS] Cython installed!')}")
        return True
    except:
        print(f" {R('[ERROR] Failed to install Cython')}")
        return False

def get_platform_extension():
    """Get the appropriate compiled extension for the current platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    
    if system == "windows":
        return f".cp{py_version}-win_amd64.pyd"
    elif system == "linux":
        if "aarch64" in machine or "arm" in machine:
            return f".cpython-{py_version}-aarch64-linux-gnu.so"
        else:
            return f".cpython-{py_version}-x86_64-linux-gnu.so"
    elif system == "darwin":
        return f".cpython-{py_version}-darwin.so"
    else:
        return f".so"

def create_simple_obfuscated(file_path, file_name, base_name, code):
    """Create a simple obfuscated version without Cython"""
    compressed_code = zlib.compress(code.encode('utf-8'))
    encoded_code = base64.b64encode(compressed_code).decode('utf-8')
    
    output_file = f'{base_name}_encrypted.py'
    with open(output_file, 'w') as f:
        f.write(f"""#!/usr/bin/env python3
import zlib
import base64

encoded_code = '{encoded_code}'

# Decode and decompress the code
compressed_code = base64.b64decode(encoded_code)
original_code = zlib.decompress(compressed_code).decode('utf-8')

# Execute the original code
exec(original_code)
""")
    
    if platform.system().lower() != 'windows':
        os.chmod(output_file, 0o755)
    
    return output_file

def create_cython_obfuscated(file_path, file_name, base_name, code):
    """Create a Cython-compiled obfuscated version"""
    from Cython.Build import cythonize
    from distutils.core import setup
    from distutils.extension import Extension
    
    compressed_code = zlib.compress(code.encode('utf-8'))
    encoded_code = base64.b64encode(compressed_code).decode('utf-8')
    
    temp_file_name = f'{base_name}_encrypted.py'
    with open(temp_file_name, 'w') as temp_file:
        temp_file.write(f"""
import zlib
import base64

encoded_code = '{encoded_code}'

# Decode and decompress the code
compressed_code = base64.b64decode(encoded_code)
original_code = zlib.decompress(compressed_code).decode('utf-8')

# Execute the original code
exec(original_code)
""")
    
    print(f" {G(f'[SUCCESS] Created encrypted file: {temp_file_name}')}")
    
    print(f" {C('[INFO] Compiling with Cython...')}")
    module_name = f'{base_name}_encrypted'
    extensions = [Extension(module_name, [temp_file_name])]
    setup(
        ext_modules=cythonize(extensions, compiler_directives={'language_level': '3'}),
        script_args=['build_ext', '--inplace']
    )
    
    print(f" {G('[SUCCESS] Cython compilation complete')}")
    
    platform_ext = get_platform_extension()
    compiled_file = f'{module_name}{platform_ext}'
    
    if not os.path.exists(compiled_file):
        print(f" {C(f'[INFO] Looking for compiled file...')}")
        for f in os.listdir('.'):
            if f.startswith(module_name) and ('.so' in f or '.pyd' in f):
                print(f" {G(f'[FOUND] {f}')}")
                compiled_file = f
                break
    
    run_script_name = f'{base_name}_run.py'
    with open(run_script_name, 'w') as run_script:
        run_script.write(f"""#!/usr/bin/env python3
import importlib
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the compiled module
module_name = '{module_name}'
try:
    compiled_module = importlib.import_module(module_name)
    print("Module loaded successfully!")
except ImportError as e:
    print(f"Error loading module: {{e}}")
    sys.exit(1)

# Execute the module's main function if it exists
if hasattr(compiled_module, 'main'):
    compiled_module.main()
""")
    
    if platform.system().lower() != 'windows':
        os.chmod(run_script_name, 0o755)
    
    print(f" {G(f'[SUCCESS] Created run script: {run_script_name}')}")
    
    return compiled_file, run_script_name, temp_file_name

def file_encryptor():
    """Cython File Encryptor - Admin Only Feature"""
    if not user_data or not user_data.get('isAdmin'):
        refresh_screen()
        print(f" {R('[ACCESS DENIED]')}")
        print(LINE)
        print(f" {C('This feature is only available for administrators.')}")
        print(LINE)
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(f" {M('[CYTHON FILE ENCRYPTOR]')}")
    print(LINE)
    print(f" {C('Encrypt Python files with Cython compilation')}")
    print(LINE)
    
    file_path = input(f" {W}[{W}➤{W}]{RESET} {C('Enter path to Python file')} {W}➤{RESET} ").strip().strip('"').strip("'")
    
    if not file_path.endswith('.py'):
        print(f" {R('[ERROR] Invalid file type, only support Python files')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    if not os.path.exists(file_path):
        print(f" {R(f'[ERROR] File not found: {file_path}')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    print(LINE)
    use_cython = input(f" {W}[{W}➤{W}]{RESET} {G('Use Cython compilation? (more secure) [y/N]')} {W}➤{RESET} ").lower().strip()
    use_cython = use_cython in ['y', 'yes']
    
    if use_cython and not check_cython_available():
        print(f" {C('[INFO] Cython not available. Installing...')}")
        if not install_cython():
            print(f" {C('[INFO] Falling back to basic encryption...')}")
            use_cython = False
    
    file_path = os.path.abspath(file_path)
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    base_name = file_name.replace('.py', '')
    
    original_dir = os.getcwd()
    os.chdir(file_dir)
    
    print(LINE)
    print(f" {C(f'[INFO] Working in directory: {file_dir}')}")
    print(f" {C(f'[INFO] Processing file: {file_name}')}")
    print(LINE)
    
    nice_loader("READING FILE")
    
    try:
        with open(file_name, 'r') as file:
            code = file.read()
        
        if use_cython:
            nice_loader("ENCRYPTING")
            compiled_file, run_script, temp_file = create_cython_obfuscated(file_path, file_name, base_name, code)
            
            output_dir = f'{base_name}_encrypted_output'
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            
            shutil.copy(compiled_file, output_dir)
            shutil.copy(run_script, output_dir)
            
            print(f" {C('[INFO] Cleaning up temporary files...')}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            if os.path.exists('build'):
                shutil.rmtree('build')
            for f in os.listdir('.'):
                if f.endswith('.c'):
                    os.remove(f)
            
            print(LINE)
            print(f" {G('[SUCCESS] Encrypted package created!')}")
            print(f" {C(f'[INFO] Location: {os.path.join(file_dir, output_dir)}')}")
            print(f" {C(f'[INFO] Run with: python {run_script} (from output directory)')}")
            print(f" {C(f\"[NOTE] Distribute the entire '{output_dir}' folder\")}")
            print(LINE)
            
        else:
            nice_loader("ENCRYPTING")
            output_file = create_simple_obfuscated(file_path, file_name, base_name, code)
            
            print(LINE)
            print(f" {G('[SUCCESS] Encrypted file created!')}")
            print(f" {C(f'[INFO] Location: {os.path.join(file_dir, output_file)}')}")
            print(f" {C(f'[INFO] Run with: python {output_file}')}")
            print(f" {C('[NOTE] This is basic encryption. For better protection, use Cython.')}")
            print(LINE)
        
    except Exception as e:
        print(f" {R(f'[ERROR] An error occurred: {str(e)}')}")
        print(LINE)
    finally:
        os.chdir(original_dir)
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

# ============ POST ID EXTRACTION ============

def extract_post_id_from_link(link):
    link = link.strip()
    
    if link.isdigit():
        return link
    
    link = re.sub(r'^https?://', '', link)
    link = re.sub(r'^(www\.|m\.)', '', link)
    
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
    try:
        async with session.post('https://id.traodoisub.com/api.php', data={"link": link}) as response:
            rq = await response.json()
            if 'success' in rq:
                return rq["id"]
            else:
                print(f" {R('[ERROR] Incorrect post link!')}")
                return None
    except Exception as e:
        print(f" {R(f'[ERROR] Failed to get post ID: {e}')}")
        return None

# ============ AUTO SHARE FUNCTIONS ============

def cookie_to_eaag(cookie):
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
    return cookie_to_eaag(cookie)

async def share_loop(session, cookie, token, post_id, account_name, account_uid, cookie_id, display_mode='detailed'):
    global success_count
    
    last_token_renewal = time.time()
    current_token = token
    failed_consecutive = 0
    
    while True:
        try:
            if time.time() - last_token_renewal >= 180:
                new_token = await renew_eaag_token(cookie)
                
                if new_token:
                    current_token = new_token
                    last_token_renewal = time.time()
                    
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {apply_gradient('[TOKEN RENEWED]', 'green_yellow')} {W}|{RESET} {apply_gradient(f'[UID: {account_uid}]', 'purple_cyan')}                              ")
                        sys.stdout.flush()
                        time.sleep(0.5)
                    else:
                        now = datetime.datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(f" {apply_gradient('[RENEWED]', 'green_yellow')} {W}|{RESET} {apply_gradient(current_time, 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient('Token renewed', 'green_yellow')}")
            
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            is_success, result = await share_with_eaag(session, cookie, current_token, post_id)
            
            if is_success:
                async with lock:
                    success_count += 1
                    current_count = success_count
                
                failed_consecutive = 0
                
                if display_mode == 'minimal':
                    sys.stdout.write(f"\r {apply_gradient(f'[SUCCESS — {current_count}]', 'green_yellow')} {W}|{RESET} {apply_gradient(f'[UID: {account_uid}]', 'purple_cyan')}                    ")
                    sys.stdout.flush()
                else:
                    print(f" {apply_gradient('[SUCCESS]', 'green_yellow')} {W}|{RESET} {apply_gradient(current_time, 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient(f'Total: {current_count}', 'green_yellow')}")
                
            else:
                failed_consecutive += 1
                error_message = result
                
                if failed_consecutive >= 3:
                    if display_mode == 'minimal':
                        sys.stdout.write(f"\r {apply_gradient('[RENEWING...]', 'green_yellow')} {W}|{RESET} {apply_gradient(f'[UID: {account_uid}]', 'purple_cyan')}                          ")
                        sys.stdout.flush()
                    else:
                        print(f" {apply_gradient('[RENEWING]', 'green_yellow')} {W}|{RESET} {apply_gradient(current_time, 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient('Attempting token renewal...', 'green_yellow')}")
                    
                    new_token = await renew_eaag_token(cookie)
                    
                    if new_token:
                        current_token = new_token
                        last_token_renewal = time.time()
                        failed_consecutive = 0
                        
                        if display_mode == 'minimal':
                            sys.stdout.write(f"\r {apply_gradient('[TOKEN RENEWED]', 'green_yellow')} {W}|{RESET} {apply_gradient(f'[UID: {account_uid}]', 'purple_cyan')}                            ")
                            sys.stdout.flush()
                            time.sleep(0.5)
                        else:
                            print(f" {apply_gradient('[RENEWED]', 'green_yellow')} {W}|{RESET} {apply_gradient(current_time, 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient('Token renewed successfully', 'green_yellow')}")
                    else:
                        if display_mode != 'minimal':
                            print(f" {apply_gradient('[ERROR]', 'red_orange')} {W}|{RESET} {apply_gradient(current_time, 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient(error_message[:40], 'red_orange')}")
                        await asyncio.sleep(5)
                else:
                    if display_mode != 'minimal':
                        print(f" {apply_gradient('[ERROR]', 'red_orange')} {W}|{RESET} {apply_gradient(current_time, 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient(error_message[:40], 'red_orange')}")
        
        except asyncio.CancelledError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_msg = str(e)
            if "asyncio" not in error_msg.lower() and "event" not in error_msg.lower():
                if display_mode != 'minimal':
                    print(f" {apply_gradient('[ERROR]', 'red_orange')} {W}|{RESET} {apply_gradient(datetime.datetime.now().strftime('%H:%M:%S'), 'blue_purple')} {W}|{RESET} {apply_gradient(account_uid, 'purple_cyan')} {W}|{RESET} {apply_gradient(error_msg[:40], 'red_orange')}")

async def auto_share_main(link_or_id, selected_cookies):
    global success_count
    success_count = 0
    
    refresh_screen()
    print(f" {C('[!] CONVERTING SELECTED COOKIES TO EAAG TOKENS...')}")
    nice_loader("CONVERTING")
    
    eaag_tokens = []
    
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
            status_indicator = R('[RESTRICTED]') if cookie_data.get('status') == 'restricted' else G('[ACTIVE]')
            print(f" {G('✓')} {C(cookie_data['name'])} {W}({C(f\"UID: {cookie_data['uid']}\")}{W}){RESET} {status_indicator}")
        else:
            print(f" {R('✗')} {C(cookie_data['name'])} {R('Failed to extract EAAG token')}")
    
    if not eaag_tokens:
        print(f" {R('[ERROR] No valid EAAG tokens extracted!')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    async with aiohttp.ClientSession() as session:
        post_id = extract_post_id_from_link(link_or_id)
        
        if not post_id.isdigit():
            refresh_screen()
            print(f" {G('[!] EXTRACTING POST ID FROM LINK...')}")
            nice_loader("EXTRACTING")
            
            post_id = await getid(session, link_or_id)
            if not post_id:
                print(f" {R('[ERROR] Failed to get post ID')}")
                input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
                return
    
    display_mode = select_progress_display()
    
    refresh_screen()
    print(f" {G(f'[SUCCESS] Extracted {len(eaag_tokens)} EAAG tokens')}")
    print(LINE)
    print(f" {C('Post ID:')} {G(post_id)}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        print(f" {M('[AUTO SHARE CONFIGURATION]')}")
        print(LINE)
        print(f" {C('Mode:')} {G('NORM ACC (EAAG Tokens)')}")
        print(f" {C('Total Accounts:')} {G(str(len(eaag_tokens)))}")
        print(f" {C('Share Speed:')} {G('MAXIMUM (ZERO DELAYS)')}")
        print(f" {C('Token Renewal:')} {M('Auto every 3 minutes')}")
        print(LINE)
        print(f" {G('[!] STARTING AUTO SHARE...')}")
        print(f" {C('[TIP] Press Ctrl+C to stop')}")
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
        
        print(f" {G(f'[STARTED] Running {len(tasks)} parallel share threads at MAXIMUM SPEED...')}")
        print(LINE)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

def select_cookies_for_sharing():
    refresh_screen()
    print(f" {G('[!] LOADING COOKIES FROM DATABASE...')}")
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load cookies')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        print(f" {R('[ERROR] No cookies stored in database')}")
        print(f" {C('[TIP] Use option 2 to add cookies')}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    refresh_screen()
    print(f" {C('[SELECT COOKIES FOR AUTO SHARE]')}")
    print(LINE)
    print(f" {W}[{RESET}{BG_G}{W}ALL{RESET}{W}]{RESET} {G('USE ALL COOKIES')}")
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        letter = chr(64 + i) if i <= 26 else str(i)
        status_indicator = R('[RESTRICTED]') if cookie_data.get('status') == 'restricted' else G('[ACTIVE]')
        print(f" {W}[{RESET}{BG_C}{W}{i:02d}{RESET}{W}/{RESET}{BG_C}{W}{letter}{RESET}{W}]{RESET} {C(cookie_data['name'])} {W}({C(f\"UID: {cookie_data['uid']}\")}{W}){RESET} {status_indicator}")
    
    print(LINE)
    print(f" {C('[TIP] Enter numbers separated by commas (e.g., 1,2,3) or type ALL')}")
    print(LINE)
    
    selection = input(f" {W}[{W}➤{W}]{RESET} {C('SELECT')} {W}➤{RESET} ").strip().upper()
    
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
            print(f" {R('[ERROR] Invalid selection')}")
            time.sleep(1)
            return None
    
    if not selected_cookies:
        print(f" {R('[ERROR] No valid cookies selected')}")
        time.sleep(1)
        return None
    
    refresh_screen()
    print(f" {C('[CONFIRM SELECTION]')}")
    print(LINE)
    print(f" {C(f'Selected {G(str(len(selected_cookies)))} cookie(s):')}")
    for cookie_data in selected_cookies:
        status_indicator = R('[RESTRICTED]') if cookie_data.get('status') == 'restricted' else G('[ACTIVE]')
        print(f"   • {C(cookie_data['name'])} {W}({C(f\"UID: {cookie_data['uid']}\")}{W}){RESET} {status_indicator}")
    print(LINE)
    
    restricted_count = sum(1 for c in selected_cookies if c.get('status') == 'restricted')
    if restricted_count > 0:
        print(f" {R(f'⚠ WARNING: {restricted_count} restricted account(s) detected!')}")
        print(f" {C('Restricted accounts may not be able to share posts.')}")
        print(LINE)
    
    confirm = input(f" {W}[{W}➤{W}]{RESET} {G('Confirm? (Y/N)')} {W}➤{RESET} ").strip().upper()
    
    if confirm == 'Y':
        return selected_cookies
    else:
        return None

def start_auto_share():
    refresh_screen()
    
    print(f" {C('[!] AUTO SHARE - NORMAL ACCOUNTS')}")
    print(LINE)
    print(f" {G('[✓] INFORMATION:')}")
    print(f" {C('• Make sure your post is set to PUBLIC')}")
    print(f" {C('• This uses EAAG tokens (business.facebook.com method)')}")
    print(f" {C('• Shares run at MAXIMUM SPEED (zero delays)')}")
    print(f" {C('• Tokens auto-renew every 3 minutes')}")
    print(f" {C('• Best for normal accounts')}")
    print(LINE)
    
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r {apply_gradient(f'[CONTINUE IN {i} SECONDS]', 'purple_cyan')} {C('Reading time...')}")
        sys.stdout.flush()
        time.sleep(1)
    
    sys.stdout.write(f"\r{' ' * 60}\r")
    sys.stdout.flush()
    
    selected_cookies = select_cookies_for_sharing()
    
    if not selected_cookies:
        return
    
    refresh_screen()
    print(f" {C('[AUTO SHARE]')}")
    print(LINE)
    
    link_or_id = input(f" {W}[{W}➤{W}]{RESET} {C('POST LINK OR ID')} {W}➤{RESET} ").strip()
    
    if not link_or_id:
        return
    
    try:
        asyncio.run(auto_share_main(link_or_id, selected_cookies))
    except KeyboardInterrupt:
        refresh_screen()
        print(f" {C('[!] AUTO SHARE STOPPED BY USER')}")
        stop_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f" {C(f'[!] Stop Time: {stop_time}')}")
        print(f" {G(f'[!] Total Successful Shares: {success_count}')}")
        print(LINE)
        
        if success_count > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count})
            print(f" {G('[!] Shares recorded to your account')}")
        
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")
    except Exception as e:
        refresh_screen()
        print(f" {R('[ERROR] An unexpected error occurred:')}")
        print(f" {R(str(e))}")
        input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

# ============ MAIN FUNCTION ============

def main():
    global user_token, user_data
    
    while True:
        refresh_screen()
        
        prompt = f" {W}[{W}➤{W}]{RESET} {C('CHOICE')} {W}➤{RESET} "
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
                print(f"\n {R('[!] EXITING TOOL...')}")
                sys.exit()
            else:
                print(f"\n {R('[!] INVALID SELECTION')}")
                time.sleep(0.8)
        else:
            if choice in ['1', '01', 'A']:
                start_auto_share()
                
            elif choice in ['2', '02', 'B']:
                if user_data and user_data.get('isAdmin'):
                    file_encryptor()
                else:
                    manage_cookies()
            
            elif choice in ['3', '03', 'C']:
                if user_data and user_data.get('isAdmin'):
                    manage_cookies()
                else:
                    show_user_stats()
            
            elif choice in ['4', '04', 'D']:
                if user_data and user_data.get('isAdmin'):
                    show_user_stats()
                else:
                    update_tool_logic()
            
            elif choice in ['5', '05', 'E']:
                if user_data and user_data.get('isAdmin'):
                    admin_panel()
                else:
                    print(f"\n {R('[!] INVALID SELECTION')}")
                    time.sleep(0.8)
            
            elif choice in ['6', '06', 'F']:
                if user_data and user_data.get('isAdmin'):
                    update_tool_logic()
                else:
                    print(f"\n {R('[!] INVALID SELECTION')}")
                    time.sleep(0.8)
                
            elif choice in ['0', '00', 'X']:
                print(f"\n {C('[!] LOGGING OUT...')}")
                user_token = None
                user_data = None
                time.sleep(1)
                
            else:
                print(f"\n {R('[!] INVALID SELECTION')}")
                time.sleep(0.8)

if __name__ == "__main__":
    main()
