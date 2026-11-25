🎬 ScenIt – AI Movie & Scene Identifier

"ScenIt" är en interaktiv webbapplikation byggd i Python och Streamlit som fungerar som ett "Shazam för film". Genom att använda multimodal AI (Computer Vision) analyserar appen skärmbilder eller korta videoklipp för att identifiera vilken film eller TV-serie scenen kommer ifrån.

✨ Funktioner
📸 Bild- & Videoanalys: Stöd för att ladda upp både skärmdumpar (PNG/JPG) och korta videoklipp (MP4/MOV).
🛡️ Inbyggd Fallback-logik: Automatisk växling mellan olika Gemini-modeller vid hög serverbelastning (503-hantering) för hög driftsäkerhet.
🕒 Sessionshistorik: Sparar tidigare identifierade scener i ett mörkt, användarvänligt neon-gränssnitt.

🛠️ Teknikstack
Språk: Python
Frontend / UI: Streamlit & Custom CSS (Dark Mode)
AI-motor: Google Gemini API (`google-genai`)
Bildhantering: Pillow (PIL)

🚀 Kom igång lokalt
1. Klona detta repository: `git clone https://github.com/AnneMarie1976/ScenIt-AI.git`
2. Installera beroenden: `pip install -r requirements.txt`
3. Lägg in din egen Google AI Studio API-nyckel i `app_scenit.py`.
4. Starta appen: `streamlit run app_scenit.py`
