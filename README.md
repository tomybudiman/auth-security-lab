# auth-security-lab

Practical exercises in authentication security — password hash cracking
(brute-force, salted hashes, iterative KDF, dictionary attack), X.509 certificate
chain analysis, and biometric/MFA authentication flows.

Repositori ini merupakan pengerjaan tugas **AFL-3: Sistem Autentikasi**. Tugas
terdiri dari 4 bagian: **Password cracking**, **X.509 Certificate investigation**,
**Biometrik**, dan **Multi-Factor Authentication (MFA)**. Bagian yang sudah
dikerjakan saat ini adalah **Password cracking**.

---

## Bagian 1 — Password Cracking

Target yang dipecahkan adalah PIN **6 digit** (`000000`–`999999`, dengan *zero
padding*) di balik berbagai skema hashing berbasis MD5. Setiap soal menaikkan
tingkat kesulitan: dari MD5 polos, menambahkan *salt*, menambahkan iterasi KDF,
hingga pendekatan *dictionary attack*.

### Prasyarat

- Python 3 (tanpa dependensi eksternal — hanya pustaka standar `hashlib`, `time`, `os`).

### Cara menjalankan

Jalankan tiap script langsung dari folder repo:

```bash
python3 password1_bruteforce_plain.py
python3 password2_bruteforce_salt.py
python3 password3_bruteforce_salt_kdf.py
python3 password4_dictionary_attack.py   # butuh pinlist.txt di folder yang sama
```

### Ringkasan hasil

| Soal | Script | Skema hash | Salt | PIN | Target hash |
|------|--------|-----------|:----:|:---:|-------------|
| #1 | `password1_bruteforce_plain.py` | `MD5(PIN)` | — | `202345` | `0110b96270248f746ecca06f1ce09746` |
| #2 | `password2_bruteforce_salt.py` | `MD5(salt‖PIN)` | `7` | `202345` | `8d4c531eb4b0f54df72aa6839abbeaec` |
| #3 | `password3_bruteforce_salt_kdf.py` | `MD5³(salt‖PIN)` (iterasi 3×) | `3` | `202345` | `b20f8b0405b88e2b0b50eb3356d34ba7` |
| #4 | `password4_dictionary_attack.py` | `MD5(PIN)` via wordlist | — | `202345` | `0110b96270248f746ecca06f1ce09746` |

---

### Soal #1 — Brute-force (plain MD5)

Skema: `hash = MD5(PIN)`. Script mencoba seluruh kombinasi PIN `000000`–`999999`
secara berurutan sampai hash-nya cocok dengan target.

<details>
<summary>Output eksekusi</summary>

```
=== Soal #1: Brute-force (plain MD5) ===
Target hash : 0110b96270248f746ecca06f1ce09746
Mencoba semua kombinasi PIN 000000-999999...

[+] PIN ditemukan : 202345
[+] Verifikasi MD5(202345) = 0110b96270248f746ecca06f1ce09746
[+] Match          : True

Waktu eksekusi: 0.101 detik
```
</details>

### Soal #2 — Brute-force + unknown salt (1 digit)

Skema: `hash = MD5(salt ‖ PIN)`, dengan *salt* 1 digit (`0`–`9`) yang digabung di
**depan** PIN dan tidak diketahui. Script membrute-force seluruh kombinasi
`salt × PIN`.

<details>
<summary>Output eksekusi</summary>

```
=== Soal #2: Brute-force + unknown salt (1 digit) ===
Target hash : 8d4c531eb4b0f54df72aa6839abbeaec
Salt candidates : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Mencoba semua kombinasi salt x PIN...

[+] Salt ditemukan : 7
[+] PIN ditemukan  : 202345
[+] Verifikasi MD5('7' || '202345') = 8d4c531eb4b0f54df72aa6839abbeaec
[+] Match          : True

Waktu eksekusi: 3.766 detik
```
</details>

### Soal #3 — Brute-force + salt + KDF (3× MD5)

Skema KDF iteratif:

