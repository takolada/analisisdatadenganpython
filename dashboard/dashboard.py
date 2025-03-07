import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set Streamlit page config
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Title
st.title(":bike: Bike Sharing Dashboard")
st.markdown("""
Dashboard ini dibuat untuk memenuhi salah satu prasyarat kelulusan kelas Analisis Data dengan Python (Dicoding).
Dataset yang dianalisis adalah Bike Sharing Dataset dan dapat diakses melalui https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view?usp=sharing.
""")

# Membaca csv database
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
df_day = pd.read_csv(os.path.join(data_path, "day.csv"))
df_hour = pd.read_csv(os.path.join(data_path, "hour.csv"))

# Filter data
min_date = df_day['dteday'].min()
max_date = df_day['dteday'].max()

# Sidebar Filters
with st.sidebar:
    st.header(":mag: Filter Data")
    min_date = df_day['dteday'].min()
    max_date = df_day['dteday'].max()

    date_range = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menggunakan kondisional bahwa akan membuat plot jika rentang waktu sudah dipilih
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_day[(pd.to_datetime(df_day['dteday']) >= pd.to_datetime(start_date)) & (pd.to_datetime(df_day['dteday']) <= pd.to_datetime(end_date))]

    st.subheader(f":date: Visualisasi Peminjaman dari Tanggal {start_date} hingga {end_date}")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=df_filtered['dteday'], y=df_filtered['cnt'], marker='o', linestyle='-', color='blue', ax=ax)
    ax.set_title("Tren Peminjaman Sepeda Harian")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Total Peminjaman")

    # Membuat sumbu x tidak berdesakan dengan membatasi jumlah tanggal yang ditampilkan
    jumlah_tanggal = 20
    tanggal = df_filtered['dteday']
    step = max(1, len(tanggal) // jumlah_tanggal)
    tanggal_tampil = tanggal[::step]
    ax.set_xticks(tanggal_tampil)
    ax.set_xticklabels(tanggal_tampil, rotation=45)
    st.pyplot(fig)
else:
    st.write("Silakan pilih rentang waktu dengan dua tanggal untuk memvisualisasikan data.")

# Membuat Tabs untuk mengklasifikasikan analisis
tabs = st.tabs([":chart_with_upwards_trend: Tren Peminjaman",
                ":link: Korelasi Antarvariabel",
                ":clock3: Faktor Waktu",
                ":seedling: Faktor Kondisi Lingkungan"])

with tabs[0]:
    st.subheader("Peminjaman Sepeda Sepanjang Tahum 2011 dan 2012")
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_day['dteday'], df_day['cnt'], linestyle='-', color='blue')
    ax.set_title("Peminjaman Sepeda Terhadap Waktu")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Total Peminjaman")
    st.pyplot(fig)
    st.markdown("""Peminjaman sepeda dari waktu ke waktu mengalami peningkatan. 
    Tren ini harus dipertahankan melalui strategi-strategi yang disusun berbasis data""")

with tabs[1]:
    st.subheader("Korelasi antara Variabel")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_day.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
    ax.set_title("Heatmap Korelasi")
    st.pyplot(fig)
    st.markdown("""
- Casual dan working day memiliki korelasi terbalik sebesar -0.52, artinya pengguna kasual akan meningkat di hari libur dan weekends. 
- Temp (temperatur) dan cnt (jumlah peminjaman sepeda) berkorelasi searah dengan nilai 0.63, artinya pengguna cenderung meningkat seiring meningkatnya temperatur lingkungan. 
- Dteday (tanggal) dan cnt (jumlah peminjaman) memiliki korelasi berbanding lurus sebesar 0.63, artinya jumlah pelanggan cenderung meningkat seiring berjalannya waktu. Hal ini dapat disebabkan oleh peningkatan permintaan, peningkatan penawaran (ketersediaan sepeda), atau keduanya.
- Temp (*temperature*) dan atemp (*feeling temperature*) memiliki korelasi mendekati 1 (korelasi linear) sehingga selanjutnya analisis akan difokuskan hanya terhadap temp (temperatur).
- Pengguna cenderung meminjam sepeda saat cuaca cerah.
- Weathersit berkorelasi linear dengan kelembapan. Semakin cerah cuaca, semakin rendah kelembapan.
- Weathersit tidak berkorelasi linear terhadap season karena variabel tersebut bersifat kategorikal.
    """)

