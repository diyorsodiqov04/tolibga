import streamlit as st
import pickle
import numpy as np

# Modelni yuklash
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit ilovasi
def main():
    # Chiroyli sarlavha va tushuntirish qo'shish
    st.markdown("""
    <div style="background-color: lightblue; padding: 20px; text-align: center;">
        <h1 style="color: #2F4F4F;">Mahsulot sotuvini bashorat qilish</h1>
        <p style="font-size: 18px; color: #5F6368;">Mahsulot haqida ma'lumot kiriting va uning sotilishi haqida bashorat oling.</p>
    </div>
    """, unsafe_allow_html=True)

    # Foydalanuvchidan ma'lumot olish
    stars = st.number_input("Yulduz (1 to 5)", min_value=1, max_value=5, step=1, help="Mahsulotning reytingi")
    reviews = st.number_input("Ko'rish sonlari", min_value=0, step=1, help="Mahsulotga qilingan sharhlar soni")
    price = st.number_input("Narxi: ($)", min_value=0.0, step=0.01, help="Mahsulotning narxi")
    is_best_seller = st.selectbox("Bu mahsulot ko'p sotilganmi(o'tkan oyda)", ("Yes", "No"))

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

    # Modelga ma'lumot yuborish va bashorat qilish
    if st.button("Bashorat qilish"):
        # 'Yes'ni 1, 'No'ni 0 ga aylantirish
        is_best_seller = 1 if is_best_seller == "Yes" else 0
        
        input_data = np.array([[stars, reviews, price, is_best_seller]])
        prediction = model.predict(input_data)

        # Natijani chiqarish
        st.markdown(f"""
        <div style="background-color: lightgreen; padding: 20px; text-align: center; border-radius: 10px;">
            <h3 style="color: #2F4F4F;">Bashorat natijasi:</h3>
            <p style="font-size: 20px; font-weight: bold;">{prediction[0]}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
