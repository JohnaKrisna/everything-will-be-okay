"""
Everything Will Be Okay — versi CMD/Terminal (Python)
Jalankan: python ewbo_cmd.py

Opsional (biar judulnya lebih mirip pixel-art seperti di gambar):
    pip install pyfiglet

Kalau blok kursor (█) atau spinner-nya tampil aneh di cmd.exe,
jalankan dulu:  chcp 65001
"""

import os
import sys
import time
import shutil
import random

# ---------- Warna ANSI (tema hitam & putih saja) ----------
WHITE = "\033[97m"
GRAY = "\033[90m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
CLEAR_LINE = "\033[K"

CURSOR_CHAR = "\u2588"  # blok solid, dipakai sebagai "kursor" yang blink


def enable_ansi_on_windows():
    """Supaya kode warna ANSI juga jalan di cmd.exe Windows."""
    if os.name == "nt":
        os.system("chcp 65001 > nul")  # aktifkan UTF-8 di cmd.exe
        os.system("")  # trik lama: mengaktifkan ANSI di cmd.exe modern


def ensure_pyfiglet():
    """Coba pasang pyfiglet otomatis kalau belum ada (biar judul lebih pixel-art)."""
    try:
        import pyfiglet  # noqa: F401
        return
    except ImportError:
        pass
    try:
        import subprocess
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "pyfiglet"],
            check=False,
        )
    except Exception:
        pass  # kalau gagal (mis. tidak ada internet), lanjut pakai fallback title


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# Atur sendiri pembagian barisnya di sini kalau mau.
TITLE_LINES = ["EVERYTHING WILL", "BE OKAY"]
FIGLET_WIDTH = 300  # perbesar kalau font/teks masih terpotong


def print_title():
    try:
        import pyfiglet
        try:
            fig = pyfiglet.Figlet(font="ansi_shadow", width=FIGLET_WIDTH)
        except pyfiglet.FontNotFound:
            fig = pyfiglet.Figlet(font="big", width=FIGLET_WIDTH)
        for line in TITLE_LINES:
            print(WHITE + BOLD + fig.renderText(line) + RESET)
    except ImportError:
        width = shutil.get_terminal_size((80, 20)).columns
        print()
        for line in TITLE_LINES:
            print(WHITE + BOLD + line.center(width) + RESET)
        print()


# ---------- Pesan-pesan (sama seperti versi HTML) ----------
messages = [
    ("Menutup semua program yang membuat cemas...", 1),
    ("Menghapus sementara pikiran yang terlalu jauh...", 1),
    ("Menata ulang harapan yang sempat berantakan...", 2),
    ("Menyimpan hal-hal baik yang masih ingin dipertahankan...", 1),
    ("Melepaskan hal-hal yang memang sudah waktunya pergi...", 2),
    ("Memproses rasa takut yang terlalu lama disimpan...", 3),
    ("Mengingat kembali bahwa tidak semuanya harus selesai hari ini...", 3),
    ("Memindahkan beban yang terlalu lama dipikul sendirian...", 3),
    ("Memberi ruang untuk hati yang sedang belajar tenang...", 2),
    ("Memulihkan sedikit kepercayaan pada hari esok...", 2),
    ("Menyisakan ruang untuk hal-hal baik yang mungkin datang...", 1),
    ("Hampir selesai... pelan-pelan, tidak apa-apa.", 2),
]

PAUSE = {1: 1.4, 2: 2.5, 3: 4.2}
TYPE_DELAY = 0.028
BAR_WIDTH = 40
SPINNER_FRAMES = "\u280b\u2819\u2839\u2838\u283c\u2834\u2826\u2827\u2807\u280f"  # ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
BLINK_INTERVAL = 0.45  # detik, kecepatan kursor blink
TICK = 0.07            # detik, kecepatan refresh animasi saat jeda


