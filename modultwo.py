import streamlit as st
import pandas as pd
import pickle

# Modelni yuklash
model = pickle.load(open("my_model.pkl", "rb"))

# Web sahifa uchun sarlavha
st.markdown("""
<div style="background-color: #f1f1f1; padding: 30px; text-align: center; border-radius: 10px;">
    <h1 style="color: #2F4F4F; font-family: Arial, sans-serif;">Firibgarlikni Aniqlash Bashorati</h1>
    <p style="font-size: 18px; color: #5F6368; font-family: Arial, sans-serif;">Tranzaksiya tafsilotlarini kiriting va uning firibgarlik yoki qonuniy ekanligini aniqlang.</p>
</div>
""", unsafe_allow_html=True)


st.header("Tranzaksiya Tafsilotlarini Kiriting")


step = st.number_input("Step (Tranzaksiya vaqti)", min_value=0, max_value=744, step=1)
transaction_type = st.selectbox("Tranzaksiya turi", ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])
amount = st.number_input("Summasi", min_value=0.0, step=0.01)
oldbalanceOrg = st.number_input("Jo‘natuvchi hisobining eski balansi", min_value=0.0, step=0.01)
newbalanceOrig = st.number_input("Jo‘natuvchi hisobining yangi balansi", min_value=0.0, step=0.01)
nameDest = st.text_input("Qabul qiluvchi nomi (masalan, C12345)")
oldbalanceDest = st.number_input("Qabul qiluvchi hisobining eski balansi", min_value=0.0, step=0.01)
isFlaggedFraud = st.selectbox("Firibgarlik sifatida belgilanganmi?", [0, 1])


st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        width: 100%;
        font-family: Arial, sans-serif;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox>div, .stNumberInput>div>div>input, .stTextInput>div>div>input {
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

if st.button("Bashorat qilish"):
   
    input_data = pd.DataFrame({
        'step': [step],
        'type': [transaction_type],
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'nameDest': [nameDest],
        'oldbalanceDest': [oldbalanceDest],
        'isFlaggedFraud': [isFlaggedFraud]
    })
    
  
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.markdown("""
        <div style="background-color: #f8d7da; padding: 20px; text-align: center; border-radius: 10px;">
            <h3 style="color: #721c24;">Firibgarlik tranzaksiyasi aniqlangan!</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #d4edda; padding: 20px; text-align: center; border-radius: 10px;">
            <h3 style="color: #155724;">Tranzaksiya qonuniy!</h3>
        </div>
        """, unsafe_allow_html=True)
