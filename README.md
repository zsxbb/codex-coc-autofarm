# 🐼 CODEX COC FARM (Clash of Clans Automation Bot)

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](#)
[![OS](https://img.shields.io/badge/OS-Windows-green.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Google%20Play%20Games%20PC-orange.svg)](#)

Bilingual documentation / Dokumentasi dalam dua bahasa:
- **[Bahasa Indonesia (Default)](#-bahasa-indonesia)**
- **[English Version](#-english)**

---

## 🇮🇩 Bahasa Indonesia

**CODEX COC FARM** adalah bot otomatisasi farm Clash of Clans yang dirancang khusus untuk **Google Play Games PC (Windows)**. Bot ini bekerja secara real-time menggunakan pencocokan gambar (OpenCV/PyAutoGUI) untuk mendeteksi layar pertempuran, melakukan pencarian lawan, menurunkan pasukan/hero/mantra secara dinamis berdasarkan koordinat persen (independen terhadap ukuran jendela), dan mengaktifkan kemampuan hero pada waktu yang tepat.

Proyek ini dibuat dan dikembangkan oleh **zsxbb**.

---

### 📂 Struktur Direktori Project

```text
coc-python/
│
├── .gitignore               # Mencegah file cache & venv masuk ke GitHub
├── README.md                # Dokumentasi utama bot ini
├── RUN_CODEX_BOT.bat        # File batch sekali klik untuk menjalankan Bot Python
├── requirements.txt         # Daftar pustaka Python yang dibutuhkan
│
├── images-fix/              # Aset gambar referensi deteksi visual
│   ├── Attack_Green.png     # Contoh: Tombol Cari Lawan
│   ├── nexticon.png         # Contoh: Tombol Next / Cari Lain
│   └── ...                  # Aset gambar pasukan & tombol lainnya
│
└── scripts/                 # Kumpulan skrip utama Python
    ├── autoattack.py        # Skrip logika bot serangan otomatis
    └── get_spawn.py         # Skrip utilitas untuk merekam koordinat spawn
```

---

### 🚀 Panduan Setup & Cara Menjalankan

#### A. Persiapan Awal Game & Emulator
1. Buka **Google Play Games PC** dan jalankan **Clash of Clans**.
2. **PENTING**: Ubah bahasa game Clash of Clans Anda ke **English** agar deteksi tombol berjalan lancar.
3. **PENTING**: Pastikan game berjalan dalam mode **Full Screen** (Layar Penuh, tekan `F11` pada keyboard) atau jendela dimaksimalkan agar koordinat pertempuran dan deteksi gambar OpenCV akurat serta konsisten.

---

#### B. Menjalankan Bot
Anda tidak perlu menginstal library Python secara manual. File batch `RUN_CODEX_BOT.bat` akan secara otomatis membuat virtual environment lokal (`codex_venv`) dan menginstal semua requirements yang dibutuhkan.

1. **Jalankan Bot**:
   - Klik dua kali file **`RUN_CODEX_BOT.bat`** di direktori utama.
   - Jika ini pertama kali dijalankan, ketik `Y` saat diminta untuk melakukan instalasi otomatis.
2. **Pilih Menu**:
   - **`[1] START BOT`**: Menjalankan siklus serangan pertempuran secara otomatis.
   - **`[2] RECORD SPAWN POINTS`**: Membuka program perekam titik spawn untuk merekam koordinat di luar wilayah base lawan.

> [!TIP]
> Jika klik dari bot tidak merespons di dalam game Clash of Clans, klik kanan pada file **`RUN_CODEX_BOT.bat`** lalu pilih **Run as Administrator** (Jalankan sebagai Administrator).

---

#### C. Menggunakan Perekam Titik Spawn (Spawn Point Recorder)
Agar pasukan diturunkan di batas luar base (zona merah/aman), Anda harus menyediakan titik-titik spawn yang sesuai.
1. Jalankan `RUN_CODEX_BOT.bat` dan pilih opsi `[2]`.
2. Klik kiri di batas luar area pertempuran di dalam game Clash of Clans untuk menyimpan titik tersebut.
3. Setelah selesai merekam beberapa titik, tekan **`Ctrl + C`** di jendela terminal.
4. Salin hasil koordinat yang tercetak di layar (misal: `points = [(0.897, 0.477), ...]`) dan tempelkan ke variabel `CODEX_SPAWN_POINTS` di dalam file `scripts/autoattack.py`.

---

### ⚙️ Kustomisasi Strategi

Buka file `scripts/autoattack.py` menggunakan teks editor (Notepad, VS Code, dll.) untuk mengubah formasi serangan Anda:

* **Formasi Pasukan (`CODEX_TROOPS`)**:
  Masukkan nama file gambar pasukan yang ada di folder `images-fix` beserta jumlah deploy.
  ```python
  CODEX_TROOPS = [
      {"image": "rootrider.png", "count": 15},
      {"image": "superwitch.png", "count": 50},
      {"image": "miniwarden.png", "count": 1},
  ]
  ```

* **Daftar Hero & Durasi Skill (`CODEX_HERO_SETTINGS`)**:
  Aktifkan kemampuan khusus hero dengan jeda waktu delay (detik) setelah dideploy.
  ```python
  CODEX_HERO_SETTINGS = {
      "dragonduke.png":   {"delay": 10, "active": True},
      "queen.png":        {"delay": 5, "active": True},
  }
  ```

* **Waktu Tunggu Tempur (`CODEX_WAKTU_TUNGGU_BATTLE`)**:
  Durasi maksimal bot menunggu pertempuran sebelum dipaksa menekan tombol kembali ke base (default: `60` detik).

---

## 🇺🇸 English

**CODEX COC FARM** is a Clash of Clans farm automation bot built specifically for the official **Google Play Games PC (Windows)**. It operates in real-time utilizing image matching (OpenCV/PyAutoGUI) to detect the battle screen, find matching bases, deploy troops/heroes/spells dynamically using percentage coordinates (independent of the game window size), and trigger hero abilities at specific delays.

This project is created and developed by **zsxbb**.

---

### 📂 Directory Structure

```text
coc-python/
│
├── .gitignore               # Prevents virtual environments and cache from being committed
├── README.md                # Main project documentation (this file)
├── RUN_CODEX_BOT.bat        # One-click batch file to run the Python Bot
├── requirements.txt         # Required Python libraries
│
├── images-fix/              # Target screenshots for image matching
│   ├── Attack_Green.png     # Example: Find Match Button
│   ├── nexticon.png         # Example: Next button
│   └── ...                  # Other troop/spell images
│
└── scripts/                 # Main Python scripts folder
    ├── autoattack.py        # Main bot automation logic
    └── get_spawn.py         # Spawn point coordinates recorder
```

---

### 🚀 Setup Guide & How to Use

#### A. Initial Game Setup
1. Launch **Clash of Clans** inside **Google Play Games PC**.
2. **IMPORTANT**: Change the in-game language to **English** for correct image-matching.
3. **IMPORTANT**: Ensure the game runs in **Full Screen** mode (press `F11` on your keyboard) or maximized window so that battle coordinates and OpenCV image matching are accurate and consistent.

---

#### B. Running the Bot
You do not need to install Python libraries manually. The runner script will set up a local virtual environment (`codex_venv`) and install all requirements for you.

1. **Start the Bot**:
   - Double-click **`RUN_CODEX_BOT.bat`** in the root folder.
   - If prompted on first run, type `Y` to automatically install the dependencies.
2. **Choose Option**:
   - **`[1] START BOT`**: Starts the automatic search and attack sequence.
   - **`[2] RECORD SPAWN POINTS`**: Opens the utility script to record deployment coordinates outside the enemy base borders.

> [!TIP]
> If clicks do not register inside the Clash of Clans window, right-click **`RUN_CODEX_BOT.bat`** and select **Run as Administrator**.

---

#### C. Recording Spawn Coordinates
To ensure your troops deploy along the safe boundary (outside the red zone), you should record valid spawn coordinate percentages.
1. Run `RUN_CODEX_BOT.bat` and select option `[2]`.
2. Left-click along the outer border of the base in your Clash of Clans window to log spawn coordinates.
3. Once completed, press **`Ctrl + C`** in the terminal.
4. Copy the output array (e.g., `points = [...]`) and paste it into the `CODEX_SPAWN_POINTS` variable inside `scripts/autoattack.py`.

---

### ⚙️ Combat Configuration

Edit `scripts/autoattack.py` with any text editor to customize your attack composition:

* **Troop Setup (`CODEX_TROOPS`)**:
  Add troop image filenames (must exist in `images-fix`) and count to deploy:
  ```python
  CODEX_TROOPS = [
      {"image": "rootrider.png", "count": 15},
      {"image": "superwitch.png", "count": 50},
  ]
  ```

* **Hero Timings (`CODEX_HERO_SETTINGS`)**:
  Enable hero ability activation with a specified delay (in seconds) after deploy:
  ```python
  CODEX_HERO_SETTINGS = {
      "dragonduke.png":   {"delay": 10, "active": True},
      "queen.png":        {"delay": 5, "active": True},
  }
  ```

* **Battle Timeout (`CODEX_WAKTU_TUNGGU_BATTLE`)**:
  Maximum wait time (seconds) before forcing the bot to exit the battle and return home.

---

## ⚠️ Disclaimer / Penolakan Tanggung Jawab

- **IND**: Bot ini dibuat hanya untuk tujuan edukasi dan pembelajaran. Penggunaan otomatisasi pihak ketiga melanggar Ketentuan Layanan Supercell. Penggunaan bot ini berisiko menyebabkan akun Anda dibanned secara permanen. Pengembang tidak bertanggung jawab atas segala konsekuensi/kerugian yang terjadi. Gunakan dengan risiko Anda sendiri!
- **ENG**: This project is for educational and research purposes only. Using third-party automation tools violates Supercell's Terms of Service. Your account may be permanently banned. The developer takes no responsibility for any consequences. Use at your own risk!