import random
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="LingoBaby - Anaokulundan 4. Sınıfa İngilizce",
    page_icon="🐱",
    layout="wide",
)

# Duolingo, MentalUP ve LED Işık CSS Efektleri
st.markdown(
    """
    <style>
    .main {
        background-color: #0F172A;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .mascot-box {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 3px solid #38BDF8;
        border-radius: 20px;
        padding: 15px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        box-shadow: 0 8px 20px rgba(56, 189, 248, 0.2);
    }
    .mascot-avatar {
        font-size: 55px;
        margin-right: 15px;
    }
    .mascot-text {
        color: #F0F9FF;
        font-size: 17px;
        font-weight: 600;
    }
    /* Canlı Yeşil LED Efekti */
    .correct-led {
        background-color: #10B981 !important;
        color: white !important;
        box-shadow: 0 0 25px #10B981, 0 0 50px #10B981 !important;
        border: 3px solid #34D399 !important;
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        font-weight: 900;
        font-size: 22px;
        margin-bottom: 15px;
    }
    /* Canlı Kırmızı LED Efekti */
    .wrong-led {
        background-color: #EF4444 !important;
        color: white !important;
        box-shadow: 0 0 25px #EF4444, 0 0 50px #EF4444 !important;
        border: 3px solid #F87171 !important;
        border-radius: 18px;
        padding: 16px;
        text-align: center;
        font-weight: 900;
        font-size: 22px;
        margin-bottom: 15px;
    }
    .zoo-viewport {
        background: linear-gradient(180deg, #0284C7 0%, #15803D 70%, #166534 100%);
        border: 5px solid #F59E0B;
        border-radius: 28px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0,0,0,0.6);
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# TÜM SINIFLARIN 1 YILLIK MEB MÜFREDATI
# ==========================================
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu (Preschool)",
        "icon": "🎨",
        "description": "Saf renkler, 1. Şahıs Safari turu, sayılar ve duygular!",
        "levels": [
            {
                "id": "k_1",
                "title": "1. Level: Pure Colors (Net Renkler)",
                "topic_desc": "Sadece belirtilen saf rengin bulunduğu görsellerle renkleri öğrenelim.",
                "type": "colors",
                "words": [
                    {
                        "en": "Red",
                        "tr": "Kırmızı",
                        "img": "https://singlecolorimage.com/get/FF0000/400x300",
                        "color": "#EF4444",
                    },
                    {
                        "en": "Blue",
                        "tr": "Mavi",
                        "img": "https://singlecolorimage.com/get/0000FF/400x300",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Yellow",
                        "tr": "Sarı",
                        "img": "https://singlecolorimage.com/get/FFFF00/400x300",
                        "color": "#FBBF24",
                    },
                    {
                        "en": "Green",
                        "tr": "Yeşil",
                        "img": "https://singlecolorimage.com/get/008000/400x300",
                        "color": "#10B981",
                    },
                    {
                        "en": "Orange",
                        "tr": "Turuncu",
                        "img": "https://singlecolorimage.com/get/FFA500/400x300",
                        "color": "#F97316",
                    },
                    {
                        "en": "Purple",
                        "tr": "Mor",
                        "img": "https://singlecolorimage.com/get/800080/400x300",
                        "color": "#A855F7",
                    },
                ],
            },
            {
                "id": "k_2",
                "title": "2. Level: Zoo Safari (Hayvanat Bahçesi)",
                "topic_desc": "1. Şahıs bakış açısıyla hayvanat bahçesini turlayalım!",
                "type": "zoo",
                "words": [
                    {
                        "en": "Lion",
                        "tr": "Aslan",
                        "img": "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=500&q=80",
                        "sound": "Kükreyen Orman Kralı",
                    },
                    {
                        "en": "Elephant",
                        "tr": "Fil",
                        "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=500&q=80",
                        "sound": "Dev Hortumlu Dostumuz",
                    },
                    {
                        "en": "Panda",
                        "tr": "Panda",
                        "img": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef9?w=500&q=80",
                        "sound": "Bambu Yiyen Şirin Panda",
                    },
                    {
                        "en": "Giraffe",
                        "tr": "Zürafa",
                        "img": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=500&q=80",
                        "sound": "Uzun Boyunlu Zürafa",
                    },
                    {
                        "en": "Monkey",
                        "tr": "Maymun",
                        "img": "https://images.unsplash.com/photo-1540573133985-780688d1e248?w=500&q=80",
                        "sound": "Neşeli Maymun",
                    },
                ],
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers 1-10 (Sayılar)",
                "topic_desc": "Eğlenceli sayılarla saymayı öğrenelim.",
                "type": "general",
                "words": [
                    {
                        "en": "One",
                        "tr": "Bir",
                        "img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&q=80",
                    },
                    {
                        "en": "Two",
                        "tr": "İki",
                        "img": "https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=400&q=80",
                    },
                    {
                        "en": "Three",
                        "tr": "Üç",
                        "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&q=80",
                    },
                    {
                        "en": "Four",
                        "tr": "Dört",
                        "img": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400&q=80",
                    },
                    {
                        "en": "Five",
                        "tr": "Beş",
                        "img": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&q=80",
                    },
                ],
            },
            {
                "id": "k_4",
                "title": "4. Level: Feelings (Duygularımız)",
                "topic_desc": "Nasıl hissettiğimizi İngilizce söyleyelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Happy",
                        "tr": "Mutlu",
                        "img": "https://images.unsplash.com/photo-1543610892-0b1f7e6d8ac1?w=400&q=80",
                    },
                    {
                        "en": "Sad",
                        "tr": "Üzgün",
                        "img": "https://images.unsplash.com/photo-1516585427167-9f4af9627e6c?w=400&q=80",
                    },
                    {
                        "en": "Energetic",
                        "tr": "Enerjik",
                        "img": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=400&q=80",
                    },
                ],
            },
        ],
    },
    "grade_1": {
        "title": "1. Sınıf (Primary Grade 1)",
        "icon": "🎒",
        "description": "Tanışma, meyveler, vücudumuz, oyuncaklar ve okul eşyaları.",
        "levels": [
            {
                "id": "g1_1",
                "title": "1. Level: Greetings (Selamlaşma)",
                "topic_desc": "Merhaba demeyi ve vedalaşmayı öğrenelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Hello",
                        "tr": "Merhaba",
                        "img": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&q=80",
                    },
                    {
                        "en": "Goodbye",
                        "tr": "Hoşça kal",
                        "img": "https://images.unsplash.com/photo-1516726817505-f5ed825624d8?w=400&q=80",
                    },
                    {
                        "en": "Good Morning",
                        "tr": "Günaydın",
                        "img": "https://images.unsplash.com/photo-1470240731273-7821a6eeb6bd?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g1_2",
                "title": "2. Level: Fruits (Meyveler)",
                "topic_desc": "Taze meyvelerin İngilizce isimleri.",
                "type": "general",
                "words": [
                    {
                        "en": "Apple",
                        "tr": "Elma",
                        "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&q=80",
                    },
                    {
                        "en": "Banana",
                        "tr": "Muz",
                        "img": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&q=80",
                    },
                    {
                        "en": "Strawberry",
                        "tr": "Çilek",
                        "img": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g1_3",
                "title": "3. Level: Body Parts (Vücudumuz)",
                "topic_desc": "Vücudumuzun organlarını tanıyalım.",
                "type": "general",
                "words": [
                    {
                        "en": "Eye",
                        "tr": "Göz",
                        "img": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&q=80",
                    },
                    {
                        "en": "Ear",
                        "tr": "Kulak",
                        "img": "https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?w=400&q=80",
                    },
                    {
                        "en": "Hand",
                        "tr": "El",
                        "img": "https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g1_4",
                "title": "4. Level: Toys (Oyuncaklar)",
                "topic_desc": "En sevdiğimiz oyuncakların isimleri.",
                "type": "general",
                "words": [
                    {
                        "en": "Ball",
                        "tr": "Top",
                        "img": "https://images.unsplash.com/photo-1614632537190-23e4146777db?w=400&q=80",
                    },
                    {
                        "en": "Doll",
                        "tr": "Oyuncak Bebek",
                        "img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&q=80",
                    },
                    {
                        "en": "Teddy Bear",
                        "tr": "Oyuncak Ayı",
                        "img": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?w=400&q=80",
                    },
                ],
            },
        ],
    },
    "grade_2": {
        "title": "2. Sınıf (Primary Grade 2)",
        "icon": "📚",
        "description": "Sınıf eşyaları, aile üyeleri, taşıtlar, yiyecekler ve evimiz.",
        "levels": [
            {
                "id": "g2_1",
                "title": "1. Level: Classroom Objects (Okul & Sınıf)",
                "topic_desc": "Sınıfta kullandığımız eşyalar.",
                "type": "general",
                "words": [
                    {
                        "en": "Pencil",
                        "tr": "Kurşun Kalem",
                        "img": "https://images.unsplash.com/photo-1585336261026-6757f5f28ed7?w=400&q=80",
                    },
                    {
                        "en": "Book",
                        "tr": "Kitap",
                        "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80",
                    },
                    {
                        "en": "Bag",
                        "tr": "Çanta",
                        "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g2_2",
                "title": "2. Level: Family Members (Canım Ailem)",
                "topic_desc": "Aile fertlerinin isimleri.",
                "type": "general",
                "words": [
                    {
                        "en": "Mother",
                        "tr": "Anne",
                        "img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80",
                    },
                    {
                        "en": "Father",
                        "tr": "Baba",
                        "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",
                    },
                    {
                        "en": "Brother",
                        "tr": "Erkek Kardeş",
                        "img": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g2_3",
                "title": "3. Level: Vehicles (Ulaşım Araçları)",
                "topic_desc": "Hızlı ve heyecanlı araçlar.",
                "type": "general",
                "words": [
                    {
                        "en": "Car",
                        "tr": "Araba",
                        "img": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&q=80",
                    },
                    {
                        "en": "Bus",
                        "tr": "Otobüs",
                        "img": "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400&q=80",
                    },
                    {
                        "en": "Plane",
                        "tr": "Uçak",
                        "img": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g2_4",
                "title": "4. Level: Food & Drinks (Yiyecek & İçecek)",
                "topic_desc": "Lezzetli yiyecek ve içecekler.",
                "type": "general",
                "words": [
                    {
                        "en": "Milk",
                        "tr": "Süt",
                        "img": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&q=80",
                    },
                    {
                        "en": "Bread",
                        "tr": "Ekmek",
                        "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&q=80",
                    },
                    {
                        "en": "Water",
                        "tr": "Su",
                        "img": "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?w=400&q=80",
                    },
                ],
            },
        ],
    },
    "grade_3": {
        "title": "3. Sınıf (Primary Grade 3)",
        "icon": "🌟",
        "description": "Gramer, yetenekler (I can/can't), sıfatlar, evimiz ve şehirde konumlar.",
        "levels": [
            {
                "id": "g3_1",
                "title": "1. Level: Abilities (Yetenekler - I can / I can't)",
                "topic_desc": "Yapabildiğimiz ve yapamadığımız eylemleri ifade edelim.",
                "type": "general",
                "words": [
                    {
                        "en": "I can fly",
                        "tr": "Uçabilirim",
                        "img": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&q=80",
                    },
                    {
                        "en": "I can swim",
                        "tr": "Yüzebilirim",
                        "img": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=400&q=80",
                    },
                    {
                        "en": "I can run",
                        "tr": "Koşabilirim",
                        "img": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g3_2",
                "title": "2. Level: Adjectives (Sıfatlar & Dış Görünüş)",
                "topic_desc": "İnsanların fiziksel özelliklerini tanımlayalım.",
                "type": "general",
                "words": [
                    {
                        "en": "Tall",
                        "tr": "Uzun boylu",
                        "img": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=400&q=80",
                    },
                    {
                        "en": "Short",
                        "tr": "Kısa boylu",
                        "img": "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=400&q=80",
                    },
                    {
                        "en": "Young",
                        "tr": "Genç",
                        "img": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g3_3",
                "title": "3. Level: House & Rooms (Evimiz ve Odalar)",
                "topic_desc": "Evin bölümlerini öğrenelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Bedroom",
                        "tr": "Yatak Odası",
                        "img": "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=400&q=80",
                    },
                    {
                        "en": "Kitchen",
                        "tr": "Mutfak",
                        "img": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=400&q=80",
                    },
                    {
                        "en": "Living Room",
                        "tr": "Oturma Odası",
                        "img": "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g3_4",
                "title": "4. Level: Weather (Hava Durumu)",
                "topic_desc": "Hava durumunu sorma ve söyleme (How is the weather?).",
                "type": "general",
                "words": [
                    {
                        "en": "Sunny",
                        "tr": "Güneşli",
                        "img": "https://images.unsplash.com/photo-1617155093730-a8bf47be792d?w=400&q=80",
                    },
                    {
                        "en": "Rainy",
                        "tr": "Yağmurlu",
                        "img": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=400&q=80",
                    },
                    {
                        "en": "Snowy",
                        "tr": "Karlı",
                        "img": "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=400&q=80",
                    },
                ],
            },
        ],
    },
    "grade_4": {
        "title": "4. Sınıf (Primary Grade 4)",
        "icon": "🚀",
        "description": "Sınıf kuralları, ülkeler, günlük rutinler, saatler ve meslekler.",
        "levels": [
            {
                "id": "g4_1",
                "title": "1. Level: Classroom Rules (Sınıf Kuralları)",
                "topic_desc": "İngilizce emir cümleleri ve sınıf içi kurallar.",
                "type": "general",
                "words": [
                    {
                        "en": "Open the door",
                        "tr": "Kapıyı aç",
                        "img": "https://images.unsplash.com/photo-1509644851169-2acc08aa15d6?w=400&q=80",
                    },
                    {
                        "en": "Listen to the teacher",
                        "tr": "Öğretmeni dinle",
                        "img": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=400&q=80",
                    },
                    {
                        "en": "Raise your hand",
                        "tr": "Elini kaldır",
                        "img": "https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g4_2",
                "title": "2. Level: Countries & Nationalities (Ülkeler & Milletler)",
                "topic_desc": "Where are you from? (Nerelisin?) sorusunu öğrenelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Turkey - Turkish",
                        "tr": "Türkiye - Türk",
                        "img": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=400&q=80",
                    },
                    {
                        "en": "England - English",
                        "tr": "İngiltere - İngiliz",
                        "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400&q=80",
                    },
                    {
                        "en": "Japan - Japanese",
                        "tr": "Japonya - Japon",
                        "img": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g4_3",
                "title": "3. Level: Daily Routines (Günlük Yaşam)",
                "topic_desc": "Günün bölümlerinde yaptıklarımızı anlatalım.",
                "type": "general",
                "words": [
                    {
                        "en": "Get up",
                        "tr": "Uyanmak / Kalkmak",
                        "img": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=400&q=80",
                    },
                    {
                        "en": "Brush teeth",
                        "tr": "Diş fırçalamak",
                        "img": "https://images.unsplash.com/photo-1559599101-f09722fb4948?w=400&q=80",
                    },
                    {
                        "en": "Have breakfast",
                        "tr": "Kahvaltı yapmak",
                        "img": "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400&q=80",
                    },
                ],
            },
            {
                "id": "g4_4",
                "title": "4. Level: Jobs & Professions (Meslekler)",
                "topic_desc": "Büyüyünce ne olmak istiyorsun? (What is your job?)",
                "type": "general",
                "words": [
                    {
                        "en": "Teacher",
                        "tr": "Öğretmen",
                        "img": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=400&q=80",
                    },
                    {
                        "en": "Doctor",
                        "tr": "Doktor",
                        "img": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=400&q=80",
                    },
                    {
                        "en": "Pilot",
                        "tr": "Pilot",
                        "img": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=80",
                    },
                ],
            },
        ],
    },
}

# State Yönetimi
if "screen" not in st.session_state:
    st.session_state.screen = "menu"
if "grade_key" not in st.session_state:
    st.session_state.grade_key = "kindergarten"
if "current_level" not in st.session_state:
    st.session_state.current_level = None
if "phase" not in st.session_state:
    st.session_state.phase = "learn"
if "stars_earned" not in st.session_state:
    st.session_state.stars_earned = {}
if "streak" not in st.session_state:
    st.session_state.streak = 1
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "is_correct" not in st.session_state:
    st.session_state.is_correct = None


# MASKOT YARDIMCI BİLEŞENİ
def show_mascot(message):
    st.markdown(
        f"""
        <div class="mascot-box">
            <div class="mascot-avatar">🐱</div>
            <div class="mascot-text"><b>Miyav diyor ki:</b> "{message}"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def go_menu():
    st.session_state.screen = "menu"


def go_map(grade_key):
    st.session_state.screen = "map"
    st.session_state.grade_key = grade_key


def start_level(level_data):
    st.session_state.screen = "game"
    st.session_state.current_level = level_data
    st.session_state.phase = "learn"
    st.session_state.quiz_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.is_correct = None


# ÜST PANEL
col_top1, col_top2, col_top3 = st.columns([3, 1, 1])
with col_top1:
    st.markdown("## 🐱 LingoBaby World", unsafe_allow_html=True)
with col_top2:
    st.markdown(f"### 🔥 Seri: {st.session_state.streak} Gün")
with col_top3:
    total_stars = sum(st.session_state.stars_earned.values())
    st.markdown(f"### ⭐ Yıldız: {total_stars}")
st.markdown("---")

# 1. ANA MENÜ EKRANI (TÜM SINIFLAR AÇIK)
if st.session_state.screen == "menu":
    show_mascot(
        "Hoş geldin! Ben kedi Miyav 🐱 Tüm seviyeler ve kilitler senin için açık! İstediğin sınıfı seçip hemen öğrenmeye başlayabilirsin."
    )

    cols = st.columns(len(CURRICULUM_DATA))
    for i, (g_key, g_info) in enumerate(CURRICULUM_DATA.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div style="background: #1E293B; border-radius: 20px; padding: 15px; text-align: center; border: 2px solid #334155; min-height: 250px;">
                    <span style="font-size: 50px;">{g_info['icon']}</span>
                    <h3 style="color: #38BDF8; margin-top: 10px;">{g_info['title']}</h3>
                    <p style="color: #94A3B8; font-size: 13px;">{g_info['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button(
                "GİRİŞ YAP 🚀",
                key=f"btn_{g_key}",
                use_container_width=True,
                type="primary",
            ):
                go_map(g_key)
                st.rerun()

# 2. SEVİYE HARİTASI (TÜM LEVELLER AÇIK)
elif st.session_state.screen == "map":
    grade_info = CURRICULUM_DATA[st.session_state.grade_key]
    if st.button("⬅ Ana Menüye Dön"):
        go_menu()
        st.rerun()

    show_mascot(
        f"{grade_info['title']} ders haritasındayız! Tüm seviyeler açık, dilediğin seviyeden başlayabilirsin!"
    )

    levels = grade_info["levels"]
    cols = st.columns(len(levels))

    for idx, lvl in enumerate(levels):
        with cols[idx]:
            lvl_id = lvl["id"]
            stars = st.session_state.stars_earned.get(lvl_id, 0)
            star_str = "⭐" * stars if stars > 0 else "HERKESE AÇIK 🔓"

            st.markdown(
                f"""
                <div style="background-color: #10B981; padding: 20px; border-radius: 20px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                    <h3>Level {idx+1}</h3>
                    <p style="font-size: 14px; font-weight: bold;">{lvl['title'].split(':')[1] if ':' in lvl['title'] else lvl['title']}</p>
                    <p style="font-size: 16px;">{star_str}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

            if st.button(
                "BAŞLA ▶️",
                key=f"lvl_btn_{lvl_id}",
                use_container_width=True,
                type="primary",
            ):
                start_level(lvl)
                st.rerun()

# 3. DERS VE TEST EKRANI
elif st.session_state.screen == "game":
    lvl_data = st.session_state.current_level
    if st.button("🗺️ Haritaya Dön"):
        go_map(st.session_state.grade_key)
        st.rerun()

    # Öğrenme Modu
    if st.session_state.phase == "learn":
        show_mascot(
            f"Şimdi '{lvl_data['title']}' konusunu öğreniyoruz! Kartlara iyi bak, birazdan alıştırma yapacağız."
        )

        cols = st.columns(min(4, len(lvl_data["words"])))
        for i, w in enumerate(lvl_data["words"]):
            col_target = cols[i % 4]
            with col_target:
                st.markdown(
                    f"""
                    <div style="background: #1E293B; border-radius: 20px; padding: 15px; text-align: center; border: 3px solid #38BDF8; margin-bottom: 15px;">
                        <img src="{w['img']}" style="width: 100%; height: 140px; object-fit: cover; border-radius: 12px;">
                        <h3 style="color: #38BDF8; margin-top: 10px;">{w['en']}</h3>
                        <p style="color: #94A3B8;">{w['tr']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")
        if st.button(
            "🎮 Öğrendim, Alıştırmalara Başla!",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.phase = "quiz"
            st.rerun()

    # Test Modu
    elif st.session_state.phase == "quiz":
        words = lvl_data["words"]
        if st.session_state.quiz_index >= len(words):
            st.session_state.phase = "result"
            st.rerun()
        else:
            current_word = words[st.session_state.quiz_index]

            # Hayvanat Bahçesi Özel 1. Şahıs Görünümü
            if lvl_data.get("type") == "zoo":
                show_mascot(
                    "📱 1. Şahıs Hayvanat Bahçesi Safari Görünümü! Dürbünümüzle baktık ve önümüzde bu hayvan duruyor. Sence İngilizce adı ne?"
                )
                st.markdown(
                    f"""
                    <div class="zoo-viewport">
                        <p style="font-size: 18px; font-weight: bold; color: #FEF08A;">🦁 HAYVANAT BAHÇESİ SAFARİ GÖZLEMİ 🌿</p>
                        <img src="{current_word['img']}" style="width: 360px; height: 230px; object-fit: cover; border-radius: 20px; border: 5px solid white;">
                        <p style="font-size: 15px; margin-top: 10px; color: #FEF3C7;"><i>İpucu: {current_word.get('sound', 'Sevimli Dostumuz')}</i></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Saf Renkler Görünümü
            elif lvl_data.get("type") == "colors":
                show_mascot(
                    "Bu saf renge dikkatlice bak! Sadece belirtilen renk var. Doğru İngilizce adını bulabilir misin?"
                )
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{current_word['img']}" style="width: 280px; height: 160px; border-radius: 20px; border: 4px solid white;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:
                show_mascot(
                    "Görsele dikkatlice bak ve doğru seçeneği işaretle!"
                )
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{current_word['img']}" style="width: 300px; height: 200px; object-fit: cover; border-radius: 20px; border: 4px solid white;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Şıkları Hazırlama
            if "current_options" not in st.session_state or st.session_state.get(
                "last_q_idx"
            ) != st.session_state.quiz_index:
                opts = [current_word["en"]]
                other_words = [
                    w["en"] for w in words if w["en"] != current_word["en"]
                ]
                if len(other_words) < 3:
                    other_words += [
                        "Apple",
                        "Dog",
                        "Red",
                        "Blue",
                        "Book",
                        "Teacher",
                    ]
                    other_words = [
                        w for w in set(other_words) if w != current_word["en"]
                    ]

                wrong_opts = random.sample(other_words, min(3, len(other_words)))
                opts.extend(wrong_opts)
                random.shuffle(opts)
                st.session_state.current_options = opts
                st.session_state.last_q_idx = st.session_state.quiz_index

            options = st.session_state.current_options

            c1, c2 = st.columns(2)
            for i, opt in enumerate(options):
                col = c1 if i % 2 == 0 else c2
                with col:
                    is_this_selected = (
                        st.session_state.selected_option == opt
                    )
                    is_correct_opt = opt == current_word["en"]

                    # Canlı LED Efekt Kontrolleri
                    if st.session_state.selected_option is not None:
                        if is_correct_opt:
                            st.markdown(
                                f"<div class='correct-led'>🟢 {opt} (DOĞRU)</div>",
                                unsafe_allow_html=True,
                            )
                        elif is_this_selected and not st.session_state.is_correct:
                            st.markdown(
                                f"<div class='wrong-led'>🔴 {opt} (YANLIŞ)</div>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.button(
                                opt,
                                key=f"opt_{i}_{st.session_state.quiz_index}",
                                disabled=True,
                                use_container_width=True,
                            )
                    else:
                        if st.button(
                            opt,
                            key=f"opt_{i}_{st.session_state.quiz_index}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_option = opt
                            if opt == current_word["en"]:
                                st.session_state.is_correct = True
                                st.session_state.score += 1
                            else:
                                st.session_state.is_correct = False
                            st.rerun()

            # Cevap Sonrası Bildirimler ve Ses
            if st.session_state.selected_option is not None:
                st.write("")
                if st.session_state.is_correct:
                    st.success("🎉 Miyav: 'Harikasın! Tam bir İngilizce şampiyonusun!'")
                    st.components.v1.html(
                        '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg"></audio>',
                        height=0,
                    )
                else:
                    st.error(
                        f"😅 Miyav: 'Doğru cevap: {current_word['en']}. Bir dahakine kesin yapacaksın!'"
                    )
                    st.components.v1.html(
                        '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2003/2003-preview.mp3" type="audio/mpeg"></audio>',
                        height=0,
                    )

                if st.button(
                    "Sonraki Soru ➡️", type="primary", use_container_width=True
                ):
                    st.session_state.quiz_index += 1
                    st.session_state.selected_option = None
                    st.session_state.is_correct = None
                    st.rerun()

    # Seviye Sonu
    elif st.session_state.phase == "result":
        total_q = len(lvl_data["words"])
        ratio = st.session_state.score / total_q

        stars = 3 if ratio == 1.0 else (2 if ratio >= 0.5 else 1)

        lvl_id = lvl_data["id"]
        st.session_state.stars_earned[lvl_id] = max(
            st.session_state.stars_earned.get(lvl_id, 0), stars
        )

        show_mascot(
            f"TEBRİKLER! {stars} yıldız kazandın! Miyav seninle gurur duyuyor! 🐱🏆"
        )

        st.markdown(
            f"<h1 style='text-align: center; color: #FBBF24;'>{'⭐' * stars}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h3 style='text-align: center;'>Skorun: {st.session_state.score} / {total_q}</h3>",
            unsafe_allow_html=True,
        )

        if st.button(
            "🗺️ Haritaya Dön", type="primary", use_container_width=True
        ):
            go_map(st.session_state.grade_key)
            st.rerun()
