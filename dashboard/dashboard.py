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
# 2. DATA LOADING (SMART VERSION)
# ==============================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    
    if not os.path.exists(file_path):
        file_path = 'main_data.csv'
    
    try:
        # PENTING: sep=None & engine='python' otomatis mendeteksi pemisah kolom
        df = pd.read_csv(file_path, sep=None, engine='python')
        
        # Bersihkan spasi di nama kolom
        df.columns = df.columns.str.strip()
        
        # Konversi skor ke string agar filter multiselect berjalan lancar
        target_cols = ['R_Score', 'F_Score', 'M_Score']
        for col in target_cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    except Exception as e:
        return pd.DataFrame()

df_raw = load_data()

# Validasi Data
if df_raw.empty:
    st.error("⚠️ Sistem tidak dapat membaca file 'main_data.csv'. Pastikan file tersedia dan tidak kosong.")
    st.stop()

# ==============================
# 3. SIDEBAR NAVIGATION & FILTER
# ==============================
st.sidebar.header("Data Filter Control")
st.sidebar.markdown("Sesuaikan parameter di bawah untuk eksplorasi dinamis.")

# Filter R_Score (Representasi Recency)
if 'R_Score' in df_raw.columns:
    r_options = sorted(df_raw['R_Score'].unique())
    selected_r = st.sidebar.multiselect(
        "Recency Level (R_Score):",
        options=r_options,
        default=r_options,
        help="Skor 5 menunjukkan pelanggan dengan transaksi terbaru."
    )

# Filter M_Score (Representasi Monetary)
if 'M_Score' in df_raw.columns:
    m_options = sorted(df_raw['M_Score'].unique())
    selected_m = st.sidebar.multiselect(
        "Value Level (M_Score):",
        options=m_options,
        default=m_options,
        help="Skor 5 menunjukkan kontribusi pendapatan tertinggi."
    )

# Logic Filter
df_filtered = df_raw[
    (df_raw['R_Score'].isin(selected_r)) & 
    (df_raw['M_Score'].isin(selected_m))
]

# ==============================
# 4. MAIN DASHBOARD CONTENT
# ==============================
st.title("E-Commerce Customer Analytics Dashboard")
st.markdown("Visualisasi ini dikembangkan untuk menjawab karakteristik pelanggan berdasarkan metodologi RFM.")
st.divider()

# --- Section 1: Business Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Observed Customers", f"{len(df_filtered):,}")

with col2:
    if 'Monetary' in df_filtered.columns:
        avg_monetary = df_filtered['Monetary'].mean()
        st.metric("Average Customer Value", f"BRL {avg_monetary:,.2f}")

with col3:
    if 'Frequency' in df_filtered.columns:
        total_freq = df_filtered['Frequency'].sum()
        st.metric("Aggregate Transaction Volume", f"{total_freq:,}")

st.divider()

# --- Section 2: Visualizations ---
row1_c1, row1_c2 = st.columns(2)

with row1_c1:
    st.subheader("Transaction Behavior Pattern")
    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=df_filtered, 
            x='Frequency', 
            y='Monetary', 
            hue='M_Score', 
            palette='coolwarm', 
            ax=ax
        )
        ax.set_title("Scatter Plot: Frequency vs Monetary Value")
        st.pyplot(fig)

with row1_c2:
    st.subheader("Customer Distribution by Value Segment")
    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(
            data=df_filtered, 
            x='M_Score', 
            palette='Blues_r', 
            order=sorted(df_raw['M_Score'].unique()),
            ax=ax
        )
        ax.set_title("Bar Chart: Count of Customers per M_Score")
        st.pyplot(fig)

# --- Section 3: Professional Insight ---
st.divider()
with st.expander("📌 Executive Summary & Analysis Insight", expanded=True):
    st.write(f"""
    Berdasarkan observasi terhadap **{len(df_filtered):,}** pelanggan, ditemukan beberapa poin krusial:
    * **Customer Base:** Sebaran data pada grafik distribusi menunjukkan proporsi segmen pelanggan berdasarkan nilai ekonominya.
    * **Engagement:** Melalui korelasi frekuensi dan moneter, bisnis dapat memetakan kelompok pelanggan yang membutuhkan strategi retensi khusus.
    * **Dynamic Exploration:** Seluruh metrik dan visualisasi di atas akan diperbarui secara *real-time* saat filter pada sidebar disesuaikan.
    """)

# Footer
st.caption("Submitted by Alviyatur Rahmaniyah | © 2026 E-Commerce Data Analytics Project")
