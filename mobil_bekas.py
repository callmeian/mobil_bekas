import streamlit as st
import pandas as pd
import pickle
import gzip

# Load pipeline yang sudah dikompresi
with gzip.open("model_pipeline.pkl.gz", "rb") as f:
    pipeline = pickle.load(f)

# Load dataset
df = pd.read_csv("used_car_ford_mercedes.csv")

# Judul
st.set_page_config(page_title="Prediksi Harga Mobil Bekas", layout="wide")
st.title("🚗 Prediksi Harga Mobil Bekas Ford & Mercedes")
st.markdown("Masukkan detail mobil di bawah untuk mendapatkan estimasi harga:")

# Dua kolom: input dan output
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔧 Input Mobil")

    # Opsi kategori
    model_options = sorted(df['model'].unique())
    transmission_options = sorted(df['transmission'].unique())
    fuel_options = sorted(df['fuelType'].unique())

    # Input dari pengguna
    user_input = {
        'model': st.selectbox('Model', model_options),
        'year': st.slider('Tahun', int(df['year'].min()), int(df['year'].max()), 2020),
        
        'transmission': st.selectbox('Transmisi', transmission_options),
        
        'mileage': st.number_input(
            f'Jarak Tempuh (Mileage)\n(min: {df["mileage"].min():,} | max: {df["mileage"].max():,})',
            min_value=1,
            max_value=323000,
            value=int(df['mileage'].median())
        ),
        
        'fuelType': st.selectbox('Tipe Bahan Bakar', fuel_options),
        
        'tax': st.number_input(
            f'Pajak (£)\n(min: {df["tax"].min()} | max: {df["tax"].max()})',
            min_value=0,
            max_value=580,
            value=int(df['tax'].median())
        ),
        
        'mpg': st.number_input(
            f'Mil per Galon (MPG)\n(min: {df["mpg"].min():.1f} | max: {df["mpg"].max():.1f})',
            min_value=18.9,
            max_value=188.3,
            value=float(df['mpg'].median())
        ),
        
        'engineSize': st.number_input(
            f'Ukuran Mesin (L)\n(min: {df["engineSize"].min():.1f} | max: {df["engineSize"].max():.1f})',
            min_value=0.0,
            max_value=6.3,
            value=float(df['engineSize'].median())
        ),
    }

    input_df = pd.DataFrame([user_input])

with col2:
    st.subheader("📊 Hasil Prediksi")

    if st.button("🎯 Prediksi Harga"):
        price_gbp = pipeline.predict(input_df)[0]

        st.balloons()

        st.success(f"💷 Estimasi Harga Mobil: **£{int(price_gbp):,}**")