```
h0 = salt ‖ PIN
h1 = MD5(h0)
h2 = MD5(h1)
h3 = MD5(h2)   ← final hash
```

Salt 1 digit (di depan) tidak diketahui, sehingga script membrute-force
`salt × PIN` lalu menerapkan 3× hashing MD5 pada tiap kandidat.

<details>
<summary>Output eksekusi</summary>

```
=== Soal #3: Brute-force + salt (1 digit) + KDF (3x MD5) ===
Target hash : b20f8b0405b88e2b0b50eb3356d34ba7
Salt candidates : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Mencoba semua kombinasi salt x PIN dengan 3x hashing MD5...

[+] Salt ditemukan : 3
[+] PIN ditemukan  : 202345
[+] h0 = '3202345'
[+] h1 = MD5(h0) = 06cc4d561dbd8d367a13a63619cbf56c
[+] h2 = MD5(h1) = 13aa4c7bc583634abf9e1d29360dc08c
[+] h3 = MD5(h2) = b20f8b0405b88e2b0b50eb3356d34ba7  <- final
[+] Match          : True

Waktu eksekusi: 4.255 detik
```
</details>

### Soal #4 — Dictionary attack (wordlist)

Skema: `hash = MD5(PIN)` dengan target **sama seperti Soal #1** (pembuktian
silang). Alih-alih brute-force seluruh ruang, script hanya mencoba kandidat dari
file `pinlist.txt` (satu PIN per baris). PIN target kebetulan ada di baris
pertama sehingga langsung ketemu pada percobaan ke-1.

> `pinlist.txt` disertakan di repo. Untuk memakai wordlist lain, ubah
> `WORDLIST_PATH` di dalam script.

<details>
<summary>Output eksekusi</summary>

```
=== Soal #4: Dictionary attack (wordlist) ===
Target hash : 0110b96270248f746ecca06f1ce09746
Wordlist    : pinlist.txt

[+] PIN ditemukan     : 202345
[+] Verifikasi MD5(202345) = 0110b96270248f746ecca06f1ce09746
[+] Match             : True
[+] Jumlah kandidat dicek sebelum ketemu: 1

Waktu eksekusi: 0.000 detik
```
</details>

---

## Refleksi

- **PIN yang sama (`202345`) muncul di tiga target berbeda meski salt-nya
  berbeda.** Artinya *salting* **tidak mengubah PIN**; ia hanya mengubah hash
  keluaran supaya hash yang bocor tidak bisa dicocokkan langsung antar sistem
  (mencegah serangan *rainbow table* yang sama dipakai ulang). Rahasia aslinya
  tetap identik.
- **Ruang kunci terlalu kecil.** PIN 6 digit hanya ~10⁶ kemungkinan dan bisa
  ditembus brute-force di bawah satu detik (Soal #1). Menambah salt 1 digit
  hanya mengalikan usaha ×10, dan KDF 3× MD5 hanya menaikkan biaya per tebakan
  sedikit — keduanya **tidak cukup** melindungi rahasia dengan entropi rendah.
- **MD5 cepat = buruk untuk password.** Fungsi hash yang cepat justru
  menguntungkan penyerang. Praktik yang benar memakai KDF lambat & ber-salt unik
  per pengguna (bcrypt, scrypt, Argon2) dengan *work factor* tinggi, bukan MD5.
- **Dictionary attack jauh lebih efisien** bila PIN termasuk pola umum/bocor:
  Soal #4 menemukan jawaban dalam 1 percobaan, dibanding memindai seluruh ruang.

---

## Struktur repo

```
.
├── password1_bruteforce_plain.py     # Soal #1 — brute-force MD5 polos
├── password2_bruteforce_salt.py      # Soal #2 — brute-force + salt 1 digit
├── password3_bruteforce_salt_kdf.py  # Soal #3 — brute-force + salt + KDF 3×
├── password4_dictionary_attack.py    # Soal #4 — dictionary attack
├── pinlist.txt                   # wordlist untuk Soal #4
└── README.md
```
