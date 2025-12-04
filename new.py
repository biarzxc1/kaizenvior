#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════╗
║              CPyLock v1.0 - BY KEN DRICK                  ║
║              FACEBOOK: facebook.com/ryoevisu              ║
║                                                           ║
║      PYTHON ENCRYPTOR - BYTECODE + MULTI-LAYER ENCRYPT   ║
╚═══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import base64
import zlib
import marshal
import random
import string
import hashlib

# --- COLORS ---
R = '\033[1;31m'
G = '\033[1;32m'
C = '\033[1;36m'
Y = '\033[1;33m'
M = '\033[1;35m'
B = '\033[1;34m'
W = '\033[1;37m'
BG_R = '\033[41m'
BG_G = '\033[42m'
BG_M = '\033[45m'
RESET = '\033[0m'

LINE = f"{M}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

HOME = os.path.expanduser("~")
DOWNLOAD = "/storage/emulated/0/Download"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{M}
    ██████╗██████╗ ██╗   ██╗██╗      ██████╗  ██████╗██╗  ██╗
   ██╔════╝██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██╔════╝██║ ██╔╝
   ██║     ██████╔╝ ╚████╔╝ ██║     ██║   ██║██║     █████╔╝ 
   ██║     ██╔═══╝   ╚██╔╝  ██║     ██║   ██║██║     ██╔═██╗ 
   ╚██████╗██║        ██║   ███████╗╚██████╔╝╚██████╗██║  ██╗
    ╚═════╝╚═╝        ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
    {RESET}""")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    tool = f"{M}[ {BG_M}{W}CPyLock{RESET}{M} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL NAME':<13} {W}➤{RESET} {tool}")
    print(LINE)

def menu():
    def k(n, c): return f"{W}[{M}{n}{Y}/{M}{c}{W}]{RESET}"
    print(f" {k('01', 'A')} {G}ENCRYPT PYTHON FILE{RESET}")
    print(f" {k('02', 'B')} {G}ENCRYPT WITH CUSTOM LAYERS{RESET}")
    print(f" {k('03', 'C')} {G}ABOUT CPyLock{RESET}")
    print(f" {k('00', 'X')} {R}EXIT{RESET}")
    print(LINE)

def loader(text, duration=1.0):
    for i in range(31):
        bar = f"{M}{'█' * i}{W}{'░' * (30 - i)}{RESET}"
        sys.stdout.write(f"\r {Y}[{RESET} {bar} {Y}]{RESET} {W}{int(i*100/30)}%{RESET} {C}{text}{RESET}")
        sys.stdout.flush()
        time.sleep(duration / 30)
    print()

def msg(text, t="info"):
    icons = {"success": (G, "✓"), "error": (R, "✗"), "warn": (Y, "!"), "info": (W, "•")}
    c, i = icons.get(t, (W, "•"))
    print(f" {c}[{RESET}{i}{c}]{RESET} {c if t != 'info' else C}{text}{RESET}")

def rand_var(length=12):
    """Generate random variable name"""
    return '_' + ''.join(random.choices(string.ascii_lowercase, k=length))

def rand_str(length=8):
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_output_dir():
    if os.path.exists(DOWNLOAD):
        return DOWNLOAD
    return HOME

# ═══════════════════════════════════════════════════════════════
#                     ENCRYPTION LAYERS
# ═══════════════════════════════════════════════════════════════

def layer_marshal_zlib_b64(code):
    """Layer: Marshal + Zlib + Base64 (strongest)"""
    try:
        compiled = compile(code, '<CPyLock>', 'exec')
        marshalled = marshal.dumps(compiled)
        compressed = zlib.compress(marshalled, 9)
        encoded = base64.b64encode(compressed).decode()
        
        v1, v2 = rand_var(), rand_var()
        
        return f'''import marshal,zlib,base64
{v1}="{encoded}"
{v2}=marshal.loads(zlib.decompress(base64.b64decode({v1})))
exec({v2})
'''
    except:
        return None

def layer_zlib_b64(code):
    """Layer: Zlib + Base64"""
    try:
        compressed = zlib.compress(code.encode('utf-8'), 9)
        encoded = base64.b64encode(compressed).decode()
        
        v1, v2 = rand_var(), rand_var()
        
        return f'''import zlib,base64
{v1}="{encoded}"
{v2}=zlib.decompress(base64.b64decode({v1})).decode()
exec({v2})
'''
    except:
        return None

def layer_b85(code):
    """Layer: Base85 encoding"""
    try:
        encoded = base64.b85encode(code.encode('utf-8')).decode()
        v1 = rand_var()
        
        return f'''import base64
{v1}="{encoded}"
exec(base64.b85decode({v1}).decode())
'''
    except:
        return None

def layer_hex(code):
    """Layer: Hex encoding"""
    try:
        encoded = code.encode('utf-8').hex()
        v1 = rand_var()
        
        return f'''{v1}="{encoded}"
exec(bytes.fromhex({v1}).decode())
'''
    except:
        return None

def layer_reverse_b64(code):
    """Layer: Reverse + Base64"""
    try:
        reversed_code = code[::-1]
        encoded = base64.b64encode(reversed_code.encode('utf-8')).decode()
        v1, v2 = rand_var(), rand_var()
        
        return f'''import base64
{v1}="{encoded}"
{v2}=base64.b64decode({v1}).decode()[::-1]
exec({v2})
'''
    except:
        return None

def layer_xor_b64(code):
    """Layer: XOR + Base64"""
    try:
        key = random.randint(1, 255)
        xored = bytes([b ^ key for b in code.encode('utf-8')])
        encoded = base64.b64encode(xored).decode()
        v1, v2 = rand_var(), rand_var()
        
        return f'''import base64
{v1}="{encoded}"
{v2}=bytes([b^{key} for b in base64.b64decode({v1})]).decode()
exec({v2})
'''
    except:
        return None

def layer_chunks_b64(code):
    """Layer: Split into chunks + Base64"""
    try:
        encoded = base64.b64encode(code.encode('utf-8')).decode()
        chunk_size = random.randint(40, 80)
        chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
        v1, v2 = rand_var(), rand_var()
        
        return f'''import base64
{v1}={chunks}
{v2}="".join({v1})
exec(base64.b64decode({v2}).decode())
'''
    except:
        return None

def layer_lambda_b64(code):
    """Layer: Lambda wrapper + Base64"""
    try:
        encoded = base64.b64encode(code.encode('utf-8')).decode()
        v1, v2, v3 = rand_var(), rand_var(), rand_var()
        
        return f'''import base64
{v1}=lambda x:exec(base64.b64decode(x).decode())
{v2}="{encoded}"
{v1}({v2})
'''
    except:
        return None

def layer_rot_b64(code):
    """Layer: Custom ROT + Base64"""
    try:
        shift = random.randint(5, 50)
        rotated = ''.join([chr((ord(c) + shift) % 65536) for c in code])
        encoded = base64.b64encode(rotated.encode('utf-8')).decode()
        v1, v2 = rand_var(), rand_var()
        
        return f'''import base64
{v1}="{encoded}"
{v2}="".join([chr((ord(c)-{shift})%65536) for c in base64.b64decode({v1}).decode()])
exec({v2})
'''
    except:
        return None

# All encryption layers
LAYERS = [
    ("MARSHAL+ZLIB+BASE64", layer_marshal_zlib_b64),
    ("ZLIB+BASE64", layer_zlib_b64),
    ("BASE85", layer_b85),
    ("HEX", layer_hex),
    ("REVERSE+BASE64", layer_reverse_b64),
    ("XOR+BASE64", layer_xor_b64),
    ("CHUNKS+BASE64", layer_chunks_b64),
    ("LAMBDA+BASE64", layer_lambda_b64),
    ("ROT+BASE64", layer_rot_b64),
]

def encrypt_code(code, num_layers=5):
    """Encrypt code with multiple layers"""
    result = code
    used_layers = []
    
    for i in range(num_layers):
        # Pick random layer
        available = LAYERS.copy()
        random.shuffle(available)
        
        success = False
        for layer_name, layer_func in available:
            encrypted = layer_func(result)
            if encrypted:
                result = encrypted
                used_layers.append(layer_name)
                success = True
                break
        
        if not success:
            break
    
    return result, used_layers

def create_encrypted_file(filepath, num_layers=5):
    """Create encrypted Python file"""
    
    # Validate file
    if not os.path.exists(filepath):
        return None, "File not found"
    
    if not filepath.endswith('.py'):
        return None, "Only .py files supported"
    
    # Read source
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return None, f"Cannot read file: {e}"
    
    # Validate Python syntax
    try:
        compile(code, filepath, 'exec')
    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    
    orig_size = len(code)
    
    # Encrypt
    encrypted, layers = encrypt_code(code, num_layers)
    
    if not layers:
        return None, "Encryption failed"
    
    # Create header
    header = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════╗
║                   ENCRYPTED BY CPyLock                    ║
║                   DEVELOPER: KEN DRICK                    ║
║                   FACEBOOK: facebook.com/ryoevisu         ║
║                                                           ║
║   ⚠️  WARNING: DO NOT MODIFY THIS FILE                    ║
║   ⚠️  TAMPERING WILL BREAK THE CODE                       ║
║                                                           ║
║   ENCRYPTION LAYERS: {len(layers):<3}                                  ║
╚═══════════════════════════════════════════════════════════╝
"""

