import streamlit as st
import pandas as pd
import pickle
import gzip  

# Load pipeline yang sudah dikompresi
with gzip.open("model_pipeline.pkl.gz", "rb") as f:  
    pipeline = pickle.load(f)

df = pd.read_csv("used_car_ford_mercedes.csv")

# Konstanta konversi
GBP_TO_IDR = 20000  # 1 GBP ≈ 20.000 IDR
GBP_TO_EUR = 1.17   # 1 GBP ≈ 1.17 EUR

# Judul
st.set_page_config(page_title="Prediksi Harga Mobil Bekas", layout="wide")
st.title("🚗 Prediksi Harga Mobil Bekas Ford & Mercedes")
st.markdown("Masukkan detail mobil di bawah untuk mendapatkan estimasi harga:")

# Dua kolom: input dan output
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔧 Input Mobil")
    
    model_options = sorted(df['model'].unique())
    transmission_options = sorted(df['transmission'].unique())
    fuel_options = sorted(df['fuelType'].unique())

    user_input = {
        'model': st.selectbox('Model', model_options),
        'year': st.slider('Tahun', int(df['year'].min()), int(df['year'].max()), 2020),
        'transmission': st.selectbox('Transmisi', transmission_options),
        'mileage': st.number_input('Jarak Tempuh (Mileage)', min_value=0, value=int(df['mileage'].median())),
        'fuelType': st.selectbox('Tipe Bahan Bakar', fuel_options),
        'tax': st.number_input('Pajak (£)', min_value=0, value=int(df['tax'].median())),
        'mpg': st.number_input('Mil per Galon (MPG)', min_value=0.0, value=float(df['mpg'].median())),
        'engineSize': st.number_input('Ukuran Mesin (L)', min_value=0.0, value=float(df['engineSize'].median())),
    }

    input_df = pd.DataFrame([user_input])

with col2:
    st.subheader("📊 Hasil Prediksi")

    if st.button("🎯 Prediksi Harga"):
        price_gbp = pipeline.predict(input_df)[0]
        price_idr = price_gbp * GBP_TO_IDR

        st.balloons()  # 🎈 efek animasi

        st.success(f"💷 Estimasi Harga Mobil: **£{int(price_gbp):,}**")
        st.warning(f"💰 Dalam Rupiah (IDR): **Rp {int(price_idr):,}**")