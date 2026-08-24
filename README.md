# 🎮 JAYANTARA NIHONGO MASTER-KIT
### 30-Day RPG Quest Log & Skill Progress Tracker
*Portal Belajar Gratis LPK JAYANTARA — Naik Level Bahasa Jepang dari Nol hingga Siap Kerja ke Jepang!*

---

## 🧭 Struktur Project

Repo ini menggunakan **Markdown sebagai source content** dan metadata terstruktur untuk curriculum, badge, dan validasi. Dengan begitu materi tetap mudah dibaca manusia sekaligus siap dipakai oleh website, quiz engine, progress tracker, dan sistem gamifikasi.

```text
jayantara-quest-log/
├── README.md
├── LICENSE.md
├── quests/                    ← 30 quest pembelajaran
│   ├── day-01.md
│   ├── ...
│   └── day-30.md
├── data/                      ← source of truth untuk struktur course
│   ├── curriculum.yaml
│   └── badges.yaml
├── scripts/                   ← content tooling
│   └── validate_quests.py
└── .github/workflows/         ← validasi otomatis
    └── validate-quests.yml
```

### Content model

Setiap quest adalah Markdown yang berisi materi, contoh, latihan, checklist, catatan pribadi, dan status. `data/curriculum.yaml` mendefinisikan tipe quest, fase, dependency, dan reward; `data/badges.yaml` mendefinisikan badge dan requirement. Struktur ini sengaja dipisahkan agar frontend tidak perlu hard-code isi Day 01–30.

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

Progress pengguna sebaiknya dihitung oleh aplikasi/automation dari status quest, bukan dipelihara sebagai angka manual. Untuk saat ini checkbox pada masing-masing quest tetap menjadi mekanisme progress yang sederhana dan transparan.

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

Detail progression, dependency, dan badge tersedia di [`data/curriculum.yaml`](data/curriculum.yaml) dan [`data/badges.yaml`](data/badges.yaml).

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

## 🧪 Validasi Content

Setiap perubahan pada `quests/`, `data/`, atau tooling akan menjalankan GitHub Actions untuk memastikan 30 quest tersedia dan mempertahankan section wajib:

- `Materi & Output Skill`
- `Checklist Belajar Hari Ini`
- `Catatan Pribadi`
- `Status`

Validator dapat dijalankan lokal dengan:

```bash
python3 scripts/validate_quests.py
```

---

## 🚀 Cara Pakai

1. Buka `quests/day-01.md` dan mulai belajar.
2. Selesaikan checklist quest.
3. Tandai `Quest selesai` ketika seluruh target hari tersebut selesai.
4. Lanjut ke quest berikutnya; checkpoint dan final exam memiliki dependency yang tercatat di curriculum.
5. Untuk pengembangan aplikasi, gunakan `data/curriculum.yaml` dan `data/badges.yaml` sebagai metadata terstruktur.

---

*LPK JAYANTARA — Lembaga Pelatihan Kerja Bahasa Jepang & Persiapan Kerja ke Jepang*

---

<sub>© 2026 LPK JAYANTARA. All Rights Reserved. Materi ini dilindungi hak cipta — dilarang menyalin, mendistribusikan ulang, atau memodifikasi tanpa izin tertulis. Lihat [LICENSE.md](LICENSE.md).</sub>
