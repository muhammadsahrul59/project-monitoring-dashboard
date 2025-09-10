import streamlit as st
import pandas as pd
import numpy as np

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
    color: #00a39d; /* Warna biru */
    margin-top: 5px;
}

/* Styling untuk setiap kartu progress */
.progress-card {
    background-color: #f7f9fc;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    width: 100%; /* Lebar tetap untuk setiap kartu */
    height: 150px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin: 5px;
}

/* Styling untuk lingkaran persentase */
.progress-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
    border: 5px solid;
}

/* Styling untuk teks di dalam lingkaran */
.progress-text {
    position: absolute;
    font-size: 1.25rem;
    font-weight: 700;
}

/* Warna lingkaran berdasarkan persentase */
.circle-green { border-color: #28a745; background-color: #e2f0e6; color: #28a745; }
.circle-red { border-color: #dc3545; background-color: #f8e1e4; color: #dc3545; }
.circle-yellow { border-color: #ffc107; background-color: #fff6e4; color: #ffc107; }

.project-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #333;
    word-wrap: break-word; /* Memastikan teks tidak melebihi lebar kartu */
    white-space: normal;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Batasi hingga 2 baris */
    -webkit-box-orient: vertical;
}

/* Gaya untuk indikator perubahan persentase */
.change-indicator {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 5px;
}

.up { color: #28a745; }
.down { color: #dc3545; }
.same { color: #6c757d; }
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
st.markdown('<div class="title-centered">📊 Dashboard Monitoring Proyek</div>', unsafe_allow_html=True)
st.markdown("---")

# 4. PERHITUNGAN METRIK UNTUK KARTU
if df_summary is not None:
    # --- PERBAIKAN: MEMBERSihkan dan mengonversi kolom persentase ke float ---
    df_summary['persentase_this_week'] = df_summary['persentase_this_week'].astype(str).str.replace('%', '').str.strip().replace('', '0').astype(float)
    df_summary['persentase_last_week'] = df_summary['persentase_last_week'].astype(str).str.replace('%', '').str.strip().replace('', '0').astype(float)
    
    # Mengisi nilai NaN pada kolom persentase yang sudah bersih dengan 0
    df_summary.fillna({'persentase_this_week': 0, 'persentase_last_week': 0}, inplace=True)

    # Menghapus baris yang tidak memiliki nama proyek
    df_summary.dropna(subset=['name_project'], inplace=True)
    df_summary['pic'] = df_summary['pic'].astype(str)

    total_projects = df_summary['name_project'].nunique()
    syarief_count = df_summary['pic'].str.contains('Syarief', case=False, na=False).sum()
    nita_count = df_summary['pic'].str.contains('Nita', case=False, na=False).sum()
    nanin_count = df_summary['pic'].str.contains('Nanin', case=False, na=False).sum()
    sahrul_count = df_summary['pic'].str.contains('Sahrul', case=False, na=False).sum()
    akmal_count = df_summary['pic'].str.contains('Akmal', case=False, na=False).sum()

    def create_metric_card(label, value):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

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
    
    st.markdown("---")

    # 5. ROW 2: PROGRESS PROJECT
st.subheader("Progress Project")

# Membuat layout grid dengan 6 kolom untuk setiap baris
cols = st.columns(6)

if "selected_project" not in st.session_state:
    st.session_state.selected_project = None

for index, row in df_summary.iterrows():
    delta = row['persentase_this_week'] - row['persentase_last_week']
    delta_str, delta_class, icon = "", "same", "🟰"
    if delta > 0:
        delta_str, delta_class, icon = f"({delta:.0f}%)", "up", "🔺"
    elif delta < 0:
        delta_str, delta_class, icon = f"({abs(delta):.0f}%)", "down", "🔻"

    if row['persentase_this_week'] >= 80:
        circle_class = "circle-green"
    elif row['persentase_this_week'] >= 50:
        circle_class = "circle-yellow"
    else:
        circle_class = "circle-red"

    # Tombol klik project
    with cols[index % 6]:
        if st.button(
            f"{row['name_project']}",
            key=f"btn_{index}",
            help="Klik untuk lihat detail proyek"
        ):
            st.session_state.selected_project = row['name_project']

        st.markdown(f"""
        <div class="progress-card">
            <div class="progress-circle {circle_class}">
                {int(row['persentase_this_week'])}%
            </div>
            <div class="project-title">{row['name_project']}</div>
            <div class="change-indicator {delta_class}">
                {icon} {delta_str}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 6. ROW 3: PROJECT DETAIL
if st.session_state.selected_project and df_detail is not None:
    selected_project = st.session_state.selected_project
    st.subheader(f"Project Detail: {selected_project}")

    df_project = df_detail[df_detail['name_project'] == selected_project]

    for _, detail in df_project.iterrows():
        with st.expander(f"📌 {detail['activity']}"):
            st.write(f"**Start Date:** {detail['start_date']}")
            st.write(f"**Due Date:** {detail['due_date']}")
            st.write(f"**Hari:** {detail['total_hari']}")
            st.write(f"**Progress Minggu Ini:** {detail['progress_this_week']}%")
            st.write(f"**Status:** {detail['status']}")

            # Jika ada detail activity
            if pd.notna(detail.get("detail_activity1")) and detail["detail_activity1"] != "":
                st.markdown(f"- {detail['detail_activity1']}")
            if pd.notna(detail.get("detail_activity2")) and detail["detail_activity2"] != "":
                st.markdown(f"- {detail['detail_activity2']}")
            if pd.notna(detail.get("detail_activity3")) and detail["detail_activity3"] != "":
                st.markdown(f"- {detail['detail_activity3']}")


# 6. TAMPILKAN TABEL DATA
st.header("Tabel Data Proyek")
st.dataframe(df_summary)

