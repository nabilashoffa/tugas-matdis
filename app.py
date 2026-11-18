import streamlit as st
from math import gcd

st.set_page_config(page_title="Kalkulator Kriptografi", page_icon="🔐")

# ---------- FUNGSI RSA ----------
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def hitung_kunci(p, q, e):
    """Return (n, phi, d, error)."""
    if not is_prime(p) or not is_prime(q):
        return None, None, None, "p dan q harus bilangan prima."
    if p == q:
        return None, None, None, "p dan q tidak boleh sama."
    n = p * q
    phi = (p - 1) * (q - 1)
    if not (1 < e < phi) or gcd(e, phi) != 1:
        return None, None, None, f"e harus 1 < e < {phi} dan relatif prima dengan {phi}."
    d = pow(e, -1, phi)
    return n, phi, d, None

def enkripsi_rsa(teks, e, n):
    return [pow(ord(c), e, n) for c in teks]

def dekripsi_rsa(daftar, d, n):
    return "".join(chr(pow(c, d, n)) for c in daftar)

# ---------- FUNGSI ASCII ----------
def teks_ke_ascii(teks):
    return [ord(c) for c in teks]

def ascii_ke_teks(daftar):
    return "".join(chr(a) for a in daftar)

# ---------- FUNGSI CAESAR ----------
def geser_huruf(teks, geser):
    hasil = ""
    for char in teks:
        if char.isalpha() and char.isascii():
            dasar = ord('A') if char.isupper() else ord('a')
            hasil += chr((ord(char) - dasar + geser) % 26 + dasar)
        else:
            hasil += char
    return hasil

# ---------- DETEKSI OTOMATIS ----------
def deteksi_jenis(teks):
    token = teks.split()
    if token and all(t.isdigit() for t in token):
        angka = [int(t) for t in token]
        return "ascii" if all(0 <= a <= 127 for a in angka) else "rsa"
    if any(c.isalpha() for c in teks):
        return "caesar"
    return "tidak dikenali"

# ---------- TAMPILAN ----------
st.title("🔐 Kalkulator Kriptografi")
st.write("RSA, ASCII, dan Caesar Cipher: enkripsi & dekripsi, plus deteksi otomatis.")

tab_rsa, tab_ascii, tab_caesar, tab_auto = st.tabs(
    ["RSA", "ASCII", "Caesar Cipher", "Deteksi Otomatis"]
)

# ===================== TAB RSA =====================
with tab_rsa:
    sub_enk, sub_dek = st.tabs(["Enkripsi", "Dekripsi"])

    # ---- Enkripsi RSA ----
    with sub_enk:
        mode = st.radio(
            "Kunci yang kamu punya:",
            ["Dari p, q, e", "Langsung e dan n"],
            horizontal=True, key="mode_enk",
        )
        e_enk, n_enk, siap = None, None, False

        if mode == "Dari p, q, e":
            c1, c2, c3 = st.columns(3)
            p = c1.number_input("p (prima)", min_value=2, value=61, step=1, key="p_enk")
            q = c2.number_input("q (prima)", min_value=2, value=53, step=1, key="q_enk")
            e_in = c3.number_input("e", min_value=2, value=17, step=1, key="e_enk_a")
            n_, phi_, d_, err = hitung_kunci(int(p), int(q), int(e_in))
            if err:
                st.error(err)
            else:
                e_enk, n_enk, siap = int(e_in), n_, True
                st.caption(f"n = {n_} | phi = {phi_} | kunci privat d = {d_} (simpan untuk dekripsi)")
        else:
            c1, c2 = st.columns(2)
            e_enk = int(c1.number_input("e", min_value=2, value=17, step=1, key="e_enk_b"))
            n_enk = int(c2.number_input("n", min_value=2, value=3233, step=1, key="n_enk_b"))
            siap = True

        pesan = st.text_input("Pesan (teks biasa):", key="pesan_rsa")
        if siap and pesan:
            if any(ord(c) >= n_enk for c in pesan):
                st.error("Ada karakter yang kode ASCII-nya >= n. Pakai n yang lebih besar.")
            else:
                st.write("Kode ASCII:", teks_ke_ascii(pesan))
                cipher = enkripsi_rsa(pesan, e_enk, n_enk)
                st.success("Hasil enkripsi: " + " ".join(map(str, cipher)))

    # ---- Dekripsi RSA ----
    with sub_dek:
        mode = st.radio(
            "Kunci yang kamu punya:",
            ["Langsung d dan n", "Dari p, q, e"],
            horizontal=True, key="mode_dek",
        )
        d_dek, n_dek, siap = None, None, False

        if mode == "Langsung d dan n":
            c1, c2 = st.columns(2)
            d_dek = int(c1.number_input("d", min_value=1, value=2753, step=1, key="d_dek_a"))
            n_dek = int(c2.number_input("n", min_value=2, value=3233, step=1, key="n_dek_a"))
            siap = True
        else:
            c1, c2, c3 = st.columns(3)
            p = c1.number_input("p (prima)", min_value=2, value=61, step=1, key="p_dek")
            q = c2.number_input("q (prima)", min_value=2, value=53, step=1, key="q_dek")
            e_in = c3.number_input("e", min_value=2, value=17, step=1, key="e_dek")
            n_, phi_, d_, err = hitung_kunci(int(p), int(q), int(e_in))
            if err:
                st.error(err)
            else:
                d_dek, n_dek, siap = d_, n_, True
                st.caption(f"d dihitung otomatis = {d_} | n = {n_}")

        cipher_in = st.text_input("Angka hasil enkripsi (pisahkan spasi):", key="cipher_rsa")
        if siap and cipher_in:
            try:
                angka = [int(x) for x in cipher_in.split()]
                st.success("Hasil dekripsi: " + dekripsi_rsa(angka, d_dek, n_dek))
            except (ValueError, OverflowError):
                st.error("Input salah, atau kunci tidak cocok dengan yang dipakai saat enkripsi.")

