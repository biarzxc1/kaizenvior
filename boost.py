import os
import sys
import requests
import time
import random
import uuid
import hashlib
from datetime import datetime
from pystyle import Colors, Colorate, Center
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ==========================================
# âš™ï¸ ADMIN CONFIG (áž€áŸ†ážŽážáŸ‹ážšáž”ážŸáŸ‹áž¢áŸ’áž“áž€)
# ==========================================
# 1. ážŠáž¶áž€áŸ‹ Link áž¯áž€ážŸáž¶ážš whitelist.txt áž–áž¸ GitHub ážšáž”ážŸáŸ‹áž¢áŸ’áž“áž€ (RAW LINK)
DATABASE_URL = "https://github.com/CyraxmodDOne/my-license/blob/main/whitelist.txt"

# 2. ážŠáž¶áž€áŸ‹ Telegram ážšáž”ážŸáŸ‹áž¢áŸ’áž“áž€
ADMIN_TELEGRAM = "https://t.me/CyraxmodTool016"

TOOL_NAME = "TDS TIKTOK VIP (LOCKED)"
# ==========================================

# Colors
P = '\x1b[1;37m' # White
M = '\x1b[1;31m' # Red
H = '\x1b[1;32m' # Green
K = '\x1b[1;33m' # Yellow
B = '\x1b[1;34m' # Blue
O = '\x1b[1;36m' # Cyan
N = '\x1b[0m'    # Reset

console = Console()
os_type = 'mb' if sys.platform.startswith('linux') else 'pc'

# --- ðŸ” LICENSE SYSTEM (áž”áŸ’ážšáž–áŸáž“áŸ’áž’ážŸáŸ„) ---
def get_hwid():
    """áž”áž„áŸ’áž€áž¾áž Key áž–áž¸áž›áŸážážŸáž˜áŸ’áž‚áž¶áž›áŸ‹áž˜áŸ‰áž¶ážŸáŸŠáž¸áž“ (ážáŸážš)"""
    try:
        id_file = "tiktok_device.lic"
        if os.path.exists(id_file):
            with open(id_file, 'r') as f:
                device_id = f.read().strip()
        else:
            device_id = str(uuid.uuid4())
            with open(id_file, 'w') as f:
                f.write(device_id)
        
        params = f"{device_id}-TIKTOK-VIP"
        hashed = hashlib.md5(params.encode()).hexdigest().upper()
        key = f"CYRAX-TIK-{hashed[:10]}"
        return key
    except:
        return "CYRAX-UNKNOWN"

def check_license():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{K}Checking License... Please wait...{N}")
    
    current_key = get_hwid()
    
    try:
        response = requests.get(DATABASE_URL, timeout=15).text
        
        if current_key in response:
            print(f"\n{H} [SUCCESS] KEY APPROVED! WELCOME VIP MEMBER.{N}")
            time.sleep(2)
            return True
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"""{M}
  _  _________  __   ____  __  ______  ________ 
 / |/ / __ \  |/  / / __ \/  |/  / _ \/ ___/ _ \\
/    / /_/ / /|_/ / / /_/ / /|_/ / ___/ /__/ // /
/_/ |_|\____/_/  /_/  \____/_/  /_/_/   \___/____/ 
                                                  
{K}==================================================
{M} [!] ACCESS DENIED! YOUR KEY IS NOT REGISTERED.
{M} [!] THIS IS A PAID TOOL.
{K}==================================================
{P} [ðŸ‘‰] YOUR KEY : {H}{current_key}
{K}==================================================
{P} [1] Copy Key ážáž¶áž„áž›áž¾
{P} [2] áž•áŸ’áž‰áž¾áž‘áŸ…áž€áž¶áž“áŸ‹ Admin ážŠáž¾áž˜áŸ’áž”áž¸áž…áž»áŸ‡ážˆáŸ’áž˜áŸ„áŸ‡
{P} [3] Telegram: {O}{ADMIN_TELEGRAM}
{K}=================================================={N}""")
            
            try:
                os.system(f"xdg-open {ADMIN_TELEGRAM}")
            except: pass
            sys.exit()
            
    except requests.exceptions.ConnectionError:
        print(f"\n{M} [!] NO INTERNET CONNECTION.{N}")
        sys.exit()
    except Exception as e:
        print(f"\n{M} [!] SERVER ERROR: {e}{N}")
        sys.exit()

# --- ðŸ› ï¸ TIKTOK TDS LOGIC ---

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    logo = """
   ______   _____  ___   _  __   __  _______  ____ 
  / ____/  / _ \ \/ / | |/_/  /  |/  / __ \/ __ \ 
 / /      / /_/ \  / /|   <   / /|_/ / / / / / / / 
/ /___   /_/    /_/ /_ /|_|  /_/  /_/_____/_____/  
                                                   
    """
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(logo), 1))
    
    info = Panel(
        Text(f"OWNER: CYRAX MOD | LOGIC: CAMBODIA RECODE | VER: 2.0", justify="center", style="bold white"),
        title=f"[bold red]â”[ {TOOL_NAME} ]â”",
        subtitle=f"[bold yellow]Tele: {ADMIN_TELEGRAM}",
        style="bold green",
        border_style="bright_blue"
    )
    console.print(info)

def linex():
    print(f'{K}=================================================={N}')

def open_url(link):
    if os_type == 'mb':
        os.system(f'xdg-open {link}')
    else:
        os.system(f'start {link}')

def delay(seconds):
    for i in range(seconds, -1, -1):
        print(f'{K}[{H}CYRAX{K}] | Wait: {P}{i}s{K}   ', end='\r')
        time.sleep(1)
    print('                    ', end='\r')

