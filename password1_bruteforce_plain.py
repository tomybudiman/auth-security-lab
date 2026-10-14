"""
AFL-3 Sistem Autentikasi - Password
Soal #1: Brute-force (plain)
Algoritma: hash = MD5(PIN)
PIN target: 6 digit, 000000-999999, zero padding

Cara pakai:
    python3 password1_bruteforce_plain.py
"""

import hashlib
import time

TARGET_HASH = "0110b96270248f746ecca06f1ce09746"


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def crack(target_hash: str):
    for n in range(1_000_000):
        pin = f"{n:06d}"
        if md5(pin) == target_hash:
            return pin
    return None


def main():
    print("=== Soal #1: Brute-force (plain MD5) ===")
    print(f"Target hash : {TARGET_HASH}")
    print("Mencoba semua kombinasi PIN 000000-999999...\n")

    start = time.time()
    pin = crack(TARGET_HASH)
    elapsed = time.time() - start

    if pin:
        print(f"[+] PIN ditemukan : {pin}")
        print(f"[+] Verifikasi MD5({pin}) = {md5(pin)}")
        print(f"[+] Match          : {md5(pin) == TARGET_HASH}")
    else:
        print("[-] PIN tidak ditemukan dalam ruang pencarian.")

    print(f"\nWaktu eksekusi: {elapsed:.3f} detik")


if __name__ == "__main__":
    main()
