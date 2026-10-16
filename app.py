import random
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="LingoBaby - Miyav ile İngilizce",
    page_icon="🐱",
    layout="wide",
)

# Duolingo Stili Kenar Asistan ve LED Işık CSS Efektleri
st.markdown(
    """
    <style>
    .main {
        background-color: #0F172A;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sağ Alt Köşede Sabit Kedi Asistan */
    .floating-mascot {
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 3px solid #38BDF8;
        border-radius: 24px;
        padding: 15px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        max-width: 320px;
        animation: floatAnim 3s ease-in-out infinite;
    }
    
    @keyframes floatAnim {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    
    .mascot-img {
        font-size: 50px;
        margin-right: 12px;
    }
    
    .mascot-msg {
        color: #F0F9FF;
        font-size: 14px;
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
        padding: 20px;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0,0,0,0.6);
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# TÜM MEB MÜFREDAT VE KESİNTİSİZ SVG GÖRSELLERİ
# ==========================================
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu",
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
                        "img": "https://api.dicebear.com/7.x/bottts/svg?seed=Lion",
                        "sound": "Kükreyen Orman Kralı 🦁",
                    },
                    {
                        "en": "Elephant",
                        "tr": "Fil",
                        "img": "https://api.dicebear.com/7.x/bottts/svg?seed=Elephant",
                        "sound": "Dev Hortumlu Dostumuz 🐘",
                    },
                    {
                        "en": "Panda",
                        "tr": "Panda",
                        "img": "https://api.dicebear.com/7.x/bottts/svg?seed=Panda",
                        "sound": "Bambu Yiyen Şirin Panda 🐼",
                    },
                    {
                        "en": "Giraffe",
                        "tr": "Zürafa",
                        "img": "https://api.dicebear.com/7.x/bottts/svg?seed=Giraffe",
                        "sound": "Uzun Boyunlu Zürafa 🦒",
                    },
                ],
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers 1-5 (Sayılar)",
                "topic_desc": "Eğlenceli sayılarla saymayı öğrenelim.",
                "type": "general",
                "words": [
                    {
                        "en": "One",
                        "tr": "Bir",
                        "img": "https://api.dicebear.com/7.x/shapes/svg?seed=One1",
                    },
                    {
                        "en": "Two",
                        "tr": "İki",
                        "img": "https://api.dicebear.com/7.x/shapes/svg?seed=Two2",
                    },
                    {
                        "en": "Three",
                        "tr": "Üç",
                        "img": "https://api.dicebear.com/7.x/shapes/svg?seed=Three3",
                    },
                ],
            },
        ],
    },
    "grade_1": {
        "title": "1. Sınıf",
        "icon": "🎒",
        "description": "Tanışma, meyveler, vücudumuz ve oyuncaklar.",
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
                        "img": "https://api.dicebear.com/7.x/thumbs/svg?seed=Hello",
                    },
                    {
                        "en": "Goodbye",
                        "tr": "Hoşça kal",
                        "img": "https://api.dicebear.com/7.x/thumbs/svg?seed=Goodbye",
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
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Apple",
                    },
                    {
                        "en": "Banana",
                        "tr": "Muz",
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Banana",
                    },
                ],
            },
        ],
    },
    "grade_2": {
        "title": "2. Sınıf",
        "icon": "📚",
        "description": "Sınıf eşyaları, aile üyeleri ve taşıtlar.",
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
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Pencil",
                    },
                    {
                        "en": "Book",
                        "tr": "Kitap",
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Book",
                    },
                ],
            }
        ],
    },
    "grade_3": {
        "title": "3. Sınıf",
        "icon": "🌟",
        "description": "Yetenekler (I can/can't), sıfatlar ve evimiz.",
        "levels": [
            {
                "id": "g3_1",
                "title": "1. Level: Abilities (Yetenekler)",
                "topic_desc": "Yapabildiğimiz eylemleri ifade edelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Fly",
                        "tr": "Uçmak",
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Fly",
                    },
                    {
                        "en": "Swim",
                        "tr": "Yüzmek",
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Swim",
                    },
                ],
            }
        ],
    },
    "grade_4": {
        "title": "4. Sınıf",
        "icon": "🚀",
        "description": "Sınıf kuralları, ülkeler ve meslekler.",
        "levels": [
            {
                "id": "g4_1",
                "title": "1. Level: Countries (Ülkeler)",
                "topic_desc": "Where are you from? (Nerelisin?)",
                "type": "general",
                "words": [
                    {
                        "en": "Turkey",
                        "tr": "Türkiye",
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=Turkey",
                    },
                    {
                        "en": "England",
                        "tr": "İngiltere",
                        "img": "https://api.dicebear.com/7.x/icons/svg?seed=England",
                    },
                ],
            }
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
if "mascot_msg" not in st.session_state:
    st.session_state.mascot_msg = (
        "Miyav! Hoş geldin! Bir sınıf seçip İngilizce öğrenmeye başlayalım! 🐱"
    )


# EKRANIN SAĞ ALT KÖŞESİNDE SABİT YAVRU KEDİ ASİSTAN
def update_mascot(msg):
    st.session_state.mascot_msg = msg


def render_floating_mascot():
    st.markdown(
        f"""
        <div class="floating-mascot">
            <div class="mascot-img">🐱</div>
            <div class="mascot-msg"><b>Miyav:</b> "{st.session_state.mascot_msg}"</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def go_menu():
    st.session_state.screen = "menu"
    update_mascot("Ana menüdeyiz! İstediğin zaman sınıfını değiştirebilirsin.")


def go_map(grade_key):
    st.session_state.screen = "map"
    st.session_state.grade_key = grade_key
    update_mascot("Level haritasındayız! İstediğin bölüme tıkla ve başla.")


def start_level(level_data):
    st.session_state.screen = "game"
    st.session_state.current_level = level_data
    st.session_state.phase = "learn"
    st.session_state.quiz_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.is_correct = None
    update_mascot(
        f"'{level_data['title']}' dersindeyiz! Görsellere iyi bak, birazdan test edeceğim."
    )


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

# 1. ANA MENÜ EKRANI
if st.session_state.screen == "menu":
    cols = st.columns(len(CURRICULUM_DATA))
    for i, (g_key, g_info) in enumerate(CURRICULUM_DATA.items()):
        with cols[i]:
            st.markdown(
                f"""
                <div style="background: #1E293B; border-radius: 20px; padding: 15px; text-align: center; border: 2px solid #334155; min-height: 220px;">
                    <span style="font-size: 50px;">{g_info['icon']}</span>
                    <h3 style="color: #38BDF8; margin-top: 10px;">{g_info['title']}</h3>
                    <p style="color: #94A3B8; font-size: 13px;">{g_info['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button(
                "GİRİŞ 🚀",
                key=f"btn_{g_key}",
                use_container_width=True,
                type="primary",
            ):
                go_map(g_key)
                st.rerun()

# 2. SEVİYE HARİTASI
elif st.session_state.screen == "map":
    grade_info = CURRICULUM_DATA[st.session_state.grade_key]
    if st.button("⬅ Ana Menüye Dön"):
        go_menu()
        st.rerun()

    levels = grade_info["levels"]
    cols = st.columns(len(levels))

    for idx, lvl in enumerate(levels):
        with cols[idx]:
            lvl_id = lvl["id"]
            stars = st.session_state.stars_earned.get(lvl_id, 0)
            star_str = "⭐" * stars if stars > 0 else "BAŞLAMAYA HAZIR 🚀"

            st.markdown(
                f"""
                <div style="background-color: #10B981; padding: 20px; border-radius: 20px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                    <h3>Level {idx+1}</h3>
                    <p style="font-size: 14px; font-weight: bold;">{lvl['title'].split(':')[1] if ':' in lvl['title'] else lvl['title']}</p>
                    <p style="font-size: 14px;">{star_str}</p>
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
        st.markdown(f"# 📚 {lvl_data['title']}")

        cols = st.columns(min(4, len(lvl_data["words"])))
        for i, w in enumerate(lvl_data["words"]):
            col_target = cols[i % 4]
            with col_target:
                st.markdown(
                    f"""
                    <div style="background: #1E293B; border-radius: 20px; padding: 15px; text-align: center; border: 3px solid #38BDF8; margin-bottom: 15px;">
                        <img src="{w['img']}" style="width: 100%; height: 140px; object-fit: contain; border-radius: 12px; background-color: white;">
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
            update_mascot(
                "Şimdi test zamanı! Doğru cevabı seçtiğinde yeşil LED yanacak!"
            )
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
                st.markdown(
                    f"""
                    <div class="zoo-viewport">
                        <p style="font-size: 18px; font-weight: bold; color: #FEF08A;">🦁 HAYVANAT BAHÇESİ SAFARİ GÖZLEMİ 🌿</p>
                        <img src="{current_word['img']}" style="width: 250px; height: 180px; object-fit: contain; border-radius: 20px; background-color: white; padding: 10px;">
                        <p style="font-size: 15px; margin-top: 10px; color: #FEF3C7;"><i>İpucu: {current_word.get('sound', 'Sevimli Dostumuz')}</i></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Saf Renkler Görünümü
            elif lvl_data.get("type") == "colors":
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{current_word['img']}" style="width: 280px; height: 160px; border-radius: 20px; border: 4px solid white;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{current_word['img']}" style="width: 220px; height: 180px; object-fit: contain; border-radius: 20px; background-color: white; padding: 10px;">
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
                                update_mascot(
                                    "Harikasın! Tam bir İngilizce dahi çocuğusun! 🎉"
                                )
                            else:
                                st.session_state.is_correct = False
                                update_mascot(
                                    f"Üzülme! Doğru cevap: {current_word['en']}. Bir dahakine kesin yapacaksın!"
                                )
                            st.rerun()

            # Cevap Sonrası Ses
            if st.session_state.selected_option is not None:
                st.write("")
                if st.session_state.is_correct:
                    st.components.v1.html(
                        '<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg"></audio>',
                        height=0,
                    )
                else:
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

        update_mascot(
            f"TEBRİKLER! {stars} yıldız kazandın! Seninle gurur duyuyorum! 🐱🏆"
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

# KEDİ MASMOTUNU ÇAĞIR
render_floating_mascot()
