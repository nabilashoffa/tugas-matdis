import streamlit as st

st.title("Kalkulator RSA + ASCII")

# ---------- FUNGSI BANTU ----------

def cek_prima(angka):
    # Prima = hanya habis dibagi 1 dan dirinya sendiri
    if angka < 2:
        return False
    for i in range(2, angka):
        if angka % i == 0:
            return False
    return True

def cari_d(e, phi):
    # d = angka yang membuat (e x d) dibagi phi bersisa 1
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None

# ---------- PILIH PROSES ----------

proses = st.radio("Pilih proses:", ["Enkripsi", "Dekripsi"], horizontal=True)

# ================= ENKRIPSI =================
if proses == "Enkripsi":
    st.subheader("Enkripsi")

    p = int(st.number_input("p (bilangan prima):", min_value=2, value=11))
    q = int(st.number_input("q (bilangan prima):", min_value=2, value=13))
    e = int(st.number_input("e (kunci publik):", min_value=2, value=7))
    pesan = st.text_input("Pesan:")

    if not cek_prima(p) or not cek_prima(q):
        st.error("p dan q harus bilangan prima.")
    elif p == q:
        st.error("p dan q tidak boleh sama.")
    else:
        # Langkah 1: hitung n, phi, dan d
        n = p * q
        phi = (p - 1) * (q - 1)
        d = cari_d(e, phi)

        st.write("n = p x q =", n)
        st.write("phi = (p-1) x (q-1) =", phi)

        if d is None:
            st.error("e tidak cocok dengan phi. Coba e yang lain.")
        else:
            st.write("d (kunci privat) =", d)

            if pesan:
                # Langkah 2: tiap huruf diubah ke ASCII, lalu dienkripsi
                tabel = []
                hasil = []
                muat = True

                for huruf in pesan:
                    m = ord(huruf)          # huruf -> angka ASCII
                    if m >= n:
                        muat = False
                    c = pow(m, e, n)        # c = m^e mod n
                    hasil.append(c)
                    tabel.append({
                        "Huruf": huruf,
                        "ASCII (m)": m,
                        "Rumus": f"{m}^{e} mod {n}",
                        "Cipher (c)": c,
                    })

                if not muat:
                    st.error("Ada kode ASCII >= n. Pakai p dan q yang lebih besar.")
                else:
                    st.table(tabel)
                    st.success("Hasil enkripsi: " + " ".join(str(x) for x in hasil))
                    st.info(f"Untuk dekripsi, simpan: n = {n} dan d = {d}")

# ================= DEKRIPSI =================
else:
    st.subheader("Dekripsi")

    n = int(st.number_input("n:", min_value=2, value=143))
    d = int(st.number_input("d:", min_value=1, value=103))
    cipher_teks = st.text_input("Angka hasil enkripsi (pisahkan dengan spasi):")

    if cipher_teks:
        try:
            # Ubah teks "114 52 ..." menjadi daftar angka
            daftar = [int(x) for x in cipher_teks.split()]

            tabel = []
            hasil = ""

            for c in daftar:
                m = pow(c, d, n)            # m = c^d mod n
                hasil = hasil + chr(m)      # angka ASCII -> huruf
                tabel.append({
                    "Cipher (c)": c,
                    "Rumus": f"{c}^{d} mod {n}",
                    "ASCII (m)": m,
                    "Huruf": chr(m),
                })

            st.table(tabel)
            st.success("Hasil dekripsi: " + hasil)
        except ValueError:
            st.error("Input salah, atau n dan d tidak cocok dengan saat enkripsi.")