def render_status_line(pct, spinner, prefix, text_with_cursor):
    """Satu baris utuh: [bar] pct% spinner  C:\\> pesan (+kursor).

    PENTING: baris ini SELALU dipotong otomatis supaya panjangnya tidak
    melebihi lebar jendela terminal saat ini. Kalau dibiarkan lebih panjang
    dari lebar terminal, cmd/Windows Terminal akan meng-wrap baris ke bawah.
    Setelah itu "\r" cuma balik ke awal baris hasil wrap (bukan ke awal baris
    aslinya), jadi bagian yang sudah wrap tidak pernah ke-clear -> tiap frame
    animasi numpuk jadi banyak baris (persis bug yang muncul di pesan-pesan
    panjang, mis. di 79%). Dengan dipotong sesuai lebar terminal, baris ini
    dijamin selalu pas 1 baris dan overwrite di tempat yang sama.
    """
    filled = int(BAR_WIDTH * pct / 100)
    bar = "#" * filled + "-" * (BAR_WIDTH - filled)

    # Hitung ulang lebar terminal tiap kali render (aman walau di-resize)
    cols = shutil.get_terminal_size((80, 20)).columns
    max_len = max(cols - 1, 10)  # -1 = jaga-jaga biar kursor sendiri tak memicu wrap

    head_plain = f"[{bar}] {pct:3d}% {spinner}  {prefix}"
    budget = max_len - len(head_plain)
    if budget < 1:
        budget = 1

    # Kalau teks pesan (+kursor) kepanjangan, tampilkan bagian EKORNYA saja
    # (biar kursor yang lagi "mengetik" tetap kelihatan di ujung).
    if len(text_with_cursor) > budget:
        text_with_cursor = text_with_cursor[-budget:]

    line = (
        f"{WHITE}[{bar}] {pct:3d}%{RESET} {GRAY}{spinner}{RESET}  "
        f"{GRAY}{prefix}{RESET}{WHITE}{text_with_cursor}{RESET}"
    )
    sys.stdout.write("\r" + CLEAR_LINE + line)
    sys.stdout.flush()


# Titik-titik progress akhir untuk tiap pesan — sengaja tidak dibuat rata,
# supaya kenaikannya terasa alami, bukan seperti hitungan mesin.
PROGRESS_MILESTONES = [8, 19, 34, 45, 61, 70, 79, 87, 91, 95, 98, 100]

# Jeda "hening" sesaat setelah progress mencapai 100%, sebelum dialog muncul.
SILENCE_AFTER_COMPLETE = 2.0


def run_loading():
    assert len(PROGRESS_MILESTONES) == len(messages)
    frame = 0
    current_pct = 0

    def nudge(target, big=False):
        """Menaikkan current_pct menuju target dengan langkah tak beraturan,
        kadang diam sesaat, kadang melompat — tidak pernah mundur."""
        nonlocal current_pct
        if current_pct >= target:
            return
        if random.random() < 0.22:
            step = 0  # sesekali seperti "macet" sejenak
        else:
            step = random.randint(2, 6) if big else random.randint(1, 3)
        current_pct = min(target, current_pct + step)

    for idx, (text, weight) in enumerate(messages):
        target = PROGRESS_MILESTONES[idx]

        # --- fase mengetik: kursor blok nempel di ujung teks yang berjalan ---
        for i in range(len(text) + 1):
            spin = SPINNER_FRAMES[frame % len(SPINNER_FRAMES)]
            frame += 1
            nudge(target, big=True)
            partial = text[:i] + (CURSOR_CHAR if i < len(text) else "")
            render_status_line(current_pct, spin, "C:\\> ", partial)
            if i < len(text):
                time.sleep(TYPE_DELAY)

        # --- fase jeda: bar & spinner tetap hidup, kursor blink on/off ---
        pause_end = time.time() + PAUSE[weight]
        blink_on = True
        last_blink = time.time()
        while time.time() < pause_end:
            spin = SPINNER_FRAMES[frame % len(SPINNER_FRAMES)]
            frame += 1
            nudge(target)
            if time.time() - last_blink >= BLINK_INTERVAL:
                blink_on = not blink_on
                last_blink = time.time()
            cursor = CURSOR_CHAR if blink_on else " "
            render_status_line(current_pct, spin, "C:\\> ", text + cursor)
            time.sleep(TICK)

        # pastikan milestone pesan ini benar-benar tercapai sebelum lanjut
        current_pct = target

    render_status_line(100, SPINNER_FRAMES[0], "C:\\> ", messages[-1][0])
    print()

    # --- hening sejenak setelah selesai: prompt kosong, kursor tetap berkedip ---
    silence_end = time.time() + SILENCE_AFTER_COMPLETE
    blink_on = True
    last_blink = time.time()
    prompt = f"{GRAY}C:\\>{RESET} "
    while time.time() < silence_end:
        if time.time() - last_blink >= BLINK_INTERVAL:
            blink_on = not blink_on
            last_blink = time.time()
        cursor = (WHITE + CURSOR_CHAR + RESET) if blink_on else " "
        sys.stdout.write("\r" + CLEAR_LINE + prompt + cursor)
        sys.stdout.flush()
        time.sleep(TICK)
    sys.stdout.write("\r" + CLEAR_LINE)
    print("\n")


