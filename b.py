import requests, sys, json, uuid, time, os
from colorama import init, Fore, Back, Style

os.system('cls' if os.name=='nt' else 'clear')
init(autoreset=True)  
API="https://zefame-free.com/api_free.php?action=config"

# --- COLOR UTILITIES ---
trang = "\033[1;37m"
xanh_la = "\033[1;32m"
xanh_duong = "\033[1;34m"
do = "\033[1;31m"
vang = "\033[1;33m"
kt_code = "</>" 

logo = f"""
\x1b[38;5;46m                        ¶¶¶¶¶¶
\x1b[38;5;46m                       ¶¶¶¶¶¶¶¶
\x1b[38;5;27m                      ¶¶¶¶¶¶¶¶¶¶
\x1b[38;5;27m                     ¶¶¶¶¶¶¶¶¶¶¶¶
\x1b[38;5;220m                     ¶¶¶¶__¶_¶¶¶¶
\x1b[38;5;220m                     ¶¶¶__¶___¶¶¶
\x1b[38;5;196m                     ¶¶¶___¶¶_¶¶¶
\x1b[38;5;196m                     ¶¶¶¶¶¶¶¶¶¶¶¶
\x1b[38;5;46m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;46m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;27m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;27m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;220m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;220m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;196m                      ¶¶_¶¶¶¶_¶¶
\x1b[38;5;196m_¶¶_¶¶¶¶_¶¶_________________________________¶¶_¶¶¶¶_¶¶
\x1b[38;5;46m_¶¶_¶¶¶¶_¶¶________________________________¶¶¶_¶¶¶¶_¶¶    
\x1b[38;5;46m_¶¶_¶¶¶¶_¶¶________________________________¶¶¶_¶¶¶¶_¶¶
\x1b[38;5;27m_¶¶_¶¶¶¶_¶¶____¶____¶____¶____¶____¶____¶___¶¶¶_¶¶¶¶ ¶
\x1b[38;5;27m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\x1b[38;5;220m_¶¶_¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\x1b[38;5;220m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\x1b[38;5;196m_¶¶_¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\x1b[38;5;196m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\x1b[38;5;46m_¶¶_¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\x1b[38;5;46m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\x1b[38;5;27m_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\033[1;32m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
\033[1;32m[\033[1;37m+\033[1;32m] \033[1;37mTikTok View Booster
\033[1;32m[\033[1;37m+\033[1;32m] \033[1;37mVersion : 1.0
\033[1;32m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

names = {
    229: "TikTok Views",
    228: "TikTok Followers",
    232: "TikTok Free Likes",
    235: "TikTok Free Shares",
    236: "TikTok Free Favorites"
}

# Display Logo
os.system('cls' if os.name=='nt' else 'clear')
print(logo)

# Fetch configuration
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        data = json.load(f)
else:
    try:
        data = requests.get("https://zefame-free.com/api_free.php?action=config").json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}ERROR: Could not fetch config from the server.{Style.RESET_ALL}")
        print(f"{Fore.RED}Please check the domain or your internet connection. ({e}){Style.RESET_ALL}")
        sys.exit()

# Display services
services = data.get('data', {}).get('tiktok', {}).get('services', [])
for i, service in enumerate(services, 1):
    sid = service.get('id')
    name = names.get(sid, service.get('name', '').strip())
    rate = service.get('description', '').strip()
    if rate:
        rate = f"[{rate.replace('vues', 'views').replace('partages', 'shares').replace('favoris', 'favorites')}]"
    
    status = f"{Fore.GREEN}[WORKING]{Style.RESET_ALL}" if service.get('available') else f"{Fore.RED}[DOWN]{Style.RESET_ALL}"
    print(f"{i}. {name} — {status}  {Fore.CYAN}{rate}{Style.RESET_ALL}")

# Get user selection
choice = input('Select number (Enter to exit): ').strip()
if not choice:
    sys.exit()

try:
    idx = int(choice)
    if idx < 1 or idx > len(services):
        print('Out of range')
        sys.exit()
except:
    print('Invalid')
    sys.exit()

selected = services[idx-1]
video_link = input('Enter video link: ')

# Get video ID
id_check = requests.post("https://zefame-free.com/api_free.php?", data={"action": "checkVideoId", "link": video_link})
video_id = id_check.json().get("data", {}).get("videoId")
print("Parsed Video ID:", video_id)

print()

# Start boost loop
while True:
    order = requests.post("https://zefame-free.com/api_free.php?action=order", data={"service": selected.get('id'), "link": video_link, "uuid": str(uuid.uuid4()), "videoId": video_id})
    result = order.json()
    print(f"{Fore.GREEN}{json.dumps(result, separators=(',',':'))}{Style.RESET_ALL}")
    wait = result.get("data", {}).get("nextAvailable")
    if wait:
        try:
            wait = float(wait)
            if wait > time.time(): 
                print(f"{Fore.YELLOW}Waiting for cooldown period...{Style.RESET_ALL}")
                time.sleep(wait - time.time() + 1)
        except:
            pass
