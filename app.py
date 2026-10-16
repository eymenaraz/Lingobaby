import random
import streamlit as st

# Sayfa Yapılandırması (Geniş Ekran ve Çocuk Odaklı Tema)
st.set_page_config(
    page_title="LingoBaby - Çocuklar İçin İnteraktif İngilizce",
    page_icon="🐣",
    layout="wide",
)

# Duolingo & MentalUP Tarzı Özel CSS, LED Işık Efektleri ve Animasyonlar
st.markdown(
    """
    <style>
    .main {
        background-color: #0F172A;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        border-radius: 18px;
        font-weight: 800;
        font-size: 18px;
        padding: 14px 28px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 6px 0 #1E293B;
    }
    .stButton>button:active {
        transform: translateY(4px);
        box-shadow: 0 2px 0 #1E293B;
    }
    /* Yeşil LED Canlı Işık Efekti */
    .correct-led {
        background-color: #10B981 !important;
        color: white !important;
        box-shadow: 0 0 25px #10B981, 0 0 50px #10B981 !important;
        border: 3px solid #34D399 !important;
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        font-weight: 900;
        font-size: 22px;
        margin-bottom: 15px;
    }
    /* Kırmızı LED Canlı Işık Efekti */
    .wrong-led {
        background-color: #EF4444 !important;
        color: white !important;
        box-shadow: 0 0 25px #EF4444, 0 0 50px #EF4444 !important;
        border: 3px solid #F87171 !important;
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        font-weight: 900;
        font-size: 22px;
        margin-bottom: 15px;
    }
    .word-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-radius: 24px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# ZENGİN VE UZATILMIŞ MEB MÜFREDATI (GERÇEK RESİMLER)
# ==========================================
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu (Preschool)",
        "icon": "🎨",
        "description": "Temel sesler, muhteşem renkler, sevimli hayvanlar ve sayılarla eğlence!",
        "levels": [
            {
                "id": "k_1",
                "title": "1. Level: Colors (Görkemli Renkler)",
                "topic_desc": "Dünyayı renklendiren temel renkleri resimleriyle öğrenelim.",
                "words": [
                    {
                        "en": "Red",
                        "tr": "Kırmızı",
                        "img": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=400&q=80",
                        "color": "#EF4444",
                    },
                    {
                        "en": "Blue",
                        "tr": "Mavi",
                        "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&q=80",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Yellow",
                        "tr": "Sarı",
                        "img": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400&q=80",
                        "color": "#FBBF24",
                    },
                    {
                        "en": "Green",
                        "tr": "Yeşil",
                        "img": "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=400&q=80",
                        "color": "#10B981",
                    },
                    {
                        "en": "Orange",
                        "tr": "Turuncu",
                        "img": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=400&q=80",
                        "color": "#F97316",
                    },
                    {
                        "en": "Purple",
                        "tr": "Mor",
                        "img": "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=400&q=80",
                        "color": "#A855F7",
                    },
                    {
                        "en": "Pink",
                        "tr": "Pembe",
                        "img": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&q=80",
                        "color": "#EC4899",
                    },
                    {
                        "en": "Brown",
                        "tr": "Kahverengi",
                        "img": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=400&q=80",
                        "color": "#8B5CF6",
                    },
                ],
            },
            {
                "id": "k_2",
                "title": "2. Level: Animals (Sevimli Hayvanlar Krallığı)",
                "topic_desc": "Doğadaki tatlı ve güçlü hayvan dostlarımızı keşfedelim.",
                "words": [
                    {
                        "en": "Cat",
                        "tr": "Kedi",
                        "img": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&q=80",
                        "color": "#F97316",
                    },
                    {
                        "en": "Dog",
                        "tr": "Köpek",
                        "img": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&q=80",
                        "color": "#B45309",
                    },
                    {
                        "en": "Bird",
                        "tr": "Kuş",
                        "img": "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&q=80",
                        "color": "#06B6D4",
                    },
                    {
                        "en": "Fish",
                        "tr": "Balık",
                        "img": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=400&q=80",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Rabbit",
                        "tr": "Tavşan",
                        "img": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&q=80",
                        "color": "#EC4899",
                    },
                    {
                        "en": "Lion",
                        "tr": "Aslan",
                        "img": "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Elephant",
                        "tr": "Fil",
                        "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400&q=80",
                        "color": "#64748B",
                    },
                    {
                        "en": "Panda",
                        "tr": "Panda",
                        "img": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef9?w=400&q=80",
                        "color": "#10B981",
                    },
                ],
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers (Sayılar Dünyası 1-10)",
                "topic_desc": "Eğlenceli sayılarla saymayı alışkanlık haline getirelim.",
                "words": [
                    {
                        "en": "One",
                        "tr": "Bir",
                        "img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400&q=80",
                        "color": "#EF4444",
                    },
                    {
                        "en": "Two",
                        "tr": "İki",
                        "img": "https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=400&q=80",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Three",
                        "tr": "Üç",
                        "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&q=80",
                        "color": "#10B981",
                    },
                    {
                        "en": "Four",
                        "tr": "Dört",
                        "img": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Five",
                        "tr": "Beş",
                        "img": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&q=80",
                        "color": "#EC4899",
                    },
                ],
            },
        ],
    },
    "grade_1": {
        "title": "1. Sınıf (Primary Grade 1)",
        "icon": "🎒",
        "description": "Günlük tanışmalar, nefis meyveler, vücudumuz ve doğa.",
        "levels": [
            {
                "id": "g1_1",
                "title": "1. Level: Greetings (Selamlaşma & İletişim)",
                "topic_desc": "Arkadaşlarınla İngilizce selamlaşmayı ve konuşmayı öğren.",
                "words": [
                    {
                        "en": "Hello",
                        "tr": "Merhaba",
                        "img": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&q=80",
                        "color": "#10B981",
                    },
                    {
                        "en": "Goodbye",
                        "tr": "Hoşça Kal",
                        "img": "https://images.unsplash.com/photo-1516726817505-f5ed825624d8?w=400&q=80",
                        "color": "#EF4444",
                    },
                    {
                        "en": "Good Morning",
                        "tr": "Günaydın",
                        "img": "https://images.unsplash.com/photo-1470240731273-7821a6eeb6bd?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Good Night",
                        "tr": "İyi Geceler",
                        "img": "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=400&q=80",
                        "color": "#6366F1",
                    },
                ],
            },
            {
                "id": "g1_2",
                "title": "2. Level: Fruits (Lezzetli Taze Meyveler)",
                "topic_desc": "En sevdiğin vitamin deposu meyveler.",
                "words": [
                    {
                        "en": "Apple",
                        "tr": "Elma",
                        "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&q=80",
                        "color": "#EF4444",
                    },
                    {
                        "en": "Banana",
                        "tr": "Muz",
                        "img": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Orange",
                        "tr": "Portakal",
                        "img": "https://images.unsplash.com/photo-1547514701-42782101795e?w=400&q=80",
                        "color": "#F97316",
                    },
                    {
                        "en": "Strawberry",
                        "tr": "Çilek",
                        "img": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&q=80",
                        "color": "#EC4899",
                    },
                    {
                        "en": "Watermelon",
                        "tr": "Karpuz",
                        "img": "https://images.unsplash.com/photo-1587049352847-4a222e784d38?w=400&q=80",
                        "color": "#10B981",
                    },
                ],
            },
            {
                "id": "g1_3",
                "title": "3. Level: Body Parts (Harika Vücudumuz)",
                "topic_desc": "Organlarımızı ve vücudumuzu yakından tanıyalım.",
                "words": [
                    {
                        "en": "Eye",
                        "tr": "Göz",
                        "img": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&q=80",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Ear",
                        "tr": "Kulak",
                        "img": "https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Mouth",
                        "tr": "Ağız",
                        "img": "https://images.unsplash.com/photo-1588516903720-8ceb67f9ef84?w=400&q=80",
                        "color": "#EC4899",
                    },
                    {
                        "en": "Hand",
                        "tr": "El",
                        "img": "https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=400&q=80",
                        "color": "#10B981",
                    },
                ],
            },
        ],
    },
    "grade_2": {
        "title": "2. Sınıf (Primary Grade 2)",
        "icon": "📚",
        "description": "Okul gereçleri, canım ailemiz, araçlar ve nefis yiyecekler.",
        "levels": [
            {
                "id": "g2_1",
                "title": "1. Level: Classroom Objects (Okul & Sınıf)",
                "topic_desc": "Çantanda ve sınıfta bulunan eşyalar.",
                "words": [
                    {
                        "en": "Pencil",
                        "tr": "Kurşun Kalem",
                        "img": "https://images.unsplash.com/photo-1585336261026-6757f5f28ed7?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Book",
                        "tr": "Kitap",
                        "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Bag",
                        "tr": "Çanta",
                        "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&q=80",
                        "color": "#EC4899",
                    },
                    {
                        "en": "Ruler",
                        "tr": "Cetvel",
                        "img": "https://images.unsplash.com/photo-1588072432836-e10032774350?w=400&q=80",
                        "color": "#10B981",
                    },
                ],
            },
            {
                "id": "g2_2",
                "title": "2. Level: Family Members (Canım Ailemiz)",
                "topic_desc": "Sevgili aile fertlerimizin isimlerini öğrenelim.",
                "words": [
                    {
                        "en": "Mother",
                        "tr": "Anne",
                        "img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80",
                        "color": "#EC4899",
                    },
                    {
                        "en": "Father",
                        "tr": "Baba",
                        "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",
                        "color": "#3B82F6",
                    },
                    {
                        "en": "Brother",
                        "tr": "Erkek Kardeş",
                        "img": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80",
                        "color": "#10B981",
                    },
                    {
                        "en": "Baby",
                        "tr": "Bebek",
                        "img": "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=400&q=80",
                        "color": "#06B6D4",
                    },
                ],
            },
            {
                "id": "g2_3",
                "title": "3. Level: Vehicles (Ulaşım Araçları)",
                "topic_desc": "Hızlı ve heyecanlı araçları yakından görelim.",
                "words": [
                    {
                        "en": "Car",
                        "tr": "Araba",
                        "img": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&q=80",
                        "color": "#EF4444",
                    },
                    {
                        "en": "Bus",
                        "tr": "Otobüs",
                        "img": "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400&q=80",
                        "color": "#F59E0B",
                    },
                    {
                        "en": "Plane",
                        "tr": "Uçak",
                        "img": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=80",
                        "color": "#0288D1",
                    },
                    {
                        "en": "Train",
                        "tr": "Tren",
                        "img": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=400&q=80",
                        "color": "#8B5CF6",
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
if "unlocked_levels" not in st.session_state:
    st.session_state.unlocked_levels = {"k_1": True}
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


# ÜST PANEL / GAMIFICATION HEADER
col_top1, col_top2, col_top3 = st.columns([3, 1, 1])
with col_top1:
    st.markdown("## 🐣 LingoBaby World", unsafe_allow_html=True)
with col_top2:
    st.markdown(f"### 🔥 Seri: {st.session_state.streak} Gün")
with col_top3:
    total_stars = sum(st.session_state.stars_earned.values())
    st.markdown(f"### ⭐ Yıldız: {total_stars}")
st.markdown("---")

# 1. ANA MENÜ EKRANI (LingoBaby World)
if st.session_state.screen == "menu":
    st.markdown(
        "<h1 style='text-align: center; color: #10B981;'>Dünyanın En Eğlenceli İngilizce Macera Dünyası! 🎉</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: #94A3B8;'>Lütfen kendi eğitim seviyeni seç ve öğrenmeye başla:</h3>",
        unsafe_allow_html=True,
    )
    st.write("")

    cols = st.columns(3)
    for i, (g_key, g_info) in enumerate(CURRICULUM_DATA.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div class="word-card">
                    <span style="font-size: 70px;">{g_info['icon']}</span>
                    <h2 style="color: #10B981; margin-top: 15px;">{g_info['title']}</h2>
                    <p style="color: #94A3B8; font-size: 15px; min-height: 50px;">{g_info['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button(
                "MACERAYA BAŞLA 🚀",
                key=f"btn_{g_key}",
                use_container_width=True,
                type="primary",
            ):
                go_map(g_key)
                st.rerun()

# 2. SEVİYE VE GÖREV HARİTASI
elif st.session_state.screen == "map":
    grade_info = CURRICULUM_DATA[st.session_state.grade_key]
    if st.button("⬅ Ana Menüye Dön"):
        go_menu()
        st.rerun()

    st.markdown(
        f"# {grade_info['icon']} {grade_info['title']} - Görev Haritası"
    )
    st.write("Kilitleri aç, görevleri tamamla ve en yüksek yıldızı topla!")

    levels = grade_info["levels"]
    cols = st.columns(len(levels))

    for idx, lvl in enumerate(levels):
        with cols[idx]:
            lvl_id = lvl["id"]
            is_unlocked = st.session_state.unlocked_levels.get(lvl_id, False)
            stars = st.session_state.stars_earned.get(lvl_id, 0)
            star_str = (
                "⭐" * stars
                if stars > 0
                else ("AÇIK 🔓" if is_unlocked else "KİLİTLİ 🔒")
            )

            card_bg = "#10B981" if is_unlocked else "#334155"

            st.markdown(
                f"""
                <div style="background-color: {card_bg}; padding: 25px; border-radius: 24px; text-align: center; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.3);">
                    <h2>Level {idx+1}</h2>
                    <p style="font-size: 16px; font-weight: bold;">{lvl['title'].split(':')[1] if ':' in lvl['title'] else lvl['title']}</p>
                    <p style="font-size: 20px;">{star_str}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

            if is_unlocked:
                if st.button(
                    "BAŞLA ▶️",
                    key=f"lvl_btn_{lvl_id}",
                    use_container_width=True,
                    type="primary",
                ):
                    start_level(lvl)
                    st.rerun()
            else:
                st.button(
                    "🔒 Kilitli",
                    key=f"lvl_btn_{lvl_id}",
                    disabled=True,
                    use_container_width=True,
                )

# 3. İNTERAKTİF DERS VE OYUN MODÜLÜ
elif st.session_state.screen == "game":
    lvl_data = st.session_state.current_level
    if st.button("🗺️ Haritaya Dön"):
        go_map(st.session_state.grade_key)
        st.rerun()

    # Öğrenme Aşaması
    if st.session_state.phase == "learn":
        st.markdown(f"# 📚 DERS: {lvl_data['title']}")
        st.info(f"💡 {lvl_data['topic_desc']}")

        cols = st.columns(min(4, len(lvl_data["words"])))
        for i, w in enumerate(lvl_data["words"]):
            col_target = cols[i % 4]
            with col_target:
                st.markdown(
                    f"""
                    <div class="word-card" style="border: 3px solid {w['color']}; margin-bottom: 20px;">
                        <img src="{w['img']}" style="width: 100%; height: 160px; object-fit: cover; border-radius: 16px;">
                        <h3 style="color: {w['color']}; margin-top: 10px;">{w['en']}</h3>
                        <p style="color: #94A3B8; font-size: 16px;">{w['tr']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")
        if st.button(
            "🎮 Hepsini İnceledim, Alıştırmaya Başla!",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.phase = "quiz"
            st.rerun()

    # Test / Soru Aşaması
    elif st.session_state.phase == "quiz":
        words = lvl_data["words"]
        if st.session_state.quiz_index >= len(words):
            st.session_state.phase = "result"
            st.rerun()
        else:
            current_word = words[st.session_state.quiz_index]

            st.progress(
                (st.session_state.quiz_index) / len(words),
                text=f"Soru {st.session_state.quiz_index + 1} / {len(words)}",
            )
            st.markdown(
                "<h2 style='text-align: center;'>Aşağıdaki resmin İngilizce ismi nedir?</h2>",
                unsafe_allow_html=True,
            )

            # Büyük Görsel
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{current_word['img']}" style="width: 320px; height: 220px; object-fit: cover; border-radius: 24px; border: 4px solid #10B981; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Şıkları Oluşturma
            if "current_options" not in st.session_state or st.session_state.get(
                "last_q_idx"
            ) != st.session_state.quiz_index:
                opts = [current_word["en"]]
                other_words = [
                    w["en"] for w in words if w["en"] != current_word["en"]
                ]
                if len(other_words) < 3:
                    other_words += [
                        "Cat",
                        "Dog",
                        "Red",
                        "Blue",
                        "Apple",
                        "Car",
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

                    # Cevap Verildikten Sonra LED Efektleri
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

            # Cevap Verildiğinde Ses ve Geri Bildirim
            if st.session_state.selected_option is not None:
                st.write("")
                if st.session_state.is_correct:
                    st.success("🎉 BRAVO! Doğru Cevap!")
                    st.components.v1.html(
                        '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg"></audio>',
                        height=0,
                    )
                else:
                    st.error(
                        f"😅 Neredeyse Oluyordu! Doğrusu: {current_word['en']}"
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

    # Sonuç Ekrani
    elif st.session_state.phase == "result":
        total_q = len(lvl_data["words"])
        ratio = st.session_state.score / total_q

        if ratio == 1.0:
            stars = 3
        elif ratio >= 0.5:
            stars = 2
        else:
            stars = 1

        lvl_id = lvl_data["id"]
        st.session_state.stars_earned[lvl_id] = max(
            st.session_state.stars_earned.get(lvl_id, 0), stars
        )

        levels = CURRICULUM_DATA[st.session_state.grade_key]["levels"]
        curr_idx = next(i for i, l in enumerate(levels) if l["id"] == lvl_id)
        if curr_idx + 1 < len(levels):
            next_lvl_id = levels[curr_idx + 1]["id"]
            st.session_state.unlocked_levels[next_lvl_id] = True

        st.markdown(
            "<h1 style='text-align: center; color: #FBBF24;'>TEBRİKLER! LEVEL TAMAMLANDI! 🏆</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h1 style='text-align: center;'>{'⭐' * stars}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h3 style='text-align: center;'>Toplam Skorun: {st.session_state.score} / {total_q}</h3>",
            unsafe_allow_html=True,
        )

        if st.button(
            "🗺️ Haritaya Dön ve İlerle",
            type="primary",
            use_container_width=True,
        ):
            go_map(st.session_state.grade_key)
            st.rerun()
