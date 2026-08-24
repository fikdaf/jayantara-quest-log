# 🎮 JAYANTARA NIHONGO MASTER-KIT
### 30-Day RPG Quest Log & Skill Progress Tracker
*Portal Belajar Gratis LPK JAYANTARA — Naik Level Bahasa Jepang dari Nol hingga Siap Kerja ke Jepang!*

---

## 🧭 Struktur Project

Repo ini menggunakan **Markdown sebagai source content** dan metadata terstruktur untuk curriculum, badge, progression, dan validasi. Dengan begitu materi tetap mudah dibaca manusia sekaligus siap dipakai oleh website, quiz engine, progress tracker, dan sistem gamifikasi.

```text
jayantara-quest-log/
├── README.md
├── LICENSE.md
├── quests/                    ← 30 quest pembelajaran
├── data/                      ← source of truth curriculum, rewards, progression
├── schemas/                   ← JSON schemas untuk content & progress state
├── scripts/                   ← validation, progression engine & CLI
└── .github/workflows/         ← validasi otomatis
```

### Content model

Setiap quest adalah Markdown yang berisi materi, contoh, latihan, checklist, catatan pribadi, dan status. Metadata frontmatter menjadi source of truth untuk quest. `data/curriculum.yaml`, `data/badges.yaml`, `data/progression.yaml`, dan `data/xp-rules.yaml` mendefinisikan aturan aplikasi secara terpisah.

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

Jika membutuhkan output tanpa persistence:

```bash
python3 scripts/complete_progress.py --json 5 1 2 3 4
```

Jika ingin menyimpan state:

```bash
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

---

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

Detail progression, dependency, dan badge tersedia di `data/curriculum.yaml` dan `data/badges.yaml`.

---

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

---

## 🧪 Validasi & Development

Semua perubahan pada `quests/`, `data/`, `schemas/`, atau `scripts/` divalidasi oleh GitHub Actions. Suite mencakup frontmatter, curriculum, dependency graph, progression, badge rules, progress state, persistence, dan CLI.

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

---

## 🚀 Cara Belajar

1. Jalankan `python3 scripts/jayantara.py start`.
2. Buka quest Day yang ditampilkan dan kerjakan materinya.
3. Selesaikan checklist belajar.
4. Jalankan `python3 scripts/jayantara.py complete N` setelah target hari selesai.
5. Lanjut ke Day berikutnya. Sistem akan menolak quest yang dilompati.
6. Gunakan `status` untuk melihat XP, badge, phase, dan current day.

---

*LPK JAYANTARA — Lembaga Pelatihan Kerja Bahasa Jepang & Persiapan Kerja ke Jepang*

---

<sub>© 2026 LPK JAYANTARA. All Rights Reserved. Materi ini dilindungi hak cipta — dilarang menyalin, mendistribusikan ulang, atau memodifikasi tanpa izin tertulis. Lihat LICENSE.md.</sub>
