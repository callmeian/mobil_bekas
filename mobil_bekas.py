import streamlit as st
import pandas as pd
import pickle

# Load model dan kolom fitur
with open("rf_model.pkl", "rb") as file:
    model, feature_columns = pickle.load(file)

st.title("🚗 Prediksi Harga Mobil Bekas")

st.markdown("Masukkan detail mobil untuk memprediksi harganya:")

# Input fitur dari user
user_input = {}
for col in feature_columns:
    if "year" in col.lower():
        user_input[col] = st.number_input(f"{col}", min_value=1980, max_value=2025, value=2018)
    elif "mileage" in col.lower():
        user_input[col] = st.number_input(f"{col}", min_value=0, value=30000)
    elif "tax" in col.lower():
        user_input[col] = st.number_input(f"{col}", min_value=0, value=150)
    elif "engine" in col.lower():
        user_input[col] = st.number_input(f"{col}", min_value=0.0, value=1.6)
    elif "mpg" in col.lower():
        user_input[col] = st.number_input(f"{col}", min_value=0.0, value=40.0)
    elif "transmission" in col.lower() or "fuel" in col.lower() or "model" in col.lower() or "brand" in col.lower():
        user_input[col] = st.text_input(f"{col}", value="manual")  # ganti sesuai label encoding
    else:
        user_input[col] = st.text_input(f"{col}", value="")

# Convert input ke DataFrame
input_df = pd.DataFrame([user_input])

# Sesuaikan kolom dengan training set
input_df = input_df.reindex(columns=feature_columns, fill_value=0)

# Prediksi
if st.button("Prediksi"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"💰 Perkiraan Harga Mobil: £{int(prediction):,}")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat prediksi: {e}")

