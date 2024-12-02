import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Modelni yuklash
try:
    model = pickle.load(open("model.pkl", "rb"))
    st.success("Model muvaffaqiyatli yuklandi!")
except Exception as e:
    st.error(f"Modelni yuklashda xatolik: {e}")

# LabelEncoder ni yaratish
encoder = LabelEncoder()
# Ilgari o'rgatilgan encoderni yuklash
try:
    with open("encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
except Exception as e:
    st.error(f"LabelEncoderni yuklashda xatolik: {e}")

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

# Ma'lumotlarni DataFrame formatiga o‘tkazish
if st.button("Bashorat qilish"):
    try:
        # Tranzaksiya turini raqamga almashtirish
        if transaction_type not in transaction_type_map:
            st.error("Tranzaksiya turi noto‘g‘ri!")
        else:
            # NameDest ni kodlash
            nameDest_encoded = encoder.transform([nameDest])[0] if nameDest in encoder.classes_ else -1
            
            # Tranzaksiya ma'lumotlari
            input_data = pd.DataFrame({
                'step': [step],
                'type': [transaction_type_map[transaction_type]],
                'amount': [amount],
                'oldbalanceOrg': [oldbalanceOrg],
                'newbalanceOrig': [newbalanceOrig],
                'nameDest': [nameDest_encoded],
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
    except ValueError as e:
        st.error(f"Kiritilgan ma'lumotda xatolik: {e}")
