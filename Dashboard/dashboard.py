import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menampung file bicycle.csv ke dalam DataFrame
bicycle_df = pd.read_csv("https://raw.githubusercontent.com/hansk88/Submission_MC006D5Y2205_HansKristiandi/refs/heads/main/Dashboard/bicycle.csv")

# Konversi tipe data pada kolom *dteday_by_hour
bicycle_df["dteday_by_hour"] = pd.to_datetime(bicycle_df["dteday_by_hour"])

# Melakukan filter sesuai tahun
def filter(df, year):
    return df[df["yr_by_hour"] == (year - 2011)]

# Membuat fungsi manual grouping untuk mengelompokkan waktu penyewaan sepeda
def category(hour):
    if 6 <= hour < 11:
        return "Morning"
    elif 11 <= hour < 15:
        return "Afternoon"
    elif 15 <= hour < 18:
        return "Evening"
    else:
        return "Night"

# Membuat fungsi manual grouping untuk mengelompokkan tingkat penyewaan sepeda berdasarkan kategori suhu
def category_1(temperature):
  if temperature <= 10:
    return "cold"
  elif 10 < temperature <= 20:
    return "Cool"
  elif 20 < temperature <= 30:
    return "Warm"
  else:
    return "Hot"

# Menambah kolom kategori waktu
bicycle_df["time_category"] = bicycle_df["hr"].apply(category)

# Menambah kolom kategori suhu
bicycle_df["temp_category"] = bicycle_df["temp_by_hour"].apply(category_1)

# Membuat fungsi
def create_byseason_df(df):
    byseason_df = df.groupby(by=["season_by_hour", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return byseason_df

def create_bymonth_df(df):
    bymonth_df = df.groupby(by=["mnth_by_hour", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return bymonth_df

def create_byday_df(df):
    byday_df = df.groupby(by=["weekday_by_hour", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return byday_df

def create_byhour_df(df):
    byhour_df = df.groupby(by=["hr", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return byhour_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by=["holiday_by_hour", "yr_by_hour"]).cnt_by_hour.mean().reset_index()
    return byholiday_df

def create_byweather_df(df):
    byweather_df = df.groupby(by=["weathersit_by_hour", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return byweather_df

def create_bytimecat_df(df):
    bytimecat_df = df.groupby(by=["time_category", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return bytimecat_df

def create_bytempcat_df(df):
    bytempcat_df = df.groupby(by=["temp_category", "yr_by_hour"]).cnt_by_hour.sum().reset_index()
    return bytempcat_df

# Membuat tampilan sidebar untuk memilih tahuun
year = st.sidebar.selectbox("Select Year", [2011, 2012])
filtered_df = filter(bicycle_df, year)

# Memanggil fungsi
byseason_df = create_byseason_df(filtered_df)
bymonth_df = create_bymonth_df(filtered_df)
byday_df = create_byday_df(filtered_df)
byhour_df = create_byhour_df(filtered_df)
byholiday_df = create_byholiday_df(filtered_df)
byweather_df = create_byweather_df(filtered_df)
bytimecat_df = create_bytimecat_df(filtered_df)
bytempcat_df = create_bytempcat_df(filtered_df)

# Membuat judul dashboard
st.title(" :man-biking: Dashboard :man-biking:")
st.write(f"These are the visualized data for {year}")

# Menampilkan grafik batang untuk tingkat penyewaan per musim
st.subheader("Bike Rentals by Season")
fig, ax = plt.subplots()
colors_1 = ["#D3D3D3", "#72BCD4"]
sns.barplot(data=byseason_df,
            x="season_by_hour",
            y="cnt_by_hour",
            ax=ax,
            palette=colors_1,
            errorbar=None)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Season")
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan per bulan
st.subheader("Bike Rentals by Month")
fig, ax = plt.subplots()
sns.barplot(data=bymonth_df,
            x="mnth_by_hour",
            y="cnt_by_hour",
            ax=ax
            )
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Month")
st.pyplot(fig)

# Menampilkan grafik garis untuk tingkat penyewaan per hari
st.subheader("Bike Rentals by Day")
fig, ax = plt.subplots()
sns.barplot(data=byday_df,
             x="weekday_by_hour",
             y="cnt_by_hour",
             ax=ax)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Day")
ax.set_xticklabels(["", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
st.pyplot(fig)

# Menampilkan grafik garis untuk tingkat penyewaan per jam
st.subheader("Bike Rentals by Hour")
fig, ax = plt.subplots()
sns.lineplot(data=byhour_df,
             x="hr",
             y="cnt_by_hour",
             marker="o",
             ax=ax
             )
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_xticks(range(0, 24, 2))
ax.set_title("Bike Rentals by Hour")
ax.grid(True, linestyle="--")
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan saat liburan
st.subheader("Bike Rentals: Holidays vs Working Days")
fig, ax = plt.subplots()
colors_2 = ["#D3D3D3", "#FF0000"]
sns.barplot(data=byholiday_df,
            x="holiday_by_hour",
            y="cnt_by_hour",
            ax=ax,
            palette=colors_2,
            errorbar=None)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals on Holidays vs Non-Holidays")
ax.set_xticklabels(["Non-holidays", "Holidays"])
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan sesuai keadaan cuaca
st.subheader("Bike Rentals by Weather Situation")
fig, ax = plt.subplots()
colors_2 = ["Green", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(data=byweather_df,
            x="weathersit_by_hour",
            y="cnt_by_hour",
            ax=ax,
            palette=colors_2)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Weather Situation")
ax.set_xticks(range(0, 4))
ax.set_xticklabels(["Clear", "Mist/Cloudy", "Light Snow/Rain", "Heavy Snow/Rain"])
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan sesuai kategori waktu
st.subheader("Bike Rentals by Time Category")
fig, ax = plt.subplots()
colors_2 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "black"]
sns.barplot(data=bytimecat_df,
            x="time_category",
            y="cnt_by_hour",
            ax=ax,
            palette=colors_2)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Time Category")
ax.set_xticks(range(0, 4))
ax.set_xticklabels(["Morning", "Afternoon", "Evening", "Night"])
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan sesuai kategori waktu
st.subheader("Bike Rentals by Temperature Category")
fig, ax = plt.subplots()
colors_3 = ["#D3D3D3", "#D3D3D3", "#E49969", "#D3D3D3"]
sns.barplot(data=bytempcat_df,
            x="temp_category",
            y="cnt_by_hour",
            ax=ax,
            palette=colors_3)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Temperature Category")
ax.set_xticks(range(0, 4))
ax.set_xticklabels(["Cold", "Cool", "Warm", "Hot"])
st.pyplot(fig)
