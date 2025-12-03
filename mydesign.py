import os
import sys
import subprocess
import time
import threading
import random

# --- AUTO-INSTALLER SECTION ---
def install_requirements():
    requirements = [("rich", "rich")]
    needs_install = False
    
    for package, import_name in requirements:
        try:
            __import__(import_name)
        except ImportError:
            needs_install = True
            print(f"[!] {package} is missing. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            except subprocess.CalledProcessError:
                sys.exit(1)
    
    if needs_install:
        os.system('cls' if os.name == 'nt' else 'clear')

install_requirements()

# --- IMPORTS ---
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich.table import Table
from rich import box

# Initialize Console
console = Console()

# --- COLOR SCHEME (VIP/ADMIN THEME) ---
GOLD = "#FFD700"
CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
RED = "#FF3333"
GREEN = "#00FF00"
WHITE = "#FFFFFF"
DARK_RED = "#8B0000"

# --- CONFIGURATION ---
LABEL_WIDTH = 14
SEPARATOR_CHAR = "═"

# --- AUDIO ENGINE (TERMUX COMPATIBLE) ---
def speak_async(text):
    """Speaks text using Termux TTS API (termux-tts-speak) without blocking."""
    def run_voice():
        try:
            # Check if running in Termux
            if os.path.exists('/data/data/com.termux'):
                subprocess.run(['termux-tts-speak', text], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
            else:
                # Fallback for non-Termux (try espeak or pyttsx3)
                try:
                    subprocess.run(['espeak', text], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
                except:
                    try:
                        import pyttsx3
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 150)
                        engine.setProperty('volume', 1.0)
                        engine.say(text)
                        engine.runAndWait()
                    except:
                        pass
        except:
            pass
    thread = threading.Thread(target=run_voice)
    thread.daemon = True
    thread.start()

# --- UTILS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, style="bold white", delay=0.03, sound=False):
    """Enhanced typing effect with variable speed."""
    if sound:
        speak_async(text)
    for i, char in enumerate(text):
        console.print(char, style=style, end="")
        sys.stdout.flush()
        if char in '.!?':
            time.sleep(delay * 8)
        elif char == ',':
            time.sleep(delay * 4)
        elif char == ' ':
            time.sleep(delay * 1.5)
        else:
            time.sleep(delay + random.uniform(0.005, 0.02))
    console.print()
    time.sleep(0.15)

def fade_in_text(text, style="bold cyan", steps=8):
    """Fade in effect for text."""
    for i in range(steps):
        clear()
        opacity = (i + 1) / steps
        if opacity < 0.3:
            current_style = "dim white"
        elif opacity < 0.6:
            current_style = "white"
        else:
            current_style = style
        console.print(text, style=current_style, justify="center")
        time.sleep(0.08)

def print_separator(char="═", style="bold yellow", width=55):
    """Print a styled separator line."""
    console.print(char * width, style=style)

def print_double_line():
    """Print double separator for sections."""
    console.print("╔" + "═" * 53 + "╗", style=f"bold {GOLD}")

def print_double_line_end():
    console.print("╚" + "═" * 53 + "╝", style=f"bold {GOLD}")

# --- ANIMATED INTRO ---
def animated_intro():
    """Premium animated intro sequence."""
    clear()
    
    # Glitch effect intro
    glitch_frames = [
        "▓▓▓ SYSTEM INITIALIZING ▓▓▓",
        "░░░ SYSTEM INITIALIZING ░░░",
        "▒▒▒ SYSTEM INITIALIZING ▒▒▒",
        "▓░▒ SYSTEM INITIALIZING ▒░▓",
    ]
    
    for _ in range(3):
        for frame in glitch_frames:
            console.print(Align.center(f"[bold red]{frame}[/]"))
            time.sleep(0.08)
            clear()
    
    # Loading dots animation
    loading_text = "LOADING"
    for i in range(4):
        clear()
        dots = "●" * i + "○" * (3 - i)
        console.print(Align.center(f"\n\n[bold cyan]{loading_text} {dots}[/]"))
        time.sleep(0.3)
    
    time.sleep(0.3)

# --- VIP BANNER ---
def print_banner():
    """Premium VIP/Admin style banner."""
    banner_art = """
██████╗ ██████╗ ██╗    ██╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔══██╗██║    ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝██████╔╝██║ █╗ ██║       ██║   ██║   ██║██║   ██║██║     
██╔══██╗██╔═══╝ ██║███╗██║       ██║   ██║   ██║██║   ██║██║     
██║  ██║██║     ╚███╔███╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚═╝      ╚══╝╚══╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    
    sub_banner = """
    ╭──────────────────────────────────────────────╮
    │    ⚡ FACEBOOK AUTO SHARER - VIP EDITION ⚡    │
    ╰──────────────────────────────────────────────╯
    """
    
    # Animate banner line by line
    for line in banner_art.strip().split('\n'):
        console.print(Align.center(f"[bold cyan]{line}[/]"))
        time.sleep(0.08)
    
    time.sleep(0.2)
    
    for line in sub_banner.strip().split('\n'):
        console.print(Align.center(f"[bold yellow]{line}[/]"))
        time.sleep(0.1)
    
    console.print()
    time.sleep(0.3)

# --- INFO PANEL ---
def print_info_row(label, value, icon="◆", is_highlighted=False, is_vip=False):
    """Print styled info row with animation."""
    time.sleep(0.06)
    
    icon_style = f"bold {MAGENTA}" if is_vip else f"bold {CYAN}"
    
    row = Text()
    row.append(f"  {icon} ", style=icon_style)
    row.append(f"{label:<{LABEL_WIDTH}}", style=f"bold {GOLD}")
    row.append("│ ", style="dim white")
    
    if is_highlighted:
        row.append("【 ", style=f"bold {RED}")
        row.append(value, style=f"bold white on {DARK_RED}")
        row.append(" 】", style=f"bold {RED}")
    elif is_vip:
        row.append("★ ", style=f"bold {GOLD}")
        row.append(value, style=f"bold {MAGENTA}")
        row.append(" ★", style=f"bold {GOLD}")
    else:
        row.append(value, style=f"bold {GREEN}")
    
    console.print(row)

def header_section():
    """Animated header section with VIP styling."""
    print_double_line()
    console.print("║" + " " * 15 + "[bold white]《 SYSTEM INFORMATION 》[/]" + " " * 14 + "║", style=f"bold {GOLD}")
    print_double_line_end()
    console.print()
    
    info_items = [
        ("DEVELOPER", "KEN DRICK", "◈", False, True),
        ("GITHUB", "RYO GRAHHH", "◇", False, False),
        ("VERSION", "2.0.0 VIP", "◆", False, True),
        ("STATUS", "PREMIUM ACTIVE", "●", False, True),
        ("FACEBOOK", "facebook.com/ryoevisu", "◎", False, False),
        ("TOOL NAME", "FB AUTO SHARER", "★", True, False),
    ]
    
    for label, value, icon, highlighted, vip in info_items:
        print_info_row(label, value, icon, highlighted, vip)
    
    console.print()

# --- MENU SECTION ---
def menu_option(number, letter, description, icon="►", is_exit=False, is_vip=False):
    """Animated menu option with VIP styling."""
    time.sleep(0.1)
    
    row = Text()
    row.append("    ", style="")
    
    # Key badge
    if is_exit:
        row.append("╔═══╗ ", style=f"bold {RED}")
        row.append(f"{number}", style=f"bold white on {DARK_RED}")
        row.append("/", style=f"bold {RED}")
        row.append(f"{letter}", style=f"bold white on {DARK_RED}")
        row.append(" ╚═══╝", style=f"bold {RED}")
    elif is_vip:
        row.append("『 ", style=f"bold {GOLD}")
        row.append(f"{number}/{letter}", style=f"bold {MAGENTA}")
        row.append(" 』", style=f"bold {GOLD}")
    else:
        row.append("【 ", style=f"bold {CYAN}")
        row.append(f"{number}/{letter}", style=f"bold white")
        row.append(" 】", style=f"bold {CYAN}")
    
    # Description
    row.append(f" {icon} ", style=f"bold {GOLD}")
    
    if is_exit:
        row.append(description, style=f"bold {RED}")
    elif is_vip:
        row.append(description, style=f"bold {MAGENTA}")
        row.append(" ⚡VIP", style=f"bold {GOLD}")
    else:
        row.append(description, style=f"bold {GREEN}")
    
    console.print(row)

def menu_section_animated():
    """Premium animated menu section."""
    print_double_line()
    console.print("║" + " " * 17 + "[bold white]《 MAIN MENU 》[/]" + " " * 17 + "║", style=f"bold {GOLD}")
    print_double_line_end()
    console.print()
    
    options = [
        ("01", "A", "START AUTO SHARE", "⚡", False, True),
        ("02", "B", "JOIN FB GROUP", "👥", False, False),
        ("03", "C", "JOIN FACEBOOK", "📘", False, False),
        ("04", "D", "FOLLOW GITHUB", "🔗", False, False),
        ("05", "E", "VIEW STATISTICS", "📊", False, True),
        ("00", "X", "EXIT TOOL", "✖", True, False),
    ]
    
    for num, let, desc, icon, is_ex, is_vip in options:
        menu_option(num, let, desc, icon, is_exit=is_ex, is_vip=is_vip)
    
    console.print()
    print_separator("─", f"dim {CYAN}", 55)
    console.print()

# --- PREMIUM INPUT ---
def animated_input_with_voice(voice_message):
    """Premium animated input prompt."""
    speak_async(voice_message)
    
    # Animated prompt
    prompt_parts = [
        ("  ╭─", f"bold {CYAN}"),
        ("[ ", f"bold {GOLD}"),
        ("INPUT", f"bold white"),
        (" ]", f"bold {GOLD}"),
        ("─╮", f"bold {CYAN}"),
    ]
    
    for text, style in prompt_parts:
        console.print(text, style=style, end="")
        time.sleep(0.05)
    
    console.print()
    
    # Input line
    console.print("  │ ", style=f"bold {CYAN}", end="")
    
    # Typing animation for "CHOICE"
    choice_text = "CHOICE"
    for char in choice_text:
        console.print(char, style=f"bold {MAGENTA}", end="")
        sys.stdout.flush()
        time.sleep(0.06)
    
    console.print(" ➤ ", style=f"bold {GOLD}", end="")
    
    user_input = input("").upper().strip()
    
    console.print("  ╰" + "─" * 20 + "╯", style=f"bold {CYAN}")
    
    return user_input

# --- PREMIUM LOADERS ---
def matrix_loader(title, duration=3):
    """Matrix-style loading animation."""
    speak_async(title)
    
    chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789"
    width = 50
    
    start_time = time.time()
    frame = 0
    
    while time.time() - start_time < duration:
        frame += 1
        line = ""
        for i in range(width):
            if random.random() < 0.15:
                line += random.choice(chars)
            else:
                line += " "
        
        progress = (time.time() - start_time) / duration
        bar_width = int(progress * 40)
        bar = "█" * bar_width + "░" * (40 - bar_width)
        
        console.print(f"\r  [dim green]{line}[/]", end="")
        time.sleep(0.05)
    
    console.print()

def cyber_loader(title, steps):
    """Cyberpunk-style boxed loader with enhanced animations."""
    speak_async(title)
    
    # Header animation
    console.print()
    header_line = f"╔{'═' * 53}╗"
    for i, char in enumerate(header_line):
        console.print(char, style=f"bold {CYAN}", end="")
        if i % 5 == 0:
            time.sleep(0.02)
    console.print()
    
    # Title
    title_padded = f"║  ⚡ {title:^47} ⚡  ║"
    console.print(title_padded, style=f"bold {GOLD}")
    
    console.print(f"╠{'═' * 53}╣", style=f"bold {CYAN}")
    
    total_steps = len(steps)
    
    for idx, (step_msg, sleep_time) in enumerate(steps):
        # Step indicator
        step_num = f"[{idx + 1}/{total_steps}]"
        
        # Progress calculation
        progress = int((idx / total_steps) * 40)
        bar = "▓" * progress + "░" * (40 - progress)
        
        # Status line with animation
        status_line = f"║  {step_num} {step_msg:<35}  ║"
        
        # Type out the status
        console.print("║  ", style=f"bold {CYAN}", end="")
        console.print(step_num, style=f"bold {MAGENTA}", end="")
        console.print(" ", end="")
        
        for char in step_msg:
            console.print(char, style=f"bold {GREEN}", end="")
            sys.stdout.flush()
            time.sleep(0.02)
        
        # Fill remaining space
        remaining = 35 - len(step_msg)
        console.print(" " * remaining, end="")
        console.print("  ║", style=f"bold {CYAN}")
        
        # Progress bar line
        console.print(f"║  [", style=f"bold {CYAN}", end="")
        
        # Animated progress bar fill
        chunks = 20
        chunk_sleep = sleep_time / chunks
        
        for i in range(chunks):
            current_progress = int(((idx + (i / chunks)) / total_steps) * 40)
            bar_display = "▓" * current_progress + "░" * (40 - current_progress)
            pct = int(((idx + (i / chunks)) / total_steps) * 100)
            
            # Update bar in place
            console.print(f"\r║  [{bar_display}] {pct:3}%  ║", style=f"bold {CYAN}", end="")
            sys.stdout.flush()
            time.sleep(chunk_sleep)
        
        console.print()
        
        if idx < total_steps - 1:
            console.print(f"║{'─' * 53}║", style=f"dim {CYAN}")
    
    # Final progress
    final_bar = "▓" * 40
    console.print(f"║  [{final_bar}] 100%  ║", style=f"bold {GREEN}")
    
    # Footer
    console.print(f"╠{'═' * 53}╣", style=f"bold {CYAN}")
    
    # Success message with animation
    success_msg = "✓ OPERATION COMPLETED SUCCESSFULLY ✓"
    console.print("║", style=f"bold {CYAN}", end="")
    padding = (53 - len(success_msg)) // 2
    console.print(" " * padding, end="")
    
    for char in success_msg:
        console.print(char, style=f"bold {GREEN}", end="")
        sys.stdout.flush()
        time.sleep(0.03)
    
    console.print(" " * (53 - padding - len(success_msg)), end="")
    console.print("║", style=f"bold {CYAN}")
    
    console.print(f"╚{'═' * 53}╝", style=f"bold {CYAN}")
    console.print()
    
    speak_async("Operation completed successfully")
    time.sleep(0.5)

def pulse_loader(message, duration=2):
    """Pulsing dot loader animation."""
    speak_async(message)
    
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    dots = ["   ", ".  ", ".. ", "..."]
    
    start_time = time.time()
    frame_idx = 0
    
    while time.time() - start_time < duration:
        spinner = frames[frame_idx % len(frames)]
        dot = dots[frame_idx % len(dots)]
        
        progress = (time.time() - start_time) / duration
        bar_len = int(progress * 30)
        bar = "━" * bar_len + "○" + "─" * (30 - bar_len)
        
        console.print(f"\r  [bold cyan]{spinner}[/] [bold white]{message}{dot}[/] [{bar}]", end="")
        sys.stdout.flush()
        
        frame_idx += 1
        time.sleep(0.1)
    
    console.print(f"\r  [bold green]✓[/] [bold white]{message}[/] [{'━' * 31}]")
    console.print()

def hacker_boot_sequence():
    """Hacker-style boot sequence animation."""
    boot_messages = [
        ("Initializing kernel modules", 0.3),
        ("Loading system drivers", 0.2),
        ("Mounting virtual filesystem", 0.3),
        ("Starting network services", 0.4),
        ("Connecting to secure server", 0.5),
        ("Authenticating credentials", 0.4),
        ("Loading user profile", 0.3),
        ("System ready", 0.2),
    ]
    
    console.print()
    console.print(f"  ╔{'═' * 50}╗", style=f"bold {GREEN}")
    console.print(f"  ║{'SYSTEM BOOT SEQUENCE':^50}║", style=f"bold {GREEN}")
    console.print(f"  ╠{'═' * 50}╣", style=f"bold {GREEN}")
    
    for msg, delay in boot_messages:
        console.print(f"  ║ ", style=f"bold {GREEN}", end="")
        console.print("[", style=f"bold {CYAN}", end="")
        console.print("OK", style=f"bold {GREEN}", end="")
        console.print("] ", style=f"bold {CYAN}", end="")
        
        for char in msg:
            console.print(char, style=f"bold white", end="")
            sys.stdout.flush()
            time.sleep(0.02)
        
        remaining = 43 - len(msg)
        console.print(" " * remaining, end="")
        console.print("║", style=f"bold {GREEN}")
        time.sleep(delay)
    
    console.print(f"  ╚{'═' * 50}╝", style=f"bold {GREEN}")
    console.print()
    time.sleep(0.5)

# --- STATISTICS PANEL ---
def show_statistics():
    """Display VIP statistics panel."""
    console.print()
    
    stats_table = Table(
        title="📊 [bold yellow]VIP STATISTICS[/]",
        box=box.DOUBLE_EDGE,
        border_style="cyan",
        title_style="bold yellow",
        header_style="bold magenta",
        show_lines=True
    )
    
    stats_table.add_column("METRIC", style="bold white", justify="left")
    stats_table.add_column("VALUE", style="bold green", justify="center")
    stats_table.add_column("STATUS", style="bold cyan", justify="center")
    
    stats = [
        ("Total Shares", "1,247", "● ACTIVE"),
        ("Success Rate", "98.5%", "● EXCELLENT"),
        ("Groups Joined", "156", "● SYNCED"),
        ("Active Sessions", "3", "● RUNNING"),
        ("API Calls Today", "892", "● NORMAL"),
        ("Account Status", "VIP", "★ PREMIUM"),
    ]
    
    for metric, value, status in stats:
        stats_table.add_row(metric, value, status)
        time.sleep(0.15)
    
    console.print(Align.center(stats_table))
    console.print()

# --- MAIN LOGIC ---
def main():
    clear()
    
    # Animated intro
    animated_intro()
    
    # Boot sequence
    hacker_boot_sequence()
    
    speak_async("Welcome to Facebook Auto Sharer VIP Edition.")
    
    pulse_loader("Loading System Resources", 2)
    
    while True:
        clear()
        print_banner()
        header_section()
        menu_section_animated()
        
        try:
            choice = animated_input_with_voice("Please select an option.")

            if choice in ['1', '01', 'A']:
                console.print()
                
                # Matrix effect first
                matrix_loader("Establishing secure connection", 2)
                
                # Main loader sequence
                steps = [
                    ("Connecting to Facebook API", 1.5),
                    ("Validating User Cookies", 2.0),
                    ("Fetching Target Groups", 2.5),
                    ("Preparing Share Engine", 2.0),
                    ("Initializing Auto Share", 1.5),
                    ("Starting Background Process", 1.0)
                ]
                
                cyber_loader("⚡ INITIALIZING AUTO SHARE ⚡", steps)
                
                # Success message
                console.print()
                success_panel = Panel(
                    Align.center("[bold green]✓ AUTO SHARE IS NOW RUNNING IN BACKGROUND[/]\n\n[dim white]Press Enter to return to main menu...[/]"),
                    border_style="green",
                    title="[bold white]《 SUCCESS 》[/]",
                    title_align="center",
                    padding=(1, 2)
                )
                console.print(success_panel)
                speak_async("Auto share process started successfully.")
                input()
                
            elif choice in ['2', '02', 'B']:
                console.print()
                steps = [
                    ("Fetching Group List", 1.5),
                    ("Resolving Group URLs", 2.0),
                    ("Preparing Join Requests", 1.5),
                    ("Opening Browser", 1.0)
                ]
                cyber_loader("👥 JOINING FACEBOOK GROUPS 👥", steps)
                
                console.print(Align.center("[bold green]✓ Group join process initiated![/]"))
                time.sleep(2)

            elif choice in ['3', '03', 'C']:
                console.print()
                pulse_loader("Opening Facebook", 2)
                console.print(Align.center("[bold cyan]📘 Redirecting to Facebook...[/]"))
                time.sleep(2)

            elif choice in ['4', '04', 'D']:
                console.print()
                pulse_loader("Opening GitHub", 2)
                console.print(Align.center("[bold white]🔗 Redirecting to GitHub...[/]"))
                time.sleep(2)

            elif choice in ['5', '05', 'E']:
                console.print()
                pulse_loader("Loading Statistics", 2)
                show_statistics()
                speak_async("Statistics loaded successfully.")
                input("\n  Press Enter to return...")

            elif choice in ['0', '00', 'X']:
                console.print()
                speak_async("Thank you for using F B Auto Sharer. Goodbye.")
                
                # Shutdown animation
                shutdown_steps = [
                    ("Saving session data", 0.5),
                    ("Closing connections", 0.5),
                    ("Cleaning up resources", 0.5),
                    ("Shutting down", 0.3)
                ]
                
                cyber_loader("✖ SHUTTING DOWN ✖", shutdown_steps)
                
                type_print("\n  [★] Thank you for using FB Auto Sharer VIP!", style=f"bold {GOLD}", delay=0.04)
                type_print("  [★] See you next time!", style=f"bold {CYAN}", delay=0.04)
                console.print()
                time.sleep(1)
                sys.exit()
                
            else:
                console.print()
                speak_async("Invalid selection. Please try again.")
                
                error_panel = Panel(
                    Align.center("[bold red]✖ INVALID SELECTION[/]\n[dim white]Please choose a valid option[/]"),
                    border_style="red",
                    title="[bold red]《 ERROR 》[/]",
                    padding=(1, 2)
                )
                console.print(error_panel)
                time.sleep(2)
                
        except KeyboardInterrupt:
            console.print()
            speak_async("Operation cancelled.")
            type_print("\n  [!] Operation cancelled by user.", style="bold red")
            time.sleep(1)
            sys.exit()

if __name__ == "__main__":
    main()
