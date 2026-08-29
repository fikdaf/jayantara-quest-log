# 🎮 JAYANTARA NIHONGO MASTER-KIT
### 30-Day RPG Quest Log & Skill Progress Tracker
*Portal Belajar Gratis LPK JAYANTARA — Naik Level Bahasa Jepang dari Nol hingga Siap Kerja ke Jepang!*

---

## 🚀 Aplikasi lintas platform

JAYANTARA sekarang disiapkan sebagai aplikasi **Web/PWA, Windows, macOS, Linux, Android, dan iOS** dengan curriculum dan progression engine yang sama. Build dan test dapat dilakukan di **GitHub Actions**; pengguna tidak perlu memasang repository di komputer untuk memakai release aplikasi.

| Platform | Cara penggunaan/pemasangan |
|---|---|
| 🌐 Browser | Buka alamat Web/PWA deployment. Tidak perlu instalasi. |
| 📱 Android | Gunakan APK/release Android yang dipublikasikan; buka file APK, izinkan pemasangan dari sumber yang dipercaya bila diminta, lalu install. |
| 🍎 iPhone/iPad | Gunakan build iOS yang dipublikasikan melalui TestFlight/App Store. Instal TestFlight bila diperlukan, lalu buka invitation/build JAYANTARA. |
| 🪟 Windows | Unduh installer `.exe` dari GitHub Release, jalankan installer, lalu buka JAYANTARA Quest Log dari Start Menu/Desktop. |
| 🍎 macOS | Unduh `.dmg`, buka, lalu seret JAYANTARA Quest Log ke Applications. Jika macOS menampilkan peringatan keamanan, gunakan pengaturan Privacy & Security untuk mengizinkan aplikasi yang memang Anda percaya. |
| 🐧 Linux | Unduh `.AppImage`, beri izin execute (`chmod +x *.AppImage`), lalu jalankan file tersebut. |

> **Catatan release:** artifact aplikasi hanya dianggap siap dipakai setelah workflow release selesai GREEN. Untuk iOS/Android, distribusi produksi membutuhkan kredensial/signing dan akun store yang sesuai; repository saja tidak dapat menyediakan kredensial tersebut.

## 🧑‍💻 Menjalankan dari source

### Prasyarat

- Python 3.12+ untuk engine/validator legacy.
- Node.js 24+ untuk Web/Desktop workspace.
- npm dengan `package-lock.json` yang sinkron.

Clone repository:

```bash
git clone https://github.com/fikdaf/jayantara-quest-log.git
cd jayantara-quest-log
npm ci
```

### Web/PWA development

```bash
npm run build --workspace @jayantara/web
```

Hasil production berada di `apps/web/dist/`. PWA mencakup manifest, service worker, dan icon aplikasi.

### Desktop development/build

```bash
npm run build --workspace @jayantara/web
npm run package --workspace @jayantara/desktop
```

Packaging menggunakan Electron Builder dan target release desktop adalah Windows NSIS/EXE, macOS DMG, dan Linux AppImage.

### GitHub Actions release

Build release lintas platform dapat dijalankan dari GitHub Actions secara manual dengan tag, misalnya `v0.1.0`. Workflow menghasilkan artifact per OS dan mempublikasikannya ke GitHub Release jika konfigurasi repository mengizinkan publish.

---

## 🎮 CLI Progress Tracker

JAYANTARA memiliki CLI sederhana untuk menjalankan progression engine secara langsung.

### Mulai quest aktif

```bash
python3 scripts/jayantara.py start
```

Menampilkan Day aktif beserta title, phase, type, level, estimasi waktu, skills, dan prerequisite.

Untuk output terstruktur:

```bash
python3 scripts/jayantara.py start --json
```

### Lihat progress

```bash
python3 scripts/jayantara.py status
```

### Selesaikan quest

```bash
python3 scripts/jayantara.py complete 1
```

Completion mengikuti aturan **sequential progression**: Day N hanya dapat diselesaikan setelah Day N-1 selesai. State canonical kemudian dihitung ulang untuk XP, badge, phase, dan current day, lalu disimpan secara atomic.

Untuk memakai file state lain:

```bash
python3 scripts/jayantara.py --state-file /tmp/player.json status
```

State default berada di `data/state/progress-state.json`. File runtime tersebut tidak perlu di-commit ke repository.

### Engine-level commands

```bash
python3 scripts/complete_progress.py --json 5 1 2 3 4
python3 scripts/complete_progress.py --save --state-file /tmp/player.json 5 1 2 3 4
```

---

## 🐕 MENTOR DIGITAL: AKIRA-SENSEI (明)

```text
  /\_/\\
 ( o.o )  "Konnichiwa, Petualang Jayantara! Aku Akira!
  > ^ <   Siapkan semangatmu untuk menaklukkan 30 Quest Bahasa Jepang ini.
          Selesaikan setiap misi harian, kumpulkan Badge, dan capai
          level Master di akhir perjalanan!"
```

---

## 📊 OVERALL QUEST PROGRESS

`[                                ] 0% (0/30 QUESTS CLEAR!)`

Progress pengguna dihitung oleh progression engine dari canonical state, bukan dipelihara sebagai angka manual.

## 🗺️ RPG QUEST MAP