with tabs[2]:
    st.subheader("Peminjaman Sepeda terhadap Waktu dalam Sehari")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=df_hour['hr'], y=df_hour['cnt'], marker='o', linestyle='-', color='green', ax=ax)
    ax.set_title("Peminjaman Sepeda terhadap Waktu dalam Sehari")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)
    st.markdown("Peminjaman sepeda mencapai puncaknya pada pukul 8 pagi dan 5 sore.")

    st.subheader("Peminjaman Berdasarkan Hari")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=['Holiday', 'Weekend', 'Workday'],
        y=[
            df_day[df_day['holiday'] == 1]['cnt'].mean(),
            df_day[df_day['weekday'].isin([0, 6])]['cnt'].mean(),
            df_day[df_day['workingday'] == 1]['cnt'].mean()
        ],
        palette='coolwarm',
        ax=ax
    )
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Tipe Hari")
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Rata-rata Peminjaman")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    st.markdown("Peminjaman sepeda paling banyak terjadi pada hari kerja.")

    st.subheader("Peminjaman Harian berdasarkan Tanggal")
    df_sorted = df_day.sort_values(by='cnt', ascending=False)

    # Plot tertinggi
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(y=df_sorted['cnt'].head(5), x=df_sorted['dteday'].head(5), palette=colors, ax=ax)
    ax.set_title("5 Tanggal dengan Peminjaman Tertinggi")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    st.markdown("Tidak ditemukan peristiwa unik pada tanggal dengan peminjaman terbanyak terjadi.")
    
    # Plot terendah
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
    sns.barplot(y=df_sorted['cnt'].tail(5), x=df_sorted['dteday'].tail(5), palette=colors, ax=ax)
    ax.set_title("5 Tanggal dengan Peminjaman Terendah")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    st.markdown("Peminjaman paling sedikit terjadi pada tanggal 2012-10-29 yaitu 22 peminjaman. Pada hari tersebut, terjadi Badai Sandy di New York City [[Wikipedia](https://en.wikipedia.org/wiki/Portal:Current_events/2012_October_29)].")

with tabs[3]:
    st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_day['season'], y=df_day['cnt'], palette='coolwarm', ax=ax)
    ax.set_title("Rata-rata Peminjaman Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig)
    st.markdown("Peminjaman terbanyak terjadi pada musim gugur dan peminjaman paling sedikit terjadi pada musim semi.")

    st.subheader("Pengaruh Cuaca terhadap Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_day['weathersit'].unique(), y=df_day.groupby('weathersit')['cnt'].mean(), palette='viridis', ax=ax)
    ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig)
    st.markdown("Pengguna lebih sering mengendarai sepeda saat cuaca cerah.")

    st.subheader("Pengaruh Temperatur terhadap Peminjaman Sepeda")
    # Regresi polinomial agar tren lebih terlihat
    x_temp = df_day['temp']
    y_temp = df_day['cnt']
    poly_temp = np.polyfit(x_temp, y_temp, 2)
    p_temp = np.poly1d(poly_temp)
    # Plot visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=x_temp, y=y_temp, alpha=0.6, color='red', ax=ax)
    ax.plot(np.sort(x_temp), p_temp(np.sort(x_temp)), color='blue')
    ax.set_title("Hubungan Temperatur dan Jumlah Peminjaman")
    ax.set_xlabel("Temperatur (ternormalisasi)")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)
    st.markdown("""Tren kenaikan jumlah peminjaman terlihat seiring meningkatnya temperatur 
    hingga menurun kembali di titik tertentu. Akan tetapi, tren ini memiliki standar deviasi yang tinggi.""")
    
    st.subheader("Pengaruh Kelembaban terhadap Peminjaman Sepeda")
    # Regresi polinomial agar tren lebih terlihat
    x_hum = df_day['hum']
    y_hum = df_day['cnt']
    poly_hum = np.polyfit(x_hum, y_hum, 2)
    p_hum = np.poly1d(poly_hum)
    # Plot visualisasi
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=x_hum, y=y_hum, alpha=0.6, color='orange', ax=ax)
    ax.plot(np.sort(x_hum), p_hum(np.sort(x_hum)), color='blue')
    ax.set_title("Hubungan Kelembaban dan Jumlah Peminjaman")
    ax.set_xlabel("Kelembaban (ternormalisasi)")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)
    st.markdown("Tidak terdapat korelasi yang signifikan antara peminjaman dengan kelembapan udara.")

st.caption("oleh Fawaz Amajida")
