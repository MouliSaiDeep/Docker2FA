# Secure 2FA Microservice – Student Project (23MH1A05N0)

A fully containerized, production-quality microservice that implements RSA-based secure seed transfer, TOTP generation, and 2FA verification. This project demonstrates strong cryptography principles, Docker-based deployment, and automated Cron logging.

Built as part of the PKI + Docker assignment.

## Features

### Secure Seed Decryption
* Encrypted seed is received from the instructor API.
* Decrypted using RSA Private Key (`student_private_key.pem`) with OAEP + SHA-256.
* Seed stored safely inside a Docker volume so it persists across restarts.

### TOTP Generation (RFC 6238)
* Generates standard 6-digit TOTP codes.
* SHA-1 based, 30-second window.
* Compatible with Google Authenticator-style systems.

### Code Verification
* Accepts user-provided TOTP codes.
* Supports a time drift tolerance of ±30 seconds.

### Fully Dockerized
* Multi-stage Python build resulting in a small, optimized final image.
* Mounted volumes for seed storage and cron logs.
* Built and deployed using `docker-compose`.

### Automated Cron Logging
* Cron job runs every minute.
* Logs the latest generated 2FA code inside the container.

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11 |
| **Framework** | FastAPI |
| **Cryptography** | cryptography (RSA/OAEP), pyotp (TOTP), hashlib |
| **Containerization** | Docker, Docker Compose |
| **Scheduling** | Linux Cron |
| **Communication** | Instructor API (AWS Lambda) |

## Project Structure

```text
├── main.py                    # FastAPI application + seed decrypt + TOTP logic
├── generate_keys.py           # Generates RSA keypair (4096-bit)
├── generate_proof.py          # Generates commit signature proof
├── get_encrypted_seed.py      # Fetches encrypted seed from Instructor API
├── student_private_key.pem    # Your private key (DO NOT COMMIT)
├── student_public_key.pem     # Public key sent to instructor
├── instructor_public.pem      # Instructor’s RSA public key
│
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Service + volume definitions
│
├── cron/
│   └── 2fa-cron               # Cron schedule (runs every minute)
│
├── scripts/
│   └── log_2fa_cron.py        # Cron script to generate & log codes
│
└── encrypted_seed.txt         # Received from Instructor API (ignored in git)

Setup & Installation
Prerequisites
Docker Desktop installed

Git installed

Python (Note: Docker runs the service, but local Python is used for initial key generation)

1. Clone Your Repository
Bash

git clone [https://github.com/MouliSaiDeep/Docker2FA](https://github.com/MouliSaiDeep/Docker2FA)
cd Docker2FA
2. Generate RSA Keys (One Time Only)
Bash

python generate_keys.py
This creates:

student_private_key.pem

student_public_key.pem

3. Request Your Encrypted Seed
Bash

python get_encrypted_seed.py
This calls the Instructor API and saves encrypted_seed.txt.

4. Build & Run
Bash

docker-compose up --build -d
The microservice is now available at: http://localhost:8080

API Endpoints
1. Decrypt Seed
Decrypts the instructor-provided encrypted seed and stores it in /data/seed.txt.

URL: /decrypt-seed

Method: POST

Body:

JSON

{
  "encrypted_seed": "BASE64_STRING_HERE"
}
2. Generate Current TOTP Code
URL: /generate-2fa

Method: GET

Response:

JSON

{
  "code": "123456",
  "valid_for": 18
}
3. Verify a TOTP Code
URL: /verify-2fa

Method: POST

Body:

JSON

{
  "code": "123456"
}
Response:

JSON

{
  "valid": true
}
Cron Job & Persistence
Persistence
The seed is stored inside a mounted volume at /data. This ensures the seed survives container restarts.

Cron Logging
A scheduled Cron task runs every minute and logs the latest 2FA code. To view these logs, run the following command:

Bash

docker exec <container_name> cat /cron/last_code.txt
Summary
This project implements strong RSA-based PKI encryption, secure seed handling, standards-compliant TOTP, a Dockerized FastAPI service, background cron automation, and persistent storage using volumes.