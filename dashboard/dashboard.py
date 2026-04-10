import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Mencari lokasi folder tempat file dashboard.py ini berada
base_dir = os.path.dirname(__file__)
# Menggabungkan lokasi folder dengan nama file csv
csv_path = os.path.join(base_dir, 'main_data.csv')

# Setup judul dashboard
st.header('E-Commerce Customer Analysis Dashboard')

# Load data
df = pd.read_csv(csv_path)

# Menampilkan Metric Sederhana
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Customers", value=df.shape[0])
with col2:
    st.metric("Avg Monetary", value=f"IDR {df.Monetary.mean():,.2f}")

# Visualisasi RFM (Scatter Plot yang kita bahas tadi)
st.subheader("Customer Segmentation (Frequency vs Monetary)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df, 
    x='Frequency', 
    y='Monetary', 
    hue='M_Score', # Pakai skor moneter biar berwarna
    palette='viridis',
    ax=ax
)
st.pyplot(fig)

st.write("Insight: Mayoritas pelanggan masih berada di frekuensi rendah (1 kali transaksi).")
