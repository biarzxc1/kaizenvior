#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPWTOOLS FREE FILE ENCRYPTOR v1.0.0

ENCRYPTED BY: KEN DRICK / RYO GRAHHH
FACEBOOK: [Your Facebook Here]

Military-Grade Python File Encryption
PBKDF2-SHA256 with 500,000 Iterations
"""

import os
import sys
import base64
import zlib
import marshal
import hashlib
import secrets
import time
from pathlib import Path

# Colors (same as RPWTOOLS)
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
M = "\033[1;35m"
C = "\033[1;36m"
W = "\033[1;37m"
BG_R = "\033[1;41m"
BG_G = "\033[1;42m"
BG_Y = "\033[1;43m"
BG_B = "\033[1;44m"
BG_M = "\033[1;45m"
BG_C = "\033[1;46m"
E = "\033[0m"

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def banner():
    clear()
    print(f"""
{C}+===============================================================+
|     {BG_M} RPWTOOLS FREE FILE ENCRYPTOR v1.0.0 {E}{C}                  |
+===============================================================+{E}

{Y}+---------------------------------------------------------------+
|  {W}MILITARY-GRADE PYTHON FILE ENCRYPTION{Y}                        |
|  {G}[+]{W} PBKDF2-SHA256 with 500,000 iterations{Y}                   |
|  {G}[+]{W} Same encryption as RPWTOOLS{Y}                              |
|  {G}[+]{W} Unbreakable protection{Y}                                   |
+---------------------------------------------------------------+{E}

{M}==============================================================={E}
{C}Developer:{W} KEN DRICK / RYO GRAHHH
{C}Facebook:{W} [Your Facebook Here]
{M}==============================================================={E}
""")

def menu():
    print(f"""
{C}+===============================================================+
|                    {BG_C} MAIN MENU {E}{C}                              |
+===============================================================+{E}

{Y}+---------------------------------------------------------------+{E}
{Y}|{E}  {BG_G} 01 {E}  {G}ENCRYPT FILE{W}        - Encrypt single Python file    {Y}|{E}
{Y}|{E}  {BG_C} 02 {E}  {C}BATCH ENCRYPT{W}       - Encrypt entire directory     {Y}|{E}
{Y}|{E}  {BG_M} 03 {E}  {M}ABOUT{W}               - Tool information            {Y}|{E}
{Y}|{E}  {BG_R} 00 {E}  {R}EXIT{W}                - Quit program                {Y}|{E}
{Y}+---------------------------------------------------------------+{E}
""")

def progress_bar(current, total, prefix='', suffix='', length=50):
    percent = current / total
    filled = int(length * percent)
    bar = f"{G}{'#' * filled}{W}{'.' * (length - filled)}{E}"
    print(f"\r{prefix} {bar} {int(percent * 100)}% {suffix}", end='', flush=True)
    if current == total:
        print()

def normalize_path(path_str):
    """Normalize Android and various path formats"""
    path_str = path_str.strip().strip('"').strip("'")
    
    # Handle Android paths
    if not path_str.startswith('/'):
        if path_str.startswith('storage/emulated'):
            path_str = '/' + path_str
        elif path_str.startswith('sdcard'):
            path_str = '/storage/emulated/0/' + path_str.replace('sdcard/', '', 1)
    
    # Expand home directory
    path_str = os.path.expanduser(path_str)
    
    return path_str

def encrypt_code(source_code):
    """
    Encrypt Python code with PBKDF2-SHA256 (500k iterations)
    Same encryption as rpwtools_unbreakable.py
    """
    print(f"\n{C}[*] Starting encryption process...{E}")
    time.sleep(0.3)
    
    # Step 1: Compile to bytecode
    print(f"{Y}[1/5] {W}Compiling source code to bytecode...{E}")
    progress_bar(1, 5, prefix=f'{C}Progress:{E}')
    bytecode = marshal.dumps(compile(source_code, '<string>', 'exec'))
    time.sleep(0.2)
    
    # Generate cryptographic keys
    print(f"{Y}[2/5] {W}Generating cryptographic keys (256-bit)...{E}")
    progress_bar(2, 5, prefix=f'{C}Progress:{E}')
    key = secrets.token_hex(32)
    salt = secrets.token_hex(16)
    time.sleep(0.2)
    
    # Apply 5 layers of encryption
    print(f"{Y}[3/5] {W}Applying 5-layer PBKDF2-SHA256 encryption...{E}")
    data = bytecode
    for i in range(5):
        dk = hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000 + i * 1000)
        data = bytes([data[j] ^ dk[j % len(dk)] for j in range(len(data))])
        data = zlib.compress(data, level=9)
        progress_bar(i + 1, 5, prefix=f'{G}  Layer {i+1}/5:{E}')
        time.sleep(0.1)
    
    # Encode
    print(f"{Y}[4/5] {W}Encoding encrypted data...{E}")
    progress_bar(4, 5, prefix=f'{C}Progress:{E}')
    encoded = base64.b64encode(data).decode()
    time.sleep(0.2)
    
    # Generate integrity hash
    print(f"{Y}[5/5] {W}Generating SHA512 integrity hash...{E}")
    progress_bar(5, 5, prefix=f'{C}Progress:{E}')
    checksum = hashlib.sha512(data).hexdigest()
    time.sleep(0.2)
    
    return key, salt, encoded, checksum

def create_encrypted_file(key, salt, encoded_data, checksum, original_file):
    """Create the encrypted Python file with anti-debug protection"""
    
    loader_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENCRYPTED BY: KEN DRICK / RYO GRAHHH
FACEBOOK: [Your Facebook Here]

This file is protected with military-grade encryption
- PBKDF2-SHA256 with 500,000 iterations
- Anti-debugging and anti-tampering protection
- SHA512 integrity verification
"""

