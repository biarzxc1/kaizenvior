import os
import sys
import subprocess
import time
import threading
import random
import json

# --- AUTO-INSTALLER SECTION ---
def install_requirements():
    # Added 'requests' for the API functionality
    requirements = [("rich", "rich"), ("pyttsx3", "pyttsx3"), ("requests", "requests")]
    needs_install = False
    
    for package, import_name in requirements:
        try:
            __import__(import_name)
        except ImportError:
            needs_install = True
            print(f"[!] {package} is missing. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError:
                sys.exit(1)
    
    if needs_install:
        os.system('cls' if os.name == 'nt' else 'clear')

install_requirements()

# --- IMPORTS ---
import pyttsx3
import requests
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align

# Initialize Console
console = Console()

# --- CONFIGURATION ---
LABEL_WIDTH = 12 
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- AUDIO ENGINE ---
def speak_async(text):
    """Speaks text without blocking animation."""
    def run_voice():
        try:
            # On Termux, you might need to install 'espeak' via: pkg install espeak
            engine = pyttsx3.init()
            engine.setProperty('rate', 140) 
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass # Silent fail if voice not supported
    thread = threading.Thread(target=run_voice)
    thread.daemon = True
    thread.start()

# --- UTILS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, style="bold white", delay=0.03):
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay + random.uniform(0.005, 0.010)) 
    console.print()

def print_line():
    console.print(SEPARATOR_LINE, style="bold green")

# --- UI COMPONENTS ---
def print_banner():
    banner = """
    ╔═╗╔╗ ┌─┐┬ ┬┌┬┐┌─┐ ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐
    ╠╣ ╠╩╗├─┤│ │ │ │ │ └─┐├─┤├─┤├┬┘├┤ ├┬┘
    ╚  ╚═╝┴ ┴└─┘ ┴ └─┘ └─┘┴ ┴┴ ┴┴└─└─┘┴└─
    """
    console.print(Align.center(banner), style="bold cyan")

def print_info_row(label, value, is_highlighted=False):
    bullet = Text("[", style="bold white")
    bullet.append("•", style="bold white")
    bullet.append("] ", style="bold white")
    
    label_text = Text(f"{label:<{LABEL_WIDTH}}", style="bold yellow")
    arrow = Text("➤ ", style="bold white")
    
    if is_highlighted:
        val_text = Text("[ ", style="bold red")
        val_text.append(value, style="bold white on red")
        val_text.append(" ]", style="bold red")
    else:
        val_text = Text(value, style="bold green")

    console.print(bullet + label_text + arrow + val_text)

def header_section():
    print_line()
    print_info_row("DEVELOPER", "KEN DRICK")
    print_info_row("GITHUB", "RYO GRAHHH")
    print_info_row("VERSION", "1.0.0")
    print_info_row("FACEBOOK", "facebook.com/ryoevisu")
    print_info_row("TOOL'S NAME", "FB AUTO SHARER", is_highlighted=True)
    print_line()

def menu_option(number, letter, description, is_exit=False):
    key_text = Text("[ ", style="bold red")
    key_text.append(f"{number}/{letter}", style="bold white on red")
    key_text.append(" ]", style="bold red")

    if is_exit:
        desc_text = Text(f" {description}", style="bold red")
    else:
        desc_text = Text(f" {description}", style="bold green")

    console.print(key_text + desc_text)

def menu_section_animated():
    options = [
        ("01", "A", "COOKIE TO TOKEN (API)", False),
        ("02", "B", "START AUTO SHARE", False),
        ("03", "C", "JOIN FACEBOOK GROUP", False),
        ("00", "X", "EXIT TOOL", True),
    ]
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
        time.sleep(0.03) 
    print_line()

def animated_input_with_voice(voice_message, prompt_text="CHOICE"):
    speak_async(voice_message)
    
    console.print(" [", style="bold white", end="")
    time.sleep(0.05)
    console.print("➤", style="bold white", end="")
    time.sleep(0.05)
    console.print("]", style="bold white", end="")
    
    for char in f" {prompt_text} ":
        console.print(char, style="bold cyan", end="")
        sys.stdout.flush()
        time.sleep(0.03)
    
    console.print("➤ ", style="bold white", end="")
    return input("").strip()

