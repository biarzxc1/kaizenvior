# ----------------------------------------------------------------------------------- #
# Mazram Obfuscator                                                                   #
# Author: AK                                                                          # 
# Date: 7/23/24                                                                       #
# Version: 1.2 (Fixed for Termux by Claude)                                          #
#                                                                                     #
# Created to protect your source code                                                 #
# 100% protection is not guaranteed as it's my first time making something like this. #
# ----------------------------------------------------------------------------------- #

import os
import sys
import zlib
import base64
import platform
import shutil
import subprocess
import colorama

colorama.init()

print(colorama.Fore.MAGENTA+r"""

___  ___                                _____ _      __                     _             
|  \/  |                               |  _  | |    / _|                   | |            
| .  . | __ _ _____ __ __ _ _ __ ___   | | | | |__ | |_ _   _ ___  ___ __ _| |_ ___  _ __ 
| |\/| |/ _` |_  / '__/ _` | '_ ` _ \  | | | | '_ \|  _| | | / __|/ __/ _` | __/ _ \| '__|
| |  | | (_| |/ /| | | (_| | | | | | | \ \_/ / |_) | | | |_| \__ \ (_| (_| | || (_) | |   
\_|  |_/\__,_/___|_|  \__,_|_| |_| |_|  \___/|_.__/|_|  \__,_|___/\___\__,_|\__\___/|_|   
                                                                                          
""")
print(colorama.Fore.MAGENTA+"Created by AK (Fixed for Termux by Claude)")
print("")
print(colorama.Fore.YELLOW+"""
DISCLAIMER: THIS TOOL WAS CREATED TO OBFUSCATE PYTHON CODE TO MAKE IT HARDER FOR PEOPLE TO REVERSE ENGINEER AND EXTRACT SOURCE CODE FOR YOUR PROGRAMS. 
            THIS IS NO WAY MEANT TO BE USED MALICIOUSLY AND THIS IS NOT GUARANTEED TO PROTECT YOUR CODE 100%.
      
      """)

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
    output_file = f'{base_name}_obfuscated.py'
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
    
    if not os.path.exists(compiled_file):
        print(colorama.Fore.YELLOW+f"[WARNING] Expected compiled file not found: {compiled_file}")
        print(colorama.Fore.YELLOW+"[INFO] Listing available .so files:")
        for f in os.listdir('.'):
            if f.startswith(module_name) and ('.so' in f or '.pyd' in f):
                print(colorama.Fore.CYAN+f"  Found: {f}")
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
    
    print(colorama.Fore.GREEN+f"[SUCCESS] Created run script: {run_script_name}")
    
    return compiled_file, run_script_name, temp_file_name

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
    use_cython = input(colorama.Fore.LIGHTGREEN_EX+"Use Cython compilation? (more secure but requires Cython) [y/N]: ").lower().strip()
    use_cython = use_cython in ['y', 'yes']
    
    if use_cython and not check_cython_available():
        print(colorama.Fore.YELLOW+"[WARNING] Cython not available. Install with: pip install Cython")
        print(colorama.Fore.CYAN+"[INFO] Falling back to basic obfuscation...")
        use_cython = False
    
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
        
        if use_cython:
            compiled_file, run_script, temp_file = create_cython_obfuscated(file_path, file_name, base_name, code)
            
            # Create output directory
            output_dir = f'{base_name}_obfuscated_output'
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            
            # Copy files to output directory
            shutil.copy(compiled_file, output_dir)
            shutil.copy(run_script, output_dir)
            
            # Clean up temporary files
            print(colorama.Fore.CYAN+"[INFO] Cleaning up temporary files...")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Clean up build artifacts
            if os.path.exists('build'):
                shutil.rmtree('build')
            for f in os.listdir('.'):
                if f.endswith('.c'):
                    os.remove(f)
            
            print(colorama.Fore.GREEN+f"\n{'='*70}")
            print(colorama.Fore.GREEN+f"[SUCCESS] Obfuscated package created!")
            print(colorama.Fore.CYAN+f"[INFO] Location: {os.path.join(file_dir, output_dir)}")
            print(colorama.Fore.CYAN+f"[INFO] Run with: python {run_script} (from output directory)")
            print(colorama.Fore.YELLOW+f"[NOTE] Distribute the entire '{output_dir}' folder")
            print(colorama.Fore.GREEN+f"{'='*70}\n")
            
        else:
            output_file = create_simple_obfuscated(file_path, file_name, base_name, code)
            
            print(colorama.Fore.GREEN+f"\n{'='*70}")
            print(colorama.Fore.GREEN+f"[SUCCESS] Obfuscated file created!")
            print(colorama.Fore.CYAN+f"[INFO] Location: {os.path.join(file_dir, output_file)}")
            print(colorama.Fore.CYAN+f"[INFO] Run with: python {output_file}")
            print(colorama.Fore.YELLOW+f"[NOTE] This is basic obfuscation. For better protection, use Cython compilation.")
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
