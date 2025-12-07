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

# Auto-install colorama for gradient support
def install_colorama():
    """Auto-install colorama if not available"""
    try:
        importlib.import_module('colorama')
    except ImportError:
        print("Installing colorama for gradient colors...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    install_colorama()
    from colorama import init, Fore, Back, Style
    init()
    COLORAMA_AVAILABLE = True
except:
    COLORAMA_AVAILABLE = False

# --- GRADIENT COLOR SYSTEM ---
def get_gradient_color(progress, color_scheme='purple_cyan'):
    """Generate RGB color code based on progress (0.0 to 1.0)"""
    progress = max(0, min(1, progress))
    
    color_schemes = {
        'purple_cyan': [
            (138, 43, 226),   # Blue Violet
            (147, 51, 234),   # Purple
            (168, 85, 247),   # Medium Purple
            (192, 132, 252),  # Light Purple
            (216, 180, 254),  # Lighter Purple
            (147, 197, 253),  # Light Blue
            (125, 211, 252),  # Sky Blue
            (34, 211, 238),   # Cyan
        ],
        'green_yellow': [
            (16, 185, 129),   # Emerald
            (52, 211, 153),   # Light Green
            (110, 231, 183),  # Lighter Green
            (167, 243, 208),  # Very Light Green
            (253, 224, 71),   # Yellow
            (250, 204, 21),   # Gold
        ],
        'red_orange': [
            (220, 38, 38),    # Red
            (239, 68, 68),    # Light Red
            (248, 113, 113),  # Lighter Red
            (251, 146, 60),   # Orange
            (253, 186, 116),  # Light Orange
            (254, 215, 170),  # Very Light Orange
        ],
        'blue_purple': [
            (37, 99, 235),    # Blue
            (59, 130, 246),   # Light Blue
            (96, 165, 250),   # Lighter Blue
            (147, 197, 253),  # Sky Blue
            (167, 139, 250),  # Lavender
            (196, 181, 253),  # Light Purple
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

# Apply gradient to constants
G = lambda text: apply_gradient(text, 'green_yellow')
R = lambda text: apply_gradient(text, 'red_orange')
C = lambda text: apply_gradient(text, 'purple_cyan')
Y = lambda text: apply_gradient(text, 'green_yellow')
M = lambda text: apply_gradient(text, 'blue_purple')
B = lambda text: apply_gradient(text, 'purple_cyan')
W = '\033[1;37m'  # White (Bold)
RESET = '\033[0m'

# Background colors for menu
BG_R = '\033[41m'
BG_G = '\033[42m'
BG_C = '\033[46m'
BG_M = '\033[45m'
BG_Y = '\033[43m'
BG_B = '\033[44m'

# --- UI CONSTANTS ---
LINE = apply_gradient("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'purple_cyan')

# --- API CONFIGURATION ---
API_URL = "https://rpwtools.onrender.com/api"
user_token = None
user_data = None

# --- GLOBAL VARIABLES FOR AUTO SHARE ---
success_count = 0
lock = asyncio.Lock()

def clear():
    """Clears the terminal screen completely."""
    os.system('clear' if os.name != 'nt' else 'cls')

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
    banner_art = """
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    """
    print(apply_gradient(banner_art, 'purple_cyan'))
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('DEVELOPER', 'purple_cyan') + f" {W}➤{RESET} " + apply_gradient('KEN DRICK', 'green_yellow'))
    print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('GITHUB', 'purple_cyan') + f"    {W}➤{RESET} " + apply_gradient('RYO GRAHHH', 'green_yellow'))
    print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('VERSION', 'purple_cyan') + f"   {W}➤{RESET} " + apply_gradient('1.0.3', 'green_yellow'))
    print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('FACEBOOK', 'purple_cyan') + f"  {W}➤{RESET} " + apply_gradient('facebook.com/ryoevisu', 'green_yellow'))
    
    tool_name = apply_gradient('[ RPWTOOLS ]', 'red_orange')
    print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient("TOOL'S NAME", 'purple_cyan') + f" {W}➤{RESET} {tool_name}")
    
    if user_data:
        print(LINE)
        username_display = user_data['username'].upper()
        print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('USERNAME', 'purple_cyan') + f"     {W}➤{RESET} " + apply_gradient(username_display, 'green_yellow'))
        
        fb_link = user_data.get('facebook', 'N/A')
        print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('FACEBOOK', 'purple_cyan') + f"     {W}➤{RESET} " + apply_gradient(fb_link, 'green_yellow'))
        
        country_display = user_data.get('country', 'N/A').upper()
        print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('COUNTRY', 'purple_cyan') + f"      {W}➤{RESET} " + apply_gradient(country_display, 'green_yellow'))
        
        # Color-coded plan display
        user_plan = user_data['plan']
        if user_plan == 'max':
            if user_data.get('planExpiry'):
                plan_display = apply_gradient('[ MAX ]', 'blue_purple')
            else:
                plan_display = apply_gradient('[ MAX LIFETIME ]', 'blue_purple')
        else:  # free
            plan_display = apply_gradient('[ FREE ]', 'green_yellow')
        
        print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('PLAN', 'purple_cyan') + f"         {W}➤{RESET} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('PLAN EXPIRY IN', 'purple_cyan') + f" {W}➤{RESET} " + apply_gradient(user_data['planExpiry'], 'red_orange'))
        
        # Show cookie count
        cookie_count = user_data.get('cookieCount', 0)
        print(f" {W}[{RESET}•{W}]{RESET} " + apply_gradient('TOTAL COOKIES', 'purple_cyan') + f"  {W}➤{RESET} " + apply_gradient(str(cookie_count), 'green_yellow'))
    
    print(LINE)

