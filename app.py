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
import string
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from html import escape as esc

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
div[data-testid="stColumn"] .stButton>button,div[data-testid="column"] .stButton>button{padding-left:.35rem;padding-right:.35rem}
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
.card.on{box-shadow:0 3px 0 #17B8A6,0 8px 18px rgba(23,184,166,.2)}
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
.bub{border-radius:20px;padding:8px 14px;margin:6px 0;max-width:86%;font-weight:600;font-size:17px;line-height:1.3;width:fit-content}
.bub.bot{background:#fff;box-shadow:0 2px 0 #C9D6EE;margin-right:auto}
.bub.me{background:#4DA3FF;color:#fff;margin-left:auto}
.lvl{display:flex;align-items:center;gap:8px;font-weight:700;font-size:14px;margin:6px 0 10px}.lvl .bar{flex:1;margin:0}.lvl small{color:#5B6A8A}
.fixed{background:#fff;border-radius:20px;padding:12px 14px;margin:8px 0;box-shadow:0 3px 0 #C9D6EE;font-weight:600}
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


def clean_emoji(s):
    s = (s or "").strip()
    return s if 0 < len(s) <= 8 and all(ord(c) > 0x2000 for c in s) else "⭐"


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
        return f'<img src="{esc(e)}" width="{px}" height="{px}" style="object-fit:cover;border-radius:18px">'
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


# ---- Mağaza: maskot aksesuarları (yuva: kafa / yüz / boyun) ----
SHOP = {"crown": ("Taç", 40, "hat"), "party": ("Parti şapkası", 25, "hat"), "glasses": ("Güneş gözlüğü", 30, "face"),
        "bow": ("Fiyonk", 20, "neck"), "scarf": ("Atkı", 35, "neck")}
ACC_SVG = {
    "crown": '<path d="M40 24 L43 6 L52 15 L60 2 L68 15 L77 6 L80 24Z" fill="#FFC531" stroke="#E0A100" stroke-width="2.5" stroke-linejoin="round"/>'
             '<circle cx="60" cy="9" r="2.5" fill="#FF5C8A"/>',
    "party": '<path d="M46 28 L60 3 L74 28Z" fill="#4DA3FF" stroke="#2E7FD6" stroke-width="2" stroke-linejoin="round"/><circle cx="60" cy="4" r="4" fill="#FFC531"/>'
             '<circle cx="56" cy="17" r="2.5" fill="#fff"/><circle cx="64" cy="22" r="2.5" fill="#FF5C8A"/>',
    "glasses": '<circle cx="42" cy="56" r="11" fill="rgba(255,255,255,.28)" stroke="#1F2A44" stroke-width="3"/>'
               '<circle cx="78" cy="56" r="11" fill="rgba(255,255,255,.28)" stroke="#1F2A44" stroke-width="3"/><path d="M53 56 h14" stroke="#1F2A44" stroke-width="3"/>',
    "bow": '<path d="M60 96 l-15 -9 v18z M60 96 l15 -9 v18z" fill="#FF5C8A"/><circle cx="60" cy="96" r="4.5" fill="#D93B69"/>',
    "scarf": '<path d="M22 92 q38 20 76 0 v10 q-38 20 -76 0z" fill="#FF7A59"/><rect x="74" y="98" width="12" height="20" rx="4" fill="#FF7A59"/>',
}


def chick(px=48, sad=False, eq=None):
    body, wing = COLORS.get(st.session_state.get("color", "Sarı"), COLORS["Sarı"])
    eq = st.session_state.get("eq", {}) if eq is None else eq
    acc = "".join(ACC_SVG[eq[s]] for s in ("neck", "face", "hat") if eq.get(s) in ACC_SVG)
    mouth = f'<path d="M52 78 q8 -7 16 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>' if sad else ""
    return (f'<svg width="{px}" height="{px}" viewBox="0 0 120 120"><path d="M52 14 q4 -10 8 0 q4 -10 8 0 q-8 8 -16 0z" fill="{CORAL}"/>'
            f'<circle cx="60" cy="64" r="46" fill="{body}"/><ellipse cx="22" cy="72" rx="12" ry="18" fill="{wing}" transform="rotate(20 22 72)"/>'
            f'<ellipse cx="98" cy="72" rx="12" ry="18" fill="{wing}" transform="rotate(-20 98 72)"/>'
            f'<circle cx="42" cy="56" r="7" fill="{INK}"/><circle cx="78" cy="56" r="7" fill="{INK}"/>'
            f'<circle cx="44" cy="53" r="2.5" fill="#fff"/><circle cx="80" cy="53" r="2.5" fill="#fff"/>'
            f'<path d="M50 68 h20 l-10 12z" fill="{CORAL}"/><circle cx="30" cy="72" r="6" fill="#FFAB91" opacity=".6"/>'
            f'<circle cx="90" cy="72" r="6" fill="#FFAB91" opacity=".6"/>{mouth}{acc}</svg>')


STAGES = [("Yumurta", "🥚"), ("Çatlıyor", "🐣"), ("Civciv", "🐥"), ("Kuş", "🐦"), ("Usta kuş", "🦜")]
INTERVALS = [0, 1, 2, 4, 7]  # Leitner kutuları: bakım aralığı (gün)
DECOS = [(3, "Çiçekler"), (6, "Kelebek"), (10, "Gökkuşağı"), (15, "Işık dizisi")]
DAYS = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


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
UNIT_BY_ID = {u["id"]: u for u in ALL_UNITS}
BASE_WORDS = {w["id"]: w for u in ALL_UNITS for w in u["words"]}
RANKS = [("A1", "Dal", 0), ("A2", "Yuva", 8), ("B1", "Ağaç", 24), ("B2", "Orman", 50), ("C1", "Gökyüzü", 80)]
GRADE_NAMES = {"k": "Anaokulu", "a": "1. Sınıf", "b": "2. Sınıf"}
AI_LIMIT = 25  # kullanıcı başına günlük yapay zekâ çağrısı

# Konuşma sahneleri: (Civi'nin cümlesi, Türkçesi, doğru cevap, Türkçesi, [iki yanlış cevap])
DIALOGS = [
    dict(id="d1", title="Okulda", ic="🏫", turns=[
        ("Hello! What is your name?", "Merhaba! Adın ne?", "My name is Sam.", "Benim adım Sam.", ["It is a cat.", "I like red."]),
        ("How are you?", "Nasılsın?", "I am fine, thank you.", "İyiyim, teşekkürler.", ["Yes, I do.", "It is blue."]),
        ("Goodbye!", "Hoşça kal!", "Goodbye, see you!", "Hoşça kal, görüşürüz!", ["I have a ball.", "Two apples."])]),
    dict(id="d2", title="Kafede", ic="☕", turns=[
        ("What do you want?", "Ne istersin?", "I want milk, please.", "Süt istiyorum, lütfen.", ["I am a pilot.", "It is sunny."]),
        ("Here you are!", "Buyur!", "Thank you!", "Teşekkürler!", ["I am sleepy.", "Red, please."]),
        ("Do you like bread?", "Ekmek sever misin?", "Yes, I like bread.", "Evet, ekmek severim.", ["It is cloudy.", "My name is Ali."])]),
    dict(id="d3", title="Ailem", ic="👨‍👩‍👧", turns=[
        ("Who is she?", "O kim?", "She is my mother.", "O benim annem.", ["It is a book.", "I can jump."]),
        ("Is he your brother?", "O senin erkek kardeşin mi?", "Yes, he is my brother.", "Evet, o benim kardeşim.", ["I like apples.", "It is hot."]),
        ("Do you love your family?", "Aileni sever misin?", "Yes, I love my family.", "Evet, ailemi severim.", ["It is rainy.", "I wear a hat."])]),
    dict(id="d4", title="Hava durumu", ic="🌦️", turns=[
        ("How is the weather?", "Hava nasıl?", "It is sunny.", "Hava güneşli.", ["I am a chef.", "My name is Lara."]),
        ("Is it cold?", "Hava soğuk mu?", "No, it is hot.", "Hayır, sıcak.", ["I have a robot.", "She is a teacher."]),
        ("Let's go outside!", "Haydi dışarı çıkalım!", "Yes, let's go!", "Evet, gidelim!", ["It is a pencil.", "Goodbye, cat."])]),
    dict(id="d5", title="Hayvanat bahçesi", ic="🦁", turns=[
        ("What do you see?", "Ne görüyorsun?", "I see a lion.", "Bir aslan görüyorum.", ["I am hot.", "I eat bread."]),
        ("Is the elephant big?", "Fil büyük mü?", "Yes, it is big.", "Evet, büyük.", ["I can swim.", "My name is Tom."]),
        ("Can the rabbit jump?", "Tavşan zıplayabilir mi?", "Yes, it can jump.", "Evet, zıplayabilir.", ["It is a red ball.", "I am a farmer."])]),
    dict(id="d6", title="Kıyafet alışverişi", ic="👗", turns=[
        ("What do you wear?", "Ne giyiyorsun?", "I wear a hat.", "Şapka giyiyorum.", ["It is rainy.", "I see a bus."]),
        ("What color is your dress?", "Elbisen ne renk?", "It is pink.", "Pembe.", ["I can run.", "I am a pilot."]),
        ("Do you like it?", "Beğendin mi?", "Yes, I like it!", "Evet, beğendim!", ["It is Tuesday.", "Goodbye, teacher."])]),
]
DLG_BY_ID = {d["id"]: d for d in DIALOGS}
ACTS = [("mm", "Eşleştir", "🧩", "Kartları eşleştir"), ("hm", "Kuş Kurtar", "🛟", "Harfleri tahmin et"), ("dlg", "Sahne", "🎭", "Civi ile konuş"),
        ("story", "Hikâye", "📖", "Kendi hikâyen"), ("speak", "Konuş", "🎤", "Söyle, dinlesin"), ("hunt", "Kelime avı", "📸", "Eşya fotoğrafla"),
        ("civi", "Civi", "💬", "Sohbet ve cümle")]

# ------------------------------------------------------------------
# STATE (Türkiye saatine göre gün)
# ------------------------------------------------------------------
def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


now = utcnow() + timedelta(hours=3)
today = now.date()
DEFAULTS = dict(screen="nest", unit=None, phase="learn", nest={}, custom=[], hist={}, streak=1, last_day=None,
                qs=[], qi=0, score=0, picked=None, ok=False, built=[], pool=[], checked=False, sfx=False,
                wids=[], bad=[], mode="review", res={}, story="", hunt=None, name="", color="Sarı", sound=True,
                goal=15, night=now.hour >= 19 or now.hour < 6, qday="", mm=None, mm_wins=0, stories=0, perfect=0,
                user=None, role="student", class_code="", guest=False, saved_h="", set_token=None, al_tried=False,
                # --- yeni ---
                xp=0, seeds=0, owned=[], eq={}, accent="us", chest_day="", hw=[], placed="", ai_day="", ai_n=0,
                hm=None, hm_wins=0, chats=0, chat=[], fix=None, qt=0, sess=dict(xp=0, seeds=0, t=[]), pl={},
                freeze=0, tests=[], big=False, calm=False, dys=False, dlg_done=[], dlg=None, act=None, t0=0.0)
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state
if not S.t0:
    S.t0 = time.time()
_x = ""
if S.dys:
    _x += ("@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;700&display=swap');"
           "html,body,.stApp,button,input,textarea{font-family:'Lexend',sans-serif!important;letter-spacing:.02em}")
if S.big:
    _x += (".ask{font-size:27px!important}.opt{font-size:23px!important;min-height:64px!important}.w{font-size:24px!important}"
           ".stButton>button{font-size:19px!important}.card .t{font-size:22px!important}.bub{font-size:20px!important}.row{font-size:17px}")
if S.calm:
    _x += "*{animation:none!important;transition:none!important}"
if _x:
    st.markdown(f"<style>{_x}</style>", unsafe_allow_html=True)


def touch_day():
    t = today.isoformat()
    if S.last_day != t:
        try:
            gap = (today - date.fromisoformat(S.last_day)).days if S.last_day else None
        except ValueError:
            gap = None
        if gap == 1:
            S.streak += 1
        elif gap == 2 and S.freeze > 0:
            S.freeze -= 1
            S.streak += 1
            st.toast("Seri koruyucu seni kurtardı, serin devam ediyor!")
        else:
            S.streak = 1
        S.last_day = t
    cut = (today - timedelta(90)).isoformat()
    for d in [d for d in S.hist if d < cut]:
        del S.hist[d]


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


def level():
    L = 1 + int((S.xp / 40) ** .5)
    lo, hi = 40 * (L - 1) ** 2, 40 * L ** 2
    return L, int((S.xp - lo) / (hi - lo) * 100), hi - S.xp


def hard_ids(n=5):
    ws = W()
    return [i for _, i in sorted((v["ok"] / v["n"], i) for i, v in S.nest.items()
                                 if v["n"] >= 2 and i in ws and v["ok"] / v["n"] < .75)][:n]


def new_entry():
    return dict(box=0, due=today.isoformat(), ok=0, n=0, ms=0)


TEST_MODES = ("placement", "pretest", "posttest")
LEAGUES = [("Bronz", 0, "🥉"), ("Gümüş", 100, "🥈"), ("Altın", 250, "🥇"), ("Elmas", 500, "💎")]


def weekly_xp():
    start = today - timedelta(today.weekday())
    return sum(S.hist.get((start + timedelta(i)).isoformat(), {}).get("xp", 0) for i in range(7))


def league(x=None):
    x = weekly_xp() if x is None else x
    return max((lg for lg in LEAGUES if x >= lg[1]), key=lambda lg: lg[1])


def test_ids():
    return [u["words"][(i * 2 + 1) % 6]["id"] for g in GRADES.values() for i, u in enumerate(g["units"])]


def get_test(kind):
    xs = [t for t in S.tests if t.get("kind") == kind]
    return (xs[0] if kind == "pre" else xs[-1]) if xs else None


def tpct(t):
    return int(round(t["score"] / t["total"] * 100)) if t and t.get("total") else 0


# ------------------------------------------------------------------
# SES (gTTS) ve KONUŞMA  (aksan seçimi + paralel üretim + hata önbelleği)
# ------------------------------------------------------------------
@st.cache_resource
def _audio_store():
    return {}


def _tld():
    return "co.uk" if S.accent == "uk" else "com"


def _gen(d, tld, t):
    k, f = f"{tld}|{t}", d.setdefault("__f", {})
    if k in d or time.time() - f.get(k, 0) < 120:
        return
    try:
        from gtts import gTTS
        b = io.BytesIO()
        gTTS(t, lang="en", tld=tld).write_to_fp(b)
        d[k] = base64.b64encode(b.getvalue()).decode()
    except Exception:
        f[k] = time.time()


def mp3_many(texts):
    d, tld = _audio_store(), _tld()
    todo = [t for t in set(texts) if f"{tld}|{t}" not in d]
    if todo:
        with ThreadPoolExecutor(6) as ex:
            list(ex.map(lambda t: _gen(d, tld, t), todo))


def player_js(items):
    mp3_many(list(items.values()))
    d, tld = _audio_store(), _tld()
    a = {k: d.get(f"{tld}|{t}", "") for k, t in items.items()}
    lang = "en-GB" if S.accent == "uk" else "en-US"
    dump = lambda o: json.dumps(o).replace("</", "<\\/")
    return (f"const A={dump(a)},T={dump(items)};"
            "function play(k){speechSynthesis.cancel();if(A[k]){new Audio('data:audio/mpeg;base64,'+A[k]).play();}"
            f"else{{const u=new SpeechSynthesisUtterance(T[k]);u.lang='{lang}';u.rate=.85;speechSynthesis.speak(u);}}}}")


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
    # onclick içindeki JSON tırnakları HTML-kaçışlı olmalı (&quot;), yoksa özellik bozulur
    rows = "".join(f'<div class="r">{pic(w["e"], 44)}<b>{esc(w["en"])}</b>'
                   f'<button onclick="listen({i},{esc(json.dumps(w["en"]))})">Söyle</button><span id="r{i}"></span></div>'
                   for i, w in enumerate(words))
    lang = "en-GB" if S.accent == "uk" else "en-US"
    components.html(
        f"""<style>body{{margin:0;font-family:'Baloo 2',Arial}}.r{{display:flex;align-items:center;gap:10px;background:#fff;border-radius:20px;padding:8px 12px;margin:6px 0;
        box-shadow:0 2px 10px rgba(31,42,68,.12)}}.r b{{flex:1;font-size:20px;color:#1F2A44}}button{{background:#FF5C8A;color:#fff;border:0;border-radius:999px;padding:6px 16px;
        font:700 15px 'Baloo 2';cursor:pointer}}span{{font-size:13px;font-weight:700;min-width:90px}}</style>{rows}
        <script>function listen(i,t){{const R=window.SpeechRecognition||window.webkitSpeechRecognition,el=document.getElementById('r'+i);
        if(!R){{el.textContent='Bu tarayıcı desteklemiyor';return}}const r=new R();r.lang='{lang}';el.textContent='Dinliyorum...';
        r.onresult=e=>{{const s=e.results[0][0].transcript.toLowerCase().trim(),ok=s.includes(t.toLowerCase());
        el.textContent=ok?'Harika! ✔':'Duydum: '+s;el.style.color=ok?'#0E7C6F':'#C42B58'}};
        r.onerror=()=>{{el.textContent='Mikrofon izni ver'}};r.start()}}</script>""", height=len(words) * 66 + 10)


# ------------------------------------------------------------------
# YAPAY ZEKÂ (isteğe bağlı: ANTHROPIC_API_KEY varsa) + günlük sınır
# ------------------------------------------------------------------
def api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY")


def ai_ready():
    if S.ai_day != today.isoformat():
        S.ai_day, S.ai_n = today.isoformat(), 0
    return bool(api_key()) and S.ai_n < AI_LIMIT


def ask_ai(content, system, max_tokens=500, msgs=None):
    import anthropic
    try:
        model = st.secrets["ANTHROPIC_MODEL"]
    except Exception:
        model = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")
    S.ai_n += 1
    r = anthropic.Anthropic(api_key=api_key()).messages.create(
        model=model, max_tokens=max_tokens, system=system, messages=msgs or [{"role": "user", "content": content}])
    return r.content[0].text.strip()


def make_story(words):
    en = [w["en"].lower() for w in words]
    S.stories += 1
    if ai_ready():
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


CHAT_SYS = ("You are Civi, a friendly baby chick who helps a Turkish child (age 6-9) practice English. Rules: reply with 1-2 very short, simple A1 English "
            "sentences, add a tiny Turkish hint in parentheses only if needed, and always end with one simple question. Be warm, playful and encouraging. "
            "Prefer these words the child knows: {words}. Never ask for or accept personal information (real name, address, school, phone, photos). "
            "If the child shares personal info or raises unsafe, scary or adult topics, gently steer to animals, food, colors or toys. "
            "If the child writes Turkish, answer in simple English and give the Turkish meaning.")


def chat_reply():
    ws = W()
    known = ", ".join(ws[i]["en"].lower() for i in list(S.nest)[:25] if i in ws) or "cat, dog, apple, red"
    msgs = [dict(m) for m in S.chat[-8:]]
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    return ask_ai(None, CHAT_SYS.format(words=known), 150, msgs=msgs)


def check_sentence(word, sent):
    if not ai_ready():
        ok = word.lower() in sent.lower()
        return dict(ok=ok, fixed=sent, tip="Kelimeyi cümlede kullandın!" if ok else f"Cümlende '{word}' kelimesi geçmeli.")
    try:
        txt = ask_ai(f'Target word: "{word}". Child sentence: "{sent}"',
                     "You are a kind English teacher for a 7-year-old Turkish child (A1). Reply ONLY JSON: "
                     '{"ok":true,"fixed":"corrected simple sentence","tip_tr":"one short friendly Turkish tip"}. '
                     "ok is true only if the sentence uses the target word and is correct English.", 200)
        d = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
        return dict(ok=bool(d.get("ok")), fixed=str(d.get("fixed", sent))[:160], tip=str(d.get("tip_tr", ""))[:200])
    except Exception:
        return None


# ------------------------------------------------------------------
# OYUN MANTIĞI
# ------------------------------------------------------------------
def distractors(w, pool, n):
    seen, out = {w["en"].lower()}, []
    for x in random.sample(pool, min(len(pool), 20)):
        if x["en"].lower() not in seen and len(out) < n:
            seen.add(x["en"].lower())
            out.append(x)
    return out


def build_session(wids, sents, mode):
    ws, pool = W(), list(W().values())
    qs = []
    for wid in wids:
        w = ws[wid]
        for k in (("see",) if mode in TEST_MODES else ("see", "hear")):
            o = [w] + distractors(w, pool, 3)
            random.shuffle(o)
            qs.append(dict(k=k, w=w, opts=o))
    random.shuffle(qs)
    if mode not in TEST_MODES:
        spell = [i for i in wids if " " not in ws[i]["en"] and len(ws[i]["en"]) <= 8]
        random.shuffle(spell)
        qs += [dict(k="spell", w=ws[i]) for i in spell[:2]]
        fills = [i for i in wids if re.search(r"\b" + re.escape(ws[i]["en"]) + r"\b", ws[i]["s"], re.I)]
        random.shuffle(fills)
        for i in fills[:2]:
            w = ws[i]
            o = [w] + distractors(w, pool, 2)
            random.shuffle(o)
            qs.append(dict(k="fill", w=w, opts=o, blank=re.sub(r"\b" + re.escape(w["en"]) + r"\b", "____", w["s"], count=1, flags=re.I)))
        dic = [i for i in wids if " " not in ws[i]["en"]]
        random.shuffle(dic)
        qs += [dict(k="dict", w=ws[i]) for i in dic[:1]]
        qs += [dict(k="sent", s=s) for s in sents]
    go(screen="play", phase="quiz", qs=qs, qi=0, score=0, picked=None, built=[], pool=[], checked=False,
       sfx=False, wids=wids, bad=[], mode=mode, qt=0, sess=dict(xp=0, seeds=0, t=[]), pl={})


def start_review():
    ids = due_ids()
    random.shuffle(ids)
    build_session(ids[:6], [], "review")


def start_weak():
    build_session(hard_ids(6), [], "weak")


def start_placement():
    wids = []
    for g in "kab":
        wids += random.sample([i for i in BASE_WORDS if i[0] == g], 4)
    build_session(wids, [], "placement")
    S.pl = {}


def start_test(kind):
    ids = test_ids()
    random.shuffle(ids)
    build_session(ids, [], kind + "test")


def start_unit(unit):
    go(screen="play", phase="learn", unit=unit)


def add_to_nest():
    u, new = S.unit, 0
    for w in u["words"]:
        if w["id"] not in S.nest:
            S.nest[w["id"]] = new_entry()
            new += 1
    hbump("new", new)
    build_session([w["id"] for w in u["words"]], u["sents"], "unit")


def add_word(wid):
    if wid not in S.nest and wid in W():
        S.nest[wid] = new_entry()
        hbump("new")
        st.toast("Yuvana yumurta olarak eklendi")


def add_custom():
    en, tr = S.cw_en.strip(), S.cw_tr.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]{0,19}", en) or not tr or len(tr) > 30:
        st.toast("İngilizce kelime sadece harf içermeli, Türkçesini de yaz.")
        return
    if len(S.custom) >= 100:
        st.toast("En fazla 100 özel kelime ekleyebilirsin.")
        return
    wid = f"c{len(S.custom)}"
    S.custom.append(dict(id=wid, en=en.capitalize(), tr=esc(tr), e=clean_emoji(S.cw_e), s=f"This is {art(en)} {en.lower()}.", u="custom"))
    S.nest[wid] = new_entry()
    hbump("new")
    S.cw_en, S.cw_tr, S.cw_e = "", "", ""
    st.toast("Kendi kelimen yuvaya eklendi")


def gain(xp=0, seeds=0):
    L0 = level()[0]
    S.xp += xp
    S.seeds += seeds
    S.sess["xp"] += xp
    S.sess["seeds"] += seeds
    if xp:
        hbump("xp", xp)
    if level()[0] > L0:
        st.toast(f"Seviye atladın! Seviye {level()[0]}")


def award(ok, wid=None):
    test = S.mode in TEST_MODES
    S.ok, S.sfx = ok, not test
    S.score += int(ok)
    dt = time.time() - S.qt if S.qt else None
    S.qt = 0
    if test:
        if wid:
            r = S.pl.setdefault(wid[0], [0, 0])
            r[0] += int(ok)
            r[1] += 1
            if not ok and wid not in S.bad:
                S.bad.append(wid)
        if dt is not None and 0 < dt < 120:
            S.sess.setdefault("t", []).append(dt)
        return
    if ok:
        gain(10, 1)
    if wid:
        if not ok and wid not in S.bad:
            S.bad.append(wid)
        if wid in S.nest:
            v = S.nest[wid]
            v["n"] += 1
            v["ok"] += int(ok)
            if dt is not None and 0 < dt < 60:
                v["ms"] = int(.7 * v["ms"] + .3 * dt * 1000) if v.get("ms") else int(dt * 1000)
    hbump("n")
    hbump("ok", int(ok))


def choose(opt_id, correct_id):
    S.picked = opt_id
    award(opt_id == correct_id, correct_id)
    if S.mode in TEST_MODES:
        next_q()


def pick_word(i):
    S.built.append(S.pool.pop(i))


def check_builder(toks, sep, wid):
    S.checked = True
    award(sep.join(S.built).lower() == sep.join(toks).lower(), wid)


def check_dict(key, w):
    S.checked = True
    norm = lambda s: re.sub(r"[^a-z ]", "", (s or "").lower()).strip()
    award(norm(S.get(key)) == norm(w["en"]), w["id"])


def reset_pool(toks):
    S.pool, S.built = random.sample(toks, len(toks)), []


def next_q():
    S.qi += 1
    S.picked, S.checked, S.built, S.pool, S.sfx, S.qt = None, False, [], [], False, 0
    if S.qi >= len(S.qs):
        moves = []
        for wid in S.wids:
            v = S.nest.get(wid)
            if not v or S.mode in TEST_MODES:
                continue
            old = v["box"]
            slow = old > 0 and v.get("ms", 0) > 7000  # doğru ama yavaş: kutu yükselmez, kelime biraz daha pekişir
            v["box"] = max(0, old - 1) if wid in S.bad else old if slow else min(4, old + 1)
            v["due"] = (today + timedelta(INTERVALS[v["box"]])).isoformat()
            moves.append((wid, old, v["box"]))
        if S.mode == "review":
            hbump("rev")
        if S.mode == "placement":
            rec = "2. Sınıf"
            for g in "kab":
                if g in S.pl and S.pl[g][0] / S.pl[g][1] < .75:
                    rec = GRADE_NAMES[g]
                    break
            S.placed = rec
        elif S.mode in TEST_MODES:
            ts = S.sess.get("t", [])
            S.tests.append(dict(kind="pre" if S.mode == "pretest" else "post", date=today.isoformat(), score=S.score, total=len(S.qs),
                                by={g: list(v) for g, v in S.pl.items()}, ms=int(sum(ts) / len(ts) * 1000) if ts else 0))
        else:
            perfect = S.score == len(S.qs)
            S.perfect += int(perfect)
            gain(20, 5 + (10 if perfect else 0))
        S.res = dict(moves=moves)
        S.phase = "result"


# ---- Eşleştirme ----
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
                gain(20, 5)


# ---- Kuş Kurtar (adam asmaca) ----
def start_hm():
    ws = W()
    ok = lambda w: re.fullmatch(r"[A-Za-z]{3,9}", w["en"])
    pool = [w for w in (ws[i] for i in S.nest if i in ws) if ok(w)] or [w for w in ws.values() if ok(w)]
    S.hm = dict(id=random.choice(pool)["id"], g=[], lives=6, done=False, won=False, b=False)


def guess_hm(c):
    h = S.hm
    if h["done"] or c in h["g"]:
        return
    h["g"].append(c)
    word = W()[h["id"]]["en"].lower()
    if c not in word:
        h["lives"] -= 1
    if all(x in h["g"] for x in word):
        h["done"] = h["won"] = True
        S.hm_wins += 1
        gain(15, 3)
    elif h["lives"] <= 0:
        h["done"] = True


# ---- Günlük sandık & mağaza ----
def open_chest():
    S.chest_day = today.isoformat()
    n = random.choice([5, 8, 10, 15, 25])
    S.seeds += n
    st.toast(f"Sandıktan {n} tohum çıktı!")


def buy(i):
    _, price, slot = SHOP[i]
    if S.seeds >= price and i not in S.owned:
        S.seeds -= price
        S.owned.append(i)
        S.eq[slot] = i


def equip(i):
    slot = SHOP[i][2]
    S.eq[slot] = None if S.eq.get(slot) == i else i


def grade_of(wid):
    return wid[0]


def dlg_opts(d, step):
    t = d["turns"][step]
    o = [t[2]] + list(t[4])
    random.shuffle(o)
    return o


def start_dlg(did):
    S.dlg = dict(id=did, step=0, picked=None, right=0, opts=dlg_opts(DLG_BY_ID[did], 0), done=False, bonus=0)


def pick_dlg(i):
    g = S.dlg
    t = DLG_BY_ID[g["id"]]["turns"][g["step"]]
    g["picked"] = i
    ok = g["opts"][i] == t[2]
    g["right"] += int(ok)
    S.ok, S.sfx = ok, True
    if ok:
        gain(5, 1)


def next_dlg():
    g = S.dlg
    d = DLG_BY_ID[g["id"]]
    g["step"] += 1
    g["picked"] = None
    if g["step"] >= len(d["turns"]):
        g["done"] = True
        g["bonus"] = 5 if g["right"] == len(d["turns"]) else 0
        gain(15, 3 + g["bonus"])
        if g["id"] not in S.dlg_done:
            S.dlg_done.append(g["id"])
    else:
        g["opts"] = dlg_opts(d, g["step"])


def buy_freeze():
    if S.seeds >= 30 and S.freeze < 3:
        S.seeds -= 30
        S.freeze += 1


def parent_report():
    ws = W()
    nm = esc(S.name or S.user or "Öğrenci")
    tot = sum(v["n"] for v in S.nest.values())
    ok = sum(v["ok"] for v in S.nest.values())
    days = [today - timedelta(d) for d in range(6, -1, -1)]
    wn = sum(S.hist.get(d.isoformat(), {}).get("n", 0) for d in days)
    active = sum(1 for d in days if S.hist.get(d.isoformat(), {}).get("n"))
    rows = ""
    for i, v in sorted(S.nest.items()):
        w = ws.get(i)
        if w:
            acc = int(v["ok"] / v["n"] * 100) if v["n"] else 0
            rows += f"<tr><td>{esc(w['en'])}</td><td>{esc(w['tr'])}</td><td>{STAGES[v['box']][0]}</td><td>%{acc}</td></tr>"
    pre, post = get_test("pre"), get_test("post")
    tline = ""
    if pre:
        tline = f"<p>Ön test: <b>%{tpct(pre)}</b> ({esc(pre['date'])})"
        if post:
            tline += f" · Son test: <b>%{tpct(post)}</b> ({esc(post['date'])}) · Değişim: <b>{tpct(post) - tpct(pre):+d} puan</b>"
        tline += "</p>"
    hard = ", ".join(esc(ws[i]["en"]) for i in hard_ids(5) if i in ws) or "yok"
    css = ("body{font-family:Arial,sans-serif;max-width:720px;margin:24px auto;padding:0 16px;color:#1F2A44}h1{color:#FF5C8A}"
           "table{width:100%;border-collapse:collapse}td,th{border-bottom:1px solid #DCE5F5;padding:6px;text-align:left}"
           ".k{display:inline-block;background:#F0F6FF;border-radius:12px;padding:8px 14px;margin:4px 6px 4px 0}")
    return ("<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>LingoNest Veli Raporu</title><style>" + css + "</style></head><body>"
            f"<h1>LingoNest Veli Raporu</h1><p><b>{nm}</b> · {today.strftime('%d.%m.%Y')}</p>"
            f"<div class='k'>Yuvadaki kelime: <b>{len(S.nest)}</b></div><div class='k'>Usta kuş: <b>{mastered()}</b></div>"
            f"<div class='k'>Doğruluk: <b>%{int(ok / tot * 100) if tot else 0}</b></div><div class='k'>Seri: <b>{S.streak} gün</b></div>"
            f"<div class='k'>Seviye: <b>{level()[0]}</b></div><div class='k'>Bu hafta: <b>{wn} cevap, {active}/7 gün</b></div>"
            f"{tline}<p>Zorlandığı kelimeler: <b>{hard}</b></p><h3>Kelime listesi</h3>"
            f"<table><tr><th>İngilizce</th><th>Türkçe</th><th>Aşama</th><th>Doğruluk</th></tr>{rows}</table>"
            "<h3>Evde nasıl destek olabilirsiniz?</h3><ul><li>Günde 10 dakika düzenli çalışma, haftada bir uzun çalışmadan daha etkilidir.</li>"
            "<li>Çocuğunuza öğrendiği kelimeyi evde bulup göstermesini söyleyin.</li><li>Hata yaptığında düzeltmek yerine doğrusunu birlikte tekrar edin.</li>"
            "<li>Ekran başında 20 dakikadan sonra mola verdirin.</li></ul></body></html>")


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
    ("Kurtarıcı", "🛟", "Kuş Kurtar'ı kazan", lambda: S.hm_wins >= 1),
    ("Sohbetçi", "💬", "Civi ile 5 kez konuş", lambda: S.chats >= 5),
    ("Alışverişçi", "🛍️", "Mağazadan bir şey al", lambda: len(S.owned) >= 1),
    ("Seviye 5", "⭐", "Seviye 5'e ulaş", lambda: level()[0] >= 5),
    ("Kâşif", "🗺️", "Seviye testini bitir", lambda: bool(S.placed)),
    ("Sahne yıldızı", "🎭", "Bir sahneyi bitir", lambda: len(S.dlg_done) >= 1),
    ("Bilim insanı", "🔬", "Ön testi tamamla", lambda: get_test("pre") is not None),
    ("İlerleyen", "📈", "Son testte ön testten yüksek al", lambda: bool(get_test("pre") and get_test("post") and tpct(get_test("post")) > tpct(get_test("pre")))),
    ("Hafta kahramanı", "🏆", "Bir haftada 250 XP", lambda: weekly_xp() >= 250),
]

# ------------------------------------------------------------------
# HESAP SİSTEMİ: yuva adı + PIN, Supabase (yoksa yerel dosya), sınıf kodu
# ------------------------------------------------------------------
PERSIST = ("nest", "custom", "hist", "streak", "last_day", "name", "color", "goal", "sound", "mm_wins", "stories", "perfect",
           "xp", "seeds", "owned", "eq", "accent", "chest_day", "hw", "placed", "ai_day", "ai_n", "hm_wins", "chats",
           "freeze", "tests", "big", "calm", "dys", "dlg_done")
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


@st.cache_data(ttl=60, show_spinner=False)
def class_rows(code, role):
    """Önbellekli sınıf listesi (PIN özeti gibi alanlar atılır)."""
    try:
        return [dict(username=r["username"], summary=r.get("summary") or {}) for r in db_class(code, role)]
    except Exception:
        return []


def summary():
    tot, ok = sum(v["n"] for v in S.nest.values()), sum(v["ok"] for v in S.nest.values())
    d = dict(words=len(S.nest), mastered=mastered(), acc=int(ok / tot * 100) if tot else 0, streak=S.streak, last=today.isoformat(),
             xp=S.xp, hard=hard_ids(5), wxp=weekly_xp(),
             pre=tpct(get_test("pre")) if get_test("pre") else None, post=tpct(get_test("post")) if get_test("post") else None)
    if S.role == "teacher":
        d["hw"] = S.hw
    return d


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
    for v in S.nest.values():
        v.setdefault("ms", 0)
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
        if (row.get("locked_until") or "") > utcnow().isoformat():
            return "Çok fazla yanlış deneme. 5 dakika sonra tekrar dene."
        if row["pin_hash"] != hpin(u, pin):
            f = (row.get("fails") or 0) + 1
            db_patch(u, dict(fails=0, locked_until=(utcnow() + timedelta(minutes=5)).isoformat()) if f >= 5 else dict(fails=f))
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
        <span class="ch">{tw('🔥', 20)}{S.streak}</span><span class="ch">{tw('🌰', 20)}{S.seeds}</span>
        <span class="ch rk">{r[0]}</span></div></div>""", unsafe_allow_html=True)
    items = [("nest", "Yuva", ":material/home:"), ("explore", "Keşfet", ":material/explore:"),
             ("adv", "Macera", ":material/auto_awesome:"), ("panel", "Panel", ":material/bar_chart:")]
    if S.role == "teacher":
        items.append(("class", "Sınıf", ":material/groups:"))
    cols = st.columns(len(items))
    for c, (k, lab, ic) in zip(cols, items):
        c.button(lab, key=f"n_{k}", icon=ic, use_container_width=True, type="primary" if S.screen == k else "secondary",
                 on_click=go, kwargs={"screen": k})
    if time.time() - S.t0 > 20 * 60:
        st.markdown('<div class="card on"><div class="t">Mola zamanı!</div><small>20 dakikadır çalışıyorsun. Su iç, gözlerini dinlendir.</small></div>',
                    unsafe_allow_html=True)
        st.button("Dinlendim, devam", key="brk", use_container_width=True, on_click=lambda: S.__setitem__("t0", time.time()))


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
        gain(0, 10)
        st.balloons()
        st.toast("Bugünkü üç görev tamam! +10 tohum")
    L, lp, need = level()
    nm = esc(S.name) or "kaşif"
    st.markdown(f'<div class="hero"><span class="bob">{chick(64)}</span><div><h2>Merhaba {nm}!</h2>'
                f'<p>{S.streak} gündür yuvana bakıyorsun.</p></div></div>'
                f'<div class="lvl"><b>Seviye {L}</b><div class="bar"><div style="width:{lp}%"></div></div><small>{need} XP</small></div>', unsafe_allow_html=True)
    lg = league()
    st.markdown(f'<div class="hint" style="margin-top:-4px">{tw(lg[2], 18)} {lg[0]} ligi · bu hafta {weekly_xp()} XP'
                f'{" · " + str(S.freeze) + " seri koruyucu" if S.freeze else ""}</div>', unsafe_allow_html=True)
    st.markdown(nest_svg([v["box"] for v in S.nest.values()], S.night), unsafe_allow_html=True)
    nxt_d = next(((t, n) for t, n in DECOS if len(S.nest) < t), None)
    st.markdown(f'<div class="hint">{f"{nxt_d[0] - len(S.nest)} kelime sonra yeni süs: {nxt_d[1]}" if nxt_d else "Yuvan tüm süslerle donandı"}</div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    b1.button("Gündüze geç" if S.night else "Geceye geç", icon=":material/light_mode:" if S.night else ":material/dark_mode:",
              use_container_width=True, on_click=lambda: S.__setitem__("night", not S.night))
    b2.button("Sandık açıldı" if S.chest_day == today.isoformat() else "Günlük sandık", icon=":material/redeem:",
              use_container_width=True, disabled=S.chest_day == today.isoformat(), on_click=open_chest)
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
        hid = hard_ids(6)
        if hid:
            st.button(f"Zor kelimeleri çalış · {len(hid)} kelime", icon=":material/fitness_center:", use_container_width=True, on_click=start_weak)
    if S.placed:
        st.markdown(f'<div class="hint">Seviye testi önerisi: {esc(S.placed)} ile başla</div>', unsafe_allow_html=True)

    # --- Öğretmenin ödevi (öğrenciler için) ---
    if S.role == "student" and S.class_code:
        t = class_rows(S.class_code, "teacher")
        hw = [i for i in ((t[0]["summary"].get("hw") if t else None) or []) if i in UNIT_BY_ID]
        if hw:
            st.markdown("<h3 style='margin-top:14px'>Öğretmenin ödevi</h3>", unsafe_allow_html=True)
            for uid in hw:
                u = UNIT_BY_ID[uid]
                have = sum(1 for w in u["words"] if w["id"] in S.nest)
                c1, c2 = st.columns([3, 2])
                c1.markdown(f'<div class="row">{tw(u["ic"], 26)}<span style="flex:1">{u["title"]}</span><small>{have}/{len(u["words"])}</small></div>', unsafe_allow_html=True)
                c2.button("Tamam" if have == len(u["words"]) else "Çalış", key=f"hw_{uid}", use_container_width=True,
                          type="secondary" if have == len(u["words"]) else "primary", on_click=start_unit, args=(u,))
        studs = class_rows(S.class_code, "student")
        if studs:
            with st.expander("Bu haftanın sıralaması"):
                top = sorted(studs, key=lambda r_: -r_["summary"].get("wxp", 0))[:5]
                st.markdown("".join(
                    f'<div class="row"><b>{i + 1}.</b><span style="flex:1">{esc(r_["username"])}{" (sen)" if r_["username"] == S.user else ""}</span>'
                    f'<small>{league(r_["summary"].get("wxp", 0))[2]} {r_["summary"].get("wxp", 0)} XP</small></div>' for i, r_ in enumerate(top)), unsafe_allow_html=True)

    wd = list(BASE_WORDS.values())[today.toordinal() % len(BASE_WORDS)]
    st.markdown(f'<h3 style="margin-top:18px">Günün kelimesi</h3><div class="card"><div class="art" style="margin:0 0 8px">{pic(wd["e"], 96)}</div>'
                f'<div class="t">{wd["en"]} = {wd["tr"]}</div><small>{wd["s"]}</small></div>', unsafe_allow_html=True)
    speak_html(wd["s"], label="Cümleyi dinle")

elif S.screen == "explore":
    head()
    if not S.placed:
        st.markdown('<div class="card"><div class="t">Nereden başlamalıyım?</div><small>12 soruluk kısa testle seviyeni bul</small></div>', unsafe_allow_html=True)
        st.button("Seviye testine başla", type="primary", use_container_width=True, icon=":material/quiz:", on_click=start_placement)
    else:
        st.markdown(f'<div class="card on"><div class="t">Önerilen başlangıç: {esc(S.placed)}</div></div>', unsafe_allow_html=True)
        st.button("Testi tekrarla", use_container_width=True, icon=":material/quiz:", on_click=start_placement)
    q = st.text_input("Kelime ara", key="srch", placeholder="İngilizce veya Türkçe kelime ara", label_visibility="collapsed").strip().lower()
    if q:
        hits = [w for w in W().values() if q in w["en"].lower() or q in w["tr"].lower()][:8]
        if not hits:
            st.caption("Bu kelimeyi bulamadım. Aşağıdan kendi kelimeni ekleyebilirsin.")
        for w in hits:
            c1, c2 = st.columns([4, 2])
            c1.markdown(f'<div class="row">{pic(w["e"], 30)}<span style="flex:1">{w["en"]} · {w["tr"]}</span></div>', unsafe_allow_html=True)
            c2.button("Yuvada" if w["id"] in S.nest else "Ekle", key=f"sr_{w['id']}", use_container_width=True, disabled=w["id"] in S.nest,
                      on_click=add_word, args=(w["id"],))
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
    with st.expander("Kendi kelimemi ekle"):
        st.text_input("İngilizce (harflerle)", key="cw_en", max_chars=20)
        st.text_input("Türkçesi", key="cw_tr", max_chars=30)
        st.text_input("Emoji (isteğe bağlı)", key="cw_e", max_chars=8)
        st.button("Yuvama ekle", type="primary", use_container_width=True, on_click=add_custom)

elif S.screen == "adv":
    head()
    nest_words = [W()[i] for i in S.nest if i in W()]
    if S.act:
        st.button("Geri", icon=":material/arrow_back:", on_click=go, kwargs={"act": None})
    if S.act is None:
        cols = st.columns(2)
        for i, (k_, nm_, em, sub) in enumerate(ACTS):
            with cols[i % 2]:
                st.markdown(f'<div class="card">{tw(em, 44)}<div class="t">{nm_}</div><small>{sub}</small></div>', unsafe_allow_html=True)
                st.button("Aç", key=f"act_{k_}", type="primary", use_container_width=True, on_click=go, kwargs={"act": k_})
    elif S.act == "dlg":
        g = S.dlg
        if not g:
            st.caption("Civi ile kısa konuşmalar yap. Her sahnede 3 cevap seçeceksin.")
            for d in DIALOGS:
                c1, c2 = st.columns([3, 2])
                c1.markdown(f'<div class="row">{tw(d["ic"], 26)}<span style="flex:1">{d["title"]}</span>'
                            f'<small>{"✔" if d["id"] in S.dlg_done else ""}</small></div>', unsafe_allow_html=True)
                c2.button("Başla", key=f"dl_{d['id']}", use_container_width=True, type="primary", on_click=start_dlg, args=(d["id"],))
        else:
            d = DLG_BY_ID[g["id"]]
            if g["done"]:
                if g["right"] == len(d["turns"]):
                    st.balloons()
                st.markdown(f'<div class="big"><span class="bob">{chick(100)}</span><h1>Sahne bitti!</h1>'
                            f'<p style="font-weight:700">{g["right"]}/{len(d["turns"])} doğru · +15 XP{" · +5 bonus tohum" if g["bonus"] else ""}</p></div>',
                            unsafe_allow_html=True)
                st.button("Başka sahne seç", type="primary", use_container_width=True, on_click=lambda: S.__setitem__("dlg", None))
            else:
                st.markdown(f"<h3>{tw(d['ic'], 28)} {d['title']} · {g['step'] + 1}/{len(d['turns'])}</h3>", unsafe_allow_html=True)
                hist = "".join(f'<div class="bub bot">{esc(t[0])}</div><div class="bub me">{esc(t[2])}</div>' for t in d["turns"][:g["step"]])
                t = d["turns"][g["step"]]
                st.markdown(f'{hist}<div class="bub bot">{esc(t[0])}<br><small style="color:#5B6A8A">{esc(t[1])}</small></div>', unsafe_allow_html=True)
                speak_html(t[0], auto=g["picked"] is None, label="Dinle")
                if g["picked"] is None:
                    for i, o in enumerate(g["opts"]):
                        st.button(o, key=f"dlo{g['step']}_{i}", use_container_width=True, on_click=pick_dlg, args=(i,))
                else:
                    sfx(S.ok)
                    for i, o in enumerate(g["opts"]):
                        cls = "right" if o == t[2] else "wrong" if i == g["picked"] else "dim"
                        st.markdown(f"<div class='opt {cls}'>{esc(o)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='sheet {'ok' if S.ok else 'no'}'>{chick(52, not S.ok)}<div><b>{'Harika!' if S.ok else 'Doğrusu:'}</b>"
                                f"<br><span>{esc(t[2])} = {esc(t[3])}</span></div></div>", unsafe_allow_html=True)
                    st.button("Devam", type="primary", use_container_width=True, on_click=next_dlg)
    elif S.act == "mm":
        st.button("Yeni oyun" if S.mm else "Oyuna başla", key="mm_start", type="primary", use_container_width=True, on_click=start_mm)
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
                st.success(f"Hepsini buldun! {m['tries']} hamlede bitirdin. +20 XP, +5 tohum")
    elif S.act == "hm":
        st.caption("Harfleri tahmin et, kuşu kurtar. 6 canın var.")
        st.button("Yeni kelime" if S.hm else "Oyuna başla", key="hm_start", type="primary", use_container_width=True, on_click=start_hm)
        h = S.hm
        if h:
            w = W()[h["id"]]
            word = w["en"].lower()
            shown = "".join(f'<span class="w" style="min-width:26px;text-align:center">{c.upper() if c in h["g"] or h["done"] else "_"}</span>' for c in word)
            st.markdown(f'<div class="art">{chick(80, sad=h["lives"] <= 2)}<h3 style="margin:4px 0">{w["tr"]}</h3>'
                        f'<div class="built" style="justify-content:center;border:0;margin:0">{shown}</div>'
                        f'<div>{"❤️" * h["lives"]}{"🖤" * (6 - h["lives"])}</div></div>', unsafe_allow_html=True)
            cols = st.columns(7)
            for i, c in enumerate(string.ascii_lowercase):
                cols[i % 7].button(c.upper(), key=f"hm_{c}", use_container_width=True, disabled=h["done"] or c in h["g"],
                                   on_click=guess_hm, args=(c,))
            if h["done"]:
                if h["won"]:
                    if not h["b"]:
                        h["b"] = True
                        st.balloons()
                    st.success("Kuşu kurtardın! +15 XP, +3 tohum")
                else:
                    st.error(f"Bu sefer olmadı. Kelime: {w['en']}")
                speak_html(w["en"])
    elif S.act == "story":
        if len(nest_words) < 3:
            st.info("Hikâye için yuvaya en az 3 kelime topla.")
        else:
            st.button("Yuvamdan hikâye yaz", type="primary", use_container_width=True,
                      on_click=lambda: S.__setitem__("story", make_story(random.sample(nest_words, min(5, len(nest_words))))))
            if S.story:
                st.markdown(f'<div class="card" style="text-align:left;font-size:18px">{esc(S.story)}</div>', unsafe_allow_html=True)
                speak_html(S.story, label="Hikâyeyi dinle")
    elif S.act == "hunt":
        if not api_key():
            st.info("Kelime avı için yapay zekâ anahtarı gerekir (ANTHROPIC_API_KEY). Öğretmen ayarlardan ekleyebilir.")
        elif not ai_ready():
            st.info("Bugünlük yapay zekâ hakkın doldu, yarın tekrar gel.")
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
                    en = (res.get("en") or "").strip()
                    if re.fullmatch(r"[A-Za-z][A-Za-z '\-]{0,19}", en) and len(S.custom) < 100:
                        wid = f"c{len(S.custom)}"
                        w = dict(id=wid, en=en.capitalize(), tr=esc(str(res.get("tr", ""))[:30]), s=f"This is {art(en)} {en.lower()}.",
                                 e="data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), u="custom")
                        S.custom.append(w)
                        S.nest[wid] = new_entry()
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
    elif S.act == "speak":
        pool = nest_words[:6] if nest_words else list(BASE_WORDS.values())[:6]
        st.caption("Söyle düğmesine bas ve kelimeyi yüksek sesle söyle.")
        speaking(pool)
    elif S.act == "civi":
        if not api_key():
            st.info("Civi ile konuşmak için yapay zekâ anahtarı gerekir (ANTHROPIC_API_KEY).")
        elif not ai_ready():
            st.info("Bugünlük yapay zekâ hakkın doldu, yarın tekrar gel.")
        else:
            mode = st.radio("Mod", ["Civi ile sohbet", "Cümle atölyesi"], horizontal=True, label_visibility="collapsed", key="ch_mode")
            if mode == "Civi ile sohbet":
                bubs = "".join(f'<div class="bub {"me" if m["role"] == "user" else "bot"}">{esc(m["content"])}</div>' for m in S.chat[-8:])
                st.markdown(bubs or '<div class="hint">Civi\'ye "Hello!" yaz. Gerçek adını veya adresini yazma.</div>', unsafe_allow_html=True)
                if S.chat and S.chat[-1]["role"] == "assistant":
                    speak_html(re.sub(r"\([^)]*\)", "", S.chat[-1]["content"]), label="Dinle")
                with st.form("chatf", clear_on_submit=True):
                    msg = st.text_input("Mesaj", max_chars=120, label_visibility="collapsed", placeholder="İngilizce yaz...")
                    sent = st.form_submit_button("Gönder", type="primary", use_container_width=True)
                if sent and msg.strip():
                    S.chat.append(dict(role="user", content=msg.strip()))
                    try:
                        S.chat.append(dict(role="assistant", content=chat_reply()))
                        S.chats += 1
                        gain(5, 0)
                        st.rerun()
                    except Exception as ex:
                        S.chat.pop()
                        st.warning(f"Civi şu an cevap veremedi ({type(ex).__name__}). Biraz sonra dene.")
                if S.chat:
                    st.button("Sohbeti temizle", icon=":material/delete:", use_container_width=True, on_click=lambda: S.__setitem__("chat", []))
            else:
                words = sorted({w["en"] for w in nest_words}) or ["Cat"]
                target = st.selectbox("Bir kelime seç", words, key="fx_w")
                text = st.text_input("Bu kelimeyle bir cümle yaz", max_chars=100, key="fx_s", placeholder="I see a cat.")
                if st.button("Kontrol et", type="primary", use_container_width=True, disabled=not text.strip()):
                    r_ = check_sentence(target, text.strip())
                    if r_ is None:
                        st.warning("Kontrol edilemedi, tekrar dene.")
                    else:
                        S.fix = r_
                        S.chats += 1
                        if r_["ok"]:
                            gain(10, 2)
                if S.fix:
                    f = S.fix
                    st.markdown(f'<div class="fixed">{"Harika cümle!" if f["ok"] else "Neredeyse!"}<br><span>{esc(f["fixed"])}</span><br><small>{esc(f["tip"])}</small></div>',
                                unsafe_allow_html=True)
                    speak_html(f["fixed"], label="Düzeltilmiş cümleyi dinle")

elif S.screen == "panel":
    head()
    p1, p4, p6, p2, p5, p3 = st.tabs(["Gelişim", "Analiz", "Test", "Rozet", "Mağaza", "Ayar"])
    with p1:
        days = [today - timedelta(d) for d in range(6, -1, -1)]
        H = [S.hist.get(d.isoformat(), {}) for d in days]
        vals = [h.get("n", 0) for h in H]
        mx = max(vals + [1])
        bars = "".join(f'<div class="cc {"t" if d == today else ""}"><em>{v or ""}</em><i style="height:{max(4, int(v / mx * 110))}px"></i>'
                       f'<span>{DAYS[d.weekday()]}</span></div>' for d, v in zip(days, vals))
        ok, n = sum(h.get("ok", 0) for h in H), sum(vals)
        dots = "".join(f'<i class="{"on" if S.hist.get((today - timedelta(d)).isoformat(), {}).get("n") else ""}"></i>' for d in range(13, -1, -1))
        st.markdown(f"""<div class="grid"><div class="tile"><b>{vals[-1]}</b><span>Bugün cevap</span></div><div class="tile"><b>{n}</b><span>Haftalık cevap</span></div>
            <div class="tile"><b>%{int(ok / n * 100) if n else 0}</b><span>Haftalık doğruluk</span></div>
            <div class="tile"><b>{mastered()}/{len(S.nest)}</b><span>Usta kuş / yuvadaki</span></div>
            <div class="tile"><b>{S.xp}</b><span>Toplam XP · Seviye {level()[0]}</span></div>
            <div class="tile"><b>{S.seeds}</b><span>Tohum</span></div></div>
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
        cw.writerow(["kelime", "turkce", "unite", "kutu", "dogru", "toplam", "ort_tepki_ms", "sonraki_bakim"])
        for i, v in S.nest.items():
            if i in W():
                w = W()[i]
                cw.writerow([w["en"], w["tr"], w.get("u", ""), v["box"], v["ok"], v["n"], v.get("ms", 0), v["due"]])
        st.download_button("Rapor (CSV)", buf.getvalue(), "lingonest_rapor.csv", use_container_width=True, icon=":material/download:")
        st.download_button("Veli raporu (HTML)", parent_report(), "lingonest_veli_raporu.html", mime="text/html", use_container_width=True,
                           icon=":material/description:")
    with p4:
        ents = [(i, v) for i, v in S.nest.items() if i in W()]
        ms = [v["ms"] for _, v in ents if v.get("ms")]
        late = sum(1 for _, v in ents if v["due"] < today.isoformat())
        tot_n, tot_ok = sum(v["n"] for _, v in ents), sum(v["ok"] for _, v in ents)
        st.markdown(f"""<div class="grid"><div class="tile"><b>{(sum(ms) / len(ms) / 1000):.1f} sn</b><span>Ortalama tepki süresi</span></div>
            <div class="tile"><b>%{int(tot_ok / tot_n * 100) if tot_n else 0}</b><span>Genel doğruluk</span></div>
            <div class="tile"><b>{late}</b><span>Bakımı geciken kelime</span></div>
            <div class="tile"><b>{S.hm_wins + S.mm_wins}</b><span>Kazanılan oyun</span></div></div>""" if ms else
                    '<div class="hint">Analiz için biraz soru çöz.</div>', unsafe_allow_html=True)
        if ents:
            st.markdown("<h3>Kutulara göre doğruluk</h3>", unsafe_allow_html=True)
            rows = ""
            for b, (nm_, em) in enumerate(STAGES):
                xs = [v for _, v in ents if v["box"] == b]
                nn, oo = sum(v["n"] for v in xs), sum(v["ok"] for v in xs)
                rows += f'<div class="row">{tw(em, 26)}<span>{nm_}</span><div class="bar"><div style="width:{int(oo / nn * 100) if nn else 0}%"></div></div><small>{len(xs)} kelime</small></div>'
            st.markdown(rows, unsafe_allow_html=True)
            st.markdown("<h3>Sınıf düzeyine göre doğruluk</h3>", unsafe_allow_html=True)
            rows = ""
            for g, gn in GRADE_NAMES.items():
                xs = [v for i, v in ents if i[0] == g]
                nn, oo = sum(v["n"] for v in xs), sum(v["ok"] for v in xs)
                rows += f'<div class="row"><span>{gn}</span><div class="bar"><div style="width:{int(oo / nn * 100) if nn else 0}%"></div></div><small>{len(xs)} kelime</small></div>'
            st.markdown(rows, unsafe_allow_html=True)
            load = [sum(1 for _, v in ents if v["due"] == (today + timedelta(d)).isoformat() or (d == 0 and v["due"] <= today.isoformat())) for d in range(7)]
            mxl = max(load + [1])
            st.markdown("<h3>Önümüzdeki 7 gün bakım yükü</h3><div class='chart'>" + "".join(
                f'<div class="cc {"t" if d == 0 else ""}"><em>{v or ""}</em><i style="height:{max(4, int(v / mxl * 110))}px"></i><span>{DAYS[(today + timedelta(d)).weekday()]}</span></div>'
                for d, v in enumerate(load)) + "</div>", unsafe_allow_html=True)
    with p6:
        pre, post = get_test("pre"), get_test("post")
        st.markdown('<div class="card"><div class="t">Öğrenme testi</div><small>Aynı 18 kelimelik test başlangıçta ve birkaç gün sonra yapılır. '
                    'Aradaki fark gelişimini gösterir. Testte doğru cevaplar gösterilmez ve XP verilmez.</small></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.markdown(f'<div class="tile"><b>{"%" + str(tpct(pre)) if pre else "-"}</b><span>Ön test{" · " + esc(pre["date"]) if pre else ""}</span></div>',
                    unsafe_allow_html=True)
        c2.markdown(f'<div class="tile"><b>{"%" + str(tpct(post)) if post else "-"}</b><span>Son test{" · " + esc(post["date"]) if post else ""}</span></div>',
                    unsafe_allow_html=True)
        c1.button("Ön test yapıldı" if pre else "Ön testi yap", key="t_pre", use_container_width=True, type="secondary" if pre else "primary",
                  disabled=bool(pre), on_click=start_test, args=("pre",))
        c2.button("Son testi tekrarla" if post else "Son testi yap", key="t_post", use_container_width=True,
                  type="primary" if pre else "secondary", disabled=not pre, on_click=start_test, args=("post",))
        if pre and not post:
            st.caption("Son testi en az bir hafta çalıştıktan sonra yapmanı öneririz.")
        if pre and post:
            dd = tpct(post) - tpct(pre)
            st.markdown(f'<div class="card on"><div class="t">{tw("📈", 26)} {dd:+d} puan</div><small>Son test eksi ön test</small></div>', unsafe_allow_html=True)
            rows = ""
            for g, gn in GRADE_NAMES.items():
                a, b = pre.get("by", {}).get(g), post.get("by", {}).get(g)
                pa = int(a[0] / a[1] * 100) if a and a[1] else 0
                pb = int(b[0] / b[1] * 100) if b and b[1] else 0
                rows += f'<div class="row"><span style="width:78px">{gn}</span><div class="bar"><div style="width:{pb}%"></div></div><small>%{pa} → %{pb}</small></div>'
            st.markdown("<h3>Sınıf düzeyine göre</h3>" + rows, unsafe_allow_html=True)
        if S.tests:
            tb = io.StringIO()
            tw_ = csv.writer(tb)
            tw_.writerow(["tur", "tarih", "dogru", "toplam", "yuzde", "ort_tepki_ms", "anaokulu", "sinif1", "sinif2"])
            for t in S.tests:
                by = t.get("by", {})
                tw_.writerow([t["kind"], t["date"], t["score"], t["total"], tpct(t), t.get("ms", 0)] + [f"{by[g][0]}/{by[g][1]}" if g in by else "" for g in "kab"])
            st.download_button("Test sonuçları (CSV)", tb.getvalue(), "lingonest_testler.csv", use_container_width=True, icon=":material/download:")
    with p2:
        got = [b for b in BADGES if b[3]()]
        html = "".join(f'<div class="bgi {"" if b in got else "off"}">{tw(b[1], 56)}<div>{b[0]}</div><small>{b[2]}</small></div>' for b in BADGES)
        st.markdown(f"<h3>{len(got)}/{len(BADGES)} rozet</h3><div class='bg'>{html}</div>", unsafe_allow_html=True)
    with p5:
        st.markdown(f'<div class="card on"><span class="bob">{chick(110)}</span><div class="t">{tw("🌰", 22)} {S.seeds} tohum</div>'
                    f'<small>Doğru cevap, oyun ve görevlerden tohum kazan</small></div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for n_, (i, (nm_, price, slot)) in enumerate(SHOP.items()):
            with cols[n_ % 2]:
                own, worn = i in S.owned, S.eq.get(slot) == i
                st.markdown(f'<div class="card {"on" if worn else ""}">{chick(70, eq={slot: i})}<div class="t" style="font-size:16px">{nm_}</div>'
                            f'<small>{"Takılı" if worn else "Sende" if own else f"{price} tohum"}</small></div>', unsafe_allow_html=True)
                if own:
                    st.button("Çıkar" if worn else "Tak", key=f"eq_{i}", use_container_width=True, on_click=equip, args=(i,))
                else:
                    st.button("Satın al", key=f"buy_{i}", type="primary", use_container_width=True, disabled=S.seeds < price, on_click=buy, args=(i,))
        st.markdown(f'<div class="card"><div class="t">{tw("🛡️", 26)} Seri koruyucu · {S.freeze}/3</div>'
                    '<small>Bir gün çalışamazsan serin bozulmaz · 30 tohum</small></div>', unsafe_allow_html=True)
        st.button("Satın al", key="buy_freeze", type="primary", use_container_width=True, disabled=S.seeds < 30 or S.freeze >= 3, on_click=buy_freeze)
    with p3:
        st.text_input("Adın", value=S.name, key="w_name", max_chars=20,
                      on_change=lambda: S.__setitem__("name", re.sub(r"[^\w \-]", "", S.w_name, flags=re.U).strip()[:20]))
        st.radio("Maskot rengi", list(COLORS), index=list(COLORS).index(S.color), horizontal=True, key="w_color",
                 on_change=lambda: S.__setitem__("color", S.w_color))
        st.radio("Ses aksanı", ["ABD", "İngiltere"], index=1 if S.accent == "uk" else 0, horizontal=True, key="w_acc",
                 on_change=lambda: S.__setitem__("accent", "uk" if S.w_acc == "İngiltere" else "us"))
        st.select_slider("Günlük hedef (doğru cevap)", [5, 10, 15, 20, 30], value=S.goal, key="w_goal",
                         on_change=lambda: S.__setitem__("goal", S.w_goal))
        st.toggle("Ses efektleri", value=S.sound, key="w_sound", on_change=lambda: S.__setitem__("sound", S.w_sound))
        st.toggle("Büyük yazı", value=S.big, key="w_big", on_change=lambda: S.__setitem__("big", S.w_big))
        st.toggle("Okuması kolay yazı tipi", value=S.dys, key="w_dys", on_change=lambda: S.__setitem__("dys", S.w_dys))
        st.toggle("Sakin mod (animasyonsuz)", value=S.calm, key="w_calm", on_change=lambda: S.__setitem__("calm", S.w_calm))
        if S.user:
            st.markdown(f'<div class="row"><b>{esc(S.user)}</b><small>{"Öğretmen" if S.role == "teacher" else "Öğrenci"}'
                        f'{" · Sınıf kodu: " + esc(S.class_code) if S.class_code else ""}</small></div>', unsafe_allow_html=True)
            st.button("Çıkış yap", icon=":material/logout:", use_container_width=True, on_click=logout)
            with st.expander("Hesabı sil"):
