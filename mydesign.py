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
            engine = pyttsx3.init()
            engine.setProperty('rate', 150) # Slightly slower for clarity
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    thread = threading.Thread(target=run_voice)
    thread.daemon = True
    thread.start()

# --- UTILS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, style="bold white", delay=0.04):
    """
    Smoother, slightly slower typing effect.
    """
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        # Add a tiny random variation to make it feel like human typing
        time.sleep(delay + random.uniform(0.005, 0.015)) 
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
    console.print(banner, style="bold cyan")

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
        ("01", "A", "START AUTO SHARE", False),
        ("02", "B", "JOIN FB GROUP", False),
        ("03", "C", "JOIN FACEBOOK", False),
        ("04", "D", "FOLLOW GITHUB", False),
        ("00", "X", "BACK TO MAIN MENU", True),
    ]
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
        time.sleep(0.04) # Slower cascade for smoothness
    print_line()

def animated_input_with_voice(voice_message):
    speak_async(voice_message)
    
    console.print(" [", style="bold white", end="")
    time.sleep(0.05)
    console.print("➤", style="bold white", end="")
    time.sleep(0.05)
    console.print("]", style="bold white", end="")
    
    # Slower typing for "CHOICE" to look cinematic
    for char in " CHOICE ":
        console.print(char, style="bold cyan", end="")
        sys.stdout.flush()
        time.sleep(0.05)
    
    console.print("➤ ", style="bold white", end="")
    return input("").upper().strip()

# --- THE NEW BOXED LOADER ---
def boxed_loader(title, steps):
    """
    Displays a nice Box (Panel) with a Progress Bar inside.
    'steps' is a list of (message, duration) tuples.
    """
    speak_async(title)
    
    # Define the progress bar structure
    progress_group = Progress(
        SpinnerColumn(style="bold yellow"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=None, complete_style="cyan", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    )

    # Wrap it in a Panel
    panel_group = Panel(
        progress_group,
        title=f"[bold white]{title}[/]",
        border_style="green",
        padding=(1, 2)
    )

    # Create a Live display
    with Live(panel_group, console=console, refresh_per_second=20):
        # Add a single task to the progress bar
        task_id = progress_group.add_task("Initializing...", total=100)
        
        current_progress = 0
        step_chunk = 100 / len(steps)
        
        for step_msg, sleep_time in steps:
            # Update text description
            progress_group.update(task_id, description=step_msg)
            
            # Speak the specific step if it's long enough
            if sleep_time > 1:
                speak_async(step_msg)

            # Smoothly fill the bar for this step
            # We break the sleep_time into tiny chunks to animate the bar smoothly
            chunks = 20
            for _ in range(chunks):
                time.sleep(sleep_time / chunks)
                current_progress += (step_chunk / chunks)
                progress_group.update(task_id, completed=min(current_progress, 100))
            
            time.sleep(0.2) # Small pause between steps

        # Ensure it hits 100% at the end
        progress_group.update(task_id, completed=100, description="[bold white]COMPLETED")
        time.sleep(0.5)

# --- MAIN LOGIC ---
def main():
    clear()
    speak_async("Welcome to F B Auto Sharer.")
    type_print("[*] Loading System Resources...", delay=0.04)
    time.sleep(0.8)

    while True:
        clear()
        print_banner()
        header_section()
        menu_section_animated()
        
        try:
            choice = animated_input_with_voice("Please select an option.")

            if choice in ['1', '01', 'A']:
                print()
                
                # --- NEW BOXED LOADER SEQUENCE ---
                steps = [
                    ("Connecting to Server", 1.5),
                    ("Validating User Cookies", 2.0),
                    ("Fetching Facebook Groups", 2.0),
                    ("Preparing Auto Share Engine", 1.5),
                    ("Starting Process", 1.0)
                ]
                
                boxed_loader("INITIALIZING AUTO SHARE", steps)
                
                console.print(Align.center("\n[bold black on green] SUCCESS [/] [bold green]Auto Share Running in Background...[/]"))
                speak_async("Process started successfully.")
                input("\n Press Enter to return...")
                
            elif choice in ['2', '02', 'B']:
                print()
                steps = [("Resolving Group Links", 2.0), ("Opening Browser", 1.0)]
                boxed_loader("JOINING GROUPS", steps)
                time.sleep(1)

            elif choice in ['0', '00', 'X']:
                print()
                speak_async("Goodbye.")
                type_print("[!] Shutting down...", style="bold red")
                time.sleep(1)
                sys.exit()
            else:
                print()
                speak_async("Invalid Choice.")
                console.print("\n [bold red][!] Invalid Selection[/]")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print()
            sys.exit()

if __name__ == "__main__":
    main()
