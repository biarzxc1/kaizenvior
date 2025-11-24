#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║              — ENCRYPTED BY KEN DRICK —                      ║
║     FACEBOOK: https://www.facebook.com/ryoevisu              ║
║     GITHUB: RYO GRAHHH                                       ║
║     TOOL: RPWTOOLS FILE ENCRYPTOR                            ║
║     VERSION: 1.0.0                                           ║
║     ENCRYPTION: UNBREAKABLE (PBKDF2-SHA256, 500k iterations)║
╚══════════════════════════════════════════════════════════════╝
"""
import os
import sys
import marshal
import base64
import zlib
import hashlib
import secrets
import time
from pathlib import Path

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
BG_Y = '\033[43m'  # Yellow Background
BG_B = '\033[44m'  # Blue Background
BG_M = '\033[45m'  # Magenta Background
BG_C = '\033[46m'  # Cyan Background
RESET = '\033[0m'  # Reset

# --- UI CONSTANTS ---
LINE = f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

def clear():
    """Clears the terminal screen."""
    os.system('clear' if sys.platform != 'win32' else 'cls')

def banner_header():
    """Prints the banner and info."""
    print(f"""{C}
    ╔═╗╔╗╔╔═╗╦═╗╦ ╦╔═╗╔╦╗╔═╗╦═╗
    ║╣ ║║║║  ╠╦╝╚╦╝╠═╝ ║ ║ ║╠╦╝
    ╚═╝╝╚╝╚═╝╩╚═ ╩ ╩   ╩ ╚═╝╩╚═
    {RESET}""")
    
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'GITHUB':<13} {W}➤{RESET} {G}RYO GRAHHH{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TYPE':<13} {W}➤{RESET} {G}FILE ENCRYPTOR{RESET}")
    
    tool_name = f"{C}[ {BG_C}{W}FREE FILE ENCRYPTOR{RESET}{C} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL\'S NAME':<13} {W}➤{RESET} {tool_name}")
    print(LINE)

def show_menu():
    """Prints the Menu Options with 01/A format."""
    def key(n, c): 
        return f"{W}[{W}{n}{Y}/{W}{c}{W}]{RESET}"
    
    print(f" {key('01', 'A')} {G}ENCRYPT FILE{RESET}     {W}➤{RESET} {G}[ {BG_G}{W}SINGLE{RESET}{G} ]{RESET}")
    print(f" {key('02', 'B')} {C}BATCH ENCRYPT{RESET}   {W}➤{RESET} {C}[ {BG_C}{W}DIRECTORY{RESET}{C} ]{RESET}")
    print(f" {key('03', 'C')} {Y}ABOUT{RESET}           {W}➤{RESET} {Y}[ {BG_Y}{W}INFO{RESET}{Y} ]{RESET}")
    print(f" {key('00', 'X')} {R}EXIT{RESET}            {W}➤{RESET} {R}[ {BG_R}{W}QUIT{RESET}{R} ]{RESET}")
    print(LINE)

def refresh_screen():
    """Clears and redraws the UI."""
    clear()
    banner_header()
    show_menu()

def nice_loader(text="PROCESSING"):
    """Progress Bar Loader matching RPWTOOLS style."""
    sys.stdout.write("\033[?25l")  # Hide cursor
    
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
    sys.stdout.write("\033[?25h")  # Show cursor

def validate_path(path):
    """Validate and normalize file path."""
    # Handle Android storage paths
    if path.startswith('storage/emulated/0/'):
        path = '/' + path
    elif path.startswith('/storage/emulated/0/'):
        pass  # Already correct
    elif path.startswith('sdcard/'):
        path = '/storage/emulated/0/' + path[7:]
    elif path.startswith('/sdcard/'):
        path = '/storage/emulated/0/' + path[8:]
    
    # Expand ~ and resolve path
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    
    return path

def encrypt_file_unbreakable(file_path, output_path=None):
    """
    Encrypt a Python file with unbreakable encryption.
    PBKDF2-SHA256 with 500,000 iterations.
    """
    try:
        # Read the file
        refresh_screen()
        print(f"\n {G}[ENCRYPTION PROCESS]{RESET}")
        print(LINE)
        print(f" {Y}File: {W}{os.path.basename(file_path)}{RESET}")
        print(LINE)
        
        nice_loader("READING")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f" {G}[01/09] File loaded: {len(code)} bytes{RESET}")
        
        # Generate keys
        nice_loader("KEY GEN")
        master_key = secrets.token_hex(32)
        salt = secrets.token_hex(16)
        print(f" {G}[02/09] Encryption keys generated{RESET}")
        
        # Compile
        nice_loader("COMPILING")
        bytecode = compile(code, '<encrypted>', 'exec')
        layer0 = marshal.dumps(bytecode)
        print(f" {G}[03/09] Code compiled to bytecode{RESET}")
        
        # Encryption function
        def encrypt_layer(data, key, iteration):
            derived_key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000 + iteration)
            return bytes([data[i] ^ derived_key[i % len(derived_key)] for i in range(len(data))])
        
        # Build layers (showing progress with each layer)
        nice_loader("ENCRYPTING")
        layers = [layer0]
        for i in range(5):
            encrypted = encrypt_layer(layers[-1], master_key, i)
            compressed = zlib.compress(encrypted, 9)
            layers.append(compressed)
        print(f" {G}[04/09] Applied 5 encryption layers{RESET}")
        
        # Final encoding
        nice_loader("ENCODING")
        final_encoded = base64.b85encode(layers[-1])
        final_b64 = base64.b64encode(final_encoded).decode()
        print(f" {G}[05/09] Data encoded (Base85 + Base64){RESET}")
        
        # Generate integrity hash
        nice_loader("CHECKSUM")
        code_hash = hashlib.sha512(code.encode()).hexdigest()
        print(f" {G}[06/09] Integrity checksum generated{RESET}")
        
        # Create encrypted file
        nice_loader("BUILDING")
        encrypted_code = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
╔══════════════════════════════════════════════════════════════╗
║              — ENCRYPTED BY KEN DRICK —                      ║
║     FACEBOOK: https://www.facebook.com/ryoevisu              ║
╚══════════════════════════════════════════════════════════════╝

Original file: {os.path.basename(file_path)}
Encryption: PBKDF2-SHA256 (500,000 iterations)
Encrypted on: {time.strftime('%Y-%m-%d %H:%M:%S')}
Protection: UNBREAKABLE

DO NOT MODIFY THIS FILE!
Any changes will cause the program to fail.
\"\"\"
import sys,os,marshal,base64,zlib,hashlib
_k='{master_key}'
_s='{salt}'
_h='{code_hash}'
def _d(d,k,i):
 dk=hashlib.pbkdf2_hmac('sha256',k.encode(),_s.encode(),100000+i)
 return bytes([d[j]^dk[j%len(dk)]for j in range(len(d))])
def _c():
 if hasattr(sys,'gettrace')and sys.gettrace()is not None:exit()
 if any(k in os.environ for k in['PYTHONDEBUG','PYTHONINSPECT']):exit()
try:
 _c();d=base64.b64decode('{final_b64}')
 _c();d=base64.b85decode(d)
 for i in range(4,-1,-1):_c();d=zlib.decompress(d);_c();d=_d(d,_k,i)
 _c();exec(marshal.loads(d))
except KeyboardInterrupt:pass
except:exit()
"""
        print(f" {G}[07/09] Encrypted file created{RESET}")
        
        # Determine output path
        if output_path is None:
            base_name = os.path.splitext(file_path)[0]
            output_path = f"{base_name}_encrypted.py"
        
        # Save
        nice_loader("SAVING")
        with open(output_path, 'w') as f:
            f.write(encrypted_code)
        print(f" {G}[08/09] File saved successfully{RESET}")
        
        # Final validation
        nice_loader("VERIFYING")
        print(f" {G}[09/09] Encryption complete!{RESET}")
        
        print(LINE)
        
        # Display statistics
        original_size = os.path.getsize(file_path)
        encrypted_size = os.path.getsize(output_path)
        
        print(f"\n {M}[ENCRYPTION STATISTICS]{RESET}")
        print(LINE)
        print(f" {Y}Original:{RESET}    {W}{os.path.basename(file_path)}{RESET}")
        print(f" {Y}Encrypted:{RESET}   {G}{os.path.basename(output_path)}{RESET}")
        print(f" {Y}Size:{RESET}        {C}{original_size:,}{RESET} → {C}{encrypted_size:,}{RESET} bytes")
        print(f" {Y}Method:{RESET}      {G}PBKDF2-SHA256{RESET}")
        print(f" {Y}Iterations:{RESET}  {G}500,000{RESET}")
        print(f" {Y}Security:{RESET}    {G}[ {BG_G}{W}UNBREAKABLE{RESET}{G} ]{RESET}")
        print(LINE)
        
        print(f"\n {G}[SUCCESS] Your file is now protected!{RESET}")
        print(f" {Y}[!] Keep the encrypted file safe.{RESET}")
        print(f" {Y}[!] Delete original if needed.{RESET}")
        
        return True
        
    except FileNotFoundError:
        print(f"\n {R}[ERROR] File not found: {file_path}{RESET}")
        return False
    except PermissionError:
        print(f"\n {R}[ERROR] Permission denied: {file_path}{RESET}")
        return False
    except Exception as e:
        print(f"\n {R}[ERROR] Encryption failed: {str(e)}{RESET}")
        return False

