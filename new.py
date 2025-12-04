#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════╗
║          CYTHON COMPILER v3.0 - BY KEN DRICK              ║
║          FACEBOOK: facebook.com/ryoevisu                  ║
╚═══════════════════════════════════════════════════════════╝

IMPORTANT: This tool must be run ON THE SAME DEVICE where you 
want to use the compiled .so file. Compiled binaries are 
architecture-specific (ARM for Termux, x86 for PC).
"""

import os
import sys
import time
import shutil
import subprocess

# --- COLORS ---
R = '\033[1;31m'
G = '\033[1;32m'
C = '\033[1;36m'
Y = '\033[1;33m'
M = '\033[1;35m'
W = '\033[1;37m'
BG_R = '\033[41m'
RESET = '\033[0m'

LINE = f"{G}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}"

HOME = os.path.expanduser("~")
DOWNLOAD = "/storage/emulated/0/Download"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{C}
   ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔  ╔═╗╔═╗╔╦╗╔═╗╦╦  ╔═╗╦═╗
   ║  ╚╦╝ ║ ╠═╣║ ║║║║  ║  ║ ║║║║╠═╝║║  ║╣ ╠╦╝
   ╚═╝ ╩  ╩ ╩ ╩╚═╝╝╚╝  ╚═╝╚═╝╩ ╩╩  ╩╩═╝╚═╝╩╚═
    {RESET}""")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'DEVELOPER':<13} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'VERSION':<13} {W}➤{RESET} {G}3.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'FACEBOOK':<13} {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    tool = f"{R}[ {BG_R}{W}CYTHON COMPILER{RESET}{R} ]{RESET}"
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'TOOL NAME':<13} {W}➤{RESET} {tool}")
    print(LINE)

def menu():
    def k(n, c): return f"{W}[{C}{n}{Y}/{C}{c}{W}]{RESET}"
    print(f" {k('01', 'A')} {G}COMPILE PYTHON TO BINARY{RESET}")
    print(f" {k('02', 'B')} {G}CHECK DEPENDENCIES{RESET}")
    print(f" {k('03', 'C')} {G}INSTALL DEPENDENCIES{RESET}")
    print(f" {k('04', 'D')} {G}ABOUT{RESET}")
    print(f" {k('00', 'X')} {R}EXIT{RESET}")
    print(LINE)

def loader(text, duration=1.0):
    for i in range(31):
        bar = f"{G}{'█' * i}{W}{'░' * (30 - i)}{RESET}"
        sys.stdout.write(f"\r {Y}[{RESET} {bar} {Y}]{RESET} {W}{int(i*100/30)}%{RESET} {C}{text}{RESET}")
        sys.stdout.flush()
        time.sleep(duration / 30)
    print()

def msg(text, t="info"):
    icons = {"success": (G, "✓"), "error": (R, "✗"), "warn": (Y, "!"), "info": (W, "•")}
    c, i = icons.get(t, (W, "•"))
    print(f" {c}[{RESET}{i}{c}]{RESET} {c if t != 'info' else C}{text}{RESET}")

def has_cmd(cmd):
    return shutil.which(cmd) is not None

def has_mod(mod):
    try:
        __import__(mod)
        return True
    except:
        return False

def check_deps():
    return {
        'python': has_cmd('python3') or has_cmd('python'),
        'compiler': has_cmd('clang') or has_cmd('gcc'),
        'cython': has_mod('Cython'),
        'setuptools': has_mod('setuptools'),
    }

def get_temp():
    for p in [f"{HOME}/.cython_build", f"{HOME}/cython_tmp", f"{DOWNLOAD}/.cython"]:
        try:
            os.makedirs(p, exist_ok=True)
            test = os.path.join(p, ".t")
            open(test, 'w').close()
            os.remove(test)
            return p
        except:
            pass
    return HOME

def get_output():
    if os.path.exists(DOWNLOAD):
        return DOWNLOAD
    p = f"{HOME}/cython_out"
    os.makedirs(p, exist_ok=True)
    return p

