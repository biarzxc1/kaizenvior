import os
import sys
import subprocess
import time
import threading
import random
import string

# --- AUTO-INSTALLER ---
def install_requirements():
    # We only need rich for the UI. Audio is handled via system commands now.
    try:
        import rich
    except ImportError:
        print("[!] Installing libraries...")
        os.system("pip install rich")
        os.system('cls' if os.name == 'nt' else 'clear')

install_requirements()

# --- IMPORTS ---
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box
from rich.align import Align
from rich.layout import Layout

# Initialize Console
console = Console()

# --- AUDIO ENGINE (TERMUX FIXED) ---
def speak(text):
    """
    Universal speak function.
    1. Tries Android native TTS (Termux).
    2. Falls back to pyttsx3 (PC).
    3. Fails silently if neither works.
    """
    def _speak_thread():
        # METHOD 1: TERMUX / ANDROID
        if os.path.exists("/data/data/com.termux/files/usr/bin/termux-tts-speak"):
            try:
                subprocess.run(["termux-tts-speak", text], check=False)
                return
            except:
                pass
        
        # METHOD 2: PC (pyttsx3)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 140) # Slow and clear
            engine.say(text)
            engine.runAndWait()
        except:
            # If no audio engine found, just do nothing (don't crash)
            pass

    # Run in background so animations don't freeze
    t = threading.Thread(target=_speak_thread)
    t.daemon = True
    t.start()

# --- ANIMATION UTILS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, style="bold white", speed=0.04):
    """
    Cinematic typing effect.
    """
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        # Randomize delay slightly for "human" feel
        time.sleep(speed + random.uniform(0.01, 0.03)) 
    console.print()

def decrypt_effect(duration=1.5):
    """
    Shows random matrix characters like it's decrypting data.
    """
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    end_time = time.time() + duration
    
    with Live(refresh_per_second=15) as live:
        while time.time() < end_time:
            random_str = "".join(random.choice(chars) for _ in range(40))
            live.update(Text(f"DECRYPTING: {random_str}", style="bold green"))
            time.sleep(0.05)

# --- UI COMPONENTS ---
def print_banner():
    # Double border banner for VIP look
    banner_text = """
    ╔═╗╔╗ ┌─┐┬ ┬┌┬┐┌─┐ ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐
    ╠╣ ╠╩╗├─┤│ │ │ │ │ └─┐├─┤├─┤├┬┘├┤ ├┬┘
    ╚  ╚═╝┴ ┴└─┘ ┴ └─┘ └─┘┴ ┴┴ ┴┴└─└─┘┴└─
    """
    panel = Panel(
        Align.center(banner_text),
        border_style="bold cyan",
        box=box.DOUBLE,
        title="[bold yellow]★ VIP EDITION ★[/]",
        subtitle="[bold red]SYSTEM ACCESS: GRANTED[/]"
    )
    console.print(panel)

def print_info():
    # Using a Table or nicely formatted text inside a box
    info = """
 [bold white][•][/] [bold yellow]DEVELOPER  [/] ➤ [bold green]KEN DRICK[/]
 [bold white][•][/] [bold yellow]GITHUB     [/] ➤ [bold green]RYO GRAHHH[/]
 [bold white][•][/] [bold yellow]VERSION    [/] ➤ [bold green]1.0.0 (PREMIUM)[/]
 [bold white][•][/] [bold yellow]FACEBOOK   [/] ➤ [bold green]facebook.com/ryoevisu[/]
 [bold white][•][/] [bold yellow]TOOL'S NAME[/] ➤ [bold white on red] FB AUTO SHARER [/]
    """
    console.print(Panel(info.strip(), border_style="bold green", box=box.ROUNDED))

def menu_option(key, desc, is_exit=False):
    style_bracket = "bold red"
    style_key = "bold white on red"
    style_desc = "bold green" if not is_exit else "bold red"
    
    # Format: [ 01/A ] DESCRIPTION
    return f"[{style_bracket}][ [{style_key}]{key}[/{style_key}] ][/{style_bracket}] [{style_desc}]{desc}[/{style_desc}]"

