#!/usr/bin/env python3
# RPWTOOLS v1.0.4 - Facebook Auto Share Tool
# Developer: KEN DRICK
# Facebook: facebook.com/ryoevisu

import os
import sys
import time
import datetime
import re
import subprocess
import zlib
import base64

def install_packages():
    packages = ['colorama', 'aiohttp', 'requests']
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

install_packages()

import requests
import aiohttp
import asyncio
from colorama import init
init()

def get_color(progress, scheme):
    schemes = {
        'cyan': [(138,43,226), (147,51,234), (168,85,247), (192,132,252), (125,211,252), (34,211,238)],
        'green': [(16,185,129), (52,211,153), (110,231,183), (167,243,208), (253,224,71), (250,204,21)],
        'red': [(220,38,38), (239,68,68), (248,113,113), (251,146,60), (253,186,116)],
        'blue': [(37,99,235), (59,130,246), (96,165,250), (147,197,253), (167,139,250)]
    }
    colors = schemes.get(scheme, schemes['cyan'])
    idx = int(progress * (len(colors) - 1))
    r, g, b = colors[min(idx, len(colors) - 1)]
    return f'\033[38;2;{r};{g};{b}m'

def gradient(text, scheme='cyan'):
    text = str(text)
    if not text.strip():
        return text
    result = []
    visible_chars = [c for c in text if c != ' ']
    if not visible_chars:
        return text
    char_index = 0
    for char in text:
        if char == ' ':
            result.append(char)
        else:
            progress = char_index / max(1, len(visible_chars) - 1)
            color = get_color(progress, scheme)
            result.append(f'{color}{char}\033[0m')
            char_index += 1
    return ''.join(result)

def G(text):
    return gradient(str(text), 'green')

def R(text):
    return gradient(str(text), 'red')

def C(text):
    return gradient(str(text), 'cyan')

def M(text):
    return gradient(str(text), 'blue')

W = '\033[1;37m'
RESET = '\033[0m'
LINE = gradient("━" * 50, 'cyan')

API_URL = "https://rpwtoolservernew-api.onrender.com/api"
user_token = None
user_data = None
success_count = 0
success_count_v2 = 0
lock = asyncio.Lock()

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def normalize_facebook_url(url):
    if not url:
        return url
    url = url.strip()
    url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
    url = re.sub(r'^(www\.|m\.)', '', url, flags=re.IGNORECASE)
    if not url.startswith('facebook.com'):
        if '/' not in url:
            url = 'facebook.com/' + url
    return url

def show_banner():
    banner_art = """
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    """
    print(gradient(banner_art, 'cyan'))
    print(LINE)
    print(f" {W}[•]{RESET} {C('DEVELOPER')}     {W}➤{RESET} {G('KEN DRICK')}")
    print(f" {W}[•]{RESET} {C('VERSION')}       {W}➤{RESET} {G('1.0.4')}")
    print(f" {W}[•]{RESET} {C('FACEBOOK')}      {W}➤{RESET} {G('facebook.com/ryoevisu')}")
    print(f" {W}[•]{RESET} {C('TOOL NAME')}     {W}➤{RESET} {R('[ RPWTOOLS ]')}")
    
    if user_data:
        print(LINE)
        print(f" {W}[•]{RESET} {C('USERNAME')}      {W}➤{RESET} {G(user_data['username'].upper())}")
        print(f" {W}[•]{RESET} {C('FACEBOOK')}      {W}➤{RESET} {G(user_data.get('facebook', 'N/A'))}")
        print(f" {W}[•]{RESET} {C('COUNTRY')}       {W}➤{RESET} {G(user_data.get('country', 'N/A').upper())}")
        
        plan = user_data.get('plan', 'inactive')
        expiry = user_data.get('planExpiry')
        
        if plan == 'inactive':
            plan_display = R('[ INACTIVE ]')
        elif plan == 'maxplus':
            if expiry:
                plan_display = M('[ MAX+ ] - ' + expiry)
            else:
                plan_display = M('[ MAX+ LIFETIME ]')
        else:
            if expiry:
                plan_display = M('[ MAX ] - ' + expiry)
            else:
                plan_display = M('[ MAX LIFETIME ]')
        
        print(f" {W}[•]{RESET} {C('PLAN')}          {W}➤{RESET} {plan_display}")
        print(f" {W}[•]{RESET} {C('COOKIES (V1)')} {W}➤{RESET} {G(str(user_data.get('cookieCount', 0)))}")
        
        if plan == 'maxplus' or user_data.get('isAdmin'):
            print(f" {W}[•]{RESET} {C('TOKENS (V2)')}  {W}➤{RESET} {G(str(user_data.get('tokenCount', 0)))}")
    
    print(LINE)

