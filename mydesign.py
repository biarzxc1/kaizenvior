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
    from rich.layout import Layout
    from rich.align import Align
    from rich import box
    import pyttsx3
except ImportError:
    os.system("pip install rich pyttsx3")
    print("\n[!] Libraries installed. Please restart the tool.")
    sys.exit()

# --- CONFIGURATION ---
console = Console()
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
VIP_GOLD = "#FFD700"
VIP_RED = "#FF0000"
ADMIN_GREEN = "#00FF00"

# --- SOUND MANAGER (TERMUX FIX) ---
class SoundManager:
    def __init__(self):
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 140) # Very slow, clear voice
            self.engine.setProperty('volume', 1.0)
        except:
            self.engine = None

    def speak(self, text):
        """Runs speech in a non-blocking thread."""
        def _run():
            if self.engine:
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except:
                    pass
            else:
                # Fallback for Termux if pyttsx3 fails (try native TTS)
                try:
                    subprocess.run(["termux-tts-speak", text], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                except:
                    pass # Silent fail if no audio capability

        t = threading.Thread(target=_run)
        t.daemon = True
        t.start()

sound = SoundManager()

# --- UTILITIES ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, style="bold white", speed=0.06, sound_effect=False):
    """
     dramatic slow typing with optional beep simulation
    """
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0.01, 0.05)) # Randomize delay for human feel
    console.print()

def print_line():
    console.print(SEPARATOR_LINE, style=f"bold {ADMIN_GREEN}")

# --- VIP UI ELEMENTS ---

def matrix_rain_effect():
    """Simulates a 'Connecting' hex dump effect."""
    chars = "ABCDEF0123456789"
    sound.speak("Establishing secure connection...")
    
    with Live(console=console, refresh_per_second=15) as live:
        for _ in range(25): # Duration of rain
            line = "".join(random.choice(chars) for _ in range(50))
            live.update(Text(line, style="dim green"))
            time.sleep(0.05)
    clear()

def print_banner():
    banner = """
    [bold cyan]╔═╗╔╗ ┌─┐┬ ┬┌┬┐┌─┐ ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐[/]
    [bold cyan]╠╣ ╠╩╗├─┤│ │ │ │ │ └─┐├─┤├─┤├┬┘├┤ ├┬┘[/]
    [bold cyan]╚  ╚═╝┴ ┴└─┘ ┴ └─┘ └─┘┴ ┴┴ ┴┴└─└─┘┴└─[/]
    """
    console.print(Align.center(banner))

def print_info_row(label, value, is_highlighted=False):
    # Fancy VIP layout for rows
    bullet = Text(" [", style="bold white")
    bullet.append("•", style=f"bold {VIP_GOLD}")
    bullet.append("] ", style="bold white")
    
    label_text = Text(f"{label:<13}", style=f"bold {VIP_GOLD}")
    arrow = Text("➤ ", style="bold white")
    
    if is_highlighted:
        val_text = Text("[ ", style=f"bold {VIP_RED}")
        val_text.append(value, style="bold white on red")
        val_text.append(" ]", style=f"bold {VIP_RED}")
    else:
        val_text = Text(value, style=f"bold {ADMIN_GREEN}")

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
    # Button Style
    key_style = f"bold white on {VIP_RED}"
    key_text = Text(" [ ", style=f"bold {VIP_RED}")
    key_text.append(f"{number}/{letter}", style=key_style)
    key_text.append(" ]", style=f"bold {VIP_RED}")

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
        time.sleep(0.15) # Increased delay for dramatic effect
    print_line()

# --- SYSTEM HACKING LOADER ---
def admin_loader(task_name, steps):
    """
    A complex, multi-stage loader with a box and progress.
    """
    sound.speak(f"{task_name} initialized.")
    
    # Custom Progress Bar Columns
    progress = Progress(
        SpinnerColumn(style=f"bold {VIP_GOLD}"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=None, complete_style=f"{VIP_GOLD}", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn()
    )

    panel = Panel(
        progress,
        title=f"[bold white]SYSTEM PROCESS: {task_name}[/]",
        border_style=f"{VIP_GOLD}",
        padding=(1, 2)
    )

    with Live(panel, console=console, refresh_per_second=10):
        task_id = progress.add_task("Waiting...", total=100)
        
        chunk_size = 100 / len(steps)
        current_val = 0

        for step_text, delay in steps:
            progress.update(task_id, description=f"[bold white]{step_text}...")
            sound.speak(step_text)
            
            # Sub-loop for smooth bar filling
            ticks = 30
            for _ in range(ticks):
                time.sleep(delay / ticks)
                current_val += (chunk_size / ticks)
                progress.update(task_id, completed=min(current_val, 100))
            
            # Pause between steps
            time.sleep(0.5)

    console.print(f"[bold green on black]   ✔ PROCESS COMPLETED: {task_name}   [/]")
    sound.speak("Process completed.")
    time.sleep(1)

# --- INPUT HANDLING ---
def get_input_animated():
    sound.speak("Please enter your command.")
    
    # Prompt construction
    console.print(" [", style="bold white", end="")
    time.sleep(0.1)
    console.print("➤", style="bold white", end="")
    time.sleep(0.1)
    console.print("]", style="bold white", end="")
    
    slow_type(" CHOICE ", style="bold cyan", speed=0.1)
    console.print("➤ ", style="bold white", end="")
    
    return input("").upper().strip()

# --- MAIN ---
def main():
    clear()
    sound.speak("Welcome to F B Auto Sharer. Admin Access Granted.")
    
    # Intro Sequence
    matrix_rain_effect()
    slow_type("[*] Authenticating User...", style="dim white", speed=0.05)
    time.sleep(1)
    slow_type("[*] Access Granted: VIP MEMBER", style=f"bold {VIP_GOLD}", speed=0.05)
    time.sleep(1)

    while True:
        clear()
        print_banner()
        header_section()
        show_menu_animated()
        
        try:
            choice = get_input_animated()

            if choice in ['1', '01', 'A']:
                print()
                steps = [
                    ("Injecting Payload", 3.0),
                    ("Bypassing Security", 2.5),
                    ("Extracting Cookies", 3.0),
                    ("Connecting to Graph API", 2.0),
                    ("Starting Auto Share", 1.5)
                ]
                admin_loader("AUTO SHARE V.1.0", steps)
                input("\nPress Enter to return...")

            elif choice in ['2', '02', 'B']:
                print()
                steps = [
                    ("Scanning Group Lists", 2.0),
                    ("Filtering Public Groups", 2.0),
                    ("Joining Target IDs", 3.0)
                ]
                admin_loader("GROUP JOINER", steps)

            elif choice in ['0', '00', 'X']:
                print()
                sound.speak("System shutting down.")
                slow_type("[!] Terminating Session...", style="bold red")
                time.sleep(2)
                sys.exit()
                
            else:
                sound.speak("Access Denied. Invalid command.")
                console.print(Panel("[bold red]INVALID SELECTION[/]", border_style="red"))
                time.sleep(1.5)

        except KeyboardInterrupt:
            print()
            sys.exit()

if __name__ == "__main__":
    main()
