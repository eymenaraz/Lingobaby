import random
import streamlit as st

# Sayfa Yapılandırması (Geniş Ekran)
st.set_page_config(
    page_title="MentalUP English World", page_icon="🌟", layout="wide"
)

# Çocuklar İçin Renkli ve Şık Arayüz Tasarımı
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
        "description": "MEB 1. Sınıf müfredatına uygun selamlaşma, meyveler ve vücudumuz.",
        "levels": [
            {
                "id": "g1_1",
                "title": "1. Level: Greetings (Selamlaşma)",
                "topic_desc": "Günlük yaşamda merhaba ve vedalaşma kelimeleri.",
                "words": [
                    {
                        "en": "Hello",
                        "tr": "Merhaba",
                        "emoji": "👋",
                        "color": "#4CAF50",
                    },
                    {
                        "en": "Goodbye",
                        "tr": "Hoşça Kal",
                        "emoji": "🙋‍♂️",
                        "color": "#F44336",
                    },
                    {
                        "en": "Good Morning",
                        "tr": "Günaydın",
                        "emoji": "🌅",
                        "color": "#FFC107",
                    },
                    {
                        "en": "Good Night",
                        "tr": "İyi Geceler",
                        "emoji": "🌙",
                        "color": "#3F51B5",
                    },
                ],
            },
            {
                "id": "g1_2",
                "title": "2. Level: Yummy Fruits (Lezzetli Meyveler)",
                "topic_desc": "Sevdiğimiz taze meyvelerin İngilizce karşılıkları.",
                "words": [
                    {
                        "en": "Apple",
                        "tr": "Elma",
                        "emoji": "🍎",
                        "color": "#F44336",
                    },
                    {
                        "en": "Banana",
                        "tr": "Muz",
                        "emoji": "🍌",
                        "color": "#FFEB3B",
                    },
                    {
                        "en": "Orange",
                        "tr": "Portakal",
                        "emoji": "🍊",
                        "color": "#FF9800",
                    },
                    {
                        "en": "Strawberry",
                        "tr": "Çilek",
                        "emoji": "🍓",
                        "color": "#E91E63",
                    },
                    {
                        "en": "Grapes",
                        "tr": "Üzüm",
                        "emoji": "🍇",
                        "color": "#9C27B0",
                    },
                ],
            },
            {
                "id": "g1_3",
                "title": "3. Level: Body Parts (Vücudumuz)",
                "topic_desc": "Vücudumuzun bölümlerini öğrenelim.",
                "words": [
                    {"en": "Eye", "tr": "Göz", "emoji": "👁️", "color": "#2196F3"},
                    {
                        "en": "Ear",
                        "tr": "Kulak",
                        "emoji": "👂",
                        "color": "#FF9800",
                    },
                    {
                        "en": "Mouth",
                        "tr": "Ağız",
                        "emoji": "👄",
                        "color": "#E91E63",
                    },
                    {
                        "en": "Nose",
                        "tr": "Burun",
                        "emoji": "👃",
                        "color": "#795548",
                    },
                    {
                        "en": "Hand",
                        "tr": "El",
                        "emoji": "✋",
                        "color": "#4CAF50",
                    },
                ],
            },
        ],
    },
    "grade_2": {
        "title": "2. Sınıf (Primary Grade 2)",
        "icon": "📚",
        "description": "MEB 2. Sınıf ünitelere uygun okul eşyaları, aile ve araçlar.",
        "levels": [
            {
                "id": "g2_1",
                "title": "1. Level: Classroom Objects (Okul Eşyaları)",
                "topic_desc": "Sınıfta ve çantamızda bulunan nesneler.",
                "words": [
                    {
                        "en": "Pencil",
                        "tr": "Kurşun Kalem",
                        "emoji": "✏️",
                        "color": "#FFC107",
                    },
                    {
                        "en": "Book",
                        "tr": "Kitap",
                        "emoji": "📖",
                        "color": "#2196F3",
                    },
                    {
                        "en": "Bag",
                        "tr": "Çanta",
                        "emoji": "🎒",
                        "color": "#E91E63",
                    },
                    {
                        "en": "Ruler",
                        "tr": "Cetvel",
                        "emoji": "📏",
                        "color": "#009688",
                    },
                    {
                        "en": "Eraser",
                        "tr": "Silgi",
                        "emoji": "🧽",
                        "color": "#9C27B0",
                    },
                ],
            },
            {
                "id": "g2_2",
                "title": "2. Level: Family Members (Ailemiz)",
                "topic_desc": "Aile fertlerini İngilizce ifade etme.",
                "words": [
                    {
                        "en": "Mother",
                        "tr": "Anne",
                        "emoji": "👩",
                        "color": "#E91E63",
                    },
                    {
                        "en": "Father",
                        "tr": "Baba",
                        "emoji": "👨",
                        "color": "#1976D2",
                    },
                    {
                        "en": "Brother",
                        "tr": "Erkek Kardeş",
                        "emoji": "👦",
                        "color": "#4CAF50",
                    },
                    {
                        "en": "Sister",
                        "tr": "Kız Kardeş",
                        "emoji": "👧",
                        "color": "#FF9800",
                    },
                    {
                        "en": "Baby",
                        "tr": "Bebek",
                        "emoji": "👶",
                        "color": "#00BCD4",
                    },
                ],
            },
            {
                "id": "g2_3",
                "title": "3. Level: Vehicles (Ulaşım Araçları)",
                "topic_desc": "Çevremizde gördüğümüz taşıtlar.",
                "words": [
                    {"en": "Car", "tr": "Araba", "emoji": "🚗", "color": "#F44336"},
                    {"en": "Bus", "tr": "Otobüs", "emoji": "🚌", "color": "#FFC107"},
                    {
                        "en": "Plane",
                        "tr": "Uçak",
                        "emoji": "✈️",
                        "color": "#0288D1",
                    },
                    {
                        "en": "Bicycle",
                        "tr": "Bisiklet",
                        "emoji": "🚲",
                        "color": "#4CAF50",
                    },
                    {
                        "en": "Train",
                        "tr": "Tren",
                        "emoji": "🚂",
                        "color": "#795548",
                    },
                ],
            },
        ],
    },
}

