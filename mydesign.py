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
    from rich import box
    from rich.align import Align
    import pyttsx3
except ImportError:
    os.system("pip install rich pyttsx3")
    print("\n[!] Libraries installed. Please restart the tool.")
    sys.exit()

# --- CONFIGURATION ---
console = Console()

# Colors from the screenshot
C_GREEN = "#00FF00"   # Neon Green
C_YELLOW = "#FFFF00"  # Yellow
C_RED = "#FF0000"     # Red
C_PURPLE = "#FF00FF"  # Purple/Magenta
C_BLUE = "#00FFFF"    # Cyan/Blue
C_WHITE = "#FFFFFF"   # White

SEPARATOR_LINE = Text("━" * 60, style=f"bold {C_GREEN}")

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
                except: pass
            else:
                try:
                    subprocess.run(["termux-tts-speak", text], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                except: pass
        t = threading.Thread(target=_run)
        t.daemon = True
        t.start()

sound = SoundManager()

# --- UTILITIES ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, style=f"bold {C_WHITE}", speed=0.04):
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0.01, 0.03))
    console.print()

# --- UI ELEMENTS (MATCHING PHOTO) ---

def print_banner():
    # A similar blocky/pixelated banner style
    banner_text = """
███████╗██████╗     █████╗ ██╗   ██╗████████╗██████╗ 
██╔════╝██╔══██╗    ██╔══██╗██║   ██║╚══██╔══╝██╔══██╗
█████╗  ██████╔╝    ███████║██║   ██║   ██║   ██║  ██║
██╔══╝  ██╔══██╗    ██╔══██║██║   ██║   ██║   ██║  ██║
██║     ██████╔╝    ██║  ██║╚██████╔╝   ██║   ██████╔╝
╚═╝     ╚═════╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═════╝ 
    """
    # Add version to the right
    banner_lines = banner_text.strip().split('\n')
    banner_lines[-1] += f"  {C_GREEN}V/3.9[/]"
    
    for line in banner_lines:
        console.print(line, style=f"bold {C_GREEN}", justify="center")

def print_header_1(key, value, val_color=C_YELLOW):
    """Style: [≈] KEY : VALUE"""
    t = Text("", style="bold")
    t.append("[≈] ", style=C_PURPLE)
    t.append(f"{key:<10}", style=C_YELLOW)
    t.append(" : ", style=C_RED)
    t.append(value, style=val_color)
    console.print(t)

def print_header_2(key, value):
    """Style: [=] KEY : VALUE"""
    t = Text("", style="bold")
    t.append("[=] ", style=C_GREEN)
    t.append(f"{key:<10}", style=C_GREEN)
    t.append(" : ", style=C_WHITE)
    t.append(value, style=C_GREEN)
    console.print(t)

def header_section():
    console.print(SEPARATOR_LINE)
    # Section 1
    print_header_1("OWNER", "KEN_DRICK_ON_FIRE")
    print_header_1("TOOL TYPE", "AUTO_SHARE_VIP")
    print_header_1("VERSION", "PREMIUM", val_color=C_BLUE)
    print_header_1("WHATSAPP", "0123456789", val_color=C_RED)
    
    console.print(SEPARATOR_LINE)
    # Section 2
    print_header_2("SIM CODE", "019")
    print_header_2("TOTAL UID", "9999")
    print_header_2("TURN", "[ON/OFF] AIRPLANE MODE EVERY 3 MIN")
    
    console.print(SEPARATOR_LINE)

def menu_option(number, letter, description, is_exit=False):
    """Adapted menu style to match the header's green theme."""
    t = Text("", style="bold")
    t.append("[=] ", style=C_GREEN)
    
    # Key part: [01/A]
    t.append("[", style=C_WHITE)
    t.append(f"{number}/{letter}", style=C_GREEN)
    t.append("] ", style=C_WHITE)
    
    # Description
    if is_exit:
        t.append(description, style=C_RED)
    else:
        t.append(description, style=C_GREEN)
    
    console.print(t)

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
        time.sleep(0.1)
    console.print(SEPARATOR_LINE)

