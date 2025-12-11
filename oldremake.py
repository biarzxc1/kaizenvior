import asyncio
import aiohttp
import sys
import os
from typing import List, Optional, Dict
import json
from datetime import datetime
from rich.console import Console
from rich import print
from rich.panel import Panel
import re
import requests
import pytz
import hashlib
import uuid
import getpass

console = Console()
os.system('clear')

API_URL = 'https://rpwtoolsold-server.onrender.com/api'

config = {
    'post_id': '',
    'tokens': [],
    'total_shares': 0,
    'target_shares': 0,
    'user_data': None
}

def validate_post_id(post_id: str) -> bool:
    if not post_id:
        return False
    post_id_pattern = r'^[0-9]+$'
    return bool(re.match(post_id_pattern, post_id))

def validate_share_count(count: str) -> bool:
    try:
        count = int(count)
        return count > 0
    except ValueError:
        return False

def get_system_info() -> Dict[str, str]:
    try:
        ip_info = requests.get('https://ipapi.co/json/').json()
        ph_tz = pytz.timezone('Asia/Manila')
        ph_time = datetime.now(ph_tz)
        return {
            'ip': ip_info.get('ip', 'Unknown'),
            'region': ip_info.get('region', 'Unknown'),
            'city': ip_info.get('city', 'Unknown'),
            'time': ph_time.strftime("%I:%M:%S %p"),
            'date': ph_time.strftime("%B %d, %Y")
        }
    except:
        return {
            'ip': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown',
            'time': datetime.now().strftime("%I:%M:%S %p"),
            'date': datetime.now().strftime("%B %d, %Y")
        }

def banner():
    os.system('clear')
    sys_info = get_system_info()
    
    print(Panel(
        r"""[red]●[yellow] ●[green] ●
[cyan]██████╗░██╗░░░██╗░█████╗░
[cyan]██╔══██╗╚██╗░██╔╝██╔══██╗
[cyan]██████╔╝░╚████╔╝░██║░░██║
[cyan]██╔══██╗░░╚██╔╝░░██║░░██║
[cyan]██║░░██║░░░██║░░░╚█████╔╝
[cyan]╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░""",
        title="[bright_white] SPAMSHARE [green]●[yellow] Active [/]",
        width=65,
        style="bold bright_white",
    ))
    
    print(Panel(
        """[cyan] Tool     : [green]SpamShare[/]
[cyan] Version  : [green]1.0.0[/]
[cyan] Dev      : [green]Ryo Evisu[/]
[cyan] Status   : [red]Paid Tools[/]""",
        title="[white on red] INFORMATION [/]",
        width=65,
        style="bold bright_white",
    ))
    
    print(Panel(
        f"""[cyan] IP       : [cyan]{sys_info['ip']}[/]
[cyan] Region   : [cyan]{sys_info['region']}[/]
[cyan] City     : [cyan]{sys_info['city']}[/]
[cyan] Time     : [cyan]{sys_info['time']}[/]
[cyan] Date     : [cyan]{sys_info['date']}[/]""",
        title="[white on red] SYSTEM INFO [/]",
        width=65,
        style="bold bright_white",
    ))

def get_device_id() -> str:
    """Generate unique device ID based on MAC address"""
    try:
        mac = uuid.getnode()
        device_id = hashlib.sha256(str(mac).encode()).hexdigest()[:16].upper()
        return f"RYO-{device_id}"
    except:
        return f"RYO-{uuid.uuid4().hex[:16].upper()}"

