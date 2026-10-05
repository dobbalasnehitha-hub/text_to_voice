
"""
Text to Voice (Text-to-Speech) App

Converts text into speech in multiple languages, including
Indian languages, using Google Text-to-Speech (gTTS).

Requirements:
    pip install streamlit gTTS

Run:
    streamlit run app.py
"""

from io import BytesIO

import streamlit as st
from gtts import gTTS


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Text to Voice",
    page_icon="🔊",
    layout="centered"
)


# ---------------------------------------------------------
# Supported Languages
# ---------------------------------------------------------

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Bengali": "bn",
    "Marathi": "mr",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
}


# ---------------------------------------------------------
# English Accents
# ---------------------------------------------------------

ACCENTS = {
    "Indian": "co.in",
    "American": "com",
    "British": "co.uk",
    "Australian": "com.au",
}


# ---------------------------------------------------------
# Sample Text
# ---------------------------------------------------------

SAMPLES = {
    "English": (
        "Hello! Welcome to my text to speech project. "
        "Have a great day."
    ),

    "Hindi": (
        "नमस्ते! मेरे टेक्स्ट टू स्पीच प्रोजेक्ट में "
        "आपका स्वागत है।"
    ),

    "Telugu": (
        "నమస్కారం! నా టెక్స్ట్ టు స్పీచ్ ప్రాజెక్ట్‌కు "
        "స్వాగతం."
    ),

    "Tamil": (
        "வணக்கம்! எனது உரையிலிருந்து பேச்சு திட்டத்திற்கு "
        "உங்களை வரவேற்கிறேன்."
    ),

    "Bengali": (
        "নমস্কার! আমার টেক্সট টু স্পিচ প্রজেক্টে "
        "আপনাকে স্বাগতম।"
    ),

    "Marathi": (
        "नमस्कार! माझ्या टेक्स्ट टू स्पीच प्रोजेक्टमध्ये "
        "तुमचे स्वागत आहे."
    ),

    "Kannada": (
        "ನಮಸ್ಕಾರ! ನನ್ನ ಟೆಕ್ಸ್ಟ್ ಟು ಸ್ಪೀಚ್ ಪ್ರಾಜೆಕ್ಟ್‌ಗೆ "
        "ಸ್ವಾಗತ."
    ),

    "Malayalam": (
        "നമസ്കാരം! എന്റെ ടെക്സ്റ്റ് ടു സ്പീച്ച് പ്രോജക്റ്റിലേക്ക് "
        "സ്വാഗതം."
    ),

    "Gujarati": (
        "નમસ્તે! મારા ટેક્સ્ટ ટુ સ્પીચ પ્રોજેક્ટમાં "
        "આપનું સ્વાગત છે."
    ),

    "Urdu": (
        "السلام علیکم! میرے ٹیکسٹ ٹو اسپیچ پروجیکٹ میں "
        "آپ کا خیر مقدم ہے۔"
    ),

    "French": (
        "Bonjour ! Bienvenue dans mon projet de synthèse "
        "vocale. Passez une excellente journée."
    ),

    "Spanish": (
        "¡Hola! Bienvenido a mi proyecto de texto a voz. "
        "Que tengas un buen día."
    ),

    "German": (
        "Hallo! Willkommen bei meinem Text-zu-Sprache-Projekt. "
        "Ich wünsche Ihnen einen schönen Tag."
    ),

    "Japanese": (
        "こんにちは！私のテキスト読み上げプロジェクトへ "
        "ようこそ。良い一日をお過ごしください。"
    ),
}


# ---------------------------------------------------------
# Text-to-Speech Function
# ---------------------------------------------------------

def synthesize(text: str, lang: str, tld: str = "com", slow: bool = False) -> bytes:
    """
    Convert text into MP3 audio using gTTS.

    For English, the selected TLD controls the accent.
    For other languages, the default Google TLD is used.
    """

    audio_buffer = BytesIO()

    # Use the selected accent only for English.
    if lang == "en":
        tts = gTTS(
            text=text,
            lang=lang,
            tld=tld,
            slow=slow
        )
    else:
        tts = gTTS(
            text=text,
            lang=lang,
            slow=slow
        )

    tts.write_to_fp(audio_buffer)

    return audio_buffer.getvalue()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.header("⚙️ Settings")

lang_name = st.sidebar.selectbox(
    "🌐 Language",
    list(LANGUAGES.keys())
)

# Accent selection is available only for English.
accent = "Indian"

if lang_name == "English":
    accent = st.sidebar.selectbox(
        "🗣️ English Accent",
        list(ACCENTS.keys())
    )

slow = st.sidebar.checkbox(
    "🐢 Slow speech"
)

st.sidebar.caption(
    "💡 Tip: Type the text in the same language you select."
)


# ---------------------------------------------------------
# Main Application
# ---------------------------------------------------------

st.title("🔊 Text to Voice")

st.write(
    "Type or upload text and convert it into speech "
    "that you can play and download."
)


# ---------------------------------------------------------
# Input Selection
# ---------------------------------------------------------

source = st.radio(
    "📥 Input type",
    ["Type text", "Upload .txt"],
    horizontal=True
)


# ---------------------------------------------------------
# Text Input
# ---------------------------------------------------------

if source == "Type text":

    text = st.text_area(
        "✍️ Your text",
        value=SAMPLES.get(lang_name, ""),
        height=200,
        max_chars=5000,
        placeholder="Enter your text here..."
    )

else:

    uploaded_file = st.file_uploader(
        "📄 Upload a .txt file",
        type=["txt"]
    )

    text = ""

    if uploaded_file is not None:

        try:
            text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            st.text_area(
                "📄 File content",
                text,
                height=200,
                disabled=True
            )

        except Exception as error:
            st.error(
                f"Unable to read the file: {error}"
            )


# ---------------------------------------------------------
# Character Counter
# ---------------------------------------------------------

st.caption(f"📝 {len(text)} / 5000 characters")


# ---------------------------------------------------------
# Convert Button
# ---------------------------------------------------------

if st.button(
    "🔊 Convert to Speech",
    type="primary",
    use_container_width=True
):

    # Check for empty input.
    if not text.strip():

        st.warning(
            "⚠️ Please enter some text before converting."
        )

    else:

        with st.spinner(
            "🎙️ Generating your speech..."
        ):

            try:

                language_code = LANGUAGES[lang_name]

                accent_tld = ACCENTS.get(
                    accent,
                    "com"
                )

                audio = synthesize(
                    text=text.strip(),
                    lang=language_code,
                    tld=accent_tld,
                    slow=slow
                )

                st.success(
                    "✅ Speech generated successfully!"
                )

                # Audio player
                st.audio(
                    audio,
                    format="audio/mp3"
                )

                # Download button
                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio,
                    file_name="speech.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )

            except Exception as error:

                st.error(
                    "❌ Failed to generate speech."
                )

                st.info(
                    "Please check your internet connection "
                    "and try again."
                )

                with st.expander("Show error details"):
                    st.code(str(error))


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "🔊 Text to Voice | Powered by Streamlit and Google Text-to-Speech"
)