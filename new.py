import os
import sys
import aiohttp
import asyncio
import datetime
import time
import uuid
import hashlib
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

console = Console()
success_count = 0
lock = asyncio.Lock()

# --- BEAUTIFUL BANNER ---
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo_art = """\033[1;37m
\033[1;35m                        ¶¶¶¶¶¶
\033[1;37m                       ¶¶¶¶¶¶¶¶
\033[1;35m                      ¶¶¶¶¶¶¶¶¶¶
\033[1;37m                     ¶¶¶¶__¶_¶¶¶¶
\033[1;37m                     ¶¶¶__¶___¶¶¶
\033[1;35m                     ¶¶¶___¶¶_¶¶¶
\033[1;37m                     ¶¶¶¶____¶¶¶¶
\033[1;35m                     ¶¶¶¶¶¶¶¶¶¶¶¶
\033[1;37m                      ¶¶_¶¶¶¶_¶¶
\033[1;35m                      ¶¶_¶¶¶¶_¶¶
\033[1;37m                      ¶¶_¶¶¶¶_¶¶
\033[1;35m                      ¶¶_¶¶¶¶_¶¶
\033[1;37m                      ¶¶_¶¶¶¶_¶¶
\033[1;35m                      ¶¶_¶¶¶¶_¶¶
\033[1;37m                      ¶¶_¶¶¶¶_¶¶
\033[1;35m_¶¶_¶¶¶¶_¶¶_______________________________________¶¶
\033[1;37m_¶¶_¶¶¶¶_¶¶______________________________________¶¶¶
\033[1;35m_¶¶_¶¶¶¶_¶¶____¶____¶____¶____¶____¶____¶____¶___¶¶¶
\033[1;37m_¶¶_¶¶¶¶_¶¶___¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶_¶¶¶¶¶
\033[1;35m_¶¶_¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\033[1;37m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\033[1;35m_¶¶_¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\033[1;37m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\033[1;35m_¶¶_¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
\033[1;37m_¶¶_¶¶¶¶_¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶__¶¶¶¶
\033[1;35m_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶"""
    print(logo_art)
    
    info = Panel(
        Text("FACEBOOK SHARE PRO | FREE VERSION | NO LICENSE REQUIRED", justify="center", style="bold white"),
        title="[bold red]━[ FACEBOOK SHARE TOOL ]━",
        subtitle="[bold yellow]⚡ MAX SPEED ⚡",
        style="bold green",
        border_style="bright_blue"
    )
    console.print(info)