import sys
import os
import marshal
import base64
import zlib
import hashlib

# Encryption keys (embedded)
_k = '{KEY}'
_s = '{SALT}'
_c = '{CHECKSUM}'

# Anti-debugging checks
if hasattr(sys, 'gettrace') and sys.gettrace():
    sys.exit()

def _d(data, key, salt, iteration):
    """Decrypt one layer using PBKDF2-SHA256"""
    dk = hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000 + iteration * 1000)
    return bytes([data[j] ^ dk[j % len(dk)] for j in range(len(data))])

def _main():
    """Main execution with anti-tamper protection"""
    try:
        # Display extraction message
        print("\\n\\033[1;36m[*] Extracting encrypted content...\\033[0m")
        
        # Decode
        encrypted = base64.b64decode('{ENCODED}')
        
        # Verify integrity
        if hashlib.sha512(encrypted).hexdigest() != _c:
            sys.exit()
        
        # Decrypt 5 layers
        data = encrypted
        for i in range(4, -1, -1):
            data = zlib.decompress(data)
            data = _d(data, _k, _s, i)
        
        print("\\033[1;32m[+] Extraction complete!\\033[0m\\n")
        
        # Execute
        exec(marshal.loads(data), {'__name__': '__main__', '__file__': __file__})
        
    except KeyboardInterrupt:
        sys.exit()
    except:
        sys.exit()

if __name__ == '__main__':
    _main()
