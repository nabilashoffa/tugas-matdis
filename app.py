import streamlit as st
import pandas as pd
import math

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="RSA Little Lab",
    page_icon="🌷",
    layout="wide"
)

# ==========================================
# CSS DESIGN
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background: #FFE0EF;
    color: #594456;
    font-family: 'DM Sans', sans-serif;
}

/* Main width */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide default header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #AD5D89 !important;
}

/* Scallop header */
.hero {
    background-color: #F7A9CD;
    background-image: radial-gradient(
        circle at 25px 0,
        #FFE0EF 24px,
        transparent 25px
    );
    background-size: 50px 50px;
    background-repeat: repeat-x;
    border-radius: 25px;
    padding: 45px 25px 30px 25px;
    text-align: center;
    box-shadow: 0 6px 15px rgba(193, 111, 157, 0.12);
}

.hero h1 {
    font-size: 42px !important;
    color: #FFFFFF !important;
    margin-bottom: 0px;
}

.hero p {
    color: #FFF7FC;
    font-size: 16px;
    margin-top: 8px;
}

/* Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFF9FC;
    border: 1.5px solid #F5C7DF;
    border-radius: 22px;
    padding: 12px;
}

/* Inputs */
.stNumberInput input,
.stTextInput input {
    background: #FFF2F8 !important;
    border: 1px solid #F1C4DB !important;
    border-radius: 12px !important;
    color: #77566B !important;
}

/* Radio */
div[role="radiogroup"] {
    background: #FFF8FC;
    border: 1px solid #F3C7DE;
    border-radius: 50px;
    padding: 10px 18px;
    width: fit-content;
}

/* Buttons */
.stButton > button {
    background: #F19BC5;
    color: white;
    border: 0px;
    border-radius: 14px;
    padding: 8px 22px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #DC7EAD;
    color: white;
    border: 0px;
    transform: translateY(-2px);
}

/* Success box */
div[data-testid="stAlert"] {
    border-radius: 16px;
}

/* Table */
div[data-testid="stDataFrame"] {
    border: 1px solid #F3C7DE;
    border-radius: 14px;
    overflow: hidden;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #FFF0F8;
    border: 1px solid #F3C7DE;
    border-radius: 18px;
    padding: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #B77D9F;
}

div[data-testid="stMetricValue"] {
    color: #A85587;
}

/* Divider */
hr {
    border-color: #F3C7DE !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #C17FA3;
    padding: 25px 5px;
    font-size: 14px;
}

/* Small screens */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 30px !important;
    }
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNCTIONS
# ==========================================

def cek_prima(angka):
    if angka < 2:
        return False

    for i in range(2, int(math.sqrt(angka)) + 1):
        if angka % i == 0:
            return False

    return True


