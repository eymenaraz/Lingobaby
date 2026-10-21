import base64
import csv
import io
import json
import os
import random
from datetime import date, timedelta

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LingoNest", page_icon="🪺", layout="centered")

TWIG, EGG, SUN, SKY, LEAF, CORAL, INK = "#8B5E3C", "#FFF4DC", "#FFC93C", "#4DB6E5", "#6BCB77", "#FF7A59", "#2F3A4A"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&display=swap');
html,body,.stApp,button,input{font-family:'Baloo 2',sans-serif!important}
.stApp{background:linear-gradient(180deg,#DFF4FF 0,#FFF9EC 280px,#FFF9EC 100%);color:#2F3A4A}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important}
.block-container{max-width:560px;padding:.8rem 1rem 3rem}
h1,h2,h3,p,span,label,div{color:#2F3A4A}
div[data-testid="stHorizontalBlock"]{flex-direction:row!important;flex-wrap:nowrap!important;gap:.5rem!important}
div[data-testid="stColumn"],div[data-testid="column"]{min-width:0!important}
.stButton>button,.stDownloadButton>button{font-weight:700;font-size:16px;border-radius:999px;border:0;background:#fff;color:#2F3A4A;
 padding:.55rem 1rem;box-shadow:0 3px 0 #E4D7BD,0 6px 14px rgba(139,94,60,.12);transition:transform .08s,box-shadow .08s}
.stButton>button:hover{background:#FFFDF6;color:#2F3A4A}
.stButton>button:active{transform:translateY(3px);box-shadow:0 0 0 #E4D7BD}
.stButton>button[kind="primary"],.stButton button[data-testid="stBaseButton-primary"]{background:#FF7A59;color:#fff;box-shadow:0 3px 0 #D95A3A,0 6px 14px rgba(255,122,89,.3)}
.stButton>button[kind="primary"]:hover,.stButton button[data-testid="stBaseButton-primary"]:hover{background:#FF8A6C;color:#fff}
.stButton>button:disabled{opacity:.5}
button[data-baseweb="tab"] p{font-weight:700;font-size:16px}
div[data-baseweb="tab-highlight"]{background:#FF7A59!important}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.bd{display:flex;align-items:center;gap:8px;font-size:28px;font-weight:800;color:#8B5E3C}.bd b{color:#FF7A59}
.chips{display:flex;gap:6px}.ch{display:flex;align-items:center;gap:4px;font-weight:700;font-size:15px;padding:2px 10px;border-radius:999px;background:#fff;box-shadow:0 2px 6px rgba(139,94,60,.15)}
.ch.rk{background:#8B5E3C;color:#fff}.ch.rk *{color:#fff}
.scene{border-radius:28px;overflow:hidden;box-shadow:0 8px 20px rgba(139,94,60,.18);margin:6px 0 10px}
.stg{display:flex;justify-content:space-between;background:#fff;border-radius:20px;padding:8px 10px;margin-bottom:10px;box-shadow:0 2px 8px rgba(139,94,60,.12)}
.stg div{text-align:center;font-weight:700;font-size:12px}.stg b{display:block;font-size:18px}
.card{background:#fff;border-radius:22px;padding:12px 14px;margin-bottom:6px;box-shadow:0 3px 0 #E4D7BD,0 6px 14px rgba(139,94,60,.1);text-align:center}
.card .t{font-size:19px;font-weight:800}.card small{display:block;color:#8A7A66;font-weight:600}
.art{background:#fff;border-radius:28px;padding:18px;text-align:center;margin:6px 0 10px;box-shadow:inset 0 0 0 3px #FFE7A8}
.art img{filter:drop-shadow(0 8px 4px rgba(0,0,0,.1))}
.ask{font-size:21px;font-weight:800;margin:4px 0 8px}
.opt{border-radius:18px;padding:12px 6px;text-align:center;font-weight:700;font-size:18px;background:#fff;margin-bottom:6px;min-height:52px;
 display:flex;align-items:center;justify-content:center;box-shadow:0 3px 0 #E4D7BD}
.opt.right{background:#DDF8E0;box-shadow:0 3px 0 #6BCB77;color:#2A8A3A}.opt.wrong{background:#FFE1D9;box-shadow:0 3px 0 #FF7A59;color:#C8452A;animation:shake .35s}
.opt.dim{opacity:.45}
.sheet{display:flex;gap:12px;align-items:center;border-radius:20px;padding:12px 16px;margin:10px 0;animation:pop .25s ease-out}
.sheet.ok{background:#DDF8E0;color:#2A8A3A}.sheet.no{background:#FFE1D9;color:#C8452A}
.sheet b{font-size:20px;font-weight:800;color:inherit}.sheet span{font-weight:600;color:inherit}
.bar{height:14px;background:#EFE3C8;border-radius:99px;overflow:hidden;margin:4px 0 10px}
.bar>div{height:100%;background:#6BCB77;border-radius:99px;transition:width .4s}
.built{min-height:60px;border-bottom:3px dashed #E4D7BD;display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:6px 2px;margin:6px 0 14px}
.w{background:#fff;border-radius:12px;padding:5px 12px;font-weight:700;font-size:19px;box-shadow:0 2px 0 #E4D7BD}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:8px 0}
.tile{background:#fff;border-radius:18px;padding:10px 14px;box-shadow:0 2px 8px rgba(139,94,60,.12)}.tile b{display:block;font-size:26px;font-weight:800}
.tile span{font-weight:600;color:#8A7A66;font-size:13px}
.chart{display:flex;gap:8px;height:170px;align-items:flex-end;border-bottom:3px solid #E4D7BD;padding:0 4px 4px;margin:10px 0 28px}
.cc{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;position:relative}
.cc i{display:block;width:100%;border-radius:8px 8px 2px 2px;background:#FFD98A}.cc.t i{background:#FF7A59}
.cc em{font-style:normal;font-weight:700;font-size:12px;color:#8A7A66}.cc span{position:absolute;bottom:-26px;font-weight:700;font-size:12px;color:#8A7A66}
.row{display:flex;align-items:center;gap:10px;background:#fff;border-radius:16px;padding:8px 12px;margin-bottom:6px;font-weight:700}
.row .bar{flex:1;margin:0}.row small{color:#8A7A66;font-weight:600}
.hatch{display:flex;align-items:center;justify-content:center;gap:8px;background:#fff;border-radius:18px;padding:8px;margin:6px 0;font-weight:700;animation:pop .5s}
.hatch .arr{font-size:22px;color:#FF7A59}.hatch .up{animation:bob 1.2s ease-in-out infinite}
.big{text-align:center}.big h1{font-size:32px;font-weight:800;margin:4px 0}
@keyframes pop{0%{transform:scale(.85);opacity:0}100%{transform:scale(1);opacity:1}}
@keyframes shake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
@keyframes bob{50%{transform:translateY(-6px)}}
.bob{animation:bob 1.6s ease-in-out infinite;display:inline-block}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# GÖRSELLER (vektör): Twemoji, özel çizilen renk/sayı/kuş/yuva sahnesi
# Kendi görsellerin için IMG_OVERRIDE'a  "kelime id": "https://..."  ekle.
# ------------------------------------------------------------------
TW = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{}.svg"
IMG_OVERRIDE = {}


def tw(e, px=64):
    cp = "-".join(f"{ord(c):x}" for c in e if ord(c) != 0xFE0F)
    return (f'<img src="{TW.format(cp)}" width="{px}" height="{px}" alt="" '
            f'onerror="this.outerHTML=\'<span style=font-size:{int(px * .8)}px>{e}</span>\'">')


def pic(e, px=96):
    if e.startswith(("http", "data:")):
        return f'<img src="{e}" width="{px}" height="{px}" style="object-fit:cover;border-radius:18px">'
    if e.startswith("col:"):
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100"><path d="M50 8c18-2 40 10 42 32 2 20-10 30-8 44-2 10-24 12-40 8'
                f'C26 88 8 78 8 58 6 36 28 10 50 8z" fill="{e[4:]}"/><ellipse cx="34" cy="30" rx="13" ry="7" fill="#fff" opacity=".45" '
                f'transform="rotate(-30 34 30)"/></svg>')
    if e.startswith("num:"):
        n = e[4:]
        c = [SKY, LEAF, CORAL, "#CE82FF", SUN, TWIG][int(n) % 6]
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100"><circle cx="50" cy="54" r="42" fill="rgba(0,0,0,.12)"/>'
                f'<circle cx="50" cy="48" r="42" fill="{c}"/><circle cx="36" cy="32" r="9" fill="#fff" opacity=".35"/>'
                f'<text x="50" y="68" text-anchor="middle" font-size="58" font-weight="800" fill="#fff" font-family="Baloo 2,Arial">{n}</text></svg>')
    return tw(e, px)


def chick(px=48, sad=False):
    mouth = f'<path d="M52 78 q8 -7 16 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>' if sad else ""
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 120 120"><path d="M52 14 q4 -10 8 0 q4 -10 8 0 q-8 8 -16 0z" fill="{CORAL}"/>'
            f'<circle cx="60" cy="64" r="46" fill="{SUN}"/><ellipse cx="22" cy="72" rx="12" ry="18" fill="#F5B52B" transform="rotate(20 22 72)"/>'
            f'<ellipse cx="98" cy="72" rx="12" ry="18" fill="#F5B52B" transform="rotate(-20 98 72)"/>'
            f'<circle cx="42" cy="56" r="7" fill="{INK}"/><circle cx="78" cy="56" r="7" fill="{INK}"/>'
            f'<circle cx="44" cy="53" r="2.5" fill="#fff"/><circle cx="80" cy="53" r="2.5" fill="#fff"/>'
            f'<path d="M50 68 h20 l-10 12z" fill="{CORAL}"/><circle cx="30" cy="72" r="6" fill="#FFAB91" opacity=".6"/>'
            f'<circle cx="90" cy="72" r="6" fill="#FFAB91" opacity=".6"/>{mouth}</svg>')


STAGES = [("Yumurta", "🥚"), ("Çatlıyor", "🐣"), ("Civciv", "🐥"), ("Kuş", "🐦"), ("Usta kuş", "🦜")]
INTERVALS = [0, 1, 2, 4, 7]  # Leitner kutuları: bakım aralığı (gün)


def creature(b, x, y):
    eye = lambda dx: f'<circle cx="{x + dx}" cy="{y - 3}" r="2.2" fill="{INK}"/>'
    egg = f'<ellipse cx="{x}" cy="{y}" rx="12" ry="15" fill="{EGG}" stroke="#E6D3A8" stroke-width="2"/>'
    if b == 0:
        return egg + f'<circle cx="{x - 4}" cy="{y - 4}" r="2" fill="#F2C48D"/><circle cx="{x + 4}" cy="{y + 5}" r="2.5" fill="#F2C48D"/>'
    if b == 1:
        return (f'<circle cx="{x}" cy="{y - 12}" r="6" fill="{SUN}"/>' + egg +
                f'<path d="M{x - 11} {y - 2} l5 -5 l5 5 l5 -5 l5 5 l4 -4" stroke="{TWIG}" stroke-width="2" fill="none"/>')
    if b == 2:
        return (f'<circle cx="{x}" cy="{y}" r="13" fill="{SUN}"/>{eye(4)}<path d="M{x + 11} {y} l8 3 l-8 3z" fill="{CORAL}"/>'
                f'<path d="M{x - 3} {y - 13} q2 -6 5 0z" fill="{CORAL}"/>')
    if b == 3:
        return (f'<path d="M{x - 14} {y + 2} l-10 -4 l2 10z" fill="#2E94C4"/><ellipse cx="{x}" cy="{y}" rx="15" ry="12" fill="{SKY}"/>'
                f'<ellipse cx="{x - 3}" cy="{y + 3}" rx="8" ry="5" fill="#2E94C4"/>{eye(7)}<path d="M{x + 14} {y - 2} l7 3 l-7 3z" fill="{SUN}"/>')
    return (f'<path d="M{x - 14} {y + 2} l-12 -6 l2 12z" fill="{SUN}"/><ellipse cx="{x}" cy="{y}" rx="15" ry="12" fill="{CORAL}"/>'
            f'<path d="M{x - 2} {y - 11} l3 -9 l3 9z M{x + 4} {y - 10} l6 -8 l1 10z" fill="{SUN}"/>'
            f'<ellipse cx="{x - 3}" cy="{y + 3}" rx="8" ry="5" fill="#E0573A"/>{eye(7)}<path d="M{x + 14} {y - 2} l7 3 l-7 3z" fill="{SUN}"/>')


def nest_svg(boxes):
    slots = [(125, 128), (155, 124), (185, 124), (215, 128), (110, 150), (140, 148), (170, 148), (200, 148), (230, 150)]
    boxes = sorted(boxes, reverse=True)[:len(slots)]
    items = "".join(creature(b, *slots[i]) for i, b in enumerate(boxes))
    empty = "" if boxes else f'<text x="180" y="132" text-anchor="middle" font-size="14" font-weight="700" fill="{TWIG}">Yuvan boş, ilk kelimeni topla</text>'
    return (f'<div class="scene"><svg viewBox="0 0 360 230" width="100%"><rect width="360" height="230" fill="#BFE8FF"/>'
            f'<circle cx="300" cy="44" r="26" fill="{SUN}"/><ellipse cx="70" cy="46" rx="34" ry="12" fill="#fff"/><ellipse cx="92" cy="40" rx="22" ry="10" fill="#fff"/>'
            f'<rect x="0" y="176" width="360" height="54" fill="{LEAF}"/><rect x="0" y="168" width="360" height="14" rx="7" fill="{TWIG}"/>'
            f'<ellipse cx="180" cy="150" rx="84" ry="30" fill="#6B4527"/>{items}{empty}'
            f'<path d="M92 148 q88 70 176 0 v14 q-88 70 -176 0z" fill="{TWIG}"/><path d="M104 160 q76 44 152 0" stroke="#B98A5E" stroke-width="3" fill="none"/>'
            f'<path d="M120 172 q60 28 120 0" stroke="#B98A5E" stroke-width="3" fill="none"/>'
            f'<ellipse cx="40" cy="156" rx="16" ry="8" fill="#4FB360" transform="rotate(-30 40 156)"/><ellipse cx="330" cy="158" rx="16" ry="8" fill="#4FB360" transform="rotate(30 330 158)"/></svg></div>')


# ------------------------------------------------------------------
# MÜFREDAT (Anaokulu, 1. ve 2. sınıf temaları)
# ------------------------------------------------------------------
def art(w):
    return "an" if w[0].lower() in "aeiou" else "a"


def U(uid, title, tr, ic, tpl, words, sents):
    ws = []
    for i, t in enumerate(words):
        en, trk, e = t[:3]
        s = t[3] if len(t) > 3 else tpl.format(w=en.lower(), A=f"{art(en)} {en.lower()}")
        ws.append(dict(id=f"{uid}{i}", en=en, tr=trk, e=IMG_OVERRIDE.get(f"{uid}{i}", e), s=s[0].upper() + s[1:], u=uid))
    return dict(id=uid, title=title, tr=tr, ic=ic, words=ws, sents=[dict(tr=a, words=b.split()) for a, b in sents])


GRADES = {
    "k": dict(title="Anaokulu", units=[
        U("k1", "Colors", "Renkler", "🎨", "It is {w}.",
          [("Red", "Kırmızı", "col:#FF4B4B"), ("Blue", "Mavi", "col:#1CB0F6"), ("Yellow", "Sarı", "col:#FFC800"),
           ("Green", "Yeşil", "col:#58CC02"), ("Orange", "Turuncu", "col:#FF9600"), ("Purple", "Mor", "col:#CE82FF")],
          [("Gökyüzü mavidir.", "The sky is blue"), ("Elma kırmızıdır.", "The apple is red")]),
        U("k2", "Animals", "Hayvanlar", "🦁", "I see {A}.",
          [("Cat", "Kedi", "🐱"), ("Dog", "Köpek", "🐶"), ("Lion", "Aslan", "🦁"),
           ("Elephant", "Fil", "🐘"), ("Rabbit", "Tavşan", "🐰"), ("Fish", "Balık", "🐟")],
          [("Bu bir kedi.", "This is a cat"), ("Aslan büyük.", "The lion is big")]),
        U("k3", "Numbers", "Sayılar", "🔢", "I can count to {w}.",
          [("One", "Bir", "num:1"), ("Two", "İki", "num:2"), ("Three", "Üç", "num:3"),
           ("Four", "Dört", "num:4"), ("Five", "Beş", "num:5"), ("Six", "Altı", "num:6")],
          [("Üç elma var.", "I have three apples"), ("Beş kuş.", "Five little birds")]),
        U("k4", "Feelings", "Duygular", "😊", "I am {w}.",
          [("Happy", "Mutlu", "😊"), ("Sad", "Üzgün", "😢"), ("Angry", "Kızgın", "😠"),
           ("Sleepy", "Uykulu", "😴"), ("Scared", "Korkmuş", "😨"), ("Surprised", "Şaşırmış", "😲")],
          [("Ben mutluyum.", "I am happy"), ("O üzgün.", "She is sad")]),
    ]),
    "1": dict(title="1. Sınıf", units=[
        U("a1", "Hello!", "Selamlaşma", "👋", "",
          [("Hello", "Merhaba", "🙋", "Hello, my friend!"), ("Goodbye", "Hoşça kal", "👋", "Goodbye, see you!"),
           ("Thanks", "Teşekkürler", "🙏", "Thanks a lot!"), ("Please", "Lütfen", "🤲", "Help me, please."),
           ("Sorry", "Özür dilerim", "😔", "I am sorry."), ("Friend", "Arkadaş", "🧑‍🤝‍🧑", "You are my friend.")],
          [("Merhaba, nasılsın?", "Hello how are you"), ("Teşekkür ederim.", "Thank you my friend")]),
        U("a2", "My Family", "Ailem", "👨‍👩‍👧", "This is my {w}.",
          [("Mother", "Anne", "👩"), ("Father", "Baba", "👨"), ("Sister", "Kız kardeş", "👧"),
           ("Brother", "Erkek kardeş", "👦"), ("Grandma", "Nine", "👵"), ("Grandpa", "Dede", "👴")],
          [("Bu benim annem.", "This is my mother"), ("Babam çok iyi.", "My father is good")]),
        U("a3", "Classroom", "Sınıf Eşyaları", "🎒", "This is my {w}.",
          [("Pencil", "Kalem", "✏️"), ("Book", "Kitap", "📖"), ("Bag", "Çanta", "🎒"),
           ("Ruler", "Cetvel", "📏"), ("Scissors", "Makas", "✂️"), ("Pen", "Tükenmez kalem", "🖊️")],
          [("Bu benim kalemim.", "This is my pencil"), ("Kitabını aç.", "Open your book")]),
        U("a4", "Fruits", "Meyveler", "🍎", "I eat {A}.",
          [("Apple", "Elma", "🍎"), ("Banana", "Muz", "🍌"), ("Strawberry", "Çilek", "🍓"),
           ("Orange", "Portakal", "🍊"), ("Grapes", "Üzüm", "🍇", "I eat grapes."), ("Watermelon", "Karpuz", "🍉")],
          [("Elma severim.", "I like apples"), ("Muz sarıdır.", "The banana is yellow")]),
    ]),
    "2": dict(title="2. Sınıf", units=[
        U("b1", "My Body", "Vücudum", "🖐️", "This is my {w}.",
          [("Eye", "Göz", "👁️"), ("Ear", "Kulak", "👂"), ("Nose", "Burun", "👃"),
           ("Mouth", "Ağız", "👄"), ("Hand", "El", "🖐️"), ("Foot", "Ayak", "🦶")],
          [("Gözlerim mavi.", "My eyes are blue"), ("Elini yıka.", "Wash your hand")]),
        U("b2", "Toys", "Oyuncaklar", "🧸", "I have {A}.",
          [("Ball", "Top", "⚽"), ("Doll", "Bebek", "🪆"), ("Kite", "Uçurtma", "🪁"),
           ("Teddy bear", "Oyuncak ayı", "🧸"), ("Car", "Araba", "🚗"), ("Robot", "Robot", "🤖")],
          [("Topum var.", "I have a ball"), ("Oyuncağını paylaş.", "Share your toy")]),
        U("b3", "Food", "Yiyecekler", "🍞", "I like {w}.",
          [("Bread", "Ekmek", "🍞"), ("Milk", "Süt", "🥛"), ("Cheese", "Peynir", "🧀"),
           ("Egg", "Yumurta", "🥚", "I like eggs."), ("Rice", "Pilav", "🍚"), ("Water", "Su", "💧")],
          [("Süt içerim.", "I drink milk"), ("Ekmek severim.", "I like bread")]),
        U("b4", "Weather", "Hava Durumu", "☀️", "It is {w}.",
          [("Sunny", "Güneşli", "☀️"), ("Rainy", "Yağmurlu", "🌧️"), ("Snowy", "Karlı", "❄️"),
           ("Windy", "Rüzgarlı", "💨"), ("Cloudy", "Bulutlu", "☁️"), ("Hot", "Sıcak", "🥵")],
          [("Hava güneşli.", "It is sunny"), ("Bugün yağmurlu.", "It is rainy today")]),
    ]),
}
ALL_UNITS = [u for g in GRADES.values() for u in g["units"]]
BASE_WORDS = {w["id"]: w for u in ALL_UNITS for w in u["words"]}
RANKS = [("A1", "Dal", 0), ("A2", "Yuva", 6), ("B1", "Ağaç", 16), ("B2", "Orman", 32), ("C1", "Gökyüzü", 60)]

# ------------------------------------------------------------------
# STATE
# ------------------------------------------------------------------
DEFAULTS = dict(screen="nest", unit=None, phase="learn", nest={}, custom=[], hist={}, streak=1, last_day=None,
                qs=[], qi=0, score=0, picked=None, ok=False, built=[], pool=[], checked=False, sfx=False,
                wids=[], bad=[], mode="review", res={}, story="", hunt=None)
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state
today = date.today()
if S.last_day != today.isoformat():
    S.streak = S.streak + 1 if S.last_day == (today - timedelta(1)).isoformat() else 1
    S.last_day = today.isoformat()


def W():
    return {**BASE_WORDS, **{w["id"]: w for w in S.custom}}


def go(**kw):
    for k, v in kw.items():
        S[k] = v


def mastered():
    return sum(1 for v in S.nest.values() if v["box"] >= 4)


def rank():
    m = len(S.nest) // 1
    return max(i for i, r in enumerate(RANKS) if m >= r[2])


def due_ids():
    return [i for i, v in S.nest.items() if v["due"] <= today.isoformat()]


# ------------------------------------------------------------------
# SES (gTTS) ve KONUŞMA
# ------------------------------------------------------------------
@st.cache_resource
def _audio_store():
    return {}


def mp3(text):
    d = _audio_store()
    if text not in d:
        try:
            from gtts import gTTS
            b = io.BytesIO()
            gTTS(text, lang="en").write_to_fp(b)
            d[text] = base64.b64encode(b.getvalue()).decode()
        except Exception:
            return ""
    return d[text]


def player_js(items):
    a = {k: mp3(t) for k, t in items.items()}
    return (f"const A={json.dumps(a)},T={json.dumps(items)};"
            "function play(k){speechSynthesis.cancel();if(A[k]){new Audio('data:audio/mpeg;base64,'+A[k]).play();}"
            "else{const u=new SpeechSynthesisUtterance(T[k]);u.lang='en-US';u.rate=.85;speechSynthesis.speak(u);}}")


SPK = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="#fff"><path d="M3 9v6h4l5 4V5L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4z"/>'
       '<path d="M14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z"/></svg>')
BTN = ("font:700 17px 'Baloo 2',Arial;background:#4DB6E5;color:#fff;border:0;border-radius:999px;padding:8px 22px;cursor:pointer;"
       "box-shadow:0 3px 0 #2E94C4;display:flex;gap:8px;align-items:center")


def speak_html(text, auto=False, label="Dinle"):
    components.html(
        f"""<button style="{BTN}" onclick="play('w')">{SPK}{label}</button>
        <script>{player_js({'w': text})}{"setTimeout(()=>play('w'),300);" if auto else ""}</script>""", height=56)


def flashcards(unit):
    items, cards = {}, ""
    for i, w in enumerate(unit["words"]):
        items[f"w{i}"], items[f"s{i}"] = w["en"], w["s"]
        cards += (f'<div class="c" onclick="this.classList.toggle(\'on\');play(\'w{i}\')"><div class="f">{pic(w["e"], 72)}'
                  f'<div class="n">{w["en"]}</div></div><div class="k"><div class="n">{w["tr"]}</div><div class="h">{w["s"]}</div>'
                  f'<button onclick="event.stopPropagation();play(\'s{i}\')">{SPK}</button></div></div>')
    rows = (len(unit["words"]) + 1) // 2
    components.html(
        f"""<style>body{{margin:0;font-family:'Baloo 2',Arial,sans-serif}}.g{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:2px 2px 8px}}
        .c{{position:relative;height:176px;cursor:pointer;perspective:800px}}
        .f,.k{{position:absolute;inset:0;border-radius:22px;display:flex;flex-direction:column;align-items:center;justify-content:center;
        backface-visibility:hidden;transition:transform .45s;background:#fff;color:#2F3A4A;padding:6px;text-align:center;box-shadow:0 3px 0 #E4D7BD,0 6px 14px rgba(139,94,60,.12)}}
        .f img,.f svg{{filter:drop-shadow(0 5px 3px rgba(0,0,0,.1))}}.k{{transform:rotateY(180deg);background:#8B5E3C;color:#fff}}
        .c.on .f{{transform:rotateY(180deg)}}.c.on .k{{transform:rotateY(360deg)}}
        .n{{font-size:22px;font-weight:800;margin-top:6px}}.h{{font-size:14px;font-weight:600;margin:4px 0 6px}}
        .k button{{background:rgba(255,255,255,.25);border:0;border-radius:12px;padding:6px 12px;cursor:pointer}}</style>
        <div class="g">{cards}</div><script>{player_js(items)}</script>""", height=rows * 188 + 12)


def sfx(ok):
    if S.sfx:
        S.sfx = False
        n = "[523,659,784]" if ok else "[300,220]"
        components.html(
            "<script>try{const c=new(window.AudioContext||window.webkitAudioContext)();" + n + ".forEach((f,i)=>{const o=c.createOscillator(),"
            "g=c.createGain(),t=c.currentTime+i*.12;o.type='triangle';o.frequency.value=f;o.connect(g);g.connect(c.destination);"
            "g.gain.setValueAtTime(.15,t);g.gain.exponentialRampToValueAtTime(.001,t+.2);o.start(t);o.stop(t+.25);});}catch(e){}</script>", height=0)


def speaking(words):
    rows = "".join(f'<div class="r">{pic(w["e"], 44)}<b>{w["en"]}</b><button onclick="listen({i},{json.dumps(w["en"])})">Söyle</button><span id="r{i}"></span></div>'
                   for i, w in enumerate(words))
    components.html(
        f"""<style>body{{margin:0;font-family:'Baloo 2',Arial}}.r{{display:flex;align-items:center;gap:10px;background:#fff;border-radius:18px;padding:8px 12px;margin:6px 0;
        box-shadow:0 2px 8px rgba(139,94,60,.15)}}.r b{{flex:1;font-size:20px}}button{{background:#FF7A59;color:#fff;border:0;border-radius:999px;padding:6px 16px;
        font:700 15px 'Baloo 2';cursor:pointer}}span{{font-size:13px;font-weight:700;min-width:90px}}</style>{rows}
        <script>function listen(i,t){{const R=window.SpeechRecognition||window.webkitSpeechRecognition,el=document.getElementById('r'+i);
        if(!R){{el.textContent='Bu tarayıcı desteklemiyor';return}}const r=new R();r.lang='en-US';el.textContent='Dinliyorum...';
        r.onresult=e=>{{const s=e.results[0][0].transcript.toLowerCase().trim(),ok=s.includes(t.toLowerCase());
        el.textContent=ok?'Harika! ✔':'Duydum: '+s;el.style.color=ok?'#2A8A3A':'#C8452A'}};
        r.onerror=()=>{{el.textContent='Mikrofon izni ver'}};r.start()}}</script>""", height=len(words) * 66 + 10)


# ------------------------------------------------------------------
# YAPAY ZEKÂ (isteğe bağlı: ANTHROPIC_API_KEY varsa)
# ------------------------------------------------------------------
def api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY")


def ask_ai(content, system, max_tokens=500):
    import anthropic
    try:
        model = st.secrets["ANTHROPIC_MODEL"]
    except Exception:
        model = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")
    r = anthropic.Anthropic(api_key=api_key()).messages.create(
        model=model, max_tokens=max_tokens, system=system, messages=[{"role": "user", "content": content}])
    return r.content[0].text.strip()


def make_story(words):
    en = [w["en"].lower() for w in words]
    if api_key():
        try:
            return ask_ai(f"Words: {', '.join(en)}", "Write a very short, warm, funny story (5 simple English sentences, A1 level) for a 6-8 year old "
                          "Turkish child using ALL of the given words. Use only simple present tense. Output only the story.")
        except Exception as ex:
            st.warning(f"Yapay zekâ şu an yanıt vermedi ({type(ex).__name__}). Basit hikâye gösteriliyor.")
    return " ".join(w["s"] for w in words[:5])


def identify(img_bytes):
    b64 = base64.b64encode(img_bytes).decode()
    txt = ask_ai([{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                  {"type": "text", "text": "Name the main everyday object in this photo for a child learning English. "
                   'Reply ONLY JSON: {"en":"one simple English noun","tr":"Türkçesi"}. If it is a person or unsafe, reply {"en":"","tr":""}.'}],
                 "You help children learn English words. Never describe people.", 100)
    return json.loads(txt[txt.index("{"): txt.rindex("}") + 1])


# ------------------------------------------------------------------
# OTURUM (Yuva bakımı + ünite)
# ------------------------------------------------------------------
def build_session(wids, sents, mode):
    ws, pool = W(), list(W().values())
    qs = []
    for wid in wids:
        w, seen, wrong = ws[wid], set(), []
        for x in random.sample(pool, min(len(pool), 14)):
            if x["en"] != w["en"] and x["en"] not in seen and len(wrong) < 3:
                seen.add(x["en"])
                wrong.append(x)
        for k in ("see", "hear"):
            o = [w] + wrong
            random.shuffle(o)
            qs.append(dict(k=k, w=w, opts=o))
    random.shuffle(qs)
    qs += [dict(k="sent", s=s) for s in sents]
    go(screen="play", phase="quiz", qs=qs, qi=0, score=0, picked=None, built=[], pool=[], checked=False,
       sfx=False, wids=wids, bad=[], mode=mode)


def start_review():
    ids = due_ids()
    random.shuffle(ids)
    build_session(ids[:6], [], "review")


def start_unit(unit):
    go(screen="play", phase="learn", unit=unit)


def add_to_nest():
    u = S.unit
    for w in u["words"]:
        S.nest.setdefault(w["id"], dict(box=0, due=today.isoformat(), ok=0, n=0))
    build_session([w["id"] for w in u["words"]], u["sents"], "unit")


def award(ok, wid=None):
    S.ok, S.sfx = ok, True
    S.score += int(ok)
    if wid:
        if not ok and wid not in S.bad:
            S.bad.append(wid)
        if wid in S.nest:
            S.nest[wid]["n"] += 1
            S.nest[wid]["ok"] += int(ok)
    d = S.hist.setdefault(today.isoformat(), dict(ok=0, n=0))
    d["ok"] += int(ok)
    d["n"] += 1


def choose(opt_id, correct_id):
    S.picked = opt_id
    award(opt_id == correct_id, correct_id)


def pick_word(i):
    S.built.append(S.pool.pop(i))


def check_sentence(target):
    S.checked = True
    award([w.lower() for w in S.built] == [w.lower() for w in target])


def reset_pool(words):
    S.pool, S.built = random.sample(words, len(words)), []


def next_q():
    S.qi += 1
    S.picked, S.checked, S.built, S.pool, S.sfx = None, False, [], [], False
    if S.qi >= len(S.qs):
        moves = []
        for wid in S.wids:
            v = S.nest.get(wid)
            if not v:
                continue
            old = v["box"]
            v["box"] = max(0, old - 1) if wid in S.bad else min(4, old + 1)
            v["due"] = (today + timedelta(INTERVALS[v["box"]])).isoformat()
            moves.append((wid, old, v["box"]))
        S.res = dict(moves=moves)
        S.phase = "result"


# ------------------------------------------------------------------
# ÜST PANEL
# ------------------------------------------------------------------
def head():
    r = RANKS[rank()]
    st.markdown(f"""<div class="top"><div class="bd">{chick(44)}<span>Lingo<b>Nest</b></span></div><div class="chips">
        <span class="ch">{tw('🔥', 20)}{S.streak}</span><span class="ch">{tw('🥚', 20)}{len(S.nest)}</span>
        <span class="ch rk">{r[0]}</span></div></div>""", unsafe_allow_html=True)
    cols = st.columns(4)
    for c, (k, lab, ic) in zip(cols, [("nest", "Yuva", ":material/home:"), ("explore", "Keşfet", ":material/explore:"),
                                      ("adv", "Macera", ":material/auto_awesome:"), ("panel", "Panel", ":material/bar_chart:")]):
        c.button(lab, key=f"n_{k}", icon=ic, use_container_width=True, type="primary" if S.screen == k else "secondary",
                 on_click=go, kwargs={"screen": k})


# ------------------------------------------------------------------
# EKRANLAR
# ------------------------------------------------------------------
if S.screen == "nest":
    head()
    st.markdown(nest_svg([v["box"] for v in S.nest.values()]), unsafe_allow_html=True)
    cnt = [sum(1 for v in S.nest.values() if v["box"] == b) for b in range(5)]
    st.markdown('<div class="stg">' + "".join(f'<div>{tw(e, 30)}<b>{cnt[i]}</b>{n}</div>' for i, (n, e) in enumerate(STAGES)) + "</div>",
                unsafe_allow_html=True)
    r = rank()
    nxt = RANKS[r + 1] if r + 1 < len(RANKS) else None
    pct = 100 if not nxt else int((len(S.nest) - RANKS[r][2]) / (nxt[2] - RANKS[r][2]) * 100)
    st.markdown(f'<div class="row"><b>{RANKS[r][0]} · {RANKS[r][1]}</b><div class="bar"><div style="width:{pct}%"></div></div>'
                f'<small>{f"{nxt[2] - len(S.nest)} kelime" if nxt else "Zirve"}</small></div>', unsafe_allow_html=True)
    n = len(due_ids())
    if not S.nest:
        st.button("İlk kelimelerini topla", type="primary", use_container_width=True, on_click=go, kwargs={"screen": "explore"})
    else:
        st.button(f"Yuva bakımı · {n} kelime bekliyor" if n else "Bugün bakım yok, yarın gel", type="primary",
                  use_container_width=True, disabled=n == 0, on_click=start_review)

elif S.screen == "explore":
    head()
    tabs = st.tabs([g["title"] for g in GRADES.values()])
    for tab, g in zip(tabs, GRADES.values()):
        with tab:
            cols = st.columns(2)
            for i, u in enumerate(g["units"]):
                have = sum(1 for w in u["words"] if w["id"] in S.nest)
                with cols[i % 2]:
                    st.markdown(f'<div class="card">{tw(u["ic"], 54)}<div class="t">{u["title"]}</div><small>{u["tr"]} · {have}/{len(u["words"])} yuvada</small></div>',
                                unsafe_allow_html=True)
                    st.button("Topla", key=f"u_{u['id']}", type="primary", use_container_width=True, on_click=start_unit, args=(u,))

elif S.screen == "adv":
    head()
    t1, t2, t3 = st.tabs(["Hikâye", "Kelime avı", "Konuş"])
    nest_words = [W()[i] for i in S.nest if i in W()]
    with t1:
        if len(nest_words) < 3:
            st.info("Hikâye için yuvaya en az 3 kelime topla.")
        else:
            st.button("Yuvamdan hikâye yaz", type="primary", use_container_width=True,
                      on_click=lambda: S.__setitem__("story", make_story(random.sample(nest_words, min(5, len(nest_words))))))
            if S.story:
                st.markdown(f'<div class="card" style="text-align:left;font-size:18px">{S.story}</div>', unsafe_allow_html=True)
                speak_html(S.story, label="Hikâyeyi dinle")
    with t2:
        if not api_key():
            st.info("Kelime avı için yapay zekâ anahtarı gerekir (ANTHROPIC_API_KEY). Öğretmen ayarlardan ekleyebilir.")
        else:
            shot = st.camera_input("Evdeki bir eşyanın fotoğrafını çek")
            if shot and st.button("Bu ne?", type="primary", use_container_width=True):
                try:
                    from PIL import Image
                    im = Image.open(shot).convert("RGB")
                    im.thumbnail((320, 320))
                    buf = io.BytesIO()
                    im.save(buf, "JPEG", quality=80)
                    res = identify(buf.getvalue())
                    if res.get("en"):
                        wid = f"c{len(S.custom)}"
                        w = dict(id=wid, en=res["en"].capitalize(), tr=res["tr"], s=f"This is {art(res['en'])} {res['en'].lower()}.",
                                 e="data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), u="custom")
                        S.custom.append(w)
                        S.nest[wid] = dict(box=0, due=today.isoformat(), ok=0, n=0)
                        S.hunt = w
                    else:
                        S.hunt = None
                        st.warning("Bu fotoğraftan kelime çıkaramadım, başka bir eşya dene.")
                except Exception as ex:
                    st.error(f"Olmadı ({type(ex).__name__}). Tekrar dene.")
            if S.hunt:
                w = S.hunt
                st.markdown(f'<div class="card"><div class="art">{pic(w["e"], 130)}</div><div class="t">{w["en"]} = {w["tr"]}</div><small>Yuvana yumurta olarak eklendi</small></div>',
                            unsafe_allow_html=True)
                speak_html(w["en"])
    with t3:
        pool = nest_words[:6] if nest_words else BASE_WORDS and list(BASE_WORDS.values())[:6]
        st.caption("Söyle düğmesine bas ve kelimeyi yüksek sesle söyle.")
        speaking(pool)

elif S.screen == "panel":
    head()
    days = [today - timedelta(d) for d in range(6, -1, -1)]
    H = [S.hist.get(d.isoformat(), {}) for d in days]
    vals = [h.get("n", 0) for h in H]
    mx = max(vals + [1])
    names = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    bars = "".join(f'<div class="cc {"t" if d == today else ""}"><em>{v or ""}</em><i style="height:{max(4, int(v / mx * 110))}px"></i>'
                   f'<span>{names[d.weekday()]}</span></div>' for d, v in zip(days, vals))
    ok, n = sum(h.get("ok", 0) for h in H), sum(vals)
    st.markdown(f"""<div class="grid"><div class="tile"><b>{vals[-1]}</b><span>Bugün cevap</span></div><div class="tile"><b>{n}</b><span>Haftalık cevap</span></div>
        <div class="tile"><b>%{int(ok / n * 100) if n else 0}</b><span>Haftalık doğruluk</span></div>
        <div class="tile"><b>{mastered()}/{len(S.nest)}</b><span>Usta kuş / yuvadaki</span></div></div>
        <h3>Son 7 gün</h3><div class="chart">{bars}</div><h3>Ünite gelişimi</h3>""", unsafe_allow_html=True)
    rows = ""
    for u in ALL_UNITS:
        ids = [w["id"] for w in u["words"]]
        have = sum(1 for i in ids if i in S.nest)
        m = sum(1 for i in ids if S.nest.get(i, {}).get("box", 0) >= 3)
        rows += f'<div class="row">{tw(u["ic"], 26)}<span>{u["title"]}</span><div class="bar"><div style="width:{m / len(ids) * 100}%"></div></div><small>{have}/{len(ids)}</small></div>'
    st.markdown(rows, unsafe_allow_html=True)
    hard = sorted([(v["ok"] / v["n"], i) for i, v in S.nest.items() if v["n"] >= 2])[:5]
    if hard:
        st.markdown("<h3>Zorlanılan kelimeler</h3>" + "".join(
            f'<div class="row">{pic(W()[i]["e"], 30)}<span>{W()[i]["en"]} · {W()[i]["tr"]}</span><small>%{int(p * 100)}</small></div>' for p, i in hard),
            unsafe_allow_html=True)
    buf = io.StringIO()
    cw = csv.writer(buf)
    cw.writerow(["kelime", "turkce", "unite", "kutu", "dogru", "toplam", "sonraki_bakim"])
    for i, v in S.nest.items():
        w = W()[i]
        cw.writerow([w["en"], w["tr"], w.get("u", ""), v["box"], v["ok"], v["n"], v["due"]])
    c1, c2 = st.columns(2)
    c1.download_button("Rapor (CSV)", buf.getvalue(), "lingonest_rapor.csv", use_container_width=True, icon=":material/download:")
    keys = ("nest", "custom", "hist", "streak", "last_day")
    c2.download_button("İlerleme kaydı", json.dumps({k: S[k] for k in keys}), "lingonest_ilerleme.json", use_container_width=True,
                       icon=":material/save:")
    up = st.file_uploader("Kayıtlı ilerlemeyi yükle", type="json")
    if up is not None and S.get("loaded") != up.name:
        try:
            S.update(json.loads(up.read()))
            S.loaded = up.name
            st.rerun()
        except Exception:
            st.error("Dosya okunamadı.")
    st.caption("Görseller: Twemoji, CC-BY 4.0")

elif S.screen == "play":
    st.button("Çık", icon=":material/close:", on_click=go, kwargs={"screen": "nest"})
    if S.phase == "learn":
        u = S.unit
        st.markdown(f"<h2>{tw(u['ic'], 34)} {u['title']}</h2>", unsafe_allow_html=True)
        with st.spinner("Sesler hazırlanıyor"):
            flashcards(u)
        st.button("Yuvaya ekle ve oyna", type="primary", use_container_width=True, on_click=add_to_nest)

    elif S.phase == "quiz":
        q = S.qs[S.qi]
        st.markdown(f'<div class="bar"><div style="width:{S.qi / len(S.qs) * 100}%"></div></div>', unsafe_allow_html=True)
        if q["k"] != "sent":
            w, seen = q["w"], q["k"] == "see"
            if seen:
                st.markdown(f"<p class='ask'>Bu İngilizce ne?</p><div class='art'>{pic(w['e'], 128)}</div>", unsafe_allow_html=True)
                speak_html(w["en"])
            else:
                st.markdown("<p class='ask'>Dinle, doğru resmi seç</p>", unsafe_allow_html=True)
                speak_html(w["en"], auto=S.picked is None)
            cols = st.columns(2)
            for i, o in enumerate(q["opts"]):
                with cols[i % 2]:
                    inner = o["en"] if seen else pic(o["e"], 84)
                    if S.picked is None:
                        if seen:
                            st.button(inner, key=f"o{S.qi}_{i}", use_container_width=True, on_click=choose, args=(o["id"], w["id"]))
                        else:
                            st.markdown(f"<div class='opt'>{inner}</div>", unsafe_allow_html=True)
                            st.button("Seç", key=f"o{S.qi}_{i}", use_container_width=True, on_click=choose, args=(o["id"], w["id"]))
                    else:
                        cls = "right" if o["id"] == w["id"] else "wrong" if o["id"] == S.picked else "dim"
                        st.markdown(f"<div class='opt {cls}'>{inner}</div>", unsafe_allow_html=True)
            if S.picked is not None:
                sfx(S.ok)
                st.markdown(f"<div class='sheet {'ok' if S.ok else 'no'}'>{chick(52, not S.ok)}<div><b>{random.choice(['Harika!', 'Süper!', 'Bravo!']) if S.ok else 'Doğrusu:'}</b>"
                            f"<br><span>{w['en']} = {w['tr']}</span></div></div>", unsafe_allow_html=True)
                st.button("Devam", type="primary", use_container_width=True, on_click=next_q)
        else:
            s = q["s"]
            if not S.pool and not S.built and not S.checked:
                reset_pool(s["words"])
            st.markdown(f"<p class='ask'>İngilizcesini kur</p><div class='art'><h2 style='margin:0'>{s['tr']}</h2></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='built'>{''.join(f'<span class=w>{x}</span>' for x in S.built)}</div>", unsafe_allow_html=True)
            if not S.checked:
                cols = st.columns(min(max(len(S.pool), 1), 3))
                for i, x in enumerate(S.pool):
                    cols[i % len(cols)].button(x, key=f"w{S.qi}_{i}_{x}", use_container_width=True, on_click=pick_word, args=(i,))
                a, b = st.columns(2)
                a.button("Sıfırla", icon=":material/refresh:", use_container_width=True, on_click=reset_pool, args=(s["words"],))
                b.button("Kontrol et", type="primary", use_container_width=True, disabled=not S.built, on_click=check_sentence, args=(s["words"],))
            else:
                sfx(S.ok)
                target = " ".join(s["words"])
                st.markdown(f"<div class='sheet {'ok' if S.ok else 'no'}'>{chick(52, not S.ok)}<div><b>{'Mükemmel!' if S.ok else 'Doğrusu:'}</b>"
                            f"<br><span>{target}</span></div></div>", unsafe_allow_html=True)
                speak_html(target)
                st.button("Devam", type="primary", use_container_width=True, on_click=next_q)

    elif S.phase == "result":
        moves = S.res.get("moves", [])
        up = [m for m in moves if m[2] > m[1]]
        if up:
            st.balloons()
        hatch = "".join(
            f'<div class="hatch">{pic(W()[i]["e"], 34)}<span>{W()[i]["en"]}</span>{tw(STAGES[a][1], 30)}<span class="arr">→</span>'
            f'<span class="up">{tw(STAGES[b][1], 38)}</span><span>{STAGES[b][0]}</span></div>' for i, a, b in moves if a != b)
        st.markdown(f"""<div class="big"><span class="bob">{chick(110)}</span><h1>{len(up)} kelime büyüdü!</h1>
            <p style="font-weight:700">{S.score}/{len(S.qs)} doğru</p></div>{hatch}""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("Keşfet", icon=":material/explore:", use_container_width=True, on_click=go, kwargs={"screen": "explore"})
        c2.button("Yuvama dön", type="primary", use_container_width=True, on_click=go, kwargs={"screen": "nest"})
