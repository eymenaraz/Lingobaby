import random
import streamlit as st

# Sayfa Yapılandırması (Geniş Ekran)
st.set_page_config(
    page_title="MentalUP English World", page_icon="🌟", layout="wide"
)

# Arayüz Özelleştirmeleri
st.markdown(
    """
    <style>
    .main {
        background-color: #1E1E2E;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# MEB MÜFREDATINA UYGUN KONU VE KELİME VERİLERİ
# ==========================================
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu (Preschool)",
        "icon": "🎨",
        "description": "Temel kavramlar, sesler, renkler ve eğlenceli görsel tanıma adımları.",
        "levels": [
            {
                "id": "k_1",
                "title": "1. Level: Colors (Renkler)",
                "topic_desc": "Temel renkleri tanıyalım ve İngilizce isimlerini öğrenelim.",
                "words": [
                    {
                        "en": "Red",
                        "tr": "Kırmızı",
                        "emoji": "🔴",
                        "color": "#FF4D4D",
                    },
                    {
                        "en": "Blue",
                        "tr": "Mavi",
                        "emoji": "🔵",
                        "color": "#4D94FF",
                    },
                    {
                        "en": "Yellow",
                        "tr": "Sarı",
                        "emoji": "🟡",
                        "color": "#FFD700",
                    },
                    {
                        "en": "Green",
                        "tr": "Yeşil",
                        "emoji": "🟢",
                        "color": "#4CAF50",
                    },
                    {
                        "en": "Orange",
                        "tr": "Turuncu",
                        "emoji": "🟠",
                        "color": "#FF9800",
                    },
                    {
                        "en": "Purple",
                        "tr": "Mor",
                        "emoji": "🟣",
                        "color": "#9C27B0",
                    },
                ],
            },
            {
                "id": "k_2",
                "title": "2. Level: Cute Animals (Sevimli Hayvanlar)",
                "topic_desc": "Çevremizdeki tatlı hayvan dostlarımızı keşfedelim.",
                "words": [
                    {
                        "en": "Cat",
                        "tr": "Kedi",
                        "emoji": "🐱",
                        "color": "#FF9800",
                    },
                    {
                        "en": "Dog",
                        "tr": "Köpek",
                        "emoji": "🐶",
                        "color": "#795548",
                    },
                    {
                        "en": "Bird",
                        "tr": "Kuş",
                        "emoji": "🐦",
                        "color": "#2196F3",
                    },
                    {
                        "en": "Fish",
                        "tr": "Balık",
                        "emoji": "🐟",
                        "color": "#00BCD4",
                    },
                    {
                        "en": "Rabbit",
                        "tr": "Tavşan",
                        "emoji": "🐰",
                        "color": "#E91E63",
                    },
                    {
                        "en": "Duck",
                        "tr": "Ördek",
                        "emoji": "🦆",
                        "color": "#8BC34A",
                    },
                ],
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers 1-5 (Sayılar 1-5)",
                "topic_desc": "İlk 5 sayıyı İngilizce saymayı öğrenelim.",
                "words": [
                    {"en": "One", "tr": "Bir", "emoji": "1️⃣", "color": "#E91E63"},
                    {"en": "Two", "tr": "İki", "emoji": "2️⃣", "color": "#9C27B0"},
                    {
                        "en": "Three",
                        "tr": "Üç",
                        "emoji": "3️⃣",
                        "color": "#3F51B5",
                    },
                    {
                        "en": "Four",
                        "tr": "Dört",
                        "emoji": "4️⃣",
                        "color": "#009688",
                    },
                    {"en": "Five", "tr": "Beş", "emoji": "5️⃣", "color": "#FF5722"},
                ],
            },
        ],
    },
    "grade_1": {
        "title": "1. Sınıf (Primary Grade 1)",
        "icon": "🎒",
        "description": "MEB 1. Sınıf müfredatına uygun selamlaş
