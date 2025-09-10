import streamlit as st
import pandas as pd

# 1. KONFIGURASI HALAMAN
# Mengatur tampilan dasar halaman web, seperti judul di tab browser dan layout.
st.set_page_config(
    page_title="Project Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. FUNGSI UNTUK MEMUAT DATA
# Fungsi ini akan membaca file CSV. @st.cache_data memastikan data hanya dibaca sekali
# dan disimpan di cache, sehingga aplikasi berjalan lebih cepat.
@st.cache_data
def load_data(filepath):
    try:
        # Kita gunakan separator ';' sesuai format file CSV Anda
        df = pd.read_csv(filepath, sep=';')
        return df
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {filepath}. Pastikan file ada di folder yang sama.")
        return None

# Memuat kedua dataset
df_detail = load_data('dataset.csv')
df_summary = load_data('dataset2.csv')


# 3. JUDUL UTAMA DASHBOARD
st.title("📊 Dashboard Monitoring Proyek")
st.markdown("---") # Garis pemisah

# 4. PERHITUNGAN METRIK UNTUK ROW 1
if df_summary is not None:
    # Menghapus baris yang tidak memiliki nama proyek (jika ada)
    df_summary.dropna(subset=['name_project'], inplace=True)
    df_summary['pic'] = df_summary['pic'].astype(str) # Pastikan kolom PIC adalah string

    # METRIK 1: Total Project
    total_projects = df_summary['name_project'].nunique()

    # METRIK 2-6: Menghitung jumlah proyek per PIC
    # Kita menggunakan .str.contains() untuk mencari nama di dalam kolom 'pic'.
    # `case=False` agar tidak membedakan huruf besar/kecil (misal: 'Nita' dan 'nita' sama).
    # `na=False` agar baris kosong (NaN) di kolom PIC tidak menyebabkan error.
    syarief_count = df_summary['pic'].str.contains('Syarief', case=False, na=False).sum()
    nita_count = df_summary['pic'].str.contains('Nita', case=False, na=False).sum()
    nanin_count = df_summary['pic'].str.contains('Nanin', case=False, na=False).sum()
    sahrul_count = df_summary['pic'].str.contains('Sahrul', case=False, na=False).sum()
    akmal_count = df_summary['pic'].str.contains('Akmal', case=False, na=False).sum()

    # 5. TAMPILKAN ROW 1 DENGAN METRIK
    st.subheader("Ringkasan Proyek Tim")

    # Membuat 6 kolom untuk menampung kotak-kotak metrik
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(label="🚀 Total Projects", value=total_projects)

    with col2:
        st.metric(label="👨‍💻 Syarief", value=syarief_count)

    with col3:
        st.metric(label="👩‍💻 Nita", value=nita_count)

    with col4:
        st.metric(label="👩‍💻 Nanin", value=nanin_count)
    
    with col5:
        st.metric(label="👨‍💻 Sahrul", value=sahrul_count)

    with col6:
        st.metric(label="👨‍💻 Akmal", value=akmal_count)
    
    st.markdown("---") # Garis pemisah

# (Tempat untuk kode row 2 Anda nanti)
st.header("Tabel Data Proyek")
st.dataframe(df_summary)