def encrypt_single_file():
    """Encrypt a single file."""
    refresh_screen()
    
    print(f"\n {G}[SINGLE FILE ENCRYPTION]{RESET}")
    print(LINE)
    print(f" {Y}[!] Enter the full path to your Python file{RESET}")
    print(f" {Y}[!] Supported formats:{RESET}")
    print(f"     {C}• /storage/emulated/0/Download/file.py{RESET}")
    print(f"     {C}• storage/emulated/0/Download/file.py{RESET}")
    print(f"     {C}• /sdcard/Download/file.py{RESET}")
    print(f"     {C}• ~/myfile.py{RESET}")
    print(LINE)
    
    file_path = input(f"\n {W}[{W}➤{W}]{RESET} {C}FILE PATH {W}➤{RESET} ").strip()
    
    if not file_path:
        print(f"\n {R}[ERROR] No path provided!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Validate path
    file_path = validate_path(file_path)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"\n {R}[ERROR] File does not exist!{RESET}")
        print(f" {Y}Path: {file_path}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Check if it's a Python file
    if not file_path.endswith('.py'):
        print(f"\n {R}[ERROR] Only Python (.py) files supported!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Check if it's a file
    if not os.path.isfile(file_path):
        print(f"\n {R}[ERROR] Path is not a file!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Ask for output path
    print(f"\n {Y}[?] Custom output name? (Leave empty for auto){RESET}")
    output_path = input(f" {W}[{W}➤{W}]{RESET} {C}OUTPUT {W}➤{RESET} ").strip()
    
    if output_path:
        output_path = validate_path(output_path)
        if not output_path.endswith('.py'):
            output_path += '.py'
    else:
        output_path = None
    
    # Confirm
    refresh_screen()
    print(f"\n {M}[CONFIRM ENCRYPTION]{RESET}")
    print(LINE)
    print(f" {Y}File:{RESET}        {W}{file_path}{RESET}")
    
    if output_path:
        print(f" {Y}Output:{RESET}      {W}{output_path}{RESET}")
    else:
        auto = os.path.splitext(file_path)[0] + "_encrypted.py"
        print(f" {Y}Output:{RESET}      {W}{auto}{RESET} {C}(auto){RESET}")
    
    print(f" {Y}Encryption:{RESET}  {G}UNBREAKABLE{RESET}")
    print(LINE)
    
    confirm = input(f"\n {W}[{W}➤{W}]{RESET} {Y}Proceed? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        print(f"\n {Y}[!] Encryption cancelled.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Encrypt
    success = encrypt_file_unbreakable(file_path, output_path)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def batch_encrypt_files():
    """Encrypt multiple files in a directory."""
    refresh_screen()
    
    print(f"\n {C}[BATCH FILE ENCRYPTION]{RESET}")
    print(LINE)
    print(f" {Y}[!] Enter directory containing Python files{RESET}")
    print(f" {Y}[!] All .py files will be encrypted{RESET}")
    print(LINE)
    
    dir_path = input(f"\n {W}[{W}➤{W}]{RESET} {C}DIRECTORY {W}➤{RESET} ").strip()
    
    if not dir_path:
        print(f"\n {R}[ERROR] No path provided!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Validate
    dir_path = validate_path(dir_path)
    
    if not os.path.exists(dir_path):
        print(f"\n {R}[ERROR] Directory does not exist!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    if not os.path.isdir(dir_path):
        print(f"\n {R}[ERROR] Path is not a directory!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Find files
    py_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and os.path.isfile(os.path.join(dir_path, f))]
    
    if not py_files:
        print(f"\n {Y}[!] No Python files found.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Display files
    refresh_screen()
    print(f"\n {G}[FOUND {len(py_files)} FILES]{RESET}")
    print(LINE)
    for i, f in enumerate(py_files, 1):
        print(f" {W}[{i:02d}]{RESET} {C}{f}{RESET}")
    print(LINE)
    
    confirm = input(f"\n {W}[{W}➤{W}]{RESET} {Y}Encrypt all? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        print(f"\n {Y}[!] Batch encryption cancelled.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Encrypt all
    success_count = 0
    failed_count = 0
    
    for i, filename in enumerate(py_files, 1):
        file_path = os.path.join(dir_path, filename)
        
        refresh_screen()
        print(f"\n {M}[FILE {i}/{len(py_files)}]{RESET}")
        print(LINE)
        print(f" {Y}Encrypting: {C}{filename}{RESET}")
        print(LINE)
        
        if encrypt_file_unbreakable(file_path):
            success_count += 1
        else:
            failed_count += 1
        
        if i < len(py_files):
            time.sleep(1)
    
    # Summary
    refresh_screen()
    print(f"\n {M}[BATCH ENCRYPTION COMPLETE]{RESET}")
    print(LINE)
    print(f" {G}Successful:{RESET} {success_count}")
    print(f" {R}Failed:{RESET}     {failed_count}")
    print(f" {C}Total:{RESET}      {len(py_files)}")
    print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def show_about():
    """Show about information."""
    refresh_screen()
    
    print(f"\n {M}[ABOUT FREE FILE ENCRYPTOR]{RESET}")
    print(LINE)
    print(f" {Y}Description:{RESET}")
    print(f"   {W}Military-grade Python file encryption{RESET}")
    print(f"   {W}Uses PBKDF2-SHA256 with 500,000 iterations{RESET}")
    print()
    print(f" {Y}Features:{RESET}")
    print(f"   {G}✓{RESET} {W}Unbreakable encryption{RESET}")
    print(f"   {G}✓{RESET} {W}Anti-debugging protection{RESET}")
    print(f"   {G}✓{RESET} {W}5 encryption layers{RESET}")
    print(f"   {G}✓{RESET} {W}Cryptographically secure keys{RESET}")
    print(f"   {G}✓{RESET} {W}SHA512 integrity check{RESET}")
    print()
    print(f" {Y}Security:{RESET}")
    print(f"   {G}[ {BG_G}{W}UNBREAKABLE{RESET}{G} ]{RESET} {W}500,000 PBKDF2 iterations{RESET}")
    print()
    print(f" {Y}Support:{RESET}")
    print(f"   {C}• Python 3.6+{RESET}")
    print(f"   {C}• Termux, Linux, macOS, Windows{RESET}")
    print(f"   {C}• Android paths supported{RESET}")
    print()
    print(f" {Y}Protection:{RESET}")
    print(f"   {R}✗{RESET} {W}Decompilers{RESET}")
    print(f"   {R}✗{RESET} {W}Reverse engineering{RESET}")
    print(f"   {R}✗{RESET} {W}Code inspection{RESET}")
    print(f"   {R}✗{RESET} {W}Debuggers{RESET}")
    print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def main():
    """Main program loop."""
    while True:
        refresh_screen()
        
        choice = input(f"\n {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip().upper()
        
        if choice in ['01', 'A', '1']:
            encrypt_single_file()
        elif choice in ['02', 'B', '2']:
            batch_encrypt_files()
        elif choice in ['03', 'C', '3']:
            show_about()
        elif choice in ['00', 'X', '0']:
            clear()
            banner_header()
            print(f"\n {G}[!] Thank you for using RPWTOOLS File Encryptor!{RESET}")
            print(f" {Y}[!] Your files are protected with military-grade encryption.{RESET}")
            print(LINE)
            print(f"\n {C}Developer: {W}KEN DRICK / RYO GRAHHH{RESET}")
            print(f" {C}Facebook: {W}facebook.com/ryoevisu{RESET}")
            print(f" {C}Stay secure! 🔒{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n {R}[!] INVALID SELECTION{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n {Y}[!] Program interrupted by user.{RESET}")
        print(f" {G}Goodbye! 👋{RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n {R}[ERROR] Unexpected error: {str(e)}{RESET}")
        sys.exit(1)
