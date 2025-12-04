#!/usr/bin/env python3
"""
encrypt_tool.py

Usage:
  python encrypt_tool.py encrypt /storage/emulated/0/Download/example.py
This writes:
  /storage/emulated/0/Download/example.enc
  /storage/emulated/0/Download/example-runner.py
The runner will prompt for the passphrase at runtime to decrypt and execute in memory.
"""
import sys
import os
import getpass
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

DOWNLOADS = "/storage/emulated/0/Download"

def derive_key(passphrase: str, salt: bytes, iterations: int = 200000) -> bytes:
    # PBKDF2-HMAC-SHA256 -> 32-byte key
    return PBKDF2(passphrase.encode("utf-8"), salt, dkLen=32, count=iterations)

def encrypt_file(src_path: str, out_path: str, passphrase: str):
    with open(src_path, "rb") as f:
        plaintext = f.read()
    salt = get_random_bytes(16)
    key = derive_key(passphrase, salt)
    nonce = get_random_bytes(12)  # recommended size for GCM
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    # Store: salt(16) | nonce(12) | tag(16) | ciphertext
    blob = salt + nonce + tag + ciphertext
    with open(out_path, "wb") as f:
        f.write(blob)
    print(f"Encrypted -> {out_path}")

def write_runner(enc_filename: str, runner_path: str):
    # The runner will ask for passphrase at runtime to avoid embedding secrets.
    runner_code = f'''#!/usr/bin/env python3
# example-runner.py  (auto-generated)
import os, sys, getpass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

ENC_PATH = r"{enc_filename}"

def derive_key(passphrase: str, salt: bytes, iterations: int = 200000) -> bytes:
    return PBKDF2(passphrase.encode("utf-8"), salt, dkLen=32, count=iterations)

def decrypt_and_exec(path):
    if not os.path.exists(path):
        sys.exit("Encrypted file not found: " + path)
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 16+12+16:
        sys.exit("Encrypted file corrupted or too small.")
    salt = data[0:16]
    nonce = data[16:28]
    tag = data[28:44]
    ciphertext = data[44:]
    passphrase = getpass.getpass("Enter passphrase to decrypt and run: ")
    key = derive_key(passphrase, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except Exception as e:
        sys.exit("Decryption failed: " + str(e))
    # Execute in a fresh module namespace
    globs = {{'__name__': '__main__', '__file__': None}}
    exec(plaintext, globs)

if __name__ == '__main__':
    decrypt_and_exec(ENC_PATH)
'''
    with open(runner_path, "w") as f:
        f.write(runner_code)
    os.chmod(runner_path, 0o755)
    print(f"Runner written -> {runner_path}")

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "encrypt":
        print("Usage: python encrypt_tool.py encrypt /path/to/source.py")
        sys.exit(1)
    src = sys.argv[2]
    if not os.path.exists(src):
        print("Source not found:", src); sys.exit(1)
    # default names based on source
    src_basename = os.path.basename(src)
    name_root = os.path.splitext(src_basename)[0]
    enc_out = os.path.join(DOWNLOADS, f"{name_root}.enc")
    runner_out = os.path.join(DOWNLOADS, f"{name_root}-runner.py")

    # prompt passphrase (twice)
    pass1 = getpass.getpass("Enter new passphrase (will be required to run): ")
    pass2 = getpass.getpass("Confirm passphrase: ")
    if pass1 != pass2:
        print("Passphrases did not match."); sys.exit(1)
    encrypt_file(src, enc_out, pass1)
    write_runner(enc_out, runner_out)
    print("Done. To run:")
    print(f"  python {runner_out}")

if __name__ == '__main__':
    main()