def cari_d(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🌷 RSA Little Lab 🌷</h1>
    <p>♡ Turn your words into little secret codes ♡</p>
</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown(
    "<p style='text-align:center;color:#B77D9F;'>"
    "✿  Choose your magical operation  ✿"
    "</p>",
    unsafe_allow_html=True
)

proses = st.radio(
    "Mode",
    ["🔒 Enkripsi", "🔓 Dekripsi"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")


# ==========================================
# ENCRYPTION
# ==========================================

if proses == "🔒 Enkripsi":

    st.markdown("## 💌 Encrypt a Message")
    st.caption("Masukkan kunci RSA dan pesan yang ingin kamu enkripsi.")

    with st.container(border=True):

        st.markdown("### ୨୧ RSA Keys")

        col1, col2, col3 = st.columns(3)

        with col1:
            p = st.number_input(
                "Prime number (p)",
                min_value=2,
                value=11,
                step=1
            )

        with col2:
            q = st.number_input(
                "Prime number (q)",
                min_value=2,
                value=13,
                step=1
            )

        with col3:
            e = st.number_input(
                "Public exponent (e)",
                min_value=2,
                value=7,
                step=1
            )

        pesan = st.text_input(
            "♡ Your message",
            placeholder="Type something sweet here..."
        )

    # Validasi p dan q
    if not cek_prima(p) or not cek_prima(q):
        st.error("Oops! p dan q harus berupa bilangan prima.")

    elif p == q:
        st.error("p dan q harus berbeda ya!")

    else:

        n = p * q
        phi = (p - 1) * (q - 1)
        d = cari_d(e, phi)

        st.markdown("### ✧ Key Summary ✧")

        c1, c2, c3 = st.columns(3)

        c1.metric("Modulus · n", n)
        c2.metric("Euler Phi · φ", phi)
        c3.metric("Private Key · d", d if d else "Invalid")

        if math.gcd(e, phi) != 1:
            st.error(
                "e harus relatif prima dengan φ(n). "
                "Coba gunakan nilai e yang lain."
            )

        elif d is None:
            st.error("Kunci d tidak dapat ditemukan.")

        else:

            if pesan:

                tabel = []
                hasil = []
                muat = True

                for huruf in pesan:

                    m = ord(huruf)

                    if m >= n:
                        muat = False

                    cipher = pow(m, e, n)
                    hasil.append(cipher)

                    tabel.append({
                        "Character": huruf,
                        "ASCII (m)": m,
                        "Encryption": f"{m}^{e} mod {n}",
                        "Cipher (c)": cipher
                    })

                if not muat:

                    st.warning(
                        f"Kode ASCII pesan harus lebih kecil dari n = {n}. "
                        "Gunakan p dan q yang lebih besar."
                    )

                else:

                    st.markdown("### 🎀 Your Ciphertext")

                    with st.container(border=True):

                        st.markdown(
                            "<p style='color:#C06B9A;font-weight:bold;'>"
                            "✧ Secret code ✧</p>",
                            unsafe_allow_html=True
                        )

                        st.code(
                            " ".join(map(str, hasil)),
                            language=None
                        )

                        st.caption(
                            "Klik ikon copy pada kotak ciphertext untuk menyalin."
                        )

                    st.markdown("### 🌸 ASCII Transformation")

                    st.dataframe(
                        pd.DataFrame(tabel),
                        use_container_width=True,
                        hide_index=True
                    )

                    st.success("Yay! Pesan berhasil dienkripsi ♡")

                    st.markdown("### 🔑 Save these keys")

                    st.code(f"n = {n}\nd = {d}")

                    st.caption(
                        "Simpan n dan d. Keduanya akan digunakan "
                        "untuk proses dekripsi."
                    )

            else:
                st.info("♡ Pesanmu masih kosong. Ketik pesan untuk memulai!")


# ==========================================
# DECRYPTION
# ==========================================

else:

    st.markdown("## 💝 Decrypt a Message")
    st.caption("Masukkan ciphertext dan kunci privat untuk membuka pesan.")

    with st.container(border=True):

        st.markdown("### ୨୧ Decryption Keys")

        col1, col2 = st.columns(2)

        with col1:
            n = st.number_input(
                "Modulus (n)",
                min_value=2,
                value=143,
                step=1
            )

        with col2:
            d = st.number_input(
                "Private key (d)",
                min_value=1,
                value=103,
                step=1
            )

        cipher_teks = st.text_input(
            "♡ Ciphertext",
            placeholder="Example: 72 117  ...",
        )

    if cipher_teks:

        try:

            daftar = [int(x) for x in cipher_teks.split()]

            tabel = []
            hasil = ""

            for c in daftar:

                if c < 0 or c >= n:
                    raise ValueError(
                        f"Cipher {c} harus berada di antara 0 dan n-1."
                    )

                m = pow(c, d, n)

                if not (0 <= m <= 0x10FFFF):
                    raise ValueError(
                        "Hasil dekripsi bukan kode karakter yang valid."
                    )

                huruf = chr(m)
                hasil += huruf

                tabel.append({
                    "Cipher (c)": c,
                    "Decryption": f"{c}^{d} mod {n}",
                    "ASCII (m)": m,
                    "Character": huruf
                })

            st.markdown("### ✨ Revealed Message")

            with st.container(border=True):

                st.markdown(
                    "<p style='color:#C06B9A;font-weight:bold;'>"
                    "♡ Your message ♡</p>",
                    unsafe_allow_html=True
                )

                st.code(hasil, language=None)

            st.markdown("### 🌷 Decryption Table")

            st.dataframe(
                pd.DataFrame(tabel),
                use_container_width=True,
                hide_index=True
            )

            st.success("Secret message successfully revealed! ♡")

        except ValueError as err:

            st.error(f"Input tidak valid: {err}")

    else:

        st.info("♡ Masukkan ciphertext untuk membuka pesan rahasia.")


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    ✿ ─────── made with love & mathematics ─────── ✿<br>
    <span style="font-size:12px;">
        RSA Little Lab · Encrypt your little secrets ♡
    </span>
</div>
""", unsafe_allow_html=True)
