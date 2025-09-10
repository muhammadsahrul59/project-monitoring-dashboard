import streamlit as st
import pandas as pd

# --- STYLING KHUSUS UNTUK DASHBOARD ---
# Menggunakan HTML dan CSS untuk menata tampilan.
# st.markdown dengan unsafe_allow_html=True memungkinkan kita menyisipkan kode HTML/CSS.
st.markdown("""
<style>
/* Mengatur font untuk seluruh aplikasi */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Mengatur judul utama di tengah halaman */
.title-centered {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: #0d47a1; /* Warna biru gelap */
    margin-bottom: 2rem;
}

/* Mengatur kotak (card) untuk metrik */
.metric-card {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center; /* Menengahkan teks di dalam kotak */
}

/* Gaya untuk label metrik */
.metric-label {
    font-size: 1rem;
    color: #4b5563; /* Warna abu-abu */
    font-weight: 600;
}

/* Gaya untuk nilai metrik */
.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1e40af; /* Warna biru */
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Project Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. FUNGSI UNTUK MEMUAT DATA
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=';')
        return df
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {filepath}. Pastikan file ada di folder yang sama.")
        return None

# Memuat kedua dataset
df_detail = load_data('dataset.csv')
df_summary = load_data('dataset2.csv')

# 3. JUDUL UTAMA DASHBOARD
# Menggunakan CSS class 'title-centered' untuk menengahkan judul
st.markdown('<div class="title-centered">📊 Dashboard Monitoring Proyek</div>', unsafe_allow_html=True)
st.markdown("---") # Garis pemisah

# 4. PERHITUNGAN METRIK UNTUK KARTU
if df_summary is not None:
    df_summary.dropna(subset=['name_project'], inplace=True)
    df_summary['pic'] = df_summary['pic'].astype(str)

    total_projects = df_summary['name_project'].nunique()

    syarief_count = df_summary['pic'].str.contains('Syarief', case=False, na=False).sum()
    nita_count = df_summary['pic'].str.contains('Nita', case=False, na=False).sum()
    nanin_count = df_summary['pic'].str.contains('Nanin', case=False, na=False).sum()
    sahrul_count = df_summary['pic'].str.contains('Sahrul', case=False, na=False).sum()
    akmal_count = df_summary['pic'].str.contains('Akmal', case=False, na=False).sum()

    # Fungsi untuk membuat dan menampilkan kartu metrik dengan styling
    def create_metric_card(label, value):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    # 5. TAMPILKAN KARTU METRIK DI TENGAH
    # Menggunakan 6 kolom untuk menampung kartu secara rata
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        create_metric_card("🚀 Total Projects", total_projects)

    with col2:
        create_metric_card("👨‍💻 Syarief", syarief_count)

    with col3:
        create_metric_card("👩‍💻 Nita", nita_count)

    with col4:
        create_metric_card("👩‍💻 Nanin", nanin_count)
    
    with col5:
        create_metric_card("👨‍💻 Sahrul", sahrul_count)

    with col6:
        create_metric_card("👨‍💻 Akmal", akmal_count)
    
    st.markdown("---") # Garis pemisah

# 6. TAMPILKAN TABEL DATA
st.header("Tabel Data Proyek")
st.dataframe(df_summary)
