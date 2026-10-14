"""
AFL-3 Sistem Autentikasi - Password
Soal #3: Brute-force + unknown salt (1 digit) + KDF (3x)
Algoritma:
    h0 = salt || PIN
    h1 = MD5(h0)
    h2 = MD5(h1)
    h3 = MD5(h2)  -> final hash
salt 1 digit, digabung di depan, salt tidak diberikan.
PIN target: 6 digit, 000000-999999, zero padding

Cara pakai:
    python3 password_bruteforce_salt_kdf.py
"""

import hashlib
import time

TARGET_HASH = "b20f8b0405b88e2b0b50eb3356d34ba7"
SALT_CANDIDATES = "0123456789"


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def kdf3(h0: str) -> str:
    h1 = md5(h0)
    h2 = md5(h1)
    h3 = md5(h2)
    return h3


def crack(target_hash: str):
    for salt in SALT_CANDIDATES:
        for n in range(1_000_000):
            pin = f"{n:06d}"
            h0 = salt + pin
            if kdf3(h0) == target_hash:
                return salt, pin
    return None, None


def main():
    print("=== Soal #3: Brute-force + salt (1 digit) + KDF (3x MD5) ===")
    print(f"Target hash : {TARGET_HASH}")
    print(f"Salt candidates : {list(SALT_CANDIDATES)}")
    print("Mencoba semua kombinasi salt x PIN dengan 3x hashing MD5...\n")

    start = time.time()
    salt, pin = crack(TARGET_HASH)
    elapsed = time.time() - start

    if pin:
        h0 = salt + pin
        h1 = md5(h0)
        h2 = md5(h1)
        h3 = md5(h2)
        print(f"[+] Salt ditemukan : {salt}")
        print(f"[+] PIN ditemukan  : {pin}")
        print(f"[+] h0 = {h0!r}")
        print(f"[+] h1 = MD5(h0) = {h1}")
        print(f"[+] h2 = MD5(h1) = {h2}")
        print(f"[+] h3 = MD5(h2) = {h3}  <- final")
        print(f"[+] Match          : {h3 == TARGET_HASH}")
    else:
        print("[-] Kombinasi salt+PIN tidak ditemukan.")

    print(f"\nWaktu eksekusi: {elapsed:.3f} detik")


if __name__ == "__main__":
    main()
