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

st.subheader(":face_with_monocle: Pertanyaan Bisnis")
st.markdown("""- Bagaimana hubungan antara variabel kondisi lingkungan dalam dataset (weather, dll.) terhadap variabel jumlah sepeda yang dipinjam (cnt) dalam suatu hari?\n
    - Specific:\n
    Pertanyaan fokus terhadap topik jumlah sepeda yang dipinjam.
    - Measurable:\n
    Kondisi lingkungan dapat diukur secara kualitatif (cuaca) atau kuantitatif (temperatur) dan jumlah sepeda dapat diukur secara diskret dalam satuan unit.
    - Action-oriented:\n
    Jawaban dari pertanyaan akan digunakan untuk menentukan berapa jumlah sepeda yang harus tersedia untuk memenuhi permintaan pasar pada suatu hari dengan kondisi lingkungan tertentu dan berapa jumlah sepeda yang dapat ditarik dari peredaran untuk dirawat (*maintenance*).
    - Relevant:\n
    Pemasalahan yang dingin diselesaikan melalui pertanyaan ini adalah ketidaktahuan perusahaan atas kebutuhan pasar di kondisi tertentu. Dengan mengetahui informasi tersebut, perusahaan dapat memaksimalkan profit dengan memasok sepeda sesuai kebutuhan pasar selagi melaksanakan perawatan sepeda secara berkala.
    - Time-bound:\n
    Berdasarkan Readme.txt dataset, waktu perekaman dataset adalah sepanjang tahun 2011 dan 2012. Dataset ini mungkin sudah tidak relevan dalam merepresentasikan atau memprediksi kondisi nyata saat proyek ini dikerjakan yaitu pada tahun 2025. Akan tetapi, dataset ini digunakan sebagai bahan pembelajaran. Satuan waktu yang digunakan untuk menghitung jumlah sepeda yang digunakan adalah per 1 hari dan per 1 jam.  

    >Lebih lanjut, pertanyaan tersebut dapat dipecah menjadi sebagai berikut.
    >- Musim apa yang menghasilkan jumlah peminjaman tertinggi?
    >- Cuaca apa yang menghasilkan jumlah peminjaman tertinggi?
    >- Berapa rentang temperatur yang menghasilkan jumlah peminjaman terbanyak?
    >- Berapa rentang kelembapan yang menghasilkan jumlah peminjaman terbanyak?  

- Bagaimana hubungan antara variabel waktu terhadap jumlah peminjaman dalam suatu hari?
    - Specific:\n
    Pertanyaan fokus terhadap topik jumlah peminjaman sepeda.
    - Measurable:\n
    Waktu dapat diukur dalam bentuk tanggal atau musim dan jumlah sepeda dapat diukur dalam satuan unit.
    - Action-oriented:\n
    Jawaban dari pertanyaan akan digunakan untuk menentukan rencana perusahaan dalam menyediakan sepeda agar dapat memaksimalkan keuntungan pada waktu-waktu dengan permintaan pasar yang tinggi.
    - Relevant:\n
    Pemasalahan yang dingin diselesaikan melalui pertanyaan ini adalah ketidaktahuan perusahaan atas kebutuhan pasar di hari tertentu. Dengan mengetahui informasi tersebut, perusahaan dapat memaksimalkan profit dengan memasok sepeda sesuai kebutuhan pasar selagi melaksanakan perawatan sepeda secara berkala.
    - Time-bound:\n
    Aspek waktu dari pertanyaan dapat dijawab dalam satuan hari, bulan, atau musim.  

    >Sama halnya seperti pertanyaan pertama, pertanyaan kedua dapat dipecah menjadi beberapa pertanyaan seperti "Kapan bulan dengan peminjaman terbanyak?", "Kapan musim dengan peminjaman terbanyak?", dan "Kapan hari dengan peminjaman terbanyak?".  

- Apa yang dapat dilakukan perusahaan untuk meningkatkan keuntungan berdasarkan insights yang diperoleh?""")

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
                ":seedling: Faktor Kondisi Lingkungan (Jawaban Pertanyaan 1)",
                ":clock3: Faktor Waktu (Jawaban Pertanyaan 2)",
                ":memo: Kesimpulan"])

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

with tabs[3]:
    st.subheader("Peminjaman Sepeda Pada Setiap Bulan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_day["mnth"], y=df_day["cnt"], errorbar=None, hue=df_day["mnth"], palette="coolwarm", legend=False)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata jumlah peminjaman")
    ax.set_title("Peminjaman sepeda pada setiap bulan")
    st.pyplot(fig)
    st.markdown("Peminjaman paling banyak terjadi di bulan Juni hingga bulan September.")
    
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
    ax.tick_params(axis='x')
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