def compile_python(filepath):
    """Compile .py to .so with runner script"""
    
    # Validate
    if not os.path.exists(filepath):
        return None, "File not found"
    if not filepath.endswith('.py'):
        return None, "Only .py files supported"
    
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        compile(code, filepath, 'exec')
    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    except Exception as e:
        return None, f"Cannot read: {e}"
    
    name = os.path.splitext(os.path.basename(filepath))[0]
    orig_size = os.path.getsize(filepath)
    
    temp = get_temp()
    out_dir = get_output()
    build = os.path.join(temp, f"b_{name}_{int(time.time())}")
    
    try:
        os.makedirs(build, exist_ok=True)
        msg(f"Build: {build}")
        
        # Copy source
        src = os.path.join(build, f"{name}.py")
        shutil.copy(filepath, src)
        msg("Source copied")
        
        # Create setup.py
        setup = f'''from setuptools import setup, Extension
from Cython.Build import cythonize
setup(ext_modules=cythonize(Extension("{name}", ["{name}.py"]), compiler_directives={{"language_level": "3"}}))
'''
        with open(os.path.join(build, "setup.py"), 'w') as f:
            f.write(setup)
        msg("Setup created")
        
        # Compile
        msg("Compiling (please wait)...")
        
        env = os.environ.copy()
        env['HOME'] = HOME
        
        proc = subprocess.run(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            cwd=build, capture_output=True, text=True, timeout=600, env=env
        )
        
        if proc.returncode != 0:
            err = proc.stderr or proc.stdout
            return None, f"Compile failed:\n{err[:500]}"
        
        msg("Compiled successfully")
        
        # Find .so file
        so_file = None
        for f in os.listdir(build):
            if f.endswith('.so') or f.endswith('.pyd'):
                so_file = os.path.join(build, f)
                break
        
        if not so_file:
            return None, ".so not found"
        
        so_name = os.path.basename(so_file)
        msg(f"Found: {so_name}")
        
        # Copy .so to output with ORIGINAL name preserved in extension
        final_so = os.path.join(out_dir, f"{name}_compiled.so")
        shutil.copy(so_file, final_so)
        os.chmod(final_so, 0o755)
        
        so_size = os.path.getsize(final_so)
        msg("Binary saved")
        
        # Create runner script (DIFFERENT NAME - adds _run suffix)
        runner_name = f"{name}_run.py"
        runner_path = os.path.join(out_dir, runner_name)
        
        runner_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════
    COMPILED BY CYTHON COMPILER v3.0
    DEVELOPER: KEN DRICK
    FACEBOOK: facebook.com/ryoevisu
    
    RUN THIS FILE TO EXECUTE YOUR COMPILED CODE
