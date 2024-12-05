import streamlit as st
import pandas as pd
import pickle

# Modelni yuklash
model = pickle.load(open("my_model.pkl", "rb"))

# Sahifaga HTML va CSS qo'shish
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .main-title {
            text-align: center;
            color: #2F4F4F;
            font-size: 36px;
            margin-top: 20px;
        }
        .sub-title {
            text-align: center;
            color: #5F6368;
            font-size: 18px;
        }
        .input-section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .result-section {
            background-color: #e7f5e6;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #2F4F4F;
        }
        .error-section {
            background-color: #f8d7da;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #842029;
        }
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

# HTML sarlavhalar
st.markdown('<div class="main-title">Firibgarlikni Aniqlash Bashorati</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Tranzaksiya tafsilotlarini kiriting va bashorat oling.</div>', unsafe_allow_html=True)

# Kiritish bo'limi


# Kiritish maydonlari
step = st.number_input("Step (Tranzaksiya vaqti)", min_value=0, max_value=744, step=1)
transaction_type = st.selectbox("Tranzaksiya turi", ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'])
amount = st.number_input("Summasi", min_value=0.0, step=0.01)
oldbalanceOrg = st.number_input("Jo‘natuvchi hisobining eski balansi", min_value=0.0, step=0.01)
newbalanceOrig = st.number_input("Jo‘natuvchi hisobining yangi balansi", min_value=0.0, step=0.01)
oldbalanceDest = st.number_input("Qabul qiluvchi hisobining eski balansi", min_value=0.0, step=0.01)
isFlaggedFraud = st.selectbox("Firibgarlik sifatida belgilanganmi?", [0, 1])

# Tranzaksiya turini raqamga o‘tkazish
transaction_type_map = {
    'CASH_IN': 1,
    'CASH_OUT': 5,
    'DEBIT': 2,
    'PAYMENT': 3,
    'TRANSFER': 4
}

st.markdown('</div>', unsafe_allow_html=True)  # Input section div tugashi

if st.button("Bashorat qilish"):
    if transaction_type not in transaction_type_map:
        st.markdown('<div class="error-section">Tranzaksiya turi noto‘g‘ri!</div>', unsafe_allow_html=True)
    else:
        # Tranzaksiya ma'lumotlari
        input_data = pd.DataFrame({
            'step': [step],
            'type': [transaction_type_map[transaction_type]],
            'amount': [amount],
            'oldbalanceOrg': [oldbalanceOrg],
            'newbalanceOrig': [newbalanceOrig],
            'oldbalanceDest': [oldbalanceDest],
            'isFlaggedFraud': [isFlaggedFraud]
        })

        # Model yordamida bashorat qilish
        prediction = model.predict(input_data)

        # Natijani chiqarish
        if prediction[0] == 1:
            st.markdown('<div class="error-section">Firibgarlik tranzaksiyasi aniqlangan!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-section">Tranzaksiya qonuniy!</div>', unsafe_allow_html=True)
