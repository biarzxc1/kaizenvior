#!/usr/bin/env python3
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
        if f.startswith("new") and (f.endswith(".so") or f.endswith(".pyd")):
            so_file = os.path.join(script_dir, f)
            break
    
    if not so_file:
        print("ERROR: Compiled module (.so) not found!")
        print(f"Make sure new_compiled.so is in the same folder as this script.")
        sys.exit(1)
    
    try:
        spec = importlib.util.spec_from_file_location("new", so_file)
        if spec is None:
            print("ERROR: Cannot load module spec")
            sys.exit(1)
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["new"] = module
        spec.loader.exec_module(module)
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
