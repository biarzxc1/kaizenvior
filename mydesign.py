import os
import sys
import time
import threading
import random
import subprocess

# --- AUTO-INSTALLER ---
try:
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.align import Align
    import pyttsx3
except ImportError:
    os.system("pip install rich pyttsx3")
    print("\n[!] Libraries installed. Please restart.")
    sys.exit()

# --- CONFIGURATION ---
console = Console()

# Colors from the screenshot
C_GREEN = "#00FF00"   # The Matrix Green
C_PINK = "#FF0055"    # The [≈] Color
C_YELLOW = "#FFFF00"  # Label Color
C_BLUE = "#00BFFF"    # Version Color (Premium)
C_RED = "#FF0000"     # Phone Number Color
C_WHITE = "#FFFFFF"

# --- AUDIO ENGINE ---
def speak_async(text):
    def _run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 145)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    t = threading.Thread(target=_run)
    t.daemon = True
    t.start()

# --- UI HELPERS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_line():
    console.print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", style=f"bold {C_GREEN}")

def slow_type(text, style="bold white", speed=0.04):
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(speed)
    console.print()

# --- SPECIFIC UI COMPONENTS (MATCHING PHOTO) ---

def print_banner():
    # The specific "AUTO" ASCII art you requested
    banner = r"""
        █████╗ ██╗   ██╗████████╗ ██████╗
        ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
        ███████║██║   ██║   ██║   ██║   ██║
        ██╔══██║██║   ██║   ██║   ██║   ██║
        ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
        ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝
    """
    console.print(Align.center(banner), style=f"bold {C_GREEN}")
    # Version right aligned or centered under banner
    console.print(Align.right("V/3.9  "), style=f"bold {C_GREEN}")

def row_style_1(label, value, value_color):
    """
    Style: [≈] LABEL : VALUE
    Colors: [≈] (Pink), LABEL (Yellow), : (Pink), VALUE (Variable)
    """
    # [≈]
    text = Text("[", style=f"bold {C_PINK}")
    text.append("≈", style=f"bold {C_PINK}")
    text.append("] ", style=f"bold {C_PINK}")
    
    # OWNER :
    text.append(f"{label:<10}", style=f"bold {C_YELLOW}")
    text.append(":", style=f"bold {C_PINK}")
    
    # VALUE
    text.append(f" {value}", style=f"bold {value_color}")
    
    console.print(text)

def row_style_2(label, value, highlight_word=None):
    """
    Style: [=] LABEL : VALUE
    Colors: [=] (Green), LABEL (Green), : (Green), VALUE (Green/White)
    """
    # [=]
    text = Text("[", style=f"bold {C_GREEN}")
    text.append("=", style=f"bold {C_GREEN}")
    text.append("] ", style=f"bold {C_GREEN}")
    
    # SIM CODE :
    text.append(f"{label:<10}", style=f"bold {C_GREEN}")
    text.append(":", style=f"bold {C_GREEN}")
    
    # VALUE (Mixed formatting)
    if highlight_word:
        # Special logic for the "TURN [ON/OFF]..." line
        parts = value.split(highlight_word)
        text.append(f" {parts[0]}", style=f"bold {C_GREEN}")
        text.append(highlight_word, style=f"bold {C_WHITE}")
        if len(parts) > 1:
            text.append(parts[1], style=f"bold {C_GREEN}")
    else:
        text.append(f" {value}", style=f"bold {C_WHITE}")
        
    console.print(text)