def show_menu():
    """Prints the Menu Options."""
    if not user_token:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y('/')}{RESET}{BG_G}{W}A{RESET}{W}]{RESET} " + apply_gradient('LOGIN', 'green_yellow'))
        print(f" {W}[{RESET}{BG_C}{W}02{RESET}{BG_C}{Y('/')}{RESET}{BG_C}{W}B{RESET}{W}]{RESET} " + apply_gradient('REGISTER', 'purple_cyan'))
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y('/')}{RESET}{BG_R}{W}X{RESET}{W}]{RESET} " + apply_gradient('EXIT', 'red_orange'))
    elif user_data and user_data.get('isAdmin'):
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y('/')}{RESET}{BG_G}{W}A{RESET}{W}]{RESET} " + apply_gradient('AUTO SHARE              — NORM ACCOUNTS', 'green_yellow'))
        print(f" {W}[{RESET}{BG_Y}{W}02{RESET}{BG_Y}{Y('/')}{RESET}{BG_Y}{W}B{RESET}{W}]{RESET} " + apply_gradient('FILE ENCRYPTOR          — CYTHON ENCRYPTION', 'blue_purple'))
        print(f" {W}[{RESET}{BG_C}{W}03{RESET}{BG_C}{Y('/')}{RESET}{BG_C}{W}C{RESET}{W}]{RESET} " + apply_gradient('MANAGE COOKIES          — DATABASE', 'purple_cyan'))
        print(f" {W}[{RESET}{BG_B}{W}04{RESET}{BG_B}{Y('/')}{RESET}{BG_B}{W}D{RESET}{W}]{RESET} " + apply_gradient('MY STATS                — STATISTICS', 'purple_cyan'))
        print(f" {W}[{RESET}{BG_M}{W}05{RESET}{BG_M}{Y('/')}{RESET}{BG_M}{W}E{RESET}{W}]{RESET} " + apply_gradient('ADMIN PANEL             — MANAGEMENT', 'blue_purple'))
        print(f" {W}[{RESET}{BG_G}{W}06{RESET}{BG_G}{Y('/')}{RESET}{BG_G}{W}F{RESET}{W}]{RESET} " + apply_gradient('UPDATE TOOL             — LATEST VERSION', 'green_yellow'))
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y('/')}{RESET}{BG_R}{W}X{RESET}{W}]{RESET} " + apply_gradient('LOGOUT', 'red_orange'))
    else:
        print(f" {W}[{RESET}{BG_G}{W}01{RESET}{BG_G}{Y('/')}{RESET}{BG_G}{W}A{RESET}{W}]{RESET} " + apply_gradient('AUTO SHARE              — NORM ACCOUNTS', 'green_yellow'))
        print(f" {W}[{RESET}{BG_Y}{W}02{RESET}{BG_Y}{Y('/')}{RESET}{BG_Y}{W}B{RESET}{W}]{RESET} " + apply_gradient('MANAGE COOKIES          — DATABASE', 'purple_cyan'))
        print(f" {W}[{RESET}{BG_B}{W}03{RESET}{BG_B}{Y('/')}{RESET}{BG_B}{W}C{RESET}{W}]{RESET} " + apply_gradient('MY STATS                — STATISTICS', 'purple_cyan'))
        print(f" {W}[{RESET}{BG_G}{W}04{RESET}{BG_G}{Y('/')}{RESET}{BG_G}{W}D{RESET}{W}]{RESET} " + apply_gradient('UPDATE TOOL             — LATEST VERSION', 'green_yellow'))
        print(f" {W}[{RESET}{BG_R}{W}00{RESET}{BG_R}{Y('/')}{RESET}{BG_R}{W}X{RESET}{W}]{RESET} " + apply_gradient('LOGOUT', 'red_orange'))
    
    print(LINE)

