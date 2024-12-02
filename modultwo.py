import pickle
import streamlit as st
from transformers import pipeline
import PyPDF2
from docx import Document

# Modelni yuklash
model = pickle.load(open('model.pkl', 'rb'))  # .pkl modelini yuklash
qa_model = pipeline("question-answering", model=model)

# Word faylini o'qish
def read_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# PDF faylini o'qish
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit interfeysi
def main():
    st.title("Savol-Javob Dasturi")
    st.write("Faylni yuklang va savollarni kiriting.")

    # Faylni yuklash
    uploaded_file = st.file_uploader("Faylni yuklang", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".docx"):
            context = read_docx(uploaded_file)
        elif uploaded_file.name.endswith(".pdf"):
            context = read_pdf(uploaded_file)
        else:
            st.error("Faqat .pdf yoki .docx fayllarini yuklashingiz mumkin!")
            return
        
        st.write("Fayl muvaffaqiyatli o'qildi!")

        # Nechta savol kerakligini so'rash
        num_questions = st.number_input("Nechta savol kerak?", min_value=1, max_value=5, value=1)

        for i in range(num_questions):
            question = st.text_input(f"Savol {i + 1}:")
            if question:
                answer = qa_model({'question': question, 'context': context})
                st.write(f"Javob: {answer['answer']}")

# Streamlit dasturini ishga tushirish
if __name__ == "__main__":
    main()
