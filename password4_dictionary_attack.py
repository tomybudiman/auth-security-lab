"""
AFL-3 Sistem Autentikasi - Password
Soal #4: Dictionary attack (wordlist)
Algoritma: hash = MD5(PIN)
Target sama dengan Soal #1 (pembuktian silang).
Wordlist: pinlist.txt (1000 kandidat PIN, salah satunya adalah PIN target)

Cara pakai:
    1. Taruh file pinlist.txt di folder yang sama dengan script ini
       (atau ubah WORDLIST_PATH di bawah)
    2. python3 password4_dictionary_attack.py
"""

import hashlib
import time
import os

TARGET_HASH = "0110b96270248f746ecca06f1ce09746"
WORDLIST_PATH = "pinlist.txt"


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def crack(target_hash: str, wordlist_path: str):
    if not os.path.exists(wordlist_path):
        print(f"[-] File wordlist tidak ditemukan: {wordlist_path}")
        print("    Taruh pinlist.txt di folder yang sama lalu jalankan ulang.")
        return None, 0

    checked = 0
    with open(wordlist_path, "r") as f:
        for line in f:
            candidate = line.strip()
            if not candidate:
                continue
            checked += 1
            if md5(candidate) == target_hash:
                return candidate, checked
    return None, checked


def main():
    print("=== Soal #4: Dictionary attack (wordlist) ===")
    print(f"Target hash : {TARGET_HASH}")
    print(f"Wordlist    : {WORDLIST_PATH}\n")

    start = time.time()
    pin, checked = crack(TARGET_HASH, WORDLIST_PATH)
    elapsed = time.time() - start

    if pin:
        print(f"[+] PIN ditemukan     : {pin}")
        print(f"[+] Verifikasi MD5({pin}) = {md5(pin)}")
        print(f"[+] Match             : {md5(pin) == TARGET_HASH}")
        print(f"[+] Jumlah kandidat dicek sebelum ketemu: {checked}")
    else:
        if checked:
            print(f"[-] PIN tidak ditemukan di {checked} kandidat dalam wordlist.")

    print(f"\nWaktu eksekusi: {elapsed:.3f} detik")


if __name__ == "__main__":
    main()
