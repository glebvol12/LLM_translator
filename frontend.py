import streamlit as st
import requests
import time

# --- Настройка страницы ---
st.set_page_config(
    page_title="LLM Translator",
    layout="wide"
)

# --- Стили CSS ---
def load_css():
    st.markdown("""
    <style>
        .header {
            color: #2e7d32;
            text-align: center;
            font-size: 2.5em !important;
            margin-bottom: 0.5em;
        }
        .language-selector {
            margin-bottom: 1.5em;
        }
        .text-box {
            margin-bottom: 1em;
        }
        .translate-btn {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold;
            border: none;
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            margin-top: 1em;
        }
        .translation-info {
            margin-top: -15px;
            margin-bottom: 15px;
            font-size: 0.8em;
            color: #666;
            text-align: right;
        }
        .model-footer {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 1em;
        }
        .model-badge {
            background-color: #673AB7;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

#языки
LANGUAGES = {
    "English": "English",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Russian": "Russian",
    "Chinese": "Chinese",
    "Japanese": "Japanese"
}

#Интерфейс 
st.markdown('<p class="header"></p>', unsafe_allow_html=True)


col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox(
        "From",
        options=list(LANGUAGES.keys()),
        key="source_lang",
        index=0
    )

with col2:
    target_lang = st.selectbox(
        "To",
        options=list(LANGUAGES.keys()),
        key="target_lang",
        index=4  # Russian по умолчанию
    )


source_text = st.text_area(
    "Text to translate",
    height=200,
    placeholder="Type or paste your text here...",
    key="input_text"
)


if st.button("Translate", key="translate_btn", use_container_width=True):
    if source_text:
        start_time = time.time()
        with st.spinner("Translating..."):
            try:
                response = requests.post(
                    "http://localhost:5000/translate",
                    json={
                        "text": source_text,
                        "source_language": LANGUAGES[source_lang],
                        "target_language": LANGUAGES[target_lang]
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    translation_time = round(time.time() - start_time, 2)
                    
                    # Время перевода (синяя область)
                    st.markdown(f"""
                    <div class="translation-info">
                        Translated in {translation_time}s
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.text_area(
                        "Translation",
                        value=result["translated_text"],
                        height=200,
                        key="output_text"
                    )
                else:
                    st.error(f"Translation error: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
    else:
        st.warning("Please enter some text to translate")


st.markdown("---")
st.markdown("""
<div class="model-footer">
    Powered by Llama 4 Scout (17Bx16E) via Together AI
</div>
""", unsafe_allow_html=True)