import streamlit as st
import pandas as pd
import pickle

# Modelni yuklash
model = pickle.load(open("my_model.pkl", "rb"))

# Web sahifa uchun sarlavha
st.markdown("""
    <div style="background-color: lightblue; padding: 20px; text-align: center;">
        <h1 style="color: #2F4F4F;">Firibgarlikni Aniqlash Bashorati</h1>
        <p style="font-size: 18px; color: #5F6368;">Tranzaksiya tafsilotlarini kiriting va firibgarlikni aniqlash uchun bashorat oling.</p>
    </div>
""", unsafe_allow_html=True)

# Foydalanuvchi uchun ma'lumotlarni kiritish
st.header("Tranzaksiya Tafsilotlarini Kiriting")

# Kiritish maydonlari
step = st.number_input("Step (Tranzaksiya vaqti)", min_value=0, max_value=744, step=1)
transaction_type = st.selectbox("Tranzaksiya turi", ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])
amount = st.number_input("Summasi", min_value=0.0, step=0.01)
oldbalanceOrg = st.number_input("Jo‘natuvchi hisobining eski balansi", min_value=0.0, step=0.01)
newbalanceOrig = st.number_input("Jo‘natuvchi hisobining yangi balansi", min_value=0.0, step=0.01)
nameDest = st.text_input("Qabul qiluvchi nomi (masalan, C12345)")
oldbalanceDest = st.number_input("Qabul qiluvchi hisobining eski balansi", min_value=0.0, step=0.01)
isFlaggedFraud = st.selectbox("Firibgarlik sifatida belgilanganmi?", [0, 1])

# Tranzaksiya turini raqamga almashtirish
transaction_type_map = {
    'CASH_IN': 1,
    'CASH_OUT': 5,
    'DEBIT': 2,
    'PAYMENT': 3,
    'TRANSFER': 4
}

# CSS orqali butonni chiroyli qilish
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
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Ma'lumotlarni DataFrame formatiga o‘tkazish
if st.button("Bashorat qilish"):
    # Foydalanuvchi ma'lumotlarini DataFrame formatida tayyorlash
    input_data = pd.DataFrame({
        'step': [step],
        'type': [transaction_type_map[transaction_type]],  # Tranzaksiya turini raqamga almashtirish
        'amount': [amount],
        'oldbalanceOrg': [oldbalanceOrg],
        'newbalanceOrig': [newbalanceOrig],
        'nameDest': [nameDest],
        'oldbalanceDest': [oldbalanceDest],
        'isFlaggedFraud': [isFlaggedFraud]
    })
    
    # Model yordamida bashorat qilish
    prediction = model.predict(input_data)

    # Natijani ko‘rsatish
    if prediction[0] == 1:
        st.error("Firibgarlik tranzaksiyasi aniqlangan!")
    else:
        st.success("Tranzaksiya qonuniy!")
