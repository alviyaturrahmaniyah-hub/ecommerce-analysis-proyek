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
    
    # Pastikan kolom tanggal jadi datetime
    # Sesuaikan 'order_purchase_timestamp' dengan nama kolom tanggal di CSV kamu
    if 'order_purchase_timestamp' in df.columns:
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    df['M_Score'] = df['M_Score'].astype(str)
    return df

df = load_data()

# ==============================
# SIDEBAR (FILTER)
# ==============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ Menu Utama ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # FILTER 1: RENTANG WAKTU (PENTING!)
    st.write("📅 **Filter Rentang Waktu**")
    min_date = df['order_purchase_timestamp'].min()
    max_date = df['order_purchase_timestamp'].max()
    
    start_date, end_date = st.date_input(
        label='Pilih Periode:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # FILTER 2: M_SCORE
    st.write("🔍 **Filter Skor Moneter**")
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect('Pilih M_Score:', options=m_score_list, default=m_score_list)
    
    st.markdown("---")
    st.info("💡 Dashboard ini menampilkan performa penjualan dan analisis pelanggan RFM.")

# Proses Filter Data
df_filtered = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & 
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date)) &
    (df['M_Score'].isin(selected_score))
]

# ==============================
# MAIN PAGE
# ==============================
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📊 E-Commerce Performance & Customer Analytics</h1>", unsafe_allow_html=True)
st.markdown("---")

# KPI Metrics
st.subheader("📌 Business Summary Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", value=f"{df_filtered.customer_id.nunique():,}")
with col2:
    total_revenue = df_filtered.Monetary.sum()
    st.metric("Total Revenue", value=f"BRL {total_revenue:,.0f}")
with col3:
    total_orders = df_filtered.Frequency.sum()
    st.metric("Total Orders", value=f"{total_orders:,.0f}")

st.markdown("---")

# BARIS 1: TREN PENJUALAN (Menjawab Pertanyaan Bisnis 1)
st.subheader("📈 Tren Penjualan Bulanan")
# Resampling data untuk tren bulanan
monthly_df = df_filtered.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "Monetary": "sum"
})
monthly_df.index = monthly_df.index.strftime('%Y-%m')
monthly_df = monthly_df.reset_index()

fig_trend, ax_trend = plt.subplots(figsize=(16, 6))
sns.lineplot(data=monthly_df, x='order_purchase_timestamp', y='Monetary', marker='o', color='#4A90E2', ax=ax_trend)
plt.title("Perkembangan Pendapatan (2016-2018)", fontsize=15)
plt.xticks(rotation=45)
st.pyplot(fig_trend)

st.markdown("---")

# BARIS 2: RFM ANALYSIS (Menjawab Pertanyaan Bisnis 2)
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🎯 Hubungan Frekuensi & Moneter")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df_filtered, x='Frequency', y='Monetary', hue='M_Score', palette='magma', ax=ax1)
    st.pyplot(fig1)

with col_right:
    st.markdown("### 📊 Sebaran Skor Pelanggan (M_Score)")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.countplot(data=df_filtered, x='M_Score', palette='magma', ax=ax2)
    st.pyplot(fig2)

# FOOTER
st.markdown("---")
st.markdown("<div style='text-align: center;'>Created with ❤️ by <b>Alviyatur Rahmaniyah</b> | © 2026</div>", unsafe_allow_html=True)
