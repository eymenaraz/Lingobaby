import random
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="LingoKids - Duolingo & MentalUP World",
    page_icon="🦉",
    layout="wide",
)

# Duolingo / MentalUP Tarzı Özel CSS ve LED Işık Efektleri
st.markdown(
    """
    <style>
    .main {
        background-color: #131927;
        color: white;
    }
    .stButton>button {
        border-radius: 16px;
        font-weight: 800;
        font-size: 18px;
        padding: 12px 24px;
        transition: all 0.2s ease-in-out;
    }
    /* Yeşil LED efekti */
    .correct-led {
        background-color: #2ecc71 !important;
        color: white !important;
        box-shadow: 0 0 20px #2ecc71, 0 0 40px #2ecc71 !important;
        border: 2px solid #27ae60 !important;
    }
    /* Kırmızı LED efekti */
    .wrong-led {
        background-color: #e74c3c !important;
        color: white !important;
        box-shadow: 0 0 20px #e74c3c, 0 0 40px #e74c3c !important;
        border: 2px solid #c0392b !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# MEB MÜFREDATINA UYGUN AŞIRI DETAYLI MÜFREDAT
# ==========================================
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu (Preschool)",
        "icon": "🎨",
        "description": "Sesler, renkler, sayılar ve sevimli dostlarımızla İngilizceye ilk adım!",
        "levels": [
            {
                "id": "k_1",
                "title": "1. Level: Colors (Renkler)",
                "topic_desc": "Görkemli renk dünyasını ve isimlerini öğrenelim.",
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
                    {
                        "en": "Pink",
                        "tr": "Pembe",
                        "emoji": "🩷",
                        "color": "#FF69B4",
                    },
                ],
            },
            {
                "id": "k_2",
                "title": "2. Level: Animals (Hayvanlar)",
                "topic_desc": "Sevimli hayvan dostlarımızı tanıyalım.",
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
                    {
                        "en": "Lion",
                        "tr": "Aslan",
                        "emoji": "🦁",
                        "color": "#FFB300",
                    },
                ],
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers 1-5 (Sayılar)",
                "topic_desc": "1'den 5'e kadar neşeyle sayalım.",
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
        "description": "Günlük konuşmalar, lezzetli meyveler ve vücudumuzun bölümleri.",
        "levels": [
            {
                "id": "g1_1",
                "title": "1. Level: Greetings (Selamlaşma)",
                "topic_desc": "İngilizce selamlaşmayı ve tanışmayı öğrenelim.",
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
                    {
                        "en": "Thank you",
                        "tr": "Teşekkür ederim",
                        "emoji": "🙏",
                        "color": "#009688",
                    },
                ],
            },
            {
                "id": "g1_2",
                "title": "2. Level: Fruits (Meyveler)",
                "topic_desc": "En sevdiğimiz taze meyveler.",
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
                        "en": "Watermelon",
                        "tr": "Karpuz",
                        "emoji": "🍉",
                        "color": "#4CAF50",
                    },
                ],
            },
            {
                "id": "g1_3",
                "title": "3. Level: Body Parts (Vücudumuz)",
                "topic_desc": "Organlarımızı ve vücudumuzu keşfedelim.",
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
        "description": "Okul eşyaları, aile üyeleri, taşıtlar ve yiyecekler.",
        "levels": [
            {
                "id": "g2_1",
                "title": "1. Level: Classroom (Okulumuz)",
                "topic_desc": "Sınıfımızda ve çantamızda olan eşyalar.",
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
                "title": "2. Level: Family (Ailemiz)",
                "topic_desc": "Sevgili aile bireylerimizin isimleri.",
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
                "title": "3. Level: Vehicles (Araçlar)",
                "topic_desc": "Hızlı ve eğlenceli ulaşım araçları.",
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


# ÜST PANEL / SCOREBAR
col_top1, col_top2 = st.columns([4, 1])
with col_top1:
    st.markdown(
        "### 🦉 LingoKids - Duolingo & MentalUP World",
        unsafe_allow_html=True,
    )
with col_top2:
    total_stars = sum(st.session_state.stars_earned.values())
    st.markdown(f"### ⭐ Toplam Yıldız: {total_stars}")
st.markdown("---")

# 1. ANA MENÜ EKRANI
if st.session_state.screen == "menu":
    st.markdown(
        "<h1 style='text-align: center; color: #58CC02;'>Öğrenme Yolculuğuna Hoş Geldin! 🎉</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: #A0A0B2;'>Lütfen sınıf düzeyini seç ve maceraya başla:</h3>",
        unsafe_allow_html=True,
    )
    st.write("")

    cols = st.columns(3)
    for i, (g_key, g_info) in enumerate(CURRICULUM_DATA.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div style="background-color: #1F2937; padding: 25px; border-radius: 20px; text-align: center; border: 3px solid #374151; min-height: 280px;">
                    <span style="font-size: 60px;">{g_info['icon']}</span>
                    <h2 style="color: #58CC02; margin-top: 10px;">{g_info['title']}</h2>
                    <p style="color: #9CA3AF; font-size: 15px;">{g_info['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button(
                "BAŞLA 🚀",
                key=f"btn_{g_key}",
                use_container_width=True,
                type="primary",
            ):
                go_map(g_key)
                st.rerun()

# 2. HARİTA EKRANI (MAP VIEW)
elif st.session_state.screen == "map":
    grade_info = CURRICULUM_DATA[st.session_state.grade_key]
    if st.button("⬅ Ana Menüye Dön"):
        go_menu()
        st.rerun()

    st.markdown(
        f"# {grade_info['icon']} {grade_info['title']} - Macera Haritası"
    )
    st.write("Seviyeleri sırasıyla tamamla ve yıldızları topla!")

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

            card_bg = "#10B981" if is_unlocked else "#374151"

            st.markdown(
                f"""
                <div style="background-color: {card_bg}; padding: 20px; border-radius: 20px; text-align: center; color: white;">
                    <h2>Level {idx+1}</h2>
                    <p style="font-size: 15px; font-weight: bold;">{lvl['title'].split(':')[1] if ':' in lvl['title'] else lvl['title']}</p>
                    <p style="font-size: 18px;">{star_str}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

            if is_unlocked:
                if st.button(
                    "OYNA ▶️",
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

# 3. DERS VE TEST EKRANI
elif st.session_state.screen == "game":
    lvl_data = st.session_state.current_level
    if st.button("🗺️ Haritaya Dön"):
        go_map(st.session_state.grade_key)
        st.rerun()

    if st.session_state.phase == "learn":
        st.markdown(f"# 📚 DERS: {lvl_data['title']}")
        st.info(f"💡 {lvl_data['topic_desc']}")

        cols = st.columns(len(lvl_data["words"]))
        for i, w in enumerate(lvl_data["words"]):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="background-color: #1F2937; padding: 20px; border-radius: 20px; text-align: center; border: 3px solid {w['color']};">
                        <span style="font-size: 55px;">{w['emoji']}</span>
                        <h3 style="color: {w['color']}; margin-top: 10px;">{w['en']}</h3>
                        <p style="color: #9CA3AF; font-size: 16px;">{w['tr']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")
        if st.button(
            "🎮 Öğrendim, Teste Başla!",
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

            st.progress(
                (st.session_state.quiz_index) / len(words),
                text=f"Soru {st.session_state.quiz_index + 1} / {len(words)}",
            )
            st.markdown(
                "<h2 style='text-align: center;'>Görselin İngilizce karşılığı nedir?</h2>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<div style='text-align: center; font-size: 100px; margin: 10px;'>{current_word['emoji']}</div>",
                unsafe_allow_html=True,
            )

            # Şıkları OLUŞTURMA
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
                    # LED Renk Durumunu Belirleme
                    is_this_selected = (
                        st.session_state.selected_option == opt
                    )
                    is_correct_opt = opt == current_word["en"]

                    btn_type = "secondary"

                    # Seçim yapıldıysa LED Renklerini Uygula
                    if st.session_state.selected_option is not None:
                        if is_correct_opt:
                            st.markdown(
                                f"<div class='correct-led' style='padding: 15px; border-radius: 16px; text-align: center; font-weight: bold; font-size: 20px; margin-bottom: 15px;'>🟢 {opt} (DOĞRU)</div>",
                                unsafe_allow_html=True,
                            )
                        elif is_this_selected and not st.session_state.is_correct:
                            st.markdown(
                                f"<div class='wrong-led' style='padding: 15px; border-radius: 16px; text-align: center; font-weight: bold; font-size: 20px; margin-bottom: 15px;'>🔴 {opt} (YANLIŞ)</div>",
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

            # Cevap Verildikten Sonraki Geri Bildirim ve "Sonraki Soru" Butonu
            if st.session_state.selected_option is not None:
                st.write("")
                if st.session_state.is_correct:
                    st.success("🎉 TEBRİKLER! Doğru Cevap!")
                    st.components.v1.html(
                        '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg"></audio>',
                        height=0,
                    )
                else:
                    st.error(
                        f"😅 Yanlış Cevap! Doğrusu: {current_word['en']}"
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
            "<h1 style='text-align: center; color: #FFD700;'>TEBRİKLER! LEVEL TAMAMLANDI! 🏆</h1>",
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
