import streamlit as st
from google import genai
from PIL import Image
import io

# Core Demo Version - ScenIt AI
# Full version with video support, custom UI, and fallback logic is kept private.

API_KEY = "YOUR_API_KEY_HERE"
client = genai.Client(api_key=API_KEY)

st.title("🎬 ScenIt – Core AI Demo")
st.write("Upload a screenshot to identify the movie or TV show.")

uploaded_img = st.file_uploader("Choose an image (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_img is not None:
    img = Image.open(io.BytesIO(uploaded_img.read()))
    st.image(img, use_container_width=True)
    
    if st.button("Analyze Scene"):
        with st.spinner("Analyzing..."):
            try:
                prompt = "Identify the movie or TV show in this image. Return Title, Year, and a short summary."
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=[img, prompt]
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
