import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(page_title="E-Commerce Customer Analytics", page_icon="📊", layout="wide")

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

# SIDEBAR
with st.sidebar:
    st.title("💡 Filter Data")
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect('Pilih M_Score:', options=m_score_list, default=m_score_list)
    st.info("Gunakan filter ini untuk melihat data berdasarkan kelompok skor pengeluaran pelanggan.")

df_filtered = df[df['M_Score'].isin(selected_score)]

# MAIN PAGE
st.title('E-Commerce Customer Analytics Dashboard 📊')
st.markdown("---")

# KPI Metrics (Angka Utama)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pelanggan", value=df_filtered.shape[0])
with col2:
    avg_mon = df_filtered.Monetary.mean()
    st.metric("Rata-rata Pengeluaran", value=f"IDR {avg_mon:,.0f}")
with col3:
    st.metric("Total Transaksi", value=f"{df_filtered.Frequency.sum():,}")

st.markdown("---")

# Visualisasi
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Frekuensi vs Moneter")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(data=df_filtered, x='Frequency', y='Monetary', hue='M_Score', palette='rocket', ax=ax1)
    st.pyplot(fig1)
    
    # PENJELASAN GAMBAR 1
    with st.expander("Klik untuk melihat penjelasan grafik 1"):
        st.write("""
            **Maksud Gambar:** Grafik ini menunjukkan hubungan antara seberapa sering pelanggan belanja (*Frequency*) 
            dengan total uang yang dihabiskan (*Monetary*). 
            
            **Insight:** Semakin ke kanan dan ke atas posisi titik, berarti pelanggan tersebut semakin loyal dan royal. 
            Pelanggan dengan **M_Score tinggi** (warna gelap) adalah target utama untuk program loyalitas.
        """)

with col_right:
    st.subheader("2. Distribusi Skor Moneter")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df_filtered, x='M_Score', palette='rocket', ax=ax2)
    st.pyplot(fig2)

    # PENJELASAN GAMBAR 2
    with st.expander("Klik untuk melihat penjelasan grafik 2"):
        st.write("""
            **Maksud Gambar:** Grafik ini menunjukkan jumlah pelanggan di setiap kategori skor moneter (1-5).
            
            **Insight:** Kita bisa melihat segmentasi pelanggan kita paling banyak menumpuk di mana. 
            Jika banyak yang di skor rendah, berarti kita butuh strategi promo untuk meningkatkan nilai belanja mereka.
        """)

st.markdown("---")
st.caption('Copyright (c) Alviyatur Rahmaniyah 2026')
