import numpy as np
import pandas as pd
import streamlit as st  
from sklearn.preprocessing import LabelEncoder
import pickle  

# Modelni yuklash
model_path = "model.pkl"  # Yuklangan fayl bilan bir xil joyda saqlang
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error(f"Model fayli topilmadi: {model_path}. Iltimos, faylni to'g'ri joylashtiring.")
    st.stop()
except Exception as e:
    st.error(f"Modelni yuklashda xato: {str(e)}")
    st.stop()

# Streamlit interfeysini bezash
st.set_page_config(page_title="Bemorga Dori Tafsiya", page_icon="💊", layout="centered")
st.markdown(
    """
    <style>
    /* Umumiy fon uchun gradient */
    .stApp {
        background: linear-gradient(to right, #dae2f8, #d6a4a4);
        color: #2C3E50;
    }

    /* Asosiy panel uchun soyalar va stil */
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        max-width: 700px;
    }

    /* Sarlavha va subtitrlar */
    h1 {
        color: #2C3E50;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 3rem;
        margin-bottom: 20px;
    }
    
    .subheader {
        font-family: 'Verdana', sans-serif;
        color: #34495E;
        margin-bottom: 10px;
    }

    /* Tugmalar uchun maxsus uslublar */
    .stButton>button {
        background-color: #3498DB !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 15px 25px !important;
        font-size: 16px !important;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #2980B9 !important;
        transform: scale(1.05);
    }

    /* Quti va radio tugmalar uchun uslub */
    .stNumberInput, .stRadio, .stSelectbox {
        margin-bottom: 20px;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Bashorat natijasini chiroyli qilish */
    .st-alert-success {
        background-color: #D4EDDA;
        border-color: #C3E6CB;
        color: #155724;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sarlavha va tavsif
st.title("💊 Bemorga Dori Tafsiya qilish")
st.markdown("<p style='text-align: center;'>Ma'lumotlaringizni kiriting va sizga mos dori tavsiya etamiz.</p>", unsafe_allow_html=True)

# Yoshni kiritish
st.subheader("1. Yoshingizni kiriting:")
Age = st.number_input("Yosh:", min_value=0, max_value=120, step=1)

# Jinsni tanlash
st.subheader("2. Jinsingizni tanlang:")
gender = st.radio("Jins:", ["Erkak", "Ayol"])

# Xolesterin darajasini tanlash
st.subheader("3. Xolesterin darajasini tanlang:")
cholesterol_level = st.selectbox("Xolesterin darajasi:", ["Normal", "High"])

# Qon bosimini tanlash
st.subheader("4. Qon bosimi darajasini tanlang:")
blood_pressure = st.selectbox("Qon bosimi:", ["Normal", "High"])

# Natriyni kaliyga nisbati
st.subheader("5. Natriyni kaliyga nisbati:")
na_to_k = st.number_input("Natriy/kaliy nisbati (na_to_k):", format="%.2f")

# Label Encoder
label_encoder = LabelEncoder()

# Jins, xolesterin darajasi va qon bosimini intga o'tkazish
gender_arr = label_encoder.fit_transform(np.array([gender]))
cholesterol_arr = label_encoder.fit_transform(np.array([cholesterol_level]))
blood_pressure_arr = label_encoder.fit_transform(np.array([blood_pressure]))



# Kiritilgan ma'lumotlarni massiv ko'rinishiga o'tkazish
features = np.array([[Age, gender_arr[0], cholesterol_arr[0], blood_pressure_arr[0], na_to_k]])

# Modelga kiritilgan ma'lumotlarni uzatamiz
if st.button("Dori tavsiya qilish"):
    if len(features[0]) == 5:  
        predect1 = decision_tree_model.predict(features)
        st.success(f"Bashorat: **{predect1[0]}**")
    else:
        st.error("Kiritilgan ma'lumotlar to'g'ri emas.")