with tabs[2]:
    st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_day['season'], y=df_day['cnt'], palette='coolwarm', ax=ax)
    ax.set_title("Rata-rata Peminjaman Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig)
    st.markdown("Peminjaman terbanyak terjadi pada musim gugur dan peminjaman paling sedikit terjadi pada musim semi.")

    st.subheader("Pengaruh Cuaca terhadap Peminjaman Sepeda")
    klaster_cuaca = df_hour.groupby("weathersit")["cnt"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=klaster_cuaca["weathersit"], y=klaster_cuaca["cnt"], legend=False, palette="coolwarm", ax=ax)
    ax.set_title("Total Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_xticks([0, 1, 2, 3],["Clear", "Mist", "Light Snow/Rain", "Severe Storm"])
    ax.set_ylabel("Total Peminjaman")
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

    st.subheader("Klasifikasi Peminjaman Berdasarkan Temperatur")
    bins = [0, 20/41, 25/41, 1.0]
    labels = ["Temp. rendah", "Temp. nyaman", "Temp. tinggi"]
    df_day["temp_group"] = pd.cut(df_day["temp"], bins=bins, labels=labels)
    klaster_temperatur = df_day.groupby("temp_group")["cnt"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=klaster_temperatur["temp_group"], y=klaster_temperatur["cnt"], hue=klaster_temperatur["temp_group"], legend=False, palette="coolwarm")
    ax.set_xlabel("Klaster")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Jumlah peminjaman berdasarkan temperatur")
    st.pyplot(fig)
    st.markdown("""Berdasarkan US EPA, temperatur ruangan yang nyaman bagi manusia adalah 20-25 
                derajat celcius. Data temperatur diklasifikasikan secara manual menjadi tiga 
                kelompok yaitu temperatur rendah (<20°C), nyaman (20-25°C), dan tinggi (>25°C). 
                Temperatur maksimum dalam dataset ini adalah 41°C. Pertanyaan: berapa temperatur 
                yang menghasilkan jumlah peminjaman terbanyak? Jawaban: 20°C-41°C""")
    
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
    st.markdown("""Dari visualisasi heatmap, diketahui bahwa jumlah peminjaman dan kelembapan tidak berkorelasi 
                secara linier. Jika dilakukan regresi kuadratik, nilai R-squared yang diperoleh 
                adalah 0.08. Artinya fungsi regresi tidak dapat mewakili variabilitas data dengan 
                baik. Standar deviasi data juga tergolong besar dibandingkan dengan rata-rata. 
                Tingginya standar deviasi ini merepresentasikan data yang sangat tersebar dari 
                rata-rata. Dengan demikian, perusahaan tidak perlu mempertimbangkan kelembapan 
                dalam strategi bisnisnya. Kendati demikian, dapat dilihat secara sekilas bahwa 
                terdapat rentang terjadinya peminjaman yaitu 0.4 hingga 0.8. Analisis dilanjutkan 
                menggunakan boxplot.""")

    st.subheader("Distribusi Kelembapan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x=x_hum)
    ax.set_title("Distribusi Kelembapan dalam Peminjaman")
    ax.set_xlabel("Kelembapan (ternormalisasi)")

    Q1 = np.percentile(x_hum, 25)
    Q3 = np.percentile(x_hum, 75)
    IQR = Q3 - Q1
    uplim_hum = Q3 + (1.5*IQR)
    lolim_hum = Q1 - (1.5*IQR)
    whisker_high = max(x_hum[x_hum <= uplim_hum])
    whisker_low = min(x_hum[x_hum >= lolim_hum])

    ax.text(
        x_hum.min() - 0.025, ax.get_ylim()[1] * 0.95, 
        f'Q1: {Q1:.2f}\nQ3: {Q3:.2f}\nWhisker atas: {whisker_high:.2f}\nWhisker bawah: {whisker_low:.2f}', 
        fontsize=10, verticalalignment='top', horizontalalignment='left'
    )

    ax.axvline(uplim_hum, color='r', linestyle='--', label=f'Q3 + 1.5*IQR ({uplim_hum:.2f})')
    ax.axvline(lolim_hum, color='b', linestyle='--', label=f'Q1 - 1.5*IQR ({lolim_hum:.2f})')
    ax.legend()
    st.pyplot(fig)

    st.markdown("""Pengguna banyak melakukan peminjaman pada kelembapan 0.25 hingga 0.97 dengan 
                50% peminjaman terjadi pada kelembapan 0.52 hingga 0.73. Pertanyaan: berapa 
                rentang kelembapan yang menghasilkan jumlah peminjaman terbanyak? Jawaban: 
                50% peminjaman terjadi pada kelembapan 0.52 sampai 0.73""")
    
with tabs[4]:
    st.subheader("Kesimpulan")
    st.markdown("""- Kondisi lingkungan yang mendukung pengguna untuk meminjam sepeda adalah musim gugur, cuaca cerah, temperatur di atas 20 derajat Celcius, dan kelembapan 0.52 sampai 0.73.\n
- Waktu yang mendukung pengguna untuk meminjam sepeda adalah musim gugur terutama pada bulan Juni hingga September, sekitar pukul 8 pagi dan 5 sore, serta weekends dan hari libur.\n
- Strategi yang dapat dilakukan adalah sebagai berikut.\n
    - Memberi voucher pelanggan baru agar user melakukan pendaftaran.\n
    - Membuat sistem poin dan daily check-in agar pengguna tertarik membuka aplikasi untuk mengumpulkan poin dan melihat penawaran yang ada.\n
    - Memberikan voucher cashback yang hanya dapat digunakan untuk transaksi peminjaman selanjutnya agar user melakukan repurchasing.\n
    - Memberikan voucher diskon kepada registered user pada masa dengan permintaan rendah untuk menaikkan penjualan.\n
    - Strategi-strategi tersebut juga dapat mendorong casual user untuk mendaftar menjadi registered user. Dengan demikian, perusahaan dapat mengumpulkan data secara lebih komprehensif. Salah satu penggunaan data tersebut adalah untuk personalisasi diskon, cashback, dan tukar poin sesuai behavior user.\n
    - Melakukan maintenance ketika jumlah permintaan rendah terutama beberapa waktu sebelum permintaan melonjak (untuk mempersiapkan peak hour).""")

st.caption("oleh Fawaz Amajida")
