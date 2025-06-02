# app.py (Versi 2.1 - FINAL & Diperbaiki)

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- PERBAIKAN #1: Muat environment dan konfigurasi halaman DI AWAL ---
# Ini harus menjadi perintah Streamlit pertama yang dijalankan.
st.set_page_config(
    page_title="AI Mentor",
    page_icon="🤖"
)
load_dotenv()

# --- FUNGSI AUTENTIKASI (Tidak ada perubahan di sini) ---
def check_password():
    """Mengembalikan True jika password benar, False jika salah."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    password_input = st.text_input("Masukkan Password Akses", type="password", key="password_input")
    correct_password = os.getenv("APP_PASSWORD")

    if st.button("Masuk"):
        if password_input == correct_password:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Password yang Anda masukkan salah.")
    return False

# --- KODE UTAMA APLIKASI ---
# Seluruh aplikasi Anda dibungkus dengan kondisi ini
if check_password():
    # Judul dan caption sekarang berada di dalam blok yang benar
    st.title("🤖 AI Mentor Pribadimu")
    st.caption("Ditenagai oleh Google Gemini & dibuat olehmu!")

    # --- PERBAIKAN #2 (BONUS): Ambil API_URL dari .env ---
    # Lebih baik menyimpan URL backend di .env agar mudah diganti
    API_URL = os.getenv("API_URL", "https://4cee6cb8-fcd1-4f7d-89af-7f18b7ec0f0b-00-1ipp6b8viwbtg.kirk.replit.dev:3001/") # Default URL jika tidak ada di .env

    # --- Inisialisasi Chat History (Tidak ada perubahan) ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Menampilkan riwayat chat (Tidak ada perubahan) ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Komponen UI di sidebar (Tidak ada perubahan) ---
    st.sidebar.header("Kontrol Mentor")
    pilihan_persona = st.sidebar.selectbox(
        "Pilih Persona:",
        ("General", "Excel", "Marketing", "Digital Product"),
        key="persona_selector"
    )

    # --- Menerima Input dari Pengguna (Tidak ada perubahan) ---
    if prompt := st.chat_input("Tulis pertanyaanmu di sini..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Mentor sedang berpikir..."):
            try:
                # Memastikan URL diakhiri dengan slash
                if not API_URL.endswith('/'):
                    API_URL += '/'
                
                full_url = f"{API_URL}ask-persona"
                
                response = requests.get(
                    full_url,
                    params={
                        "persona": pilihan_persona.lower(),
                        "pertanyaan": prompt
                    }
                )
                response.raise_for_status()
                hasil = response.json()
                jawaban_ai = hasil.get('jawaban_ai', 'Maaf, terjadi kesalahan pada format jawaban.')
                
                with st.chat_message("assistant"):
                    st.markdown(jawaban_ai)
                st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})

            except Exception as e:
                st.error(f"Gagal memproses permintaan: {e}")
