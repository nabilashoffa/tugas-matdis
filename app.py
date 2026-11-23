import streamlit as st
import hashlib
import base64

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Digital Signature Lab",
    page_icon="🌷",
    layout="wide"
)


# ==========================================
# CSS DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #FFE0EF;
    color: #594456;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #AD5D89 !important;
}

.hero {
    background: #F7A9CD;
    border-radius: 25px;
    padding: 40px 25px;
    text-align: center;
    box-shadow: 0 6px 15px rgba(193,111,157,0.12);
}

.hero h1 {
    color: white !important;
    font-size: 40px;
}

.hero p {
    color: #FFF7FC;
    font-size: 16px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFF9FC;
    border: 1.5px solid #F5C7DF;
    border-radius: 20px;
    padding: 12px;
}

.stButton > button {
    background: #F19BC5;
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 8px 20px;
}

.stButton > button:hover {
    background: #DC7EAD;
    color: white;
}

.stDownloadButton > button {
    background: #E8A0C3;
    color: white;
    border-radius: 12px;
    border: none;
}

div[data-testid="stMetric"] {
    background: #FFF0F8;
    border: 1px solid #F3C7DE;
    border-radius: 15px;
    padding: 15px;
}

div[data-testid="stMetricValue"] {
    color: #A85587;
}

