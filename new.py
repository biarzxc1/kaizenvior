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
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}1.0.0{RESET}")
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

def check_command(cmd):
    """Check if a command exists"""
    return shutil.which(cmd) is not None

def check_python_module(module):
    """Check if a Python module is installed"""
    try:
        __import__(module)
        return True
    except ImportError:
        return False

def get_python_version():
    """Get Python version info"""
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def check_all_dependencies():
    """Check all required dependencies"""
    deps = {
        'python3': check_command('python3'),
        'gcc': check_command('gcc') or check_command('clang'),
        'cython': check_python_module('Cython'),
        'setuptools': check_python_module('setuptools'),
    }
    return deps

def compile_to_so(filepath):
    """Compile a Python file to .so using Cython"""
    try:
        # Validate file exists
        if not os.path.exists(filepath):
            return None, "File not found"
        
        if not filepath.endswith('.py'):
            return None, "Only Python (.py) files are supported"
        
        # Get file info
        file_dir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        
        # Set output directory
        output_dir = "/storage/emulated/0/Download"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Create temp build directory
        build_dir = f"/tmp/cython_build_{name}_{int(time.time())}"
        os.makedirs(build_dir, exist_ok=True)
        
        # Copy source file to build dir
        shutil.copy(filepath, os.path.join(build_dir, filename))
        
        # Create setup.py for compilation
        python_version = get_python_version()
        setup_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import sys

ext_modules = [
    Extension(
        "{name}",
        ["{filename}"],
        extra_compile_args=["-O3", "-fPIC"],
    )
]

