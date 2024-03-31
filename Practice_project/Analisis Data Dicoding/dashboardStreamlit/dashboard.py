import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("day.csv")

# Mengubah nama kolom
all_df.rename(columns={
    'dteday':'dateDay',
    'yr':'year',
    'mnth':'month',
    'hr':'hour',
    'hum':'humidity',
    'tempt':'temperature',
    'weathersit':'weath_cond',
    'cnt':'rent_count'
}, inplace = True)
all_df.head()

# Mengubah keterangan cuaca, bulan, hari, musim
all_df['weath_cond'] = all_df['weath_cond'].map({
    1 : 'Clear/Partly Cloudy',
    2 : 'Mist/Cloudy',
    3 : 'Light Snow/Rain/Scattered Clouds',
    4 : 'Worst Weather'
})

all_df['month'] = all_df['month'].map({
    1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun',
    7:'Jul', 8:'Aug', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Dec'
})

all_df['weekday'] = all_df['weekday'].map({
    0:'Sun', 1:'Mon', 2:'Tue', 3:'Wed', 
    4:'Thu', 5:'Fri', 6:'Sat'
})

all_df['season'] = all_df['season'].map({
    1:'springer', 2:'summer', 
    3:'fall', 4:'winter'
})

all_df['workingday'] = all_df['workingday'].map({
    0:'weekend/non-workday',
    1:'workday'
})

all_df['year'] = all_df['year'].map({
    0:'2011',
    1:'2012'
})

all_df['holiday'] = all_df['holiday'].map({
    0:'holiday',
    1:'not'
})
# Membuat helper function

def create_daily_registered(df): # Menyiapkan daily registered
    daily_registered_df = df.groupby(by='dateDay').agg({
        'registered':'sum'
    }).reset_index()
    return daily_registered_df

def create_daily_casual(df): # Menyiapkan daily casual
    daily_casual_df = df.groupby(by='dateDay').agg({
        'casual':'sum'
    }).reset_index()
    return daily_casual_df

def create_daily_rent(df): # Menyiapkan daily registered & casual
    daily_rent_df = df.groupby(by='dateDay').agg({
        'rent_count':'sum'
    }).reset_index()
    return daily_rent_df

def create_season_rent(df): # Menyiapkan season rent
    season_rent_df = df.groupby(by='season').agg({
        'rent_count':'sum'
    }).reset_index()
    return season_rent_df

def create_workingday_rent(df): # Menyiapkan workingday rent
    workingday_rent_df = df.groupby(by='workingday').agg({
        'rent_count':'sum'
    }).reset_index()
    return workingday_rent_df

def create_holiday_rent(df): # Menyiapkan holiday rent
    holiday_rent_df = df.groupby(by='holiday').agg({
        'rent_count':'sum'
    }).reset_index()
    return holiday_rent_df

def create_weekday_rent(df): # Menyiapkan weekday rent
    weekday_rent_df = df.groupby(by='weekday').agg({
        'rent_count':'sum'
    }).reset_index()
    return weekday_rent_df

def create_weatherCond_rent(df): # Menyiapkan wheather condition rent
    weatherCond_rent_df = df.groupby(by='weath_cond').agg({
        'rent_count':'sum'
    }).reset_index()
    return weatherCond_rent_df

def create_monthly_rent(df):  # Menyiapkan monthly rent
    monthly_rent_df = df.groupby(by='month').agg({
        'rent_count':'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Membuat Komponen Filter
min_date = pd.to_datetime(all_df['dateDay']).dt.date.min()
max_date = pd.to_datetime(all_df['dateDay']).dt.date.max()

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

main_df = all_df[(all_df["dateDay"] >= str(start_date)) & 
                (all_df["dateDay"] <= str(end_date))]

# Memanggil Helper function yang telah dibuat
daily_rent_df = create_daily_rent(main_df)
registered_rent_df = create_daily_registered(main_df)
casual_rent_df = create_daily_casual(main_df)
season_rent_df = create_season_rent(main_df)
workingday_rent_df = create_workingday_rent(main_df)
holiday_rent_df = create_holiday_rent(main_df)
weekday_rent_df = create_weekday_rent(main_df)
weatherCond_rent_df = create_weatherCond_rent(main_df)
monthly_rent_df = create_monthly_rent(main_df)

st.header('Proyek Analisis Data: Bike Sharing Dataset :sparkles:')

# Jumlah Penyewa Harian
st.subheader('Daily Rent')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent = daily_rent_df.rent_count.sum()
    st.metric("Total rental registered & casual", value=daily_rent)

with col2:
    registered_rent = registered_rent_df['registered'].sum()
    st.metric("Total rental registered", value=registered_rent)

with col3:
    casual_rent = casual_rent_df['casual'].sum()
    st.metric("Total rental casual", value=casual_rent)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df['rent_count'],
    registered_rent_df['registered'],
    casual_rent_df['casual'],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Jumlah Penyewa Bulanan
st.subheader('Monthly Rent')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['rent_count'],
    marker='o', 
    linewidth=2,
    color='skyblue'
)

for index, row in enumerate(monthly_rent_df['rent_count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Jumlah Penyewa Berdasarkan Musim dan Keadaan Cuaca
st.subheader("Jumlah Penyewa")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="rent_count", y="season", data=season_rent_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Penyewa Musiman", fontsize=30)
ax[0].set_title("Berdasarkan Musim", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="rent_count", y="weath_cond", data=weatherCond_rent_df.sort_values(by="rent_count", ascending=True), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Penyewa Saat Cuaca", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Berdasarkan Cuaca", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

# Jumlah Penyewa WorkingDay,  Weekday, dan Holiday
st.subheader("Penyewa Saat Workingday, Weekday, dan Holiday")
 
col1, col2 = st.columns(2)

with col1: # Menampilkan data jumlah penyewa saat workingday
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="rent_count", 
        x="workingday",
        data=workingday_rent_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Penyewa saat Hari Kerja", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2: # Menampilkan data jumlah penyewa saat holiday
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="rent_count", 
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
    x="rent_count", 
    y="weekday",
    data=weekday_rent_df.sort_values(by="rent_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Jumlah Penyewa ketika hari biasa", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)