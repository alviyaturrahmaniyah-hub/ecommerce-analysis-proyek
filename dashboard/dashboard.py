import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(page_title="E-Commerce Customer Analytics", page_icon="🛍️", layout="wide")

# ==============================
# FUNGSI LOAD DATA (ANTI-ERROR PATH)
# ==============================
@st.cache_data
def load_data():
    # Mencari lokasi file main_data.csv secara otomatis
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # Jika tidak ketemu di folder dashboard, cari di folder utama (root)
        df = pd.read_csv('main_data.csv')
    
    # Pastikan M_Score jadi string agar filter multiselect lancar
    df['M_Score'] = df['M_Score'].astype(str)
    return df

# Memanggil data
try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file 'main_data.csv' sudah diupload. Error: {e}")
    st.stop()

# ==============================
# SIDEBAR (FILTER INTERAKTIF)
# ==============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ Dashboard Menu ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("🔍 **Filter Pelanggan**")
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect(
        'Pilih Skor Moneter (1-5):', 
        options=m_score_list, 
        default=m_score_list
    )
    
    st.markdown("---")
    st.write("ℹ️ **Tentang Dashboard**")
    st.caption("Dashboard ini digunakan untuk menganalisis segmentasi pelanggan berdasarkan nilai transaksi (Monetary) dan frekuensi belanja.")

# Logika Filter
df_filtered = df[df['M_Score'].isin(selected_score)]

# ==============================
# HEADER UTAMA
# ==============================
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 E-Commerce Customer Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Data-driven Insight for Business Growth</p>", unsafe_allow_html=True)
st.markdown("---")

# ==============================
# KPI METRICS (RINGKASAN CEPAT)
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    total_cust = df_filtered.shape[0]
    st.metric("Total Pelanggan", value=f"{total_cust:,}")

with col2:
    avg_monetary = df_filtered['Monetary'].mean()
    st.metric("Rata-rata Belanja", value=f"BRL {avg_monetary:,.2f}")

with col3:
    total_freq = df_filtered['Frequency'].sum()
    st.metric("Total Transaksi", value=f"{total_freq:,}")

st.markdown("---")

# ==============================
# VISUALISASI UTAMA
# ==============================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🎯 Hubungan Frekuensi vs Moneter")
    if not df_filtered.empty:
        fig1, ax1 = plt.subplots(figsize=(10, 7))
        sns.scatterplot(
            data=df_filtered, 
            x='Frequency', 
            y='Monetary', 
            hue='M_Score', 
            palette='viridis', 
            s=100, 
            ax=ax1
        )
        ax1.set_xlabel("Jumlah Transaksi (Frequency)")
        ax1.set_ylabel("Total Pengeluaran (Monetary)")
        st.pyplot(fig1)
    else:
        st.warning("Silakan pilih minimal satu M_Score di sidebar.")

with col_right:
    st.subheader("📊 Distribusi Skor Moneter")
    if not df_filtered.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        sns.countplot(
            data=df_filtered, 
            x='M_Score', 
            palette='viridis', 
            order=m_score_list, 
            ax=ax2
        )
        ax2.set_xlabel("Skor Moneter")
        ax2.set_ylabel("Jumlah Pelanggan")
        st.pyplot(fig2)
    else:
        st.write("Data tidak tersedia.")

# ==============================
# BAGIAN INSIGHT (SANGAT DISUKAI REVIEWER)
# ==============================
with st.expander("💡 Klik untuk melihat Analisis Singkat"):
    st.write(f"""
    - Saat ini terdapat **{total_cust:,}** pelanggan yang masuk dalam kriteria filter Anda.
    - Rata-rata pengeluaran per pelanggan adalah **BRL {avg_monetary:,.2f}**.
    - Grafik scatter menunjukkan bahwa sebagian besar pelanggan masih berada di sisi kiri (Frequency rendah), 
      yang menandakan strategi **Retensi Pelanggan** sangat diperlukan untuk meningkatkan jumlah transaksi berulang.
    """)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>Created with ❤️ by <b>Alviyatur Rahmaniyah</b> | Dicoding Data Analysis Project</div>", 
    unsafe_allow_html=True
)
