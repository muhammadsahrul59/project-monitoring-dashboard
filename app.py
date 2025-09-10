import streamlit as st
import pandas as pd

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
        st.error(f"File tidak ditemukan: {filepath}. Pastikan file CSV sudah diupload.")
        return None
    except Exception as e:
        st.error(f"Error membaca file: {str(e)}")
        return None

# 3. UPLOAD FILE CSV
st.title("📊 Dashboard Monitoring Proyek")
st.markdown("### Upload File CSV Anda")

# File uploader untuk kedua dataset
uploaded_file1 = st.file_uploader("Upload dataset.csv", type=['csv'], key="dataset1")
uploaded_file2 = st.file_uploader("Upload dataset2.csv", type=['csv'], key="dataset2")

# Memuat data dari file yang diupload
df_detail = None
df_summary = None

if uploaded_file1 is not None:
    try:
        df_detail = pd.read_csv(uploaded_file1, sep=';')
        st.success("✅ dataset.csv berhasil diupload!")
    except Exception as e:
        st.error(f"Error membaca dataset.csv: {str(e)}")

if uploaded_file2 is not None:
    try:
        df_summary = pd.read_csv(uploaded_file2, sep=';')
        st.success("✅ dataset2.csv berhasil diupload!")
    except Exception as e:
        st.error(f"Error membaca dataset2.csv: {str(e)}")

st.markdown("---")

# 4. PERHITUNGAN METRIK (hanya jika data tersedia)
if df_summary is not None:
    # Pastikan data bersih
    df_summary.dropna(subset=['name_project'], inplace=True)
    df_summary['pic'] = df_summary['pic'].astype(str)

    # METRIK 1: Total Project
    total_projects = df_summary['name_project'].nunique()

    # METRIK 2-6: Menghitung jumlah proyek per PIC
    syarief_count = df_summary['pic'].str.contains('Syarief', case=False, na=False).sum()
    nita_count = df_summary['pic'].str.contains('Nita', case=False, na=False).sum()
    nanin_count = df_summary['pic'].str.contains('Nanin', case=False, na=False).sum()
    sahrul_count = df_summary['pic'].str.contains('Sahrul', case=False, na=False).sum()
    akmal_count = df_summary['pic'].str.contains('Akmal', case=False, na=False).sum()

    # 5. TAMPILKAN METRIK
    st.subheader("📈 Ringkasan Proyek Tim")

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
    
    st.markdown("---")

    # 6. TAMPILKAN TABEL DATA
    st.subheader("📋 Tabel Data Proyek")
    
    # Tambahkan filter dan pencarian
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        if 'pic' in df_summary.columns:
            pic_options = ['Semua'] + list(df_summary['pic'].unique())
            selected_pic = st.selectbox("Filter berdasarkan PIC:", pic_options)
    
    with col_filter2:
        search_term = st.text_input("Cari nama proyek:")
    
    # Apply filters
    filtered_df = df_summary.copy()
    
    if selected_pic != 'Semua':
        filtered_df = filtered_df[filtered_df['pic'] == selected_pic]
    
    if search_term:
        filtered_df = filtered_df[filtered_df['name_project'].str.contains(search_term, case=False, na=False)]
    
    # Tampilkan dataframe dengan paging
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Informasi tambahan
    st.info(f"Menampilkan {len(filtered_df)} dari {len(df_summary)} proyek total")
    
    # Opsi download hasil filter
    if len(filtered_df) > 0:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data Terfilter (CSV)",
            data=csv,
            file_name="filtered_projects.csv",
            mime="text/csv"
        )

else:
    st.warning("⚠️ File dataset2.csv tidak ditemukan di repository. Pastikan file sudah diupload ke GitHub.")

# 7. TAMPILKAN DATA DETAIL JIKA ADA
if df_detail is not None:
    st.markdown("---")
    st.subheader("📊 Data Detail")
    st.dataframe(df_detail, use_container_width=True, height=300)

# Footer
st.markdown("---")
st.markdown("**Dashboard Monitoring Proyek** | Dibuat dengan ❤️ menggunakan Streamlit")