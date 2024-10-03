import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import types

# Load data
@st.cache_data(hash_funcs={types.FunctionType: id})
def load_data():
    day_url = 'https://raw.githubusercontent.com/savirau/bike-sharing/refs/heads/main/day.csv'
    df_day = pd.read_csv(day_url)
    return df_day

df_day = load_data()

# Mengatur halaman judul
st.title('Bike Sharing Dashboard')

# Menampilkan informasi sidebar
st.sidebar.title("Informasi")
st.sidebar.markdown("**Savira Hayyun Audina**")

# Menampilkan Rangkuman Statistik Jika Diseleksi pada Sidebar
st.sidebar.title("Bike Sharing Dataset")
if st.sidebar.checkbox("Tampilkan Dataset"):
    st.subheader("Data Sebelum Analisis")
    st.write(df_day)

# Menampilkan Rangkuman Statistik Jika Diseleksi pada Sidebar
if st.sidebar.checkbox("Tampilkan Statistik"):
    st.subheader("Statistik Data")
    st.write(df_day.describe())

# Sidebar untuk pilihan visualisasi
st.sidebar.title("Visualisasi Data")
opsi_visualisasi = st.sidebar.radio("Pilih Visualisasi: ", ["Pengaruh Musim terhadap Persewaan Sepeda",
                                                            "Fluktuasi Data Bulanan Pesepeda"])

# Mapping nilai musim
season = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_day['season'] = df_day['season'].map(season)

# Data untuk fluktuasi bulanan
fluk = df_day.groupby(['yr', 'mnth'])['cnt'].sum().unstack(level=0)
fluk.columns = ['2011', '2012']

# Visualisasi berdasarkan opsi yang dipilih
if opsi_visualisasi == "Pengaruh Musim terhadap Persewaan Sepeda":
    st.subheader("Pengaruh Musim terhadap Persewaan Sepeda")
    figure = px.pie(df_day, values='cnt', names='season', title='Jumlah Penyewaan Sepeda Berdasarkan Musim')
    figure.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(figure)

else:
    # Membuat bar chart menggunakan matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    fluk.plot(kind='bar', ax=ax)  

    # Mengatur judul dan label sumbu
    ax.set_title('Fluktuasi Bulanan Penyewaan Sepeda')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.legend(title='Tahun')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
