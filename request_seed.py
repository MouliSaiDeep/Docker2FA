import requests
import json
import sys

STUDENT_ID = "23MH1A05N0"
GITHUB_REPO_URL = "https://github.com/MouliSaiDeep/Docker2FA" 
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def get_encrypted_seed():
    print(f"🔹 preparing request for Student ID: {STUDENT_ID}")

    try:
        with open("student_public.pem", "r") as f:
            public_key_content = f.read()
    except FileNotFoundError:
        print("Error: student_public.pem not found. Did you run Step 2?")
        return

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key_content
    }

    print("🔹 Sending request to Instructor API...")
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status() # Raise error for bad status codes (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"   Server response: {e.response.text}")
        return

    try:
        data = response.json()
        if "encrypted_seed" not in data:
            print("Error: Response did not contain 'encrypted_seed'")
            print(f"Full response: {data}")
            return
            
        encrypted_seed = data["encrypted_seed"]
        print("Received encrypted seed successfully!")
        
    except json.JSONDecodeError:
        print("Error: Could not parse server response as JSON.")
        return

    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)
    
    print("Saved to encrypted_seed.txt")
    print("REMINDER: Do NOT commit encrypted_seed.txt to your repository.")

if __name__ == "__main__":
    get_encrypted_seed()