import streamlit as st

st.title("Kalkulator Enkripsi & Dekripsi")
st.write("Halo, web berhasil jalan!")
import streamlit as st

def geser_huruf(teks, geser):
    hasil = ""
    for char in teks:
        if char.isalpha():
            dasar = ord('A') if char.isupper() else ord('a')
            hasil += chr((ord(char) - dasar + geser) % 26 + dasar)
        else:
            hasil += char
    return hasil

def enkripsi(teks, kunci):
    return geser_huruf(teks, kunci)

def dekripsi(teks, kunci):
    return geser_huruf(teks, -kunci)

st.title("Kalkulator Enkripsi & Dekripsi")
st.write("Metode: Caesar Cipher")

pesan = st.text_input("Masukkan pesan:")
kunci = st.number_input("Kunci (geseran):", min_value=1, max_value=25, value=3, step=1)

if pesan:
    st.subheader("Hasil")
    st.success(f"Enkripsi: {enkripsi(pesan, kunci)}")
    st.info(f"Dekripsi: {dekripsi(pesan, kunci)}")
