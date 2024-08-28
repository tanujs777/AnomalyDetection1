import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path=path, mime_type=mime_type)
    st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

st.set_page_config(page_title="Power BI Report Anomaly Detector")
st.title("Power BI Report Anomaly Detector")
st.subheader("Upload your Power BI report to detect anomalies")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Power BI Report', use_column_width=True)
    
    temp_file_path = f"temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Upload the image to Google Gemini and get the file URI
    file = upload_to_gemini(temp_file_path, mime_type="image/jpeg")
    
    # Define generation configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Create the generative model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    # Start a chat session with the image
    chat_session = model.start_chat(history=[
        {
            "role": "user",
            "parts": [file, "Can you detect any anomalies in this image?\n"]
        }
    ])

    # Send a follow-up message
    response = chat_session.send_message("Please provide a detailed analysis of any detected anomalies.")
    
    # Display the response
    st.write("Anomaly Detection Result:")
    st.write(response.text)
    
    # Clean up temporary file
    os.remove(temp_file_path)
