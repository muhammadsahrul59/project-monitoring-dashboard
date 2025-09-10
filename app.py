import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- STYLING KHUSUS UNTUK DASHBOARD ---
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
    color: #00a39d; /* Warna biru gelap */
    margin-bottom: 2rem;
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
    """
    Loads data from a CSV file.
    """
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
st.markdown('<div class="title-centered">📊 Dashboard Monitoring Proyek</div>', unsafe_allow_html=True)
st.markdown("---")

# 4. PERHITUNGAN METRIK UNTUK KARTU (Menggunakan st.metric yang lebih bersih)
if df_summary is not None:
    # --- PERBAIKAN: membersihkan dan mengonversi kolom persentase ke float ---
    df_summary['persentase_this_week'] = df_summary['persentase_this_week'].astype(str).str.replace('%', '').str.strip().replace('', '0').astype(float)
    df_summary['persentase_last_week'] = df_summary['persentase_last_week'].astype(str).str.replace('%', '').str.strip().replace('', '0').astype(float)
    
    # Mengisi nilai NaN pada kolom persentase yang sudah bersih dengan 0
    df_summary.fillna({'persentase_this_week': 0, 'persentase_last_week': 0}, inplace=True)

    # Menghapus baris yang tidak memiliki nama proyek
    df_summary.dropna(subset=['name_project'], inplace=True)
    df_summary['pic'] = df_summary['pic'].astype(str)

    total_projects = df_summary['name_project'].nunique()
    pic_counts = df_summary['pic'].str.lower().value_counts()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("🚀 Total Projects", total_projects)

    with col2:
        st.metric("👨‍💻 Syarief", pic_counts.get('syarief', 0))

    with col3:
        st.metric("👩‍💻 Nita", pic_counts.get('nita', 0))

    with col4:
        st.metric("👩‍💻 Nanin", pic_counts.get('nanin', 0))
    
    with col5:
        st.metric("👨‍💻 Sahrul", pic_counts.get('sahrul', 0))

    with col6:
        st.metric("👨‍💻 Akmal", pic_counts.get('akmal', 0))
    
    st.markdown("---")

    # 5. ROW 2: PROGRESS PROJECT (Menggunakan Plotly Gauge Charts)
    st.subheader("Progress Project")

    # Membuat layout grid dengan 6 kolom
    cols = st.columns(6)
    
    # Menampilkan gauge chart untuk setiap proyek
    for index, row in df_summary.iterrows():
        # Menghitung selisih persentase
        delta = row['persentase_this_week'] - row['persentase_last_week']
        delta_str = f" from {row['persentase_last_week']:.0f}%"

        # Menentukan warna berdasarkan persentase
        if row['persentase_this_week'] >= 80:
            range_color = 'green'
        elif row['persentase_this_week'] >= 50:
            range_color = 'gold'
        else:
            range_color = 'red'

        # Membuat objek Plotly Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=row['persentase_this_week'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"**{row['name_project']}**", 'font': {'size': 16}},
            delta={'reference': row['persentase_last_week'], 'position': "bottom", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#00a39d"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 49], 'color': 'lightcoral'},
                    {'range': [50, 79], 'color': 'khaki'},
                    {'range': [80, 100], 'color': 'lightgreen'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))

        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="lavender",
            font={'color': "darkblue", 'family': "Arial"}
        )

        # Menampilkan chart di kolom yang sesuai
        with cols[index % 6]:
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

# 6. TAMPILKAN TABEL DATA
st.header("Tabel Data Proyek")
if df_summary is not None:
    st.dataframe(df_summary)
