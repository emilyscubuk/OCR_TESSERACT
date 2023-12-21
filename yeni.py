import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import io


# CSS ile arka plan rengini ayarla

st.markdown(
    """
    <style>
    .stApp {
        background-color:#C8A2C8;  
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p style="background-color: #CCB800; color: white; font-size: 30px; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);">Görüntü İşleme ve OCR Uygulaması </p>', unsafe_allow_html=True)


# Custom CSS to change the background color of the file uploader widget
st.markdown(
    """
    <style>
    div.stFileUploader {
        background-color: #C8A2C8;  /* Example: Acid Lila color */
        border-radius: 10px;  /* Optional: for rounded corners */
        padding: 10px;  /* Optional: for spacing */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# File uploader widget
uploaded_file = st.file_uploader("Bir görüntü yükleyin", type=["png", "jpg", "jpeg"])

# Custom CSS to change the sidebar background color to yellow
st.markdown(
    """
    <style>
    .css-1lcbmhc {
        background-color: #FFFF00;  /* Sarı renk */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar içeriği
with st.sidebar:
    with st.expander("Seçenekler", expanded=True):
        option = st.selectbox(
            'Hangi işlemi yapmak istersiniz?',
            ('OCR İşlemi', 'Görüntü Üzerinde Bounding Box', 'Oneamz Yazısından Sonra Gelen Sayı')
        )
    st.sidebar.info('Bu uygulama, ONEAMZ kargo kod numarasını bulmak için oluşturulmuştur')

    image = Image.open('ocr.png')
    st.image(image)
        
if uploaded_file is not None:
    # Yüklenen dosyayı oku ve görsel olarak göster
    image_stream = io.BytesIO(uploaded_file.getvalue())
    image = Image.open(image_stream)
    st.image(image, caption='Yüklenen Fotoğraf', width=400)


# OCR İşlemi
def perform_ocr(image_data):
    text = pytesseract.image_to_string(image_data)
    return text

# Görüntü Üzerinde Bounding Box
def bounding_box(image_data):
    image_np = np.array(image_data)
    d = pytesseract.image_to_data(image_np, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Yeşil renk
    return image_np



# Önekten Sonra Gelen Sayıyı Çıkarma
def extract_number_with_prefix(image_data, prefixes):
    text = pytesseract.image_to_string(image_data)
    for prefix in prefixes:
        if prefix in text:
            index = text.find(prefix) + len(prefix)
            after_prefix = text[index:]
            number = ''
            for char in after_prefix:
                if char.isdigit():
                    number += char
                elif number:
                    break
            if number:
                return number
    return "Belirtilen önek bulunamadı."

# Yüklenen dosyayı işlemek
if uploaded_file is not None:
    image_stream = io.BytesIO(uploaded_file.getvalue())
    image = Image.open(image_stream)

    if option == 'OCR İşlemi':
        result_text = perform_ocr(image)
        st.write(result_text)
    elif option == 'Görüntü Üzerinde Bounding Box':
        result_image = bounding_box(image)
        st.image(result_image, caption='İşlenmiş Görüntü', width=400)
    elif option == 'Oneamz Yazısından Sonra Gelen Sayı':
        prefixes_to_search = ['ONEAMZ~','ONE RN', '# GNEANZ—', '# ONEAM2-', '# ONEAM?-', '# ‘ONEAMZ —', '# ONEANZ-', 'PONEAM?', 'ONEAMZ —', 'AVE # ONEAMZ-', '# ONEAMZ', 'ONEAMZ-', 'ONEAMZ—']
        extracted_number = extract_number_with_prefix(image, prefixes_to_search)
        st.write(f"Çıkarılan Numara: {extracted_number}")

else:
    st.write("Lütfen bir görüntü yükleyin.")
    
    
st.subheader("Geri Bildirim")
feedback = st.text_area("Uygulama hakkında yorumlarınızı ve önerilerinizi buraya yazabilirsiniz:")
if st.button("Gönder"):
    st.write("Geri bildiriminiz için teşekkürler!")

    