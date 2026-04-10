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
    df['M_Score'] = df['M_Score'].astype(str)
    return df

df = load_data()

# ==============================
# SIDEBAR DENGAN HIASAN
# ==============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ Menu Utama ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("🔍 **Pengaturan Filter**")
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect('Pilih M_Score Pelanggan:', options=m_score_list, default=m_score_list)
    
    st.markdown("---")
    st.info("💡 **Tips:** Filter ini akan merubah seluruh data di metrik dan grafik secara *real-time*.")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("🚀 *Data Analysis Project v2.0*")

df_filtered = df[df['M_Score'].isin(selected_score)]

# ==============================
# MAIN PAGE (TAMPILAN UTAMA)
# ==============================
# Judul dengan gaya lebih kece
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 E-Commerce Customer Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Memahami Perilaku Pelanggan melalui Segmentasi Moneter</p>", unsafe_allow_html=True)
st.markdown("---")

# KPI Metrics dengan hiasan kolom
st.subheader("📌 Ringkasan Data Saat Ini")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🏠 **Total Pelanggan**")
    st.title(f"{df_filtered.shape[0]}")
with col2:
    st.markdown("💰 **Rata-rata Belanja**")
    avg_mon = df_filtered.Monetary.mean()
    st.title(f"IDR {avg_mon:,.0f}")
with col3:
    st.markdown("🛒 **Total Transaksi**")
    st.title(f"{df_filtered.Frequency.sum():,}")

st.markdown("---")

# Visualisasi
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📈 Hubungan Frekuensi & Moneter")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    # Pakai warna palette 'magma' biar lebih 'nyala'
    sns.scatterplot(data=df_filtered, x='Frequency', y='Monetary', hue='M_Score', palette='magma', ax=ax1)
    st.pyplot(fig1)
    
    with st.expander("📝 Lihat Insight"):
        st.write("Grafik ini membantu kita mengidentifikasi pelanggan **High-Value**. Semakin gelap warnanya, semakin besar kontribusi ekonominya.")

with col_right:
    st.markdown("### 📊 Sebaran Skor Pelanggan")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.countplot(data=df_filtered, x='M_Score', palette='magma', ax=ax2)
    st.pyplot(fig2)

    with st.expander("📝 Lihat Insight"):
        st.write("Distribusi ini menunjukkan apakah basis pelanggan kita didominasi oleh pembelanja kecil (skor 1-2) atau pembelanja besar (skor 4-5).")

# Footer cantik
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>Created with ❤️ by <b>Alviyatur Rahmaniyah</b> | © 2026</div>", 
    unsafe_allow_html=True
)