═══════════════════════════════════════════════════════════
"""
import sys
import os
import importlib.util

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for the compiled .so file
    so_file = None
    for f in os.listdir(script_dir):
        if f.startswith("{name}") and (f.endswith(".so") or f.endswith(".pyd")):
            so_file = os.path.join(script_dir, f)
            break
    
    if not so_file:
        print("ERROR: Compiled module (.so) not found!")
        print(f"Make sure {name}_compiled.so is in the same folder as this script.")
        sys.exit(1)
    
    try:
        spec = importlib.util.spec_from_file_location("{name}", so_file)
        if spec is None:
            print("ERROR: Cannot load module spec")
            sys.exit(1)
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["{name}"] = module
        spec.loader.exec_module(module)
        
    except Exception as e:
        print(f"ERROR: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        with open(runner_path, 'w') as f:
            f.write(runner_code)
        os.chmod(runner_path, 0o755)
        msg("Runner created")
        
        # Cleanup
        shutil.rmtree(build, ignore_errors=True)
        
        return {
            'so_path': final_so,
            'runner_path': runner_path,
            'orig_size': orig_size,
            'so_size': so_size,
            'name': name,
        }, None
        
    except subprocess.TimeoutExpired:
        shutil.rmtree(build, ignore_errors=True)
        return None, "Timeout"
    except Exception as e:
        shutil.rmtree(build, ignore_errors=True)
        return None, str(e)

def opt_compile():
    clear()
    banner()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}       {Y}COMPILE PYTHON TO BINARY{RESET}               {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    deps = check_deps()
    missing = [k for k, v in deps.items() if not v]
    
    if missing:
        msg(f"Missing: {', '.join(missing)}", "error")
        print(f" {Y}Run option [03/C] to install{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
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
    loader("STEP 01/A - PREPARING", 0.3)
    
    result, err = compile_python(path)
    
    if err:
        print(LINE)
        msg("COMPILATION FAILED!", "error")
        print(f" {R}{err}{RESET}")
        print(LINE)
        input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")
        return
    
    loader("STEP 02/B - FINALIZING", 0.2)
    
    print()
    print(LINE)
    msg("COMPILATION SUCCESSFUL!", "success")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'BINARY (.so)':<14} {W}➤{RESET} {G}{result['so_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'RUNNER (.py)':<14} {W}➤{RESET} {G}{result['runner_path']}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'ORIGINAL':<14} {W}➤{RESET} {C}{result['orig_size']} bytes{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}{'COMPILED':<14} {W}➤{RESET} {M}{result['so_size']} bytes{RESET}")
    print(LINE)
    print(f" {R}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {R}║{RESET} {Y}⚠️  HOW TO RUN YOUR COMPILED CODE:{RESET}            {R}║{RESET}")
    print(f" {R}╚═══════════════════════════════════════════════╝{RESET}")
    print(f" {G}   python3 {result['runner_path']}{RESET}")
    print()
    print(f" {R}   ❌ DO NOT run: python3 {result['so_path']}{RESET}")
    print(f" {R}   ❌ .so files cannot be run directly!{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def opt_check():
    clear()
    banner()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}          {Y}CHECK DEPENDENCIES{RESET}                  {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    loader("CHECKING", 0.5)
    
    deps = check_deps()
    
    print()
    for k, v in deps.items():
        s = f"{G}OK ✓{RESET}" if v else f"{R}MISSING ✗{RESET}"
        print(f" {W}[{RESET}•{W}]{RESET} {C}{k:<12}{RESET} {W}➤{RESET} {s}")
    
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}PYTHON{RESET}  {W}➤{RESET} {G}{sys.version.split()[0]}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}ARCH{RESET}    {W}➤{RESET} {G}{os.uname().machine}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TEMP{RESET}    {W}➤{RESET} {G}{get_temp()}{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}OUTPUT{RESET}  {W}➤{RESET} {G}{get_output()}{RESET}")
    print(LINE)
    
    missing = [k for k, v in deps.items() if not v]
    if missing:
        msg(f"Missing: {', '.join(missing)}", "error")
    else:
        msg("All dependencies OK!", "success")
    
    print(LINE)
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def opt_install():
    clear()
    banner()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}        {Y}INSTALL DEPENDENCIES{RESET}                  {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    
    print(f" {W}[{RESET}•{W}]{RESET} {C}FOR TERMUX:{RESET}")
    print(f"     {G}pkg update && pkg upgrade{RESET}")
    print(f"     {G}pkg install python clang{RESET}")
    print(f"     {G}pip install cython setuptools{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}FOR LINUX:{RESET}")
    print(f"     {G}sudo apt install python3-dev gcc{RESET}")
    print(f"     {G}pip3 install cython setuptools{RESET}")
    print(LINE)
    
    ans = input(f" {W}[{RESET}?{W}]{RESET} {Y}Install pip packages? (y/n){RESET} {Y}➤{RESET} ").strip().lower()
    
    if ans in ['y', 'yes']:
        print()
        for pkg in ['cython', 'setuptools']:
            msg(f"Installing {pkg}...")
            try:
                r = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--user', pkg],
                    capture_output=True, timeout=120
                )
                if r.returncode == 0:
                    msg(f"{pkg} OK", "success")
                else:
                    msg(f"{pkg} failed", "error")
            except Exception as e:
                msg(str(e), "error")
        
        print(LINE)
        msg("Done! Install clang manually: pkg install clang", "warn")
    
    print(LINE)
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def opt_about():
    clear()
    banner()
    print(f" {C}╔═══════════════════════════════════════════════╗{RESET}")
    print(f" {C}║{RESET}               {Y}ABOUT{RESET}                           {C}║{RESET}")
    print(f" {C}╚═══════════════════════════════════════════════╝{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {Y}TOOL{RESET}      {W}➤{RESET} {G}CYTHON COMPILER{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}VERSION{RESET}   {W}➤{RESET} {G}3.0.0{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}DEVELOPER{RESET} {W}➤{RESET} {G}KEN DRICK{RESET}")
    print(f" {W}[{RESET}•{W}]{RESET} {Y}FACEBOOK{RESET}  {W}➤{RESET} {G}facebook.com/ryoevisu{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}WHAT IT DOES:{RESET}")
    print(f"     {G}Compiles Python (.py) to binary (.so){RESET}")
    print(f"     {G}using Cython. Your source code becomes{RESET}")
    print(f"     {G}machine code that cannot be easily read.{RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}OUTPUT FILES:{RESET}")
    print(f"     {G}• yourfile_compiled.so  (the binary){RESET}")
    print(f"     {G}• yourfile_run.py       (runner script){RESET}")
    print(LINE)
    print(f" {W}[{RESET}•{W}]{RESET} {C}HOW TO USE:{RESET}")
    print(f"     {G}python3 yourfile_run.py{RESET}")
    print(LINE)
    print(f" {R}[{RESET}!{R}]{RESET} {R}IMPORTANT:{RESET}")
    print(f"     {Y}• You CANNOT run .so files directly{RESET}")
    print(f"     {Y}• Always use the _run.py script{RESET}")
    print(f"     {Y}• Compile ON Termux for Termux use{RESET}")
    print(LINE)
    
    input(f"\n {W}[{RESET}•{W}]{RESET} {Y}Press ENTER...{RESET}")

def main():
    while True:
        clear()
        banner()
        menu()
        
        ch = input(f" {W}[{RESET}?{W}]{RESET} {C}SELECT{RESET} {Y}➤{RESET} ").strip().upper()
        
        if ch in ['01', '1', 'A']:
            opt_compile()
        elif ch in ['02', '2', 'B']:
            opt_check()
        elif ch in ['03', '3', 'C']:
            opt_install()
        elif ch in ['04', '4', 'D']:
            opt_about()
        elif ch in ['00', '0', 'X']:
            clear()
            banner()
            msg("Goodbye!", "success")
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
