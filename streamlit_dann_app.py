import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Matplotlib",
    page_icon="📊",
    layout="wide"
)

# =========================
# TITLE
# =========================
st.title("🌐 DanWeb")
st.caption("✨ Dashboard ini menampilkan ringkasan penjualan dan pengunjung secara interaktif menggunakan Streamlit dan Matplotlib.")

st.markdown("""
Selamat datang di **Dashboard Penjualan**!  
Gunakan panel **sidebar** untuk:
- 📂 Upload file CSV
- 📅 Filter hari
- 🍔 Filter kategori (jika tersedia)

Dashboard akan otomatis menampilkan **KPI**, **tabel data**, dan **visualisasi grafik**.
""")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Pengaturan & Filter")

uploaded_file = st.sidebar.file_uploader("📂 Upload CSV (opsional)", type=["csv"])

@st.cache_data
def load_sample_data():
    df = pd.DataFrame({
        "Hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"],
        "Kategori": ["Makanan", "Minuman", "Makanan", "Minuman", "Makanan", "Minuman", "Makanan"],
        "Penjualan": [120, 150, 90, 170, 200, 220, 180],
        "Pengunjung": [50, 60, 30, 80, 90, 120, 100]
    })
    return df

# Load data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Data berhasil diupload!")
else:
    df = load_sample_data()
    st.sidebar.info("ℹ️ Menggunakan data contoh bawaan.")

# =========================
# FILTERS
# =========================
hari_list = df["Hari"].unique().tolist()
selected_hari = st.sidebar.multiselect("📅 Filter Hari", hari_list, default=hari_list)

if "Kategori" in df.columns:
    kategori_list = df["Kategori"].unique().tolist()
    selected_kategori = st.sidebar.multiselect("🍔 Filter Kategori", kategori_list, default=kategori_list)
else:
    selected_kategori = []

# Apply filter
filtered_df = df[df["Hari"].isin(selected_hari)]
if "Kategori" in df.columns:
    filtered_df = filtered_df[filtered_df["Kategori"].isin(selected_kategori)]

st.sidebar.markdown("---")

# Download data
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="⬇️ Download Data (CSV)",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

# =========================
# KPI SECTION
# =========================
st.header("📌 Ringkasan (KPI)")

total_sales = filtered_df["Penjualan"].sum()
total_visitors = filtered_df["Pengunjung"].sum()
avg_sales = filtered_df["Penjualan"].mean()
avg_visitors = filtered_df["Pengunjung"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Penjualan", f"{total_sales}")
col2.metric("👥 Total Pengunjung", f"{total_visitors}")
col3.metric("📈 Rata-rata Penjualan", f"{avg_sales:.1f}")
col4.metric("📊 Rata-rata Pengunjung", f"{avg_visitors:.1f}")

st.markdown("---")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Visualisasi", "📋 Data", "💻 Info & Code"])

# =========================
# TAB 1: VISUALIZATION (MATPLOTLIB)
# =========================
with tab1:
    st.subheader("📈 Trend Penjualan & Pengunjung")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered_df["Hari"], filtered_df["Penjualan"], marker="o", label="Penjualan")
    ax.plot(filtered_df["Hari"], filtered_df["Pengunjung"], marker="o", label="Pengunjung")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jumlah")
    ax.set_title("Trend Penjualan & Pengunjung")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📊 Bar Chart Penjualan")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(filtered_df["Hari"], filtered_df["Penjualan"])
        ax2.set_title("Penjualan per Hari")
        ax2.set_xlabel("Hari")
        ax2.set_ylabel("Penjualan")
        ax2.grid(True, axis="y", alpha=0.3)
        st.pyplot(fig2)

    with colB:
        if "Kategori" in df.columns:
            st.subheader("🥧 Pie Chart Penjualan per Kategori")
            pie_df = filtered_df.groupby("Kategori")["Penjualan"].sum()

            fig3, ax3 = plt.subplots(figsize=(6, 4))
            ax3.pie(pie_df, labels=pie_df.index, autopct="%1.1f%%", startangle=90)
            ax3.set_title("Distribusi Penjualan per Kategori")
            st.pyplot(fig3)
        else:
            st.info("Kolom 'Kategori' tidak tersedia, Pie chart tidak ditampilkan.")

# =========================
# TAB 2: DATA DISPLAY
# =========================
with tab2:
    st.subheader("📌 DataFrame (Interactive)")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📌 Table (Static)")
    st.table(filtered_df)

    with st.expander("🔍 Statistik Data"):
        st.write(filtered_df.describe())

# =========================
# TAB 3: INFO & CODE
# =========================
with tab3:
    st.subheader("🧠 Penjelasan")
    st.write("""
    Dashboard ini menggunakan:
    - **Streamlit** untuk UI web
    - **Pandas** untuk manipulasi data
    - **Matplotlib** untuk chart
    - Sidebar untuk filter dan upload file
    """)

    st.subheader("💻 Contoh Potongan Kode")
    st.code("""
    fig, ax = plt.subplots()
    ax.plot(df["Hari"], df["Penjualan"], marker="o")
    ax.set_title("Trend Penjualan")
    st.pyplot(fig)
    """, language="python")
