# Bike Sharing Dashboard ✨

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```

>## **Dataset Tambahan**  
>Terdapat dataset tambahan yang digunakan untuk mencoba Geospatial Analysis.
>Dataset tersebut adalah "2011-capitalbikeshare-tripdata.zip" dan "2012-capitalbikeshare-tripdata.zip" 
>yang memuat catatan tempat terjadinya peminjaman sepeda. Dataset tersebut berukuran besar
>dan tidak dapat diunggah ke Github. Dataset dapat diakses melalui https://s3.amazonaws.com/capitalbikeshare-data/index.html.
>Dataset tersebut disusun dengan path sebagai berikut.
>
>- \data\Bike Sharing Raw\2011-capitalbikeshare-tripdata.csv  
>- \data\Bike Sharing Raw\2012Q1-capitalbikeshare-tripdata.csv  
>- \data\Bike Sharing Raw\2012Q2-capitalbikeshare-tripdata.csv  
>- \data\Bike Sharing Raw\2012Q3-capitalbikeshare-tripdata.csv  
>- \data\Bike Sharing Raw\2012Q4-capitalbikeshare-tripdata.csv