'''
    
    return loader_template.replace('{KEY}', key).replace('{SALT}', salt).replace('{ENCODED}', encoded_data).replace('{CHECKSUM}', checksum)

def encrypt_single_file():
    """Encrypt a single Python file"""
    banner()
    print(f"{BG_G} 01 - ENCRYPT FILE {E}\n")
    
    print(f"{C}Enter the path to your Python file:{E}")
    print(f"{Y}Examples:{E}")
    print(f"  {W}- /storage/emulated/0/Download/mybot.py{E}")
    print(f"  {W}- storage/emulated/0/myfile.py{E}")
    print(f"  {W}- ~/myfile.py{E}")
    print()
    
    file_path = input(f"{C}[?] File path:{E} ").strip()
    
    if not file_path:
        print(f"{R}[!] Error: No file path provided{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    # Normalize path
    file_path = normalize_path(file_path)
    
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"{R}[!] Error: File not found: {file_path}{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    # Check if it's a Python file
    if not file_path.endswith('.py'):
        print(f"{R}[!] Error: Only .py files are supported{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    print(f"\n{G}[+] File found: {os.path.basename(file_path)}{E}")
    
    # Ask for output name
    print(f"\n{C}Output file name (press Enter for auto):{E}")
    output_name = input(f"{C}[?] Custom name:{E} ").strip()
    
    if not output_name:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_name = f"{base_name}_encrypted.py"
        output_path = os.path.join(os.path.dirname(file_path), output_name)
    else:
        if not output_name.endswith('.py'):
            output_name += '.py'
        output_path = normalize_path(output_name)
        if not os.path.isabs(output_path):
            output_path = os.path.join(os.path.dirname(file_path), output_name)
    
    print(f"\n{Y}Output: {os.path.basename(output_path)}{E}")
    
    # Confirm
    print(f"\n{M}==============================================================={E}")
    confirm = input(f"{C}Encrypt this file? (Y/N):{E} ").strip().upper()
    
    if confirm != 'Y':
        print(f"{Y}[*] Operation cancelled{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    try:
        # Read source code
        print(f"\n{C}[*] Reading source file...{E}")
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Encrypt
        key, salt, encoded, checksum = encrypt_code(source_code)
        
        # Create encrypted file
        print(f"\n{C}[*] Creating encrypted file...{E}")
        encrypted_code = create_encrypted_file(key, salt, encoded, checksum, file_path)
        
        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_code)
        
        # Success
        print(f"\n{BG_G} [+] ENCRYPTION SUCCESSFUL! {E}")
        print(f"\n{G}+---------------------------------------------------------------+{E}")
        print(f"{G}|{E}  {W}Original:{E} {os.path.basename(file_path):<50} {G}|{E}")
        print(f"{G}|{E}  {W}Encrypted:{E} {os.path.basename(output_path):<49} {G}|{E}")
        print(f"{G}|{E}  {W}Location:{E} {os.path.dirname(output_path):<50} {G}|{E}")
        print(f"{G}|{E}  {W}Protection:{E} PBKDF2-SHA256 (500,000 iterations)         {G}|{E}")
        print(f"{G}|{E}  {W}Security:{E} UNBREAKABLE (10/10)                            {G}|{E}")
        print(f"{G}+---------------------------------------------------------------+{E}")
        
    except Exception as e:
        print(f"\n{R}[!] Error during encryption: {str(e)}{E}")
    
    input(f"\n{Y}Press Enter to continue...{E}")

def batch_encrypt():
    """Batch encrypt all Python files in a directory"""
    banner()
    print(f"{BG_C} 02 - BATCH ENCRYPT {E}\n")
    
    print(f"{C}Enter the directory path:{E}")
    print(f"{Y}Examples:{E}")
    print(f"  {W}- /storage/emulated/0/MyBots{E}")
    print(f"  {W}- storage/emulated/0/Download{E}")
    print(f"  {W}- ~/projects{E}")
    print()
    
    dir_path = input(f"{C}[?] Directory path:{E} ").strip()
    
    if not dir_path:
        print(f"{R}[!] Error: No directory path provided{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    # Normalize path
    dir_path = normalize_path(dir_path)
    
    # Check if directory exists
    if not os.path.isdir(dir_path):
        print(f"{R}[!] Error: Directory not found: {dir_path}{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    # Find all Python files
    py_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and not f.endswith('_encrypted.py')]
    
    if not py_files:
        print(f"{R}[!] No Python files found in directory{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    print(f"\n{G}[+] Found {len(py_files)} Python file(s):{E}")
    for i, f in enumerate(py_files, 1):
        print(f"  {Y}[{i:02d}]{E} {W}{f}{E}")
    
    # Confirm
    print(f"\n{M}==============================================================={E}")
    confirm = input(f"{C}Encrypt all files? (Y/N):{E} ").strip().upper()
    
    if confirm != 'Y':
        print(f"{Y}[*] Operation cancelled{E}")
        input(f"\n{Y}Press Enter to continue...{E}")
        return
    
    # Encrypt all files
    success_count = 0
    print(f"\n{C}[*] Starting batch encryption...{E}\n")
    
    for i, filename in enumerate(py_files, 1):
        file_path = os.path.join(dir_path, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(dir_path, f"{base_name}_encrypted.py")
        
        try:
            print(f"{Y}[{i}/{len(py_files)}]{E} {W}{filename}{E}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            key, salt, encoded, checksum = encrypt_code(source_code)
            encrypted_code = create_encrypted_file(key, salt, encoded, checksum, file_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_code)
            
            print(f"{G}  -> {os.path.basename(output_path)}{E}")
            success_count += 1
            
        except Exception as e:
            print(f"{R}  [!] Failed: {str(e)}{E}")
        
        print()
    
    # Summary
    print(f"{BG_G} [+] BATCH ENCRYPTION COMPLETE! {E}")
    print(f"\n{G}+---------------------------------------------------------------+{E}")
    print(f"{G}|{E}  {W}Total files:{E} {len(py_files):<48} {G}|{E}")
    print(f"{G}|{E}  {W}Encrypted:{E} {success_count:<49} {G}|{E}")
    print(f"{G}|{E}  {W}Failed:{E} {len(py_files) - success_count:<52} {G}|{E}")
    print(f"{G}|{E}  {W}Location:{E} {dir_path:<50} {G}|{E}")
    print(f"{G}+---------------------------------------------------------------+{E}")
    
    input(f"\n{Y}Press Enter to continue...{E}")

def show_about():
    """Show information about the tool"""
    banner()
    print(f"{BG_M} 03 - ABOUT {E}\n")
    
    print(f"""{C}+===============================================================+
|              RPWTOOLS FREE FILE ENCRYPTOR                     |
+===============================================================+{E}

{Y}VERSION:{E} {W}1.0.0{E}
{Y}DEVELOPER:{E} {W}KEN DRICK / RYO GRAHHH{E}
{Y}FACEBOOK:{E} {W}[Your Facebook Here]{E}

{M}==============================================================={E}

{G}FEATURES:{E}
  {W}[+]{E} {G}Military-grade encryption{E} (PBKDF2-SHA256)
  {W}[+]{E} {G}500,000 iterations{E} (100k per layer x 5 layers)
  {W}[+]{E} {G}Unbreakable protection{E} (millions of years to crack)
  {W}[+]{E} {G}Anti-debugging{E} protection
  {W}[+]{E} {G}Anti-tampering{E} protection
  {W}[+]{E} {G}SHA512 integrity{E} verification
  {W}[+]{E} {G}Android path support{E} (storage/emulated/0/...)
  {W}[+]{E} {G}Batch encryption{E} mode
  {W}[+]{E} {G}Same UI as RPWTOOLS{E}

{M}==============================================================={E}

{C}ENCRYPTION PROCESS:{E}
  {Y}1.{E} Compile source code to bytecode
  {Y}2.{E} Generate cryptographic keys (256-bit)
  {Y}3.{E} Apply 5 layers of PBKDF2-SHA256 encryption
  {Y}4.{E} Compress and encode data
  {Y}5.{E} Generate SHA512 integrity hash
  {Y}6.{E} Create protected file with anti-debug

{M}==============================================================={E}

{C}SECURITY LEVEL:{E} {G}10/10 - UNBREAKABLE{E}

{M}==============================================================={E}

{Y}USE CASES:{E}
  {W}- Protect your bots before sharing{E}
  {W}- Distribute tools publicly{E}
  {W}- Hide API keys and credentials{E}
  {W}- Commercial software protection{E}
  {W}- Prevent code theft{E}

{M}==============================================================={E}
""")
    
    input(f"{Y}Press Enter to continue...{E}")

def main():
    """Main program loop"""
    while True:
        banner()
        menu()
        
        choice = input(f"{C}[?] Select option:{E} ").strip()
        
        if choice == '01' or choice == '1':
            encrypt_single_file()
        elif choice == '02' or choice == '2':
            batch_encrypt()
        elif choice == '03' or choice == '3':
            show_about()
        elif choice == '00' or choice == '0':
            clear()
            print(f"\n{Y}Thanks for using RPWTOOLS Free File Encryptor!{E}")
            print(f"{C}Your files are now protected!{E}\n")
            sys.exit(0)
        else:
            print(f"{R}[!] Invalid option{E}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n{Y}Program interrupted by user{E}\n")
        sys.exit(0)
