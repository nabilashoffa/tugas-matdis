import streamlit as st
from math import gcd

st.set_page_config(page_title="Kalkulator RSA", page_icon="🔐")

# ---------- FUNGSI BANTU ----------
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def buat_kunci(p, q, e):
    """Mengembalikan (n, phi, d) atau pesan error."""
    if not is_prime(p) or not is_prime(q):
        return None, "p dan q harus bilangan prima."
    if p == q:
        return None, "p dan q tidak boleh sama."
    n = p * q
    if n < 256:
        return None, "p x q harus minimal 256 supaya semua kode ASCII muat."
    phi = (p - 1) * (q - 1)
    if not (1 < e < phi) or gcd(e, phi) != 1:
        return None, f"e harus 1 < e < {phi} dan relatif prima dengan {phi}."
    d = pow(e, -1, phi)  # invers modulo
    return (n, phi, d), None

def enkripsi_rsa(teks, e, n):
    hasil = []
    for char in teks:
        m = ord(char)              # huruf -> ASCII
        hasil.append(pow(m, e, n)) # c = m^e mod n
    return hasil

def dekripsi_rsa(daftar_angka, d, n):
    teks = ""
    for c in daftar_angka:
        m = pow(c, d, n)           # m = c^d mod n
        teks += chr(m)             # ASCII -> huruf
    return teks

def geser_huruf(teks, geser):
    hasil = ""
    for char in teks:
        if char.isalpha() and char.isascii():
            dasar = ord('A') if char.isupper() else ord('a')
            hasil += chr((ord(char) - dasar + geser) % 26 + dasar)
        else:
            hasil += char
    return hasil

def deteksi_jenis(teks):
    token = teks.split()
    if token and all(t.isdigit() for t in token):
        angka = [int(t) for t in token]
        if all(0 <= a <= 127 for a in angka):
            return "ascii"
        return "rsa"
    if any(c.isalpha() for c in teks):
        return "caesar"
    return "tidak dikenali"

# ---------- SIDEBAR: KUNCI RSA ----------
st.sidebar.header("Pengaturan Kunci RSA")
p = st.sidebar.number_input("Bilangan prima p", min_value=2, value=61, step=1)
q = st.sidebar.number_input("Bilangan prima q", min_value=2, value=53, step=1)
e = st.sidebar.number_input("Kunci publik e", min_value=2, value=17, step=1)

kunci, error = buat_kunci(int(p), int(q), int(e))

st.title("🔐 Kalkulator RSA")
st.write("Enkripsi & dekripsi RSA dengan kode ASCII, plus deteksi otomatis ASCII / Caesar Cipher.")

if error:
    st.error(error)
    st.stop()

n, phi, d = kunci
st.sidebar.success("Kunci valid")
st.sidebar.write(f"n = {n}")
st.sidebar.write(f"phi(n) = {phi}")
st.sidebar.write(f"**Kunci publik (e, n)** = ({e}, {n})")
st.sidebar.write(f"**Kunci privat (d, n)** = ({d}, {n})")

# ---------- TAB ----------
tab1, tab2, tab3 = st.tabs(["Enkripsi RSA", "Dekripsi RSA", "Deteksi Otomatis"])

with tab1:
    pesan = st.text_input("Masukkan pesan (teks biasa):", key="pesan_enk")
    if pesan:
        if any(ord(c) >= n for c in pesan):
            st.error("Ada karakter yang kode ASCII-nya >= n. Perbesar p dan q.")
        else:
            st.write("Kode ASCII:", [ord(c) for c in pesan])
            cipher = enkripsi_rsa(pesan, int(e), n)
            st.success("Hasil enkripsi: " + " ".join(map(str, cipher)))

with tab2:
    cipher_in = st.text_input("Masukkan angka hasil enkripsi (pisahkan spasi):", key="cipher_dek")
    if cipher_in:
        try:
            angka = [int(x) for x in cipher_in.split()]
            teks = dekripsi_rsa(angka, d, n)
            st.success("Hasil dekripsi: " + teks)
        except (ValueError, OverflowError):
            st.error("Input harus berupa angka yang dipisah spasi, dan harus dari kunci yang sama.")

with tab3:
    teks_in = st.text_input("Masukkan teks / angka apa saja:", key="deteksi")
    if teks_in:
        jenis = deteksi_jenis(teks_in)
        if jenis == "ascii":
            st.info("Terdeteksi: **kode ASCII**")
            hasil = "".join(chr(int(x)) for x in teks_in.split())
            st.success("Diterjemahkan ke huruf: " + hasil)
        elif jenis == "rsa":
            st.info("Terdeteksi: **angka besar, kemungkinan hasil RSA**")
            st.write("Coba tempel ke tab **Dekripsi RSA** (pakai kunci yang sama).")
        elif jenis == "caesar":
            st.info("Terdeteksi: **teks huruf, kemungkinan Caesar Cipher**")
            st.write("Semua kemungkinan geseran:")
            tabel = [{"Geseran": k, "Hasil dekripsi": geser_huruf(teks_in, -k)} for k in range(1, 26)]
            st.table(tabel)
        else:
            st.warning("Jenis input tidak dikenali.")
            