def show_menu():
    menu_text = "\n".join([
        menu_option("01/A", "START AUTO SHARE"),
        menu_option("02/B", "JOIN FB GROUP"),
        menu_option("03/C", "JOIN FACEBOOK"),
        menu_option("04/D", "FOLLOW GITHUB"),
        "",
        menu_option("00/X", "BACK TO MAIN MENU", is_exit=True)
    ])
    
    # Print menu with a nice fade-in effect simulation (line by line)
    console.print(Panel(menu_text, title="[bold white]MENU SELECTION[/]", border_style="bold yellow", box=box.HEAVY_EDGE))

def vip_loader(title, steps):
    """
    A high-end 'Admin' style loader with double borders and slow progress.
    """
    speak(f"Starting {title} protocol.")
    
    # Custom Progress Bar Columns
    progress = Progress(
        SpinnerColumn(style="bold yellow"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=None, complete_style="bold green", finished_style="bold green"),
        TextColumn("[bold white]{task.percentage:>3.0f}%"),
        expand=True
    )

    # Box layout
    panel = Panel(
        progress,
        title=f"[bold yellow]★ {title} ★[/]",
        border_style="bold yellow",
        box=box.DOUBLE,
        padding=(1, 2)
    )

    with Live(panel, console=console, refresh_per_second=10):
        task_id = progress.add_task("Initializing...", total=100)
        
        # Calculate chunks based on steps
        chunk_size = 100 / len(steps)
        current_val = 0

        for description, delay in steps:
            # Update text
            progress.update(task_id, description=f"[bold yellow]>>[/] {description}")
            speak(description)
            
            # Slow fill animation
            # We slice the delay into tiny pieces to make the bar move smoothly
            frames = int(delay * 20) # 20 updates per second
            for _ in range(frames):
                time.sleep(0.05)
                current_val += (chunk_size / frames)
                progress.update(task_id, completed=min(current_val, 100))
            
            # Extra pause after a step finishes
            time.sleep(0.5)
            
        progress.update(task_id, description="[bold green]ACCESS GRANTED[/]", completed=100)
        time.sleep(1)

def input_animation(prompt_text):
    """
    Animated Input box with Voice.
    """
    speak("Please enter your choice.")
    
    console.print(f"\n [bold white][[bold yellow]?[/bold yellow]] {prompt_text}", end="")
    
    # Blinking cursor simulation before typing
    for _ in range(3):
        console.print(" .", style="bold green", end="")
        sys.stdout.flush()
        time.sleep(0.3)
    
    console.print("\n [bold white]➤ [/]", end="")
    return input().upper().strip()

# --- MAIN ---
def main():
    clear()
    
    # 1. Fake Login / Boot Sequence
    speak("System Booting. Please Wait.")
    type_print(" [ SYSTEM BOOT SEQUENCE INITIATED ]", style="bold green", speed=0.03)
    time.sleep(0.5)
    decrypt_effect(duration=2.0) # Matrix effect
    
    while True:
        clear()
        print_banner()
        print_info()
        
        # Delay before showing menu for dramatic effect
        time.sleep(0.5)
        show_menu()
        
        try:
            choice = input_animation("WAITING FOR COMMAND")

            if choice in ['1', '01', 'A']:
                print()
                # VIP LOADER
                steps = [
                    ("Connecting to Facebook API...", 3.0),
                    ("Bypassing Security Token...", 4.0), # Longer delay
                    ("Extracting Cookies...", 3.0),
                    ("Injecting Auto Share Script...", 2.5),
                    ("Finalizing Process...", 2.0)
                ]
                vip_loader("AUTO SHARE V.1", steps)
                
                speak("Process Successful.")
                console.print(Panel(Align.center("[bold green]✓ AUTO SHARE ACTIVE[/]"), style="bold green"))
                input("\n [bold white]Press Enter to continue...[/]")
                
            elif choice in ['2', '02', 'B']:
                print()
                steps = [
                    ("Fetching Group Database...", 3.0),
                    ("Optimizing Search...", 2.0)
                ]
                vip_loader("GROUP JOINER", steps)
                
            elif choice in ['0', '00', 'X']:
                print()
                speak("Shutting down system.")
                type_print(" [!] TERMINATING SESSION...", style="bold red", speed=0.08)
                time.sleep(1)
                sys.exit()
                
            else:
                speak("Access Denied.")
                console.print("\n [bold red on white] X INVALID COMMAND [/]", justify="center")
                time.sleep(1.5)

        except KeyboardInterrupt:
            print()
            sys.exit()

if __name__ == "__main__":
    main()
