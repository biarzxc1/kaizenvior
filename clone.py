# -*- coding: utf-8 -*-
# Facebook Cookie Getter - M1 & M2 Methods
import os
import sys
import time
import uuid
import random
import requests
from random import randint as rr

# Suppress warnings
requests.urllib3.disable_warnings()

# Color codes
X = '\x1b[1;37m'
rad = '\x1b[38;5;196m'
G = '\x1b[38;5;46m'
Y = '\x1b[38;5;220m'
W = '\x1b[1;37m'
B = '\x1b[1;36m'

def clear():
    os.system('clear' if 'win' not in sys.platform else 'cls')

def linex():
    print('\x1b[38;5;48m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

def window1():
    """Generates random Windows User-Agent string."""
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {random.choice(range(6, 11))}.0; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.0 Safari/534.{aV}"
    
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {random.choice(range(6, 11))}.{random.choice(['0', '1'])}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{bz}"
    
    latest_build = rr(6000, 9000)
    latest_patch = rr(100, 200)
    C = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    
    return random.choice([A, B, C])

def banner():
    """Display banner."""
    clear()
    print("\033[1;31m" + "─" * 65 + "\033[0m")
    
    logo = r"""
░█████╗░░█████╗░░█████╗░██╗░░██╗██╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██║██╔════╝
██║░░╚═╝██║░░██║██║░░██║█████═╝░██║█████╗░░
██║░░██╗██║░░██║██║░░██║██╔═██╗░██║██╔══╝░░
╚█████╔╝╚█████╔╝╚█████╔╝██║░╚██╗██║███████╗
░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚══════╝

    ░██████╗░███████╗████████╗████████╗███████╗██████╗░
    ██╔════╝░██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
    ██║░░██╗░█████╗░░░░░██║░░░░░░██║░░░█████╗░░██████╔╝
    ██║░░╚██╗██╔══╝░░░░░██║░░░░░░██║░░░██╔══╝░░██╔══██╗
    ╚██████╔╝███████╗░░░██║░░░░░░██║░░░███████╗██║░░██║
    ░╚═════╝░╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
"""
    print("\033[1;36m" + logo + "\033[0m")
    print("\033[1;33m" + "─" * 65 + "\033[0m")
    print("\033[1;33mTool: \033[1;36mFacebook Cookie Extractor\033[0m")
    print("\033[1;33mVersion: \033[1;36m2.0\033[0m")
    print("\033[1;33mAuthor: \033[1;36mASIM\033[0m")
    print("\033[1;31m" + "─" * 65 + "\033[0m")

def save_cookie(email, password, cookie, method):
    """Save cookie to file."""
    try:
        with open('/sdcard/FB-COOKIES.txt', 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Email/ID: {email}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Method: {method}\n")
            f.write(f"Cookie: {cookie}\n")
            f.write(f"{'='*50}\n")
        return True
    except:
        try:
            with open('FB-COOKIES.txt', 'a') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Email/ID: {email}\n")
                f.write(f"Password: {password}\n")
                f.write(f"Method: {method}\n")
                f.write(f"Cookie: {cookie}\n")
                f.write(f"{'='*50}\n")
            return True
        except:
            return False

def extract_cookie(response_cookies):
    """Extract and format cookie from response."""
    cookie_parts = []
    for key, value in response_cookies.items():
        cookie_parts.append(f"{key}={value}")
    return "; ".join(cookie_parts)

def method_1(email, password):
    """Method 1 - Graph API Login."""
    try:
        session = requests.Session()
        
        data = {
            'adid': str(uuid.uuid4()),
            'format': 'json',
            'device_id': str(uuid.uuid4()),
            'cpl': 'true',
            'family_device_id': str(uuid.uuid4()),
            'credentials_type': 'device_based_login_password',
            'error_detail_type': 'button_with_disabled',
            'source': 'device_based_login',
            'email': str(email),
            'password': str(password),
            'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
            'generate_session_cookies': '1',
            'meta_inf_fbmeta': '',
            'advertiser_id': str(uuid.uuid4()),
            'currently_logged_in_userid': '0',
            'locale': 'en_US',
            'client_country_code': 'US',
            'method': 'auth.login',
            'fb_api_req_friendly_name': 'authenticate',
            'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
            'api_key': '882a8490361da98702bf97a021ddc14d'
        }
        
        headers = {
            'User-Agent': window1(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'graph.facebook.com',
            'X-FB-Net-HNI': str(rr(20000, 40000)),
            'X-FB-SIM-HNI': str(rr(20000, 40000)),
            'X-FB-Connection-Type': 'MOBILE.LTE',
            'X-Tigon-Is-Retry': 'False',
            'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
            'x-fb-device-group': '5120',
            'X-FB-Friendly-Name': 'ViewerReactionsMutation',
            'X-FB-Request-Analytics-Tags': 'graphservice',
            'X-FB-HTTP-Engine': 'Liger',
            'X-FB-Client-IP': 'True',
            'X-FB-Server-Cluster': 'True',
            'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
        }
        
        response = session.post(
            'https://b-graph.facebook.com/auth/login',
            data=data,
            headers=headers,
            allow_redirects=False
        )
        
        result = response.json()
        
        if 'session_key' in result:
            # Extract session cookies
            session_cookies = result.get('session_cookies', [])
            cookie_string = ""
            
            for cookie in session_cookies:
                cookie_string += f"{cookie.get('name')}={cookie.get('value')}; "
            
            # Also get cookies from response
            response_cookie = extract_cookie(response.cookies)
            
            if cookie_string:
                full_cookie = cookie_string.strip('; ')
            else:
                full_cookie = response_cookie
            
            return {
                'status': 'success',
                'cookie': full_cookie,
                'access_token': result.get('access_token', 'N/A'),
                'uid': result.get('uid', 'N/A'),
                'session_key': result.get('session_key', 'N/A')
            }
        elif 'error' in result:
            error_msg = result['error'].get('message', 'Unknown error')
            if 'checkpoint' in error_msg.lower() or 'www.facebook.com' in error_msg:
                return {'status': 'checkpoint', 'message': 'Account has checkpoint'}
            return {'status': 'failed', 'message': error_msg}
        else:
            return {'status': 'failed', 'message': 'Invalid credentials'}
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def method_2(email, password):
    """Method 2 - API Login."""
    try:
        session = requests.Session()
        
        headers = {
            'x-fb-connection-bandwidth': str(rr(20000000, 29999999)),
            'x-fb-sim-hni': str(rr(20000, 40000)),
            'x-fb-net-hni': str(rr(20000, 40000)),
            'x-fb-connection-quality': 'EXCELLENT',
            'x-fb-connection-type': 'cell.CTRadioAccessTechnologyHSDPA',
            'user-agent': window1(),
            'content-type': 'application/x-www-form-urlencoded',
            'x-fb-http-engine': 'Liger'
        }
        
        url = f"https://b-api.facebook.com/method/auth.login?format=json&email={str(email)}&password={str(password)}&credentials_type=device_based_login_password&generate_session_cookies=1&error_detail_type=button_with_disabled&source=device_based_login&meta_inf_fbmeta=%20&currently_logged_in_userid=0&method=GET&locale=en_US&client_country_code=US&fb_api_caller_class=com.facebook.fos.headersv2.fb4aorca.HeadersV2ConfigFetchRequestHandler&access_token=350685531728|62f8ce9f74b12f84c123cc23437a4a32&fb_api_req_friendly_name=authenticate&cpl=true"
        
        response = session.get(url, headers=headers)
        result = response.json()
        
        if 'session_key' in result or 'access_token' in result:
            # Extract session cookies
            session_cookies = result.get('session_cookies', [])
            cookie_string = ""
            
            for cookie in session_cookies:
                cookie_string += f"{cookie.get('name')}={cookie.get('value')}; "
            
            # Also get cookies from response
            response_cookie = extract_cookie(response.cookies)
            
            if cookie_string:
                full_cookie = cookie_string.strip('; ')
            else:
                full_cookie = response_cookie
            
            return {
                'status': 'success',
                'cookie': full_cookie,
                'access_token': result.get('access_token', 'N/A'),
                'uid': result.get('uid', 'N/A'),
                'session_key': result.get('session_key', 'N/A')
            }
        elif 'error' in result:
            error_msg = result['error'].get('error_msg', 'Unknown error')
            if 'checkpoint' in error_msg.lower():
                return {'status': 'checkpoint', 'message': 'Account has checkpoint'}
            return {'status': 'failed', 'message': error_msg}
        else:
            return {'status': 'failed', 'message': 'Invalid credentials'}
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def get_cookie():
    """Main cookie getter function."""
    banner()
    
    print(f"\n{G}[+] Enter Facebook Credentials{W}")
    linex()
    
    email = input(f"{Y}[?] Email/ID/Phone: {G}").strip()
    password = input(f"{Y}[?] Password: {G}").strip()
    
    if not email or not password:
        print(f"\n{rad}[!] Email and Password are required!{W}")
        time.sleep(2)
        return get_cookie()
    
    linex()
    print(f"\n{B}[*] Select Method:{W}")
    print(f"{Y}[1] Method 1 (Graph API)")
    print(f"{Y}[2] Method 2 (API)")
    print(f"{Y}[3] Try Both Methods")
    linex()
    
    choice = input(f"{Y}[?] Choose (1/2/3): {G}").strip()
    
    print(f"\n{B}[*] Processing...{W}\n")
    linex()
    
    if choice == '1':
        print(f"{G}[+] Trying Method 1...{W}")
        result = method_1(email, password)
        display_result(email, password, result, "Method 1")
        
    elif choice == '2':
        print(f"{G}[+] Trying Method 2...{W}")
        result = method_2(email, password)
        display_result(email, password, result, "Method 2")
        
    elif choice == '3':
        print(f"{G}[+] Trying Method 1...{W}")
        result1 = method_1(email, password)
        
        if result1['status'] == 'success':
            display_result(email, password, result1, "Method 1")
        else:
            print(f"{rad}[!] Method 1 Failed: {result1.get('message', 'Unknown error')}{W}")
            print(f"\n{G}[+] Trying Method 2...{W}")
            result2 = method_2(email, password)
            display_result(email, password, result2, "Method 2")
    else:
        print(f"{rad}[!] Invalid choice!{W}")
        time.sleep(2)
        return get_cookie()

def display_result(email, password, result, method):
    """Display the result."""
    linex()
    
    if result['status'] == 'success':
        print(f"\n{G}[✓] Login Successful!{W}")
        print(f"{G}[✓] Method: {method}{W}")
        linex()
        print(f"\n{B}Account Details:{W}")
        print(f"{Y}Email/ID: {G}{email}{W}")
        print(f"{Y}Password: {G}{password}{W}")
        print(f"{Y}UID: {G}{result.get('uid', 'N/A')}{W}")
        print(f"{Y}Access Token: {G}{result.get('access_token', 'N/A')[:50]}...{W}")
        linex()
        print(f"\n{G}[✓] Cookie:{W}")
        print(f"{B}{result['cookie']}{W}")
        linex()
        
        # Save to file
        if save_cookie(email, password, result['cookie'], method):
            try:
                print(f"\n{G}[✓] Cookie saved to: /sdcard/FB-COOKIES.txt{W}")
            except:
                print(f"\n{G}[✓] Cookie saved to: FB-COOKIES.txt{W}")
        else:
            print(f"\n{rad}[!] Failed to save cookie to file{W}")
            
    elif result['status'] == 'checkpoint':
        print(f"\n{Y}[!] Account Checkpoint!{W}")
        print(f"{Y}[!] {result['message']}{W}")
        
    elif result['status'] == 'failed':
        print(f"\n{rad}[✗] Login Failed!{W}")
        print(f"{rad}[!] {result['message']}{W}")
        
    else:
        print(f"\n{rad}[✗] Error Occurred!{W}")
        print(f"{rad}[!] {result.get('message', 'Unknown error')}{W}")
    
    linex()
    print(f"\n{Y}[?] Want to try another account? (y/n): {W}", end='')
    again = input().strip().lower()
    
    if again == 'y':
        get_cookie()
    else:
        print(f"\n{G}[✓] Thank you for using Cookie Getter!{W}\n")
        sys.exit()

def main_menu():
    """Main menu."""
    banner()
    
    print(f"\n{G}[+] Facebook Cookie Getter - Main Menu{W}")
    linex()
    print(f"{Y}[1] Get Cookie (Login)")
    print(f"{Y}[2] Exit")
    linex()
    
    choice = input(f"{Y}[?] Choose option: {G}").strip()
    
    if choice == '1':
        get_cookie()
    elif choice == '2':
        print(f"\n{G}[✓] Goodbye!{W}\n")
        sys.exit()
    else:
        print(f"\n{rad}[!] Invalid option!{W}")
        time.sleep(1)
        main_menu()

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{rad}[!] Interrupted by user!{W}\n")
        sys.exit()
    except Exception as e:
        print(f"\n{rad}[!] Error: {e}{W}\n")
        sys.exit()