# ===================== TAB ASCII =====================
with tab_ascii:
    a1, a2 = st.tabs(["Enkripsi (teks → ASCII)", "Dekripsi (ASCII → teks)"])
    with a1:
        t = st.text_input("Teks:", key="teks_ascii")
        if t:
            st.success("Kode ASCII: " + " ".join(map(str, teks_ke_ascii(t))))
    with a2:
        k = st.text_input("Kode ASCII (pisahkan spasi):", key="kode_ascii")
        if k:
            try:
                st.success("Teks: " + ascii_ke_teks([int(x) for x in k.split()]))
            except (ValueError, OverflowError):
                st.error("Isi dengan angka yang dipisah spasi (0 sampai 1114111).")

# ===================== TAB CAESAR =====================
with tab_caesar:
    c_enk, c_dek = st.tabs(["Enkripsi", "Dekripsi"])
    with c_enk:
        t = st.text_input("Teks asli:", key="teks_cae_enk")
        geser = st.slider("Kunci geseran", 1, 25, 3, key="geser_enk")
        if t:
            st.success("Hasil enkripsi: " + geser_huruf(t, geser))
    with c_dek:
        t = st.text_input("Teks terenkripsi:", key="teks_cae_dek")
        cara = st.radio(
            "Cara dekripsi:",
            ["Kunci diketahui", "Coba semua 25 kemungkinan"],
            horizontal=True, key="cara_cae",
        )
        if t:
            if cara == "Kunci diketahui":
                geser = st.slider("Kunci geseran", 1, 25, 3, key="geser_dek")
                st.success("Hasil dekripsi: " + geser_huruf(t, -geser))
            else:
                st.table([{"Geseran": k, "Hasil": geser_huruf(t, -k)} for k in range(1, 26)])

# ===================== TAB DETEKSI OTOMATIS =====================
with tab_auto:
    teks_in = st.text_input("Masukkan teks / angka apa saja:", key="deteksi")
    if teks_in:
        jenis = deteksi_jenis(teks_in)
        if jenis == "ascii":
            st.info("Terdeteksi: **kode ASCII**")
            st.success("Teks: " + "".join(chr(int(x)) for x in teks_in.split()))
        elif jenis == "rsa":
            st.info("Terdeteksi: **angka besar, kemungkinan hasil RSA**")
            st.write("Tempel ke tab **RSA > Dekripsi** dan isi kunci d dan n.")
        elif jenis == "caesar":
            st.info("Terdeteksi: **teks huruf, kemungkinan Caesar Cipher**")
            st.table([{"Geseran": k, "Hasil dekripsi": geser_huruf(teks_in, -k)} for k in range(1, 26)])
        else:
            st.warning("Jenis input tidak dikenali.")
