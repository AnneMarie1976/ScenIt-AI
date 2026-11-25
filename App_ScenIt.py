import streamlit as st
from google import genai
from PIL import Image
import io
import os
import tempfile
import time

# 1. API-nyckel (Klistra in din riktiga nyckel här utan svenska tecken)
API_KEY = "DIN_GEMINI_API_NYCKEL_HÄR"
client = genai.Client(api_key=API_KEY)

# 2. Sidinställningar
st.set_page_config(page_title="ScenIt", page_icon="🎬", layout="centered")

# Initiera historik-minnet i sessionen om det inte redan finns
if "history" not in st.session_state:
    st.session_state.history = []

# 3. Egen CSS för din mörka neon-design
st.markdown("""
<style>
    .stApp { background-color: #0B0B0E; color: #FFFFFF; }
    .neon-circle {
        width: 150px; height: 150px; border-radius: 50%;
        background-color: #A855F7; margin: 15px auto;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        box-shadow: 0 0 25px #A855F7; font-weight: bold; font-size: 18px;
        letter-spacing: 2px; color: white; text-align: center;
    }
    .stFileUploader {
        background-color: #16161F; padding: 15px; border-radius: 12px; border: 1px solid #272732;
    }
    .stButton>button {
        background-color: #A855F7; color: white; border-radius: 8px;
        border: none; width: 100%; font-weight: bold; padding: 10px;
    }
    .history-card {
        background-color: #16161F; padding: 15px; border-radius: 10px;
        border-left: 4px solid #A855F7; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- GRÄNSSNITTET ---
st.markdown("<h1 style='text-align: center; letter-spacing: 2px;'>🎬 ScenIt</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="neon-circle">
    <span>⚡</span>
    <span>AI SCAN</span>
    <span>⚡</span>
</div>
<p style='text-align: center; color: #9CA3AF; font-size: 14px;'>Välj om du vill skanna en skärmbild eller ett kort videoklipp</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Prompt på ren engelska (undviker ASCII-felet) som ber AI:n svara på svenska
SAFE_PROMPT = """
Identify the movie or TV show in this media. Respond cleanly in Swedish using this exact format:
- **Titel:** [Name] ([Year])
- **Skadespelare:** [Names]
- **Scen:** [Short description]
"""

# Smart hjälpfunktion som automatiskt testar reservmodeller vid 503-fel
def analyze_with_fallback(content_list):
    models_to_try = [
        'gemini-3.8-flash', 
        'gemini-3.6-flash',
        'gemini-3.1-flash-lite', 
        'gemini-3.5-flash-lite'
    ]
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=content_list
            )
            return response.text
        except Exception as e:
            last_error = e
            error_str = str(e)
            # Hoppa vidare till nästa modell både vid överbelastning (503) och om ett namn saknas (404)
            if "503" in error_str or "UNAVAILABLE" in error_str or "404" in error_str:
                time.sleep(1.5) # Väntar 1,5 sekund innan nästa försök
                continue
            else:
                raise e
    raise Exception(f"Alla AI-modeller har tillfälligt hög belastning. Vänta 30 sekunder och klicka igen. ({last_error})")

# --- PUNKT 1: FLIKAR FÖR BÅDE BILD OCH VIDEO ---
tab1, tab2 = st.tabs(["📸 Skärmbild (Bild)", "🎬 Videoklipp (Max 5 sek)"])

# FLIK 1: BILDUPPLADDNING
with tab1:
    uploaded_img = st.file_uploader("Ladda upp skärmbild (PNG, JPG)", type=["png", "jpg", "jpeg"], key="img_up")
    if uploaded_img is not None:
        img = Image.open(io.BytesIO(uploaded_img.read()))
        st.image(img, use_container_width=True)
        
        if st.button("🪄 Analysera Bild", key="btn_img"):
            with st.spinner("AI-motorn skannar bildrutan..."):
                try:
                    result_text = analyze_with_fallback([img, SAFE_PROMPT])
                    st.success("Träff!")
                    st.markdown(result_text)
                    st.session_state.history.insert(0, {"typ": "📸 Bild", "resultat": result_text})
                except Exception as e:
                    st.error(f"Fel: {e}")

# FLIK 2: VIDEOUPPLADDNING (5 SEKUNDER)
with tab2:
    uploaded_vid = st.file_uploader("Ladda upp videoklipp (MP4, MOV)", type=["mp4", "mov"], key="vid_up")
    if uploaded_vid is not None:
        st.video(uploaded_vid)
        
        if st.button("🪄 Analysera Videoklipp", key="btn_vid"):
            with st.spinner("Laddar upp och analyserar videon med AI (kan ta 5-10 sek)..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                        tmp_file.write(uploaded_vid.read())
                        tmp_path = tmp_file.name
                    
                    video_file = client.files.upload(file=tmp_path)
                    result_text = analyze_with_fallback([video_file, SAFE_PROMPT])
                    os.remove(tmp_path)
                    
                    st.success("Träff!")
                    st.markdown(result_text)
                    st.session_state.history.insert(0, {"typ": "🎬 Video", "resultat": result_text})
                except Exception as e:
                    st.error(f"Fel vid videoanalys: {e}")

# --- PUNKT 2: HISTORIK-SEKTION LÄNGST NER ---
st.markdown("---")
st.subheader("🕒 Tidigare Skanningar (Historik)")

if len(st.session_state.history) == 0:
    st.caption("Inga skanningar gjorda än under den här sessionen.")
else:
    for item in st.session_state.history:
        st.markdown(f"""
        <div class="history-card">
            <small style="color: #A855F7; font-weight: bold;">{item['typ']}</small><br>
            {item['resultat']}
        </div>
        """, unsafe_allow_html=True)