def show_menu():
    if not user_token:
        print(f" {W}[01/A]{RESET} {G('LOGIN')}")
        print(f" {W}[02/B]{RESET} {C('REGISTER')}")
        print(f" {W}[00/X]{RESET} {R('EXIT')}")
    elif user_data and user_data.get('isAdmin'):
        print(f" {W}[01/A]{RESET} {G('AUTO SHARE V1           — COOKIE/EAAG METHOD')}")
        print(f" {W}[02/B]{RESET} {C('AUTO SHARE V2           — TOKEN METHOD')}")
        print(f" {W}[03/C]{RESET} {M('FILE ENCRYPTOR          — CYTHON ENCRYPTION')}")
        print(f" {W}[04/D]{RESET} {G('MANAGE COOKIES          — V1 DATABASE')}")
        print(f" {W}[05/E]{RESET} {C('MANAGE TOKENS           — V2 DATABASE')}")
        print(f" {W}[06/F]{RESET} {M('MY STATS                — STATISTICS')}")
        print(f" {W}[07/G]{RESET} {G('ADMIN PANEL             — MANAGEMENT')}")
        print(f" {W}[00/X]{RESET} {R('LOGOUT')}")
    elif user_data and user_data.get('plan') == 'maxplus':
        print(f" {W}[01/A]{RESET} {G('AUTO SHARE V1           — COOKIE/EAAG METHOD')}")
        print(f" {W}[02/B]{RESET} {C('AUTO SHARE V2           — TOKEN METHOD')}")
        print(f" {W}[03/C]{RESET} {M('MANAGE COOKIES          — V1 DATABASE')}")
        print(f" {W}[04/D]{RESET} {G('MANAGE TOKENS           — V2 DATABASE')}")
        print(f" {W}[05/E]{RESET} {C('MY STATS                — STATISTICS')}")
        print(f" {W}[00/X]{RESET} {R('LOGOUT')}")
    else:
        print(f" {W}[01/A]{RESET} {G('AUTO SHARE V1           — COOKIE/EAAG METHOD')}")
        print(f" {W}[02/B]{RESET} {M('MANAGE COOKIES          — V1 DATABASE')}")
        print(f" {W}[03/C]{RESET} {C('MY STATS                — STATISTICS')}")
        print(f" {W}[00/X]{RESET} {R('LOGOUT')}")
    print(LINE)

def refresh_screen():
    clear_screen()
    show_banner()
    show_menu()

def show_loader(text="PROCESSING"):
    sys.stdout.write("\033[?25l")
    for i in range(21):
        filled = "■" * i
        empty = "□" * (20 - i)
        bar = gradient(filled + empty, 'cyan')
        percent = M(str(i * 5) + '%')
        sys.stdout.write(f"\r {W}[•]{RESET} {G(text)} {W}➤{RESET} [{bar}] {percent}")
        sys.stdout.flush()
        time.sleep(0.03)
    sys.stdout.write(f"\r{' ' * 70}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")

def get_user_country():
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
        headers["Authorization"] = "Bearer " + user_token
    
    url = API_URL + endpoint
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=15)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=15)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=15)
        else:
            return None, "Invalid method"
        
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to server"
    except requests.exceptions.Timeout:
        return None, "Request timeout"
    except Exception as e:
        return None, str(e)

