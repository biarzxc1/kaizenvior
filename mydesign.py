import os
import sys
import time
import threading
import random
import subprocess

# --- AUTO-INSTALL LIBRARIES ---
try:
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.align import Align
    import pyttsx3
except ImportError:
    os.system("pip install rich pyttsx3")
    print("\n[!] Libraries installed. Restarting...")
    # Rerun script automatically
    os.execv(sys.executable, ['python'] + sys.argv)

# --- CONFIGURATION ---
console = Console()
# Colors from the screenshot
# The screenshot uses standard terminal bright green, red, yellow.
COLOR_ACCENT = "bold green"     # Main Text
COLOR_LABEL = "bold yellow"     # Labels
COLOR_TAG = "bold red"          # [≈] Brackets
COLOR_VALUE = "bold green"      # Values like Name
COLOR_VALUE_VIP = "bold blue"   # "PREMIUM" value
COLOR_WARN = "bold white on green" # The "Airplane Mode" line background

# --- SOUND MANAGER ---
class SoundManager:
    def __init__(self):
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 140)
            self.engine.setProperty('volume', 1.0)
        except:
            self.engine = None

    def speak(self, text):
        def _run():
            if self.engine:
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except:
                    pass
            else:
                try:
                    subprocess.run(["termux-tts-speak", text], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                except:
                    pass
        t = threading.Thread(target=_run)
        t.daemon = True
        t.start()

sound = SoundManager()

# --- UTILITIES ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, style="bold white", speed=0.04):
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0.005, 0.01)) 
    console.print()

# --- UI ELEMENTS ---

def print_banner():
    # Big blocky text similar to "AKASH"
    banner = r"""
 [bold green]
  █████╗ ██╗   ██╗████████╗ ██████╗ 
 ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
 ███████║██║   ██║   ██║   ██║   ██║
 ██╔══██║██║   ██║   ██║   ██║   ██║
 ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
 ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
 [/] [bold green]V/3.9[/]
    """
    console.print(Align.center(banner))

def print_line():
    console.print("[bold green]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")

def info_line(symbol, label, value, value_color="bold green"):
    """
    Format: [≈] OWNER    : AKASH_ON_FIRE
    """
    # 1. The Symbol [≈]
    # Red brackets, Red tilde
    sym_text = Text("[", style="bold red")
    sym_text.append(symbol, style="bold red")
    sym_text.append("] ", style="bold red")
    
    # 2. Label (Yellow) padded
    # We use a fixed width to align the colons
    label_text = Text(f"{label:<10}", style=COLOR_LABEL)
    
    # 3. Colon (Red)
    colon = Text(": ", style="bold red")
    
    # 4. Value
    val_text = Text(str(value), style=value_color)
    
    console.print(sym_text + label_text + colon + val_text)

def header_section_akash_style():
    print_line()
    
    # Section 1: User Info (using ≈)
    info_line("≈", "OWNER", "KEN DRICK") # Your name
    info_line("≈", "TOOL TYPE", "AUTO_SHARE")
    info_line("≈", "VERSION", "PREMIUM", value_color="bold blue") # Blue for premium
    info_line("≈", "WHATSAPP", "+1234567890", value_color="bold red")
    
    print_line()
    
    # Section 2: Sim Info (using =)
    info_line("=", "SIM CODE", "019")
    info_line("=", "TOTAL UID", "9999")
    
    # Section 3: Warning Line (Green Background)
    console.print("[bold green][=] TURN [ON/OFF] AIRPLANE MODE EVERY 3 MIN[/]")
    
    print_line()

def menu_option(number, letter, description, is_exit=False):
    """
    Keeps your VIP buttons but fits the theme.
    """
    key_style = "bold white on red"
    key_text = Text("[ ", style="bold red")
    key_text.append(f"{number}/{letter}", style=key_style)
    key_text.append(" ]", style="bold red")

    if is_exit:
        desc_text = Text(f" {description}", style="bold red")
    else:
        desc_text = Text(f" {description}", style="bold green")
    
    console.print(key_text + desc_text)

def show_menu_animated():
    options = [
        ("01", "A", "START AUTO SHARE", False),
        ("02", "B", "JOIN FB GROUP", False),
        ("03", "C", "JOIN FACEBOOK", False),
        ("04", "D", "FOLLOW GITHUB", False),
        ("00", "X", "BACK TO MAIN MENU", True),
    ]
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
        time.sleep(0.05)
    print_line()

# --- LOADERS (VIP STYLE) ---
def admin_loader(task_name, steps):
    sound.speak(f"Starting {task_name}")
    
    progress = Progress(
        SpinnerColumn(style="bold yellow"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=None, complete_style="green", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    
    panel = Panel(progress, title=f"[bold white]{task_name}[/]", border_style="green", padding=(1, 2))
    
    with Live(panel, console=console, refresh_per_second=10):
        task_id = progress.add_task("Running...", total=100)
        chunk = 100 / len(steps)
        curr = 0
        
        for step, delay in steps:
            progress.update(task_id, description=step)
            # sound.speak(step) # Optional: uncomment if too talkative
            
            ticks = 20
            for _ in range(ticks):
                time.sleep(delay/ticks)
                curr += chunk/ticks
                progress.update(task_id, completed=min(curr, 100))
    
    console.print(f"[bold green on black] [OK] PROCESS COMPLETED: {task_name} [/]")
    time.sleep(1)

# --- NEW INPUT STYLE ---
def get_input_fixed():
    """
    Fixed input: [?] CHOICE >
    """
    sound.speak("Waiting for choice.")
    
    # 1. [?]
    console.print("[", style="bold green", end="")
    console.print("?", style="bold yellow", end="")
    console.print("] ", style="bold green", end="")
    
    # 2. CHOICE
    console.print("CHOICE ", style="bold white", end="")
    
    # 3. >
    console.print("> ", style="bold green", end="")
    
    return input("").upper().strip()

# --- MAIN ---
def main():
    clear()
    # Matrix effect (VIP feature)
    sound.speak("Welcome Ken Drick.")
    
    while True:
        clear()
        print_banner()
        header_section_akash_style() # New UI Style
        show_menu_animated()
        
        try:
            choice = get_input_fixed() # New Input Style

            if choice in ['1', '01', 'A']:
                print()
                steps = [
                    ("Injecting Cookies...", 2.0),
                    ("Bypassing Security...", 2.0),
                    ("Auto Share Started...", 1.5)
                ]
                admin_loader("AUTO SHARE", steps)
                input("\n Press Enter...")

            elif choice in ['2', '02', 'B']:
                print()
                steps = [("Fetching Groups...", 2.0), ("Joining...", 2.0)]
                admin_loader("GROUP JOINER", steps)

            elif choice in ['0', '00', 'X']:
                print()
                sound.speak("Shutting down.")
                sys.exit()
                
            else:
                console.print("\n[bold red][!] INVALID SELECTION[/]")
                time.sleep(1)

        except KeyboardInterrupt:
            print()
            sys.exit()

if __name__ == "__main__":
    main()
