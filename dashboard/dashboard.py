import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(page_title="E-Commerce Customer Analytics", page_icon="🛍️", layout="wide")

# FUNGSI LOAD DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dashboard/main_data.csv')
    except:
        df = pd.read_csv('main_data.csv')
    
    # Pastikan M_Score jadi string untuk filter
    df['M_Score'] = df['M_Score'].astype(str)
    return df

df = load_data()

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ Menu Utama ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("🔍 **Filter Skor Moneter**")
    # Urutkan M_Score dari 1 ke 5
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect(
        'Pilih M_Score Pelanggan:', 
        options=m_score_list, 
        default=m_score_list
    )
    
    st.markdown("---")
    st.info("💡 Filter ini akan menyaring data pelanggan berdasarkan segmentasi skor moneter mereka.")

# Proses Filter Data (Hanya Berdasarkan M_Score agar Aman)
df_filtered = df[df['M_Score'].isin(selected_score)]

# ==============================
# MAIN PAGE
# ==============================
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 E-Commerce Customer Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Segmentasi Pelanggan Berdasarkan RFM (Monetary Fokus)</p>", unsafe_allow_html=True)
st.markdown("---")

# KPI Metrics
st.subheader("📌 Ringkasan Data Terfilter")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pelanggan", value=f"{df_filtered.shape[0]:,}")
with col2:
    avg_mon = df_filtered.Monetary.mean()
    st.metric("Rata-rata Belanja", value=f"BRL {avg_mon:,.2f}")
with col3:
    total_freq = df_filtered.Frequency.sum()
    st.metric("Total Transaksi", value=f"{total_freq:,}")

st.markdown("---")

# Visualisasi
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📈 Hubungan Frekuensi & Moneter")
    if not df_filtered.empty:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df_filtered, x='Frequency', y='Monetary', hue='M_Score', palette='magma', ax=ax1)
        st.pyplot(fig1)
    else:
        st.warning("Data kosong, silakan pilih M_Score di sidebar.")

with col_right:
    st.markdown("### 📊 Sebaran Skor Pelanggan (M_Score)")
    if not df_filtered.empty:
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.countplot(data=df_filtered, x='M_Score', palette='magma', order=m_score_list, ax=ax2)
        st.pyplot(fig2)
    else:
        st.warning("Data kosong.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>Created with ❤️ by <b>Alviyatur Rahmaniyah</b> | © 2026</div>", 
    unsafe_allow_html=True
)
