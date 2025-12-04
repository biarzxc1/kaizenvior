#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════╗
║          CYTHON COMPILER - BY KEN DRICK                   ║
║          FACEBOOK: facebook.com/ryoevisu                  ║
╚═══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import shutil
import subprocess

# --- NEON COLOR PALETTE ---
R = '\033[1;31m'
G = '\033[1;32m'
C = '\033[1;36m'
Y = '\033[1;33m'
M = '\033[1;35m'
B = '\033[1;34m'
W = '\033[1;37m'
BG_R = '\033[41m'
BG_G = '\033[42m'
BG_C = '\033[46m'
RESET = '\033[0m'

# --- UI CONSTANTS ---
LINE = f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

# --- GLOBAL CONFIG ---
HOME_DIR = os.path.expanduser("~")
DOWNLOAD_DIR = "/storage/emulated/0/Download"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner_header():
    print(f"""{C}
   ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔  ╔═╗╔═╗╔╦╗╔═╗╦╦  ╔═╗╦═╗
   ║  ╚╦╝ ║ ╠═╣║ ║║║║  ║  ║ ║║║║╠═╝║║  ║╣ ╠╦╝
   ╚═╝ ╩  ╩ ╩ ╩╚═╝╝╚╝  ╚═╝╚═╝╩ ╩╩  ╩╩═╝╚═╝╩╚═
    {RESET}""")
    
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'GITHUB':<13} {W}➤{RESET} {G}RYO GRAHHH{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}2.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    
    tool_name = f"{R}[ {BG_R}{W}CYTHON COMPILER{RESET}{R} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL NAME':<13} {W}➤{RESET} {tool_name}")
    print(LINE)

def show_menu():
    def key(n, c): return f"{W}[{C}{n}{Y}/{C}{c}{W}]{RESET}"
    
    print(f" {key('01', 'A')} {G}COMPILE TO .SO FILE{RESET}")
    print(f" {key('02', 'B')} {G}COMPILE WITH WRAPPER{RESET}")
    print(f" {key('03', 'C')} {G}CHECK DEPENDENCIES{RESET}")
    print(f" {key('04', 'D')} {G}INSTALL DEPENDENCIES{RESET}")
    print(f" {key('05', 'E')} {G}ABOUT TOOL{RESET}")
    print(f" {key('00', 'X')} {R}EXIT TOOL{RESET}")
    print(LINE)

def nice_loader(text="PROCESSING", duration=1.5):
    bar_length = 30
    for i in range(bar_length + 1):
        progress = i / bar_length
        filled = int(bar_length * progress)
        bar = f"{G}{'█' * filled}{W}{'░' * (bar_length - filled)}{RESET}"
        percent = int(progress * 100)
        sys.stdout.write(f"\r {Y}[{RESET} {bar} {Y}]{RESET} {W}{percent}%{RESET} {C}{text}{RESET}")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    print()

def status_msg(msg, status="info"):
    if status == "success":
        print(f" {G}[{RESET}✓{G}]{RESET} {G}{msg}{RESET}")
    elif status == "error":
        print(f" {R}[{RESET}✗{R}]{RESET} {R}{msg}{RESET}")
    elif status == "warning":
        print(f" {Y}[{RESET}!{Y}]{RESET} {Y}{msg}{RESET}")
    else:
        print(f" {W}[{RESET}•{W}]{RESET} {C}{msg}{RESET}")

def check_command(cmd):
    return shutil.which(cmd) is not None

def check_python_module(module):
    try:
        __import__(module)
        return True
    except ImportError:
        return False

def check_all_dependencies():
    deps = {
        'python3': check_command('python3') or check_command('python'),
        'gcc/clang': check_command('gcc') or check_command('clang'),
        'cython': check_python_module('Cython'),
        'setuptools': check_python_module('setuptools'),
    }
    return deps

def get_writable_temp_dir():
    candidates = [
        os.path.join(HOME_DIR, ".cython_build"),
        os.path.join(HOME_DIR, "cython_temp"),
        os.path.join(DOWNLOAD_DIR, ".cython_build"),
    ]
    
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            test_file = os.path.join(path, ".test")
            with open(test_file, 'w') as f:
                f.write("t")
            os.remove(test_file)
            return path
        except:
            continue
    return HOME_DIR

def get_output_dir():
    if os.path.exists(DOWNLOAD_DIR):
        return DOWNLOAD_DIR
    output = os.path.join(HOME_DIR, "cython_output")
    os.makedirs(output, exist_ok=True)
    return output

