import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- STYLING KHUSUS UNTUK DASHBOARD ---
st.markdown("""
<style>
/* Mengatur font untuk seluruh aplikasi */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f8fafc;
}

/* Mengatur judul utama di tengah halaman */
.title-centered {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Mengatur kotak (card) untuk metrik */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 24px;
    margin: 8px 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

/* Gaya untuk label metrik */
.metric-label {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

/* Gaya untuk nilai metrik */
.metric-value {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 5px;
}

/* Styling untuk setiap kartu progress */
.progress-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    width: 100%;
    height: 180px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.progress-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
}

/* Styling untuk oval persentase - BENTUK LONJONG */
.progress-oval {
    width: 100px;
    height: 65px; /* Lebih kecil dari width untuk bentuk lonjong */
    border-radius: 50px 50px 50px 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    font-weight: 800;
    color: white;
    margin-bottom: 12px;
    border: 4px solid;
    position: relative;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    transition: all 0.3s ease;
}

.progress-card:hover .progress-oval {
    transform: scale(1.1);
}

/* Warna oval berdasarkan persentase */
.oval-excellent { 
    border-color: #10b981; 
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
}
.oval-good { 
    border-color: #3b82f6; 
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
}
.oval-warning { 
    border-color: #f59e0b; 
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
}
.oval-danger { 
    border-color: #ef4444; 
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
}

.project-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #1e293b;
    word-wrap: break-word;
    white-space: normal;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-height: 1.4;
    margin-bottom: 8px;
}

/* Gaya untuk indikator perubahan persentase */
.change-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 8px;
    padding: 4px 8px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.up { 
    color: #059669; 
    background-color: rgba(16, 185, 129, 0.1);
}
.down { 
    color: #dc2626; 
    background-color: rgba(239, 68, 68, 0.1);
}
.same { 
    color: #6b7280; 
    background-color: rgba(107, 114, 128, 0.1);
}

/* Section headers */
.section-header {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1e293b;
    margin: 2rem 0 1rem 0;
    text-align: center;
    position: relative;
}

.section-header::after {
    content: '';
    display: block;
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    margin: 12px auto 0;
    border-radius: 2px;
}

/* Filter section styling */
.filter-container {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 20px;
    border-radius: 16px;
    margin: 20px 0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Data table styling improvements */
.dataframe {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08) !important;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8, #6a42a0);
}

/* Animation for cards */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.progress-card, .metric-card {
    animation: fadeInUp 0.6s ease-out;
}
</style>
""", unsafe_allow_html=True)

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Project Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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

# 3. SIDEBAR - FILTER DAN KONTROL
st.sidebar.markdown("### 🎛️ Dashboard Controls")

# Filter berdasarkan PIC
if df_summary is not None:
    df_summary['pic'] = df_summary['pic'].astype(str)
    pic_options = ['All'] + sorted(df_summary['pic'].unique())
    selected_pic = st.sidebar.selectbox("Filter by PIC:", pic_options)
    
    # Filter berdasarkan progress range
    progress_range = st.sidebar.slider(
        "Progress Range (%)", 
        min_value=0, 
        max_value=100, 
        value=(0, 100),
        step=5
    )
    
    # Sorting options
    sort_by = st.sidebar.selectbox(
        "Sort by:",
        ["Project Name", "Progress (High to Low)", "Progress (Low to High)", "Recent Changes"]
    )