def type_simple(text, delay=TYPE_DELAY, end="\n"):
    for ch in text:
        sys.stdout.write(WHITE + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def dialog():
    time.sleep(0.6)
    print(BOLD + WHITE + "Nothing needs to be fixed right now." + RESET)
    print(GRAY + "You can just rest." + RESET)
    input(DIM + "\n[ Tekan Enter untuk OK ]" + RESET)
    # hapus baris prompt "[ Tekan Enter untuk OK ]" setelah ditekan
    sys.stdout.write("\033[1A" + CLEAR_LINE + "\r")
    sys.stdout.flush()


def make_a_wish():
    print()
    wish = input(
        WHITE + "Kalau boleh, tuliskan satu harapan kecilmu untuk hari ini: " + RESET
    ).strip()
    if not wish:
        wish = "sesuatu yang baik, apapun itu"

    # hapus baris pertanyaan + jawaban yang baru diketik
    sys.stdout.write("\033[1A" + CLEAR_LINE + "\r")
    sys.stdout.write("\033[1A" + CLEAR_LINE + "\r")
    sys.stdout.flush()

    # jeda sejenak seolah sedang "membaca" apa yang baru saja ditulis
    time.sleep(1.3)

    print()
    type_simple("Menjaga harapanmu", delay=0.06, end="")
    for _ in range(3):
        time.sleep(0.35)
        sys.stdout.write(WHITE + "." + RESET)
        sys.stdout.flush()
    print("\n")
    time.sleep(0.6)

    print(BOLD + WHITE + f'"{wish}"' + RESET)
    time.sleep(1.0)
    print(GRAY + "...semoga menemukan jalannya." + RESET)
    time.sleep(0.8)


def closing():
    lines = [
        "Selesai.",
        "Mungkin semuanya belum baik-baik saja.",
        "Tapi kamu sudah sampai sejauh ini,",
        "dan untuk hari ini, itu cukup.",
    ]
    print()
    for i, l in enumerate(lines):
        style = BOLD if i == 0 else ""
        print(style + WHITE + l + RESET)
        time.sleep(0.5)
    print()


def main():
    enable_ansi_on_windows()
    ensure_pyfiglet()
    clear()
    print_title()
    print(WHITE + "Tekan Enter untuk memulai proses." + RESET)
    input()
    print()
    run_loading()
    dialog()
    make_a_wish()
    closing()
    input(DIM + "Tekan Enter untuk menutup jendela ini..." + RESET)


if __name__ == "__main__":
    main()
