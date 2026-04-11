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
# FUNGSI LOAD DATA
# ==============================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        df = pd.read_csv('main_data.csv')
    
    # --- TAMBAHAN UNTUK FILTER TANGGAL ---
    # Pastikan kolom tanggal ada dan dikonversi ke datetime
    # Sesuaikan 'order_purchase_timestamp' dengan nama kolom tanggal di CSV-mu
    if 'order_purchase_timestamp' in df.columns:
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    df['M_Score'] = df['M_Score'].astype(str)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# ==============================
# SIDEBAR (FILTER INTERAKTIF)
# ==============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ Dashboard Menu ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- FILTER TANGGAL (RELEVAN LAINNYA) ---
    st.write("📅 **Filter Rentang Waktu**")
    if 'order_purchase_timestamp' in df.columns:
        min_date = df['order_purchase_timestamp'].min().date()
        max_date = df['order_purchase_timestamp'].max().date()

        start_date, end_date = st.date_input(
            label='Pilih Rentang Waktu:',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    else:
        st.warning("Kolom tanggal tidak ditemukan untuk filter waktu.")

    st.markdown("---")
    st.write("🔍 **Filter Pelanggan**")
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect(
        'Pilih Skor Moneter (1-5):', 
        options=m_score_list, 
        default=m_score_list
    )

# Logic Filter Data
if 'order_purchase_timestamp' in df.columns:
    df_filtered = df[
        (df['order_purchase_timestamp'].dt.date >= start_date) & 
        (df['order_purchase_timestamp'].dt.date <= end_date) &
        (df['M_Score'].isin(selected_score))
    ]
else:
    df_filtered = df[df['M_Score'].isin(selected_score)]

# ==============================
# MAIN PAGE
# ==============================
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 E-Commerce Customer Analysis</h1>", unsafe_allow_html=True)
st.markdown("---")

# KPI Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pelanggan", value=f"{df_filtered.shape[0]:,}")
with col2:
    avg_monetary = df_filtered['Monetary'].mean() if not df_filtered.empty else 0
    st.metric("Rata-rata Belanja", value=f"BRL {avg_monetary:,.2f}")
with col3:
    total_freq = df_filtered['Frequency'].sum() if not df_filtered.empty else 0
    st.metric("Total Transaksi", value=f"{total_freq:,}")

st.markdown("---")

# Visualisasi
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🎯 Hubungan Frekuensi vs Moneter")
    if not df_filtered.empty:
        fig1, ax1 = plt.subplots(figsize=(10, 7))
        sns.scatterplot(data=df_filtered, x='Frequency', y='Monetary', hue='M_Score', palette='viridis', s=100, ax=ax1)
        st.pyplot(fig1)
    else:
        st.warning("Data tidak tersedia untuk filter ini.")

with col_right:
    st.subheader("📊 Distribusi Skor Moneter")
    if not df_filtered.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        sns.countplot(data=df_filtered, x='M_Score', palette='viridis', order=m_score_list, ax=ax2)
        st.pyplot(fig2)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Alviyatur Rahmaniyah | Dicoding Project</div>", unsafe_allow_html=True)