# 4. JUDUL UTAMA DASHBOARD
st.markdown('<div class="title-centered">📊 Project Monitoring Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# 5. PERHITUNGAN METRIK UNTUK KARTU
if df_summary is not None:
    # --- PERBAIKAN: Membersihkan dan mengonversi kolom persentase ke float ---
    df_summary['persentase_this_week'] = df_summary['persentase_this_week'].astype(str).str.replace('%', '').str.strip().replace('', '0').astype(float)
    df_summary['persentase_last_week'] = df_summary['persentase_last_week'].astype(str).str.replace('%', '').str.strip().replace('', '0').astype(float)
    
    # Mengisi nilai NaN pada kolom persentase yang sudah bersih dengan 0
    df_summary.fillna({'persentase_this_week': 0, 'persentase_last_week': 0}, inplace=True)

    # Menghapus baris yang tidak memiliki nama proyek
    df_summary.dropna(subset=['name_project'], inplace=True)
    
    # Apply filters
    filtered_df = df_summary.copy()
    
    if selected_pic != 'All':
        filtered_df = filtered_df[filtered_df['pic'].str.contains(selected_pic, case=False, na=False)]
    
    filtered_df = filtered_df[
        (filtered_df['persentase_this_week'] >= progress_range[0]) & 
        (filtered_df['persentase_this_week'] <= progress_range[1])
    ]
    
    # Apply sorting
    if sort_by == "Progress (High to Low)":
        filtered_df = filtered_df.sort_values('persentase_this_week', ascending=False)
    elif sort_by == "Progress (Low to High)":
        filtered_df = filtered_df.sort_values('persentase_this_week', ascending=True)
    elif sort_by == "Recent Changes":
        filtered_df['change'] = filtered_df['persentase_this_week'] - filtered_df['persentase_last_week']
        filtered_df = filtered_df.sort_values('change', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('name_project')

    # Hitung metrik
    total_projects = df_summary['name_project'].nunique()
    syarief_count = df_summary['pic'].str.contains('Syarief', case=False, na=False).sum()
    nita_count = df_summary['pic'].str.contains('Nita', case=False, na=False).sum()
    nanin_count = df_summary['pic'].str.contains('Nanin', case=False, na=False).sum()
    sahrul_count = df_summary['pic'].str.contains('Sahrul', case=False, na=False).sum()
    akmal_count = df_summary['pic'].str.contains('Akmal', case=False, na=False).sum()
    
    # Calculate additional metrics
    avg_progress = df_summary['persentase_this_week'].mean()
    completed_projects = len(df_summary[df_summary['persentase_this_week'] >= 100])
    at_risk_projects = len(df_summary[df_summary['persentase_this_week'] < 50])

    def create_metric_card(label, value, is_percentage=False):
        display_value = f"{value:.1f}%" if is_percentage else str(value)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{display_value}</div>
        </div>
        """, unsafe_allow_html=True)

    # First row of metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_metric_card("🚀 Total Projects", total_projects)

    with col2:
        create_metric_card("📈 Avg Progress", avg_progress, is_percentage=True)

    with col3:
        create_metric_card("✅ Completed", completed_projects)

    with col4:
        create_metric_card("⚠️ At Risk", at_risk_projects)
    
    # Second row of metrics - PIC breakdown
    col5, col6, col7, col8, col9 = st.columns(5)

    with col5:
        create_metric_card("👨‍💻 Syarief", syarief_count)

    with col6:
        create_metric_card("👩‍💻 Nita", nita_count)

    with col7:
        create_metric_card("👩‍💻 Nanin", nanin_count)
    
    with col8:
        create_metric_card("👨‍💻 Sahrul", sahrul_count)

    with col9:
        create_metric_card("👨‍💻 Akmal", akmal_count)
    
    st.markdown("---")

    # 6. CHARTS SECTION
    st.markdown('<div class="section-header">📊 Analytics Overview</div>', unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("📈 Progress Distribution")
        # Progress distribution using Streamlit built-in charts
        progress_bins = ['0-25%', '26-50%', '51-75%', '76-99%', '100%']
        progress_counts = [
            len(df_summary[(df_summary['persentase_this_week'] >= 0) & (df_summary['persentase_this_week'] <= 25)]),
            len(df_summary[(df_summary['persentase_this_week'] >= 26) & (df_summary['persentase_this_week'] <= 50)]),
            len(df_summary[(df_summary['persentase_this_week'] >= 51) & (df_summary['persentase_this_week'] <= 75)]),
            len(df_summary[(df_summary['persentase_this_week'] >= 76) & (df_summary['persentase_this_week'] <= 99)]),
            len(df_summary[df_summary['persentase_this_week'] >= 100])
        ]
        
        progress_df = pd.DataFrame({
            'Progress Range': progress_bins,
            'Count': progress_counts
        })
        
        st.bar_chart(progress_df.set_index('Progress Range'))
        
        # Show progress summary in cards
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("🔴 Critical (0-25%)", progress_counts[0])
        with col_b:
            st.metric("🟡 At Risk (26-50%)", progress_counts[1])
        with col_c:
            st.metric("🟢 Good (51%+)", sum(progress_counts[2:]))
    
    with chart_col2:
        st.subheader("👥 Projects per PIC")
        # PIC workload bar chart using Streamlit
        pic_data = pd.DataFrame({
            'PIC': ['Syarief', 'Nita', 'Nanin', 'Sahrul', 'Akmal'],
            'Projects': [syarief_count, nita_count, nanin_count, sahrul_count, akmal_count]
        })
        
        st.bar_chart(pic_data.set_index('PIC'))
        
        # Show top performers
        pic_data_sorted = pic_data.sort_values('Projects', ascending=False)
        st.info(f"🏆 Most Active: {pic_data_sorted.iloc[0]['PIC']} ({pic_data_sorted.iloc[0]['Projects']} projects)")
        
        # Average workload
        avg_workload = pic_data['Projects'].mean()
        st.info(f"📊 Average Workload: {avg_workload:.1f} projects per PIC")

    st.markdown("---")

    # 7. ROW: PROGRESS PROJECT (dengan bentuk oval)
    st.markdown('<div class="section-header">🎯 Project Progress</div>', unsafe_allow_html=True)
    
    # Show number of filtered results
    st.info(f"Showing {len(filtered_df)} of {len(df_summary)} projects")

    # Membuat layout grid dengan 6 kolom untuk setiap baris
    cols = st.columns(6)

    for index, row in filtered_df.iterrows():
        # Menghitung selisih persentase
        delta = row['persentase_this_week'] - row['persentase_last_week']
        delta_str = ""
        delta_class = "same"
        icon = ""

        if delta > 0:
            delta_str = f"↗ {delta:.0f}%"
            delta_class = "up"
        elif delta < 0:
            delta_str = f"↘ {abs(delta):.0f}%"
            delta_class = "down"
        else:
            delta_str = "→ 0%"
            delta_class = "same"

        # Menentukan warna oval berdasarkan persentase dengan lebih banyak kategori
        oval_class = ""
        if row['persentase_this_week'] >= 90:
            oval_class = "oval-excellent"
        elif row['persentase_this_week'] >= 70:
            oval_class = "oval-good"
        elif row['persentase_this_week'] >= 40:
            oval_class = "oval-warning"
        else:
            oval_class = "oval-danger"

        # Menampilkan kartu di kolom yang sesuai
        with cols[index % 6]:
            st.markdown(f"""
            <div class="progress-card">
                <div class="progress-oval {oval_class}">
                    {int(row['persentase_this_week'])}%
                </div>
                <div class="project-title">{row['name_project']}</div>
                <div class="change-indicator {delta_class}">
                    {delta_str}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")

# 8. TAMPILKAN TABEL DATA
st.markdown('<div class="section-header">📋 Detailed Project Data</div>', unsafe_allow_html=True)

if df_summary is not None:
    # Add some additional calculated columns for the table
    display_df = filtered_df.copy()
    display_df['Progress Change'] = display_df['persentase_this_week'] - display_df['persentase_last_week']
    display_df['Status'] = display_df['persentase_this_week'].apply(
        lambda x: '✅ Complete' if x >= 100 
                 else '🟢 On Track' if x >= 70
                 else '🟡 At Risk' if x >= 40
                 else '🔴 Critical'
    )
    
    # Format the dataframe for better display
    display_df = display_df[['name_project', 'pic', 'persentase_this_week', 'persentase_last_week', 'Progress Change', 'Status']]
    display_df.columns = ['Project Name', 'PIC', 'Current Progress (%)', 'Last Week (%)', 'Change (%)', 'Status']
    
    st.dataframe(
        display_df, 
        use_container_width=True,
        hide_index=True
    )

    # Download button for filtered data
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="project_monitoring_filtered.csv",
        mime="text/csv"
    )

# 9. FOOTER
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748b; padding: 20px;'>
        <p>📊 Project Monitoring Dashboard | Made with ❤️ using Streamlit</p>
        <p><em>Last updated: Real-time data</em></p>
    </div>
    """, 
    unsafe_allow_html=True
)