def read_lines(filename):
    """Read lines from a file and return as list"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[bold red]❌ File '{filename}' not found![/]")
        return []
    except Exception as e:
        console.print(f"[bold red]❌ Error reading '{filename}': {e}[/]")
        return []

# --- CORE LOGIC ---
async def getid(session, link):
    """Extract Facebook post ID from link"""
    try:
        async with session.post('https://id.traodoisub.com/api.php', data={"link": link}, timeout=10) as response:
            rq = await response.json()
            return rq.get("id")
    except asyncio.TimeoutError:
        console.print("[bold red]⚠️ Timeout getting post ID[/]")
        return None
    except Exception as e:
        console.print(f"[bold red]⚠️ Error getting post ID: {e}[/]")
        return None

async def get_token(session, token, cookie):
    """Get all pages associated with a token"""
    headers = {
        'cookie': cookie, 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        async with session.get(
            f'https://graph.facebook.com/me/accounts?access_token={token}', 
            headers=headers,
            timeout=15
        ) as r:
            rq = await r.json()
            return rq.get('data', [])
    except asyncio.TimeoutError:
        console.print("[bold yellow]⚠️ Timeout fetching pages for a token[/]")
        return []
    except Exception as e:
        console.print(f"[bold yellow]⚠️ Error fetching pages: {e}[/]")
        return []

async def share_post(session, tk, ck, post_id, published):
    """Share a post using page token"""
    headers = {
        'cookie': ck, 
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = f'https://graph.facebook.com/me/feed?method=POST&link=https://m.facebook.com/{post_id}&published={published}&access_token={tk}'
    
    try:
        async with session.get(url, headers=headers, timeout=15) as r:
            data = await r.json()
            if 'id' in data:
                return True, data['id']
            
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            return False, error_msg
    except asyncio.TimeoutError:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

async def worker(session, page, post_id, semaphore):
    """Worker function to handle sharing for a single page"""
    global success_count
    published = 0
    
    async with semaphore:
        while True:
            is_ok, result = await share_post(session, page['tk'], page['ck'], post_id, published)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            if is_ok:
                async with lock:
                    success_count += 1
                    count = success_count
                
                # Success log
                log_msg = (
                    f"[bold green]SUCCESS[/] "
                    f"[white]•[/] [cyan]{timestamp}[/] "
                    f"[white]•[/] [bold blue]ID:{page['page_id']}[/] "
                    f"[white]•[/] [magenta]Method:{published}[/] "
                    f"[white]➜[/] [bold yellow]TOTAL: {count}[/]"
                )
                console.print(log_msg)
                await asyncio.sleep(0.5)
            else:
                error_lower = str(result).lower()
                
                # Handle specific errors
                if "blocked" in error_lower or "spam" in error_lower:
                    console.print(f"[bold red]BLOCKED • Page ID:{page['page_id']} • Pausing 5 minutes...[/]")
                    await asyncio.sleep(300)  # Wait 5 minutes
                elif "invalid" in error_lower or "token" in error_lower:
                    console.print(f"[bold red]INVALID TOKEN • Page ID:{page['page_id']} • Stopping this worker[/]")
                    break  # Stop this worker
                elif "rate limit" in error_lower:
                    console.print(f"[bold yellow]RATE LIMIT • Page ID:{page['page_id']} • Waiting 30s[/]")
                    await asyncio.sleep(30)
                else:
                    # Switch between published methods (0 = draft, 1 = published)
                    published = 1 if published == 0 else 0
                    await asyncio.sleep(2)

async def main():
    """Main function"""
    banner()
    
    # Get post link from user
    post_link = console.input("\n[bold green][?] Enter Facebook Post Link: [bold white]")
    
    if not post_link.strip():
        console.print("[bold red]❌ Post link cannot be empty![/]")
        return
    
    async with aiohttp.ClientSession() as session:
        # Extract post ID
        console.print("[bold yellow]🔄 Extracting Post ID...[/]")
        post_id = await getid(session, post_link)
        
        if not post_id:
            console.print("[bold red]❌ Invalid Post Link or Unable to Extract ID![/]")
            return
        
        console.print(f"[bold green]✅ Post ID: {post_id}[/]\n")
        
        # Read tokens and cookies
        console.print("[bold yellow]📂 Reading token.txt and cookie.txt...[/]")
        tokens = read_lines('token.txt')
        cookies = read_lines('cookie.txt')
        
        if not tokens:
            console.print("[bold red]❌ token.txt is empty or missing![/]")
            console.print("[bold yellow]💡 Create 'token.txt' with one token per line[/]")
            return
        
        if not cookies:
            console.print("[bold red]❌ cookie.txt is empty or missing![/]")
            console.print("[bold yellow]💡 Create 'cookie.txt' with one cookie per line[/]")
            return
        
        console.print(f"[bold green]✅ Loaded {len(tokens)} token(s) and {len(cookies)} cookie(s)[/]\n")
        
        # Scan pages from all tokens
        console.print(f"[bold yellow]🔍 Scanning Pages from {len(tokens)} Token(s)...[/]")
        pages = []
        
        for idx, token in enumerate(tokens, 1):
            console.print(f"[bold cyan]   → Scanning token {idx}/{len(tokens)}...[/]", end="\r")
            p_data = await get_token(session, token, cookies[0])
            
            for p in p_data:
                pages.append({
                    "tk": p.get("access_token", ""),
                    "page_id": p.get("id", ""),
                    "name": p.get("name", "Unknown"),
                    "ck": cookies[0]
                })
        
        if not pages:
            console.print("\n[bold red]❌ No Pages Found! Check your tokens.[/]")
            return
        
        console.print(f"\n[bold green]✅ Found {len(pages)} Page(s)[/]")
        
        # Display page list
        table = Table(title="📄 Pages Found", show_header=True, header_style="bold magenta")
        table.add_column("No.", style="cyan", justify="center")
        table.add_column("Page Name", style="green")
        table.add_column("Page ID", style="yellow")
        
        for idx, page in enumerate(pages[:10], 1):  # Show first 10
            table.add_row(str(idx), page['name'], page['page_id'])
        
        if len(pages) > 10:
            table.add_row("...", f"... and {len(pages) - 10} more", "...")
        
        console.print(table)
        console.print()
        
        # Start sharing
        console.print(f"[bold green]🚀 Starting Share Attack with {len(pages)} Pages...[/]\n")
        console.print("[bold yellow]Press CTRL+C to stop[/]\n")
        
        # Create workers with semaphore to limit concurrent tasks
        semaphore = asyncio.Semaphore(100)  # Max 100 concurrent requests
        tasks = [worker(session, p, post_id, semaphore) for p in pages]
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            console.print(f"\n[bold red]❌ Error: {e}[/]")

if __name__ == "__main__":
    try:
        # Check if required libraries are installed
        console.print("[bold cyan]🔧 Checking dependencies...[/]")
        
        # Run main function
        asyncio.run(main())
        
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]⚠️ Stopped by user (CTRL+C)[/]")
        console.print("[bold green]👋 Thank you for using Facebook Share Tool![/]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Fatal Error: {e}[/]")
        import traceback
        console.print(f"[bold red]{traceback.format_exc()}[/]")
