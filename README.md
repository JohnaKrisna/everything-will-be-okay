# Everything Will Be Okay

Sebuah program kecil bergaya terminal. Bukan aplikasi produktivitas, bukan alat kerja. Cuma ruang singkat untuk berhenti sejenak, membaca beberapa kalimat, dan menuliskan satu harapan kecil.

Tersedia dalam tiga cara untuk dijalankan: lewat Python, lewat file exe (tanpa perlu install Python), atau langsung di browser.

## Coba versi web

Buka langsung di sini, tidak perlu install apa apa:

[https://johnakrisna.github.io/everything-will-be-okay/ewbo_web_cmd.html](https://johnakrisna.github.io/everything-will-be-okay/ewbo_web_cmd.html)

Disarankan dibuka di laptop atau komputer. Di layar HP tampilannya akan menyarankan buka di PC, karena pengalaman gaya terminal ini paling pas di layar besar.

## Coba versi CMD (Windows)

Ada dua cara:

### 1. Pakai file exe (paling gampang)

Download `EverythingWillBeOkay.exe` (Bahasa Indonesia) atau `EverythingWillBeOkayEN.exe` (English) dari halaman [Releases](../../releases), lalu jalankan langsung. Tidak perlu install Python.

Langkah lengkapnya:

1. Buka halaman [Releases](../../releases), klik release terbaru
2. Di bagian Assets, klik file exe yang diinginkan, otomatis terdownload ke folder Downloads
3. Buka folder Downloads, double-click file exe yang baru didownload
4. Kalau muncul peringatan biru "Windows protected your PC", klik "More info" lalu "Run anyway". Ini wajar untuk program baru yang belum dikenal banyak orang, bukan berarti virus.
5. Program langsung terbuka di jendela CMD. Tekan Enter untuk mulai. Tidak perlu install apapun, tidak mengubah sistem, tinggal ditutup kalau sudah selesai.

Catatan: Windows Defender atau SmartScreen kadang menampilkan peringatan untuk file exe yang belum dikenal banyak orang. Ini wajar untuk aplikasi baru yang belum "dikenal" oleh sistem Microsoft, bukan berarti virus.

### 2. Pakai file Python

Butuh Python terinstall di komputer.

```
pip install pyfiglet
python ewbo_cmd.py
```

Untuk versi bahasa Inggris:

```
python ewbo_cmd_en.py
```

`pyfiglet` bersifat opsional, dipakai supaya judul tampil sebagai ASCII art. Kalau tidak diinstall, judul tetap muncul dengan tampilan sederhana.

## Struktur repo

```
ewbo_cmd.py                 versi Python (Bahasa Indonesia) untuk CMD/terminal
ewbo_cmd_en.py               versi Python (English) untuk CMD/terminal
ewbo_web_cmd.html           versi web, bisa dibuka langsung di browser
images/qris.png             QRIS untuk dukungan
README.md
```

## Dukung

Kalau project ini terasa berarti dan ingin membantu, bisa lewat QRIS di bawah ini. Tidak wajib, cukup dengan mencoba dan membagikannya juga sudah sangat berarti.

![QRIS Everything Will Be Okay](images/qris.png)
