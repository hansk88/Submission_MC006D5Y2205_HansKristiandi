import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menampung file bicycle.csv ke dalam DataFrame
bicycle_df = pd.read_csv("https://github.com/hansk88/Submission_MC006D5Y2205_HansKristiandi/Pandas_read_save_files/main/Dashboard/bicycle.csv")
bicycle_df = pd.read_csv("bicycle.csv")

# Konversi tipe data pada kolom *dteday_by_hour
bicycle_df["dteday_by_hour"] = pd.to_datetime(bicycle_df["dteday_by_hour"])

# Melakukan filter sesuai tahun
def filter(df, year):
    return df[df["yr_by_hour"] == (year - 2011)]

# Membuat tampilan sidebar untuk memilih tahuun
year = st.sidebar.selectbox("Select Year", [2011, 2012])
filtered_df = filter(bicycle_df, year)

# Membuat judul dashboard
st.title(" :man-biking: Dashboard :man-biking:")
st.write(f"These are the visualized data for {year}")

# Menampilkan grafik garis untuk tingkat penyewaan per jam
st.subheader("Bike Rentals by Hour")
hourly_rentals = filtered_df.groupby("hr")["cnt_by_hour"].sum()
fig, ax = plt.subplots()
sns.lineplot(x=hourly_rentals.index,
             y=hourly_rentals.values,
             marker="o",
             ax=ax)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_xticks(range(0, 24, 2))
ax.set_title("Bike Rentals by Hour")
ax.grid(True, linestyle="--")
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan per musim
st.subheader("Bike Rentals by Season")
season_rentals = filtered_df.groupby("season_by_hour")["cnt_by_hour"].sum()
fig, ax = plt.subplots()
colors_1 = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]
sns.barplot(x=season_rentals.index,
            y=season_rentals.values,
            ax=ax,
            palette=colors_1)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Season")
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan per bulan
st.subheader("Bike Rentals by Month")
month_rentals = filtered_df.groupby("mnth_by_hour")["cnt_by_hour"].sum()
fig, ax = plt.subplots()
colors_2 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3","#D3D3D3"]
sns.barplot(x=month_rentals.index,
            y=month_rentals.values,
            ax=ax,
            )
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Month")
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan saat liburan
st.subheader("Bike Rentals: Holidays vs Working Days")
holiday_rentals = filtered_df.groupby("holiday_by_hour")["cnt_by_hour"].sum()
fig, ax = plt.subplots()
sns.barplot(x=["Working Day", "Holiday"], y=holiday_rentals.values, ax=ax, palette="Oranges")
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals on Holidays vs Non-Holidays")
st.pyplot(fig)

# Menampilkan grafik batang untuk tingkat penyewaan sesuai keadaan cuaca
st.subheader("Bike Rentals by Weather Situation")
weather_rentals = filtered_df.groupby("weathersit_by_hour")["cnt_by_hour"].sum()
fig, ax = plt.subplots()
colors_2 = ["Green", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x=weather_rentals.index,
            y=weather_rentals.values,
            ax=ax,
            palette=colors_2)
ax.set_xlabel(None)
ax.set_ylabel("Total Rentals")
ax.set_title("Bike Rentals by Weather Situation")
ax.set_xticks(range(0, 4))
ax.set_xticklabels(["Clear", "Mist/Cloudy", "Light Snow/Rain", "Heavy Snow/Rain"])
st.pyplot(fig)