.footer {
    text-align: center;
    color: #C17FA3;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "private_key_pem" not in st.session_state:
    st.session_state.private_key_pem = None

if "public_key_pem" not in st.session_state:
    st.session_state.public_key_pem = None

if "signature_data" not in st.session_state:
    st.session_state.signature_data = None


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🌷 Digital Signature Lab 🌷</h1>
    <p>♡ Secure your documents with digital signatures ♡</p>
</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown(
    "<p style='text-align:center;color:#B77D9F;'>"
    "✿ Create keys · Sign documents · Verify signatures ✿"
    "</p>",
    unsafe_allow_html=True
)


# ==========================================
# GENERATE KEY PAIR
# ==========================================

st.markdown("## 🔑 Generate Digital Keys")

with st.container(border=True):

    st.write(
        "Buat pasangan kunci yang terdiri dari "
        "Private Key dan Public Key menggunakan Ed25519."
    )

    if st.button("Generate Key Pair"):

        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        st.session_state.private_key_pem = private_pem
        st.session_state.public_key_pem = public_pem
        st.session_state.signature_data = None

        st.success("Key pair berhasil dibuat!")


    if st.session_state.private_key_pem:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔐 Private Key")

            st.download_button(
                "Download Private Key",
                data=st.session_state.private_key_pem,
                file_name="private_key.pem",
                mime="application/x-pem-file"
            )

        with col2:
            st.markdown("### 🔓 Public Key")

            st.download_button(
                "Download Public Key",
                data=st.session_state.public_key_pem,
                file_name="public_key.pem",
                mime="application/x-pem-file"
            )

        st.warning(
            "Simpan Private Key secara rahasia. "
            "Jangan membagikannya kepada penerima dokumen."
        )

    else:
        st.info("Generate key pair terlebih dahulu.")


st.divider()


# ==========================================
# DIGITAL SIGNATURE OPERATIONS
# ==========================================

tab1, tab2 = st.tabs([
    "✍️ Create Signature",
    "🔍 Verify Signature"
])


# ==========================================
# CREATE SIGNATURE
# ==========================================

with tab1:

    st.markdown("## ✍️ Create Digital Signature")

    st.caption(
        "Upload dokumen untuk menghasilkan hash "
        "dan tanda tangan digital."
    )

    with st.container(border=True):

        document = st.file_uploader(
            "Upload your document",
            key="sign_document"
        )

        if st.button("Create Digital Signature"):

            if document is None:

                st.error("Upload dokumen terlebih dahulu.")

            elif st.session_state.private_key_pem is None:

                st.error("Generate Key Pair terlebih dahulu.")

            else:

                # Membaca isi dokumen
                document_data = document.getvalue()

                # Membuat SHA-256 hash
                document_hash = hashlib.sha256(
                    document_data
                ).digest()

                # Memuat private key
                private_key = serialization.load_pem_private_key(
                    st.session_state.private_key_pem,
                    password=None
                )

                # Menandatangani hash menggunakan private key
                signature = private_key.sign(document_hash)

                # Mengubah signature menjadi Base64
                signature_base64 = base64.b64encode(
                    signature
                ).decode("utf-8")

                # Menyimpan hasil
                st.session_state.signature_data = {
                    "signature": signature_base64,
                    "hash": document_hash.hex(),
                    "filename": document.name
                }

                st.success("Digital Signature berhasil dibuat!")


    if st.session_state.signature_data:

        result = st.session_state.signature_data

        st.markdown("### 🌸 Document Hash (SHA-256)")

        st.code(result["hash"])

        st.markdown("### 🎀 Digital Signature")

        st.code(result["signature"])

        st.download_button(
            "Download Digital Signature",
            data=result["signature"],
            file_name="digital_signature.txt",
            mime="text/plain"
        )

        st.caption(
            "Signature ini dibuat menggunakan Private Key. "
            "Simpan signature bersama dokumen yang ditandatangani."
        )


# ==========================================
# VERIFY SIGNATURE
# ==========================================

with tab2:

    st.markdown("## 🔍 Verify Digital Signature")

    st.caption(
        "Periksa keaslian dokumen menggunakan Public Key "
        "dan Digital Signature."
    )

    with st.container(border=True):

        verify_document = st.file_uploader(
            "Upload document to verify",
            key="verify_document"
        )

        public_key_file = st.file_uploader(
            "Upload Public Key (.pem)",
            type=["pem"],
            key="verify_public_key"
        )

        signature_file = st.file_uploader(
            "Upload Digital Signature (.txt)",
            type=["txt"],
            key="verify_signature"
        )

        if st.button("Verify Digital Signature"):

            if (
                verify_document is None
                or public_key_file is None
                or signature_file is None
            ):

                st.error("Lengkapi semua file terlebih dahulu.")

            else:

                try:

                    # Membaca dokumen
                    document_data = verify_document.getvalue()

                    # Membuat ulang SHA-256 hash
                    document_hash = hashlib.sha256(
                        document_data
                    ).digest()

                    # Memuat public key
                    public_key = serialization.load_pem_public_key(
                        public_key_file.getvalue()
                    )

                    if not isinstance(public_key, Ed25519PublicKey):
                        raise ValueError(
                            "Public Key bukan format Ed25519."
                        )

                    # Membaca signature Base64
                    signature_base64 = (
                        signature_file.getvalue().decode("utf-8").strip()
                    )

                    signature = base64.b64decode(
                        signature_base64,
                        validate=True
                    )

                    # Memverifikasi signature
                    public_key.verify(
                        signature,
                        document_hash
                    )

                    st.success(
                        "SIGNATURE VALID! "
                        "Dokumen sesuai dengan tanda tangan digital."
                    )

                    st.markdown("### 🌸 Verification Result")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Document Status",
                        "Authentic"
                    )

                    col2.metric(
                        "Signature Status",
                        "Valid"
                    )

                    st.markdown("### SHA-256 Hash")

                    st.code(document_hash.hex())

                except InvalidSignature:

                    st.error(
                        "SIGNATURE INVALID! "
                        "Dokumen berubah atau signature tidak cocok "
                        "dengan Public Key."
                    )

                except (ValueError, TypeError, UnicodeDecodeError) as err:

                    st.error(f"Input tidak valid: {err}")

                except Exception:

                    st.error(
                        "Terjadi kesalahan saat memproses file atau key."
                    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
    ✿ ───── made with love & mathematics ───── ✿
    <br>
    <span style="font-size:12px;">
        Digital Signature Lab · Secure your documents ♡
    </span>
</div>
""", unsafe_allow_html=True)