def refresh_screen():
    """Instantly wipes screen and repaints the UI base."""
    clear()
    banner_header()
    show_menu()

def nice_loader(text="PROCESSING"):
    """Improved Progress Bar Loader with gradient."""
    sys.stdout.write("\033[?25l")
    
    filled = "■"
    empty = "□"
    width = 20
    
    for i in range(width + 1):
        percent = int((i / width) * 100)
        bar = filled * i + empty * (width - i)
        bar_gradient = apply_gradient(bar, 'purple_cyan')
        
        sys.stdout.write(f"\r {W}[{RESET}•{W}]{RESET} " + apply_gradient(text, 'green_yellow') + f" {W}➤{RESET} [{bar_gradient}] {apply_gradient(f'{percent}%', 'blue_purple')}")
        sys.stdout.flush()
        time.sleep(0.04) 
    
    time.sleep(0.3) 
    sys.stdout.write(f"\r{' ' * 80}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")

# Continue with rest of the functions...
# (I'll add the remaining functions in the next part to stay within limits)

def select_progress_display():
    """Let user choose progress display mode"""
    refresh_screen()
    print(" " + apply_gradient('[SHARING PROGRESS DISPLAY]', 'purple_cyan'))
    print(LINE)
    print(" " + apply_gradient('Choose how you want to see sharing progress:', 'green_yellow'))
    print(LINE)
    print(f" {W}[{RESET}{BG_G}{W}1{RESET}{W}]{RESET} " + apply_gradient('SUCCESS COUNTER (1/100)', 'green_yellow'))
    print(f"     " + apply_gradient('• Best for smaller screens (mobile)', 'purple_cyan'))
    print(f"     " + apply_gradient('• Shows only success count', 'purple_cyan'))
    print(f"     " + apply_gradient('• Minimal display, stays in one place', 'purple_cyan'))
    print(LINE)
    print(f" {W}[{RESET}{BG_C}{W}2{RESET}{W}]{RESET} " + apply_gradient('DETAILED LOGS', 'purple_cyan'))
    print(f"     " + apply_gradient('• Best for larger screens (desktop)', 'green_yellow'))
    print(f"     " + apply_gradient('• Shows success, time, account info', 'green_yellow'))
    print(f"     " + apply_gradient('• Full process information', 'green_yellow'))
    print(LINE)
    
    while True:
        choice = input(f" {W}[{W}➤{W}]{RESET} " + apply_gradient('CHOICE (1 or 2)', 'purple_cyan') + f" {W}➤{RESET} ").strip()
        
        if choice == '1':
            return 'minimal'
        elif choice == '2':
            return 'detailed'
        else:
            print(" " + apply_gradient('[!] Invalid choice. Please enter 1 or 2', 'red_orange'))
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

# NOTE: Due to character limits, I'll provide the complete code in parts.
# This is Part 1 with the gradient color system and core functions.
# Would you like me to continue with the remaining functions including:
# - Login/Register functions
# - Cookie management
# - Auto share functions
# - Admin panel
# - Cython encryptor (NEW)
# - Main function

if __name__ == "__main__":
    print(apply_gradient("RPWTOOLS v1.0.3 - Loading...", 'purple_cyan'))
    time.sleep(1)