def header_section():
    print_line()
    
    # --- FIRST SECTION (PINK/YELLOW THEME) ---
    row_style_1("OWNER", "KEN DRICK", C_YELLOW)
    row_style_1("TOOL TYPE", "AUTO_SHARE", C_GREEN)
    row_style_1("VERSION", "PREMIUM", C_BLUE)
    row_style_1("WHATSAPP", "+1234567890", C_RED)
    
    print_line()
    
    # --- SECOND SECTION (GREEN THEME) ---
    row_style_2("SIM CODE", "019")
    row_style_2("TOTAL UID", "9999")
    
    # Special formatting for the Airplane Mode line to match photo color mix
    # "[=] TURN [ON/OFF] AIRPLANE MODE EVERY 3 MIN"
    # We construct this manually to match the photo exactly
    t = Text("[", style=f"bold {C_GREEN}")
    t.append("=", style=f"bold {C_GREEN}")
    t.append("] ", style=f"bold {C_GREEN}")
    t.append("TURN ", style=f"bold {C_GREEN}")
    t.append("[ON/OFF]", style=f"bold {C_WHITE}")
    t.append(" AIRPLANE MODE EVERY ", style=f"bold {C_GREEN}")
    t.append("3", style=f"bold {C_WHITE}")
    t.append(" MIN", style=f"bold {C_GREEN}")
    console.print(t)
    
    print_line()

def menu_option(number, letter, description, is_exit=False):
    """
    Style: [ 01/A ] DESCRIPTION
    Matches the clean look in your description.
    """
    # Bracket Key
    key = Text("[ ", style=f"bold {C_WHITE}")
    key.append(f"{number}/{letter}", style=f"bold {C_WHITE}")
    key.append(" ]", style=f"bold {C_WHITE}")
    
    # Description
    desc_color = C_RED if is_exit else C_WHITE
    desc = Text(f" {description}", style=f"bold {desc_color}")
    
    console.print(key + desc)

def menu_section():
    options = [
        ("01", "A", "START AUTO SHARE", False),
        ("02", "B", "JOIN FB GROUP", False),
        ("03", "C", "JOIN FACEBOOK", False),
        ("04", "D", "FOLLOW GITHUB", False),
        ("00", "X", "BACK TO MAIN MENU", True),
    ]
    
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
        time.sleep(0.02) # Fast cascade
    print_line()

# --- INPUT & LOADERS ---

def animated_input():
    """
    Restored the ➤ Arrow as requested.
    Format: [➤] CHOICE ➤ 
    """
    speak_async("Select your option")
    
    # [➤]
    console.print(" [", style="bold white", end="")
    console.print("➤", style="bold white", end="")
    console.print("] ", style="bold white", end="")
    
    # CHOICE
    for char in "CHOICE":
        console.print(char, style="bold cyan", end="")
        sys.stdout.flush()
        time.sleep(0.02)
    
    # ➤ 
    console.print(" ➤ ", style="bold white", end="")
    
    return input("").upper().strip()

def vip_loader(title, duration=3):
    """
    A minimal, VIP style loader.
    """
    speak_async(f"Starting {title}")
    
    with Progress(
        SpinnerColumn(style="bold yellow"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(complete_style="red", finished_style="green"),
        TextColumn("[bold white]{task.percentage:>3.0f}%"),
        transient=True
    ) as progress:
        task = progress.add_task(f"{title}...", total=100)
        
        while not progress.finished:
            progress.update(task, advance=2)
            time.sleep(duration / 50)

# --- MAIN LOOP ---

def main():
    clear()
    speak_async("Welcome to Auto Share Premium.")
    
    while True:
        clear()
        print_banner()
        header_section()
        menu_section()
        
        try:
            choice = animated_input()

            if choice in ['1', '01', 'A']:
                print()
                vip_loader("ACCESSING SERVER", 2)
                vip_loader("BYPASSING SECURITY", 2)
                
                # Mock output like the green text in your photo
                console.print("\n[bold green][AUTO -OK] 100092384728...[/]")
                console.print("[bold green][COOKIE] c_user=100... xs=17:9Ngw2...[/]")
                slow_type("Process Running...", style="dim green")
                input("\n[bold white]Press Enter to return...[/]")
                
            elif choice in ['2', '02', 'B']:
                print()
                vip_loader("FETCHING GROUPS", 2)
                time.sleep(1)

            elif choice in ['0', '00', 'X']:
                print()
                speak_async("Goodbye.")
                sys.exit()
                
            else:
                speak_async("Invalid")
                console.print("\n[bold red][!] INVALID SELECTION[/]")
                time.sleep(1)

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    main()