setup(
    name="{name}",
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={{
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
        }},
        annotate=False,
    ),
    zip_safe=False,
)
'''
        
        setup_path = os.path.join(build_dir, "setup.py")
        with open(setup_path, 'w') as f:
            f.write(setup_content)
        
        # Run compilation
        original_dir = os.getcwd()
        os.chdir(build_dir)
        
        result = subprocess.run(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            capture_output=True,
            text=True
        )
        
        os.chdir(original_dir)
        
        if result.returncode != 0:
            # Cleanup
            shutil.rmtree(build_dir, ignore_errors=True)
            error_msg = result.stderr if result.stderr else result.stdout
            return None, f"Compilation failed:\n{error_msg[:500]}"
        
        # Find the .so file
        so_file = None
        for f in os.listdir(build_dir):
            if f.endswith('.so') or f.endswith('.pyd'):
                so_file = f
                break
        
        if not so_file:
            shutil.rmtree(build_dir, ignore_errors=True)
            return None, "Compilation completed but .so file not found"
        
        # Copy to output directory
        output_filename = f"{name}-output.so"
        output_path = os.path.join(output_dir, output_filename)
        shutil.copy(os.path.join(build_dir, so_file), output_path)
        
        # Get file sizes
        original_size = os.path.getsize(filepath)
        compiled_size = os.path.getsize(output_path)
        
        # Cleanup build directory
        shutil.rmtree(build_dir, ignore_errors=True)
        
        return {
            'output_path': output_path,
            'original_size': original_size,
            'compiled_size': compiled_size,
            'original_file': filepath,
        }, None
        
    except Exception as e:
        return None, str(e)

def compile_with_wrapper(filepath):
    """Compile to .so and create a Python wrapper to run it"""
    try:
        # First compile to .so
        result, error = compile_to_so(filepath)
        
        if error:
            return None, error
        
        # Get file info
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        output_dir = "/storage/emulated/0/Download"
        
        # Get the actual .so filename (it includes Python version)
        so_filename = f"{name}-output.so"
        
        # Create wrapper script
        wrapper_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════
    COMPILED BY CYTHON COMPILER
    DEVELOPER: KEN DRICK
    FACEBOOK: facebook.com/ryoevisu
    
    ⚠️  THIS IS A COMPILED BINARY WRAPPER
    ⚠️  REQUIRES: {so_filename}
═══════════════════════════════════════════════════════════
"""

import sys
import os
import importlib.util

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for the .so file
    so_file = None
    for f in os.listdir(script_dir):
        if f.startswith("{name}") and (f.endswith(".so") or f.endswith(".pyd")):
            so_file = os.path.join(script_dir, f)
            break
    
    if not so_file:
        print("Error: Compiled module (.so) not found!")
        print(f"Expected: {name}*.so in {{script_dir}}")
        sys.exit(1)
    
    # Load and execute the module
    try:
        spec = importlib.util.spec_from_file_location("{name}", so_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules["{name}"] = module
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error loading module: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        wrapper_path = os.path.join(output_dir, f"{name}-wrapper.py")
        with open(wrapper_path, 'w') as f:
            f.write(wrapper_content)
        
        result['wrapper_path'] = wrapper_path
        
        return result, None
        
    except Exception as e:
        return None, str(e)

def option_compile_so():
    """Option 1: Compile Python to .so"""
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}         {Y}COMPILE TO .SO FILE{RESET}                  {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    # Check dependencies first
    deps = check_all_dependencies()
    missing = [k for k, v in deps.items() if not v]
    
    if missing:
        print(f" {R}[{RESET}!{R}]{RESET} {R}MISSING DEPENDENCIES:{RESET}")
        for dep in missing:
            print(f"     {R}• {dep}{RESET}")
        print(LINE)
        print(f" {Y}[{RESET}•{Y}]{RESET} {Y}Please run option [04/D] to install dependencies{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")
        return
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}Enter the path to your Python file{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {G}Example: /storage/emulated/0/Download/test.py{RESET}")
    print(LINE)
    
    filepath = input(f" {W}[{RESET}?{W}]{RESET} {C}FILE PATH{RESET} {Y}➤{RESET} ").strip()
    
    if not filepath:
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}No file path provided!{RESET}")
        time.sleep(2)
        return
    
    if not os.path.exists(filepath):
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}File not found: {filepath}{RESET}")
        time.sleep(2)
        return
    
    if not filepath.endswith('.py'):
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}Only Python (.py) files are supported!{RESET}")
        time.sleep(2)
        return
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}COMPILING TO BINARY (.so)...{RESET}")
    print(LINE)
    
    nice_loader("STEP 01/A - PARSING SOURCE CODE", 0.5)
    nice_loader("STEP 02/B - GENERATING C CODE", 1.0)
    nice_loader("STEP 03/C - COMPILING TO BINARY", 1.5)
    nice_loader("STEP 04/D - FINALIZING OUTPUT", 0.5)
    
    result, error = compile_to_so(filepath)
    
    if error:
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}COMPILATION FAILED:{RESET}")
        print(f" {R}{error}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")
        return
    
    print()
    print(LINE)
    print(f" {G}[{RESET}✓{G}]{RESET} {G}COMPILATION SUCCESSFUL!{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'INPUT FILE':<15} {W}➤{RESET} {C}{result['original_file']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'OUTPUT FILE':<15} {W}➤{RESET} {G}{result['output_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL SIZE':<15} {W}➤{RESET} {C}{result['original_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COMPILED SIZE':<15} {W}➤{RESET} {M}{result['compiled_size']} bytes{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}HOW TO USE:{RESET}")
    print(f"     {G}python3 -c \"import {os.path.basename(filepath).replace('.py', '')}\"{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")

def option_compile_wrapper():
    """Option 2: Compile with wrapper"""
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}        {Y}COMPILE WITH WRAPPER{RESET}                  {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    # Check dependencies first
    deps = check_all_dependencies()
    missing = [k for k, v in deps.items() if not v]
    
    if missing:
        print(f" {R}[{RESET}!{R}]{RESET} {R}MISSING DEPENDENCIES:{RESET}")
        for dep in missing:
            print(f"     {R}• {dep}{RESET}")
        print(LINE)
        print(f" {Y}[{RESET}•{Y}]{RESET} {Y}Please run option [04/D] to install dependencies{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")
        return
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}Enter the path to your Python file{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {G}Example: /storage/emulated/0/Download/test.py{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}NOTE: This creates .so + wrapper .py file{RESET}")
    print(LINE)
    
    filepath = input(f" {W}[{RESET}?{W}]{RESET} {C}FILE PATH{RESET} {Y}➤{RESET} ").strip()
    
    if not filepath:
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}No file path provided!{RESET}")
        time.sleep(2)
        return
    
    if not os.path.exists(filepath):
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}File not found: {filepath}{RESET}")
        time.sleep(2)
        return
    
    if not filepath.endswith('.py'):
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}Only Python (.py) files are supported!{RESET}")
        time.sleep(2)
        return
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}COMPILING WITH WRAPPER...{RESET}")
    print(LINE)
    
    nice_loader("STEP 01/A - PARSING SOURCE CODE", 0.5)
    nice_loader("STEP 02/B - GENERATING C CODE", 1.0)
    nice_loader("STEP 03/C - COMPILING TO BINARY", 1.5)
    nice_loader("STEP 04/D - CREATING WRAPPER", 0.5)
    nice_loader("STEP 05/E - FINALIZING OUTPUT", 0.3)
    
    result, error = compile_with_wrapper(filepath)
    
    if error:
        print(f"\n {R}[{RESET}!{R}]{RESET} {R}COMPILATION FAILED:{RESET}")
        print(f" {R}{error}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")
        return
    
    print()
    print(LINE)
    print(f" {G}[{RESET}✓{G}]{RESET} {G}COMPILATION SUCCESSFUL!{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'INPUT FILE':<15} {W}➤{RESET} {C}{result['original_file']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'SO FILE':<15} {W}➤{RESET} {G}{result['output_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'WRAPPER FILE':<15} {W}➤{RESET} {G}{result['wrapper_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL SIZE':<15} {W}➤{RESET} {C}{result['original_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COMPILED SIZE':<15} {W}➤{RESET} {M}{result['compiled_size']} bytes{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}HOW TO USE:{RESET}")
    print(f"     {G}python3 {result['wrapper_path']}{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")

def option_check_deps():
    """Option 3: Check dependencies"""
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}        {Y}CHECK DEPENDENCIES{RESET}                    {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    nice_loader("CHECKING DEPENDENCIES", 1.0)
    
    deps = check_all_dependencies()
    
    print()
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}DEPENDENCY STATUS:{RESET}")
    print(LINE)
    
    for dep, installed in deps.items():
        status = f"{G}INSTALLED ✓{RESET}" if installed else f"{R}NOT FOUND ✗{RESET}"
        print(f" {W}[{RESET}•{W}]{RESET} {C}{dep:<15}{RESET} {W}➤{RESET} {status}")
    
    print(LINE)
    
    # Additional info
    print(f" {W}[{RESET}•{W}]{RESET} {Y}PYTHON VERSION{RESET}  {W}➤{RESET} {G}{sys.version.split()[0]}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}PLATFORM{RESET}        {W}➤{RESET} {G}{sys.platform}{RESET}")
    print(LINE)
    
    missing = [k for k, v in deps.items() if not v]
    if missing:
        print(f" {R}[{RESET}!{R}]{RESET} {R}Missing: {', '.join(missing)}{RESET}")
        print(f" {Y}[{RESET}•{Y}]{RESET} {Y}Run option [04/D] to install{RESET}")
    else:
        print(f" {G}[{RESET}✓{G}]{RESET} {G}All dependencies are installed!{RESET}")
    
    print(LINE)
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")

def option_install_deps():
    """Option 4: Install dependencies"""
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}       {Y}INSTALL DEPENDENCIES{RESET}                   {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    print(f" {W}[{RESET}•{W}]{RESET} {Y}INSTALLATION COMMANDS:{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FOR TERMUX:{RESET}")
    print(f"     {G}pkg update && pkg upgrade{RESET}")
    print(f"     {G}pkg install python clang{RESET}")
    print(f"     {G}pip install cython setuptools{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FOR LINUX (Debian/Ubuntu):{RESET}")
    print(f"     {G}sudo apt update{RESET}")
    print(f"     {G}sudo apt install python3-dev gcc{RESET}")
    print(f"     {G}pip3 install cython setuptools{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FOR ARCH LINUX:{RESET}")
    print(f"     {G}sudo pacman -S python gcc{RESET}")
    print(f"     {G}pip install cython setuptools{RESET}")
    print(LINE)
    
    confirm = input(f" {W}[{RESET}?{W}]{RESET} {Y}Auto-install Python packages? (y/n){RESET} {Y}➤{RESET} ").strip().lower()
    
    if confirm in ['y', 'yes']:
        print()
        print(LINE)
        print(f" {W}[{RESET}•{W}]{RESET} {Y}INSTALLING PYTHON PACKAGES...{RESET}")
        print(LINE)
        
        packages = ['cython', 'setuptools']
        
        for pkg in packages:
            print(f" {W}[{RESET}•{W}]{RESET} {C}Installing {pkg}...{RESET}")
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', pkg, '--quiet'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f" {G}[{RESET}✓{G}]{RESET} {G}{pkg} installed successfully{RESET}")
                else:
                    print(f" {R}[{RESET}!{R}]{RESET} {R}Failed to install {pkg}{RESET}")
            except Exception as e:
                print(f" {R}[{RESET}!{R}]{RESET} {R}Error: {e}{RESET}")
        
        print(LINE)
        print(f" {G}[{RESET}✓{G}]{RESET} {G}Installation complete!{RESET}")
        print(LINE)
        print(f" {Y}[{RESET}•{Y}]{RESET} {Y}NOTE: You still need to install gcc/clang manually{RESET}")
        print(f" {Y}[{RESET}•{Y}]{RESET} {Y}Termux: pkg install clang{RESET}")
        print(f" {Y}[{RESET}•{Y}]{RESET} {Y}Linux: sudo apt install gcc{RESET}")
    
    print(LINE)
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")

def option_about():
    """Option 5: About the tool"""
    clear()
    banner_header()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}             {Y}ABOUT THIS TOOL{RESET}                   {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TOOL NAME{RESET}       {W}➤{RESET} {G}CYTHON COMPILER{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}VERSION{RESET}         {W}➤{RESET} {G}1.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}DEVELOPER{RESET}       {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}FACEBOOK{RESET}        {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}DESCRIPTION:{RESET}")
    print(f"     {G}A powerful tool that compiles Python (.py){RESET}")
    print(f"     {G}files into binary shared objects (.so) using{RESET}")
    print(f"     {G}Cython. This protects your source code from{RESET}")
    print(f"     {G}being easily read or reverse-engineered.{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FEATURES:{RESET}")
    print(f"     {W}[{RESET}{C}01{Y}/{C}A{W}]{RESET} {G}Compile .py to .so binary{RESET}")
    print(f"     {W}[{RESET}{C}02{Y}/{C}B{W}]{RESET} {G}Create wrapper for easy execution{RESET}")
    print(f"     {W}[{RESET}{C}03{Y}/{C}C{W}]{RESET} {G}Dependency checker{RESET}")
    print(f"     {W}[{RESET}{C}04{Y}/{C}D{W}]{RESET} {G}Auto-install dependencies{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}BENEFITS:{RESET}")
    print(f"     {G}• Source code protection{RESET}")
    print(f"     {G}• Faster execution (compiled C){RESET}")
    print(f"     {G}• Cannot be easily decompiled{RESET}")
    print(f"     {G}• Professional distribution{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}REQUIREMENTS:{RESET}")
    print(f"     {G}• Python 3.6+{RESET}")
    print(f"     {G}• Cython{RESET}")
    print(f"     {G}• GCC or Clang compiler{RESET}")
    print(f"     {G}• setuptools{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}SUPPORTED PLATFORMS:{RESET}")
    print(f"     {G}• Termux (Android){RESET}")
    print(f"     {G}• Linux{RESET}")
    print(f"     {G}• macOS{RESET}")
    print(f"     {G}• Windows (with MinGW){RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER to continue...{RESET}")

def main():
    while True:
        clear()
        banner_header()
        show_menu()
        
        choice = input(f" {W}[{RESET}?{W}]{RESET} {C}SELECT OPTION{RESET} {Y}➤{RESET} ").strip().upper()
        
        if choice in ['01', '1', 'A']:
            option_compile_so()
        elif choice in ['02', '2', 'B']:
            option_compile_wrapper()
        elif choice in ['03', '3', 'C']:
            option_check_deps()
        elif choice in ['04', '4', 'D']:
            option_install_deps()
        elif choice in ['05', '5', 'E']:
            option_about()
        elif choice in ['00', '0', 'X']:
            clear()
            banner_header()
            print(f" {G}[{RESET}✓{G}]{RESET} {Y}Thank you for using CYTHON COMPILER!{RESET}")
            print(f" {W}[{RESET}•{W}]{RESET} {G}Goodbye!{RESET}")
            print(LINE)
            sys.exit(0)
        else:
            print(f"\n {R}[{RESET}!{R}]{RESET} {R}Invalid option! Please try again.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n {R}[{RESET}!{R}]{RESET} {Y}Program interrupted by user.{RESET}")
        sys.exit(0)