| Fase | Hari | Fokus | Reward |
| --- | --- | --- | --- |
| 🟢 **Foundation** | 01–05 | Hiragana, Katakana, salam, perkenalan | Rookie → 🥉 Bronze |
| 🔵 **Novice** | 06–10 | Angka, waktu, kalender, benda, verba, belanja | Novice → 🥈 Silver |
| 🟣 **Adept Warrior** | 11–15 | Grammar N5, adjective, lokasi, perbandingan | Adept Warrior |
| 🟠 **Kanji Apprentice** | 16–20 | Kanji dasar N5 + review | Kanji Apprentice |
| 🔴 **Japan Ready** | 21–25 | Workplace Japanese & keselamatan | Japan Ready |
| 🟡 **Interview Master** | 26–30 | Rirekisho, mensetsu, roleplay, final exam | Interview Master → 🥇 Gold |

### Quest files

| Hari | Mission | Tipe |
| --- | --- | --- |
| 01 | Gerbang Hiragana Pass | Lesson |
| 02 | Lembah Katakana Blitz | Lesson |
| 03 | Salam & Aisatsu Harian | Lesson |
| 04 | Perkenalan Diri (Jikoshoukai) | Lesson |
| 05 | ⚔️ BOSS BATTLE 1: Checkpoint Pemula | Checkpoint |
| 06 | Angka & Jam (Jikan) | Lesson |
| 07 | Hari, Bulan, & Tanggal | Lesson |
| 08 | Kata Benda & Benda Sekitar | Lesson |
| 09 | Aktivitas Harian (Verba ~masu) | Lesson |
| 10 | ⚔️ BOSS BATTLE 2: Misi Pasar & Toko | Checkpoint |
| 11 | Kata Sifat & Tata Bahasa N5 (1) | Lesson |
| 12 | Kata Sifat & Tata Bahasa N5 (2) | Lesson |
| 13 | Kata Sifat & Tata Bahasa N5 (3) | Lesson |
| 14 | Kata Sifat & Tata Bahasa N5 (4) | Lesson |
| 15 | Kata Sifat & Tata Bahasa N5 (5) | Checkpoint |
| 16 | Kanji Dasar N5 (1) | Lesson |
| 17 | Kanji Dasar N5 (2) | Lesson |
| 18 | Kanji Dasar N5 (3) | Lesson |
| 19 | Kanji Dasar N5 (4) | Lesson |
| 20 | Kanji Review + Flashcard | Checkpoint |
| 21 | Instruksi Kerja & Keselamatan (1) | Lesson |
| 22 | Instruksi Kerja & Keselamatan (2) | Lesson |
| 23 | Instruksi Kerja & Keselamatan (3) | Lesson |
| 24 | Instruksi Kerja & Keselamatan (4) | Lesson |
| 25 | Instruksi Kerja & Keselamatan (5) | Lesson |
| 26 | Simulasi Mensetsu & Rirekisho (1) | Lesson |
| 27 | Simulasi Mensetsu & Rirekisho (2) | Lesson |
| 28 | Simulasi Mensetsu & Rirekisho (3) | Lesson |
| 29 | Simulasi Mensetsu & Rirekisho (4) | Lesson |
| 30 | 🏆 FINAL BOSS: Trial Exam N5 & Mensetsu | Final Exam |

## 🏅 Sistem Badge

- `Rookie I–IV` — Day 01–04
- 🥉 **BRONZE BADGE** — Day 05
- `Novice I–IV` — Day 06–09
- 🥈 **SILVER BADGE** — Day 10
- `Adept Warrior` — Day 11–15
- `Kanji Apprentice` — Day 16–20
- `Japan Ready` — Day 21–25
- `Interview Master` — Day 26–29
- 🥇 **GOLD JAYANTARA** — Day 30

## 🧪 Validasi & Development

GitHub Actions memvalidasi frontmatter, curriculum, dependency graph, progression, badge rules, progress state, persistence, CLI, Web/PWA, dan Desktop packaging.

Validator utama:

```bash
python3 scripts/validate_quests.py
python3 scripts/check_frontmatter.py
python3 scripts/validate_curriculum.py
python3 scripts/validate_dependencies.py
python3 scripts/validate_progression.py
python3 scripts/validate_badges.py
```

Regression suite:

```bash
python3 scripts/test_progress.py
python3 scripts/test_complete_quest.py
python3 scripts/test_complete_progress.py
python3 scripts/test_save_progress.py
python3 scripts/test_complete_progress_persistence.py
python3 scripts/test_quest_details.py
python3 scripts/test_jayantara_cli.py
```

## 📚 Tutorial penggunaan

1. Buka JAYANTARA di browser atau instal release untuk device Anda.
2. Mulai dari Day 01 dan ikuti quest secara berurutan.
3. Baca materi dan kerjakan latihan/checklist.
4. Tandai quest selesai melalui aplikasi atau CLI.
5. Pantau XP, badge, phase, dan current day.
6. Jangan melompati prerequisite: progression engine menjaga urutan quest.
7. Gunakan Web/PWA bila ingin akses cepat tanpa instalasi; gunakan desktop/mobile bila ingin pengalaman aplikasi native/shell.

---

*LPK JAYANTARA — Lembaga Pelatihan Kerja Bahasa Jepang & Persiapan Kerja ke Jepang*

<sub>© 2026 LPK JAYANTARA. All Rights Reserved. Materi ini dilindungi hak cipta — dilarang menyalin, mendistribusikan ulang, atau memodifikasi tanpa izin tertulis. Lihat LICENSE.md.</sub>
