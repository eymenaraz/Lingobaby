import random
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="LingoBaby - Akıllı İngilizce Öğrenme Platformu",
    page_icon="🐱",
    layout="wide",
)

# Arayüz ve LED Efekt CSS Tasarımı
st.markdown(
    """
    <style>
    .main {
        background-color: #0F172A;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .logo-box {
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Sağ Alt Köşede Sabit Kedi Asistan (Miyav) */
    .floating-mascot {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 3px solid #38BDF8;
        border-radius: 20px;
        padding: 12px 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        max-width: 320px;
    }
    
    .mascot-img {
        font-size: 42px;
        margin-right: 12px;
    }
    
    .mascot-msg {
        color: #F0F9FF;
        font-size: 13px;
        font-weight: 600;
    }

    /* Doğru Şık LED Efekti */
    .correct-led {
        background-color: #10B981 !important;
        color: white !important;
        box-shadow: 0 0 25px #10B981, 0 0 50px #10B981 !important;
        border: 3px solid #34D399 !important;
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        font-weight: 900;
        font-size: 18px;
        margin-bottom: 12px;
    }
    
    /* Yanlış Şık LED Efekti */
    .wrong-led {
        background-color: #EF4444 !important;
        color: white !important;
        box-shadow: 0 0 25px #EF4444, 0 0 50px #EF4444 !important;
        border: 3px solid #F87171 !important;
        border-radius: 18px;
        padding: 14px;
        text-align: center;
        font-weight: 900;
        font-size: 18px;
        margin-bottom: 12px;
    }
    
    .zoo-viewport {
        background: linear-gradient(180deg, #0284C7 0%, #15803D 70%, #166534 100%);
        border: 4px solid #F59E0B;
        border-radius: 24px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        margin-bottom: 15px;
    }
    
    .color-block {
        width: 100%;
        height: 160px;
        border-radius: 16px;
        border: 4px solid white;
        margin-bottom: 10px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# LOGO KODU (SVG)
LINGOBABY_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 130" width="100%" height="100">
  <rect x="10" y="10" width="480" height="110" rx="20" fill="#1E293B" stroke="#38BDF8" stroke-width="4"/>
  <text x="250" y="70" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-weight="900" font-size="44" fill="#38BDF8">Lingo<tspan fill="#10B981">Baby</tspan></text>
  <text x="250" y="98" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-weight="600" font-size="14" fill="#94A3B8">TÜBİTAK Uyumlu İnteraktif İngilizce Müfredatı</text>
</svg>
"""

# ==========================================
# TÜM SINIFLARIN DETAYLI VE GENİŞ MEB MÜFREDATI
# ==========================================
CURRICULUM_DATA = {
    "kindergarten": {
        "title": "Anaokulu",
        "icon": "🎨",
        "description": "Saf renkler, 1. Şahıs Safari turu, sayılar ve duygular.",
        "levels": [
            {
                "id": "k_1",
                "title": "1. Level: Pure Colors (Saf Renkler)",
                "topic_desc": "Tek renk alanlarıyla renkleri karıştırmadan öğrenelim.",
                "type": "colors",
                "words": [
                    {"en": "Red", "tr": "Kırmızı", "hex": "#FF0000"},
                    {"en": "Blue", "tr": "Mavi", "hex": "#0000FF"},
                    {"en": "Yellow", "tr": "Sarı", "hex": "#FFFF00"},
                    {"en": "Green", "tr": "Yeşil", "hex": "#008000"},
                    {"en": "Orange", "tr": "Turuncu", "hex": "#FFA500"},
                    {"en": "Purple", "tr": "Mor", "hex": "#800080"},
                    {"en": "Pink", "tr": "Pembe", "hex": "#FFC0CB"},
                ],
            },
            {
                "id": "k_2",
                "title": "2. Level: Zoo Safari (Hayvanat Bahçesi)",
                "topic_desc": "1. Şahıs bakış açısıyla hayvanları tanıyalım.",
                "type": "zoo",
                "words": [
                    {
                        "en": "Lion",
                        "tr": "Aslan",
                        "img": "https://images.unsplash.com/photo-1534188753412-3e26d1d618d6?w=500&q=80",
                        "sound": "Orman Kralı 🦁",
                    },
                    {
                        "en": "Elephant",
                        "tr": "Fil",
                        "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=500&q=80",
                        "sound": "Dev Hortumlu 🐘",
                    },
                    {
                        "en": "Panda",
                        "tr": "Panda",
                        "img": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef9?w=500&q=80",
                        "sound": "Şirin Panda 🐼",
                    },
                    {
                        "en": "Giraffe",
                        "tr": "Zürafa",
                        "img": "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=500&q=80",
                        "sound": "Uzun Boyunlu 🦒",
                    },
                ],
            },
            {
                "id": "k_3",
                "title": "3. Level: Numbers 1-5 (Sayılar)",
                "topic_desc": "Temel sayıları saymayı öğrenelim.",
                "type": "general",
                "words": [
                    {
                        "en": "One",
                        "tr": "Bir",
                        "img": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=500&q=80",
                    },
                    {
                        "en": "Two",
                        "tr": "İki",
                        "img": "https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=500&q=80",
                    },
                    {
                        "en": "Three",
                        "tr": "Üç",
                        "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500&q=80",
                    },
                ],
            },
            {
                "id": "k_4",
                "title": "4. Level: Feelings (Duygularımız)",
                "topic_desc": "Duyguları ifade edelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Happy",
                        "tr": "Mutlu",
                        "img": "https://images.unsplash.com/photo-1543610892-0b1f7e6d8ac1?w=500&q=80",
                    },
                    {
                        "en": "Sad",
                        "tr": "Üzgün",
                        "img": "https://images.unsplash.com/photo-1516585427167-9f4af9627e6c?w=500&q=80",
                    },
                ],
            },
        ],
    },
    "grade_1": {
        "title": "1. Sınıf",
        "icon": "🎒",
        "description": "Tanışma, meyveler, vücudumuz, oyuncaklar.",
        "levels": [
            {
                "id": "g1_1",
                "title": "1. Level: Greetings (Selamlaşma)",
                "topic_desc": "Selamlaşma diyalogları.",
                "type": "general",
                "words": [
                    {
                        "en": "Hello",
                        "tr": "Merhaba",
                        "img": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=500&q=80",
                    },
                    {
                        "en": "Goodbye",
                        "tr": "Hoşça kal",
                        "img": "https://images.unsplash.com/photo-1516726817505-f5ed825624d8?w=500&q=80",
                    },
                ],
            },
            {
                "id": "g1_2",
                "title": "2. Level: Fruits (Lezzetli Meyveler)",
                "topic_desc": "Taze meyveler.",
                "type": "general",
                "words": [
                    {
                        "en": "Apple",
                        "tr": "Elma",
                        "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500&q=80",
                    },
                    {
                        "en": "Banana",
                        "tr": "Muz",
                        "img": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&q=80",
                    },
                    {
                        "en": "Strawberry",
                        "tr": "Çilek",
                        "img": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=500&q=80",
                    },
                ],
            },
            {
                "id": "g1_3",
                "title": "3. Level: Body Parts (Vücudumuz)",
                "topic_desc": "Organlarımız.",
                "type": "general",
                "words": [
                    {
                        "en": "Eye",
                        "tr": "Göz",
                        "img": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=500&q=80",
                    },
                    {
                        "en": "Hand",
                        "tr": "El",
                        "img": "https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=500&q=80",
                    },
                ],
            },
        ],
    },
    "grade_2": {
        "title": "2. Sınıf",
        "icon": "📚",
        "description": "Sınıf eşyaları, aile, taşıtlar ve yiyecekler.",
        "levels": [
            {
                "id": "g2_1",
                "title": "1. Level: Classroom Objects (Sınıf Eşyaları)",
                "topic_desc": "Okul malzemeleri.",
                "type": "general",
                "words": [
                    {
                        "en": "Pencil",
                        "tr": "Kurşun Kalem",
                        "img": "https://images.unsplash.com/photo-1585336261026-6757f5f28ed7?w=500&q=80",
                    },
                    {
                        "en": "Book",
                        "tr": "Kitap",
                        "img": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&q=80",
                    },
                    {
                        "en": "Bag",
                        "tr": "Çanta",
                        "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&q=80",
                    },
                ],
            },
            {
                "id": "g2_2",
                "title": "2. Level: Family (Ailemiz)",
                "topic_desc": "Aile fertleri.",
                "type": "general",
                "words": [
                    {
                        "en": "Mother",
                        "tr": "Anne",
                        "img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&q=80",
                    },
                    {
                        "en": "Father",
                        "tr": "Baba",
                        "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&q=80",
                    },
                ],
            },
            {
                "id": "g2_3",
                "title": "3. Level: Vehicles (Ulaşım Araçları)",
                "topic_desc": "Taşıtlar.",
                "type": "general",
                "words": [
                    {
                        "en": "Car",
                        "tr": "Araba",
                        "img": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=500&q=80",
                    },
                    {
                        "en": "Bus",
                        "tr": "Otobüs",
                        "img": "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=500&q=80",
                    },
                ],
            },
        ],
    },
    "grade_3": {
        "title": "3. Sınıf",
        "icon": "🌟",
        "description": "Yetenekler (I can/can't), sıfatlar, evimiz ve hava durumu.",
        "levels": [
            {
                "id": "g3_1",
                "title": "1. Level: Abilities (Yetenekler)",
                "topic_desc": "Yapabildiğimiz eylemler.",
                "type": "general",
                "words": [
                    {
                        "en": "Swim",
                        "tr": "Yüzmek",
                        "img": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=500&q=80",
                    },
                    {
                        "en": "Run",
                        "tr": "Koşmak",
                        "img": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500&q=80",
                    },
                ],
            },
            {
                "id": "g3_2",
                "title": "2. Level: Weather (Hava Durumu)",
                "topic_desc": "Hava durumunu ifade edelim.",
                "type": "general",
                "words": [
                    {
                        "en": "Sunny",
                        "tr": "Güneşli",
                        "img": "https://images.unsplash.com/photo-1617155093730-a8bf47be792d?w=500&q=80",
                    },
                    {
                        "en": "Rainy",
                        "tr": "Yağmurlu",
                        "img": "https://images.unsplash.com/photo-1519692933481-e162a57d6721?w=500&q=80",
                    },
                ],
            },
        ],
    },
    "grade_4": {
        "title": "4. Sınıf",
        "icon": "🚀",
        "description": "Ülkeler, meslekler, günlük rutinler ve saatler.",
        "levels": [
            {
                "id": "g4_1",
                "title": "1. Level: Countries (Ülkeler)",
                "topic_desc": "Dünya ülkeleri.",
                "type": "general",
                "words": [
                    {
                        "en": "Turkey",
                        "tr": "Türkiye",
                        "img": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=500&q=80",
                    },
                    {
                        "en": "England",
                        "tr": "İngiltere",
                        "img": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=500&q=80",
                    },
                ],
            },
            {
                "id": "g4_2",
                "title": "2. Level: Professions (Meslekler)",
                "topic_desc": "Meslekler.",
                "type": "general",
                "words": [
                    {
                        "en": "Doctor",
                        "tr": "Doktor",
                        "img": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=500&q=80",
                    },
                    {
                        "en": "Teacher",
                        "tr": "Öğretmen",
                        "img": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=500&q=80",
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
if "mascot_msg" not in st.session_state:
    st.session_state.mascot_msg = (
        "Merhaba! Ben Miyav 🐱 Öğrenmeye hazır mısın?"
    )


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
    update_mascot(
        "Ana menüye döndük! İstediğin sınıfı seçip inceleyebilirsin."
    )


def go_map(grade_key):
    st.session_state.screen = "map"
    st.session_state.grade_key = grade_key
    update_mascot("Level haritasındayız. Bir seviye seçip başla!")


def start_level(level_data):
    st.session_state.screen = "game"
    st.session_state.current_level = level_data
    st.session_state.phase = "learn"
    st.session_state.quiz_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.is_correct = None
    update_mascot(
        f"'{level_data['title']}' dersindeyiz! Kartları inceledikten sonra teste geçebilirsin."
    )


# LOGO VE ÜST PANEL
st.markdown(
    f"<div class='logo-box'>{LINGOBABY_LOGO_SVG}</div>", unsafe_allow_html=True
)

col_top1, col_top2, col_top3 = st.columns([2, 1, 1])
with col_top1:
    if st.session_state.screen != "menu":
        if st.button("🏠 Ana Menüye Dön", type="secondary"):
            go_menu()
            st.rerun()
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
                <div style="background: #1E293B; border-radius: 20px; padding: 15px; text-align: center; border: 2px solid #334155; min-height: 210px;">
                    <span style="font-size: 45px;">{g_info['icon']}</span>
                    <h3 style="color: #38BDF8; margin-top: 10px;">{g_info['title']}</h3>
                    <p style="color: #94A3B8; font-size: 12px;">{g_info['description']}</p>
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

    c_b1, c_b2 = st.columns([1, 4])
    with c_b1:
        if st.button("⬅ Sınıf Seçimi"):
            go_menu()
            st.rerun()

    levels = grade_info["levels"]
    cols = st.columns(len(levels))

    for idx, lvl in enumerate(levels):
        with cols[idx]:
            lvl_id = lvl["id"]
            stars = st.session_state.stars_earned.get(lvl_id, 0)
            star_str = "⭐" * stars if stars > 0 else "HAZIR 🚀"

            st.markdown(
                f"""
                <div style="background-color: #10B981; padding: 18px; border-radius: 20px; text-align: center; color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                    <h3>Level {idx+1}</h3>
                    <p style="font-size: 13px; font-weight: bold;">{lvl['title'].split(':')[1] if ':' in lvl['title'] else lvl['title']}</p>
                    <p style="font-size: 13px;">{star_str}</p>
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

    c_b1, c_b2 = st.columns([1, 4])
    with c_b1:
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
                if lvl_data.get("type") == "colors":
                    st.markdown(
                        f"""
                        <div style="background: #1E293B; border-radius: 20px; padding: 15px; text-align: center; border: 3px solid #38BDF8; margin-bottom: 15px;">
                            <div class="color-block" style="background-color: {w['hex']};"></div>
                            <h3 style="color: #38BDF8; margin-top: 10px;">{w['en']}</h3>
                            <p style="color: #94A3B8;">{w['tr']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
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
            "🎮 İnceledim, Teste Başla!",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.phase = "quiz"
            update_mascot(
                "Test başladı! Doğru cevabı seçtiğinde yeşil LED yanacak."
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

            if lvl_data.get("type") == "colors":
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div class="color-block" style="background-color: {current_word['hex']}; width: 280px; height: 160px; margin: 0 auto;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif lvl_data.get("type") == "zoo":
                st.markdown(
                    f"""
                    <div class="zoo-viewport">
                        <p style="font-size: 16px; font-weight: bold; color: #FEF08A;">🦁 SAFARİ GÖZLEMİ 🌿</p>
                        <img src="{current_word['img']}" style="width: 300px; height: 190px; object-fit: cover; border-radius: 18px; border: 3px solid white;">
                        <p style="font-size: 14px; margin-top: 8px; color: #FEF3C7;"><i>Bilgi: {current_word.get('sound', 'Canlı')}</i></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="{current_word['img']}" style="width: 300px; height: 190px; object-fit: cover; border-radius: 18px; border: 3px solid white;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Şık Hazırlığı
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
                        "Turkey",
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
                                update_mascot("Harika! Doğru yanıt. 🎉")
                            else:
                                st.session_state.is_correct = False
                                update_mascot(
                                    f"Doğru yanıt '{current_word['en']}' olmalıydı."
                                )
                            st.rerun()

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
            f"Tebrikler! Seviye başarıyla tamamlandı. Kazanılan Yıldız: {stars}"
        )

        st.markdown(
            f"<h1 style='text-align: center; color: #FBBF24;'>{'⭐' * stars}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h3 style='text-align: center;'>Başarı Skoru: {st.session_state.score} / {total_q}</h3>",
            unsafe_allow_html=True,
        )

        if st.button(
            "🗺️ Haritaya Dön", type="primary", use_container_width=True
        ):
            go_map(st.session_state.grade_key)
            st.rerun()

# KEDİ ASİSTANI ÇAĞIR
render_floating_mascot()