class TDS_API:
    def __init__(self, token):
        self.token = token
        self.url = 'https://traodoisub.com/api/'
    
    def login(self):
        try:
            r = requests.get(f'{self.url}?fields=profile&access_token={self.token}')
            return r.json().get('data', False)
        except: return False

    def config_run(self, tiktok_id):
        try:
            r = requests.get(f'{self.url}?fields=tiktok_run&id={tiktok_id}&access_token={self.token}')
            return r.json().get('data', False)
        except: return False

    def get_jobs(self, job_type):
        try:
            r = requests.get(f'{self.url}?fields={job_type}&access_token={self.token}')
            return r.json()
        except: return False

    def cache_job(self, job_id, job_type):
        try:
            r = requests.get(f'{self.url}coin/?type={job_type}&id={job_id}&access_token={self.token}')
            data = r.json()
            if 'cache' in data: 
                return True
            return False
        except: return False

    def claim_money(self, job_type):
        api_id_map = {
            'TIKTOK_LIKE': 'TIKTOK_LIKE_API',
            'TIKTOK_FOLLOW': 'TIKTOK_FOLLOW_API'
        }
        api_id = api_id_map.get(job_type, 'TIKTOK_FOLLOW_API')
        
        try:
            r = requests.get(f'{self.url}coin/?type={job_type}&id={api_id}&access_token={self.token}')
            return r.json()
        except: return False

def main():
    # 1. áž áŸ… Check License áž˜áž»áž“áž‚áŸ
    check_license()
    
    banner()
    
    if os.path.exists('config_tds.txt'):
        with open('config_tds.txt', 'r') as f: token = f.read().strip()
    else:
        token = input(f"{H}[?] Enter TDS Token: {P}")
        with open('config_tds.txt', 'w') as f: f.write(token)
    
    api = TDS_API(token)
    info = api.login()
    
    if not info:
        print(f"{M}[!] Token Invalid! Delete config_tds.txt{N}")
        sys.exit()
    
    banner()
    print(f"{H} [âœ“] USER: {O}{info['user']}")
    print(f"{H} [âœ“] COIN: {K}{info['xu']}")
    linex()
    
    print(f"{H} [1] {P}Auto Like")
    print(f"{H} [2] {P}Auto Follow")
    print(f"{H} [3] {P}Auto Follow (TikTok Now)")
    linex()
    
    option = input(f"{H} [?] Choose: {P}")
    delay_time = int(input(f"{H} [?] Delay (sec): {P}"))
    job_limit = int(input(f"{H} [?] Claim after (Recommend 8-10): {P}"))
    
    tiktok_user = input(f"{H} [?] Enter TikTok ID to run: {P}")
    if api.config_run(tiktok_user):
        print(f"{H} [âœ“] Configured successfully!{N}")
    else:
        print(f"{M} [!] Config failed! Check ID.{N}")
        sys.exit()
        
    linex()
    
    if option == '1':
        get_type = 'tiktok_like'
        cache_type = 'TIKTOK_LIKE_CACHE'
        claim_type = 'TIKTOK_LIKE'
        log_text = "LIKE"
    else:
        get_type = 'tiktok_follow'
        cache_type = 'TIKTOK_FOLLOW_CACHE'
        claim_type = 'TIKTOK_FOLLOW'
        log_text = "FOLLOW"

    count = 0
    
    while True:
        jobs_data = api.get_jobs(get_type)
        
        if not jobs_data:
            continue
            
        if 'error' in str(jobs_data):
            err = jobs_data.get('error', '')
            if 'thao tac qua nhanh' in err.lower():
                 print(f"{M}[!] Too fast! Waiting...{N}", end='\r')
                 delay(10)
            else:
                 api.claim_money(claim_type)
            continue
            
        job_list = jobs_data.get('data', [])
        if not job_list:
            print(f"{K}[!] No jobs found, retrying...{N}", end='\r')
            delay(2)
            continue
            
        print(f"{H}[+] Found {len(job_list)} jobs.{N}")
        
        for job in job_list:
            job_id = job['id']
            link = job['link']
            
            if option == '3':
                uid = job_id.split('_')[0]
                unique = job.get('uniqueID', 'user')
                if os_type == 'mb':
                    link = f'tiktoknow://user/profile?user_id={uid}'
                else:
                    link = f'https://now.tiktok.com/@{unique}'

            open_url(link)
            
            is_cached = api.cache_job(job_id, cache_type)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if is_cached:
                count += 1
                print(f"{P}[{count}] {M}| {O}{timestamp} {M}| {H}{log_text} {M}| {P}{job_id} {H}| OK")
                delay(delay_time)
            else:
                print(f"{P}[X] {M}| {O}{timestamp} {M}| {H}{log_text} {M}| {P}{job_id} {M}| FAILED")
            
            if count % job_limit == 0:
                print(f"{K}[*] Claiming coins...{N}")
                res = api.claim_money(claim_type)
                
                if res and 'data' in res:
                    msg = res['data'].get('msg', 'Claimed')
                    xu_them = res['data'].get('xu_them', 0)
                    total_xu = res['data'].get('xu', 0)
                    
                    print(f"{H}â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€{N}")
                    print(f"{H} [âœ“] SUCCESS: {P}+{xu_them} Xu")
                    print(f"{H} [âœ“] TOTAL  : {K}{total_xu} Xu")
                    print(f"{H} [âœ“] MSG    : {O}{msg}")
                    print(f"{H}â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€{N}")
                    delay(5)
                else:
                    print(f"{M}[!] Claim failed. Will try again later.{N}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{M}[!] Stopped.{N}")