# Session State Tanımlamaları
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
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0


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


# ÜST BİLGİ ÇUBUĞU
col_top1, col_top2 = st.columns([4, 1])
with col_top1:
    st.markdown("### 🌟 MentalUP English World", unsafe_allow_html=True)
with col_top2:
    total_stars = sum(st.session_state.stars_earned.values())
    st.markdown(f"### ⭐ Yıldız: {total_stars}")
st.markdown("---")

# 1. ANA MENÜ EKRANI
if st.session_state.screen == "menu":
    st.markdown(
        "<h2 style='text-align: center; color: white;'>Hoş Geldin Küçük Öğrenci! Eğitim Düzeyini Seç:</h2>",
        unsafe_allow_html=True,
    )
    st.write("")

    cols = st.columns(3)
    for i, (g_key, g_info) in enumerate(CURRICULUM_DATA.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div style="background-color: #2B2D42; padding: 25px; border-radius: 15px; text-align: center; border: 2px solid #3D3C5A; min-height: 280px;">
                    <span style="font-size: 50px;">{g_info['icon']}</span>
                    <h3 style="color: #4E9F3D; margin-top: 10px;">{g_info['title']}</h3>
                    <p style="color: #A0A0B2; font-size: 14px;">{g_info['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"Maceraya Başla 🚀",
                key=f"btn_{g_key}",
                use_container_width=True,
            ):
                go_map(g_key)
                st.rerun()

# 2. SEVİYE HARİTASI EKRANI
elif st.session_state.screen == "map":
    grade_info = CURRICULUM_DATA[st.session_state.grade_key]
    if st.button("⬅ Ana Menüye Dön"):
        go_menu()
        st.rerun()

    st.markdown(
        f"## {grade_info['icon']} {grade_info['title']} - Görev Haritası"
    )
    st.write("Aşağıdaki seviyelerden birini seçerek eğlenceye başla!")

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

            st.markdown(
                f"""
                <div style="background-color: {'#FF9F1A' if is_unlocked else '#455A64'}; padding: 20px; border-radius: 15px; text-align: center; color: white;">
                    <h3>Level {idx+1}</h3>
                    <p style="font-size: 13px; font-weight: bold;">{lvl['title'].split(':')[1] if ':' in lvl['title'] else lvl['title']}</p>
                    <p style="font-size: 16px;">{star_str}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if is_unlocked:
                if st.button(
                    f"Seç #{idx+1}",
                    key=f"lvl_btn_{lvl_id}",
                    use_container_width=True,
                ):
                    start_level(lvl)
                    st.rerun()
            else:
                st.button(
                    "Kilitli",
                    key=f"lvl_btn_{lvl_id}",
                    disabled=True,
                    use_container_width=True,
                )

# 3. DERS VE OYUN EKRANI
elif st.session_state.screen == "game":
    lvl_data = st.session_state.current_level
    if st.button("🗺️ Haritaya Dön"):
        go_map(st.session_state.grade_key)
        st.rerun()

    if st.session_state.phase == "learn":
        st.markdown(f"## 📚 DERS: {lvl_data['title']}")
        st.info(f"💡 {lvl_data['topic_desc']}")

        cols = st.columns(len(lvl_data["words"]))
        for i, w in enumerate(lvl_data["words"]):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="background-color: #2B2D42; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid {w['color']};">
                        <span style="font-size: 50px;">{w['emoji']}</span>
                        <h4 style="color: {w['color']}; margin-top: 10px;">{w['en']}</h4>
                        <p style="color: #A0A0B2;">{w['tr']}</p>
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

    elif st.session_state.phase == "quiz":
        words = lvl_data["words"]
        if st.session_state.quiz_index >= len(words):
            st.session_state.phase = "result"
            st.rerun()
        else:
            current_word = words[st.session_state.quiz_index]
            st.markdown(
                f"### Soru {st.session_state.quiz_index + 1} / {len(words)}"
            )
            st.markdown(
                "<h3 style='text-align: center;'>Aşağıdaki görselin İngilizce karşılığı hangisidir?</h3>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<div style='text-align: center; font-size: 90px;'>{current_word['emoji']}</div>",
                unsafe_allow_html=True,
            )

            options = [current_word["en"]]
            all_other = [
                w["en"] for w in words if w["en"] != current_word["en"]
            ]
            if len(all_other) < 3:
                all_other = ["Cat", "Dog", "Red", "Blue", "Apple", "Car"]
                all_other = [w for w in all_other if w != current_word["en"]]

            random_wrong = random.sample(all_other, min(3, len(all_other)))
            options.extend(random_wrong)
            random.shuffle(options)

            c1, c2 = st.columns(2)
            for i, opt in enumerate(options):
                col = c1 if i % 2 == 0 else c2
                with col:
                    if st.button(
                        opt,
                        key=f"opt_{i}_{st.session_state.quiz_index}",
                        use_container_width=True,
                    ):
                        if opt == current_word["en"]:
                            st.success("Doğru Cevap! 🎉 Harikasın!")
                            st.session_state.score += 1
                        else:
                            st.error(
                                f"Yanlış! Doğrusu: {current_word['en']}"
                            )

                        st.session_state.quiz_index += 1
                        st.rerun()

    elif st.session_state.phase == "result":
        total_q = len(lvl_data["words"])
        ratio = st.session_state.score / total_q

        if ratio == 1.0:
            
