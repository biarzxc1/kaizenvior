import os
import sys
import subprocess
import time
import threading

# --- AUTO-INSTALLER SECTION ---
def install_requirements():
    """
    Checks if required libraries are installed.
    If not, installs them automatically.
    """
    requirements = [
        ("rich", "rich"),       # (package_name, import_name)
        ("pyttsx3", "pyttsx3")
    ]
    
    needs_install = False
    
    for package, import_name in requirements:
        try:
            __import__(import_name)
        except ImportError:
            needs_install = True
            print(f"[!] {package} is not installed. Installing now...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"[✓] {package} installed successfully.")
            except subprocess.CalledProcessError:
                print(f"[X] Failed to install {package}. Please install manually.")
                sys.exit(1)
    
    if needs_install:
        print("[!] All requirements installed. Starting tool...\n")
        time.sleep(1)
        # Clear screen to make it clean before importing rich
        os.system('cls' if os.name == 'nt' else 'clear')

# Run the installer BEFORE importing specific libraries
install_requirements()

# --- IMPORTS (After Auto-Install) ---
import pyttsx3
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner

# Initialize Rich Console
console = Console()

# --- CONFIGURATION ---
LABEL_WIDTH = 12 
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- VOICE / AUDIO ENGINE ---
def speak_async(text):
    """
    Speaks text in a separate thread so it doesn't block the animation.
    """
    def run_voice():
        try:
            # Initialize engine inside the thread to avoid loop issues
            engine = pyttsx3.init()
            engine.setProperty('rate', 160) 
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception:
            # This prevents crashes on Termux if 'espeak' isn't installed in the OS
            pass
            
    thread = threading.Thread(target=run_voice)
    thread.daemon = True # Kills thread if program exits
    thread.start()

# --- UTILS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_print(text, style="bold white", delay=0.02):
    """Types out text character by character."""
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)

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
        # The Red Highlight Style
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
    """
    Prints menu option with HIGHLIGHTED keys (White on Red).
    """
    # Create the block: [ 01/A ] with Red Background
    key_text = Text("[ ", style="bold red")
    key_text.append(f"{number}/{letter}", style="bold white on red")
    key_text.append(" ]", style="bold red")

    if is_exit:
        desc_text = Text(f" {description}", style="bold red")
    else:
        desc_text = Text(f" {description}", style="bold green")

    console.print(key_text + desc_text)

def menu_section_animated():
    """
    Shows menu items one by one with a cascade effect.
    """
    options = [
        ("01", "A", "START AUTO SHARE", False),
        ("02", "B", "JOIN FB GROUP", False),
        ("03", "C", "JOIN FACEBOOK", False),
        ("04", "D", "FOLLOW GITHUB", False),
        ("00", "X", "BACK TO MAIN MENU", True),
    ]
    
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
        time.sleep(0.03)
    
    print_line()

def animated_input_with_voice(prompt_text_display, voice_message):
    """
    1. Speaks the voice message.
    2. Animates the prompt text simultaneously.
    3. Returns the user input.
    """
    speak_async(voice_message)
    
    # Visual Prompt Construction: [➤] CHOICE ➤ 
    console.print(" [", style="bold white", end="")
    time.sleep(0.05)
    console.print("➤", style="bold white", end="")
    time.sleep(0.05)
    console.print("]", style="bold white", end="")
    
    # Type " CHOICE " nicely
    type_print(" CHOICE ", style="bold cyan", delay=0.04)
    
    console.print("➤ ", style="bold white", end="")
    
    # Capture input
    return input("").upper().strip()

def process_loader(message):
    """
    A fancy loader that spins while speaking.
    """
    speak_async(message)
    spinner = Spinner("dots12", text=f" [bold green]{message}...", style="bold green")
    
    # Run the spinner for 3 seconds to simulate work
    with Live(spinner, refresh_per_second=20, transient=True):
        time.sleep(3)

# --- MAIN LOGIC ---
def main():
    clear()
    speak_async("Welcome to F B Auto Sharer. Created by Ken Drick.")
    type_print("[*] Loading System...", delay=0.03)
    time.sleep(0.5)

    while True:
        clear()
        print_banner()
        header_section()
        menu_section_animated()
        
        try:
            choice = animated_input_with_voice(
                prompt_text_display="CHOICE", 
                voice_message="Please enter your choice."
            )

            if choice in ['1', '01', 'A']:
                print()
                speak_async("Starting Auto Share Process.")
                type_print("[!] Initializing...", style="bold yellow")
                
                # --- INPUT EXAMPLE WITH VOICE ---
                # Example of asking for a cookie or token with voice
                # speak_async("Please paste your cookies.")
                # cookie = input(" [?] Paste Cookie: ")
                
                # Fancy Loaders
                process_loader("Extracting Cookies from Browser")
                process_loader("Validating Access Token")
                process_loader("Targeting Facebook Groups")
                
                speak_async("Process Completed Successfully.")
                console.print("\n [bold green on white] ✓ SUCCESS [/] [bold green]Share completed successfully![/]")
                time.sleep(2)
                
            elif choice in ['2', '02', 'B']:
                print()
                speak_async("Opening Facebook Groups.")
                process_loader("Redirecting to Groups")
                time.sleep(1)

            elif choice in ['0', '00', 'X']:
                print()
                speak_async("Exiting the program. Goodbye.")
                console.print("\n [bold red][!] Exiting...[/]")
                time.sleep(1)
                sys.exit()
            else:
                print()
                speak_async("Invalid selection. Please try again.")
                console.print("\n [bold red][!] Invalid Selection[/]")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print()
            speak_async("Force exit detected.")
            console.print("\n\n [bold red][!] Force Exit[/]")
            sys.exit()

if __name__ == "__main__":
    main()