'''
    
    final_code = header + encrypted
    
    # Generate output path
    name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = get_output_dir()
    output_path = os.path.join(output_dir, f"{name}-encrypted.py")
    
    # Save
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        os.chmod(output_path, 0o755)
    except Exception as e:
        return None, f"Cannot save: {e}"
    
    enc_size = len(final_code)
    
    return {
        'output': output_path,
        'orig_size': orig_size,
        'enc_size': enc_size,
        'layers': layers,
        'name': name,
    }, None

def opt_encrypt():
    """Encrypt with default 5 layers"""
    clear()
    banner()
    print(f" {M}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {M}║{RESET}         {Y}ENCRYPT PYTHON FILE{RESET}                  {M}║{RESET}")
    print(f" {M}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}Enter path to your Python file:{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {G}Example: /storage/emulated/0/Download/myfile.py{RESET}")
    print(LINE)
    
    path = input(f" {W}[{RESET}?{W}]{RESET} {C}PATH{RESET} {Y}➤{RESET} ").strip()
    
    if not path:
        msg("No path!", "error")
        time.sleep(1)
        return
    
    path = os.path.expanduser(path)
    
    if not os.path.exists(path):
        msg(f"Not found: {path}", "error")
        time.sleep(2)
        return
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}ENCRYPTING WITH 5 LAYERS...{RESET}")
    print(LINE)
    
    loader("LAYER 01/A - PROCESSING", 0.2)
    loader("LAYER 02/B - PROCESSING", 0.2)
    loader("LAYER 03/C - PROCESSING", 0.2)
    loader("LAYER 04/D - PROCESSING", 0.2)
    loader("LAYER 05/E - PROCESSING", 0.2)
    
    result, err = create_encrypted_file(path, 5)
    
    if err:
        print(LINE)
        msg("ENCRYPTION FAILED!", "error")
        print(f" {R}{err}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    loader("FINALIZING", 0.2)
    
    print()
    print(LINE)
    msg("ENCRYPTION SUCCESSFUL!", "success")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'OUTPUT FILE':<14} {W}➤{RESET} {G}{result['output']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL':<14} {W}➤{RESET} {C}{result['orig_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ENCRYPTED':<14} {W}➤{RESET} {M}{result['enc_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'LAYERS':<14} {W}➤{RESET} {G}{len(result['layers'])}{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}LAYERS USED:{RESET}")
    
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for i, layer in enumerate(result['layers']):
        l = letters[i] if i < len(letters) else 'X'
        print(f"     {W}[{M}{i+1:02d}{Y}/{M}{l}{W}]{RESET} {G}{layer}{RESET}")
    
    print(LINE)
    print(f" {G}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {G}║{RESET} {Y}✅ HOW TO RUN:{RESET}                                {G}║{RESET}")
    print(f" {G}╚═══════════════════════════════════════════════╝{RESET}")
    print(f"    {G}python3 {result['output']}{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def opt_encrypt_custom():
    """Encrypt with custom layers"""
    clear()
    banner()
    print(f" {M}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {M}║{RESET}       {Y}ENCRYPT WITH CUSTOM LAYERS{RESET}              {M}║{RESET}")
    print(f" {M}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}Enter path to your Python file:{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {G}Example: /storage/emulated/0/Download/myfile.py{RESET}")
    print(LINE)
    
    path = input(f" {W}[{RESET}?{W}]{RESET} {C}PATH{RESET} {Y}➤{RESET} ").strip()
    
    if not path:
        msg("No path!", "error")
        time.sleep(1)
        return
    
    path = os.path.expanduser(path)
    
    if not os.path.exists(path):
        msg(f"Not found: {path}", "error")
        time.sleep(2)
        return
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}NUMBER OF LAYERS (1-15):{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {C}More layers = harder to crack but larger file{RESET}")
    print(LINE)
    
    try:
        layers = int(input(f" {W}[{RESET}?{W}]{RESET} {C}LAYERS{RESET} {Y}➤{RESET} ").strip())
        layers = max(1, min(15, layers))
    except:
        layers = 5
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}ENCRYPTING WITH {layers} LAYERS...{RESET}")
    print(LINE)
    
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(layers):
        l = letters[i] if i < len(letters) else 'X'
        loader(f"LAYER {i+1:02d}/{l} - PROCESSING", 0.15)
    
    result, err = create_encrypted_file(path, layers)
    
    if err:
        print(LINE)
        msg("ENCRYPTION FAILED!", "error")
        print(f" {R}{err}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    loader("FINALIZING", 0.2)
    
    print()
    print(LINE)
    msg("ENCRYPTION SUCCESSFUL!", "success")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'OUTPUT FILE':<14} {W}➤{RESET} {G}{result['output']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL':<14} {W}➤{RESET} {C}{result['orig_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ENCRYPTED':<14} {W}➤{RESET} {M}{result['enc_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'LAYERS':<14} {W}➤{RESET} {G}{len(result['layers'])}{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}LAYERS USED:{RESET}")
    
    for i, layer in enumerate(result['layers']):
        l = letters[i] if i < len(letters) else 'X'
        print(f"     {W}[{M}{i+1:02d}{Y}/{M}{l}{W}]{RESET} {G}{layer}{RESET}")
    
    print(LINE)
    print(f" {G}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {G}║{RESET} {Y}✅ HOW TO RUN:{RESET}                                {G}║{RESET}")
    print(f" {G}╚═══════════════════════════════════════════════╝{RESET}")
    print(f"    {G}python3 {result['output']}{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def opt_about():
    """About CPyLock"""
    clear()
    banner()
    print(f" {M}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {M}║{RESET}             {Y}ABOUT CPyLock{RESET}                     {M}║{RESET}")
    print(f" {M}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TOOL{RESET}      {W}➤{RESET} {G}CPyLock{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}VERSION{RESET}   {W}➤{RESET} {G}1.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}DEVELOPER{RESET} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}FACEBOOK{RESET}  {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}DESCRIPTION:{RESET}")
    print(f"     {G}CPyLock encrypts Python source code using{RESET}")
    print(f"     {G}multiple layers of obfuscation including:{RESET}")
    print(f"     {G}Marshal, Zlib, Base64, XOR, and more.{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}ENCRYPTION LAYERS:{RESET}")
    print(f"     {W}[{M}01{W}]{RESET} {G}MARSHAL + ZLIB + BASE64{RESET}")
    print(f"     {W}[{M}02{W}]{RESET} {G}ZLIB + BASE64{RESET}")
    print(f"     {W}[{M}03{W}]{RESET} {G}BASE85 ENCODING{RESET}")
    print(f"     {W}[{M}04{W}]{RESET} {G}HEX ENCODING{RESET}")
    print(f"     {W}[{M}05{W}]{RESET} {G}REVERSE + BASE64{RESET}")
    print(f"     {W}[{M}06{W}]{RESET} {G}XOR + BASE64{RESET}")
    print(f"     {W}[{M}07{W}]{RESET} {G}CHUNKS + BASE64{RESET}")
    print(f"     {W}[{M}08{W}]{RESET} {G}LAMBDA + BASE64{RESET}")
    print(f"     {W}[{M}09{W}]{RESET} {G}ROT + BASE64{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FEATURES:{RESET}")
    print(f"     {G}• Multi-layer encryption{RESET}")
    print(f"     {G}• Random variable names{RESET}")
    print(f"     {G}• Works on any Python environment{RESET}")
    print(f"     {G}• No external dependencies{RESET}")
    print(f"     {G}• Termux compatible{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}OUTPUT:{RESET}")
    print(f"     {G}yourfile-encrypted.py{RESET}")
    print(f"     {Y}Run directly with: python3 yourfile-encrypted.py{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def main():
    while True:
        clear()
        banner()
        menu()
        
        ch = input(f" {W}[{RESET}?{W}]{RESET} {C}SELECT{RESET} {Y}➤{RESET} ").strip().upper()
        
        if ch in ['01', '1', 'A']:
            opt_encrypt()
        elif ch in ['02', '2', 'B']:
            opt_encrypt_custom()
        elif ch in ['03', '3', 'C']:
            opt_about()
        elif ch in ['00', '0', 'X']:
            clear()
            banner()
            msg("Thank you for using CPyLock!", "success")
            print(LINE)
            sys.exit(0)
        else:
            msg("Invalid option!", "error")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n {R}Interrupted{RESET}")
        sys.exit(0)
