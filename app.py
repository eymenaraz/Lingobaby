import base64
import copy
import csv
import hashlib
import hmac
import io
import json
import os
import random
import re
from datetime import datetime, timedelta

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LingoNest", page_icon="🪺", layout="centered")

INK, SKY, YOLK, TEAL, BERRY, TWIG, LEAF, CORAL = "#1F2A44", "#4DA3FF", "#FFC531", "#17B8A6", "#FF5C8A", "#8B5E3C", "#5CCB7A", "#FF7A59"
SHADOW = "#C9D6EE"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&display=swap');
html,body,.stApp,button,input,textarea{font-family:'Baloo 2',sans-serif!important}
.stApp{background:linear-gradient(180deg,#D6E8FF 0,#EEF0FF 340px,#F6F3FF 100%);color:#1F2A44}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important}
.block-container{max-width:580px;padding:.8rem 1rem 3rem}
h1,h2,h3,p,span,label,div{color:#1F2A44}
div[data-testid="stHorizontalBlock"]{flex-direction:row!important;flex-wrap:nowrap!important;gap:.5rem!important}
div[data-testid="stColumn"],div[data-testid="column"]{min-width:0!important}
.stButton>button,.stDownloadButton>button{font-weight:700;font-size:16px;border-radius:999px;border:0;background:#fff;color:#1F2A44;
 padding:.55rem 1rem;box-shadow:0 3px 0 #C9D6EE,0 8px 18px rgba(31,42,68,.10);transition:transform .08s,box-shadow .08s}
.stButton>button:hover{background:#F7FAFF;color:#1F2A44}
.stButton>button:active{transform:translateY(3px);box-shadow:0 0 0 #C9D6EE}
.stButton>button[kind="primary"],.stButton button[data-testid="stBaseButton-primary"]{background:#FF5C8A;color:#fff;box-shadow:0 3px 0 #D93B69,0 8px 18px rgba(255,92,138,.28)}
.stButton>button[kind="primary"]:hover,.stButton button[data-testid="stBaseButton-primary"]:hover{background:#FF73A0;color:#fff}
.stButton>button:disabled{opacity:.5}
button[data-baseweb="tab"] p{font-weight:700;font-size:16px}
div[data-baseweb="tab-highlight"]{background:#FF5C8A!important}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.bd{display:flex;align-items:center;gap:8px;font-size:28px;font-weight:800;color:#1F2A44;letter-spacing:-.5px}.bd b{color:#FF5C8A}
.chips{display:flex;gap:6px}.ch{display:flex;align-items:center;gap:4px;font-weight:700;font-size:15px;padding:2px 10px;border-radius:999px;background:#fff;box-shadow:0 2px 8px rgba(31,42,68,.12)}
.ch.rk{background:#1F2A44}.ch.rk,.ch.rk *{color:#fff}
.hero{display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:26px;background:linear-gradient(120deg,#FFD35A,#FFB36B);margin:4px 0 12px;box-shadow:0 10px 24px rgba(255,160,60,.28)}
.hero h2{margin:0;font-size:24px;font-weight:800;line-height:1.1}.hero p{margin:2px 0 0;font-weight:600;font-size:15px}
.scene{border-radius:30px;overflow:hidden;box-shadow:0 12px 28px rgba(31,42,68,.2);margin:6px 0 8px}
.hint{font-weight:600;font-size:13px;color:#5B6A8A;text-align:center;margin-bottom:10px}
.stg{display:flex;justify-content:space-between;background:#fff;border-radius:22px;padding:8px 10px;margin-bottom:10px;box-shadow:0 2px 10px rgba(31,42,68,.1)}
.stg div{text-align:center;font-weight:700;font-size:12px}.stg b{display:block;font-size:18px}
.card{background:#fff;border-radius:24px;padding:12px 14px;margin-bottom:6px;box-shadow:0 3px 0 #C9D6EE,0 8px 18px rgba(31,42,68,.08);text-align:center}
.card .t{font-size:19px;font-weight:800}.card small{display:block;color:#5B6A8A;font-weight:600}
.art{background:#fff;border-radius:30px;padding:18px;text-align:center;margin:6px 0 10px;box-shadow:inset 0 0 0 3px #FFE08A}
.art img{filter:drop-shadow(0 8px 4px rgba(0,0,0,.1))}
.ask{font-size:21px;font-weight:800;margin:4px 0 8px}
.opt{border-radius:18px;padding:12px 6px;text-align:center;font-weight:700;font-size:18px;background:#fff;margin-bottom:6px;min-height:52px;
 display:flex;align-items:center;justify-content:center;box-shadow:0 3px 0 #C9D6EE}
.opt.right{background:#D8F7EE;box-shadow:0 3px 0 #17B8A6;color:#0E7C6F}.opt.wrong{background:#FFE0E8;box-shadow:0 3px 0 #FF5C8A;color:#C42B58;animation:shake .35s}
.opt.dim{opacity:.45}
.sheet{display:flex;gap:12px;align-items:center;border-radius:22px;padding:12px 16px;margin:10px 0;animation:pop .25s ease-out}
.sheet.ok{background:#D8F7EE;color:#0E7C6F}.sheet.no{background:#FFE0E8;color:#C42B58}
.sheet b{font-size:20px;font-weight:800;color:inherit}.sheet span{font-weight:600;color:inherit}
.bar{height:14px;background:#DCE5F5;border-radius:99px;overflow:hidden;margin:4px 0 10px}
.bar>div{height:100%;background:#17B8A6;border-radius:99px;transition:width .4s}
.built{min-height:60px;border-bottom:3px dashed #C9D6EE;display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:6px 2px;margin:6px 0 14px}
.w{background:#fff;border-radius:12px;padding:5px 12px;font-weight:700;font-size:19px;box-shadow:0 2px 0 #C9D6EE}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:8px 0}
.tile{background:#fff;border-radius:20px;padding:10px 14px;box-shadow:0 2px 10px rgba(31,42,68,.1)}.tile b{display:block;font-size:26px;font-weight:800}
.tile span{font-weight:600;color:#5B6A8A;font-size:13px}
.chart{display:flex;gap:8px;height:170px;align-items:flex-end;border-bottom:3px solid #C9D6EE;padding:0 4px 4px;margin:10px 0 28px}
.cc{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;position:relative}
.cc i{display:block;width:100%;border-radius:8px 8px 2px 2px;background:#A9CBFF}.cc.t i{background:#FF5C8A}
.cc em{font-style:normal;font-weight:700;font-size:12px;color:#5B6A8A}.cc span{position:absolute;bottom:-26px;font-weight:700;font-size:12px;color:#5B6A8A}
.row{display:flex;align-items:center;gap:10px;background:#fff;border-radius:18px;padding:8px 12px;margin-bottom:6px;font-weight:700;box-shadow:0 2px 8px rgba(31,42,68,.08)}
.row .bar{flex:1;margin:0}.row small{color:#5B6A8A;font-weight:600}
.hatch{display:flex;align-items:center;justify-content:center;gap:8px;background:#fff;border-radius:20px;padding:8px;margin:6px 0;font-weight:700;animation:pop .5s}
.hatch .arr{font-size:22px;color:#FF5C8A}.hatch .up{animation:bob 1.2s ease-in-out infinite}
.big{text-align:center}.big h1{font-size:32px;font-weight:800;margin:4px 0}
.qs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}
.q{background:#fff;border-radius:22px;padding:10px 6px;text-align:center;box-shadow:0 2px 10px rgba(31,42,68,.1)}
.q b{display:block;font-size:16px}.q small{font-weight:600;color:#5B6A8A;font-size:12px}
.ring{width:56px;height:56px;margin:0 auto 4px;border-radius:50%;background:conic-gradient(#17B8A6 calc(var(--p)*1%),#DCE5F5 0);display:flex;align-items:center;justify-content:center}
.ring span{width:42px;height:42px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}
.dots{display:flex;gap:6px;justify-content:space-between;margin:6px 0 14px}.dots i{flex:1;height:12px;border-radius:99px;background:#DCE5F5}.dots i.on{background:#FF5C8A}
.bg{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:10px}
.bgi{text-align:center;font-weight:700;font-size:13px;background:#fff;border-radius:20px;padding:10px 4px;box-shadow:0 2px 10px rgba(31,42,68,.1)}
.bgi small{display:block;color:#5B6A8A;font-weight:600;font-size:11px}.bgi.off img{filter:grayscale(1) opacity(.3)}
@keyframes pop{0%{transform:scale(.85);opacity:0}100%{transform:scale(1);opacity:1}}
@keyframes shake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
@keyframes bob{50%{transform:translateY(-6px)}}
.bob{animation:bob 1.8s ease-in-out infinite;display:inline-block}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# GÖRSELLER (vektör). Kendi görselleriniz için IMG_OVERRIDE: {"kelime id": "https://..."}
# ------------------------------------------------------------------
TW = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{}.svg"
IMG_OVERRIDE = {}
COLORS = {"Sarı": (YOLK, "#F5A623"), "Mavi": ("#86CBFF", "#4DA3FF"), "Pembe": ("#FFB8CF", "#FF8FB0"), "Yeşil": ("#A6E8B5", "#5CCB7A")}


def tw(e, px=64):
    keep = "\u200d" in e
    cp = "-".join(f"{ord(c):x}" for c in e if keep or ord(c) != 0xFE0F)
    return (f'<img src="{TW.format(cp)}" width="{px}" height="{px}" alt="" '
            f'onerror="this.outerHTML=\'<span style=font-size:{int(px * .8)}px>{e}</span>\'">')


SHAPES = {"circle": ('<circle cx="50" cy="50" r="40"', CORAL), "square": ('<rect x="14" y="14" width="72" height="72" rx="10"', SKY),
          "triangle": ('<polygon points="50,10 92,88 8,88" stroke-linejoin="round"', YOLK),
          "star": ('<polygon points="50,8 61,38 93,38 67,57 77,90 50,70 23,90 33,57 7,38 39,38" stroke-linejoin="round"', "#FFB020"),
          "heart": ('<path d="M50 88 C10 58 6 28 28 20 C40 16 48 22 50 30 C52 22 60 16 72 20 C94 28 90 58 50 88Z"', BERRY),
          "rectangle": ('<rect x="6" y="26" width="88" height="48" rx="10"', LEAF)}


def pic(e, px=96):
    if e.startswith(("http", "data:")):
        return f'<img src="{e}" width="{px}" height="{px}" style="object-fit:cover;border-radius:18px">'
    if e.startswith("shp:"):
        tag, c = SHAPES[e[4:]]
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100">{tag} fill="{c}" stroke="rgba(0,0,0,.15)" stroke-width="3"/>'
                f'<ellipse cx="34" cy="30" rx="10" ry="5" fill="#fff" opacity=".45" transform="rotate(-30 34 30)"/></svg>')
    if e.startswith("col:"):
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100"><path d="M50 8c18-2 40 10 42 32 2 20-10 30-8 44-2 10-24 12-40 8'
                f'C26 88 8 78 8 58 6 36 28 10 50 8z" fill="{e[4:]}"/><ellipse cx="34" cy="30" rx="13" ry="7" fill="#fff" opacity=".45" '
                f'transform="rotate(-30 34 30)"/></svg>')
    if e.startswith("num:"):
        n = e[4:]
        c = [SKY, TEAL, CORAL, "#B58CFF", YOLK, BERRY][int(n) % 6]
        return (f'<svg width="{px}" height="{px}" viewBox="0 0 100 100"><circle cx="50" cy="54" r="42" fill="rgba(0,0,0,.12)"/>'
                f'<circle cx="50" cy="48" r="42" fill="{c}"/><circle cx="36" cy="32" r="9" fill="#fff" opacity=".35"/>'
                f'<text x="50" y="68" text-anchor="middle" font-size="58" font-weight="800" fill="#fff" font-family="Baloo 2,Arial">{n}</text></svg>')
    return tw(e, px)


def chick(px=48, sad=False):
    body, wing = COLORS.get(st.session_state.get("color", "Sarı"), COLORS["Sarı"])
    mouth = f'<path d="M52 78 q8 -7 16 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>' if sad else ""
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 120 120"><path d="M52 14 q4 -10 8 0 q4 -10 8 0 q-8 8 -16 0z" fill="{CORAL}"/>'
            f'<circle cx="60" cy="64" r="46" fill="{body}"/><ellipse cx="22" cy="72" rx="12" ry="18" fill="{wing}" transform="rotate(20 22 72)"/>'
            f'<ellipse cx="98" cy="72" rx="12" ry="18" fill="{wing}" transform="rotate(-20 98 72)"/>'
            f'<circle cx="42" cy="56" r="7" fill="{INK}"/><circle cx="78" cy="56" r="7" fill="{INK}"/>'
            f'<circle cx="44" cy="53" r="2.5" fill="#fff"/><circle cx="80" cy="53" r="2.5" fill="#fff"/>'
            f'<path d="M50 68 h20 l-10 12z" fill="{CORAL}"/><circle cx="30" cy="72" r="6" fill="#FFAB91" opacity=".6"/>'
            f'<circle cx="90" cy="72" r="6" fill="#FFAB91" opacity=".6"/>{mouth}</svg>')


STAGES = [("Yumurta", "🥚"), ("Çatlıyor", "🐣"), ("Civciv", "🐥"), ("Kuş", "🐦"), ("Usta kuş", "🦜")]
INTERVALS = [0, 1, 2, 4, 7]  # Leitner kutuları: bakım aralığı (gün)
DECOS = [(3, "Çiçekler"), (6, "Kelebek"), (10, "Gökkuşağı"), (15, "Işık dizisi")]


def creature(b, x, y):
    eye = lambda dx: f'<circle cx="{x + dx}" cy="{y - 3}" r="2.2" fill="{INK}"/>'
    egg = f'<ellipse cx="{x}" cy="{y}" rx="12" ry="15" fill="#FFF6E2" stroke="#E6D3A8" stroke-width="2"/>'
    if b == 0:
        return egg + f'<circle cx="{x - 4}" cy="{y - 4}" r="2" fill="#F2C48D"/><circle cx="{x + 4}" cy="{y + 5}" r="2.5" fill="#F2C48D"/>'
    if b == 1:
        return (f'<circle cx="{x}" cy="{y - 12}" r="6" fill="{YOLK}"/>' + egg +
                f'<path d="M{x - 11} {y - 2} l5 -5 l5 5 l5 -5 l5 5 l4 -4" stroke="{TWIG}" stroke-width="2" fill="none"/>')
    if b == 2:
        return (f'<circle cx="{x}" cy="{y}" r="13" fill="{YOLK}"/>{eye(4)}<path d="M{x + 11} {y} l8 3 l-8 3z" fill="{CORAL}"/>'
                f'<path d="M{x - 3} {y - 13} q2 -6 5 0z" fill="{CORAL}"/>')
    if b == 3:
        return (f'<path d="M{x - 14} {y + 2} l-10 -4 l2 10z" fill="#2E7FD6"/><ellipse cx="{x}" cy="{y}" rx="15" ry="12" fill="{SKY}"/>'
                f'<ellipse cx="{x - 3}" cy="{y + 3}" rx="8" ry="5" fill="#2E7FD6"/>{eye(7)}<path d="M{x + 14} {y - 2} l7 3 l-7 3z" fill="{YOLK}"/>')
    return (f'<path d="M{x - 14} {y + 2} l-12 -6 l2 12z" fill="{YOLK}"/><ellipse cx="{x}" cy="{y}" rx="15" ry="12" fill="{BERRY}"/>'
            f'<path d="M{x - 2} {y - 11} l3 -9 l3 9z M{x + 4} {y - 10} l6 -8 l1 10z" fill="{YOLK}"/>'
            f'<ellipse cx="{x - 3}" cy="{y + 3}" rx="8" ry="5" fill="#D93B69"/>{eye(7)}<path d="M{x + 14} {y - 2} l7 3 l-7 3z" fill="{YOLK}"/>')


def nest_svg(boxes, night):
    n = len(boxes)
    slots = [(125, 128), (155, 124), (185, 124), (215, 128), (110, 150), (140, 148), (170, 148), (200, 148), (230, 150)]
    shown = sorted(boxes, reverse=True)[:len(slots)]
    items = "".join(creature(b, *slots[i]) for i, b in enumerate(shown))
    sky, ground = ("#1B2747", "#2F7D4C") if night else ("#BFE0FF", LEAF)
    sun = (f'<circle cx="300" cy="46" r="22" fill="#F4F1D0"/><circle cx="310" cy="40" r="20" fill="{sky}"/>' +
           "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".85"/>' for x, y, r in [(50, 30, 2), (90, 58, 1.5), (150, 24, 2), (230, 40, 1.5), (30, 90, 1.5), (260, 80, 2)])
           if night else f'<circle cx="300" cy="44" r="26" fill="{YOLK}"/><ellipse cx="70" cy="46" rx="34" ry="12" fill="#fff"/><ellipse cx="92" cy="40" rx="22" ry="10" fill="#fff"/>')
    rainbow = "".join(f'<path d="M{180 - r} 176 A{r} {r} 0 0 1 {180 + r} 176" stroke="{c}" stroke-width="8" fill="none" opacity="{.35 if night else .55}"/>'
                      for r, c in [(150, CORAL), (142, YOLK), (134, LEAF), (126, SKY)]) if n >= 10 else ""
    lights = "".join(f'<circle cx="{20 + 30 * i}" cy="174" r="4" fill="{c}"/>' + (f'<circle cx="{20 + 30 * i}" cy="174" r="9" fill="{c}" opacity=".3"/>' if night else "")
                     for i, c in enumerate([CORAL, YOLK, SKY, BERRY] * 3)) if n >= 15 else ""
    flowers = "".join(f'<path d="M{x} {y} v12" stroke="#2F9E50" stroke-width="2"/><circle cx="{x}" cy="{y}" r="5" fill="{c}"/><circle cx="{x}" cy="{y}" r="2" fill="{YOLK}"/>'
                      for x, y, c in [(30, 194, "#FF8FB0"), (52, 200, "#fff"), (320, 196, "#FF8FB0"), (340, 202, "#fff")]) if n >= 3 else ""
    fly = (f'<ellipse cx="286" cy="104" rx="7" ry="5" fill="{BERRY}" transform="rotate(-25 286 104)"/><ellipse cx="298" cy="104" rx="7" ry="5" fill="{YOLK}" '
           f'transform="rotate(25 298 104)"/><rect x="290" y="99" width="2" height="10" fill="{INK}"/>') if n >= 6 else ""
    empty = "" if shown else f'<text x="180" y="132" text-anchor="middle" font-size="14" font-weight="700" fill="{TWIG}">Yuvan boş, ilk kelimeni topla</text>'
    return (f'<div class="scene"><svg viewBox="0 0 360 230" width="100%"><rect width="360" height="230" fill="{sky}"/>{sun}{rainbow}'
            f'<rect x="0" y="176" width="360" height="54" fill="{ground}"/><rect x="0" y="168" width="360" height="14" rx="7" fill="{TWIG}"/>{lights}{flowers}{fly}'
            f'<ellipse cx="180" cy="150" rx="84" ry="30" fill="#6B4527"/>{items}{empty}'
            f'<path d="M92 148 q88 70 176 0 v14 q-88 70 -176 0z" fill="{TWIG}"/><path d="M104 160 q76 44 152 0" stroke="#B98A5E" stroke-width="3" fill="none"/>'
            f'<path d="M120 172 q60 28 120 0" stroke="#B98A5E" stroke-width="3" fill="none"/></svg></div>')


# ------------------------------------------------------------------
# MÜFREDAT: Anaokulu, 1. ve 2. sınıf (her biri 6 ünite, 6'şar kelime)
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
        U("k5", "Shapes", "Şekiller", "🔷", "This is {A}.",
          [("Circle", "Daire", "shp:circle"), ("Square", "Kare", "shp:square"), ("Triangle", "Üçgen", "shp:triangle"),
           ("Star", "Yıldız", "shp:star"), ("Heart", "Kalp", "shp:heart"), ("Rectangle", "Dikdörtgen", "shp:rectangle")],
          [("Bu bir daire.", "This is a circle"), ("Yıldız sarıdır.", "The star is yellow")]),
        U("k6", "Vehicles", "Taşıtlar", "🚌", "I see {A}.",
          [("Car", "Araba", "🚗"), ("Bus", "Otobüs", "🚌"), ("Bike", "Bisiklet", "🚲"),
           ("Plane", "Uçak", "✈️"), ("Boat", "Tekne", "⛵"), ("Train", "Tren", "🚆")],
          [("Araba hızlı.", "The car is fast"), ("Otobüse bin.", "Take the bus")]),
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
        U("a5", "My House", "Evim", "🏠", "I see {A}.",
          [("Bed", "Yatak", "🛏️"), ("Chair", "Sandalye", "🪑"), ("Door", "Kapı", "🚪"),
           ("Window", "Pencere", "🪟"), ("Lamp", "Lamba", "💡"), ("TV", "Televizyon", "📺", "I see the TV.")],
          [("Yatak rahat.", "The bed is soft"), ("Kapıyı aç.", "Open the door")]),
        U("a6", "Clothes", "Kıyafetler", "👕", "I wear my {w}.",
          [("T-shirt", "Tişört", "👕"), ("Pants", "Pantolon", "👖"), ("Dress", "Elbise", "👗"),
           ("Shoes", "Ayakkabı", "👟"), ("Hat", "Şapka", "🧢"), ("Socks", "Çorap", "🧦")],
          [("Şapkamı giyerim.", "I wear my hat"), ("Elbise güzel.", "The dress is nice")]),
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
        U("b5", "Jobs", "Meslekler", "👩‍🏫", "I am {A}.",
          [("Doctor", "Doktor", "🧑‍⚕️"), ("Teacher", "Öğretmen", "🧑‍🏫"), ("Chef", "Aşçı", "🧑‍🍳"),
           ("Farmer", "Çiftçi", "🧑‍🌾"), ("Pilot", "Pilot", "🧑‍✈️"), ("Firefighter", "İtfaiyeci", "🧑‍🚒")],
          [("Ben bir aşçıyım.", "I am a chef"), ("O bir doktor.", "She is a doctor")]),
        U("b6", "Actions", "Hareketler", "🏃", "I can {w}.",
          [("Run", "Koşmak", "🏃"), ("Swim", "Yüzmek", "🏊"), ("Jump", "Zıplamak", "🤸"),
           ("Dance", "Dans etmek", "💃"), ("Sing", "Şarkı söylemek", "🎤"), ("Draw", "Resim çizmek", "🖍️")],
          [("Ben koşabilirim.", "I can run"), ("O dans edebilir.", "She can dance")]),
    ]),
}
ALL_UNITS = [u for g in GRADES.values() for u in g["units"]]
BASE_WORDS = {w["id"]: w for u in ALL_UNITS for w in u["words"]}
RANKS = [("A1", "Dal", 0), ("A2", "Yuva", 8), ("B1", "Ağaç", 24), ("B2", "Orman", 50), ("C1", "Gökyüzü", 80)]

# ------------------------------------------------------------------
# STATE (Türkiye saatine göre gün)
# ------------------------------------------------------------------
now = datetime.utcnow() + timedelta(hours=3)
today = now.date()
DEFAULTS = dict(screen="nest", unit=None, phase="learn", nest={}, custom=[], hist={}, streak=1, last_day=None,
                qs=[], qi=0, score=0, picked=None, ok=False, built=[], pool=[], checked=False, sfx=False,
                wids=[], bad=[], mode="review", res={}, story="", hunt=None, name="", color="Sarı", sound=True,
                goal=15, night=now.hour >= 19 or now.hour < 6, qday="", mm=None, mm_wins=0, stories=0, perfect=0,
                user=None, role="student", class_code="", guest=False, saved_h="", set_token=None, al_tried=False)
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state


def touch_day():
    if S.last_day != today.isoformat():
        S.streak = S.streak + 1 if S.last_day == (today - timedelta(1)).isoformat() else 1
        S.last_day = today.isoformat()


def W():
    return {**BASE_WORDS, **{w["id"]: w for w in S.custom}}


def go(**kw):
    for k, v in kw.items():
        S[k] = v


def hbump(k, v=1):
    d = S.hist.setdefault(today.isoformat(), {})
    d[k] = d.get(k, 0) + v


def mastered():
    return sum(1 for v in S.nest.values() if v["box"] >= 4)


def rank():
    return max(i for i, r in enumerate(RANKS) if len(S.nest) >= r[2])


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
BTN = ("font:700 17px 'Baloo 2',Arial;background:#4DA3FF;color:#fff;border:0;border-radius:999px;padding:8px 22px;cursor:pointer;"
       "box-shadow:0 3px 0 #2E7FD6;display:flex;gap:8px;align-items:center")


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
        .f,.k{{position:absolute;inset:0;border-radius:24px;display:flex;flex-direction:column;align-items:center;justify-content:center;
        backface-visibility:hidden;transition:transform .45s;background:#fff;color:#1F2A44;padding:6px;text-align:center;box-shadow:0 3px 0 #C9D6EE,0 8px 18px rgba(31,42,68,.1)}}
        .f img,.f svg{{filter:drop-shadow(0 5px 3px rgba(0,0,0,.1))}}.k{{transform:rotateY(180deg);background:#1F2A44;color:#fff}}
        .c.on .f{{transform:rotateY(180deg)}}.c.on .k{{transform:rotateY(360deg)}}
        .n{{font-size:22px;font-weight:800;margin-top:6px}}.h{{font-size:14px;font-weight:600;margin:4px 0 6px}}
        .k button{{background:rgba(255,255,255,.22);border:0;border-radius:12px;padding:6px 12px;cursor:pointer}}</style>
        <div class="g">{cards}</div><script>{player_js(items)}</script>""", height=rows * 188 + 12)


def sfx(ok):
    if S.sfx:
        S.sfx = False
        if not S.sound:
            return
        n = "[523,659,784]" if ok else "[300,220]"
        components.html(
            "<script>try{const c=new(window.AudioContext||window.webkitAudioContext)();" + n + ".forEach((f,i)=>{const o=c.createOscillator(),"
            "g=c.createGain(),t=c.currentTime+i*.12;o.type='triangle';o.frequency.value=f;o.connect(g);g.connect(c.destination);"
            "g.gain.setValueAtTime(.15,t);g.gain.exponentialRampToValueAtTime(.001,t+.2);o.start(t);o.stop(t+.25);});}catch(e){}</script>", height=0)


def speaking(words):
    rows = "".join(f'<div class="r">{pic(w["e"], 44)}<b>{w["en"]}</b><button onclick="listen({i},{json.dumps(w["en"])})">Söyle</button><span id="r{i}"></span></div>'
                   for i, w in enumerate(words))
    components.html(
        f"""<style>body{{margin:0;font-family:'Baloo 2',Arial}}.r{{display:flex;align-items:center;gap:10px;background:#fff;border-radius:20px;padding:8px 12px;margin:6px 0;
        box-shadow:0 2px 10px rgba(31,42,68,.12)}}.r b{{flex:1;font-size:20px;color:#1F2A44}}button{{background:#FF5C8A;color:#fff;border:0;border-radius:999px;padding:6px 16px;
        font:700 15px 'Baloo 2';cursor:pointer}}span{{font-size:13px;font-weight:700;min-width:90px}}</style>{rows}
        <script>function listen(i,t){{const R=window.SpeechRecognition||window.webkitSpeechRecognition,el=document.getElementById('r'+i);
        if(!R){{el.textContent='Bu tarayıcı desteklemiyor';return}}const r=new R();r.lang='en-US';el.textContent='Dinliyorum...';
        r.onresult=e=>{{const s=e.results[0][0].transcript.toLowerCase().trim(),ok=s.includes(t.toLowerCase());
        el.textContent=ok?'Harika! ✔':'Duydum: '+s;el.style.color=ok?'#0E7C6F':'#C42B58'}};
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
    S.stories += 1
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
# OYUN MANTIĞI
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
    spell = [i for i in wids if " " not in ws[i]["en"] and len(ws[i]["en"]) <= 8]
    random.shuffle(spell)
    qs += [dict(k="spell", w=ws[i]) for i in spell[:2]]
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
    u, new = S.unit, 0
    for w in u["words"]:
        if w["id"] not in S.nest:
            S.nest[w["id"]] = dict(box=0, due=today.isoformat(), ok=0, n=0)
            new += 1
    hbump("new", new)
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
    hbump("n")
    hbump("ok", int(ok))


def choose(opt_id, correct_id):
    S.picked = opt_id
    award(opt_id == correct_id, correct_id)


def pick_word(i):
    S.built.append(S.pool.pop(i))


def check_builder(toks, sep, wid):
    S.checked = True
    award(sep.join(S.built).lower() == sep.join(toks).lower(), wid)


def reset_pool(toks):
    S.pool, S.built = random.sample(toks, len(toks)), []


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
        if S.mode == "review":
            hbump("rev")
        S.perfect += int(S.score == len(S.qs))
        S.res = dict(moves=moves)
        S.phase = "result"


def start_mm():
    ws = list(W().values())
    pool = [W()[i] for i in S.nest if i in W()]
    pick = random.sample(pool, min(6, len(pool)))
    for w in random.sample(ws, len(ws)):
        if len(pick) >= 6:
            break
        if w["id"] not in [p["id"] for p in pick]:
            pick.append(w)
    cards = [(w["id"], w["en"]) for w in pick] + [(w["id"], w["tr"]) for w in pick]
    random.shuffle(cards)
    S.mm = dict(cards=cards, open=[], done=[], tries=0, won=False)


def mm_flip(i):
    m = S.mm
    if len(m["open"]) == 2:
        m["open"] = []
    if i in m["open"] or i in m["done"]:
        return
    m["open"].append(i)
    if len(m["open"]) == 2:
        a, b = m["open"]
        m["tries"] += 1
        if m["cards"][a][0] == m["cards"][b][0]:
            m["done"] += [a, b]
            m["open"] = []
            if len(m["done"]) == len(m["cards"]):
                S.mm_wins += 1


def grade_of(wid):
    return wid[0]


BADGES = [
    ("İlk yumurta", "🥚", "İlk kelimeni topla", lambda: len(S.nest) >= 1),
    ("Civciv", "🐥", "Bir kelime civciv olsun", lambda: any(v["box"] >= 2 for v in S.nest.values())),
    ("Usta kuş", "🦜", "Bir kelime usta kuş olsun", lambda: mastered() >= 1),
    ("Fidan", "🌱", "10 kelime topla", lambda: len(S.nest) >= 10),
    ("Ağaç", "🌳", "30 kelime topla", lambda: len(S.nest) >= 30),
    ("Orman", "🌲", "60 kelime topla", lambda: len(S.nest) >= 60),
    ("Ateş", "🔥", "3 gün üst üste", lambda: S.streak >= 3),
    ("Kusursuz", "💯", "Hatasız tur yap", lambda: S.perfect >= 1),
    ("Eşleştirici", "🧩", "Eşleştirmeyi bitir", lambda: S.mm_wins >= 1),
    ("Fotoğrafçı", "📸", "Kelime avı yap", lambda: len(S.custom) >= 1),
    ("Hikâyeci", "📖", "Hikâye oluştur", lambda: S.stories >= 1),
    ("Gezgin", "🧭", "3 sınıftan kelime topla", lambda: len({grade_of(i) for i in S.nest if i[0] in "kab"}) >= 3),
]

# ------------------------------------------------------------------
# HESAP SİSTEMİ: yuva adı + PIN, Supabase (yoksa yerel dosya), sınıf kodu
# ------------------------------------------------------------------
PERSIST = ("nest", "custom", "hist", "streak", "last_day", "name", "color", "goal", "sound", "mm_wins", "stories", "perfect")
TRMAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
DATA_DIR = "data_lingonest"


def secret(k, default=None):
    try:
        return st.secrets[k]
    except Exception:
        return os.environ.get(k, default)


def norm_user(u):
    return re.sub(r"[^a-z0-9_]", "", u.strip().translate(TRMAP).lower())


def hpin(u, pin):
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), (u + (secret("AUTH_SECRET") or "dev")).encode(), 100_000).hex()


def make_token(u, ph):
    return u + "." + hmac.new((secret("AUTH_SECRET") or "dev").encode(), (u + ph).encode(), "sha256").hexdigest()[:32]


def _sb():
    url, key = secret("SUPABASE_URL"), secret("SUPABASE_KEY")
    return (url.rstrip("/") + "/rest/v1/profiles", {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}) if url and key else None


def _fp(u):
    return os.path.join(DATA_DIR, f"{u}.json")


def db_get(u):
    import requests
    c = _sb()
    if c:
        r = requests.get(c[0], params={"username": f"eq.{u}", "select": "*"}, headers=c[1], timeout=10)
        r.raise_for_status()
        rows = r.json()
        return rows[0] if rows else None
    return json.load(open(_fp(u), encoding="utf-8")) if os.path.exists(_fp(u)) else None


def db_insert(row):
    import requests
    c = _sb()
    if c:
        requests.post(c[0], headers={**c[1], "Prefer": "return=minimal"}, json=row, timeout=10).raise_for_status()
    else:
        os.makedirs(DATA_DIR, exist_ok=True)
        json.dump(row, open(_fp(row["username"]), "w", encoding="utf-8"), ensure_ascii=False)


def db_patch(u, fields):
    import requests
    c = _sb()
    if c:
        requests.patch(c[0], params={"username": f"eq.{u}"}, headers={**c[1], "Prefer": "return=minimal"}, json=fields, timeout=10).raise_for_status()
    else:
        row = db_get(u)
        if row:
            row.update(fields)
            db_insert(row)


def db_delete(u):
    import requests
    c = _sb()
    if c:
        requests.delete(c[0], params={"username": f"eq.{u}"}, headers=c[1], timeout=10).raise_for_status()
    elif os.path.exists(_fp(u)):
        os.remove(_fp(u))


def db_class(code, role):
    import requests
    c = _sb()
    if c:
        r = requests.get(c[0], params={"class_code": f"eq.{code}", "role": f"eq.{role}", "select": "username,summary"}, headers=c[1], timeout=10)
        r.raise_for_status()
        return r.json()
    out = []
    for f in os.listdir(DATA_DIR) if os.path.isdir(DATA_DIR) else []:
        row = json.load(open(os.path.join(DATA_DIR, f), encoding="utf-8"))
        if row.get("class_code") == code and row.get("role") == role:
            out.append(row)
    return out


def summary():
    tot, ok = sum(v["n"] for v in S.nest.values()), sum(v["ok"] for v in S.nest.values())
    return dict(words=len(S.nest), mastered=mastered(), acc=int(ok / tot * 100) if tot else 0, streak=S.streak, last=today.isoformat())


def autosave():
    if not S.user:
        return
    blob = {k: S[k] for k in PERSIST}
    h = hashlib.md5(json.dumps(blob, sort_keys=True).encode()).hexdigest()
    if h != S.saved_h:
        try:
            db_patch(S.user, {"data": blob, "summary": summary()})
            S.saved_h = h
        except Exception:
            st.toast("Kayıt yapılamadı, internet bağlantısını kontrol et.")


def enter(row, remember):
    d = row.get("data") or {}
    for k in PERSIST:
        if k in d:
            S[k] = d[k]
    S.user, S.role, S.class_code, S.saved_h = row["username"], row.get("role", "student"), row.get("class_code") or "", ""
    S.screen = "nest"
    if remember:
        S.set_token = make_token(row["username"], row["pin_hash"])
        st.query_params["t"] = S.set_token


def verify_token(t):
    try:
        u = t.split(".")[0]
        row = db_get(u)
        if row and hmac.compare_digest(t, make_token(u, row["pin_hash"])):
            return row
    except Exception:
        pass
    return None


def do_login(u, pin, remember):
    u = norm_user(u)
    try:
        row = db_get(u)
        if not row:
            return "Bu adla bir yuva bulunamadı."
        if (row.get("locked_until") or "") > datetime.utcnow().isoformat():
            return "Çok fazla yanlış deneme. 5 dakika sonra tekrar dene."
        if row["pin_hash"] != hpin(u, pin):
            f = (row.get("fails") or 0) + 1
            db_patch(u, dict(fails=0, locked_until=(datetime.utcnow() + timedelta(minutes=5)).isoformat()) if f >= 5 else dict(fails=f))
            return "PIN yanlış."
        db_patch(u, dict(fails=0))
        enter(row, remember)
    except Exception as ex:
        return f"Bağlantı sorunu ({type(ex).__name__}). Biraz sonra tekrar dene."
    return None


def do_register(u, pin, pin2, role, code, consent, remember):
    u = norm_user(u)
    if not 3 <= len(u) <= 20:
        return "Yuva adı 3-20 harf veya rakam olmalı (boşluk ve özel işaret yok)."
    if not re.fullmatch(r"\d{4,6}", pin):
        return "PIN 4-6 rakam olmalı."
    if pin != pin2:
        return "PIN'ler aynı değil."
    if not consent:
        return "Devam etmek için veli/öğretmen onayı gerekli."
    try:
        if db_get(u):
            return "Bu ad dolu, başka bir ad dene."
        code = code.strip().upper()
        if role == "teacher":
            code = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))
        elif code and not db_class(code, "teacher"):
            return "Bu sınıf kodu bulunamadı."
        row = dict(username=u, pin_hash=hpin(u, pin), role=role, class_code=code or None, data={}, summary={}, fails=0, locked_until="")
        db_insert(row)
        enter(row, remember)
    except Exception as ex:
        return f"Bağlantı sorunu ({type(ex).__name__}). Biraz sonra tekrar dene."
    return None


def logout():
    for k, v in DEFAULTS.items():
        S[k] = copy.deepcopy(v)
    S.set_token, S.al_tried = "", True
    try:
        st.query_params.clear()
    except Exception:
        pass


def flush_token():
    if S.set_token is not None:
        components.html(f"<script>try{{localStorage.setItem('lnt',{json.dumps(S.set_token)})}}catch(e){{}}</script>", height=0)
        S.set_token = None


def autologin_js():
    components.html("<script>try{const t=localStorage.getItem('lnt');const p=window.parent;"
                    "if(t&&!p.location.search.includes('t=')){p.location.search='?t='+encodeURIComponent(t);}}catch(e){}</script>", height=0)


def auth_screen():
    st.markdown(f'<div class="hero"><span class="bob">{chick(72)}</span><div><h2>LingoNest</h2><p>Kelimelerini yuvada büyüt.</p></div></div>', unsafe_allow_html=True)
    flush_token()
    if not S.al_tried:
        S.al_tried = True
        autologin_js()
    t1, t2 = st.tabs(["Giriş yap", "Yeni yuva kur"])
    with t1:
        u = st.text_input("Yuva adı", key="li_u")
        p = st.text_input("PIN", type="password", max_chars=6, key="li_p")
        r = st.checkbox("Bu cihazda hatırla", value=True, key="li_r")
        if st.button("Giriş yap", type="primary", use_container_width=True, key="li_b"):
            err = do_login(u, p, r)
            st.error(err) if err else st.rerun()
    with t2:
        st.caption("Gerçek ad yazma, takma ad seç. Kişisel veri toplanmaz.")
        u = st.text_input("Yuva adı (takma ad)", key="rg_u")
        c1, c2 = st.columns(2)
        p = c1.text_input("PIN (4-6 rakam)", type="password", max_chars=6, key="rg_p")
        p2 = c2.text_input("PIN tekrar", type="password", max_chars=6, key="rg_p2")
        role = st.radio("Ben", ["Öğrenci", "Öğretmen"], horizontal=True, key="rg_r")
        code = st.text_input("Sınıf kodu (varsa)", key="rg_c") if role == "Öğrenci" else ""
        ok = st.checkbox("Veli veya öğretmen onayıyla kullanıyorum", key="rg_ok")
        r = st.checkbox("Bu cihazda hatırla", value=True, key="rg_rem")
        if st.button("Yuvamı kur", type="primary", use_container_width=True, key="rg_b"):
            err = do_register(u, p, p2, "teacher" if role == "Öğretmen" else "student", code, ok, r)
            st.error(err) if err else st.rerun()
    st.button("Misafir olarak dene (kaydedilmez)", use_container_width=True, on_click=go, kwargs={"guest": True})
    if not _sb():
        st.caption("Not: Veritabanı bağlı değil, hesaplar sunucu yeniden başlayınca silinebilir.")


tok = st.query_params.get("t")
if tok and not S.user:
    _row = verify_token(tok)
    if _row:
        enter(_row, False)
    else:
        S.set_token = ""
        st.query_params.clear()
if not S.user and not S.guest:
    auth_screen()
    st.stop()
touch_day()
flush_token()


# ------------------------------------------------------------------
# ÜST PANEL
# ------------------------------------------------------------------
def head():
    r = RANKS[rank()]
    st.markdown(f"""<div class="top"><div class="bd">{chick(44)}<span>Lingo<b>Nest</b></span></div><div class="chips">
        <span class="ch">{tw('🔥', 20)}{S.streak}</span><span class="ch">{tw('🥚', 20)}{len(S.nest)}</span>
        <span class="ch rk">{r[0]}</span></div></div>""", unsafe_allow_html=True)
    items = [("nest", "Yuva", ":material/home:"), ("explore", "Keşfet", ":material/explore:"),
             ("adv", "Macera", ":material/auto_awesome:"), ("panel", "Panel", ":material/bar_chart:")]
    if S.role == "teacher":
        items.append(("class", "Sınıf", ":material/groups:"))
    cols = st.columns(len(items))
    for c, (k, lab, ic) in zip(cols, items):
        c.button(lab, key=f"n_{k}", icon=ic, use_container_width=True, type="primary" if S.screen == k else "secondary",
                 on_click=go, kwargs={"screen": k})


def quests():
    d = S.hist.get(today.isoformat(), {})
    qs = [("Yeni kelime", d.get("new", 0), 3, "🥚"), ("Yuva bakımı", d.get("rev", 0), 1, "🌱"), ("Doğru cevap", d.get("ok", 0), S.goal, "🎯")]
    html = "".join(f'<div class="q"><div class="ring" style="--p:{min(100, int(v / g * 100))}"><span>{tw(ic, 24)}</span></div><b>{min(v, g)}/{g}</b><small>{lab}</small></div>'
                   for lab, v, g, ic in qs)
    return f'<div class="qs">{html}</div>', all(v >= g for _, v, g, _ in qs)


# ------------------------------------------------------------------
# EKRANLAR
# ------------------------------------------------------------------
if S.screen == "nest":
    head()
    q_html, q_done = quests()
    if q_done and S.qday != today.isoformat():
        S.qday = today.isoformat()
        st.balloons()
        st.toast("Bugünkü üç görev tamam!")
    st.markdown(f'<div class="hero"><span class="bob">{chick(64)}</span><div><h2>Merhaba {S.name or "kaşif"}!</h2>'
                f'<p>{S.streak} gündür yuvana bakıyorsun.</p></div></div>', unsafe_allow_html=True)
    st.markdown(nest_svg([v["box"] for v in S.nest.values()], S.night), unsafe_allow_html=True)
    nxt_d = next(((t, n) for t, n in DECOS if len(S.nest) < t), None)
    st.markdown(f'<div class="hint">{f"{nxt_d[0] - len(S.nest)} kelime sonra yeni süs: {nxt_d[1]}" if nxt_d else "Yuvan tüm süslerle donandı"}</div>', unsafe_allow_html=True)
    st.button("Gündüze geç" if S.night else "Geceye geç", icon=":material/light_mode:" if S.night else ":material/dark_mode:",
              use_container_width=True, on_click=lambda: S.__setitem__("night", not S.night))
    cnt = [sum(1 for v in S.nest.values() if v["box"] == b) for b in range(5)]
    st.markdown('<div class="stg">' + "".join(f'<div>{tw(e, 30)}<b>{cnt[i]}</b>{n}</div>' for i, (n, e) in enumerate(STAGES)) + "</div>",
                unsafe_allow_html=True)
    r = rank()
    nxt = RANKS[r + 1] if r + 1 < len(RANKS) else None
    pct = 100 if not nxt else int((len(S.nest) - RANKS[r][2]) / (nxt[2] - RANKS[r][2]) * 100)
    st.markdown(f'<div class="row"><b>{RANKS[r][0]} {RANKS[r][1]}</b><div class="bar"><div style="width:{pct}%"></div></div>'
                f'<small>{f"{nxt[2] - len(S.nest)} kelime" if nxt else "Zirve"}</small></div>{q_html}', unsafe_allow_html=True)
    n = len(due_ids())
    if not S.nest:
        st.button("İlk kelimelerini topla", type="primary", use_container_width=True, on_click=go, kwargs={"screen": "explore"})
    else:
        st.button(f"Yuva bakımı · {n} kelime bekliyor" if n else "Bugün bakım yok, yarın gel", type="primary",
                  use_container_width=True, disabled=n == 0, on_click=start_review)
    wd = list(BASE_WORDS.values())[today.toordinal() % len(BASE_WORDS)]
    st.markdown(f'<h3 style="margin-top:18px">Günün kelimesi</h3><div class="card"><div class="art" style="margin:0 0 8px">{pic(wd["e"], 96)}</div>'
                f'<div class="t">{wd["en"]} = {wd["tr"]}</div><small>{wd["s"]}</small></div>', unsafe_allow_html=True)
    speak_html(wd["s"], label="Cümleyi dinle")

elif S.screen == "explore":
    head()
    tabs = st.tabs([g["title"] for g in GRADES.values()])
    for tab, g in zip(tabs, GRADES.values()):
        with tab:
            cols = st.columns(2)
            for i, u in enumerate(g["units"]):
                have = sum(1 for w in u["words"] if w["id"] in S.nest)
                with cols[i % 2]:
                    st.markdown(f'<div class="card">{tw(u["ic"], 54)}<div class="t">{u["title"]}</div><small>{u["tr"]}</small>'
                                f'<div class="bar" style="margin-top:8px"><div style="width:{have / len(u["words"]) * 100}%"></div></div><small>{have}/{len(u["words"])} yuvada</small></div>',
                                unsafe_allow_html=True)
                    st.button("Tekrar çalış" if have == len(u["words"]) else "Topla", key=f"u_{u['id']}", type="primary", use_container_width=True,
                              on_click=start_unit, args=(u,))

elif S.screen == "adv":
    head()
    t0, t1, t2, t3 = st.tabs(["Eşleştir", "Hikâye", "Kelime avı", "Konuş"])
    nest_words = [W()[i] for i in S.nest if i in W()]
    with t0:
        st.button("Yeni oyun" if S.mm else "Oyuna başla", type="primary", use_container_width=True, on_click=start_mm)
        m = S.mm
        if m:
            st.caption(f"Hamle: {m['tries']} · Bulunan çift: {len(m['done']) // 2}/{len(m['cards']) // 2}")
            cols = st.columns(3)
            for i, (wid, text) in enumerate(m["cards"]):
                shown = i in m["open"] or i in m["done"]
                cols[i % 3].button(text if shown else "?", key=f"mm{i}", use_container_width=True, disabled=i in m["done"],
                                   type="primary" if i in m["done"] else "secondary", on_click=mm_flip, args=(i,))
            if len(m["done"]) == len(m["cards"]):
                if not m["won"]:
                    m["won"] = True
                    st.balloons()
                st.success(f"Hepsini buldun! {m['tries']} hamlede bitirdin.")
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
            st.caption("Kişi fotoğrafı çekme, sadece eşya göster.")
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
        pool = nest_words[:6] if nest_words else list(BASE_WORDS.values())[:6]
        st.caption("Söyle düğmesine bas ve kelimeyi yüksek sesle söyle.")
        speaking(pool)

elif S.screen == "panel":
    head()
    p1, p2, p3 = st.tabs(["Gelişim", "Rozetler", "Ayarlar"])
    with p1:
        days = [today - timedelta(d) for d in range(6, -1, -1)]
        H = [S.hist.get(d.isoformat(), {}) for d in days]
        vals = [h.get("n", 0) for h in H]
        mx = max(vals + [1])
        names = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        bars = "".join(f'<div class="cc {"t" if d == today else ""}"><em>{v or ""}</em><i style="height:{max(4, int(v / mx * 110))}px"></i>'
                       f'<span>{names[d.weekday()]}</span></div>' for d, v in zip(days, vals))
        ok, n = sum(h.get("ok", 0) for h in H), sum(vals)
        dots = "".join(f'<i class="{"on" if S.hist.get((today - timedelta(d)).isoformat(), {}).get("n") else ""}"></i>' for d in range(13, -1, -1))
        st.markdown(f"""<div class="grid"><div class="tile"><b>{vals[-1]}</b><span>Bugün cevap</span></div><div class="tile"><b>{n}</b><span>Haftalık cevap</span></div>
            <div class="tile"><b>%{int(ok / n * 100) if n else 0}</b><span>Haftalık doğruluk</span></div>
            <div class="tile"><b>{mastered()}/{len(S.nest)}</b><span>Usta kuş / yuvadaki</span></div></div>
            <h3>Son 7 gün</h3><div class="chart">{bars}</div><h3>Son 14 gün</h3><div class="dots">{dots}</div><h3>Ünite gelişimi</h3>""",
                    unsafe_allow_html=True)
        rows = ""
        for u in ALL_UNITS:
            ids = [w["id"] for w in u["words"]]
            have = sum(1 for i in ids if i in S.nest)
            m = sum(1 for i in ids if S.nest.get(i, {}).get("box", 0) >= 3)
            rows += f'<div class="row">{tw(u["ic"], 26)}<span>{u["title"]}</span><div class="bar"><div style="width:{m / len(ids) * 100}%"></div></div><small>{have}/{len(ids)}</small></div>'
        st.markdown(rows, unsafe_allow_html=True)
        hard = sorted([(v["ok"] / v["n"], i) for i, v in S.nest.items() if v["n"] >= 2 and i in W()])[:5]
        if hard:
            st.markdown("<h3>Zorlanılan kelimeler</h3>" + "".join(
                f'<div class="row">{pic(W()[i]["e"], 30)}<span>{W()[i]["en"]} · {W()[i]["tr"]}</span><small>%{int(p * 100)}</small></div>' for p, i in hard),
                unsafe_allow_html=True)
        buf = io.StringIO()
        cw = csv.writer(buf)
        cw.writerow(["kelime", "turkce", "unite", "kutu", "dogru", "toplam", "sonraki_bakim"])
        for i, v in S.nest.items():
            if i in W():
                w = W()[i]
                cw.writerow([w["en"], w["tr"], w.get("u", ""), v["box"], v["ok"], v["n"], v["due"]])
        st.download_button("Rapor (CSV)", buf.getvalue(), "lingonest_rapor.csv", use_container_width=True, icon=":material/download:")
    with p2:
        got = [b for b in BADGES if b[3]()]
        html = "".join(f'<div class="bgi {"" if b in got else "off"}">{tw(b[1], 56)}<div>{b[0]}</div><small>{b[2]}</small></div>' for b in BADGES)
        st.markdown(f"<h3>{len(got)}/{len(BADGES)} rozet</h3><div class='bg'>{html}</div>", unsafe_allow_html=True)
    with p3:
        st.text_input("Adın", value=S.name, key="w_name", on_change=lambda: S.__setitem__("name", S.w_name))
        st.radio("Maskot rengi", list(COLORS), index=list(COLORS).index(S.color), horizontal=True, key="w_color",
                 on_change=lambda: S.__setitem__("color", S.w_color))
        st.select_slider("Günlük hedef (doğru cevap)", [5, 10, 15, 20, 30], value=S.goal, key="w_goal",
                         on_change=lambda: S.__setitem__("goal", S.w_goal))
        st.toggle("Ses efektleri", value=S.sound, key="w_sound", on_change=lambda: S.__setitem__("sound", S.w_sound))
        if S.user:
            st.markdown(f'<div class="row"><b>{S.user}</b><small>{"Öğretmen" if S.role == "teacher" else "Öğrenci"}'
                        f'{" · Sınıf kodu: " + S.class_code if S.class_code else ""}</small></div>', unsafe_allow_html=True)
            st.button("Çıkış yap", icon=":material/logout:", use_container_width=True, on_click=logout)
            with st.expander("Hesabı sil"):
                st.caption("Tüm ilerleme ve hesap kalıcı olarak silinir.")
                if st.checkbox("Silinmesini istiyorum", key="del_ok") and st.button("Hesabı kalıcı sil", use_container_width=True):
                    try:
                        db_delete(S.user)
                        logout()
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Silinemedi ({type(ex).__name__}).")
        else:
            st.info("Misafir modundasın, ilerleme kaydedilmez.")
            st.button("Giriş yap veya kayıt ol", type="primary", use_container_width=True, on_click=go, kwargs={"guest": False})
        st.download_button("Yedek indir (JSON)", json.dumps({k: S[k] for k in PERSIST}), "lingonest_yedek.json", use_container_width=True,
                           icon=":material/save:")
        st.caption("Görseller: Twemoji, CC-BY 4.0")

elif S.screen == "class" and S.role == "teacher":
    head()
    st.markdown(f'<div class="hero"><div><h2>Sınıf kodun: {S.class_code}</h2><p>Öğrenciler kayıt olurken bu kodu girer.</p></div></div>', unsafe_allow_html=True)
    try:
        studs = db_class(S.class_code, "student")
    except Exception as ex:
        studs = []
        st.error(f"Liste alınamadı ({type(ex).__name__}).")
    if not studs:
        st.info("Henüz sınıfa katılan öğrenci yok.")
    else:
        rows, buf = "", io.StringIO()
        cw = csv.writer(buf)
        cw.writerow(["ogrenci", "kelime", "usta_kus", "dogruluk", "seri", "son_giris"])
        for r in sorted(studs, key=lambda r: -(r.get("summary") or {}).get("words", 0)):
            sm = r.get("summary") or {}
            rows += (f'<div class="row"><b style="flex:1">{r["username"]}</b><small>{sm.get("words", 0)} kelime · {sm.get("mastered", 0)} usta · '
                     f'%{sm.get("acc", 0)} · {sm.get("last", "-")}</small></div>')
            cw.writerow([r["username"], sm.get("words", 0), sm.get("mastered", 0), sm.get("acc", 0), sm.get("streak", 0), sm.get("last", "")])
        st.markdown(f"<h3>{len(studs)} öğrenci</h3>{rows}", unsafe_allow_html=True)
        st.download_button("Sınıf raporu (CSV)", buf.getvalue(), "sinif_raporu.csv", use_container_width=True, icon=":material/download:")

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
        if q["k"] in ("see", "hear"):
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
            spell = q["k"] == "spell"
            toks = list(q["w"]["en"].lower()) if spell else q["s"]["words"]
            sep, wid = ("", q["w"]["id"]) if spell else (" ", None)
            if not S.pool and not S.built and not S.checked:
                reset_pool(toks)
            if spell:
                st.markdown(f"<p class='ask'>Kelimeyi harflerle yaz</p><div class='art'>{pic(q['w']['e'], 110)}<h3 style='margin:6px 0 0'>{q['w']['tr']}</h3></div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='ask'>İngilizcesini kur</p><div class='art'><h2 style='margin:0'>{q['s']['tr']}</h2></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='built'>{''.join(f'<span class=w>{x}</span>' for x in S.built)}</div>", unsafe_allow_html=True)
            if not S.checked:
                nc = 4 if spell else 3
                cols = st.columns(min(max(len(S.pool), 1), nc))
                for i, x in enumerate(S.pool):
                    cols[i % len(cols)].button(x, key=f"w{S.qi}_{i}_{x}", use_container_width=True, on_click=pick_word, args=(i,))
                a, b = st.columns(2)
                a.button("Sıfırla", icon=":material/refresh:", use_container_width=True, on_click=reset_pool, args=(toks,))
                b.button("Kontrol et", type="primary", use_container_width=True, disabled=not S.built, on_click=check_builder, args=(toks, sep, wid))
            else:
                sfx(S.ok)
                target = sep.join(toks)
                st.markdown(f"<div class='sheet {'ok' if S.ok else 'no'}'>{chick(52, not S.ok)}<div><b>{'Mükemmel!' if S.ok else 'Doğrusu:'}</b>"
                            f"<br><span>{target}</span></div></div>", unsafe_allow_html=True)
                speak_html(q["w"]["en"] if spell else target)
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


autosave()
