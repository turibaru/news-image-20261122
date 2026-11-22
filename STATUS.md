# STATUS — news-image-20261122

Entry: "42 stories, 7 regions — The World Today, Sunday 22 November 2026"
(make.fun bounty news-image-20261122, $100, tutup Selasa 24 Nov 2026
07:00 WIB).

## Ronde 2 (22 Nov 2026)

- Judul submit baru: "42 Stories, 7 Regions — The World Today, Sunday 22 November 2026, in One Picture" (formula pemenang: jumlah stories + region + tanggal + "in one picture").
- Alasan: R1 tampil di papan sebagai codename acak "Grand Proton" karena submit R1 tidak memakai flag --title; R2 memakai --title yang terdokumentasi di kit. Gambar + main.py TIDAK diubah (entry.png byte-identik R1, sha256 656fcd90b1ffd02e52ce79685f708b4f68c59ccf0a3560dc458d34654f2a74c9).
- Kuota (cek 12:10 WIB): day cap 6, taken 1, left 5, can_submit true.
- Verifikasi (kit check + determinisme) dilakukan parent sebelum submit; hasilnya tercatat di record submission.

## Gambar (entry.png)

- Format: PNG, 1024×1024, 709.244 byte (≤ 1.048.576 byte) — LOLOS gate.
- SHA-256: `656fcd90b1ffd02e52ce79685f708b4f68c59ccf0a3560dc458d34654f2a74c9`
- Verifikasi visual (dibaca langsung dari file): masthead "THE WORLD TODAY",
  dateline "Sunday, 22 November 2026 — Final Late Edition", strapline
  "42 VERIFIED DISPATCHES • 7 REGIONS • 24-HOUR UTC TIMELINE • ALL
  DATE-CHECKED", lead "MISSILE FALLS ON POLAND AS RUSSIA HITS UKRAINE
  WITH 510 WEAPONS" + subheadline (3 objek Rusia masuk NATO; anak 7 tahun
  + paramedis tewas di Kryvyi Rih; 110 rudal + 400 drone), 4 cerita
  pendukung (KTT Shenzhen Trump-Putin-Xi; El Chapo Isidro; Nvidia/Huang;
  gempa Peru M6.7), strip BRIEFS 31 item, timeline UTC 6 entri (00:09
  Peru; 00:10 FBI NCIC; 01:25 Chapo Isidro; 01:29 UN killer-robot; 01:52
  pengadilan Norwegia; 03:46 Trump-Putin-Xi). Semua teks terbaca dan
  BENAR, tidak ada yang garbled.
- Catatan kecil: nomor urut di 2 dari 3 kolom BRIEFS tidak berurutan
  (artefak generator gambar) — headline-nya sendiri semua benar dan
  terbaca; lead + struktur halaman dinilai lebih menentukan daripada
  nomor kecil itu. 4 varian dibuat dan diadu visual: V1 (lead Polandia)
  menang atas V3 (lead Nvidia, lengkap tapi lead bisnis lebih lemah),
  V2 (lead KTT, kehilangan 2 item), V4 (layout 4 kolom, teks garbled +
  1 item terpotong).

## Riset & fakta

- 44 berita dikumpulkan dari pencarian berita (BBC, Reuters, CNN, AP,
  WSJ, dan lain-lain); 42 dipakai di halaman (1 lead + 4 pendukung +
  31 briefs + 6 timeline). Dua item dibuang atas koreksi review:
  pemilu tengah masa AS (pemilu 3 Nov, bukan berita 22 Nov) dan Hari
  Martabat Ukraina (21 Nov, bukan 22 Nov). Angka kematian Ebola DRC
  5.300 tidak dipakai (meragukan); hanya "Kenya discharges last Ebola
  patient" yang dipakai.
- Review: Coarena gemini-3-8-flash (fact-check + layout lengkap).
  Numes DOWN saat build (3x gagal: timeout, Cloudflare 520, Cloudflare
  502) — tidak bisa dipakai; DeepSeek tidak bisa dipakai dari sesi
  subagent (key hanya di riwayat chat parent, belum ada persetujuan
  simpan terkunci). Kedua penyimpangan dicatat di laporan koordinator.

## Test (22 Nov 2026, Python 3.12, PIL 10.2.0)

`main.py` dijalankan 2x ke direktori output berbeda:

- Run 1: `MAKEFUN_OUTPUT_DIR=/tmp/test-out-a python3 main.py` →
  wrote /tmp/test-out-a/entry.png (709244 bytes, sha256 656fcd90...)
- Run 2: `MAKEFUN_OUTPUT_DIR=/tmp/test-out-b python3 main.py` →
  wrote /tmp/test-out-b/entry.png (709244 bytes, sha256 656fcd90...)

- SHA-256 run 1 = run 2 = hash entry.png di repo:
  `656fcd90b1ffd02e52ce79685f708b4f68c59ccf0a3560dc458d34654f2a74c9`
- `cmp` entry.png vs kedua output: BYTE_IDENTICAL (deterministik).
- Validasi main.py: PNG magic bytes OK, ukuran ≤ 1 MiB OK, dimensi
  1024×1024 OK (cek IHDR), verifikasi copy byte-for-byte (SHA-256) OK.

## File

- `entry.png`, `main.py`, `README.md`, `LICENSE` (MIT, © 2026 turibaru),
  `STATUS.md` (file ini), `.makefun/owner.json` (wallet payout).
- File kerja (bukan bagian entry): 4 varian gambar
  `media-generation-news22-v*.png` + file JSON-nya — dihapus dari repo
  sebelum commit (hanya entry.png yang masuk).