def do_login():
    global user_token, user_data
    
    refresh_screen()
    print(f" {G('[LOGIN TO RPWTOOLS]')}")
    print(LINE)
    
    username = input(f" {W}[➤]{RESET} {C('USERNAME')} {W}➤{RESET} ").strip()
    if not username:
        return
    
    password = input(f" {W}[➤]{RESET} {C('PASSWORD')} {W}➤{RESET} ").strip()
    if not password:
        return
    
    refresh_screen()
    show_loader("LOGGING IN")
    
    status, response = api_request("POST", "/auth/login", {
        "username": username,
        "password": password
    }, use_token=False)
    
    if status == 200 and response.get('success'):
        user_token = response.get('token')
        user_data = response.get('user')
        
        print(f" {G('[SUCCESS] Login successful!')}")
        print(LINE)
        uname = user_data['username'].upper()
        print(f" {G('Welcome,')} {M(uname)}")
        
        plan = user_data.get('plan', 'inactive')
        if plan == 'inactive':
            print(f" {R('[!] Your account is INACTIVE.')}")
            print(f" {C('Contact admin to activate your plan.')}")
        elif user_data.get('planExpired'):
            print(f" {R('[!] Your plan has EXPIRED.')}")
            print(f" {C('Contact admin to renew your plan.')}")
        elif plan == 'maxplus':
            print(f" {G('Plan:')} {M('MAX+ (V1 + V2)')}")
        else:
            print(f" {G('Plan:')} {M('MAX (V1 Only)')}")
        
        if user_data.get('isAdmin'):
            print(f" {M('[ADMIN ACCESS GRANTED]')}")
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Login failed')
        print(f" {R('[ERROR]')} {R(error_msg)}")
    
    print(LINE)
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def do_register():
    global user_token, user_data
    
    refresh_screen()
    print(f" {G('[REGISTER NEW ACCOUNT]')}")
    print(LINE)
    print(f" {R('[!] New accounts are INACTIVE by default.')}")
    print(f" {C('Contact admin after registration to activate.')}")
    print(LINE)
    print(f" {G('PRICING:')}")
    print(f" {M('MAX')}  (V1 Only):  1m=₱150 | 3m=₱250 | LIFETIME")
    print(f" {M('MAX+')} (V1+V2):    1m=₱200 | 3m=₱350 | LIFETIME")
    print(LINE)
    
    username = input(f" {W}[➤]{RESET} {C('USERNAME')} {W}➤{RESET} ").strip()
    if not username:
        return
    
    password = input(f" {W}[➤]{RESET} {C('PASSWORD')} {W}➤{RESET} ").strip()
    if not password:
        return
    
    facebook = input(f" {W}[➤]{RESET} {C('FACEBOOK LINK')} {W}➤{RESET} ").strip()
    if not facebook:
        return
    
    facebook = normalize_facebook_url(facebook)
    
    show_loader("DETECTING COUNTRY")
    country = get_user_country()
    print(f" {G('Detected Country:')} {C(country)}")
    
    confirm = input(f" {W}[➤]{RESET} {G('Is this correct? (Y/N)')} {W}➤{RESET} ").strip().upper()
    if confirm == 'N':
        country = input(f" {W}[➤]{RESET} {C('ENTER YOUR COUNTRY')} {W}➤{RESET} ").strip()
        if not country:
            country = 'Unknown'
    
    show_loader("REGISTERING")
    
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
        print(f" {R('[!] Your account is INACTIVE.')}")
        print(f" {C('Contact admin to activate your plan.')}")
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Registration failed')
        print(f" {R('[ERROR]')} {R(error_msg)}")
    
    print(LINE)
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def show_stats():
    refresh_screen()
    show_loader("LOADING STATS")
    
    status, response = api_request("GET", "/user/stats")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats', {})
        
        refresh_screen()
        print(f" {G('[USER STATISTICS]')}")
        print(LINE)
        uname = stats.get('username', 'N/A').upper()
        print(f" {C('Username:')} {M(uname)}")
        print(f" {C('Facebook:')} {G(stats.get('facebook', 'N/A'))}")
        print(f" {C('Country:')} {G(stats.get('country', 'N/A'))}")
        
        plan = stats.get('plan', 'inactive')
        plan_name = 'INACTIVE' if plan == 'inactive' else ('MAX+' if plan == 'maxplus' else 'MAX')
        print(f" {C('Plan:')} {M(plan_name)}")
        
        if stats.get('planExpiry'):
            print(f" {C('Expiry:')} {R(stats['planExpiry'])}")
        elif plan != 'inactive':
            print(f" {C('Type:')} {M('LIFETIME')}")
        
        print(LINE)
        print(f" {G('Total Shares V1:')} {M(str(stats.get('totalShares', 0)))}")
        
        if plan == 'maxplus' or stats.get('isAdmin'):
            print(f" {G('Total Shares V2:')} {M(str(stats.get('totalSharesV2', 0)))}")
        
        print(f" {G('Cookies Stored:')} {C(str(stats.get('cookieCount', 0)))}")
        
        if plan == 'maxplus' or stats.get('isAdmin'):
            print(f" {G('Tokens Stored:')} {C(str(stats.get('tokenCount', 0)))}")
        
        print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load stats')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def manage_cookies():
    while True:
        refresh_screen()
        print(f" {G('[MANAGE COOKIES - V1]')}")
        print(LINE)
        print(f" {W}[1]{RESET} {G('VIEW ALL COOKIES')}")
        print(f" {W}[2]{RESET} {G('ADD NEW COOKIE')}")
        print(f" {W}[3]{RESET} {R('DELETE COOKIE')}")
        print(f" {W}[4]{RESET} {R('DELETE ALL COOKIES')}")
        print(f" {W}[0]{RESET} {C('BACK TO MENU')}")
        print(LINE)
        
        choice = input(f" {W}[➤]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip()
        
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

def view_cookies():
    refresh_screen()
    show_loader("LOADING COOKIES")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status == 200 and response.get('success'):
        cookies = response.get('cookies', [])
        
        refresh_screen()
        total = len(cookies)
        print(f" {G('[COOKIES] Total: ' + str(total))}")
        print(LINE)
        
        if not cookies:
            print(f" {C('No cookies stored yet.')}")
        else:
            for i, cookie in enumerate(cookies, 1):
                num = str(i).zfill(2)
                print(f" {W}[{num}]{RESET} {M(cookie['name'])} {W}(UID: {C(cookie['uid'])}){RESET}")
                print(f"      Status: {G(cookie['status'])} | Added: {G(cookie['addedAt'])}")
                print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load cookies')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def add_cookie():
    refresh_screen()
    print(f" {G('[ADD NEW COOKIE]')}")
    print(LINE)
    
    cookie = input(f" {W}[➤]{RESET} {C('COOKIE')} {W}➤{RESET} ").strip()
    if not cookie:
        return
    
    print(f" {C('Validating cookie... (may take 10-15 seconds)')}")
    show_loader("VALIDATING COOKIE")
    
    status, response = api_request("POST", "/user/cookies", {"cookie": cookie})
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS] Cookie added!')}")
        print(f" {C('Account Name:')} {M(response.get('name', 'Unknown'))}")
        print(f" {C('Account UID:')} {C(response.get('uid', 'Unknown'))}")
        
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed')
        print(f" {R('[ERROR]')} {R(error_msg)}")
    
    print(LINE)
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def delete_cookie():
    show_loader("LOADING COOKIES")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load cookies')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        print(f" {C('No cookies to delete.')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(f" {R('[DELETE COOKIE]')}")
    print(LINE)
    
    for i, cookie in enumerate(cookies, 1):
        print(f" {W}[{i}]{RESET} {M(cookie['name'])} (UID: {cookie['uid']})")
    
    print(LINE)
    choice = input(f" {W}[➤]{RESET} {C('ENTER NUMBER (0 to cancel)')} {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(cookies):
            show_loader("DELETING")
            cookie_id = cookies[index]['id']
            status, response = api_request("DELETE", "/user/cookies/" + cookie_id)
            
            if status == 200 and response.get('success'):
                print(f" {G('[SUCCESS] Cookie deleted!')}")
                if user_data:
                    user_data['cookieCount'] = response.get('totalCookies', 0)
            else:
                print(f" {R('[ERROR] Failed to delete cookie')}")
        else:
            print(f" {R('[ERROR] Invalid selection')}")
    except ValueError:
        print(f" {R('[ERROR] Invalid input')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def delete_all_cookies():
    refresh_screen()
    print(f" {R('[DELETE ALL COOKIES]')}")
    print(LINE)
    
    confirm = input(f" {W}[➤]{RESET} {R('Type YES to confirm')} {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    show_loader("DELETING ALL")
    
    status, response = api_request("DELETE", "/user/cookies")
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS] All cookies deleted!')}")
        if user_data:
            user_data['cookieCount'] = 0
    else:
        print(f" {R('[ERROR] Failed to delete cookies')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def manage_tokens():
    while True:
        refresh_screen()
        print(f" {G('[MANAGE TOKENS - V2]')}")
        print(LINE)
        print(f" {W}[1]{RESET} {G('VIEW ALL TOKENS')}")
        print(f" {W}[2]{RESET} {G('ADD NEW TOKEN')}")
        print(f" {W}[3]{RESET} {R('DELETE TOKEN')}")
        print(f" {W}[4]{RESET} {R('DELETE ALL TOKENS')}")
        print(f" {W}[0]{RESET} {C('BACK TO MENU')}")
        print(LINE)
        
        choice = input(f" {W}[➤]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip()
        
        if choice == '1':
            view_tokens()
        elif choice == '2':
            add_token()
        elif choice == '3':
            delete_token()
        elif choice == '4':
            delete_all_tokens()
        elif choice == '0':
            return

def view_tokens():
    refresh_screen()
    show_loader("LOADING TOKENS")
    
    status, response = api_request("GET", "/user/tokens")
    
    if status == 403:
        print(f" {R('[ERROR] MAX+ plan required')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    if status == 200 and response.get('success'):
        tokens = response.get('tokens', [])
        
        refresh_screen()
        total = len(tokens)
        print(f" {G('[TOKENS] Total: ' + str(total))}")
        print(LINE)
        
        if not tokens:
            print(f" {C('No tokens stored yet.')}")
        else:
            for i, token in enumerate(tokens, 1):
                num = str(i).zfill(2)
                print(f" {W}[{num}]{RESET} {M(token['name'])} {W}(UID: {C(token['uid'])}){RESET}")
                print(f"      Status: {G(token['status'])} | Added: {G(token['addedAt'])}")
                print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load tokens')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def add_token():
    refresh_screen()
    print(f" {G('[ADD NEW TOKEN]')}")
    print(LINE)
    
    token = input(f" {W}[➤]{RESET} {C('TOKEN')} {W}➤{RESET} ").strip()
    if not token:
        return
    
    show_loader("VALIDATING TOKEN")
    
    status, response = api_request("POST", "/user/tokens", {"token": token})
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS] Token added!')}")
        print(f" {C('Account Name:')} {M(response.get('name', 'Unknown'))}")
        print(f" {C('Account UID:')} {C(response.get('uid', 'Unknown'))}")
        
        if user_data:
            user_data['tokenCount'] = response.get('totalTokens', 0)
    elif status == 403:
        print(f" {R('[ERROR] MAX+ plan required')}")
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed')
        print(f" {R('[ERROR]')} {R(error_msg)}")
    
    print(LINE)
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def delete_token():
    show_loader("LOADING TOKENS")
    
    status, response = api_request("GET", "/user/tokens")
    
    if status == 403:
        print(f" {R('[ERROR] MAX+ plan required')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load tokens')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    tokens = response.get('tokens', [])
    
    if not tokens:
        print(f" {C('No tokens to delete.')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(f" {R('[DELETE TOKEN]')}")
    print(LINE)
    
    for i, token in enumerate(tokens, 1):
        print(f" {W}[{i}]{RESET} {M(token['name'])} (UID: {token['uid']})")
    
    print(LINE)
    choice = input(f" {W}[➤]{RESET} {C('ENTER NUMBER (0 to cancel)')} {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(tokens):
            show_loader("DELETING")
            token_id = tokens[index]['id']
            status, response = api_request("DELETE", "/user/tokens/" + token_id)
            
            if status == 200 and response.get('success'):
                print(f" {G('[SUCCESS] Token deleted!')}")
                if user_data:
                    user_data['tokenCount'] = response.get('totalTokens', 0)
            else:
                print(f" {R('[ERROR] Failed to delete token')}")
        else:
            print(f" {R('[ERROR] Invalid selection')}")
    except ValueError:
        print(f" {R('[ERROR] Invalid input')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def delete_all_tokens():
    refresh_screen()
    print(f" {R('[DELETE ALL TOKENS]')}")
    print(LINE)
    
    confirm = input(f" {W}[➤]{RESET} {R('Type YES to confirm')} {W}➤{RESET} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    show_loader("DELETING ALL")
    
    status, response = api_request("DELETE", "/user/tokens")
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS] All tokens deleted!')}")
        if user_data:
            user_data['tokenCount'] = 0
    else:
        print(f" {R('[ERROR] Failed to delete tokens')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def admin_panel():
    while True:
        refresh_screen()
        print(f" {M('[ADMIN PANEL]')}")
        print(LINE)
        print(f" {W}[1]{RESET} {G('VIEW ALL USERS')}")
        print(f" {W}[2]{RESET} {C('ACTIVATE USER PLAN')}")
        print(f" {W}[3]{RESET} {R('DELETE USER')}")
        print(f" {W}[4]{RESET} {G('DASHBOARD STATS')}")
        print(f" {W}[0]{RESET} {C('BACK TO MENU')}")
        print(LINE)
        
        choice = input(f" {W}[➤]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip()
        
        if choice == '1':
            admin_view_users()
        elif choice == '2':
            admin_activate_plan()
        elif choice == '3':
            admin_delete_user()
        elif choice == '4':
            admin_dashboard()
        elif choice == '0':
            return

def admin_view_users():
    show_loader("LOADING USERS")
    
    status, response = api_request("GET", "/admin/users")
    
    if status == 200 and response.get('success'):
        users = response.get('users', [])
        
        refresh_screen()
        total = len(users)
        print(f" {G('[ALL USERS] Total: ' + str(total))}")
        print(LINE)
        
        for i, user in enumerate(users, 1):
            admin_badge = " " + M('[ADMIN]') if user.get('isAdmin') else ""
            
            plan = user.get('plan', 'inactive')
            if plan == 'inactive':
                plan_status = R('INACTIVE')
            elif user.get('isLifetime'):
                plan_status = M(plan.upper() + ' LIFETIME')
            elif user.get('planExpiry') == 'Expired':
                plan_status = R('EXPIRED')
            else:
                plan_status = G(user.get('planExpiry', 'Active'))
            
            plan_name = 'MAX+' if plan == 'maxplus' else plan.upper()
            num = str(i).zfill(2)
            uname = user['username'].upper()
            
            print(f" {W}[{num}]{RESET} {C(uname)}{admin_badge}")
            print(f"      Plan: {M(plan_name)} | Status: {plan_status}")
            print(f"      Facebook: {G(user.get('facebook', 'N/A'))}")
            print(f"      Country: {G(user.get('country', 'N/A'))} | Cookies: {C(str(user.get('cookieCount', 0)))} | Tokens: {C(str(user.get('tokenCount', 0)))}")
            print(f"      Shares V1: {G(str(user.get('totalShares', 0)))} | V2: {G(str(user.get('totalSharesV2', 0)))}")
            print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load users')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def admin_activate_plan():
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load users')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    users = response.get('users', [])
    
    refresh_screen()
    print(f" {C('[SELECT USER TO ACTIVATE]')}")
    print(LINE)
    
    for i, user in enumerate(users, 1):
        plan = user.get('plan', 'inactive')
        if plan == 'inactive':
            status_str = R('INACTIVE')
        elif user.get('isLifetime'):
            status_str = M('LIFETIME')
        else:
            status_str = G(user.get('planExpiry', 'Active'))
        
        uname = user['username'].upper()
        print(f" {W}[{i}]{RESET} {C(uname)} - {status_str}")
    
    print(LINE)
    choice = input(f" {W}[➤]{RESET} {C('USER NUMBER (0 to cancel)')} {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(users):
            print(f" {R('[ERROR] Invalid selection')}")
            input(f" {G('[PRESS ENTER TO CONTINUE]')}")
            return
        
        selected_user = users[index]
    except ValueError:
        print(f" {R('[ERROR] Invalid input')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    selected_username = selected_user['username']
    
    refresh_screen()
    uname_upper = selected_username.upper()
    print(f" {C('[PLAN FOR: ' + uname_upper + ']')}")
    print(LINE)
    print(f" {W}[1]{RESET} {M('MAX')} - V1 Only (Cookie/EAAG)")
    print(f" {W}[2]{RESET} {M('MAX+')} - V1 + V2 (Cookie + Token)")
    print(f" {W}[3]{RESET} {R('DEACTIVATE')} - Set to INACTIVE")
    print(LINE)
    
    plan_choice = input(f" {W}[➤]{RESET} {C('PLAN TYPE')} {W}➤{RESET} ").strip()
    
    if plan_choice == '3':
        show_loader("DEACTIVATING")
        api_request("PUT", "/admin/users/" + selected_username + "/plan", {"plan": "inactive"})
        print(f" {G('[SUCCESS] User deactivated!')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    plan_map = {'1': 'max', '2': 'maxplus'}
    if plan_choice not in plan_map:
        return
    
    selected_plan = plan_map[plan_choice]
    
    print(LINE)
    print(f" {W}[1]{RESET} 1 Month")
    print(f" {W}[2]{RESET} 2 Months")
    print(f" {W}[3]{RESET} 3 Months")
    print(f" {W}[4]{RESET} LIFETIME (No expiry)")
    print(LINE)
    
    duration_choice = input(f" {W}[➤]{RESET} {C('DURATION')} {W}➤{RESET} ").strip()
    
    duration_map = {'1': 1, '2': 2, '3': 3, '4': None}
    if duration_choice not in duration_map:
        return
    
    duration = duration_map[duration_choice]
    
    show_loader("ACTIVATING PLAN")
    
    status, response = api_request("PUT", "/admin/users/" + selected_username + "/plan", {
        "plan": selected_plan,
        "duration": duration
    })
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS]')} {G(response.get('message', 'Plan activated'))}")
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed')
        print(f" {R('[ERROR]')} {R(error_msg)}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def admin_delete_user():
    status, response = api_request("GET", "/admin/users")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load users')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    users = response.get('users', [])
    
    refresh_screen()
    print(f" {R('[DELETE USER]')}")
    print(LINE)
    
    for i, user in enumerate(users, 1):
        admin_badge = " " + M('[ADMIN]') if user.get('isAdmin') else ""
        uname = user['username'].upper()
        print(f" {W}[{i}]{RESET} {C(uname)}{admin_badge}")
    
    print(LINE)
    choice = input(f" {W}[➤]{RESET} {C('USER NUMBER (0 to cancel)')} {W}➤{RESET} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(users):
            return
        
        selected_user = users[index]
    except ValueError:
        return
    
    selected_username = selected_user['username']
    
    confirm_text = 'Delete user ' + selected_username + '? (YES/NO)'
    confirm = input(f" {R(confirm_text)} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    show_loader("DELETING USER")
    
    status, response = api_request("DELETE", "/admin/users/" + selected_username)
    
    if status == 200 and response.get('success'):
        print(f" {G('[SUCCESS] User deleted!')}")
    else:
        print(f" {R('[ERROR] Failed to delete user')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def admin_dashboard():
    show_loader("LOADING DASHBOARD")
    
    status, response = api_request("GET", "/admin/dashboard")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats', {})
        
        refresh_screen()
        print(f" {G('[ADMIN DASHBOARD]')}")
        print(LINE)
        print(f" {C('Total Users:')} {G(str(stats.get('totalUsers', 0)))}")
        print(f" {C('Active Users:')} {G(str(stats.get('activeUsers', 0)))}")
        print(f" {C('Inactive Users:')} {R(str(stats.get('inactiveUsers', 0)))}")
        print(f" {C('Expired Users:')} {R(str(stats.get('expiredUsers', 0)))}")
        print(f" {C('Lifetime Users:')} {M(str(stats.get('lifetimeUsers', 0)))}")
        print(LINE)
        print(f" {C('MAX Users:')} {G(str(stats.get('maxUsers', 0)))}")
        print(f" {C('MAX+ Users:')} {M(str(stats.get('maxPlusUsers', 0)))}")
        print(LINE)
        print(f" {C('Total V1 Shares:')} {G(str(stats.get('totalShares', 0)))}")
        print(f" {C('Total V2 Shares:')} {G(str(stats.get('totalSharesV2', 0)))}")
        print(f" {C('Total Cookies:')} {G(str(stats.get('totalCookies', 0)))}")
        print(f" {C('Total Tokens:')} {G(str(stats.get('totalTokens', 0)))}")
        print(LINE)
    else:
        print(f" {R('[ERROR] Failed to load dashboard')}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def file_encryptor():
    if not user_data or not user_data.get('isAdmin'):
        print(f" {R('[ACCESS DENIED] Admin only feature')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(f" {M('[FILE ENCRYPTOR - CYTHON ENCRYPTION]')}")
    print(LINE)
    
    file_path = input(f" {W}[➤]{RESET} {C('Python file path')} {W}➤{RESET} ").strip()
    file_path = file_path.strip('"\'')
    
    if not file_path.endswith('.py'):
        print(f" {R('[ERROR] File must be a .py file')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    if not os.path.exists(file_path):
        print(f" {R('[ERROR] File not found')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    show_loader("ENCRYPTING FILE")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
        
        compressed = zlib.compress(original_code.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('utf-8')
        
        encrypted_code = 'import zlib,base64;exec(zlib.decompress(base64.b64decode("' + encoded + '")).decode())'
        
        output_path = file_path.replace('.py', '_encrypted.py')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_code)
        
        print(f" {G('[SUCCESS] File encrypted!')}")
        print(f" {C('Output:')} {G(output_path)}")
    except Exception as e:
        print(f" {R('[ERROR] ' + str(e))}")
    
    input(f" {G('[PRESS ENTER TO CONTINUE]')}")

def extract_post_id(link):
    link = link.strip()
    
    if link.isdigit():
        return link
    
    patterns = [
        r'/posts/(\d+)',
        r'story_fbid=(\d+)',
        r'fbid=(\d+)',
        r'/permalink/(\d+)',
        r'/photos/[^/]+/(\d+)',
        r'/(\d+)/?$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    
    return link

async def get_post_id_from_api(session, link):
    try:
        async with session.post('https://id.traodoisub.com/api.php', data={"link": link}, timeout=aiohttp.ClientTimeout(total=15)) as response:
            data = await response.json()
            if 'id' in data:
                return data['id']
            return None
    except:
        return None

def convert_cookie_to_eaag(cookie):
    try:
        response = requests.get(
            'https://business.facebook.com/business_locations',
            headers={
                'cookie': cookie,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'referer': 'https://www.facebook.com/',
                'host': 'business.facebook.com'
            },
            timeout=15
        )
        
        match = re.search(r'(EAAG\w+)', response.text)
        if match:
            return match.group(1)
        return None
    except:
        return None

async def share_post_v1(session, cookie, token, post_id):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'cookie': cookie,
        'host': 'b-graph.facebook.com'
    }
    
    url = 'https://b-graph.facebook.com/me/feed?link=https://mbasic.facebook.com/' + post_id + '&published=0&access_token=' + token
    
    for attempt in range(3):
        try:
            async with session.post(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                data = await response.json()
                if 'id' in data:
                    return True, data
        except:
            pass
    
    return False, None

async def share_post_v2(session, token, post_id):
    url = 'https://graph.facebook.com/me/feed?link=https://facebook.com/' + post_id + '&published=0&access_token=' + token
    
    for attempt in range(3):
        try:
            async with session.post(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                data = await response.json()
                if 'id' in data:
                    return True, data
        except:
            pass
    
    return False, None

async def share_worker_v1(session, cookie, token, post_id, uid, display_mode):
    global success_count
    
    while True:
        try:
            success, _ = await share_post_v1(session, cookie, token, post_id)
            
            if success:
                async with lock:
                    success_count += 1
                    current_count = success_count
                
                if display_mode == 'minimal':
                    output = '\r ' + G('[V1 SUCCESS — ' + str(current_count) + ']') + ' | UID: ' + uid + '              '
                    sys.stdout.write(output)
                    sys.stdout.flush()
                else:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f" {G('[V1]')} {timestamp} | UID: {uid} | Total: {current_count}")
        except asyncio.CancelledError:
            break
        except:
            pass

async def share_worker_v2(session, token, post_id, uid, display_mode):
    global success_count_v2
    
    while True:
        try:
            success, _ = await share_post_v2(session, token, post_id)
            
            if success:
                async with lock:
                    success_count_v2 += 1
                    current_count = success_count_v2
                
                if display_mode == 'minimal':
                    output = '\r ' + G('[V2 SUCCESS — ' + str(current_count) + ']') + ' | UID: ' + uid + '              '
                    sys.stdout.write(output)
                    sys.stdout.flush()
                else:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f" {G('[V2]')} {timestamp} | UID: {uid} | Total: {current_count}")
        except asyncio.CancelledError:
            break
        except:
            pass

def select_display_mode():
    refresh_screen()
    print(f" {C('[SELECT DISPLAY MODE]')}")
    print(LINE)
    print(f" {W}[1]{RESET} {G('COUNTER MODE')} (Single line, good for mobile)")
    print(f" {W}[2]{RESET} {C('DETAILED MODE')} (Shows each share)")
    print(LINE)
    
    while True:
        choice = input(f" {W}[➤]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip()
        if choice == '1':
            return 'minimal'
        elif choice == '2':
            return 'detailed'

def select_cookies_for_sharing():
    show_loader("LOADING COOKIES")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load cookies')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        print(f" {R('[ERROR] No cookies found. Add cookies first.')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    refresh_screen()
    print(f" {C('[SELECT COOKIES FOR V1 SHARING]')}")
    print(LINE)
    print(f" {W}[ALL]{RESET} {G('USE ALL COOKIES')}")
    
    for i, cookie in enumerate(cookies, 1):
        print(f" {W}[{i}]{RESET} {M(cookie['name'])} (UID: {cookie['uid']})")
    
    print(LINE)
    selection = input(f" {W}[➤]{RESET} {C('Selection (ALL or 1,2,3)')} {W}➤{RESET} ").strip().upper()
    
    if not selection:
        return None
    
    if selection == 'ALL':
        return cookies
    
    selected = []
    for part in selection.replace(',', ' ').split():
        try:
            index = int(part) - 1
            if 0 <= index < len(cookies):
                selected.append(cookies[index])
        except:
            pass
    
    return selected if selected else None

def select_tokens_for_sharing():
    show_loader("LOADING TOKENS")
    
    status, response = api_request("GET", "/user/tokens")
    
    if status == 403:
        print(f" {R('[ERROR] MAX+ plan required for V2')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    if status != 200 or not response.get('success'):
        print(f" {R('[ERROR] Failed to load tokens')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    tokens = response.get('tokens', [])
    
    if not tokens:
        print(f" {R('[ERROR] No tokens found. Add tokens first.')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return None
    
    refresh_screen()
    print(f" {C('[SELECT TOKENS FOR V2 SHARING]')}")
    print(LINE)
    print(f" {W}[ALL]{RESET} {G('USE ALL TOKENS')}")
    
    for i, token in enumerate(tokens, 1):
        print(f" {W}[{i}]{RESET} {M(token['name'])} (UID: {token['uid']})")
    
    print(LINE)
    selection = input(f" {W}[➤]{RESET} {C('Selection (ALL or 1,2,3)')} {W}➤{RESET} ").strip().upper()
    
    if not selection:
        return None
    
    if selection == 'ALL':
        return tokens
    
    selected = []
    for part in selection.replace(',', ' ').split():
        try:
            index = int(part) - 1
            if 0 <= index < len(tokens):
                selected.append(tokens[index])
        except:
            pass
    
    return selected if selected else None

async def run_auto_share_v1(link, cookies):
    global success_count
    success_count = 0
    
    print(f" {C('[!] Converting cookies to EAAG tokens...')}")
    
    valid_accounts = []
    for cookie in cookies:
        token = convert_cookie_to_eaag(cookie['cookie'])
        if token:
            valid_accounts.append({
                'cookie': cookie['cookie'],
                'token': token,
                'uid': cookie['uid'],
                'name': cookie['name']
            })
            print(f" {G('✓')} {cookie['name']} - Token extracted")
        else:
            print(f" {R('✗')} {cookie['name']} - Failed to extract token")
    
    if not valid_accounts:
        print(f" {R('[ERROR] No valid accounts!')}")
        return
    
    post_id = extract_post_id(link)
    
    async with aiohttp.ClientSession() as session:
        if not post_id.isdigit():
            print(f" {G('[!] Extracting post ID from link...')}")
            post_id = await get_post_id_from_api(session, link)
            
            if not post_id:
                print(f" {R('[ERROR] Could not extract post ID')}")
                return
    
    print(f" {G('[!] Post ID:')} {C(post_id)}")
    
    display_mode = select_display_mode()
    
    refresh_screen()
    account_count = len(valid_accounts)
    print(f" {G('[V1 AUTO SHARE] Using ' + str(account_count) + ' accounts')}")
    print(f" {C('Post ID:')} {G(post_id)}")
    print(f" {C('Speed:')} {G('MAXIMUM')} | {C('Retries:')} {M('3 per share')}")
    print(LINE)
    print(f" {G('[!] Sharing started... Press Ctrl+C to stop')}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for account in valid_accounts:
            task = asyncio.create_task(
                share_worker_v1(session, account['cookie'], account['token'], post_id, account['uid'], display_mode)
            )
            tasks.append(task)
        
        try:
            await asyncio.gather(*tasks)
        except:
            for task in tasks:
                if not task.done():
                    task.cancel()

async def run_auto_share_v2(link, tokens):
    global success_count_v2
    success_count_v2 = 0
    
    post_id = extract_post_id(link)
    
    async with aiohttp.ClientSession() as session:
        if not post_id.isdigit():
            print(f" {G('[!] Extracting post ID from link...')}")
            post_id = await get_post_id_from_api(session, link)
            
            if not post_id:
                print(f" {R('[ERROR] Could not extract post ID')}")
                return
    
    print(f" {G('[!] Post ID:')} {C(post_id)}")
    
    display_mode = select_display_mode()
    
    refresh_screen()
    token_count = len(tokens)
    print(f" {G('[V2 AUTO SHARE] Using ' + str(token_count) + ' tokens')}")
    print(f" {C('Post ID:')} {G(post_id)}")
    print(f" {C('Speed:')} {G('MAXIMUM')} | {C('Retries:')} {M('3 per share')}")
    print(LINE)
    print(f" {G('[!] Sharing started... Press Ctrl+C to stop')}")
    print(LINE)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for token_data in tokens:
            task = asyncio.create_task(
                share_worker_v2(session, token_data['token'], post_id, token_data['uid'], display_mode)
            )
            tasks.append(task)
        
        try:
            await asyncio.gather(*tasks)
        except:
            for task in tasks:
                if not task.done():
                    task.cancel()

def auto_share_v1():
    refresh_screen()
    print(f" {C('[AUTO SHARE V1 - COOKIE/EAAG METHOD]')}")
    print(LINE)
    print(f" {G('• Post must be set to PUBLIC')}")
    print(f" {G('• Uses EAAG tokens extracted from cookies')}")
    print(f" {G('• Maximum speed with 3 retries per share')}")
    print(f" {G('• Press Ctrl+C to stop sharing')}")
    print(LINE)
    
    cookies = select_cookies_for_sharing()
    if not cookies:
        return
    
    refresh_screen()
    cookie_count = len(cookies)
    print(f" {G('[SELECTED] ' + str(cookie_count) + ' cookie(s)')}")
    print(LINE)
    
    link = input(f" {W}[➤]{RESET} {C('POST LINK OR ID')} {W}➤{RESET} ").strip()
    if not link:
        return
    
    try:
        asyncio.run(run_auto_share_v1(link, cookies))
    except KeyboardInterrupt:
        print(f"\n\n {C('[STOPPED]')} Total V1 shares: {G(str(success_count))}")
        
        if success_count > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count, "version": "v1"})
            print(f" {G('[!] Shares recorded to your account')}")
    except Exception as e:
        print(f" {R('[ERROR] ' + str(e))}")
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def auto_share_v2():
    if user_data and user_data.get('plan') != 'maxplus' and not user_data.get('isAdmin'):
        print(f" {R('[ERROR] MAX+ plan required for V2 sharing')}")
        input(f" {G('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(f" {C('[AUTO SHARE V2 - TOKEN METHOD]')}")
    print(LINE)
    print(f" {G('• Post must be set to PUBLIC')}")
    print(f" {G('• Uses direct Facebook access tokens')}")
    print(f" {G('• Maximum speed with 3 retries per share')}")
    print(f" {G('• Press Ctrl+C to stop sharing')}")
    print(LINE)
    
    tokens = select_tokens_for_sharing()
    if not tokens:
        return
    
    refresh_screen()
    token_count = len(tokens)
    print(f" {G('[SELECTED] ' + str(token_count) + ' token(s)')}")
    print(LINE)
    
    link = input(f" {W}[➤]{RESET} {C('POST LINK OR ID')} {W}➤{RESET} ").strip()
    if not link:
        return
    
    try:
        asyncio.run(run_auto_share_v2(link, tokens))
    except KeyboardInterrupt:
        print(f"\n\n {C('[STOPPED]')} Total V2 shares: {G(str(success_count_v2))}")
        
        if success_count_v2 > 0:
            api_request("POST", "/share/complete", {"totalShares": success_count_v2, "version": "v2"})
            print(f" {G('[!] Shares recorded to your account')}")
    except Exception as e:
        print(f" {R('[ERROR] ' + str(e))}")
    
    input(f"\n {G('[PRESS ENTER TO CONTINUE]')}")

def main():
    global user_token, user_data
    
    while True:
        refresh_screen()
        
        try:
            choice = input(f" {W}[➤]{RESET} {C('CHOICE')} {W}➤{RESET} ").strip().upper()
        except KeyboardInterrupt:
            print(f"\n {R('[!] Goodbye!')}")
            sys.exit(0)
        
        if not user_token:
            if choice in ['1', '01', 'A']:
                do_login()
            elif choice in ['2', '02', 'B']:
                do_register()
            elif choice in ['0', '00', 'X']:
                print(f" {R('[!] Goodbye!')}")
                sys.exit(0)
        
        elif user_data and user_data.get('isAdmin'):
            if choice in ['1', '01', 'A']:
                auto_share_v1()
            elif choice in ['2', '02', 'B']:
                auto_share_v2()
            elif choice in ['3', '03', 'C']:
                file_encryptor()
            elif choice in ['4', '04', 'D']:
                manage_cookies()
            elif choice in ['5', '05', 'E']:
                manage_tokens()
            elif choice in ['6', '06', 'F']:
                show_stats()
            elif choice in ['7', '07', 'G']:
                admin_panel()
            elif choice in ['0', '00', 'X']:
                user_token = None
                user_data = None
        
        elif user_data and user_data.get('plan') == 'maxplus':
            if choice in ['1', '01', 'A']:
                auto_share_v1()
            elif choice in ['2', '02', 'B']:
                auto_share_v2()
            elif choice in ['3', '03', 'C']:
                manage_cookies()
            elif choice in ['4', '04', 'D']:
                manage_tokens()
            elif choice in ['5', '05', 'E']:
                show_stats()
            elif choice in ['0', '00', 'X']:
                user_token = None
                user_data = None
        
        else:
            if choice in ['1', '01', 'A']:
                auto_share_v1()
            elif choice in ['2', '02', 'B']:
                manage_cookies()
            elif choice in ['3', '03', 'C']:
                show_stats()
            elif choice in ['0', '00', 'X']:
                user_token = None
                user_data = None

if __name__ == "__main__":
    main()
