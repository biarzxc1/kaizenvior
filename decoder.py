#!/usr/bin/env python3
"""
Python Decoder for Termux/Android
Works with /storage/emulated/0/ paths
"""

import sys
import base64
import binascii
import marshal
import lzma
import zlib
import re
import os
from pathlib import Path

def decode_base64(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        return base64.b64decode(data), "Base64"
    except:
        return None, None

def decode_base85(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        return base64.b85decode(data), "Base85"
    except:
        return None, None

def decode_base32(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        return base64.b32decode(data), "Base32"
    except:
        return None, None

def decode_hex(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        return binascii.unhexlify(data), "Hex"
    except:
        return None, None

def decode_lzma(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        return lzma.decompress(data), "LZMA"
    except:
        return None, None

def decode_zlib(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        return zlib.decompress(data), "Zlib"
    except:
        return None, None

def decode_marshal(data):
    try:
        if isinstance(data, str):
            data = data.encode()
        result = marshal.loads(data)
        return str(result), "Marshal"
    except:
        return None, None

def try_all_decoders(data):
    """Try all available decoders in order"""
    decoders = [
        decode_base85,  # Try Base85 first (like your original file)
        decode_base64,
        decode_base32,
        decode_hex,
        decode_lzma,
        decode_zlib,
        decode_marshal,
    ]
    
    for decoder in decoders:
        result, method = decoder(data)
        if result is not None:
            return result, method
    
    return None, None

def extract_encoded_content(file_content):
    """Extract encoded content from Python file"""
    
    # Pattern 1: encoded_content = b'...'
    pattern1 = r"encoded_content\s*=\s*b['\"]([^'\"]+)['\"]"
    match = re.search(pattern1, file_content, re.DOTALL)
    if match:
        encoded_str = match.group(1)
        # Handle escape sequences properly
        return encoded_str.encode('utf-8')
    
    # Pattern 2: Look for large base64/base85 strings (100+ chars)
    pattern2 = r"b['\"]([A-Za-z0-9+/=_\-~!@#$%^&*(){}[\]|:;<>,.?]{100,})['\"]"
    match = re.search(pattern2, file_content, re.DOTALL)
    if match:
        return match.group(1).encode('utf-8')
    
    # Pattern 3: exec(decode(...)) pattern
    pattern3 = r"exec\([^)]*b['\"]([^'\"]+)['\"]"
    match = re.search(pattern3, file_content, re.DOTALL)
    if match:
        return match.group(1).encode('utf-8')
    
    return None

def auto_decode_recursive(data, max_depth=15):
    """Recursively decode data until no more encoding is detected"""
    decode_chain = []
    current_data = data
    
    for depth in range(max_depth):
        decoded, method = try_all_decoders(current_data)
        
        if decoded is None:
            break
        
        decode_chain.append(method)
        print(f"  ✓ Layer {depth + 1}: {method}")
        
        # Check if it's readable Python code
        try:
            if isinstance(decoded, bytes):
                decoded_str = decoded.decode('utf-8', errors='ignore')
                if 'import' in decoded_str or 'def ' in decoded_str or 'class ' in decoded_str:
                    print(f"  ✓ Found Python code!")
                    return decoded_str, decode_chain
        except:
            pass
        
        current_data = decoded
    
    # Final conversion to string if bytes
    if isinstance(current_data, bytes):
        try:
            current_data = current_data.decode('utf-8', errors='ignore')
        except:
            pass
    
    return current_data, decode_chain

def decode_file(input_file, output_file=None):
    """Main function to decode a file"""
    try:
        # Expand path if it contains ~
        input_file = os.path.expanduser(input_file)
        
        # Check if file exists
        if not os.path.exists(input_file):
            print(f"❌ Error: File not found: {input_file}")
            return None
        
        # Read the file
        print(f"\n📂 Reading: {input_file}")
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(f"📊 File size: {len(content)} bytes")
        
        # Extract encoded content
        print("🔎 Extracting encoded content...")
        encoded_data = extract_encoded_content(content)
        
        if encoded_data is None:
            print("⚠️  No encoded pattern found, trying full file...")
            encoded_data = content.encode('utf-8')
        else:
            print("✓ Encoded content found!")
        
        # Decode recursively
        print("\n🔍 Starting decode process...")
        decoded_content, decode_chain = auto_decode_recursive(encoded_data)
        
        if not decode_chain:
            print("\n⚠️  No encoding detected or already decoded")
            return None
        
        print(f"\n✅ Success!")
        print(f"📊 Decode chain: {' → '.join(decode_chain)}")
        
        # Determine output file
        if output_file is None:
            # Get the directory and filename
            input_path = Path(input_file)
            output_file = str(input_path.parent / f"{input_path.stem}_decoded{input_path.suffix}")
        
        # Save decoded content
        print(f"\n💾 Saving to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            # Add header
            header = f'''"""
Decoded from: {input_file}
Decode chain: {' → '.join(decode_chain)}
Decoded by: Python Decoder Tool
"""

'''
            f.write(header)
            f.write(str(decoded_content))
        
        print(f"✓ File saved successfully!")
        print(f"📊 Output size: {os.path.getsize(output_file)} bytes")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║         PYTHON DECODER - TERMUX/ANDROID VERSION          ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    if len(sys.argv) < 2:
        print("📝 Usage:")
        print("  python decoder_termux.py <input_file> [output_file]")
        print("\n📋 Examples:")
        print("  python decoder_termux.py /storage/emulated/0/Download/example.py")
        print("  python decoder_termux.py example.py decoded.py")
        print("  python decoder_termux.py ~/Download/tool.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = decode_file(input_file, output_file)
    
    if result:
        print(f"\n🎉 Decoding complete!")
        print(f"📁 Decoded file: {result}")
    else:
        print(f"\n❌ Decoding failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
