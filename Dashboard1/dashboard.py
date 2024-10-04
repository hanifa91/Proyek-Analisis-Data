import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

# Menyiapkan data day_df
day_df  = pd.read_csv("day_byke_2012.csv")
day_df.head()

# Mengubah nama judul kolom 

day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather',
    'cnt': 'count',
}, inplace=True)

# Membuat DataFrame berdasarkan weathersin dan season

# Menyiapkan create_byweather_day_2012()
def create_weather_df(df):
    weather_df = df.groupby(by="weather").agg({
        "count": "mean"
    }).reset_index()
    return weather_df
    
#Menyiapkan create_byseason_day_2012
def create_season_df(df):
    season_df = df.groupby(by="season").agg({
        "count": "mean"
    }).reset_index()
    return season_df

# membuat filter dengan widget date input 
day_df ['dateday'] = pd.to_datetime(day_df['dateday'])  # Mengonversi ke datetime

# Menentukan min_date dan max_date
min_date = day_df["dateday"].min().date()  # Mengambil tanggal minimum
max_date = day_df["dateday"].max().date()  # Mengambil tanggal maksimum

# Membuat filter dengan widget date input 
with st.sidebar:
    # Menambahkan logo perusahaan
    #st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)  # Menggunakan tuple
    )

# Memfilter day_df berdasarkan rentang tanggal
# Mengonversi start_date dan end_date ke tipe datetime
start_date = pd.to_datetime(start_date) 
end_date = pd.to_datetime(end_date)

main_df = day_df[(day_df['dateday'] >= start_date) & (day_df['dateday'] <= end_date)]

# Menghasilkan DataFrame berdasarkan main_df
weather_df = create_weather_df(main_df)
season_df = create_season_df(main_df)

# Menampilkan header utama
st.header('Dashboard Penyewaan Sepeda Dicoding :sparkles:')

# Menampilkan DataFrame yang telah difilter
st.subheader("Data Penyewaan Sepeda dari {} hingga {}".format(start_date.date(), end_date.date()))
st.dataframe(main_df)

# Menampilkan DataFrame berdasarkan cuaca
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
st.dataframe(weather_df)

# Menampilkan DataFrame berdasarkan musim
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
st.dataframe(season_df)

# Visualisasi DataFrame berdasarkan cuaca
plt.figure(figsize=(10, 5))
sns.barplot(data=weather_df, x='weather', y='count', hue='weather', palette='viridis', legend=False)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca (2012)')
plt.xlabel('Cuaca')
plt.ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(plt)  # Menampilkan plot di Streamlit

# Visualisasi DataFrame berdasarkan musim
plt.figure(figsize=(10, 5))
sns.barplot(data=season_df, x='season', y='count', hue='season', palette='plasma', legend=False)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Musim (2012)')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(plt)  # Menampilkan plot di Streamlit


