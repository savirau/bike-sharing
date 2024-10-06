import streamlit as st  # Mengimpor pustaka Streamlit untuk membuat aplikasi web
import pandas as pd  # Mengimpor pustaka Pandas untuk manipulasi dan analisis data
import matplotlib.pyplot as plt  # Mengimpor matplotlib untuk visualisasi data
import plotly.express as px  # Mengimpor Plotly Express untuk visualisasi interaktif
import types  # Mengimpor modul types untuk mendukung penggunaan caching

# Load data
@st.cache_data(hash_funcs={types.FunctionType: id})  # Mencache fungsi load_data untuk mengoptimalkan performa
def load_data():
    # URL untuk dataset penyewaan sepeda
    day_url = 'https://raw.githubusercontent.com/savirau/bike-sharing/refs/heads/main/Bike-Sharing-Dataset/day.csv'
    df_day = pd.read_csv(day_url)  # Memuat dataset dari URL
    return df_day  # Mengembalikan DataFrame yang dimuat

# Memanggil fungsi load_data untuk mendapatkan data
df_day = load_data()

# Mengatur halaman judul
st.title('Bike Sharing Dashboard')  # Menampilkan judul aplikasi

# Menampilkan informasi sidebar
st.sidebar.title("Informasi")  # Judul untuk sidebar
st.sidebar.markdown("**Savira Hayyun Audina**")  # Menampilkan nama pengguna di sidebar

# Menampilkan Rangkuman Statistik Jika Diseleksi pada Sidebar
st.sidebar.title("Bike Sharing Dataset")  # Judul untuk bagian dataset di sidebar
if st.sidebar.checkbox("Tampilkan Dataset"):  # Checkbox untuk menampilkan dataset
    st.subheader("Data Sebelum Analisis")  # Subjudul untuk bagian dataset
    st.write(df_day)  # Menampilkan DataFrame

# Menampilkan Rangkuman Statistik Jika Diseleksi pada Sidebar
if st.sidebar.checkbox("Tampilkan Statistik"):  # Checkbox untuk menampilkan statistik
    st.subheader("Statistik Data")  # Subjudul untuk statistik
    st.write(df_day.describe())  # Menampilkan ringkasan statistik

# Sidebar untuk pilihan visualisasi
st.sidebar.title("Visualisasi Data")  # Judul untuk bagian visualisasi di sidebar
opsi_visualisasi = st.sidebar.radio("Pilih Visualisasi: ", ["Persentase Penyewaan Sepeda Berdasarkan Musim", 
                                                            "Fluktuasi Data Bulanan Pesepeda"])  # Pilihan visualisasi

# Mapping nilai musim
season = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}  # Mapped nilai musim ke nama
df_day['season'] = df_day['season'].map(season)  # Mengubah kolom 'season' dari angka ke nama musim

# Data untuk fluktuasi bulanan
fluk = df_day.groupby(['yr', 'mnth'])['cnt'].sum().unstack(level=0)  # Mengelompokkan data berdasarkan tahun dan bulan, menjumlahkan 'cnt'
fluk.columns = ['2011', '2012']  # Menamai kolom untuk tahun

# Visualisasi berdasarkan opsi yang dipilih
if opsi_visualisasi == "Persentase Penyewaan Sepeda Berdasarkan Musim":  # Jika opsi visualisasi dipilih
    st.subheader("Persentase Penyewaan Sepeda Berdasarkan Musim")  # Subjudul untuk visualisasi musim
    figure = px.pie(df_day, values='cnt', names='season', title='Jumlah Penyewaan Sepeda Berdasarkan Musim')  # Membuat pie chart
    figure.update_traces(textposition='inside', textinfo='percent+label')  # Mengupdate posisi teks dan informasi
    st.plotly_chart(figure)  # Menampilkan pie chart di aplikasi

else:  # Jika opsi visualisasi adalah fluktuasi bulanan
    # Membuat bar chart menggunakan matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))  # Membuat figure dan axis untuk plotting
    fluk.plot(kind='bar', ax=ax)  # Menggunakan ax untuk memasukkan plot ke dalam figure

    # Mengatur judul dan label sumbu
    ax.set_title('Fluktuasi Bulanan Penyewaan Sepeda')  # Judul untuk bar chart
    ax.set_xlabel('Bulan')  # Label sumbu X
    ax.set_ylabel('Jumlah Penyewaan')  # Label sumbu Y
    ax.legend(title='Tahun')  # Menambahkan legenda

    # Menampilkan plot di Streamlit
    st.pyplot(fig)  # Menampilkan grafik di aplikasi Streamlit
