# 🎮 JAYANTARA NIHONGO MASTER-KIT

**30-Day RPG Quest Log & Skill Progress Tracker** — fondasi aplikasi lintas platform untuk belajar Bahasa Jepang dari nol sampai siap kerja ke Jepang.

> **Release:** `v0.1.0` · Web/PWA · Windows · macOS · Linux · Android/iOS foundation

## 🚀 Mulai cepat

### Pengguna biasa

Pengguna **tidak perlu meng-install repository atau Node.js** untuk memakai release. Pilih cara yang sesuai perangkat:

| Perangkat | Cara pakai | Paket/release |
|---|---|---|
| 🌐 Browser | Buka deployment Web/PWA | Web URL |
| 📱 Android | Unduh APK, izinkan pemasangan dari sumber tepercaya bila diminta, lalu install | APK |
| 🍎 iPhone/iPad | Gunakan TestFlight/App Store build yang dipublikasikan | iOS build |
| 🪟 Windows | Unduh installer `.exe`, jalankan, lalu buka aplikasi | `.exe` |
| 🍎 macOS | Unduh `.dmg`, buka, lalu seret aplikasi ke `Applications` | `.dmg` |
| 🐧 Linux | Unduh `.AppImage`, beri izin execute, lalu jalankan | `.AppImage` |

**Catatan:** distribusi Android/iOS produksi membutuhkan signing credentials dan akun store/TestFlight yang sesuai. Repository ini menyediakan fondasi dan pipeline; kredensial tidak disimpan di repository.

## 📦 Release v0.1.0

Semua file rilis berasal dari GitHub Actions. Untuk release final, gunakan halaman GitHub Release `v0.1.0` dan pilih file sesuai OS.

Struktur asset yang diharapkan:

```text
v0.1.0
├── Windows   → installer .exe / artefak Windows
├── macOS     → .dmg
├── Linux     → .AppImage
├── Web/PWA   → web build artifact
└── Mobile    → build Android/iOS bila signing & distribution tersedia
```

**Jangan menjalankan file dari folder artifact secara acak.** Pilih paket berdasarkan perangkat dan arsitektur yang disediakan pada release.

## 🧑‍💻 Menjalankan dari source

### Prasyarat

- Node.js 24+
- npm
- Python 3.12+ untuk validator/CLI Python

Clone dan install:

```bash
git clone https://github.com/fikdaf/jayantara-quest-log.git
cd jayantara-quest-log
npm ci
```

> Jika hanya ingin memakai aplikasi, lewati bagian development ini dan gunakan release.

### Web/PWA

```bash
npm run build --workspace @jayantara/web
npm run dev --workspace @jayantara/web
```

Production output berada di `apps/web/dist/` dan harus berisi `index.html`, `manifest.webmanifest`, `sw.js`, serta `icons/icon.svg`.

### Desktop

```bash
npm run build:core
npm run package --workspace @jayantara/desktop
```

Packaging menggunakan Electron Builder. Target desktop: Windows installer, macOS DMG, dan Linux AppImage.

## 🎮 Tutorial penggunaan

1. Buka JAYANTARA melalui Web/PWA atau instal aplikasi sesuai perangkat.
2. Mulai dari **Day 01**.
3. Ikuti quest secara berurutan dan selesaikan materi/latihan.
4. Selesaikan quest untuk mendapatkan XP dan membuka progression berikutnya.
5. Pantau current day, phase, XP, dan badge.
6. Jangan melewati prerequisite; progression engine menjaga urutan quest.
7. Gunakan Web/PWA untuk akses cepat tanpa instalasi atau aplikasi desktop/mobile untuk pengalaman aplikasi.

### CLI

```bash
python3 scripts/jayantara.py start
python3 scripts/jayantara.py status
python3 scripts/jayantara.py complete 1
```

Output JSON:

```bash
python3 scripts/jayantara.py start --json
```

State default berada di `data/state/progress-state.json` dan merupakan runtime state, bukan file yang perlu di-commit.

## 🗺️ RPG Quest Map

| Fase | Hari | Fokus | Reward |
|---|---:|---|---|
| 🟢 Foundation | 01–05 | Hiragana, Katakana, salam, perkenalan | Rookie → Bronze |
| 🔵 Novice | 06–10 | Angka, waktu, kalender, benda, verba, belanja | Novice → Silver |
| 🟣 Adept Warrior | 11–15 | Grammar N5, adjective, lokasi, perbandingan | Adept Warrior |
| 🟠 Kanji Apprentice | 16–20 | Kanji dasar N5 + review | Kanji Apprentice |
| 🔴 Japan Ready | 21–25 | Workplace Japanese & keselamatan | Japan Ready |
| 🟡 Interview Master | 26–30 | Rirekisho, mensetsu, roleplay, final exam | Interview Master → Gold |

## 🏅 Sistem Badge

- `Rookie I–IV` — Day 01–04
- 🥉 **BRONZE** — Day 05
- `Novice I–IV` — Day 06–09
- 🥈 **SILVER** — Day 10
- `Adept Warrior` — Day 11–15
- `Kanji Apprentice` — Day 16–20
- `Japan Ready` — Day 21–25
- `Interview Master` — Day 26–29
- 🥇 **GOLD JAYANTARA** — Day 30

## 🧪 Validasi dan CI

CI memvalidasi core engine, curriculum, progression, persistence, Web/PWA, dan desktop packaging.

Validator utama:

```bash
python3 scripts/validate_quests.py
python3 scripts/check_frontmatter.py
python3 scripts/validate_curriculum.py
python3 scripts/validate_dependencies.py
python3 scripts/validate_progression.py
python3 scripts/validate_badges.py
```

Regression tests:

```bash
python3 scripts/test_progress.py
python3 scripts/test_complete_quest.py
python3 scripts/test_complete_progress.py
python3 scripts/test_save_progress.py
python3 scripts/test_complete_progress_persistence.py
python3 scripts/test_quest_details.py
python3 scripts/test_jayantara_cli.py
```

## ✅ Checklist pengguna sebelum mulai

- [ ] Memilih Web/PWA atau installer sesuai perangkat.
- [ ] Menggunakan release `v0.1.0` dari halaman Release.
- [ ] Membuka aplikasi dan memastikan halaman utama tampil.
- [ ] Memulai Day 01.
- [ ] Menyelesaikan quest secara berurutan.
- [ ] Memastikan progress/XP berubah setelah completion.
- [ ] Menjaga state lokal/runtime bila memakai CLI.

## 🔧 Checklist maintainer sebelum release

- [ ] Semua GitHub Actions GREEN.
- [ ] Web/PWA menghasilkan seluruh file wajib.
- [ ] Desktop Windows/macOS/Linux berhasil package.
- [ ] Artifact hanya berisi file yang dapat dipublikasikan.
- [ ] Release menggunakan tag versi yang benar.
- [ ] Asset release dapat diunduh dan dibuka pada OS target.
- [ ] README dan instruksi instalasi sesuai asset yang benar-benar tersedia.
- [ ] Tidak ada secret/signing credential di repository.

## 📄 Lisensi

Lihat `LICENSE.md` untuk ketentuan penggunaan dan distribusi.

---

*LPK JAYANTARA — Lembaga Pelatihan Kerja Bahasa Jepang & Persiapan Kerja ke Jepang*  
*© 2026 LPK JAYANTARA.*
