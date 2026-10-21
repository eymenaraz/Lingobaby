import json
import math
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LingoCat", page_icon="🐱", layout="centered")

# ------------------------------------------------------------------
# TASARIM: parlak oyuncak paleti, kalın hatlı "tıkla-bas" butonlar
# ------------------------------------------------------------------
INK, SKY, SUN, CORAL, MINT, BG = "#2B2D6E", "#4CC9F0", "#FFD23F", "#FF6B6B", "#3DDC97", "#F3F0FF"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
html, body, .stApp, [class*="css"] {{ font-family: 'Fredoka', sans-serif !important; }}
.stApp {{ background: {BG}; color: {INK}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem; max-width: 760px; }}
h1, h2, h3, p, span, label {{ color: {INK}; }}

.stButton > button {{
    font-family: 'Fredoka', sans-serif; font-weight: 600; font-size: 18px;
    border-radius: 18px; border: 3px solid {INK}; background: white; color: {INK};
    box-shadow: 0 5px 0 {INK}; padding: .55rem 1rem; transition: transform .08s, box-shadow .08s;
}}
.stButton > button:hover {{ border-color: {INK}; color: {INK}; background: #FFFBEA; }}
.stButton > button:active {{ transform: translateY(4px); box-shadow: 0 1px 0 {INK}; }}
.stButton > button[kind="primary"] {{ background: {CORAL}; color: white; }}
.stButton > button[kind="primary"]:hover {{ background: #FF5252; color: white; }}
.stButton > button:disabled {{ opacity: .55; box-shadow: 0 2px 0 {INK}; }}

.brand {{ display:flex; align-items:center; gap:10px; font-size:34px; font-weight:700; color:{INK}; }}
.brand b {{ color:{CORAL}; }}
.chips {{ display:flex; gap:8px; flex-wrap:wrap; margin:8px 0 14px; }}
.chip {{ background:white; border:3px solid {INK}; border-radius:999px; padding:2px 14px; font-weight:600; font-size:15px; }}
.bubble {{ display:flex; gap:12px; align-items:center; background:white; border:3px solid {INK};
          border-radius:22px; padding:10px 16px; margin-bottom:16px; box-shadow:0 5px 0 {INK}; }}
.bubble .cat {{ font-size:44px; }}
.bubble .msg {{ font-size:16px; font-weight:500; }}
.gcard {{ border:3px solid {INK}; border-radius:24px; padding:16px; box-shadow:0 6px 0 {INK}; margin-bottom:8px; }}
.gcard .ic {{ font-size:46px; }} .gcard h3 {{ margin:4px 0 2px; font-size:24px; }}
.gcard p {{ margin:0; font-size:14px; opacity:.85; }}
.unit {{ border:3px solid {INK}; border-radius:22px; padding:12px 16px; background:white; box-shadow:0 5px 0 {INK}; margin-bottom:6px; }}
.unit .t {{ font-size:20px; font-weight:700; }} .unit .v {{ font-size:13px; opacity:.8; }}
.stage {{ text-align:center; background:white; border:3px solid {INK}; border-radius:28px;
         padding:18px 10px; box-shadow:0 6px 0 {INK}; margin-bottom:14px; }}
.stage .big {{ font-size:96px; line-height:1.1; }}
.stage .q {{ font-size:18px; font-weight:600; }}
.sentence {{ min-height:64px; background:white; border:3px dashed {SKY}; border-radius:20px;
            padding:12px; text-align:center; font-size:26px; font-weight:700; margin:8px 0 14px; }}
.ok {{ background:{MINT}; color:{INK}; border:3px solid {INK}; border-radius:18px; padding:12px;
      text-align:center; font-weight:700; font-size:19px; box-shadow:0 5px 0 {INK}; margin:6px 0 12px; }}
.no {{ background:{CORAL}; color:white; border:3px solid {INK}; border-radius:18px; padding:12px;
      text-align:center; font-weight:700; font-size:19px; box-shadow:0 5px 0 {INK}; margin:6px 0 12px; }}
.pickdone {{ border:3px solid {INK}; border-radius:18px; padding:12px; text-align:center;
            font-size:22px; font-weight:600; background:white; margin-bottom:10px; opacity:.6; }}
.pickdone.right {{ background:{MINT}; opacity:1; }} .pickdone.wrong {{ background:{CORAL}; color:white; opacity:1; }}
.bar {{ height:16px; background:white; border:3px solid {INK}; border-radius:999px; overflow:hidden; margin-bottom:14px; }}
.bar > div {{ height:100%; background:{MINT}; }}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# MÜFREDAT (kelime: İngilizce, Türkçe, emoji) – Maarif Modeli değerleriyle
# NOT: Üniteler MEB İngilizce öğretim programı temalarına göre hazırlanmıştır;
# resmi program ile karşılaştırıp kolayca düzenleyebilirsiniz.
# ------------------------------------------------------------------
def U(uid, title, tr, icon, value, words, sents):
    return dict(id=uid, title=title, tr=tr, icon=icon, value=value,
                words=[dict(en=a, tr=b, e=c) for a, b, c in words],
                sents=[dict(tr=a, words=b.split()) for a, b in sents])


GRADES = {
    "k": dict(title="Anaokulu", icon="🎨", color=SUN, desc="Renkler, hayvanlar, sayılar, duygular", units=[
        U("k1", "Colors", "Renkler", "🌈", "Doğa sevgisi",
          [("Red", "Kırmızı", "🔴"), ("Blue", "Mavi", "🔵"), ("Yellow", "Sarı", "🟡"),
           ("Green", "Yeşil", "🟢"), ("Orange", "Turuncu", "🟠"), ("Purple", "Mor", "🟣")],
          [("Gökyüzü mavidir.", "The sky is blue"), ("Elma kırmızıdır.", "The apple is red")]),
        U("k2", "Animals", "Hayvanlar", "🦁", "Hayvan sevgisi",
          [("Cat", "Kedi", "🐱"), ("Dog", "Köpek", "🐶"), ("Lion", "Aslan", "🦁"),
           ("Elephant", "Fil", "🐘"), ("Rabbit", "Tavşan", "🐰"), ("Bird", "Kuş", "🐦")],
          [("Bu bir kedi.", "This is a cat"), ("Aslan büyük.", "The lion is big")]),
        U("k3", "Numbers", "Sayılar", "🔢", "Çalışkanlık",
          [("One", "Bir", "1️⃣"), ("Two", "İki", "2️⃣"), ("Three", "Üç", "3️⃣"),
           ("Four", "Dört", "4️⃣"), ("Five", "Beş", "5️⃣"), ("Six", "Altı", "6️⃣")],
          [("Üç elma var.", "I have three apples"), ("Beş kuş.", "Five little birds")]),
        U("k4", "Feelings", "Duygular", "😊", "Empati",
          [("Happy", "Mutlu", "😊"), ("Sad", "Üzgün", "😢"), ("Angry", "Kızgın", "😠"),
           ("Sleepy", "Uykulu", "😴"), ("Scared", "Korkmuş", "😨"), ("Surprised", "Şaşırmış", "😲")],
          [("Ben mutluyum.", "I am happy"), ("O üzgün.", "She is sad")]),
    ]),
    "1": dict(title="1. Sınıf", icon="🎒", color=SKY, desc="Selamlaşma, aile, sınıf, meyveler", units=[
        U("a1", "Hello!", "Selamlaşma", "👋", "Saygı",
          [("Hello", "Merhaba", "🙋"), ("Goodbye", "Hoşça kal", "👋"), ("Thanks", "Teşekkürler", "🙏"),
           ("Please", "Lütfen", "🤲"), ("Sorry", "Özür dilerim", "😔"), ("Friend", "Arkadaş", "🧑‍🤝‍🧑")],
          [("Merhaba, nasılsın?", "Hello how are you"), ("Teşekkür ederim.", "Thank you my friend")]),
        U("a2", "My Family", "Ailem", "👨‍👩‍👧", "Sevgi ve aile bağı",
          [("Mother", "Anne", "👩"), ("Father", "Baba", "👨"), ("Sister", "Kız kardeş", "👧"),
           ("Brother", "Erkek kardeş", "👦"), ("Grandma", "Babaanne / Nine", "👵"), ("Grandpa", "Dede", "👴")],
          [("Bu benim annem.", "This is my mother"), ("Babam çok iyi.", "My father is good")]),
        U("a3", "Classroom", "Sınıf Eşyaları", "✏️", "Sorumluluk",
          [("Pencil", "Kalem", "✏️"), ("Book", "Kitap", "📖"), ("Bag", "Çanta", "🎒"),
           ("Ruler", "Cetvel", "📏"), ("Scissors", "Makas", "✂️"), ("Pen", "Tükenmez kalem", "🖊️")],
          [("Bu benim kalemim.", "This is my pencil"), ("Kitabını aç.", "Open your book")]),
        U("a4", "Fruits", "Meyveler", "🍎", "Sağlıklı yaşam",
          [("Apple", "Elma", "🍎"), ("Banana", "Muz", "🍌"), ("Strawberry", "Çilek", "🍓"),
           ("Orange", "Portakal", "🍊"), ("Grapes", "Üzüm", "🍇"), ("Watermelon", "Karpuz", "🍉")],
          [("Elma severim.", "I like apples"), ("Muz sarıdır.", "The banana is yellow")]),
    ]),
    "2": dict(title="2. Sınıf", icon="🚀", color=MINT, desc="Vücudum, oyuncaklar, yiyecek, hava", units=[
        U("b1", "My Body", "Vücudum", "🖐️", "Sağlık ve temizlik",
          [("Eye", "Göz", "👁️"), ("Ear", "Kulak", "👂"), ("Nose", "Burun", "👃"),
           ("Mouth", "Ağız", "👄"), ("Hand", "El", "🖐️"), ("Foot", "Ayak", "🦶")],
          [("Gözlerim mavi.", "My eyes are blue"), ("Elini yıka.", "Wash your hand")]),
        U("b2", "Toys", "Oyuncaklar", "🧸", "Paylaşma",
          [("Ball", "Top", "⚽"), ("Doll", "Bebek", "🪆"), ("Kite", "Uçurtma", "🪁"),
           ("Teddy bear", "Oyuncak ayı", "🧸"), ("Car", "Araba", "🚗"), ("Robot", "Robot", "🤖")],
          [("Topum var.", "I have a ball"), ("Oyuncağını paylaş.", "Share your toy")]),
        U("b3", "Food", "Yiyecekler", "🍞", "Şükran ve israf etmeme",
          [("Bread", "Ekmek", "🍞"), ("Milk", "Süt", "🥛"), ("Cheese", "Peynir", "🧀"),
           ("Egg", "Yumurta", "🥚"), ("Rice", "Pilav", "🍚"), ("Water", "Su", "💧")],
          [("Süt içerim.", "I drink milk"), ("Ekmek severim.", "I like bread")]),
        U("b4", "Weather", "Hava Durumu", "☀️", "Çevre bilinci",
          [("Sunny", "Güneşli", "☀️"), ("Rainy", "Yağmurlu", "🌧️"), ("Snowy", "Karlı", "❄️"),
           ("Windy", "Rüzgarlı", "💨"), ("Cloudy", "Bulutlu", "☁️"), ("Hot", "Sıcak", "🥵")],
          [("Hava güneşli.", "It is sunny"), ("Bugün yağmurlu.", "It is rainy today")]),
    ]),
}
ALL_WORDS = [w for g in GRADES.values() for u in g["units"] for w in u["words"]]

# ------------------------------------------------------------------
# STATE
# ------------------------------------------------------------------
DEFAULTS = dict(screen="home", grade="k", unit=None, phase="learn", stars={}, xp=0, streak=1,
                qs=[], qi=0, score=0, picked=None, built=[], pool=[], checked=False, ok=False,
                msg="Merhaba! Ben LinCat 🐱 Hadi birlikte öğrenelim!")
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state


def say(m):
    S.msg = m


def go(screen, **kw):
    S.screen = screen
    for k, v in kw.items():
        S[k] = v


def speak_html(text, label="🔊 Dinle", autoplay=False):
    t = json.dumps(text)
    auto = f"setTimeout(()=>say(),300);" if autoplay else ""
    components.html(
        f"""<button id=b style="font:600 17px Fredoka,Arial;background:#FFD23F;color:#2B2D6E;border:3px solid #2B2D6E;
        border-radius:16px;padding:6px 18px;box-shadow:0 4px 0 #2B2D6E;cursor:pointer">{label}</button>
        <script>function say(){{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance({t});u.lang='en-US';u.rate=.85;speechSynthesis.speak(u);}}
        document.getElementById('b').onclick=say;{auto}</script>""",
        height=56,
    )


def flashcards(unit, color):
    cards = "".join(
        f"""<div class=c onclick="flip(this,{json.dumps(w['en'])})"><div class=f><div class=e>{w['e']}</div>
        <div class=n>{w['en']}</div><div class=h>dokun 👆</div></div><div class=bk><div class=n>{w['tr']}</div>
        <div class=h>{w['en']}</div></div></div>""" for w in unit["words"])
    rows = math.ceil(len(unit["words"]) / 2)
    components.html(
        f"""<style>body{{margin:0;font-family:Fredoka,Arial,sans-serif}}
        .g{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;padding:4px 4px 10px}}
        .c{{perspective:700px;height:150px;cursor:pointer}}
        .f,.bk{{position:absolute;inset:0;border:3px solid #2B2D6E;border-radius:22px;box-shadow:0 5px 0 #2B2D6E;
        display:flex;flex-direction:column;align-items:center;justify-content:center;backface-visibility:hidden;
        transition:transform .45s;color:#2B2D6E}}
        .c{{position:relative}} .f{{background:{color}}} .bk{{background:#fff;transform:rotateY(180deg)}}
        .c.on .f{{transform:rotateY(180deg)}} .c.on .bk{{transform:rotateY(360deg)}}
        .e{{font-size:58px;line-height:1}} .n{{font-size:24px;font-weight:700}} .h{{font-size:13px;opacity:.7}}</style>
        <div class=g>{cards}</div>
        <script>function flip(el,t){{el.classList.toggle('on');speechSynthesis.cancel();
        const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=.85;speechSynthesis.speak(u);}}</script>""",
        height=rows * 170 + 20,
    )


def current_unit():
    return S.unit


def start_unit(unit):
    words = unit["words"][:]
    random.shuffle(words)
    qs = []
    for w in words:
        pool = [x for x in unit["words"] if x is not w] + random.sample(ALL_WORDS, 4)
        pool = [x for x in {p["en"]: p for p in pool}.values() if x["en"] != w["en"]]
        random.shuffle(pool)
        wrong = pool[:3]
        qs.append(dict(k="see", w=w, opts=random.sample([w["en"]] + [x["en"] for x in wrong], 4)))
        qs.append(dict(k="hear", w=w, opts=random.sample([w["e"]] + [x["e"] for x in wrong], 4)))
    random.shuffle(qs)
    qs = qs[:8] + [dict(k="sent", s=s) for s in unit["sents"]]
    go("unit", unit=unit, phase="learn", qs=qs, qi=0, score=0, picked=None, built=[], pool=[], checked=False)
    say(f"{unit['title']} zamanı! Değerimiz: {unit['value']} 💛")


def choose(opt, correct):
    S.picked = opt
    S.ok = opt == correct
    if S.ok:
        S.score += 1
        say(random.choice(["Süpersin! 🎉", "Harika! 🌟", "Bravo! 🐾", "Tam isabet! 🎯"]))
    else:
        say("Önemli değil, birlikte tekrar edelim! 💪")


def next_q():
    S.qi += 1
    S.picked, S.checked, S.built, S.pool = None, False, [], []
    if S.qi >= len(S.qs):
        S.phase = "result"


def pick_word(i):
    S.built.append(S.pool.pop(i))


def check_sentence(target):
    S.checked = True
    S.ok = [w.lower() for w in S.built] == [w.lower() for w in target]
    if S.ok:
        S.score += 1
        say("Cümleyi kusursuz kurdun! 🏆")
    else:
        say("Biraz daha dene, yapabilirsin! 🐱")


# ------------------------------------------------------------------
# ÜST PANEL
# ------------------------------------------------------------------
total_stars = sum(S.stars.values())
player_level = S.xp // 50 + 1
st.markdown(
    f"""<div class=brand>🐱 Lingo<b>Cat</b></div>
    <div class=chips><span class=chip>🔥 {S.streak} gün</span><span class=chip>⭐ {total_stars}</span>
    <span class=chip>⚡ {S.xp} XP</span><span class=chip>🏅 Seviye {player_level}</span></div>
    <div class=bubble><div class=cat>🐱</div><div class=msg>{S.msg}</div></div>""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# EKRANLAR
# ------------------------------------------------------------------
if S.screen == "home":
    st.markdown("### Sınıfını seç")
    for key, g in GRADES.items():
        st.markdown(
            f"<div class=gcard style='background:{g['color']}'><div class=ic>{g['icon']}</div>"
            f"<h3>{g['title']}</h3><p>{g['desc']}</p></div>", unsafe_allow_html=True)
        st.button(f"{g['title']} başla", key=f"g_{key}", type="primary", use_container_width=True,
                  on_click=lambda k=key: (go("map", grade=k), say("Bir macera seç, haydi başlayalım!")))
        st.write("")

elif S.screen == "map":
    g = GRADES[S.grade]
    st.button("⬅ Sınıflar", on_click=lambda: go("home"))
    st.markdown(f"## {g['icon']} {g['title']}")
    for u in g["units"]:
        n = S.stars.get(u["id"], 0)
        st.markdown(
            f"<div class=unit><div class=t>{u['icon']} {u['title']} <span style='font-weight:400'>· {u['tr']}</span></div>"
            f"<div class=v>Maarif değeri: {u['value']}</div><div>{'⭐' * n + '☆' * (3 - n)}</div></div>",
            unsafe_allow_html=True)
        st.button("Oyna", key=f"u_{u['id']}", type="primary", use_container_width=True,
                  on_click=start_unit, args=(u,))
        st.write("")

elif S.screen == "unit":
    u = S.unit
    g = GRADES[S.grade]
    st.button("🗺️ Harita", on_click=lambda: go("map"))

    # ---- ÖĞREN ----
    if S.phase == "learn":
        st.markdown(f"## {u['icon']} {u['title']}")
        st.caption(f"💛 Değerimiz: {u['value']} · Kartlara dokun: çevir ve dinle")
        flashcards(u, g["color"])
        st.button("🎮 Hazırım, oyna!", type="primary", use_container_width=True,
                  on_click=lambda: (S.__setitem__("phase", "quiz"), say("Oyun başladı!")))

    # ---- OYUN ----
    elif S.phase == "quiz":
        q = S.qs[S.qi]
        st.markdown(f"<div class=bar><div style='width:{S.qi / len(S.qs) * 100}%'></div></div>",
                    unsafe_allow_html=True)

        if q["k"] in ("see", "hear"):
            w = q["w"]
            if q["k"] == "see":
                st.markdown(f"<div class=stage><div class=big>{w['e']}</div>"
                            f"<div class=q>Bu İngilizce ne?</div></div>", unsafe_allow_html=True)
                correct = w["en"]
            else:
                st.markdown("<div class=stage><div class=q>🎧 Dinle ve doğru resmi seç</div></div>",
                            unsafe_allow_html=True)
                correct = w["e"]
            speak_html(w["en"], autoplay=(q["k"] == "hear" and S.picked is None))

            cols = st.columns(2)
            for i, opt in enumerate(q["opts"]):
                with cols[i % 2]:
                    if S.picked is None:
                        st.button(opt, key=f"o{S.qi}_{i}", use_container_width=True,
                                  on_click=choose, args=(opt, correct))
                    else:
                        cls = "right" if opt == correct else ("wrong" if opt == S.picked else "")
                        st.markdown(f"<div class='pickdone {cls}'>{opt}</div>", unsafe_allow_html=True)
            if S.picked is not None:
                st.markdown(f"<div class={'ok' if S.ok else 'no'}>"
                            f"{'Doğru! ' if S.ok else 'Doğrusu: '}{w['en']} = {w['tr']} {w['e']}</div>",
                            unsafe_allow_html=True)
                if S.ok:
                    st.balloons() if S.score == len(S.qs) else None
                st.button("Devam ➡️", type="primary", use_container_width=True, on_click=next_q)

        else:  # cümle kurma
            s = q["s"]
            if not S.pool and not S.built and not S.checked:
                S.pool = random.sample(s["words"], len(s["words"]))
            st.markdown(f"<div class=stage><div class=q>🧩 İngilizce söyle</div>"
                        f"<h2>🇹🇷 {s['tr']}</h2></div>", unsafe_allow_html=True)
            st.markdown(f"<div class=sentence>{' '.join(S.built) or '···'}</div>", unsafe_allow_html=True)
            if not S.checked:
                cols = st.columns(min(len(S.pool), 4) or 1)
                for i, w in enumerate(S.pool):
                    with cols[i % len(cols)]:
                        st.button(w, key=f"w{S.qi}_{i}_{w}", use_container_width=True,
                                  on_click=pick_word, args=(i,))
                a, b = st.columns(2)
                a.button("↩️ Sıfırla", use_container_width=True,
                         on_click=lambda: (S.__setitem__("pool", random.sample(s["words"], len(s["words"]))),
                                           S.__setitem__("built", [])))
                b.button("✅ Kontrol", type="primary", use_container_width=True,
                         disabled=len(S.built) == 0, on_click=check_sentence, args=(s["words"],))
            else:
                target = " ".join(s["words"])
                st.markdown(f"<div class={'ok' if S.ok else 'no'}>"
                            f"{'Mükemmel cümle! 🌟' if S.ok else 'Doğrusu: ' + target}</div>",
                            unsafe_allow_html=True)
                speak_html(target)
                st.button("Devam ➡️", type="primary", use_container_width=True, on_click=next_q)

    # ---- SONUÇ ----
    elif S.phase == "result":
        total = len(S.qs)
        ratio = S.score / total
        stars = 3 if ratio >= 0.8 else 2 if ratio >= 0.5 else 1
        if S.stars.get(u["id"], 0) < stars:
            gain = S.score * 5 + stars * 10
            S.xp += gain
            S.stars[u["id"]] = stars
        say("Tebrikler! LinCat seninle gurur duyuyor! 🏆")
        if stars == 3:
            st.balloons()
        st.markdown(
            f"<div class=stage><div class=big>{'⭐' * stars}</div><h2>{S.score} / {total} doğru</h2>"
            f"<p>💛 Bu ünitenin değeri: <b>{u['value']}</b></p></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("🔁 Tekrar oyna", use_container_width=True, on_click=start_unit, args=(u,))
        c2.button("🗺️ Haritaya dön", type="primary", use_container_width=True, on_click=lambda: go("map"))
