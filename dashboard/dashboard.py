import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menghilangkan padding default Streamlit agar lebih rapi
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# ==============================
# FUNGSI LOAD DATA
# ==============================
@st.cache_data
def load_data():
    # Menggunakan path relatif agar tidak error di reviewer
    try:
        # Mencoba load jika file python dijalankan dari root proyek
        df = pd.read_csv('dashboard/main_data.csv')
    except:
        # Mencoba load jika file python dijalankan dari dalam folder dashboard
        df = pd.read_csv('main_data.csv')
    
    # Pastikan M_Score adalah kategori untuk sorting yang benar di grafik
    df['M_Score'] = df['M_Score'].astype(str)
    return df

# Memanggil data
df = load_data()

# ==============================
# SIDEBAR (Bagian Kiri)
# ==============================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=100) # Logo opsional
    st.title("💡 Filter Data")
    st.markdown("---")
    
    # Filter Interaktif berdasarkan M_Score (Syarat Kriteria 5)
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect(
        'Pilih Kelompok M_Score (Skor Moneter):',
        options=m_score_list,
        default=m_score_list
    )
    
    st.markdown("---")
    st.markdown("**Catatan:** Skor 1 (Rendah) s/id 5 (Tinggi)")

# Menerapkan Filter ke Data Utama
df_filtered = df[df['M_Score'].isin(selected_score)]

# ==============================
# MAIN PAGE (Bagian Utama)
# ==============================

# 1. Judul Utama
st.title('E-Commerce Customer Analytics Dashboard 📊')
st.markdown("---")

# 2. Bagian KPI Metrics (Kartu Angka)
st.subheader("Ringkasan Performa Pelanggan")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Pelanggan", value=df_filtered.shape[0])
with col2:
    avg_monetary = df_filtered.Monetary.mean()
    # Format mata uang menggunakan Babel agar rapi (sesuaikan jika perlu currency lain)
    st.metric("Rata-rata Pengeluaran", value=format_currency(avg_monetary, "IDR", locale='id_ID'))
with col3:
    total_transaction = df_filtered.Frequency.sum()
    st.metric("Total Transaksi", value=f"{total_transaction:,}")
with col4:
    max_monetary = df_filtered.Monetary.max()
    st.metric("Pengeluaran Tertinggi", value=format_currency(max_monetary, "IDR", locale='id_ID'))

st.markdown("---")

# 3. Bagian Visualisasi (Syarat Minimal 2 Grafik)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Frekuensi vs Moneter (RFM)")
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    
    # Menggunakan scatterplot dengan palet warna yang menarik
    sns.scatterplot(
        data=df_filtered, 
        x='Frequency', 
        y='Monetary', 
        hue='M_Score', 
        palette='rocket', # Palet warna yang elegan
        alpha=0.7, # Sedikit transparan agar titik yang bertumpuk kelihatan
        ax=ax1
    )
    ax1.set_title("Analisis Segmentasi Pelanggan", fontsize=16)
    ax1.set_xlabel("Jumlah Transaksi (Frequency)", fontsize=12)
    ax1.set_ylabel("Total Pengeluaran (Monetary)", fontsize=12)
    st.pyplot(fig1)
    
    # Menambahkan Insight di bawah grafik
    with st.expander("Lihat Insight Grafik 1"):
        st.write("""
            Grafik ini menunjukkan hubungan antara seberapa sering pelanggan berbelanja (Frequency) 
            dan total uang yang mereka habiskan (Monetary). Pelanggan dengan M_Score tinggi (warna gelap) 
            cenderung berada di area kanan-atas, yang berarti mereka adalah pelanggan paling berharga.
        """)

with col_right:
    st.subheader("2. Distribusi Skor Moneter")
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    
    # Menggunakan countplot untuk melihat jumlah per kategori
    sns.countplot(
        data=df_filtered, 
        x='M_Score', 
        palette='rocket_r', # Palet warna dibalik agar konsisten
        ax=ax2
    )
    ax2.set_title("Jumlah Pelanggan per Kelompok M_Score", fontsize=16)
    ax2.set_xlabel("Skor Moneter", fontsize=12)
    ax2.set_ylabel("Jumlah Pelanggan", fontsize=12)
    st.pyplot(fig2)
    
    # Menambahkan Insight di bawah grafik
    with st.expander("Lihat Insight Grafik 2"):
        st.write("""
            Grafik ini menampilkan berapa banyak pelanggan yang masuk dalam setiap kategori Skor Moneter. 
            Makin tinggi skor (mendekati 5), makin besar kontribusi mereka terhadap pendapatan.
            Distribusinya membantu kita memahami segmentasi pasar kita.
        """)

st.markdown("---")
# Footer
st.caption('Dashboard dikembangkan oleh Alviyatur Rahmaniyah | Data source: E-Commerce Dataset')
