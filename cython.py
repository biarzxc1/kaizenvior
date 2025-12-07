# ----------------------------------------------------------------------------------- #
# Mazram Obfuscator                                                                   #
# Author: AK                                                                          # 
# Date: 7/23/24                                                                       #
# Version: 1.1 (Fixed by Claude)                                                      #
#                                                                                     #
# Created to protect your source code                                                 #
# 100% protection is not guaranteed as it's my first time making something like this. #
# ----------------------------------------------------------------------------------- #

import os
import sys
import zlib
import base64
import platform
from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension
import subprocess
import colorama

colorama.init()

print(colorama.Fore.MAGENTA+"""

___  ___                                _____ _      __                     _             
|  \/  |                               |  _  | |    / _|                   | |            
| .  . | __ _ _____ __ __ _ _ __ ___   | | | | |__ | |_ _   _ ___  ___ __ _| |_ ___  _ __ 
| |\/| |/ _` |_  / '__/ _` | '_ ` _ \  | | | | '_ \|  _| | | / __|/ __/ _` | __/ _ \| '__|
| |  | | (_| |/ /| | | (_| | | | | | | \ \_/ / |_) | | | |_| \__ \ (_| (_| | || (_) | |   
\_|  |_/\__,_/___|_|  \__,_|_| |_| |_|  \___/|_.__/|_|  \__,_|___/\___\__,_|\__\___/|_|   
                                                                                          
""")
print(colorama.Fore.MAGENTA+"Created by AK (Fixed by Claude)")
print("")
print(colorama.Fore.YELLOW+"""
DISCLAIMER: THIS TOOL WAS CREATED TO OBFUSCATE PYTHON CODE TO MAKE IT HARDER FOR PEOPLE TO REVERSE ENGINEER AND EXTRACT SOURCE CODE FOR YOUR PROGRAMS. 
            THIS IS NO WAY MEANT TO BE USED MALICIOUSLY AND THIS IS NOT GUARANTEED TO PROTECT YOUR CODE 100%.
      
      """)

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

def obfuscate_and_compile():
    file_path = input(colorama.Fore.LIGHTCYAN_EX+"Enter path to python file: ")
    
    # Validate file type
    if not file_path.endswith('.py'):
        print(colorama.Fore.RED+"[ERROR]: Invalid file type, only support python files")
        return
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(colorama.Fore.RED+f"[ERROR]: File not found: {file_path}")
        return
    
    print("")
    requirements_file = input(colorama.Fore.LIGHTGREEN_EX+"Please provide the path to your requirements.txt file (leave blank to skip): ")
    
    # Get the absolute path and extract directory and filename
    file_path = os.path.abspath(file_path)
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    base_name = file_name.replace('.py', '')
    
    # Change to the file's directory
    original_dir = os.getcwd()
    os.chdir(file_dir)
    
    print(colorama.Fore.CYAN+f"\n[INFO] Working in directory: {file_dir}")
    print(colorama.Fore.CYAN+f"[INFO] Processing file: {file_name}")
    
    try:
        # Read the original code
        with open(file_name, 'r') as file:
            code = file.read()
        
        # Compress and encode
        compressed_code = zlib.compress(code.encode('utf-8'))
        encoded_code = base64.b64encode(compressed_code).decode('utf-8')
        
        # Create obfuscated file
        temp_file_name = f'{base_name}_obfuscated.py'
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
        
        print(colorama.Fore.GREEN+f"[SUCCESS] Created obfuscated file: {temp_file_name}")
        
        # Compile with Cython
        print(colorama.Fore.CYAN+"[INFO] Compiling with Cython...")
        module_name = f'{base_name}_obfuscated'
        extensions = [Extension(module_name, [temp_file_name])]
        setup(
            ext_modules=cythonize(extensions, compiler_directives={'language_level': '3'}),
            script_args=['build_ext', '--inplace']
        )
        
        print(colorama.Fore.GREEN+"[SUCCESS] Cython compilation complete")
        
        # Get the correct extension for this platform
        platform_ext = get_platform_extension()
        compiled_file = f'{module_name}{platform_ext}'
        
        # Create run script
        run_script_name = f'{base_name}_run.py'
        with open(run_script_name, 'w') as run_script:
            run_script.write(f"""
import importlib

# Import the compiled module
module_name = '{module_name}'
compiled_module = importlib.import_module(module_name)

# Execute the module's main function if it exists
if hasattr(compiled_module, 'main'):
    compiled_module.main()
""")
        
        print(colorama.Fore.GREEN+f"[SUCCESS] Created run script: {run_script_name}")
        
        # Prepare PyInstaller command
        hidden_imports = ['zlib', 'base64', 'Cython', 'importlib']
        if requirements_file and os.path.exists(requirements_file):
            with open(requirements_file, 'r') as req_file:
                for line in req_file:
                    package = line.strip().split('==')[0].split('>=')[0].split('<=')[0]
                    if package and not package.startswith('#'):
                        hidden_imports.append(package)
        
        hidden_imports_args = []
        for hidden_import in hidden_imports:
            hidden_imports_args.extend(['--hidden-import', hidden_import])
        
        # Run PyInstaller
        print(colorama.Fore.CYAN+"[INFO] Running PyInstaller...")
        pyinstaller_cmd = [
            'pyinstaller', 
            '--onefile', 
            '--add-data', f'{compiled_file};.',
            *hidden_imports_args, 
            run_script_name
        ]
        
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(colorama.Fore.GREEN+"[SUCCESS] PyInstaller completed successfully")
        else:
            print(colorama.Fore.YELLOW+"[WARNING] PyInstaller finished with warnings")
            if result.stderr:
                print(colorama.Fore.YELLOW+f"Details: {result.stderr[:500]}")
        
        # Clean up temporary files
        print(colorama.Fore.CYAN+"[INFO] Cleaning up temporary files...")
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        if os.path.exists(run_script_name):
            os.remove(run_script_name)
        
        # Report final location
        dist_dir = os.path.join(file_dir, 'dist')
        print(colorama.Fore.GREEN+f"\n{'='*70}")
        print(colorama.Fore.GREEN+f"[SUCCESS] Executable created successfully!")
        print(colorama.Fore.CYAN+f"[INFO] Location: {dist_dir}")
        print(colorama.Fore.YELLOW+f"[NOTE] Executable might take a while to run on first launch")
        print(colorama.Fore.GREEN+f"{'='*70}\n")
        
    except Exception as e:
        print(colorama.Fore.RED+f"[ERROR] An error occurred: {str(e)}")
        import traceback
        print(colorama.Fore.RED+traceback.format_exc())
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    try:
        obfuscate_and_compile()
    except KeyboardInterrupt:
        print(colorama.Fore.YELLOW+"\n\n[INFO] Operation cancelled by user")
    except Exception as e:
        print(colorama.Fore.RED+f"\n[ERROR] Fatal error: {str(e)}")
