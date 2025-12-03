import os
import sys
import subprocess
import time
import threading
import random

# --- AUTO-INSTALLER SECTION ---
def install_requirements():
    requirements = [("rich", "rich"), ("pyttsx3", "pyttsx3")]
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
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.layout import Layout
from rich.align import Align
from rich.table import Table

# Initialize Console
console = Console()

# --- CONFIGURATION ---
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- ADVANCED AUDIO ENGINE (Termux Compatible) ---
def speak(text):
    """
    Tries to use Termux native TTS first.
    Falls back to pyttsx3 if on PC/Windows.
    Runs in a thread to not block the animation.
    """
    def run_voice():
        # Check if running in Termux with API installed
        if os.path.exists("/data/data/com.termux/files/usr/bin/termux-tts-speak"):
            os.system(f"termux-tts-speak '{text}'")
        else:
            # Fallback for Windows/PC
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 140) 
                engine.setProperty('volume', 1.0)
                engine.say(text)
                engine.runAndWait()
            except:
                pass # Fail silently if no audio engine found

    thread = threading.Thread(target=run_voice)
    thread.daemon = True
    thread.start()

# --- UTILS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, style="bold white", speed=0.04):
    """
    Cinematic typing effect.
    """
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        # Random variance makes it feel like "hacking"
        time.sleep(speed + random.uniform(0.01, 0.03)) 
    console.print()

def print_line():
    console.print(SEPARATOR_LINE, style="bold dim green")

# --- UI COMPONENTS ---
def print_banner():
    # Added gradients or colors to banner
    banner = """
    ╔═╗╔╗ ┌─┐┬ ┬┌┬┐┌─┐ ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐
    ╠╣ ╠╩╗├─┤│ │ │ │ │ └─┐├─┤├─┤├┬┘├┤ ├┬┘
    ╚  ╚═╝┴ ┴└─┘ ┴ └─┘ └─┘┴ ┴┴ ┴┴└─└─┘┴└─
    """
    console.print(Align.center(banner), style="bold cyan")
    time.sleep(0.5)

def print_info_row(label, value, is_highlighted=False):
    # Setup the table structure for perfect alignment
    grid = Table.grid(expand=True)
    grid.add_column(style="bold white", width=3)
    grid.add_column(style="bold yellow", width=15)
    grid.add_column(style="bold white", width=3)
    grid.add_column(style="bold green")

    if is_highlighted:
        val_render = Text(f" {value} ", style="bold white on red")
    else:
        val_render = Text(value, style="bold green")

    grid.add_row("[•]", label, "➤", val_render)
    console.print(grid)
    time.sleep(0.1) # Short delay between rows for effect

def header_section():
    print_line()
    print_info_row("DEVELOPER", "KEN DRICK")
    print_info_row("GITHUB", "RYO GRAHHH")
    print_info_row("VERSION", "1.0.0")
    print_info_row("FACEBOOK", "facebook.com/ryoevisu")
    print_info_row("TOOL'S NAME", "FB AUTO SHARER", is_highlighted=True)
    print_line()

def menu_option(number, letter, description, is_exit=False):
    grid = Table.grid(expand=True)
    grid.add_column(width=10) # Indent
    grid.add_column()

    key_text = Text("[ ", style="bold red")
    key_text.append(f"{number}/{letter}", style="bold white on red")
    key_text.append(" ]", style="bold red")

    if is_exit:
        desc_text = Text(f" {description}", style="bold red")
    else:
        desc_text = Text(f" {description}", style="bold green")

    grid.add_row("", key_text + desc_text)
    console.print(grid)
    time.sleep(0.2) # Slower cascade for that "Menu Loading" feel

def menu_section_animated():
    options = [
        ("01", "A", "START AUTO SHARE", False),
        ("02", "B", "JOIN FB GROUP", False),
        ("03", "C", "JOIN FACEBOOK", False),
        ("04", "D", "FOLLOW GITHUB", False),
        ("00", "X", "BACK TO MAIN MENU", True),
    ]
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
    print_line()

