import streamlit as st
from math import gcd

st.set_page_config(page_title="Kalkulator RSA", page_icon="🔐")

# ---------- FUNGSI RSA ----------
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def pilih_e(phi):
    """Pilih e otomatis: utamakan 17, kalau tidak cocok cari yang terkecil."""
    if 17 < phi and gcd(17, phi) == 1:
        return 17
    for e in range(3, phi):
        if gcd(e, phi) == 1:
            return e
    return None

def buat_kunci(p, q):
    """Return (n, e, d, error)."""
    if not is_prime(p) or not is_prime(q):
        return None, None, None, "p dan q harus bilangan prima."
    if p == q:
        return None, None, None, "p dan q tidak boleh sama."
    n = p * q
    phi = (p - 1) * (q - 1)
    e = pilih_e(phi)
    if e is None:
        return None, None, None, "Prima terlalu kecil, pilih p dan q yang lebih besar."
    d = pow(e, -1, phi)
    return n, e, d, None

def rsa_enkripsi(angka_ascii, e, n):
    return [pow(m, e, n) for m in angka_ascii]

def rsa_dekripsi(cipher, d, n):
    return [pow(c, d, n) for c in cipher]

# ---------- FUNGSI ASCII & CAESAR ----------
def teks_ke_ascii(teks):
    return [ord(c) for c in teks]

def ascii_ke_teks(daftar):
    return "".join(chr(a) for a in daftar)

def geser_huruf(teks, geser):
    hasil = ""
    for char in teks:
        if char.isalpha() and char.isascii():
            dasar = ord('A') if char.isupper() else ord('a')
            hasil += chr((ord(char) - dasar + geser) % 26 + dasar)
        else:
            hasil += char
    return hasil

# ---------- FUNGSI TAMPILAN BERSAMA ----------
def form_enkripsi(prefix, pakai_caesar):
    c1, c2 = st.columns(2)
    p = int(c1.number_input("p (bilangan prima)", min_value=2, value=61, step=1, key=prefix + "_p"))
    q = int(c2.number_input("q (bilangan prima)", min_value=2, value=53, step=1, key=prefix + "_q"))
    geser = 0
    if pakai_caesar:
        geser = st.slider("Kunci Caesar (geseran)", 1, 25, 3, key=prefix + "_geser")
    pesan = st.text_input("Pesan:", key=prefix + "_pesan")

    n, e, d, err = buat_kunci(p, q)
    if err:
        st.error(err)
        return
    st.caption(f"Kunci publik (e, n) = ({e}, {n})  |  Kunci privat (d, n) = ({d}, {n})")

    if not pesan:
        return
    teks = geser_huruf(pesan, geser) if pakai_caesar else pesan
    if pakai_caesar:
        st.write("Setelah Caesar:", teks)
    ascii_list = teks_ke_ascii(teks)
    st.write("Kode ASCII:", ascii_list)
    if any(a >= n for a in ascii_list):
        st.error("Ada karakter yang kode ASCII-nya >= n. Pakai p dan q yang lebih besar.")
        return
    cipher = rsa_enkripsi(ascii_list, e, n)
    st.success("Hasil enkripsi: " + " ".join(map(str, cipher)))
    st.info(f"Simpan untuk dekripsi: n = {n}, d = {d}" + (f", kunci Caesar = {geser}" if pakai_caesar else ""))

def form_dekripsi(prefix, pakai_caesar):
    c1, c2 = st.columns(2)
    n = int(c1.number_input("n", min_value=2, value=3233, step=1, key=prefix + "_n"))
    d = int(c2.number_input("d", min_value=1, value=2753, step=1, key=prefix + "_d"))
    cipher_in = st.text_input("Angka hasil enkripsi (pisahkan spasi):", key=prefix + "_cipher")

    mode = "Kunci diketahui"
    geser = 0
    if pakai_caesar:
        mode = st.radio("Kunci Caesar:", ["Kunci diketahui", "Coba semua 25 kemungkinan"],
                        horizontal=True, key=prefix + "_mode")
        if mode == "Kunci diketahui":
            geser = st.slider("Kunci Caesar (geseran)", 1, 25, 3, key=prefix + "_geser")

    if not cipher_in:
        return
    try:
        cipher = [int(x) for x in cipher_in.split()]
        ascii_list = rsa_dekripsi(cipher, d, n)
        teks = ascii_ke_teks(ascii_list)
    except (ValueError, OverflowError):
        st.error("Gagal dekripsi. Cek angka input dan pastikan n dan d sepasang dengan saat enkripsi.")
        return

    st.write("Kode ASCII hasil RSA:", ascii_list)
    if not pakai_caesar:
        st.success("Hasil dekripsi: " + teks)
    elif mode == "Kunci diketahui":
        st.write("Teks sebelum Caesar dibalik:", teks)
        st.success("Hasil dekripsi: " + geser_huruf(teks, -geser))
    else:
        st.table([{"Geseran": k, "Hasil": geser_huruf(teks, -k)} for k in range(1, 26)])

# ---------- TAMPILAN ----------
st.title("🔐 Kalkulator RSA")
st.write("RSA + ASCII dan RSA + Caesar Cipher")

menu1, menu2 = st.tabs(["RSA + ASCII", "RSA + Caesar Cipher"])

with menu1:
    mode = st.radio("Pilih proses:", ["Enkripsi", "Dekripsi"], horizontal=True, key="mode1")
    if mode == "Enkripsi":
        form_enkripsi("a_enk", pakai_caesar=False)
    else:
        form_dekripsi("a_dek", pakai_caesar=False)

with menu2:
    mode = st.radio("Pilih proses:", ["Enkripsi", "Dekripsi"], horizontal=True, key="mode2")
    if mode == "Enkripsi":
        form_enkripsi("c_enk", pakai_caesar=True)
    else:
        form_dekripsi("c_dek", pakai_caesar=True)