def compile_to_so(filepath, verbose=True):
    """Compile Python to .so using Cython"""
    
    if not os.path.exists(filepath):
        return None, "File not found"
    
    if not filepath.endswith('.py'):
        return None, "Only .py files supported"
    
    # Validate syntax
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, filepath, 'exec')
    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    except Exception as e:
        return None, f"Cannot read file: {e}"
    
    filename = os.path.basename(filepath)
    name = os.path.splitext(filename)[0]
    original_size = os.path.getsize(filepath)
    
    temp_dir = get_writable_temp_dir()
    output_dir = get_output_dir()
    build_dir = os.path.join(temp_dir, f"build_{name}_{int(time.time())}")
    
    try:
        os.makedirs(build_dir, exist_ok=True)
        if verbose:
            status_msg(f"Build dir: {build_dir}")
    except Exception as e:
        return None, f"Cannot create build dir: {e}"
    
    try:
        # Copy source
        src_copy = os.path.join(build_dir, filename)
        shutil.copy(filepath, src_copy)
        if verbose:
            status_msg("Source copied")
        
        # Create setup.py
        setup_content = f'''from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        Extension("{name}", ["{filename}"], extra_compile_args=["-O2"]),
        compiler_directives={{"language_level": "3"}}
    )
)
'''
        with open(os.path.join(build_dir, "setup.py"), 'w') as f:
            f.write(setup_content)
        
        if verbose:
            status_msg("Setup.py created")
            status_msg("Compiling... (this may take a moment)")
        
        # Compile
        env = os.environ.copy()
        env['HOME'] = HOME_DIR
        
        proc = subprocess.Popen(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            cwd=build_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        
        stdout, stderr = proc.communicate(timeout=300)
        
        if proc.returncode != 0:
            err = stderr.decode('utf-8', errors='ignore') or stdout.decode('utf-8', errors='ignore')
            shutil.rmtree(build_dir, ignore_errors=True)
            return None, f"Compilation failed:\n{err[:800]}"
        
        if verbose:
            status_msg("Compilation done")
        
        # Find .so
        so_file = None
        for f in os.listdir(build_dir):
            if f.endswith('.so') or f.endswith('.pyd'):
                so_file = os.path.join(build_dir, f)
                break
        
        if not so_file:
            shutil.rmtree(build_dir, ignore_errors=True)
            return None, ".so file not found after compilation"
        
        if verbose:
            status_msg(f"Found: {os.path.basename(so_file)}")
        
        # Copy output
        out_name = f"{name}-output.so"
        out_path = os.path.join(output_dir, out_name)
        shutil.copy(so_file, out_path)
        os.chmod(out_path, 0o755)
        
        compiled_size = os.path.getsize(out_path)
        
        if verbose:
            status_msg("Output saved")
        
        # Always create runner script
        runner_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════
    COMPILED BY CYTHON COMPILER
    DEVELOPER: KEN DRICK
    FACEBOOK: facebook.com/ryoevisu
═══════════════════════════════════════════════════════════
"""
import sys, os, importlib.util

script_dir = os.path.dirname(os.path.abspath(__file__))
so_file = os.path.join(script_dir, "{out_name}")

if not os.path.exists(so_file):
    # Try to find any matching .so file
    for f in os.listdir(script_dir):
        if f.startswith("{name}") and f.endswith((".so", ".pyd")):
            so_file = os.path.join(script_dir, f)
            break

if not os.path.exists(so_file):
    print("Error: Compiled module not found!")
    sys.exit(1)

try:
    spec = importlib.util.spec_from_file_location("{name}", so_file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["{name}"] = mod
    spec.loader.exec_module(mod)
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
'''
        
        runner_path = os.path.join(output_dir, f"{name}-output.py")
        with open(runner_path, 'w') as f:
            f.write(runner_code)
        os.chmod(runner_path, 0o755)
        
        if verbose:
            status_msg("Runner script created")
        
        # Cleanup
        shutil.rmtree(build_dir, ignore_errors=True)
        
        return {
            'output_path': out_path,
            'runner_path': runner_path,
            'original_size': original_size,
            'compiled_size': compiled_size,
            'original_file': filepath,
            'module_name': name,
        }, None
        
    except subprocess.TimeoutExpired:
        shutil.rmtree(build_dir, ignore_errors=True)
        return None, "Compilation timed out"
    except Exception as e:
        shutil.rmtree(build_dir, ignore_errors=True)
        return None, f"Error: {str(e)}"

def compile_with_wrapper(filepath):
    result, error = compile_to_so(filepath, verbose=True)
    if error:
        return None, error
    
    name = result['module_name']
    output_dir = os.path.dirname(result['output_path'])
    so_file = os.path.basename(result['output_path'])
    
    wrapper = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPILED BY CYTHON COMPILER
DEVELOPER: KEN DRICK
REQUIRES: {so_file}
"""
import sys, os, importlib.util

script_dir = os.path.dirname(os.path.abspath(__file__))
so = None
for f in os.listdir(script_dir):
    if f.startswith("{name}") and f.endswith((".so", ".pyd")):
        so = os.path.join(script_dir, f)
        break

if not so:
    print("Error: .so file not found!")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("{name}", so)
mod = importlib.util.module_from_spec(spec)
sys.modules["{name}"] = mod
spec.loader.exec_module(mod)
'''
    
    wrapper_path = os.path.join(output_dir, f"{name}-wrapper.py")
    with open(wrapper_path, 'w') as f:
        f.write(wrapper)
    os.chmod(wrapper_path, 0o755)
    
    result['wrapper_path'] = wrapper_path
    return result, None

def option_compile_so():
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}         {Y}COMPILE TO .SO FILE{RESET}                  {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    deps = check_all_dependencies()
    missing = [k for k, v in deps.items() if not v]
    
    if missing:
        status_msg(f"Missing: {', '.join(missing)}", "error")
        print(f" {Y}Run option [04/D] to install{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}Enter path to Python file{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {G}Example: /storage/emulated/0/Download/test.py{RESET}")
    print(LINE)
    
    filepath = input(f" {W}[{RESET}?{W}]{RESET} {C}FILE PATH{RESET} {Y}➤{RESET} ").strip()
    
    if not filepath:
        status_msg("No path provided!", "error")
        time.sleep(2)
        return
    
    filepath = os.path.expanduser(filepath)
    
    if not os.path.exists(filepath):
        status_msg(f"Not found: {filepath}", "error")
        time.sleep(2)
        return
    
    if not filepath.endswith('.py'):
        status_msg("Only .py files!", "error")
        time.sleep(2)
        return
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}COMPILING...{RESET}")
    print(LINE)
    
    nice_loader("STEP 01/A - PREPARING", 0.3)
    
    result, error = compile_to_so(filepath, verbose=True)
    
    if error:
        print(LINE)
        status_msg("FAILED", "error")
        print(f" {R}{error}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    nice_loader("STEP 02/B - FINALIZING", 0.3)
    
    print()
    print(LINE)
    status_msg("COMPILATION SUCCESSFUL!", "success")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'INPUT':<12} {W}➤{RESET} {C}{result['original_file']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'SO FILE':<12} {W}➤{RESET} {G}{result['output_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'RUNNER':<12} {W}➤{RESET} {G}{result['runner_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL':<12} {W}➤{RESET} {C}{result['original_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COMPILED':<12} {W}➤{RESET} {M}{result['compiled_size']} bytes{RESET}")
    print(LINE)
    print(f" {R}[{RESET}!{R}]{RESET} {R}IMPORTANT: You CANNOT run .so directly!{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {C}HOW TO RUN:{RESET}")
    print(f"     {G}python3 {result['runner_path']}{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def option_compile_wrapper():
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}        {Y}COMPILE WITH WRAPPER{RESET}                  {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    deps = check_all_dependencies()
    missing = [k for k, v in deps.items() if not v]
    
    if missing:
        status_msg(f"Missing: {', '.join(missing)}", "error")
        print(f" {Y}Run option [04/D] to install{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}Enter path to Python file{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {G}Example: /storage/emulated/0/Download/test.py{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {C}Creates: .so + wrapper .py{RESET}")
    print(LINE)
    
    filepath = input(f" {W}[{RESET}?{W}]{RESET} {C}FILE PATH{RESET} {Y}➤{RESET} ").strip()
    
    if not filepath:
        status_msg("No path provided!", "error")
        time.sleep(2)
        return
    
    filepath = os.path.expanduser(filepath)
    
    if not os.path.exists(filepath):
        status_msg(f"Not found: {filepath}", "error")
        time.sleep(2)
        return
    
    if not filepath.endswith('.py'):
        status_msg("Only .py files!", "error")
        time.sleep(2)
        return
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}COMPILING WITH WRAPPER...{RESET}")
    print(LINE)
    
    nice_loader("STEP 01/A - PREPARING", 0.3)
    
    result, error = compile_with_wrapper(filepath)
    
    if error:
        print(LINE)
        status_msg("FAILED", "error")
        print(f" {R}{error}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    nice_loader("STEP 02/B - WRAPPER", 0.2)
    nice_loader("STEP 03/C - FINALIZING", 0.2)
    
    print()
    print(LINE)
    status_msg("COMPILATION SUCCESSFUL!", "success")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'INPUT':<12} {W}➤{RESET} {C}{result['original_file']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'SO FILE':<12} {W}➤{RESET} {G}{result['output_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'WRAPPER':<12} {W}➤{RESET} {G}{result['wrapper_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL':<12} {W}➤{RESET} {C}{result['original_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COMPILED':<12} {W}➤{RESET} {M}{result['compiled_size']} bytes{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}USAGE:{RESET}")
    print(f"     {G}python3 {result['wrapper_path']}{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def option_check_deps():
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}        {Y}CHECK DEPENDENCIES{RESET}                    {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    nice_loader("CHECKING", 0.5)
    
    deps = check_all_dependencies()
    
    print()
    print(LINE)
    
    for dep, ok in deps.items():
        if ok:
            print(f" {W}[{RESET}•{W}]{RESET} {C}{dep:<15}{RESET} {W}➤{RESET} {G}OK ✓{RESET}")
        else:
            print(f" {W}[{RESET}•{W}]{RESET} {C}{dep:<15}{RESET} {W}➤{RESET} {R}MISSING ✗{RESET}")
    
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}PYTHON{RESET}    {W}➤{RESET} {G}{sys.version.split()[0]}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}PLATFORM{RESET}  {W}➤{RESET} {G}{sys.platform}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}HOME{RESET}      {W}➤{RESET} {G}{HOME_DIR}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}OUTPUT{RESET}    {W}➤{RESET} {G}{get_output_dir()}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TEMP{RESET}      {W}➤{RESET} {G}{get_writable_temp_dir()}{RESET}")
    print(LINE)
    
    missing = [k for k, v in deps.items() if not v]
    if missing:
        status_msg(f"Missing: {', '.join(missing)}", "error")
    else:
        status_msg("All OK!", "success")
    
    print(LINE)
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def option_install_deps():
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}       {Y}INSTALL DEPENDENCIES{RESET}                   {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    print(f" {W}[{RESET}•{W}]{RESET} {C}TERMUX:{RESET}")
    print(f"     {G}pkg update && pkg upgrade{RESET}")
    print(f"     {G}pkg install python clang{RESET}")
    print(f"     {G}pip install cython setuptools{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}LINUX:{RESET}")
    print(f"     {G}sudo apt install python3-dev gcc{RESET}")
    print(f"     {G}pip3 install cython setuptools{RESET}")
    print(LINE)
    
    ans = input(f" {W}[{RESET}?{W}]{RESET} {Y}Install pip packages? (y/n){RESET} {Y}➤{RESET} ").strip().lower()
    
    if ans in ['y', 'yes']:
        print()
        for pkg in ['cython', 'setuptools']:
            status_msg(f"Installing {pkg}...")
            try:
                r = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--user', pkg],
                    capture_output=True, timeout=120
                )
                if r.returncode == 0:
                    status_msg(f"{pkg} OK", "success")
                else:
                    status_msg(f"{pkg} failed", "error")
            except Exception as e:
                status_msg(str(e), "error")
        
        print(LINE)
        status_msg("Done! Install clang/gcc manually", "warning")
    
    print(LINE)
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def option_about():
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}             {Y}ABOUT THIS TOOL{RESET}                   {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TOOL{RESET}      {W}➤{RESET} {G}CYTHON COMPILER{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}VERSION{RESET}   {W}➤{RESET} {G}2.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}DEVELOPER{RESET} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}FACEBOOK{RESET}  {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}DESCRIPTION:{RESET}")
    print(f"     {G}Compiles Python (.py) to binary (.so){RESET}")
    print(f"     {G}using Cython. Protects your source code.{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FEATURES:{RESET}")
    print(f"     {W}[{C}01/A{W}]{RESET} {G}Compile to .so{RESET}")
    print(f"     {W}[{C}02/B{W}]{RESET} {G}Compile + wrapper{RESET}")
    print(f"     {W}[{C}03/C{W}]{RESET} {G}Check dependencies{RESET}")
    print(f"     {W}[{C}04/D{W}]{RESET} {G}Install dependencies{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}BENEFITS:{RESET}")
    print(f"     {G}• Code protection{RESET}")
    print(f"     {G}• Faster execution{RESET}")
    print(f"     {G}• Cannot decompile{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def main():
    while True:
        clear()
        banner_header()
        show_menu()
        
        ch = input(f" {W}[{RESET}?{W}]{RESET} {C}SELECT{RESET} {Y}➤{RESET} ").strip().upper()
        
        if ch in ['01', '1', 'A']:
            option_compile_so()
        elif ch in ['02', '2', 'B']:
            option_compile_wrapper()
        elif ch in ['03', '3', 'C']:
            option_check_deps()
        elif ch in ['04', '4', 'D']:
            option_install_deps()
        elif ch in ['05', '5', 'E']:
            option_about()
        elif ch in ['00', '0', 'X']:
            clear()
            banner_header()
            status_msg("Thank you!", "success")
            print(LINE)
            sys.exit(0)
        else:
            status_msg("Invalid!", "error")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n {R}Interrupted{RESET}")
        sys.exit(0)