def animated_input(prompt_text):
    speak(prompt_text)
    
    console.print("\n [", style="bold white", end="")
    time.sleep(0.1)
    console.print("?", style="bold yellow", end="")
    time.sleep(0.1)
    console.print("] ", style="bold white", end="")
    
    for char in prompt_text:
        console.print(char, style="bold cyan", end="")
        sys.stdout.flush()
        time.sleep(0.03)
        
    console.print(" ➤ ", style="bold blink white", end="")
    return input("").upper().strip()

# --- VIP ADMIN LOADER ---
def vip_loader(title, processes):
    """
    A high-end, boxed loader that looks like an Admin/VIP tool.
    processes = list of ("Text to display", duration_seconds)
    """
    speak(f"{title} initiated.")
    
    # 1. Setup the Progress Bar
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn("dots", style="bold yellow"),
        BarColumn(bar_width=None, complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    
    task_id = job_progress.add_task(f"[bold cyan]Initializing...", total=100)

    # 2. Create the Layout
    # We use a Panel to wrap the progress bar to give it that "Boxed" look
    panel = Panel(
        job_progress,
        title=f"[bold yellow]♕ {title} ♕[/]",
        subtitle="[bold dim white]Processing Request...[/]",
        border_style="green",
        padding=(1, 2)
    )

    # 3. Run the Live Display
    with Live(panel, console=console, refresh_per_second=12):
        step_value = 100 / len(processes)
        current_val = 0
        
        for text, duration in processes:
            # Update text
            job_progress.update(task_id, description=f"[bold white]{text}")
            
            # Speak occasional steps (every other step to avoid overlap)
            if random.choice([True, False]): 
                speak(text)

            # Smooth bar fill logic
            chunks = int(duration * 10) # 10 updates per second
            for _ in range(chunks):
                time.sleep(0.1)
                current_val += (step_value / chunks)
                job_progress.update(task_id, completed=min(current_val, 100))
        
        # Finish
        job_progress.update(task_id, description="[bold green]COMPLETED", completed=100)
        time.sleep(0.8)
        speak("Operation completed.")

# --- MAIN LOGIC ---
def main():
    clear()
    speak("System starting. Welcome back, Administrator.")
    slow_type("[*] ESTABLISHING SECURE CONNECTION...", speed=0.05)
    time.sleep(1.0) # Dramatic pause

    while True:
        clear()
        print_banner()
        header_section()
        menu_section_animated()
        
        try:
            choice = animated_input("ENTER SELECTION")

            if choice in ['1', '01', 'A']:
                print()
                # VIP Loader Steps
                steps = [
                    ("Connecting to Facebook API...", 2.0),
                    ("Bypassing Security Token...", 1.5),
                    ("Injecting Cookies...", 1.5),
                    ("Extracting Target Groups...", 2.0),
                    ("Starting Auto Share Engine...", 1.0)
                ]
                vip_loader("AUTO SHARE PROTOCOL", steps)
                
                # Result screen
                console.print(Panel(Align.center("[bold green]Background Task Running Successfully[/]"), border_style="bold green"))
                speak("Task running in background.")
                input("\n Press Enter to return...")
                
            elif choice in ['2', '02', 'B']:
                print()
                steps = [
                    ("Resolving DNS...", 1.0),
                    ("Fetching Group IDs...", 1.5), 
                    ("Opening Secure Browser...", 1.0)
                ]
                vip_loader("GROUP JOINER", steps)
                time.sleep(1)

            elif choice in ['3', '03', 'C']:
                # Example for placeholder
                print()
                steps = [("Redirecting...", 1.5)]
                vip_loader("REDIRECTING", steps)

            elif choice in ['0', '00', 'X']:
                print()
                speak("Shutting down system.")
                slow_type(">> CLOSING SESSIONS...", speed=0.06)
                time.sleep(0.5)
                slow_type(">> GOODBYE.", style="bold red")
                sys.exit()
            else:
                print()
                speak("Error. Invalid input.")
                console.print(Panel("[bold red]ACCESS DENIED: Invalid Selection[/]", border_style="red"))
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            print()
            sys.exit()

if __name__ == "__main__":
    main()
