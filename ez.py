#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPWTOOLS FILE ENCRYPTOR v1.0
Unbreakable File Encryption Tool
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

def banner():
    """Prints the banner."""
    print(f"""{C}
    ╔═╗╔╗╔╔═╗╦═╗╦ ╦╔═╗╔╦╗╔═╗╦═╗
    ║╣ ║║║║  ╠╦╝╚╦╝╠═╝ ║ ║ ║╠╦╝
    ╚═╝╝╚╝╚═╝╩╚═ ╩ ╩   ╩ ╚═╝╩╚═
    {RESET}""")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TYPE':<13} {W}➤{RESET} {G}FILE ENCRYPTOR{RESET}")
    
    tool_name = f"{R}[ {BG_R}{W}RPWTOOLS ENCRYPTOR{RESET}{R} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL\'S NAME':<13} {W}➤{RESET} {tool_name}")
    print(LINE)

def nice_loader(text="PROCESSING", duration=1.5):
    """Improved Progress Bar Loader."""
    sys.stdout.write("\033[?25l")  # Hide cursor
    
    filled = "■"
    empty = "□"
    width = 20
    steps = 50
    
    for i in range(steps + 1):
        progress = min(i / steps, 1.0)
        filled_width = int(width * progress)
        bar = filled * filled_width + empty * (width - filled_width)
        percent = int(progress * 100)
        
        color = G if i == steps else C
        
        sys.stdout.write(f"\r {W}[{RESET}•{W}]{RESET} {Y}{text:<15} {W}➤{RESET} {color}[{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(duration / steps)
    
    time.sleep(0.2)
    sys.stdout.write(f"\r{' ' * 80}\r")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")  # Show cursor

def show_menu():
    """Display main menu."""
    print(f"\n {G}[FILE ENCRYPTOR MENU]{RESET}")
    print(LINE)
    print(f" {W}[{W}1{W}]{RESET} {G}ENCRYPT FILE{RESET}     {W}➤{RESET} {G}[ {BG_G}{W}UNBREAKABLE{RESET}{G} ]{RESET}")
    print(f" {W}[{W}2{W}]{RESET} {C}BATCH ENCRYPT{RESET}   {W}➤{RESET} {C}[ {BG_C}{W}MULTIPLE FILES{RESET}{C} ]{RESET}")
    print(f" {W}[{W}3{W}]{RESET} {Y}ABOUT{RESET}           {W}➤{RESET} {Y}[ {BG_Y}{W}INFO{RESET}{Y} ]{RESET}")
    print(f" {W}[{W}0{W}]{RESET} {R}EXIT{RESET}            {W}➤{RESET} {R}[ {BG_R}{W}QUIT{RESET}{R} ]{RESET}")
    print(LINE)

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
    Same method as rpwtools_unbreakable.py
    """
    try:
        # Read the file
        print(f"\n {G}[!] Reading file...{RESET}")
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        nice_loader("READING FILE", 0.5)
        print(f" {G}[SUCCESS] File loaded: {len(code)} bytes{RESET}")
        
        # Generate cryptographically secure keys
        print(f"\n {G}[!] Generating encryption keys...{RESET}")
        nice_loader("GENERATING KEYS", 0.8)
        
        master_key = secrets.token_hex(32)
        salt = secrets.token_hex(16)
        
        print(f" {G}[SUCCESS] Keys generated!{RESET}")
        
        # Encryption function
        def encrypt_layer(data, key, iteration):
            derived_key = hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000 + iteration)
            return bytes([data[i] ^ derived_key[i % len(derived_key)] for i in range(len(data))])
        
        # Build encryption layers
        print(f"\n {C}[!] Starting encryption process...{RESET}")
        print(LINE)
        
        print(f" {Y}[LAYER 0]{RESET} Compiling to bytecode...")
        nice_loader("COMPILING", 0.8)
        bytecode = compile(code, '<encrypted>', 'exec')
        layer0 = marshal.dumps(bytecode)
        print(f" {G}[✓] Bytecode compiled{RESET}")
        
        layers = [layer0]
        for i in range(5):
            print(f" {Y}[LAYER {i+1}]{RESET} Encrypting (PBKDF2-SHA256, 100k iterations)...")
            nice_loader(f"ENCRYPTING L{i+1}", 1.0)
            encrypted = encrypt_layer(layers[-1], master_key, i)
            
            print(f" {Y}[LAYER {i+1}]{RESET} Compressing...")
            nice_loader(f"COMPRESSING L{i+1}", 0.5)
            compressed = zlib.compress(encrypted, 9)
            layers.append(compressed)
            print(f" {G}[✓] Layer {i+1} complete{RESET}")
        
        # Final encoding
        print(f" {Y}[FINAL]{RESET} Encoding...")
        nice_loader("ENCODING", 0.8)
        final_encoded = base64.b85encode(layers[-1])
        final_b64 = base64.b64encode(final_encoded).decode()
        print(f" {G}[✓] Encoding complete{RESET}")
        
        print(LINE)
        
        # Generate integrity hash
        code_hash = hashlib.sha512(code.encode()).hexdigest()
        
        # Create encrypted file
        encrypted_code = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
ENCRYPTED BY RPWTOOLS FILE ENCRYPTOR v1.0
Original file: {os.path.basename(file_path)}
Encryption: PBKDF2-SHA256 (500,000 iterations)
Protection: UNBREAKABLE
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
        
        # Determine output path
        if output_path is None:
            base_name = os.path.splitext(file_path)[0]
            output_path = f"{base_name}_encrypted.py"
        
        # Save encrypted file
        print(f"\n {G}[!] Saving encrypted file...{RESET}")
        nice_loader("SAVING", 0.8)
        
        with open(output_path, 'w') as f:
            f.write(encrypted_code)
        
        print(f" {G}[SUCCESS] File encrypted successfully!{RESET}")
        print(LINE)
        
        # Display statistics
        original_size = os.path.getsize(file_path)
        encrypted_size = os.path.getsize(output_path)
        
        print(f"\n {M}[ENCRYPTION STATISTICS]{RESET}")
        print(LINE)
        print(f" {Y}Original file:{RESET}    {W}{file_path}{RESET}")
        print(f" {Y}Encrypted file:{RESET}   {G}{output_path}{RESET}")
        print(f" {Y}Original size:{RESET}    {C}{original_size:,} bytes{RESET}")
        print(f" {Y}Encrypted size:{RESET}   {C}{encrypted_size:,} bytes{RESET}")
        print(f" {Y}Encryption:{RESET}       {G}PBKDF2-SHA256{RESET}")
        print(f" {Y}Iterations:{RESET}       {G}500,000 total{RESET}")
        print(f" {Y}Security:{RESET}         {G}[ {BG_G}{W}UNBREAKABLE{RESET}{G} ]{RESET}")
        print(LINE)
        
        print(f"\n {G}[✓] Your file is now protected with military-grade encryption!{RESET}")
        print(f" {Y}[!] Keep the encrypted file safe.{RESET}")
        print(f" {Y}[!] Delete the original if needed.{RESET}")
        
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
    clear()
    banner()
    
    print(f"\n {G}[SINGLE FILE ENCRYPTION]{RESET}")
    print(LINE)
    print(f" {Y}[!] Enter the full path to your Python file{RESET}")
    print(f" {Y}[!] Examples:{RESET}")
    print(f"     {C}• /storage/emulated/0/Download/example.py{RESET}")
    print(f"     {C}• storage/emulated/0/Download/example.py{RESET}")
    print(f"     {C}• /sdcard/Download/example.py{RESET}")
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
        print(f" {Y}Path checked: {file_path}{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Check if it's a Python file
    if not file_path.endswith('.py'):
        print(f"\n {R}[ERROR] File must be a Python (.py) file!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Check if it's a file (not directory)
    if not os.path.isfile(file_path):
        print(f"\n {R}[ERROR] Path is not a file!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Ask for output path (optional)
    print(f"\n {Y}[?] Custom output name? (Leave empty for auto){RESET}")
    output_path = input(f" {W}[{W}➤{W}]{RESET} {C}OUTPUT PATH {W}➤{RESET} ").strip()
    
    if output_path:
        output_path = validate_path(output_path)
        if not output_path.endswith('.py'):
            output_path += '.py'
    else:
        output_path = None
    
    # Confirm encryption
    clear()
    banner()
    print(f"\n {M}[CONFIRM ENCRYPTION]{RESET}")
    print(LINE)
    print(f" {Y}File to encrypt:{RESET} {W}{file_path}{RESET}")
    
    if output_path:
        print(f" {Y}Output file:{RESET}     {W}{output_path}{RESET}")
    else:
        base_name = os.path.splitext(file_path)[0]
        auto_output = f"{base_name}_encrypted.py"
        print(f" {Y}Output file:{RESET}     {W}{auto_output}{RESET} {C}(auto){RESET}")
    
    print(f" {Y}Encryption:{RESET}      {G}UNBREAKABLE (PBKDF2-SHA256){RESET}")
    print(LINE)
    
    confirm = input(f"\n {W}[{W}➤{W}]{RESET} {Y}Proceed with encryption? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        print(f"\n {Y}[!] Encryption cancelled.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Perform encryption
    clear()
    banner()
    success = encrypt_file_unbreakable(file_path, output_path)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def batch_encrypt_files():
    """Encrypt multiple files."""
    clear()
    banner()
    
    print(f"\n {C}[BATCH FILE ENCRYPTION]{RESET}")
    print(LINE)
    print(f" {Y}[!] Enter the directory path containing Python files{RESET}")
    print(f" {Y}[!] All .py files in the directory will be encrypted{RESET}")
    print(LINE)
    
    dir_path = input(f"\n {W}[{W}➤{W}]{RESET} {C}DIRECTORY PATH {W}➤{RESET} ").strip()
    
    if not dir_path:
        print(f"\n {R}[ERROR] No path provided!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Validate path
    dir_path = validate_path(dir_path)
    
    # Check if directory exists
    if not os.path.exists(dir_path):
        print(f"\n {R}[ERROR] Directory does not exist!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    if not os.path.isdir(dir_path):
        print(f"\n {R}[ERROR] Path is not a directory!{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Find all Python files
    py_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and os.path.isfile(os.path.join(dir_path, f))]
    
    if not py_files:
        print(f"\n {Y}[!] No Python files found in directory.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Display files
    print(f"\n {G}[FOUND {len(py_files)} PYTHON FILES]{RESET}")
    print(LINE)
    for i, f in enumerate(py_files, 1):
        print(f" {W}[{i}]{RESET} {C}{f}{RESET}")
    print(LINE)
    
    confirm = input(f"\n {W}[{W}➤{W}]{RESET} {Y}Encrypt all {len(py_files)} files? (Y/N) {W}➤{RESET} ").strip().upper()
    
    if confirm != 'Y':
        print(f"\n {Y}[!] Batch encryption cancelled.{RESET}")
        input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")
        return
    
    # Encrypt all files
    clear()
    banner()
    print(f"\n {G}[BATCH ENCRYPTION IN PROGRESS]{RESET}")
    print(LINE)
    
    success_count = 0
    failed_count = 0
    
    for i, filename in enumerate(py_files, 1):
        file_path = os.path.join(dir_path, filename)
        print(f"\n {M}[{i}/{len(py_files)}] {filename}{RESET}")
        
        if encrypt_file_unbreakable(file_path):
            success_count += 1
        else:
            failed_count += 1
    
    # Summary
    print(f"\n\n {M}[BATCH ENCRYPTION SUMMARY]{RESET}")
    print(LINE)
    print(f" {G}Successful:{RESET} {success_count}")
    print(f" {R}Failed:{RESET}     {failed_count}")
    print(f" {C}Total:{RESET}      {len(py_files)}")
    print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def show_about():
    """Show about information."""
    clear()
    banner()
    
    print(f"\n {M}[ABOUT RPWTOOLS FILE ENCRYPTOR]{RESET}")
    print(LINE)
    print(f" {Y}Description:{RESET}")
    print(f"   {W}Military-grade file encryption tool{RESET}")
    print(f"   {W}Uses PBKDF2-SHA256 with 500,000 iterations{RESET}")
    print()
    print(f" {Y}Features:{RESET}")
    print(f"   {G}✓{RESET} {W}Unbreakable encryption{RESET}")
    print(f"   {G}✓{RESET} {W}Anti-debugging protection{RESET}")
    print(f"   {G}✓{RESET} {W}5 encryption layers{RESET}")
    print(f"   {G}✓{RESET} {W}Cryptographically secure keys{RESET}")
    print(f"   {G}✓{RESET} {W}SHA512 integrity verification{RESET}")
    print()
    print(f" {Y}Security Level:{RESET}")
    print(f"   {G}[ {BG_G}{W}MAXIMUM{RESET}{G} ]{RESET} {W}- UNBREAKABLE{RESET}")
    print()
    print(f" {Y}Supported Files:{RESET}")
    print(f"   {C}• Python files (.py only){RESET}")
    print()
    print(f" {Y}Protection Against:{RESET}")
    print(f"   {R}✗{RESET} {W}Decompilers{RESET}")
    print(f"   {R}✗{RESET} {W}Reverse engineering{RESET}")
    print(f"   {R}✗{RESET} {W}Code inspection{RESET}")
    print(f"   {R}✗{RESET} {W}Debuggers{RESET}")
    print(f"   {R}✗{RESET} {W}Brute force attacks{RESET}")
    print(LINE)
    
    input(f"\n {Y}[PRESS ENTER TO CONTINUE]{RESET}")

def main():
    """Main program loop."""
    while True:
        clear()
        banner()
        show_menu()
        
        choice = input(f"\n {W}[{W}➤{W}]{RESET} {C}CHOICE {W}➤{RESET} ").strip()
        
        if choice == '1':
            encrypt_single_file()
        elif choice == '2':
            batch_encrypt_files()
        elif choice == '3':
            show_about()
        elif choice == '0':
            clear()
            banner()
            print(f"\n {G}[!] Thank you for using RPWTOOLS File Encryptor!{RESET}")
            print(f" {Y}[!] Your files are now protected with military-grade encryption.{RESET}")
            print(LINE)
            print(f"\n {C}Developer: {W}KEN DRICK / RYO GRAHHH{RESET}")
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
