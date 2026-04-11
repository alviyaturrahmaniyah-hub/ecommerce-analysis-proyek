import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# ==============================
# 1. PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="E-Commerce Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==============================
# 2. DATA LOADING (PRO VERSION)
# ==============================
@st.cache_data
def load_data():
    # Mengamankan path file agar fleksibel di lokal maupun cloud
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    
    try:
        # Load data dengan deteksi pemisah otomatis
        df = pd.read_csv(file_path, sep=None, engine='python')
        df.columns = df.columns.str.strip()
        
        # Standarisasi tipe data untuk filter
        categorical_cols = ['R_Score', 'F_Score', 'M_Score']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    except Exception:
        return pd.DataFrame()

df_raw = load_data()

# Validasi jika data gagal dimuat
if df_raw.empty:
    st.error("Error: 'main_data.csv' tidak ditemukan atau format tidak sesuai.")
    st.stop()

# ==============================
# 3. SIDEBAR FILTERING
# ==============================
st.sidebar.header("Dashboard Filter")
st.sidebar.markdown("Gunakan filter di bawah untuk melakukan observasi data secara spesifik.")

# Filter R_Score (Sebagai Representasi Recency/Waktu)
r_options = sorted(df_raw['R_Score'].unique())
selected_r = st.sidebar.multiselect(
    "Recency Score (1-5):",
    options=r_options,
    default=r_options,
    help="Skor 5 menunjukkan pelanggan yang paling baru bertransaksi."
)

# Filter M_Score (Representasi Value/Monetary)
m_options = sorted(df_raw['M_Score'].unique())
selected_m = st.sidebar.multiselect(
    "Monetary Score (1-5):",
    options=m_options,
    default=m_options,
    help="Skor 5 menunjukkan pelanggan dengan total belanja tertinggi."
)

# Apply Filter
df_filtered = df_raw[
    (df_raw['R_Score'].isin(selected_r)) & 
    (df_raw['M_Score'].isin(selected_m))
]

# ==============================
# 4. MAIN CONTENT
# ==============================
st.title("E-Commerce Customer Analytics")
st.markdown("Analisis Karakteristik Pelanggan Berdasarkan Parameter RFM (Recency, Frequency, Monetary).")
st.divider()

# --- Section 1: Key Performance Indicators ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Unique Customers", f"{len(df_filtered):,}")

with col2:
    avg_val = df_filtered['Monetary'].mean() if not df_filtered.empty else 0
    st.metric("Avg. Monetary Value", f"BRL {avg_val:,.2f}")

with col3:
    total_tx = df_filtered['Frequency'].sum() if not df_filtered.empty else 0
    st.metric("Total Transactions", f"{total_tx:,}")

st.divider()

# --- Section 2: Visualizations ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Frequency vs Monetary Relationship")
    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=df_filtered, 
            x='Frequency', 
            y='Monetary', 
            hue='M_Score', 
            palette='viridis', 
            ax=ax
        )
        ax.set_title("Distribution of Customer Value by Frequency")
        st.pyplot(fig)
    else:
        st.info("No data available for the selected filters.")

with row1_col2:
    st.subheader("Customer Distribution by Monetary Score")
    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(
            data=df_filtered, 
            x='M_Score', 
            palette='viridis', 
            order=m_options,
            ax=ax
        )
        ax.set_title("Volume of Customers per Monetary Segment")
        st.pyplot(fig)

# --- Section 3: Summary & Interpretation ---
st.divider()
st.subheader("Business Insights")

expander = st.expander("Klik untuk melihat detail analisis", expanded=True)
with expander:
    st.write(f"""
    Analisis terhadap **{len(df_filtered):,}** pelanggan terpilih menunjukkan bahwa:
    1. **Segmentasi:** Distribusi pelanggan pada grafik bar membantu mengidentifikasi porsi segmen kontributor pendapatan terbesar.
    2. **Pola Transaksi:** Melalui scatter plot, kita dapat melihat korelasi antara frekuensi transaksi dan total nilai moneter yang dihasilkan.
    3. **Rekomendasi:** Segmen dengan Recency rendah (R_Score 1-2) memerlukan strategi *win-back* untuk meningkatkan kembali aktivitas transaksi mereka.
    """)

# ==============================
# 5. FOOTER
# ==============================
st.caption("Copyright © 2026 | Alviyatur Rahmaniyah | Data Analysis Project Submission")