# --- THE BOXED LOADER ---
def boxed_loader(title, steps):
    speak_async(title)
    
    progress_group = Progress(
        SpinnerColumn(style="bold yellow"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=None, complete_style="cyan", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    )

    panel_group = Panel(
        progress_group,
        title=f"[bold white]{title}[/]",
        border_style="green",
        padding=(1, 2)
    )

    with Live(panel_group, console=console, refresh_per_second=20):
        task_id = progress_group.add_task("Initializing...", total=100)
        current_progress = 0
        step_chunk = 100 / len(steps)
        
        for step_msg, sleep_time in steps:
            progress_group.update(task_id, description=step_msg)
            
            # Sub-progress for smoothness
            chunks = 15
            for _ in range(chunks):
                time.sleep(sleep_time / chunks)
                current_progress += (step_chunk / chunks)
                progress_group.update(task_id, completed=min(current_progress, 100))
            
    time.sleep(0.5)

# --- MAIN LOGIC ---
def main():
    clear()
    speak_async("System initializing.")
    type_print("[*] Loading Modules...", delay=0.04)
    time.sleep(0.5)

    while True:
        clear()
        print_banner()
        header_section()
        menu_section_animated()
        
        try:
            choice = animated_input_with_voice("Please select an option.", "OPTION").upper()

            # --- OPTION 1: COOKIE TO TOKEN (API INTEGRATION) ---
            if choice in ['1', '01', 'A']:
                print()
                cookie = animated_input_with_voice("Enter your Facebook Cookie", "COOKIE")
                
                if not cookie:
                    console.print("\n [bold red][!] Cookie cannot be empty![/]")
                    time.sleep(2)
                    continue

                # The new Loader UI
                steps = [
                    ("Connecting to Kazux API", 1.5),
                    ("Validating Cookie Session", 2.0),
                    ("Extracting Access Token", 2.0),
                    ("Finalizing Data", 1.0)
                ]
                boxed_loader("CONVERTING COOKIE", steps)

                # API LOGIC
                try:
                    url = "https://kazuxapi.vercel.app/tools/cookie-to-token"
                    data = {"cookie": cookie}
                    headers = {
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
                    }
                    
                    response = requests.post(url, json=data, headers=headers)
                    result = response.json()

                    if "access_token" in result:
                        token = result['access_token']
                        
                        # Display result in a nice Panel
                        result_panel = Panel(
                            f"[bold yellow]Access Token Generated Successfully![/]\n\n[bold green]{token}[/]",
                            title="[bold white]SUCCESS[/]",
                            border_style="green"
                        )
                        console.print(result_panel)
                        speak_async("Token generated successfully.")
                        
                        # Optional: Save to file
                        with open("token.txt", "w") as f:
                            f.write(token)
                        console.print("\n[dim]Token saved to token.txt[/]")
                        
                    else:
                        err_msg = result.get('error', 'Unknown Error')
                        console.print(f"\n [bold red][!] Failed: {err_msg}[/]")
                        speak_async("Failed to generate token.")

                except Exception as e:
                    console.print(f"\n [bold red][!] API Error: {e}[/]")

                input("\n Press Enter to return...")

            # --- OPTION 2: AUTO SHARE (Placeholder for future logic) ---
            elif choice in ['2', '02', 'B']:
                print()
                steps = [
                    ("Checking Saved Token", 1.0),
                    ("Loading Share Targets", 1.5),
                    ("Starting Spammer Engine", 2.0)
                ]
                boxed_loader("STARTING AUTO SHARE", steps)
                console.print(Align.center("\n[bold black on green] ACTIVE [/] [bold green]Auto Share is running...[/]"))
                input("\n Press Enter to stop...")

            # --- EXIT ---
            elif choice in ['0', '00', 'X']:
                print()
                speak_async("Shutting down system.")
                type_print("[!] Exiting...", style="bold red")
                time.sleep(1)
                sys.exit()
            else:
                print()
                console.print("\n [bold red][!] Invalid Selection[/]")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print()
            sys.exit()

if __name__ == "__main__":
    main()
