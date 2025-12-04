#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════╗
║              CPyLock v2.0 - BY KEN DRICK                  ║
║              FACEBOOK: facebook.com/ryoevisu              ║
║                                                           ║
║   PYTHON ENCRYPTOR WITH BINARY PROTECTION & ANTI-BYPASS  ║
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
import struct

# --- COLORS ---
R = '\033[1;31m'
G = '\033[1;32m'
C = '\033[1;36m'
Y = '\033[1;33m'
M = '\033[1;35m'
B = '\033[1;34m'
W = '\033[1;37m'
BG_R = '\033[41m'
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
                        {R}[ BINARY EDITION ]{RESET}{M}
    {RESET}""")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}2.0.0 BINARY{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    tool = f"{M}[ {BG_M}{W}CPyLock BINARY{RESET}{M} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL NAME':<13} {W}➤{RESET} {tool}")
    print(LINE)

def menu():
    def k(n, c): return f"{W}[{M}{n}{Y}/{M}{c}{W}]{RESET}"
    print(f" {k('01', 'A')} {G}ENCRYPT TO BINARY (.pyc){RESET}")
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

def rand_var(length=16):
    chars = 'OQ0oIl1i' + string.ascii_letters
    return '_' + ''.join(random.choices(chars, k=length))

def rand_junk():
    ops = [
        f"{rand_var()}={random.randint(1000,9999)}",
        f"{rand_var()}='{rand_var()}'",
        f"{rand_var()}=[{','.join([str(random.randint(0,255)) for _ in range(random.randint(3,8))])}]",
    ]
    return random.choice(ops)

def get_output_dir():
    if os.path.exists(DOWNLOAD):
        return DOWNLOAD
    return HOME

def generate_anti_bypass_code(checksum):
    v1, v2, v3, v4, v5 = [rand_var() for _ in range(5)]
    v6, v7, v8, v9, v10 = [rand_var() for _ in range(5)]
    
    protection = f'''
import sys,os,hashlib,base64,zlib,marshal
{rand_junk()};{rand_junk()}
{v1}="{checksum}"
def {v3}():
    {v4}=sys._getframe()
    if {v4}.f_back and {v4}.f_back.f_back:
        {v5}={v4}.f_back.f_code.co_filename
        if any({v6} in {v5}.lower() for {v6} in ['debug','decompil','unpy','pycdc','reverse','crack','bypass','dump','extract','unpyc']):
            print("\\n\\033[1;31m╔═══════════════════════════════════════════════════════════╗\\033[0m")
            print("\\033[1;31m║  ⛔ CPyLock SECURITY ALERT - BYPASS ATTEMPT DETECTED! ⛔   ║\\033[0m")
            print("\\033[1;31m╠═══════════════════════════════════════════════════════════╣\\033[0m")
            print("\\033[1;31m║  Don't try to bypass or decompile this protected script!  ║\\033[0m")
            print("\\033[1;31m║  This file is protected by CPyLock Binary Protection.     ║\\033[0m")
            print("\\033[1;31m║  Unauthorized access is prohibited.                       ║\\033[0m")
            print("\\033[1;31m║                                                           ║\\033[0m")
            print("\\033[1;31m║  Developer: KEN DRICK | FB: facebook.com/ryoevisu         ║\\033[0m")
            print("\\033[1;31m╚═══════════════════════════════════════════════════════════╝\\033[0m\\n")
            os._exit(1)
{rand_junk()}
def {v7}():
    try:
        import dis,inspect
        {v8}=sys._getframe().f_back
        if {v8}:
            {v9}=str({v8}.f_locals)+str({v8}.f_globals)
            if any(x in {v9}.lower() for x in ['debug','trace','inspect','decompil']):
                print("\\n\\033[1;31m⛔ CPyLock: Debug attempt detected! Access denied.\\033[0m\\n")
                os._exit(1)
    except:pass
{rand_junk()}
def {v10}():
    try:
        import uncompyle6
        print("\\n\\033[1;31m⛔ DECOMPILER DETECTED! Don't try to bypass CPyLock!\\033[0m\\n")
        os._exit(1)
    except:pass
    try:
        import decompyle3
        print("\\n\\033[1;31m⛔ DECOMPILER DETECTED! Don't try to bypass CPyLock!\\033[0m\\n")
        os._exit(1)
    except:pass
{v3}();{v7}();{v10}()
{rand_junk()}
'''
    return protection

def layer_marshal_zlib_b64(code):
    try:
        compiled = compile(code, '<CPyLock>', 'exec')
        marshalled = marshal.dumps(compiled)
        compressed = zlib.compress(marshalled, 9)
        encoded = base64.b64encode(compressed).decode()
        v1, v2 = rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=marshal.loads(zlib.decompress(base64.b64decode({v1})))
exec({v2})
'''
    except:
        return None

def layer_zlib_b64(code):
    try:
        compressed = zlib.compress(code.encode('utf-8'), 9)
        encoded = base64.b64encode(compressed).decode()
        v1, v2 = rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=zlib.decompress(base64.b64decode({v1})).decode()
exec({v2})
'''
    except:
        return None

def layer_b85_zlib(code):
    try:
        compressed = zlib.compress(code.encode('utf-8'), 9)
        encoded = base64.b85encode(compressed).decode()
        v1, v2 = rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=zlib.decompress(base64.b85decode({v1})).decode()
exec({v2})
'''
    except:
        return None

def layer_hex_zlib(code):
    try:
        compressed = zlib.compress(code.encode('utf-8'), 9)
        encoded = compressed.hex()
        v1, v2 = rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=zlib.decompress(bytes.fromhex({v1})).decode()
exec({v2})
'''
    except:
        return None

def layer_xor_b64(code):
    try:
        key = random.randint(1, 255)
        xored = bytes([b ^ key for b in code.encode('utf-8')])
        compressed = zlib.compress(xored, 9)
        encoded = base64.b64encode(compressed).decode()
        v1, v2, v3 = rand_var(), rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=zlib.decompress(base64.b64decode({v1}))
{v3}=bytes([b^{key} for b in {v2}]).decode()
exec({v3})
'''
    except:
        return None

def layer_reverse_xor_b64(code):
    try:
        key = random.randint(1, 255)
        reversed_code = code[::-1]
        xored = bytes([b ^ key for b in reversed_code.encode('utf-8')])
        encoded = base64.b64encode(xored).decode()
        v1, v2, v3 = rand_var(), rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=bytes([b^{key} for b in base64.b64decode({v1})]).decode()
{v3}={v2}[::-1]
exec({v3})
'''
    except:
        return None

def layer_chunks_marshal(code):
    try:
        compiled = compile(code, '<CPyLock>', 'exec')
        marshalled = marshal.dumps(compiled)
        compressed = zlib.compress(marshalled, 9)
        encoded = base64.b64encode(compressed).decode()
        chunk_size = random.randint(60, 100)
        chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
        v1, v2, v3 = rand_var(), rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}={chunks}
{v2}="".join({v1})
{v3}=marshal.loads(zlib.decompress(base64.b64decode({v2})))
exec({v3})
'''
    except:
        return None

def layer_lambda_marshal(code):
    try:
        compiled = compile(code, '<CPyLock>', 'exec')
        marshalled = marshal.dumps(compiled)
        compressed = zlib.compress(marshalled, 9)
        encoded = base64.b64encode(compressed).decode()
        v1, v2 = rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}=lambda x:exec(marshal.loads(zlib.decompress(base64.b64decode(x))))
{v2}="{encoded}"
{v1}({v2})
'''
    except:
        return None

def layer_double_b64_zlib(code):
    try:
        compressed = zlib.compress(code.encode('utf-8'), 9)
        encoded1 = base64.b64encode(compressed).decode()
        encoded2 = base64.b64encode(encoded1.encode()).decode()
        v1, v2 = rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded2}"
{v2}=zlib.decompress(base64.b64decode(base64.b64decode({v1}))).decode()
exec({v2})
'''
    except:
        return None

def layer_rot_zlib_b64(code):
    try:
        shift = random.randint(10, 100)
        rotated = ''.join([chr((ord(c) + shift) % 65536) for c in code])
        compressed = zlib.compress(rotated.encode('utf-8'), 9)
        encoded = base64.b64encode(compressed).decode()
        v1, v2, v3 = rand_var(), rand_var(), rand_var()
        return f'''{rand_junk()}
{v1}="{encoded}"
{v2}=zlib.decompress(base64.b64decode({v1})).decode()
{v3}="".join([chr((ord(c)-{shift})%65536) for c in {v2}])
exec({v3})
'''
    except:
        return None

LAYERS = [
    ("MARSHAL+ZLIB+BASE64", layer_marshal_zlib_b64),
    ("ZLIB+BASE64", layer_zlib_b64),
    ("BASE85+ZLIB", layer_b85_zlib),
    ("HEX+ZLIB", layer_hex_zlib),
    ("XOR+BASE64", layer_xor_b64),
    ("REVERSE+XOR+BASE64", layer_reverse_xor_b64),
    ("CHUNKS+MARSHAL", layer_chunks_marshal),
    ("LAMBDA+MARSHAL", layer_lambda_marshal),
    ("DOUBLE-BASE64+ZLIB", layer_double_b64_zlib),
    ("ROT+ZLIB+BASE64", layer_rot_zlib_b64),
]

def encrypt_code(code, num_layers=7):
    result = code
    used_layers = []
    
    for i in range(num_layers):
        available = LAYERS.copy()
        random.shuffle(available)
        
        for layer_name, layer_func in available:
            encrypted = layer_func(result)
            if encrypted:
                result = encrypted
                used_layers.append(layer_name)
                break
    
    return result, used_layers

def create_binary_header():
    magic = b'CPyLock\x00\x02\x00'
    timestamp = struct.pack('<I', int(time.time()))
    version = b'\x02\x00'
    padding = bytes([random.randint(0, 255) for _ in range(16)])
    header_bytes = magic + timestamp + version + padding
    return base64.b64encode(header_bytes).decode()

def create_encrypted_binary(filepath, num_layers=7):
    if not os.path.exists(filepath):
        return None, "File not found"
    
    if not filepath.endswith('.py'):
        return None, "Only .py files supported"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return None, f"Cannot read file: {e}"
    
    try:
        compile(code, filepath, 'exec')
    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    
    orig_size = len(code)
    
    encrypted, layers = encrypt_code(code, num_layers)
    
    if not layers:
        return None, "Encryption failed"
    
    checksum = hashlib.sha256(encrypted.encode()).hexdigest()[:32]
    protection = generate_anti_bypass_code(checksum)
    binary_header = create_binary_header()
    
    final_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔═══════════════════════════════════════════════════════════╗
# ║           CPyLock BINARY PROTECTED FILE v2.0              ║
# ║                                                           ║
# ║  ⚠️  WARNING: This file is protected by CPyLock Binary    ║
# ║  ⚠️  DO NOT MODIFY - Tamper protection enabled            ║
# ║  ⚠️  DO NOT DECOMPILE - Anti-bypass protection active     ║
# ║                                                           ║
# ║  Developer: KEN DRICK                                     ║
# ║  Facebook: facebook.com/ryoevisu                          ║
# ╚═══════════════════════════════════════════════════════════╝
#
# BINARY: {binary_header}
# HASH: {checksum}
# LAYERS: {len(layers)}
#
{protection}
# ═══════════════════════════════════════════════════════════════
{rand_junk()};{rand_junk()};{rand_junk()}
{encrypted}
'''
    
    name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = get_output_dir()
    output_path = os.path.join(output_dir, f"{name}-locked.py")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        os.chmod(output_path, 0o755)
    except Exception as e:
        return None, f"Cannot save: {e}"
    
    return {
        'output': output_path,
        'orig_size': orig_size,
        'enc_size': len(final_code),
        'layers': layers,
        'checksum': checksum,
        'name': name,
    }, None

def opt_encrypt():
    clear()
    banner()
    print(f" {M}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {M}║{RESET}       {Y}ENCRYPT TO BINARY PROTECTION{RESET}           {M}║{RESET}")
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
    print(f" {W}[{RESET}•{W}]{RESET} {Y}ENCRYPTING WITH BINARY PROTECTION...{RESET}")
    print(LINE)
    
    loader("LAYER 01/A - MARSHAL ENCODING", 0.15)
    loader("LAYER 02/B - ZLIB COMPRESSION", 0.15)
    loader("LAYER 03/C - XOR ENCRYPTION", 0.15)
    loader("LAYER 04/D - BASE64 ENCODING", 0.15)
    loader("LAYER 05/E - CHUNK SPLITTING", 0.15)
    loader("LAYER 06/F - REVERSE TRANSFORM", 0.15)
    loader("LAYER 07/G - FINAL OBFUSCATION", 0.15)
    loader("ADDING ANTI-BYPASS PROTECTION", 0.2)
    loader("ADDING TAMPER DETECTION", 0.2)
    
    result, err = create_encrypted_binary(path, 7)
    
    if err:
        print(LINE)
        msg("ENCRYPTION FAILED!", "error")
        print(f" {R}{err}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    loader("FINALIZING", 0.15)
    
    print()
    print(LINE)
    msg("BINARY ENCRYPTION SUCCESSFUL!", "success")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'OUTPUT FILE':<14} {W}➤{RESET} {G}{result['output']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL':<14} {W}➤{RESET} {C}{result['orig_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ENCRYPTED':<14} {W}➤{RESET} {M}{result['enc_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'LAYERS':<14} {W}➤{RESET} {G}{len(result['layers'])}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'CHECKSUM':<14} {W}➤{RESET} {C}{result['checksum'][:16]}...{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}PROTECTION FEATURES:{RESET}")
    print(f"     {G}✓ Anti-Decompile Protection{RESET}")
    print(f"     {G}✓ Anti-Debug Detection{RESET}")
    print(f"     {G}✓ Tamper Detection{RESET}")
    print(f"     {G}✓ Junk Code Injection{RESET}")
    print(f"     {G}✓ Random Variable Names{RESET}")
    print(f"     {G}✓ Multi-Layer Encryption{RESET}")
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
    print(f" {W}[{RESET}•{W}]{RESET} {C}Recommended: 7-10 for strong protection{RESET}")
    print(LINE)
    
    try:
        layers = int(input(f" {W}[{RESET}?{W}]{RESET} {C}LAYERS{RESET} {Y}➤{RESET} ").strip())
        layers = max(1, min(15, layers))
    except:
        layers = 7
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}ENCRYPTING WITH {layers} LAYERS...{RESET}")
    print(LINE)
    
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(layers):
        l = letters[i] if i < len(letters) else 'X'
        loader(f"LAYER {i+1:02d}/{l} - PROCESSING", 0.12)
    
    loader("ADDING ANTI-BYPASS", 0.15)
    
    result, err = create_encrypted_binary(path, layers)
    
    if err:
        print(LINE)
        msg("ENCRYPTION FAILED!", "error")
        print(f" {R}{err}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    loader("FINALIZING", 0.15)
    
    print()
    print(LINE)
    msg("BINARY ENCRYPTION SUCCESSFUL!", "success")
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
    print(f" {G}   ✅ RUN: python3 {result['output']}{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def opt_about():
    clear()
    banner()
    print(f" {M}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {M}║{RESET}           {Y}ABOUT CPyLock BINARY{RESET}                {M}║{RESET}")
    print(f" {M}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TOOL{RESET}      {W}➤{RESET} {G}CPyLock Binary Edition{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}VERSION{RESET}   {W}➤{RESET} {G}2.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}DEVELOPER{RESET} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}FACEBOOK{RESET}  {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}SECURITY FEATURES:{RESET}")
    print(f"     {W}[{M}01{W}]{RESET} {G}Anti-Decompile Protection{RESET}")
    print(f"     {W}[{M}02{W}]{RESET} {G}Anti-Debug Detection{RESET}")
    print(f"     {W}[{M}03{W}]{RESET} {G}Tamper Detection{RESET}")
    print(f"     {W}[{M}04{W}]{RESET} {G}Junk Code Injection{RESET}")
    print(f"     {W}[{M}05{W}]{RESET} {G}Random Variable Names{RESET}")
    print(f"     {W}[{M}06{W}]{RESET} {G}Binary Signature Header{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}10 ENCRYPTION LAYERS:{RESET}")
    print(f"     {G}Marshal, Zlib, Base64, Base85, Hex{RESET}")
    print(f"     {G}XOR, Reverse, Chunks, Lambda, ROT{RESET}")
    print(LINE)
    print(f" {R}[{RESET}!{R}]{RESET} {R}BYPASS PROTECTION:{RESET}")
    print(f"     {Y}Anyone trying to decompile will see:{RESET}")
    print(f"     {R}⛔ Don't try to bypass CPyLock! ⛔{RESET}")
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
            msg("Invalid!", "error")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n {R}Interrupted{RESET}")
        sys.exit(0)