def register_user(username: str, password: str) -> Dict:
    """Register new user with API"""
    try:
        device_id = get_device_id()
        response = requests.post(
            f'{API_URL}/users/register',
            json={'username': username, 'password': password, 'deviceId': device_id},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {'success': False, 'message': str(e)}

def login_user(username: str, password: str) -> Dict:
    """Login user with API"""
    try:
        device_id = get_device_id()
        response = requests.post(
            f'{API_URL}/users/login',
            json={'username': username, 'password': password, 'deviceId': device_id},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {'success': False, 'message': str(e)}

def add_token_to_user(username: str, token: str) -> Dict:
    """Add token to user's account"""
    try:
        response = requests.post(
            f'{API_URL}/users/add-token',
            json={'username': username, 'token': token},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_user_tokens(username: str) -> List[str]:
    """Get all tokens for user"""
    try:
        response = requests.get(
            f'{API_URL}/users/tokens/{username}',
            timeout=10
        )
        data = response.json()
        if data.get('success'):
            return data.get('tokens', [])
        return []
    except:
        return []

def update_share_count(username: str, shares: int) -> Dict:
    """Update user's total share count"""
    try:
        response = requests.post(
            f'{API_URL}/users/update-shares',
            json={'username': username, 'shares': shares},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {'success': False, 'message': str(e)}

def secure_input(prompt: str, is_password: bool = False) -> str:
    """Secure input function that shows asterisks for password"""
    if is_password:
        print(f"[bright_white]{prompt}", end='', flush=True)
        password = getpass.getpass('')
        return password
    else:
        return console.input(f"[bright_white]{prompt}")

def verify_key() -> bool:
    """Verify if user is approved"""
    while True:
        os.system('clear')
        banner()
        
        print(Panel(
            """[cyan]1.[white] Login
[cyan]2.[white] Register
[cyan]3.[white] Exit""",
            title="[bright_white]>> [Menu] <<",
            width=65,
            style="bold bright_white",
            subtitle="╭─────",
            subtitle_align="left"
        ))
        
        choice = console.input("[bright_white]   ╰─> ").strip()
        
        if choice == '1':
            # Login
            os.system('clear')
            banner()
            
            print(Panel("[white]Enter your credentials (づ｡◕‿‿◕｡)づ", 
                title="[bright_white]>> [Login] <<",
                width=65,
                style="bold bright_white",
                subtitle="╭─────",
                subtitle_align="left"
            ))
            
            username = console.input("[bright_white]   ╰─> Username: ").strip()
            password = secure_input("   ╰─> Password: ", is_password=True).strip()
            
            if not username or not password:
                print(Panel("[red]Username and password cannot be empty! (｡•́︿•̀｡)", 
                    title="[bright_white]>> [Error] <<",
                    width=65,
                    style="bold bright_white"
                ))
                console.input("\n[bright_white]Press Enter to continue...")
                continue
            
            result = login_user(username, password)
            
            if result.get('success'):
                config['user_data'] = result.get('user')
                os.system('clear')
                banner()
                print(Panel(
                    f"""[green]✓ Welcome back! (≧▽≦)

[white]Username: [cyan]{config['user_data']['username']}[/]
[white]Key: [cyan]{config['user_data']['deviceId']}[/]
[white]Total Shares: [cyan]{config['user_data']['totalShares']}[/]
[white]Status: [green]Active[/]""", 
                    title="[bright_white]>> [Login Success] <<",
                    width=65,
                    style="bold bright_white"
                ))
                console.input("\n[bright_white]Press Enter to continue...")
                return True
            else:
                print(Panel(f"[red]Login failed! (｡•́︿•̀｡)\n[white]{result.get('message', 'Unknown error')}", 
                    title="[bright_white]>> [Error] <<",
                    width=65,
                    style="bold bright_white"
                ))
                console.input("\n[bright_white]Press Enter to continue...")
        
        elif choice == '2':
            # Register
            os.system('clear')
            banner()
            
            device_id = get_device_id()
            
            print(Panel(
                f"""[white]Your Key: [cyan]{device_id}[/]
[yellow]This key will be used to identify your device[/]

[white]Create your account (づ｡◕‿‿◕｡)づ""", 
                title="[bright_white]>> [Registration] <<",
                width=65,
                style="bold bright_white",
                subtitle="╭─────",
                subtitle_align="left"
            ))
            
            username = console.input("[bright_white]   ╰─> Username: ").strip()
            password = secure_input("   ╰─> Password: ", is_password=True).strip()
            confirm_password = secure_input("   ╰─> Confirm Password: ", is_password=True).strip()
            
            if not username or not password:
                print(Panel("[red]Username and password cannot be empty! (｡•́︿•̀｡)", 
                    title="[bright_white]>> [Error] <<",
                    width=65,
                    style="bold bright_white"
                ))
                console.input("\n[bright_white]Press Enter to continue...")
                continue
            
            if password != confirm_password:
                print(Panel("[red]Passwords do not match! (｡•́︿•̀｡)", 
                    title="[bright_white]>> [Error] <<",
                    width=65,
                    style="bold bright_white"
                ))
                console.input("\n[bright_white]Press Enter to continue...")
                continue
            
            register_result = register_user(username, password)
            
            if register_result.get('success'):
                print(Panel(
                    f"""[green]Registration successful! (≧▽≦)

[white]Username: [cyan]{username}[/]
[white]Key: [cyan]{device_id}[/]

[yellow]Please send your Username and Key to:
[cyan]@ryograhhh[/] for approval

[white]After approval, login to use the tool!""", 
                    title="[bright_white]>> [Pending Approval] <<",
                    width=65,
                    style="bold bright_white"
                ))
            else:
                print(Panel(f"[red]Registration failed! (｡•́︿•̀｡)\n[white]{register_result.get('message', 'Unknown error')}", 
                    title="[bright_white]>> [Error] <<",
                    width=65,
                    style="bold bright_white"
                ))
            
            console.input("\n[bright_white]Press Enter to continue...")
        
        elif choice == '3':
            return False
        
        else:
            print(Panel("[red]Invalid choice! (｡•́︿•̀｡)", 
                title="[bright_white]>> [Error] <<",
                width=65,
                style="bold bright_white"
            ))
            console.input("\n[bright_white]Press Enter to continue...")

def manage_tokens():
    """Manage user tokens"""
    while True:
        os.system('clear')
        banner()
        
        username = config['user_data']['username']
        tokens = get_user_tokens(username)
        
        print(Panel(f"[white]Total Tokens: [green]{len(tokens)}[/]", 
            title="[bright_white]>> [Token Manager] <<",
            width=65,
            style="bold bright_white"
        ))
        
        print(Panel(
            """[cyan]1.[white] Add Token
[cyan]2.[white] View Tokens
[cyan]3.[white] Continue to Tool
[cyan]4.[white] Exit""",
            title="[bright_white]>> [Menu] <<",
            width=65,
            style="bold bright_white",
            subtitle="╭─────",
            subtitle_align="left"
        ))
        
        choice = console.input("[bright_white]   ╰─> ").strip()
        
        if choice == '1':
            print(Panel("[white]Enter Facebook Access Token:", 
                title="[bright_white]>> [Add Token] <<",
                width=65,
                style="bold bright_white",
                subtitle="╭─────",
                subtitle_align="left"
            ))
            token = console.input("[bright_white]   ╰─> ").strip()
            
            if token:
                result = add_token_to_user(username, token)
                if result.get('success'):
                    print(Panel("[green]Token added successfully! (≧▽≦)", 
                        title="[bright_white]>> [Success] <<",
                        width=65,
                        style="bold bright_white"
                    ))
                else:
                    print(Panel(f"[red]Failed to add token! (｡•́︿•̀｡)\n[white]{result.get('message', 'Unknown error')}", 
                        title="[bright_white]>> [Error] <<",
                        width=65,
                        style="bold bright_white"
                    ))
                console.input("\n[bright_white]Press Enter to continue...")
        
        elif choice == '2':
            if tokens:
                token_list = '\n'.join([f"[cyan]{i+1}.[white] {token[:30]}..." for i, token in enumerate(tokens)])
                print(Panel(token_list, 
                    title="[bright_white]>> [Your Tokens] <<",
                    width=65,
                    style="bold bright_white"
                ))
            else:
                print(Panel("[yellow]No tokens found! Add some tokens first.", 
                    title="[bright_white]>> [No Tokens] <<",
                    width=65,
                    style="bold bright_white"
                ))
            console.input("\n[bright_white]Press Enter to continue...")
        
        elif choice == '3':
            if tokens:
                config['tokens'] = tokens
                return True
            else:
                print(Panel("[red]Please add at least one token first! (｡•́︿•̀｡)", 
                    title="[bright_white]>> [Error] <<",
                    width=65,
                    style="bold bright_white"
                ))
                console.input("\n[bright_white]Press Enter to continue...")
        
        elif choice == '4':
            return False
        
        else:
            print(Panel("[red]Invalid choice! (｡•́︿•̀｡)", 
                title="[bright_white]>> [Error] <<",
                width=65,
                style="bold bright_white"
            ))
            console.input("\n[bright_white]Press Enter to continue...")

class ShareManager:
    def __init__(self):
        self.error_count = 0
        self.success_count = 0
        self.total_shares = 0
        
    async def share(self, session: aiohttp.ClientSession, token: str, target_shares: int):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'accept-encoding': 'gzip, deflate',
            'host': 'graph.facebook.com'
        }
        
        while True:
            try:
                async with session.post(
                    'https://graph.facebook.com/me/feed',
                    params={
                        'link': f'https://facebook.com/{config["post_id"]}',
                        'published': '0',
                        'access_token': token
                    },
                    headers=headers,
                    timeout=10
                ) as response:
                    data = await response.json()
                    if 'id' in data:
                        self.success_count += 1
                        self.total_shares += 1
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        console.print(f"[cyan][{timestamp}][/cyan][green] Share Completed [yellow]{config['post_id']} [red]{self.total_shares}/{target_shares}")
                        
                        if self.total_shares >= target_shares:
                            return
                    else:
                        self.error_count += 1
                        if 'error' in data:
                            error_msg = data['error'].get('message', 'Unknown error')
                            if "Error validating access token" in error_msg or "blocking" in error_msg:
                                return
            except:
                self.error_count += 1
                continue

def get_user_input_sync(prompt: str, validator_func, error_message: str) -> Optional[str]:
    """Synchronous user input function"""
    while True:
        os.system('clear')
        banner()
        
        print(Panel(
            f"""[white]USERNAME: [cyan]{config['user_data']['username']}[/]
[white]KEY: [cyan]{config['user_data']['deviceId']}[/]
[white]TOTAL SHARES: [cyan]{config['user_data']['totalShares']}[/]
[white]OVERALL SHARES USERS DONE: [cyan]{config['user_data'].get('overallShares', 0)}[/]""",
            title="[bright_white]>> [Profile Info] <<",
            width=65,
            style="bold bright_white"
        ))
        
        print(Panel(f"[white]Loaded [green]{len(config['tokens'])}[white] tokens", 
            title="[bright_white]>> [Information] <<",
            width=65,
            style="bold bright_white"
        ))
        
        print(Panel(prompt, 
            title="[bright_white]>> [Input] (｡♡‿♡｡) <<",
            width=65,
            style="bold bright_white",
            subtitle="╭─────",
            subtitle_align="left"
        ))
        user_input = console.input("[bright_white]   ╰─> ").strip()
        
        if user_input.lower() == 'exit':
            return None
            
        if validator_func(user_input):
            return user_input
        else:
            print(Panel(f"[red]{error_message} (｡•́︿•̀｡)", 
                title="[bright_white]>> [Error] <<",
                width=65,
                style="bold bright_white"
            ))
            console.input("\n[bright_white]Press Enter to continue...")

def boost_again() -> bool:
    """Ask if user wants to boost again"""
    print(Panel("[white]Do you want to boost again? (y/n) (◕‿◕✿)", 
        title="[bright_white]>> [Input] <<",
        width=65,
        style="bold bright_white",
        subtitle="╭─────",
        subtitle_align="left"
    ))
    response = console.input("[bright_white]   ╰─> ").lower()
    return response == 'y'

async def main():
    try:
        # Verify user first
        if not verify_key():
            return
        
        # Manage tokens
        if not manage_tokens():
            return
        
        while True:
            banner()
            
            print(Panel(
                f"""[white]USERNAME: [cyan]{config['user_data']['username']}[/]
[white]KEY: [cyan]{config['user_data']['deviceId']}[/]
[white]TOTAL SHARES: [cyan]{config['user_data']['totalShares']}[/]
[white]OVERALL SHARES USERS DONE: [cyan]{config['user_data'].get('overallShares', 0)}[/]""",
                title="[bright_white]>> [Profile Info] <<",
                width=65,
                style="bold bright_white"
            ))
            
            print(Panel(f"[white]Tokens: [green]{len(config['tokens'])}[/]", 
                title="[bright_white]>> [Information] <<",
                width=65,
                style="bold bright_white"
            ))
            
            config['post_id'] = get_user_input_sync(
                "[white]Enter Post ID (づ｡◕‿‿◕｡)づ",
                validate_post_id,
                "Invalid Post ID format. Please enter a valid numeric Post ID."
            )
            
            if not config['post_id']:
                return
                
            share_count_input = get_user_input_sync(
                "[white]Enter total shares (no limit) (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
                validate_share_count,
                "Invalid share count. Please enter a positive number."
            )
            
            if not share_count_input:
                return
                
            target_shares = int(share_count_input)
            
            os.system('clear')
            banner()
            
            print(Panel(
                f"""[white]Starting share process... (ง •̀ω•́)ง✧
Target: [green]{target_shares}[white] shares""", 
                title="[bright_white]>> [Process Started] <<",
                width=65,
                style="bold bright_white"
            ))
            
            share_manager = ShareManager()
            
            connector = aiohttp.TCPConnector(limit=0)
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                for token in config['tokens']:
                    task = asyncio.create_task(share_manager.share(session, token, target_shares))
                    tasks.append(task)
                await asyncio.gather(*tasks)
            
            # Update total shares in database
            username = config['user_data']['username']
            new_total = config['user_data']['totalShares'] + share_manager.total_shares
            update_share_count(username, new_total)
            config['user_data']['totalShares'] = new_total
            
            os.system('clear')
            banner()
            print(Panel(
                f"""[green]PROCESS COMPLETED (≧▽≦)
[white]Shares Completed: [cyan]{share_manager.total_shares}[/]
[white]Your Total Shares: [cyan]{new_total}[/]
[white]Time to celebrate! ♪┏(・o･)┛♪┗ ( ･o･) ┓♪""", 
                title="[bright_white]>> [Completed] <<",
                width=65,
                style="bold bright_white"
            ))
            
            if not boost_again():
                break

    except KeyboardInterrupt:
        print(Panel("[white]Script terminated by user (╥﹏╥)", 
            title="[bright_white]>> [Terminated] <<",
            width=65,
            style="bold bright_white"
        ))
    except Exception as e:
        print(Panel(f"[red]{str(e)} (っ˘̩╭╮˘̩)っ", 
            title="[bright_white]>> [Error] <<",
            width=65,
            style="bold bright_white"
        ))
    finally:
        print(Panel("[white]Press Enter to exit... (｡•́︿•̀｡)", 
            title="[bright_white]>> [Exit] <<",
            width=65,
            style="bold bright_white",
            subtitle="╭─────",
            subtitle_align="left"
        ))
        console.input("[bright_white]   ╰─> ")

if __name__ == "__main__":
    asyncio.run(main())
