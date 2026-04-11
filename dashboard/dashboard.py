# ==============================
# FUNGSI LOAD DATA (SESUAIKAN NAMA KOLOM)
# ==============================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dashboard/main_data.csv')
    except:
        df = pd.read_csv('main_data.csv')
    
    # Cek apakah kolom tanggal ada, kalau tidak ada kita skip filter tanggalnya
    # supaya dashboard gak nge-crash/error lagi
    date_col = 'order_purchase_timestamp' # Ganti ini kalau nama kolom tanggalmu beda
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
    
    df['M_Score'] = df['M_Score'].astype(str)
    return df

df = load_data()

# ==============================
# SIDEBAR (VERSI AMAN)
# ==============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ Menu Utama ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Filter Tanggal hanya muncul kalau kolomnya ada
    date_col = 'order_purchase_timestamp' 
    if date_col in df.columns:
        st.write("📅 **Filter Rentang Waktu**")
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        start_date, end_date = st.date_input(
            label='Pilih Periode:',
            min_value=min_date, max_value=max_date,
            value=[min_date, max_date]
        )
        # Proses filter tanggal
        df_filtered = df[(df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))]
    else:
        # Kalau gak ada kolom tanggal, df_filtered pakai data asli dulu
        df_filtered = df.copy()

    # FILTER M_SCORE
    st.write("🔍 **Filter Skor Moneter**")
    m_score_list = sorted(df['M_Score'].unique())
    selected_score = st.multiselect('Pilih M_Score:', options=m_score_list, default=m_score_list)
    
    # Apply filter M_Score
    df_filtered = df_filtered[df_filtered['M_Score'].isin(selected_score)]
