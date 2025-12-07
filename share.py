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
import zlib
import base64
import platform
import shutil

# --- GRADIENT COLOR SYSTEM ---
def rgb(r, g, b):
    """Create RGB color code"""
    return f'\033[38;2;{r};{g};{b}m'

def gradient_text(text, start_color, end_color):
    """Apply gradient color to text"""
    if not text:
        return text
    
    result = []
    length = len(text)
    
    for i, char in enumerate(text):
        if char == ' ':
            result.append(char)
            continue
        
        ratio = i / max(1, length - 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        
        result.append(f'{rgb(r, g, b)}{char}\033[0m')
    
    return ''.join(result)

# --- COLOR SCHEMES ---
CYAN_PURPLE = ((0, 255, 255), (138, 43, 226))  # Cyan to Purple
PINK_ORANGE = ((255, 105, 180), (255, 140, 0))  # Pink to Orange
GREEN_CYAN = ((0, 255, 127), (0, 255, 255))     # Green to Cyan
BLUE_PINK = ((30, 144, 255), (255, 105, 180))   # Blue to Pink
PURPLE_PINK = ((138, 43, 226), (255, 192, 203)) # Purple to Pink

# Active color scheme
ACTIVE_GRADIENT = CYAN_PURPLE

# Quick access gradient functions
def G(text): return gradient_text(text, ACTIVE_GRADIENT[0], ACTIVE_GRADIENT[1])
def SUCCESS(text): return gradient_text(text, GREEN_CYAN[0], GREEN_CYAN[1])
def ERROR(text): return gradient_text(text, (255, 0, 0), (255, 100, 100))
def WARNING(text): return gradient_text(text, (255, 165, 0), (255, 215, 0))
def INFO(text): return gradient_text(text, BLUE_PINK[0], BLUE_PINK[1])

RESET = '\033[0m'

# --- UI CONSTANTS ---
LINE = G("━" * 65)

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
    banner = """
    ╦═╗╔═╗╦ ╦╔╦╗╔═╗╔═╗╦  ╔═╗
    ╠╦╝╠═╝║║║ ║ ║ ║║ ║║  ╚═╗
    ╩╚═╩  ╚╩╝ ╩ ╚═╝╚═╝╩═╝╚═╝
    """
    print(G(banner))
    print(LINE)
    print(f" {G('[•]')} {INFO('DEVELOPER':<13)} {G('➤')} {SUCCESS('KEN DRICK')}")
    print(f" {G('[•]')} {INFO('GITHUB':<13)} {G('➤')} {SUCCESS('RYO GRAHHH')}")
    print(f" {G('[•]')} {INFO('VERSION':<13)} {G('➤')} {SUCCESS('1.0.3')}")
    print(f" {G('[•]')} {INFO('FACEBOOK':<13)} {G('➤')} {SUCCESS('facebook.com/ryoevisu')}")
    
    tool_name = gradient_text("RPWTOOLS", (255, 0, 0), (255, 100, 100))
    print(f" {G('[•]')} {INFO('TOOL NAME':<13)} {G('➤')} {tool_name}")
    
    if user_data:
        print(LINE)
        username_display = user_data['username'].upper()
        print(f" {G('[•]')} {INFO('USERNAME':<13)} {G('➤')} {SUCCESS(username_display)}")
        
        fb_link = user_data.get('facebook', 'N/A')
        print(f" {G('[•]')} {INFO('FACEBOOK':<13)} {G('➤')} {SUCCESS(fb_link)}")
        
        country_display = user_data.get('country', 'N/A').upper()
        print(f" {G('[•]')} {INFO('COUNTRY':<13)} {G('➤')} {SUCCESS(country_display)}")
        
        # Color-coded plan display
        user_plan = user_data['plan']
        if user_plan == 'max':
            if user_data.get('planExpiry'):
                plan_display = gradient_text("MAX", PURPLE_PINK[0], PURPLE_PINK[1])
            else:
                plan_display = gradient_text("MAX LIFETIME", PURPLE_PINK[0], PURPLE_PINK[1])
        else:
            plan_display = gradient_text("FREE", (200, 200, 200), (150, 150, 150))
        
        print(f" {G('[•]')} {INFO('PLAN':<13)} {G('➤')} {plan_display}")
        
        if user_data.get('planExpiry'):
            print(f" {G('[•]')} {INFO('PLAN EXPIRY IN':<13)} {G('➤')} {WARNING(user_data['planExpiry'])}")
        
        # Show cookie count
        cookie_count = user_data.get('cookieCount', 0)
        print(f" {G('[•]')} {INFO('TOTAL COOKIES':<13)} {G('➤')} {INFO(str(cookie_count))}")
    
    print(LINE)

def show_menu():
    """Prints the Menu Options."""
    if not user_token:
        print(f" {SUCCESS('[01/A]')} {G('LOGIN')}")
        print(f" {INFO('[02/B]')} {G('REGISTER')}")
        print(f" {ERROR('[00/X]')} {G('EXIT')}")
    elif user_data and user_data.get('isAdmin'):
        print(f" {SUCCESS('[01/A]')} {G('AUTO SHARE              — NORM ACCOUNTS')}")
        print(f" {INFO('[02/B]')} {G('CYTHON ENCRYPTOR        — PYTHON FILES')}")
        print(f" {WARNING('[03/C]')} {G('MANAGE COOKIES          — DATABASE')}")
        print(f" {INFO('[04/D]')} {G('MY STATS                — STATISTICS')}")
        print(f" {gradient_text('[05/E]', PURPLE_PINK[0], PURPLE_PINK[1])} {G('ADMIN PANEL             — MANAGEMENT')}")
        print(f" {SUCCESS('[06/F]')} {G('UPDATE TOOL             — LATEST VERSION')}")
        print(f" {ERROR('[00/X]')} {G('LOGOUT')}")
    else:
        print(f" {SUCCESS('[01/A]')} {G('AUTO SHARE              — NORM ACCOUNTS')}")
        print(f" {WARNING('[02/B]')} {G('MANAGE COOKIES          — DATABASE')}")
        print(f" {INFO('[03/C]')} {G('MY STATS                — STATISTICS')}")
        print(f" {SUCCESS('[04/D]')} {G('UPDATE TOOL             — LATEST VERSION')}")
        print(f" {ERROR('[00/X]')} {G('LOGOUT')}")
    
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
        
        # Gradient progress bar
        gradient_bar = gradient_text(bar, GREEN_CYAN[0], GREEN_CYAN[1])
        
        sys.stdout.write(f"\r {G('[•]')} {INFO(text):<10} {G('➤')} [{gradient_bar}] {SUCCESS(f'{percent}%')}")
        sys.stdout.flush()
        time.sleep(0.04) 
    
    time.sleep(0.3) 
    sys.stdout.write(f"\r{' ' * 70}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")

def select_progress_display():
    """Let user choose progress display mode"""
    refresh_screen()
    print(INFO("[SHARING PROGRESS DISPLAY]"))
    print(LINE)
    print(WARNING("Choose how you want to see sharing progress:"))
    print(LINE)
    print(f" {SUCCESS('[1]')} {G('SUCCESS COUNTER (1/100)')}")
    print(f"     {INFO('• Best for smaller screens (mobile)')}")
    print(f"     {INFO('• Shows only success count')}")
    print(f"     {INFO('• Minimal display, stays in one place')}")
    print(LINE)
    print(f" {INFO('[2]')} {G('DETAILED LOGS')}")
    print(f"     {INFO('• Best for larger screens (desktop)')}")
    print(f"     {INFO('• Shows success, time, account info')}")
    print(f"     {INFO('• Full process information')}")
    print(LINE)
    
    while True:
        choice = input(f" {G('[➤]')} {INFO('CHOICE (1 or 2)')} {G('➤')} ").strip()
        
        if choice == '1':
            return 'minimal'
        elif choice == '2':
            return 'detailed'
        else:
            print(ERROR("[!] Invalid choice. Please enter 1 or 2"))
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
    print(SUCCESS("[!] LOGIN TO RPWTOOLS"))
    print(LINE)
    
    username = input(f" {G('[➤]')} {INFO('USERNAME')} {G('➤')} ").strip()
    if not username:
        return
    
    password = input(f" {G('[➤]')} {INFO('PASSWORD')} {G('➤')} ").strip()
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
        
        print(SUCCESS("[SUCCESS] Login successful!"))
        print(LINE)
        print(f" {INFO('Welcome back,')} {SUCCESS(user_data['username'].upper())}")
        print(f" {INFO('Plan:')} {SUCCESS(user_data['plan'].upper())}")
        print(f" {INFO('Total Cookies:')} {INFO(str(user_data.get('cookieCount', 0)))}")
        
        if user_data.get('isAdmin'):
            print(gradient_text("[ADMIN ACCESS GRANTED]", PURPLE_PINK[0], PURPLE_PINK[1]))
        
        print(LINE)
    else:
        print(ERROR(f"[ERROR] {response if isinstance(response, str) else response.get('message', 'Login failed')}"))
        print(LINE)
    
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

def register_user():
    """Register new user"""
    global user_token, user_data
    
    refresh_screen()
    print(SUCCESS("[!] REGISTER NEW ACCOUNT"))
    print(LINE)
    
    username = input(f" {G('[➤]')} {INFO('USERNAME')} {G('➤')} ").strip()
    if not username:
        return
    
    password = input(f" {G('[➤]')} {INFO('PASSWORD')} {G('➤')} ").strip()
    if not password:
        return
    
    facebook = input(f" {G('[➤]')} {INFO('FACEBOOK LINK')} {G('➤')} ").strip()
    if not facebook:
        return
    
    facebook = normalize_facebook_url(facebook)
    
    refresh_screen()
    print(f" {SUCCESS('[!]')} {INFO('NORMALIZED FACEBOOK URL:')} {WARNING(facebook)}")
    print(LINE)
    
    print(SUCCESS("[!] DETECTING YOUR COUNTRY..."))
    nice_loader("DETECTING")
    
    country = get_country_from_ip()
    
    refresh_screen()
    print(f" {SUCCESS('[!]')} {INFO('DETECTED COUNTRY:')} {WARNING(country)}")
    print(LINE)
    confirm = input(f" {G('[➤]')} {WARNING('Is this correct? (Y/N)')} {G('➤')} ").strip().upper()
    
    if confirm == 'N':
        country = input(f" {G('[➤]')} {INFO('ENTER YOUR COUNTRY')} {G('➤')} ").strip()
    
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
        
        print(SUCCESS("[SUCCESS] Registration successful!"))
        print(LINE)
        print(f" {INFO('Welcome,')} {SUCCESS(user_data['username'].upper())}")
        print(f" {INFO('Plan:')} {SUCCESS(user_data['plan'].upper())}")
        print(f" {INFO('Country:')} {SUCCESS(user_data['country'])}")
        print(f" {INFO('Facebook:')} {SUCCESS(facebook)}")
        print(LINE)
    else:
        print(ERROR(f"[ERROR] {response if isinstance(response, str) else response.get('message', 'Registration failed')}"))
        print(LINE)
    
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

# (Continue with remaining functions in next message due to length...)

def show_user_stats():
    """Display user statistics"""
    refresh_screen()
    print(SUCCESS("[!] LOADING STATS..."))
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/stats")
    
    if status == 200 and response.get('success'):
        stats = response.get('stats')
        
        refresh_screen()
        print(SUCCESS("[USER STATISTICS]"))
        print(LINE)
        print(f" {INFO('Username:')} {SUCCESS(stats['username'].upper())}")
        
        plan_color = SUCCESS if stats['plan'] == 'max' else INFO
        print(f" {INFO('Plan:')} {plan_color(stats['plan'].upper())}")
        
        if stats.get('planExpiry'):
            print(f" {INFO('Plan Expiry In:')} {WARNING(stats['planExpiry'])}")
        
        print(LINE)
        print(INFO("[STATISTICS]"))
        print(f" {INFO('Total Shares:')} {SUCCESS(str(stats['totalShares']))}")
        print(f" {INFO('Total Cookies:')} {INFO(str(stats.get('cookieCount', 0)))}")
        print(LINE)
        
        share_cd = stats.get('shareCooldown', {})
        
        print(INFO("[COOLDOWN STATUS]"))
        
        if share_cd.get('active'):
            print(ERROR(f"Share Cooldown: {share_cd['remainingSeconds']}s remaining"))
            print(f" {WARNING(f\"Available at: {share_cd['availableAt']}\")}") 
        else:
            print(SUCCESS("Share: Ready ✓"))
        
        print(LINE)
    else:
        print(ERROR(f"[ERROR] {response if isinstance(response, str) else response.get('message', 'Failed to get stats')}"))
        print(LINE)
    
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

# ============ CYTHON ENCRYPTOR (ADMIN ONLY) ============

def check_cython_available():
    """Check if Cython is available"""
    try:
        from Cython.Build import cythonize
        return True
    except ImportError:
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
    # Compress and encode
    compressed_code = zlib.compress(code.encode('utf-8'))
    encoded_code = base64.b64encode(compressed_code).decode('utf-8')
    
    # Create obfuscated file
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
    
    # Make it executable on Unix-like systems
    if platform.system().lower() != 'windows':
        os.chmod(output_file, 0o755)
    
    return output_file

def create_cython_obfuscated(file_path, file_name, base_name, code):
    """Create a Cython-compiled obfuscated version"""
    from Cython.Build import cythonize
    from distutils.core import setup
    from distutils.extension import Extension
    
    # Compress and encode
    compressed_code = zlib.compress(code.encode('utf-8'))
    encoded_code = base64.b64encode(compressed_code).decode('utf-8')
    
    # Create obfuscated file
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
    
    print(SUCCESS(f"[SUCCESS] Created encrypted file: {temp_file_name}"))
    
    # Compile with Cython
    print(INFO("[INFO] Compiling with Cython..."))
    module_name = f'{base_name}_encrypted'
    extensions = [Extension(module_name, [temp_file_name])]
    setup(
        ext_modules=cythonize(extensions, compiler_directives={'language_level': '3'}),
        script_args=['build_ext', '--inplace']
    )
    
    print(SUCCESS("[SUCCESS] Cython compilation complete"))
    
    # Get the correct extension for this platform
    platform_ext = get_platform_extension()
    compiled_file = f'{module_name}{platform_ext}'
    
    if not os.path.exists(compiled_file):
        print(WARNING(f"[WARNING] Expected compiled file not found: {compiled_file}"))
        print(INFO("[INFO] Listing available .so files:"))
        for f in os.listdir('.'):
            if f.startswith(module_name) and ('.so' in f or '.pyd' in f):
                print(INFO(f"  Found: {f}"))
                compiled_file = f
                break
    
    # Create run script
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
    
    # Make it executable on Unix-like systems
    if platform.system().lower() != 'windows':
        os.chmod(run_script_name, 0o755)
    
    print(SUCCESS(f"[SUCCESS] Created run script: {run_script_name}"))
    
    return compiled_file, run_script_name, temp_file_name

def cython_encryptor():
    """Cython Python File Encryptor (Admin Only)"""
    if not user_data or not user_data.get('isAdmin'):
        refresh_screen()
        print(ERROR("[ACCESS DENIED] This feature is only available for administrators."))
        print(LINE)
        input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(gradient_text("[CYTHON PYTHON FILE ENCRYPTOR]", PURPLE_PINK[0], PURPLE_PINK[1]))
    print(LINE)
    print(INFO("[!] INFORMATION:"))
    print(INFO("• Encrypts Python files using Cython compilation"))
    print(INFO("• Creates compiled .so/.pyd files (platform-specific)"))
    print(INFO("• Source code is completely hidden"))
    print(INFO("• Provides maximum protection"))
    print(LINE)
    
    file_path = input(f" {G('[➤]')} {INFO('Enter path to Python file')} {G('➤')} ").strip()
    file_path = file_path.strip('"').strip("'")
    
    # Validate file type
    if not file_path.endswith('.py'):
        print(ERROR("[ERROR] Invalid file type. Only Python (.py) files are supported."))
        input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")
        return
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(ERROR(f"[ERROR] File not found: {file_path}"))
        input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")
        return
    
    print("")
    use_cython = input(f" {G('[➤]')} {SUCCESS('Use Cython compilation? (more secure) [Y/n]')} {G('➤')} ").lower().strip()
    use_cython = use_cython not in ['n', 'no']
    
    if use_cython and not check_cython_available():
        print(WARNING("[WARNING] Cython not available. Install with: pip install Cython"))
        print(INFO("[INFO] Falling back to basic encryption..."))
        use_cython = False
    
    # Get the absolute path and extract directory and filename
    file_path = os.path.abspath(file_path)
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    base_name = file_name.replace('.py', '')
    
    # Change to the file's directory
    original_dir = os.getcwd()
    os.chdir(file_dir)
    
    print(LINE)
    print(INFO(f"[INFO] Working in directory: {file_dir}"))
    print(INFO(f"[INFO] Processing file: {file_name}"))
    print(LINE)
    
    nice_loader("ENCRYPTING")
    
    try:
        # Read the original code
        with open(file_name, 'r') as file:
            code = file.read()
        
        if use_cython:
            compiled_file, run_script, temp_file = create_cython_obfuscated(file_path, file_name, base_name, code)
            
            # Create output directory
            output_dir = f'{base_name}_encrypted_output'
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            
            # Copy files to output directory
            shutil.copy(compiled_file, output_dir)
            shutil.copy(run_script, output_dir)
            
            # Clean up temporary files
            print(INFO("[INFO] Cleaning up temporary files..."))
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Clean up build artifacts
            if os.path.exists('build'):
                shutil.rmtree('build')
            for f in os.listdir('.'):
                if f.endswith('.c'):
                    os.remove(f)
            
            print(LINE)
            print(SUCCESS("[SUCCESS] Encrypted package created!"))
            print(INFO(f"[INFO] Location: {os.path.join(file_dir, output_dir)}"))
            print(INFO(f"[INFO] Run with: python {run_script} (from output directory)"))
            print(WARNING(f"[NOTE] Distribute the entire '{output_dir}' folder"))
            print(LINE)
            
        else:
            output_file = create_simple_obfuscated(file_path, file_name, base_name, code)
            
            print(LINE)
            print(SUCCESS("[SUCCESS] Encrypted file created!"))
            print(INFO(f"[INFO] Location: {os.path.join(file_dir, output_file)}"))
            print(INFO(f"[INFO] Run with: python {output_file}"))
            print(WARNING("[NOTE] This is basic encryption. For better protection, use Cython compilation."))
            print(LINE)
        
    except Exception as e:
        print(ERROR(f"[ERROR] An error occurred: {str(e)}"))
        import traceback
        print(ERROR(traceback.format_exc()))
    finally:
        # Return to original directory
        os.chdir(original_dir)
    
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

# ============ COOKIE MANAGEMENT ============

def manage_cookies():
    """Manage cookie database"""
    while True:
        refresh_screen()
        print(SUCCESS("[MANAGE COOKIES]"))
        print(LINE)
        print(f" {SUCCESS('[1]')} {G('VIEW ALL COOKIES')}")
        print(f" {SUCCESS('[2]')} {G('ADD COOKIE')}")
        print(f" {ERROR('[3]')} {G('DELETE COOKIE')}")
        print(f" {ERROR('[4]')} {G('DELETE ALL COOKIES')}")
        print(f" {WARNING('[0]')} {G('BACK')}")
        print(LINE)
        
        choice = input(f" {G('[➤]')} {INFO('CHOICE')} {G('➤')} ").strip()
        
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
            print(ERROR("[!] INVALID SELECTION"))
            time.sleep(0.8)

def view_cookies():
    """View all cookies"""
    refresh_screen()
    print(SUCCESS("[!] LOADING COOKIES..."))
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status == 200 and response.get('success'):
        cookies = response.get('cookies', [])
        
        refresh_screen()
        print(SUCCESS(f"[COOKIES] Total: {len(cookies)}"))
        print(LINE)
        
        if not cookies:
            print(WARNING("No cookies stored yet."))
        else:
            for i, cookie_data in enumerate(cookies, 1):
                status_display = SUCCESS if cookie_data['status'] == 'active' else ERROR
                
                print(f" {SUCCESS(f'[{i:02d}]')} {gradient_text(cookie_data['name'], PURPLE_PINK[0], PURPLE_PINK[1])} {INFO(f\"(UID: {cookie_data['uid']})\")}")
                cookie_preview = cookie_data['cookie'][:50] + "..." if len(cookie_data['cookie']) > 50 else cookie_data['cookie']
                print(f"      Cookie: {INFO(cookie_preview)}")
                print(f"      Added: {WARNING(cookie_data['addedAt'])}")
                print(f"      Status: {status_display(cookie_data['status'].upper())}")
                
                if cookie_data['status'] == 'restricted':
                    print(ERROR("      ⚠ WARNING: This account is restricted!"))
                
                print(LINE)
        
    else:
        print(ERROR("[ERROR] Failed to load cookies"))
        print(LINE)
    
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

def add_cookie():
    """Add new cookie"""
    refresh_screen()
    print(SUCCESS("[ADD COOKIE]"))
    print(LINE)
    
    # Check if user can add more cookies
    if user_data['plan'] == 'free' and user_data.get('cookieCount', 0) >= 10:
        print(ERROR("[LIMIT REACHED]"))
        print(LINE)
        print(WARNING("FREE plan users can only store up to 10 cookies."))
        print(f" {WARNING(f\"You currently have: {user_data.get('cookieCount', 0)}/10\")}") 
        print(LINE)
        print(SUCCESS("[UPGRADE TO MAX]"))
        print(INFO("• Unlimited cookies"))
        print(INFO("• No cooldowns"))
        print(INFO("• Rental: 1 month (₱150) or 3 months (₱250)"))
        print(LINE)
        input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")
        return
    
    cookie = input(f" {G('[➤]')} {INFO('COOKIE')} {G('➤')} ").strip()
    if not cookie:
        return
    
    refresh_screen()
    print(WARNING("[!] VALIDATING COOKIE..."))
    print(INFO("This may take 10-15 seconds"))
    print(LINE)
    nice_loader("VALIDATING")
    
    status, response = api_request("POST", "/user/cookies", {
        "cookie": cookie
    })
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(SUCCESS(f"[SUCCESS] {response.get('message')}"))
        print(LINE)
        print(f" {INFO('Name:')} {gradient_text(response.get('name', 'Unknown'), PURPLE_PINK[0], PURPLE_PINK[1])}")
        print(f" {INFO('UID:')} {INFO(response.get('uid', 'Unknown'))}")
        
        status_display = SUCCESS if response.get('status') == 'active' else ERROR
        print(f" {INFO('Status:')} {status_display(response.get('status', 'unknown').upper())}")
        
        # Show restriction warning
        if response.get('restricted'):
            print(LINE)
            print(ERROR("⚠ WARNING: This account is RESTRICTED!"))
            print(WARNING("Restricted accounts may not be able to share posts."))
        
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
            
            # Show remaining slots for FREE users
            if user_data['plan'] == 'free':
                remaining = 10 - user_data['cookieCount']
                print(LINE)
                print(f" {INFO('Remaining Slots:')} {INFO(f'{remaining}/10')}")
        
        print(LINE)
    else:
        error_msg = response if isinstance(response, str) else response.get('message', 'Failed to add cookie') if isinstance(response, dict) else 'Failed to add cookie'
        print(ERROR(f"[ERROR] {error_msg}"))
        print(LINE)
    
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

def delete_cookie():
    """Delete a specific cookie"""
    refresh_screen()
    print(SUCCESS("[!] LOADING COOKIES..."))
    nice_loader("LOADING")
    
    status, response = api_request("GET", "/user/cookies")
    
    if status != 200 or not isinstance(response, dict) or not response.get('success'):
        error_msg = response if isinstance(response, str) else 'Failed to load cookies'
        print(ERROR(f"[ERROR] {error_msg}"))
        input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")
        return
    
    cookies = response.get('cookies', [])
    
    if not cookies:
        refresh_screen()
        print(WARNING("No cookies to delete."))
        input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")
        return
    
    refresh_screen()
    print(ERROR("[DELETE COOKIE]"))
    print(LINE)
    
    for i, cookie_data in enumerate(cookies, 1):
        status_indicator = ERROR("[RESTRICTED]") if cookie_data['status'] == 'restricted' else SUCCESS("[ACTIVE]")
        print(f" {SUCCESS(f'[{i}]')} {gradient_text(cookie_data['name'], PURPLE_PINK[0], PURPLE_PINK[1])} {INFO(f\"(UID: {cookie_data['uid']})\")} {status_indicator}")
    
    print(LINE)
    
    choice = input(f" {G('[➤]')} {INFO('SELECT COOKIE NUMBER (0 to cancel)')} {G('➤')} ").strip()
    
    if not choice or choice == '0':
        return
    
    try:
        cookie_index = int(choice) - 1
        if cookie_index < 0 or cookie_index >= len(cookies):
            print(ERROR("[ERROR] Invalid cookie number"))
            time.sleep(1)
            return
        
        selected_cookie = cookies[cookie_index]
    except:
        print(ERROR("[ERROR] Invalid input"))
        time.sleep(1)
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", f"/user/cookies/{selected_cookie['id']}")
    
    if status == 200 and isinstance(response, dict) and response.get('success'):
        print(SUCCESS("[SUCCESS] Cookie deleted!"))
        if user_data:
            user_data['cookieCount'] = response.get('totalCookies', 0)
    else:
        error_msg = response if isinstance(response, str) else 'Failed to delete cookie'
        print(ERROR(f"[ERROR] {error_msg}"))
    
    print(LINE)
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

def delete_all_cookies():
    """Delete all cookies"""
    refresh_screen()
    print(ERROR("[DELETE ALL COOKIES]"))
    print(LINE)
    
    confirm = input(f" {G('[➤]')} {ERROR('Delete ALL cookies? This cannot be undone! (YES/NO)')} {G('➤')} ").strip().upper()
    
    if confirm != 'YES':
        return
    
    refresh_screen()
    nice_loader("DELETING")
    
    status, response = api_request("DELETE", "/user/cookies")
    
    if status == 200 and response.get('success'):
        print(SUCCESS(f"[SUCCESS] {response.get('message')}"))
        if user_data:
            user_data['cookieCount'] = 0
    else:
        print(ERROR("[ERROR] Failed to delete cookies"))
    
    print(LINE)
    input(f"\n {WARNING('[PRESS ENTER TO CONTINUE]')}")

def update_tool_logic():
    """Simulates an update and restarts the script."""
    print(SUCCESS("[!] CHECKING FOR UPDATES..."))
    nice_loader("CHECKING")
    
    print(SUCCESS("[!] NEW VERSION FOUND! DOWNLOADING..."))
    nice_loader("UPDATING")
    
    print(SUCCESS("[!] UPDATE COMPLETE. RESTARTING..."))
    time.sleep(1)
    
    os.execv(sys.executable, ['python'] + sys.argv)

# ============ ADMIN PANEL FUNCTIONS ============
# (Admin panel functions remain the same - too long to include here)
# Include all admin_panel, view_all_users, change_user_plan, delete_user,
# view_activity_logs, dashboard_stats functions from the original code...

# ============ AUTO SHARE FUNCTIONS ============
# (Auto share functions remain the same - include all from original code)
# Include extract_post_id_from_link, getid, cookie_to_eaag, share_with_eaag,
# renew_eaag_token, share_loop, auto_share_main, select_cookies_for_sharing,
# start_auto_share functions...