# --- LOADERS & ANIMATIONS ---
def matrix_rain():
    chars = "ABCDEF0123456789"
    sound.speak("Initializing VIP System...")
    with Live(console=console, refresh_per_second=15, transient=True):
        for _ in range(30):
            line = "".join(random.choice(chars) for _ in range(60))
            console.print(line, style=f"dim {C_GREEN}")
            time.sleep(0.04)
    clear()

def vip_loader(task_name, steps):
    sound.speak(f"{task_name} started.")
    progress = Progress(
        SpinnerColumn(style=f"bold {C_GREEN}"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=None, complete_style=f"{C_GREEN}", finished_style="dim green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    
    # Using a simple box style to match the raw look of the screenshot
    panel = Panel(
        progress,
        title=f"[bold {C_GREEN}]PROCESS: {task_name}[/]",
        border_style=f"{C_GREEN}",
        box=box.SQUARE,
        padding=(1, 2)
    )

    with Live(panel, console=console, refresh_per_second=10):
        task_id = progress.add_task("Waiting...", total=100)
        chunk = 100 / len(steps)
        curr = 0
        for step, delay in steps:
            progress.update(task_id, description=f"[bold {C_GREEN}]{step}...")
            sound.speak(step)
            ticks = 20
            for _ in range(ticks):
                time.sleep(delay / ticks)
                curr += (chunk / ticks)
                progress.update(task_id, completed=min(curr, 100))
    
    console.print(f"[{C_GREEN}] [✓] {task_name} COMPLETED SUCCESSFULLY![/]")
    sound.speak("Completed.")
    time.sleep(1)

def get_input():
    sound.speak("Enter choice.")
    # Style: [AKASH-] - [19... [OK/CP]-[2/0] █
    # Adapting for input prompt
    t = Text("\n[", style=f"bold {C_GREEN}")
    t.append("KEN_DRICK-", style=f"bold {C_GREEN}")
    t.append("] ➤ ", style=f"bold {C_WHITE}")
    console.print(t, end="")
    return input("").upper().strip()

# --- MAIN ---
def main():
    clear()
    matrix_rain()
    print_banner()
    header_section()
    
    while True:
        clear()
        print_banner()
        header_section()
        show_menu_animated()
        
        try:
            choice = get_input()

            if choice in ['1', '01', 'A']:
                print()
                steps = [("Injecting", 2.0), ("Bypassing", 2.0), ("Sharing", 3.0)]
                vip_loader("AUTO SHARE", steps)
                
                # Simulate the log style from the photo
                sound.speak("Showing activity logs.")
                console.print(SEPARATOR_LINE)
                console.print(f"[{C_GREEN}KEN_DRICK -OK{C_WHITE}] 10000...", style=f"bold {C_GREEN}")
                console.print(f"[{C_GREEN}COOKIE{C_WHITE}] c_user=1000...xs=17:9Ngw...", style=f"bold {C_WHITE}")
                console.print(f"[{C_GREEN}KEN_DRICK -OK{C_WHITE}] 10000...", style=f"bold {C_GREEN}")
                console.print(f"[{C_GREEN}COOKIE{C_WHITE}] c_user=1000...xs=29:p4lr...", style=f"bold {C_WHITE}")
                console.print(SEPARATOR_LINE)
                input(f"\n[{C_YELLOW} PRESS ENTER TO BACK {C_WHITE}]")

            elif choice in ['2', '02', 'B']:
                print()
                steps = [("Scanning", 2.0), ("Joining", 2.5)]
                vip_loader("GROUP JOINER", steps)

            elif choice in ['0', '00', 'X']:
                print()
                sound.speak("Exiting.")
                slow_type("[!] Exiting...", style=f"bold {C_RED}")
                sys.exit()
            else:
                sound.speak("Invalid error.")
                console.print(f"\n[{C_RED}] INVALID SELECTION [/]")
                time.sleep(1)

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    main()
