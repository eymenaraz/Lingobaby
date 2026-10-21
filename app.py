import base64
import io
import json
import random
from datetime import date, timedelta

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LingoCat", page_icon="🐱", layout="centered")

GREEN, BLUE, YELLOW, RED, ORANGE, PURPLE, INK = "#58CC02", "#1CB0F6", "#FFC800", "#FF4B4B", "#FF9600", "#CE82FF", "#3C3C3C"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap');
html,body,.stApp,button,input{font-family:'Nunito',sans-serif!important}
.stApp{background:#fff;color:#3C3C3C}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important}
.block-container{max-width:560px;padding:.8rem 1rem 3rem}
h1,h2,h3,p,span,label,div{color:#3C3C3C}
div[data-testid="stHorizontalBlock"]{flex-direction:row!important;flex-wrap:nowrap!important;gap:.6rem!important}
div[data-testid="stColumn"],div[data-testid="column"]{min-width:0!important}
.stButton>button{font-weight:800;font-size:16px;border-radius:16px;border:2px solid #E5E5E5;border-bottom-width:4px;
 background:#fff;color:#4B4B4B;padding:.55rem .8rem;transition:transform .05s}
.stButton>button:hover{background:#F7F7F7;border-color:#E5E5E5;color:#4B4B4B}
.stButton>button:active{transform:translateY(3px);border-bottom-width:1px}
.stButton>button[kind="primary"],.stButton button[data-testid="stBaseButton-primary"]{background:#58CC02;border-color:#46A302;color:#fff}
.stButton>button[kind="primary"]:hover,.stButton button[data-testid="stBaseButton-primary"]:hover{background:#61E002;color:#fff;border-color:#46A302}
.stButton>button:disabled{opacity:.5}
button[data-baseweb="tab"] p{font-weight:800;font-size:16px}
div[data-baseweb="tab-highlight"]{background:#58CC02!important}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.bd{display:flex;align-items:center;gap:8px;font-size:28px;font-weight:900;color:#58CC02}.bd b{color:#1CB0F6}
.chips{display:flex;gap:6px}.ch{display:flex;align-items:center;gap:4px;font-weight:900;font-size:16px;padding:3px 10px;border-radius:999px;background:#F7F7F7;border:2px solid #E5E5E5}
.ch.rk{background:#1CB0F6;border-color:#1899D6;color:#fff}
.node{text-align:center;margin:10px 0 2px}
.disc{width:88px;height:88px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;
 box-shadow:0 7px 0 rgba(0,0,0,.22);border:4px solid rgba(255,255,255,.55)}
.disc.lock{background:#E5E5E5!important;box-shadow:0 7px 0 #CFCFCF}.disc.lock img{filter:grayscale(1) opacity(.45)}
.nt{font-weight:900;font-size:18px;margin-top:10px}.nt small{display:block;font-weight:700;color:#8A8A8A;font-size:13px}
.stars img{margin:0 1px}.off{filter:grayscale(1) opacity(.3)}
.art{background:#EAF7FF;border-radius:28px;padding:18px;text-align:center;margin:6px 0 10px;border:2px solid #D3EEFF}
.art img{filter:drop-shadow(0 8px 0 rgba(0,0,0,.08))}
.ask{font-size:22px;font-weight:900;margin:4px 0 8px}
.opt{border:2px solid #E5E5E5;border-bottom-width:4px;border-radius:16px;padding:12px 6px;text-align:center;font-weight:800;
 font-size:18px;background:#fff;margin-bottom:6px;min-height:52px;display:flex;align-items:center;justify-content:center}
.opt.right{background:#D7FFB8;border-color:#58CC02;color:#58A700}.opt.wrong{background:#FFDFE0;border-color:#FF4B4B;color:#EA2B2B;animation:shake .35s}
.opt.dim{opacity:.45}
.sheet{display:flex;gap:12px;align-items:center;border-radius:18px;padding:12px 16px;margin:10px 0;animation:pop .25s ease-out}
.sheet.ok{background:#D7FFB8;color:#58A700}.sheet.no{background:#FFDFE0;color:#EA2B2B}
.sheet b{font-size:20px;font-weight:900;color:inherit}.sheet span{font-weight:700;color:inherit}
.bar{height:16px;background:#E5E5E5;border-radius:99px;overflow:hidden;margin:4px 0 12px}
.bar>div{height:100%;background:#58CC02;border-radius:99px;transition:width .4s}
.built{min-height:64px;border-bottom:3px solid #E5E5E5;display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:6px 2px;margin:6px 0 14px}
.w{border:2px solid #E5E5E5;border-bottom-width:4px;border-radius:12px;padding:6px 12px;font-weight:800;font-size:19px}
.combo{display:inline-flex;gap:4px;align-items:center;font-weight:900;color:#FF9600;animation:pop .3s}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:8px 0}
.tile{border:2px solid #E5E5E5;border-radius:16px;padding:10px 14px}.tile b{display:block;font-size:26px;font-weight:900}
.tile span{font-weight:700;color:#8A8A8A;font-size:13px}
.chart{display:flex;gap:8px;height:170px;align-items:flex-end;border-bottom:3px solid #E5E5E5;padding:0 4px 4px;margin:10px 0 24px}
.cc{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;position:relative}
.cc i{display:block;width:100%;border-radius:8px 8px 2px 2px;background:#BFE3FF}.cc.t i{background:#58CC02}
.cc em{font-style:normal;font-weight:800;font-size:12px;color:#8A8A8A}.cc span{position:absolute;bottom:-26px;font-weight:800;font-size:12px;color:#8A8A8A}
.bg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:12px}
.bgi{text-align:center;font-weight:800;font-size:13px}.bgi small{display:block;color:#8A8A8A;font-weight:700}
.bgi.off img{filter:grayscale(1) opacity(.3)}
.big{text-align:center}.big h1{font-size:34px;font-weight:900;margin:6px 0}
.rankup{background:#1CB0F6;color:#fff;border-radius:18px;padding:12px;text-align:center;font-weight:900;font-size:19px;animation:pop .5s;margin:10px 0}
.rankup *{color:#fff}
@keyframes pop{0%{transform:scale(.85);opacity:0}100%{transform:scale(1);opacity:1}}
@keyframes shake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
@keyframes bob{50%{transform:translateY(-6px)}}
.bob{animation:bob 1.6s ease-in-out infinite;display:inline-block}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# GÖRSELLER: vektör çizimler (Twemoji SVG), özel çizilen renk lekeleri, sayı rozetleri ve LinCat
# Kendi fotoğraflarınızı kullanmak için IMG_OVERRIDE içine  "Kelime id": "https://..."  ekleyin.
# ------------------------------------------------------------------
TW = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{}.svg"
IMG_OVERRIDE = {}


def tw(e, px=64):
    cp = "-".join(f"{ord(c):x}" for c in e if ord(c) != 0xFE0F)
    return (f'<img src="{TW.format(cp)}" width="{px}" height="{px}" alt="" '
            f'onerror="this.outerHTML=\'<span style=font-size:{int(px * .8)}px>{e}</span>\'">')


def pic(e, px=96):
    if e.startswith("http"):
        return f'<img src="{e}" width="{px}" height="{px}" style="object-fit:cover;border-radius:16px">'
    if e.startswith("col:"):
        h = e[4:]
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100"><path d="M50 8c18-2 40 10 42 32 2 20-10 30-8 44-2 10-24 12-40 8'
                f'C26 88 8 78 8 58 6 36 28 10 50 8z" fill="{h}"/><ellipse cx="34" cy="30" rx="13" ry="7" fill="#fff" opacity=".45" '
                f'transform="rotate(-30 34 30)"/></svg>')
    if e.startswith("num:"):
        n = e[4:]
        c = [BLUE, GREEN, ORANGE, PURPLE, RED, YELLOW][int(n) % 6]
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100"><circle cx="50" cy="54" r="42" fill="rgba(0,0,0,.12)"/>'
                f'<circle cx="50" cy="48" r="42" fill="{c}"/><circle cx="36" cy="32" r="9" fill="#fff" opacity=".35"/>'
                f'<text x="50" y="68" text-anchor="middle" font-size="58" font-weight="900" fill="#fff" font-family="Nunito,Arial">{n}</text></svg>')
    return tw(e, px)


def cat(px=48, sad=False):
    mouth = "M50 84 q10 -8 20 0" if sad else "M50 78 q5 7 10 0 q5 7 10 0"
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 120 110"><path d="M16 44 L24 6 L52 26Z" fill="{ORANGE}"/>'
            f'<path d="M104 44 L96 6 L68 26Z" fill="{ORANGE}"/><path d="M26 34 L29 16 L42 27Z" fill="#FFB3C1"/>'
            f'<path d="M94 34 L91 16 L78 27Z" fill="#FFB3C1"/><ellipse cx="60" cy="62" rx="46" ry="40" fill="{ORANGE}"/>'
            f'<path d="M50 28 v10 M60 26 v12 M70 28 v10" stroke="#E07A00" stroke-width="4" stroke-linecap="round"/>'
            f'<ellipse cx="60" cy="76" rx="27" ry="20" fill="#FFE3B8"/><ellipse cx="42" cy="56" rx="7" ry="9" fill="{INK}"/>'
            f'<ellipse cx="78" cy="56" rx="7" ry="9" fill="{INK}"/><circle cx="44" cy="52" r="2.5" fill="#fff"/><circle cx="80" cy="52" r="2.5" fill="#fff"/>'
            f'<path d="M54 68 h12 l-6 7z" fill="#FF6B81"/><path d="{mouth}" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<path d="M8 66 l22 4 M8 80 l22 -4 M112 66 l-22 4 M112 80 l-22 -4" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/></svg>')


# ------------------------------------------------------------------
# MÜFREDAT
# ------------------------------------------------------------------
def art(w):
    return "an" if w[0].lower() in "aeiou" else "a"


def U(uid, title, tr, ic, tpl, words, sents):
    ws = []
    for i, t in enumerate(words):
        en, trk, e = t[:3]
        s = t[3] if len(t) > 3 else tpl.format(w=en.lower(), A=f"{art(en)} {en.lower()}")
        ws.append(dict(id=f"{uid}{i}", en=en, tr=trk, e=IMG_OVERRIDE.get(f"{uid}{i}", e), s=s[0].upper() + s[1:]))
    return dict(id=uid, title=title, tr=tr, ic=ic, words=ws, sents=[dict(tr=a, words=b.split()) for a, b in sents])


GRADES = {
    "k": dict(title="Anaokulu", color=ORANGE, units=[
        U("k1", "Colors", "Renkler", "🎨", "It is {w}.",
          [("Red", "Kırmızı", "col:#FF4B4B"), ("Blue", "Mavi", "col:#1CB0F6"), ("Yellow", "Sarı", "col:#FFC800"),
           ("Green", "Yeşil", "col:#58CC02"), ("Orange", "Turuncu", "col:#FF9600"), ("Purple", "Mor", "col:#CE82FF")],
          [("Gökyüzü mavidir.", "The sky is blue"), ("Elma kırmızıdır.", "The apple is red")]),
        U("k2", "Animals", "Hayvanlar", "🦁", "I see {A}.",
          [("Cat", "Kedi", "🐱"), ("Dog", "Köpek", "🐶"), ("Lion", "Aslan", "🦁"),
           ("Elephant", "Fil", "🐘"), ("Rabbit", "Tavşan", "🐰"), ("Bird", "Kuş", "🐦")],
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
    "1": dict(title="1. Sınıf", color=BLUE, units=[
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
    "2": dict(title="2. Sınıf", color=GREEN, units=[
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
for gk, g in GRADES.items():
    for u in g["units"]:
        u["g"] = gk
ALL_WORDS = [w for g in GRADES.values() for u in g["units"] for w in u["words"]]
ALL_UNITS = [u for g in GRADES.values() for u in g["units"]]

# A1 → C1 kademeleri ve rozetler
RANKS = [("A1", "Yavru Kedi", 0), ("A2", "Meraklı Kedi", 100), ("B1", "Cesur Kedi", 300),
         ("B2", "Usta Kedi", 600), ("C1", "Efsane Kedi", 1000)]


def rank(xp):
    return max(i for i, r in enumerate(RANKS) if xp >= r[2])


BADGES = [
    ("İlk adım", "🐾", "İlk üniteyi bitir", lambda: bool(S.stars)),
    ("Parlak", "🌟", "3 yıldız kazan", lambda: 3 in S.stars.values()),
    ("Kusursuz", "💯", "Hatasız tur yap", lambda: S.perfect >= 1),
    ("Ateşli", "🔥", "5 üst üste doğru", lambda: S.best >= 5),
    ("Enerjik", "⚡", "100 XP topla", lambda: S.xp >= 100),
    ("Kupa", "🏆", "500 XP topla", lambda: S.xp >= 500),
    ("Şampiyon", "👑", "Bir sınıfı bitir", lambda: any(all(S.stars.get(u["id"], 0) for u in g["units"]) for g in GRADES.values())),
    ("Roket", "🚀", "5 tur tamamla", lambda: S.rounds >= 5),
    ("Usta", "🎓", "B1 seviyesine ulaş", lambda: S.xp >= 300),
]


def earned():
    return {b[0] for b in BADGES if b[3]()}


# ------------------------------------------------------------------
# STATE
# ------------------------------------------------------------------
DEFAULTS = dict(screen="learn", unit=None, phase="learn", stars={}, xp=0, streak=1, last_day=None, hist={},
                best=0, perfect=0, rounds=0, qs=[], qi=0, score=0, combo=0, picked=None, ok=False, built=[],
                pool=[], checked=False, sfx=False, unit_xp=0, rank0=0, res={})
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state

today = date.today()
if S.last_day != today.isoformat():
    S.streak = S.streak + 1 if S.last_day == (today - timedelta(1)).isoformat() else 1
    S.last_day = today.isoformat()


def go(**kw):
    for k, v in kw.items():
        S[k] = v


def log(ok, gain):
    d = S.hist.setdefault(today.isoformat(), dict(xp=0, ok=0, n=0))
    d["xp"] += gain
    d["ok"] += int(ok)
    d["n"] += 1


# ------------------------------------------------------------------
# SES: gTTS (sunucuda mp3 üretir), olmazsa tarayıcı sesine döner
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


def speak_html(text, auto=False):
    components.html(
        f"""<style>body{{margin:0}}button{{font:800 17px Nunito,Arial;background:#1CB0F6;color:#fff;border:2px solid #1899D6;
        border-bottom-width:4px;border-radius:16px;padding:8px 20px;cursor:pointer;display:flex;gap:8px;align-items:center}}</style>
        <button onclick="play('w')">{SPK}Dinle</button>
        <script>{player_js({'w': text})}{"setTimeout(()=>play('w'),300);" if auto else ""}</script>""",
        height=58)


def flashcards(unit, color):
    items, cards = {}, ""
    for i, w in enumerate(unit["words"]):
        items[f"w{i}"], items[f"s{i}"] = w["en"], w["s"]
        cards += (f'<div class="c" onclick="this.classList.toggle(\'on\');play(\'w{i}\')"><div class="f">{pic(w["e"], 72)}'
                  f'<div class="n">{w["en"]}</div></div><div class="k"><div class="n">{w["tr"]}</div><div class="h">{w["s"]}</div>'
                  f'<button onclick="event.stopPropagation();play(\'s{i}\')">{SPK}</button></div></div>')
    rows = (len(unit["words"]) + 1) // 2
    components.html(
        f"""<style>body{{margin:0;font-family:Nunito,Arial,sans-serif}}.g{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:2px 2px 8px}}
        .c{{position:relative;height:176px;cursor:pointer;perspective:800px}}
        .f,.k{{position:absolute;inset:0;border:2px solid #E5E5E5;border-bottom-width:5px;border-radius:20px;display:flex;flex-direction:column;
        align-items:center;justify-content:center;backface-visibility:hidden;transition:transform .45s;background:#fff;color:#3C3C3C;padding:6px;text-align:center}}
        .f img,.f svg{{filter:drop-shadow(0 5px 0 rgba(0,0,0,.08))}}.k{{transform:rotateY(180deg);background:{color};border-color:rgba(0,0,0,.25);color:#fff}}
        .c.on .f{{transform:rotateY(180deg)}}.c.on .k{{transform:rotateY(360deg)}}
        .n{{font-size:22px;font-weight:900;margin-top:6px}}.h{{font-size:14px;font-weight:700;margin:4px 0 6px}}
        .k button{{background:rgba(255,255,255,.28);border:0;border-radius:12px;padding:6px 12px;cursor:pointer}}</style>
        <div class="g">{cards}</div><script>{player_js(items)}</script>""",
        height=rows * 188 + 12)


def sfx(ok):
    if S.sfx:
        S.sfx = False
        n = "[523,659,784]" if ok else "[300,220]"
        components.html(
            "<script>try{const c=new(window.AudioContext||window.webkitAudioContext)();" + n + ".forEach((f,i)=>{const o=c.createOscillator(),"
            "g=c.createGain(),t=c.currentTime+i*.12;o.type='triangle';o.frequency.value=f;o.connect(g);g.connect(c.destination);"
            "g.gain.setValueAtTime(.15,t);g.gain.exponentialRampToValueAtTime(.001,t+.2);o.start(t);o.stop(t+.25);});}catch(e){}</script>",
            height=0)


# ------------------------------------------------------------------
# OYUN MANTIĞI
# ------------------------------------------------------------------
def start_unit(unit):
    words = unit["words"][:]
    random.shuffle(words)
    qs = []
    for w in words:
        others = [x for x in unit["words"] if x["id"] != w["id"]] + random.sample(ALL_WORDS, 6)
        seen, wrong = set(), []
        random.shuffle(others)
        for x in others:
            if x["en"] != w["en"] and x["en"] not in seen and len(wrong) < 3:
                seen.add(x["en"])
                wrong.append(x)
        for k in ("see", "hear"):
            o = [w] + wrong
            random.shuffle(o)
            qs.append(dict(k=k, w=w, opts=o))
    random.shuffle(qs)
    qs = qs[:8] + [dict(k="sent", s=s) for s in unit["sents"]]
    go(screen="unit", unit=unit, phase="learn", qs=qs, qi=0, score=0, combo=0, picked=None, built=[], pool=[],
       checked=False, unit_xp=0, rank0=rank(S.xp), sfx=False)


def award(ok):
    S.ok = ok
    S.sfx = True
    if ok:
        S.score += 1
        S.combo += 1
        S.best = max(S.best, S.combo)
        gain = 10 + (5 if S.combo >= 3 else 0)
    else:
        S.combo, gain = 0, 0
    S.xp += gain
    S.unit_xp += gain
    log(ok, gain)


def choose(opt_id, correct_id):
    S.picked = opt_id
    award(opt_id == correct_id)


def pick_word(i):
    S.built.append(S.pool.pop(i))


def check_sentence(target):
    S.checked = True
    award([w.lower() for w in S.built] == [w.lower() for w in target])


def next_q():
    S.qi += 1
    S.picked, S.checked, S.built, S.pool, S.sfx = None, False, [], [], False
    if S.qi >= len(S.qs):
        n, old = len(S.qs), earned()
        r = S.score / n
        stars = 3 if r >= .85 else 2 if r >= .6 else 1
        S.stars[S.unit["id"]] = max(S.stars.get(S.unit["id"], 0), stars)
        S.rounds += 1
        S.perfect += int(S.score == n)
        S.res = dict(stars=stars, new=sorted(earned() - old), up=rank(S.xp) > S.rank0)
        S.phase = "result"


def reset_pool(words):
    S.pool, S.built = random.sample(words, len(words)), []


# ------------------------------------------------------------------
# ÜST PANEL / MENÜ
# ------------------------------------------------------------------
def head():
    r = RANKS[rank(S.xp)]
    st.markdown(f"""<div class="top"><div class="bd">{cat(44)}<span>Lingo<b>Cat</b></span></div><div class="chips">
        <span class="ch">{tw('🔥', 20)}{S.streak}</span><span class="ch">{tw('⚡', 20)}{S.xp}</span>
        <span class="ch rk">{r[0]}</span></div></div>""", unsafe_allow_html=True)
    cols = st.columns(3)
    for c, (k, lab, ic) in zip(cols, [("learn", "Öğren", ":material/home:"), ("stats", "İlerleme", ":material/bar_chart:"),
                                      ("badges", "Rozetler", ":material/emoji_events:")]):
        c.button(lab, key=f"n_{k}", icon=ic, use_container_width=True, type="primary" if S.screen == k else "secondary",
                 on_click=go, kwargs={"screen": k})


def stars_html(n, px=22):
    return "".join(f'<span class="{"" if i < n else "off"}">{tw("⭐", px)}</span>' for i in range(3))


# ------------------------------------------------------------------
# EKRANLAR
# ------------------------------------------------------------------
if S.screen == "learn":
    head()
    tabs = st.tabs([g["title"] for g in GRADES.values()])
    offs = [(1, 1), (.2, 1.8), (1, 1), (1.8, .2)]
    for tab, (gk, g) in zip(tabs, GRADES.items()):
        with tab:
            for i, u in enumerate(g["units"]):
                locked = i > 0 and not S.stars.get(g["units"][i - 1]["id"], 0)
                a, b = offs[i % 4]
                _, mid, _ = st.columns([a, 2, b])
                with mid:
                    st.markdown(f"""<div class="node"><div class="disc {'lock' if locked else ''}" style="background:{g['color']}">
                        {tw(u['ic'], 46)}</div><div class="nt">{u['title']}<small>{u['tr']}</small></div>
                        <div class="stars">{stars_html(S.stars.get(u['id'], 0), 20)}</div></div>""", unsafe_allow_html=True)
                    st.button("Kilitli" if locked else "Başla", key=f"u_{u['id']}", disabled=locked, use_container_width=True,
                              type="secondary" if locked else "primary", icon=":material/lock:" if locked else None,
                              on_click=start_unit, args=(u,))

elif S.screen == "stats":
    head()
    days = [today - timedelta(d) for d in range(6, -1, -1)]
    H = [S.hist.get(d.isoformat(), {}) for d in days]
    vals = [h.get("xp", 0) for h in H]
    mx = max(vals + [1])
    names = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    bars = "".join(f'<div class="cc {"t" if d == today else ""}"><em>{v or ""}</em><i style="height:{max(4, int(v / mx * 110))}px"></i>'
                   f'<span>{names[d.weekday()]}</span></div>' for d, v in zip(days, vals))
    ok, n = sum(h.get("ok", 0) for h in H), sum(h.get("n", 0) for h in H)
    r = rank(S.xp)
    nxt = RANKS[r + 1] if r + 1 < len(RANKS) else None
    pct = 100 if not nxt else int((S.xp - RANKS[r][2]) / (nxt[2] - RANKS[r][2]) * 100)
    st.markdown(f"""<h3>{RANKS[r][0]} · {RANKS[r][1]}</h3><div class="bar"><div style="width:{pct}%"></div></div>
        <p style="margin:-6px 0 10px;font-weight:700;color:#8A8A8A">{f"{nxt[0]} için {nxt[2] - S.xp} XP kaldı" if nxt else "En üst seviyedesin"}</p>
        <div class="grid"><div class="tile"><b>{vals[-1]}</b><span>Bugünkü XP</span></div><div class="tile"><b>{sum(vals)}</b><span>Haftalık XP</span></div>
        <div class="tile"><b>%{int(ok / n * 100) if n else 0}</b><span>Haftalık doğruluk</span></div>
        <div class="tile"><b>{len(S.stars)}/{len(ALL_UNITS)}</b><span>Biten ünite</span></div></div>
        <h3 style="margin-top:18px">Son 7 gün</h3><div class="chart">{bars}</div>""", unsafe_allow_html=True)
    keys = ("stars", "xp", "hist", "best", "perfect", "rounds", "streak", "last_day")
    st.download_button("İlerlemeyi kaydet", json.dumps({k: S[k] for k in keys}), "lingocat_ilerleme.json",
                       use_container_width=True, icon=":material/download:")
    up = st.file_uploader("Kayıtlı ilerlemeyi yükle", type="json")
    if up is not None and S.get("loaded") != up.name:
        try:
            S.update(json.loads(up.read()))
            S.loaded = up.name
            st.rerun()
        except Exception:
            st.error("Dosya okunamadı.")
    st.caption("Görseller: Twemoji, CC-BY 4.0")

elif S.screen == "badges":
    head()
    got = earned()
    html = "".join(f'<div class="bgi {"" if b[0] in got else "off"}">{tw(b[1], 64)}<div>{b[0]}</div><small>{b[2]}</small></div>' for b in BADGES)
    st.markdown(f"<h3>{len(got)}/{len(BADGES)} rozet</h3><div class='bg'>{html}</div>", unsafe_allow_html=True)

elif S.screen == "unit":
    u, g = S.unit, GRADES[S.unit["g"]]
    st.button("Çık", icon=":material/close:", on_click=go, kwargs={"screen": "learn"})

    if S.phase == "learn":
        st.markdown(f"<h2>{tw(u['ic'], 34)} {u['title']}</h2>", unsafe_allow_html=True)
        with st.spinner("Sesler hazırlanıyor"):
            flashcards(u, g["color"])
        st.button("Oyuna başla", type="primary", use_container_width=True, on_click=go, kwargs={"phase": "quiz"})

    elif S.phase == "quiz":
        q = S.qs[S.qi]
        combo = f'<span class="combo">{tw("🔥", 22)}{S.combo}</span>' if S.combo >= 2 else ""
        st.markdown(f'<div class="bar"><div style="width:{S.qi / len(S.qs) * 100}%"></div></div>'
                    f'<div style="height:26px">{combo}</div>', unsafe_allow_html=True)

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
                st.markdown(f"<div class='sheet {'ok' if S.ok else 'no'}'>{cat(52, not S.ok)}<div><b>{random.choice(['Harika!', 'Süper!', 'Bravo!']) if S.ok else 'Doğrusu:'}</b>"
                            f"<br><span>{w['en']} = {w['tr']}</span></div></div>", unsafe_allow_html=True)
                st.button("Devam", type="primary", use_container_width=True, on_click=next_q)
        else:
            s = q["s"]
            if not S.pool and not S.built and not S.checked:
                reset_pool(s["words"])
            st.markdown(f"<p class='ask'>İngilizcesini kur</p><div class='art'><h2 style='margin:0'>{s['tr']}</h2></div>", unsafe_allow_html=True)
            chips = "".join(f"<span class='w'>{x}</span>" for x in S.built)
            st.markdown(f"<div class='built'>{chips}</div>", unsafe_allow_html=True)
            if not S.checked:
                cols = st.columns(min(max(len(S.pool), 1), 3))
                for i, x in enumerate(S.pool):
                    cols[i % len(cols)].button(x, key=f"w{S.qi}_{i}_{x}", use_container_width=True, on_click=pick_word, args=(i,))
                a, b = st.columns(2)
                a.button("Sıfırla", icon=":material/refresh:", use_container_width=True, on_click=reset_pool, args=(s["words"],))
                b.button("Kontrol et", type="primary", use_container_width=True, disabled=not S.built,
                         on_click=check_sentence, args=(s["words"],))
            else:
                sfx(S.ok)
                target = " ".join(s["words"])
                st.markdown(f"<div class='sheet {'ok' if S.ok else 'no'}'>{cat(52, not S.ok)}<div><b>{'Mükemmel!' if S.ok else 'Doğrusu:'}</b>"
                            f"<br><span>{target}</span></div></div>", unsafe_allow_html=True)
                speak_html(target)
                st.button("Devam", type="primary", use_container_width=True, on_click=next_q)

    elif S.phase == "result":
        res, n = S.res, len(S.qs)
        if res["stars"] == 3:
            st.balloons()
        up = f"<div class='rankup'>Yeni seviye: {RANKS[rank(S.xp)][0]} · {RANKS[rank(S.xp)][1]}</div>" if res["up"] else ""
        nb = "".join(f"<div class='bgi' style='display:inline-block;margin:6px 10px'>{tw(next(b[1] for b in BADGES if b[0] == x), 52)}<div>{x}</div></div>"
                     for x in res["new"])
        st.markdown(f"""<div class="big"><span class="bob">{cat(120)}</span><h1>{S.score}/{n} doğru</h1><div class="stars">{stars_html(res['stars'], 52)}</div>
            <p style="font-weight:900;font-size:20px;color:#FF9600;margin-top:10px">+{S.unit_xp} XP</p></div>{up}
            <div style="text-align:center">{nb}</div>""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("Tekrar", icon=":material/refresh:", use_container_width=True, on_click=start_unit, args=(u,))
        c2.button("Devam", type="primary", use_container_width=True, on_click=go, kwargs={"screen": "learn"})
