import hashlib
import time

TARGET_HASH = "8d4c531eb4b0f54df72aa6839abbeaec"
SALT_CANDIDATES = "0123456789"


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def crack(target_hash: str):
    for salt in SALT_CANDIDATES:
        for n in range(1_000_000):
            pin = f"{n:06d}"
            if md5(salt + pin) == target_hash:
                return salt, pin
    return None, None


def main():
    print("=== Soal #2: Brute-force + unknown salt (1 digit) ===")
    print(f"Target hash : {TARGET_HASH}")
    print(f"Salt candidates : {list(SALT_CANDIDATES)}")
    print("Mencoba semua kombinasi salt x PIN...\n")

    start = time.time()
    salt, pin = crack(TARGET_HASH)
    elapsed = time.time() - start

    if pin:
        combo = salt + pin
        print(f"[+] Salt ditemukan : {salt}")
        print(f"[+] PIN ditemukan  : {pin}")
        print(f"[+] Verifikasi MD5({salt!r} || {pin!r}) = {md5(combo)}")
        print(f"[+] Match          : {md5(combo) == TARGET_HASH}")
    else:
        print("[-] Kombinasi salt+PIN tidak ditemukan.")

    print(f"\nWaktu eksekusi: {elapsed:.3f} detik")


if __name__ == "__main__":
    main()
