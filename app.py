import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Power BI Report Anomaly Detector")
st.title("Power BI Report Anomaly Detector")
st.subheader("Upload your Power BI report to detect anomalies")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if st.button("Detect Anomalies"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file) 
        st.image(image, caption='Uploaded Power BI Report', use_column_width=True)

        resized_image = image.resize((500, 500))
        st.image(resized_image, caption='Resized Power BI Report', use_column_width=True)

        try:
            encoded_image = encode_image(resized_image)

            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro"
            )
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(f"data:image/png;base64,{encoded_image}")
            
            response_text = response.json().get('response', 'No response found')

            st.write("Anomaly Detection Result:")
            st.text(response_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an image file.")
