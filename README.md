🎬 ScenIt – AI Scene Identifier (Core Demo)

ScenIt is an interactive web application built in Python and Streamlit that acts as a "Shazam for movies." Using multimodal AI (Computer Vision), it analyzes screenshots to identify the movie or TV show.

🔒 Note on Code Visibility: This public repository contains a simplified core demo of the image-recognition logic for portfolio purposes. The full version—including custom dark-mode neon UI, short video clip analysis, session history, and multi-model fallback handling—is kept private.

✨ Demo Features
📸 Image Analysis: Upload screenshots (PNG/JPG) to identify movie titles, release years, and scene context.
⚡ Lightweight UI: Clean and fast web interface built with Streamlit.

🛠️ Tech Stack
Language: Python
Frontend / UI: Streamlit
AI Engine: Google Gemini API (`google-genai`)
Image Processing: Pillow (PIL)

🚀 Run Locally
1. Clone this repository: `git clone https://github.com/AnneMarie1976/ScenIt-AI.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your own Google AI Studio API key in `App_ScenIt.py`.
4. Start the app: `streamlit run App_ScenIt.py`
