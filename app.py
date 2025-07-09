import streamlit as st
from utils import extract_text, extract_bab1, analyze_bab1

st.title("📘 Feedback Otomatis Naskah Akademik Mahasiswa")
st.markdown("Upload file skripsi (.docx / .pdf), dan sistem akan memberikan evaluasi otomatis untuk Bab I.")

uploaded_file = st.file_uploader("📎 Upload file", type=["docx", "pdf"])

if uploaded_file:
    st.success("✅ File berhasil diunggah")
    text = extract_text(uploaded_file)
    bab1 = extract_bab1(text)

    if bab1 != "Bab I tidak ditemukan":
        with st.spinner("🤖 Sedang menganalisis isi Bab I..."):
            feedback = analyze_bab1(bab1)
            st.markdown("### 📝 Hasil Evaluasi:")
            st.text_area("Feedback AI", feedback, height=400)
    else:
        st.warning("⚠️ Bab I tidak ditemukan dalam dokumen.")