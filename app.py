import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit app title and description
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
        image = Image.open(uploaded_file)  # Open the image with PIL
        st.image(image, caption='Uploaded Power BI Report', use_column_width=True)

        # Resize the image if needed
        resized_image = image.resize((500, 500))
        st.image(resized_image, caption='Resized Power BI Report', use_column_width=True)

        try:
            # Convert the image to base64
            encoded_image = encode_image(resized_image)

            # Create the model and send the image (assuming the API supports this)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro"
            )
            chat_session = model.start_chat(history=[])
            # Hypothetically sending the image
            response = chat_session.send_message(f"data:image/png;base64,{encoded_image}")
            
            response_text = response.json().get('response', 'No response found')

            st.write("Anomaly Detection Result:")
            st.text(response_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an image file.")
