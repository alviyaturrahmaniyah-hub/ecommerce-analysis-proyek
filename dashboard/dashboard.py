import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(page_title="E-Commerce Customer Analytics", layout="wide")

# ==============================
# FUNGSI LOAD DATA (VERSI FIX CSV)
# ==============================
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), 'main_data.csv')
    if not os.path.exists(path):
        path = 'main_data.csv'
        
    try:
        # Gunakan sep=None dan engine='python' untuk deteksi pemisah otomatis
        df = pd.read_csv(path, sep=None, engine='python')
        
        # Bersihkan nama kolom kalau ada spasi tersembunyi
        df.columns = df.columns.str.strip()
        
        # Pastikan skor jadi string untuk filter
        for col in ['R_Score', 'F_Score', 'M_Score']:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("⚠️ Data gagal dimuat atau kosong. Pastikan file 'main_data.csv' sudah benar!")
    st.stop()

# ==============================
# SIDEBAR (FILTER INTERAKTIF)
# ==============================
with st.sidebar:
    st.title("✨ Menu Filter ✨")
    st.info("Gunakan filter di bawah untuk eksplorasi data secara dinamis.")
    
    # Filter 1: R_Score (Relevansi Waktu)
    st.write("📅 **Filter Kedekatan Waktu (Recency)**")
    r_list = sorted(df['R_Score'].unique())
    selected_r = st.multiselect('Pilih R_Score (5=Baru, 1=Lama):', r_list, default=r_list)
    
    # Filter 2: M_Score (Relevansi Ekonomi)
    st.write("💰 **Filter Nilai Moneter**")
    m_list = sorted(df['M_Score'].unique())
    selected_m = st.multiselect('Pilih M_Score (5=Tinggi, 1=Rendah):', m_list, default=m_list)

# Proses Filter
df_filtered = df[df['R_Score'].isin(selected_r) & df['M_Score'].isin(selected_m)]

# ==============================
# TAMPILAN UTAMA
# ==============================
st.title("📊 E-Commerce Customer RFM Analytics")
st.markdown("---")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pelanggan", f"{len(df_filtered):,}")
with col2:
    val = df_filtered['Monetary'].mean() if not df_filtered.empty else 0
    st.metric("Rata-rata Monetary", f"BRL {val:,.2f}")
with col3:
    val = df_filtered['Frequency'].sum() if not df_filtered.empty else 0
    st.metric("Total Transaksi", f"{val:,}")

st.markdown("---")

# Visualisasi
c1, c2 = st.columns(2)
with c1:
    st.subheader("🎯 Hubungan Frequency & Monetary")
    if not df_filtered.empty:
        fig, ax = plt.subplots()
        sns.scatterplot(data=df_filtered, x='Frequency', y='Monetary', hue='M_Score', ax=ax)
        st.pyplot(fig)

with c2:
    st.subheader("📊 Distribusi Pelanggan")
    if not df_filtered.empty:
        fig, ax = plt.subplots()
        sns.countplot(data=df_filtered, x='M_Score', palette='magma', ax=ax)
        st.pyplot(fig)

st.write("👈 *Gunakan sidebar untuk memfilter data dan melihat perubahan secara dinamis.*")
