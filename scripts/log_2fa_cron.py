import os
import time
import sys
import datetime
import base64
import hashlib
import pyotp

SEED_FILE = "/data/seed.txt"

def main():
    if not os.path.exists(SEED_FILE):
        print(f"[{datetime.datetime.utcnow()}] Seed file not found at {SEED_FILE}", file=sys.stderr)
        return

    try:
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
            
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        
        totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
        current_code = totp.now()
        
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - 2FA Code: {current_code}")
        
    except Exception as e:
        print(f"Error generating code: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()