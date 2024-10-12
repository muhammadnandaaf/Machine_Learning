import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_daily_registered(df): # Menyiapkan daily registered
    daily_registered_df = df.groupby(by='date').agg({
        'registered':'sum'
    }).reset_index()
    return daily_registered_df

def create_daily_casual(df): # Menyiapkan daily casual
    daily_casual_df = df.groupby(by='date').agg({
        'casual':'sum'
    }).reset_index()
    return daily_casual_df

def create_daily_rent(df): # Menyiapkan daily registered & casual
    daily_rent_df = df.groupby(by='date').agg({
        'total_renters':'sum'
    }).reset_index()
    return daily_rent_df

def create_season_rent(df): # Menyiapkan season rent
    season_rent_df = df.groupby(by='season').agg({
        'total_renters':'sum'
    }).reset_index()
    return season_rent_df

def create_holiday_rent(df): # Menyiapkan holiday rent
    holiday_rent_df = df.groupby(by='holiday').agg({
        'total_renters':'sum'
    }).reset_index()
    return holiday_rent_df

def create_weekday_rent(df): # Menyiapkan weekday rent
    weekday_rent_df = df.groupby(by='weekday').agg({
        'total_renters':'sum'
    }).reset_index()
    return weekday_rent_df

def create_weekend_rent(df): # Menyiapkan weekend rent
    weekend_rent_df = df.groupby(by='day_type').agg({
        'total_renters':'sum'
    }).reset_index()
    return weekend_rent_df

def create_weatherCond_rent(df): # Menyiapkan wheather condition rent
    weatherCond_rent_df = df.groupby(by='weather_situation').agg({
        'total_renters':'sum'
    }).reset_index()
    return weatherCond_rent_df

def create_monthly_rent(df):  # Menyiapkan monthly rent
    monthly_rent_df = df.groupby(by='month').agg({
        'total_renters':'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

day_df = pd.read_csv("Processed_day_df.csv")

# Membuat Komponen Filter
min_date = pd.to_datetime(day_df['date']).dt.date.min()
max_date = pd.to_datetime(day_df['date']).dt.date.max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["date"] >= str(start_date)) & 
                (day_df["date"] <= str(end_date))]

# Memanggil Helper function yang telah dibuat
daily_rent_df = create_daily_rent(main_df)
registered_rent_df = create_daily_registered(main_df)
casual_rent_df = create_daily_casual(main_df)
season_rent_df = create_season_rent(main_df)
holiday_rent_df = create_holiday_rent(main_df)
weekday_rent_df = create_weekday_rent(main_df)
weekend_rent_df = create_weekend_rent(main_df)
weatherCond_rent_df = create_weatherCond_rent(main_df)
monthly_rent_df = create_monthly_rent(main_df)


st.header('Proyek Analisis Data: Bike Rental Sharing Dataset :sparkles:')

# Jumlah Penyewa Harian
st.subheader('Daily Rent')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent = daily_rent_df.total_renters.sum()
    st.metric("Total rental registered & casual", value=daily_rent)

with col2:
    registered_rent = registered_rent_df['registered'].sum()
    st.metric("Total rental registered", value=registered_rent)

with col3:
    casual_rent = casual_rent_df['casual'].sum()
    st.metric("Total rental casual", value=casual_rent)

# tren Penjualan

st.subheader("Tren Penjualan perusahaan dalam 2 tahun terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["date"],
    day_df["total_renters"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Jumlah Penyewa Berdasarkan Musim dan Keadaan Cuaca
st.subheader("Jumlah Penyewa")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="total_renters", 
    y="season", data=season_rent_df, 
    palette=colors, 
    ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Penyewa Musiman", fontsize=30)
ax[0].set_title("Berdasarkan Musim", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    x="total_renters", 
    y="weather_situation", 
    data=weatherCond_rent_df.sort_values(by="total_renters", ascending=True), 
    palette=colors, 
    ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Penyewa Saat Cuaca", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Berdasarkan Cuaca", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

# Jumlah Penyewa Weekend,  Weekday, dan Holiday
st.subheader("Penyewa Saat Weekend, Weekday, dan Holiday")
 
col1, col2 = st.columns(2)

with col1: # Menampilkan data jumlah penyewa saat weekend
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="total_renters", 
        x="day_type",
        data=weekend_rent_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Penyewa saat Akhir Pekan", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2: # Menampilkan data jumlah penyewa saat holiday
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="total_renters", 
        x="holiday",
        data=holiday_rent_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Penyewa Saat Holiday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Menampilkan data jumlah penyewa saat weekday
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="total_renters", 
    y="weekday",
    data=weekday_rent_df.sort_values(by="total_renters", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Jumlah Penyewa ketika hari biasa", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)