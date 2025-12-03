import os
import sys
import time
import threading
import shutil
import random
from rich.console import Console
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.panel import Panel

# Initialize Rich Console
console = Console()

# --- CONSTANTS ---
LABEL_WIDTH = 12 
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

def clear():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def speak(text):
    """
    Uses Termux TTS to speak text.
    Runs in a separate thread so it doesn't block the animation.
    """
    def _speak_thread():
        # Check if termux-tts-speak exists (Termux environment)
        if shutil.which("termux-tts-speak"):
            # Execute the command in the background
            os.system(f"termux-tts-speak '{text}'")
        else:
            # Fallback for PC (optional, just prints if no TTS)
            pass 
            
    # Start the voice in the background
    threading.Thread(target=_speak_thread, daemon=True).start()

def type_print(text, style="bold green", delay=0.02):
    """Types text char-by-char."""
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)

def print_banner():
    banner = """
    ╔═╗╔╗ ┌─┐┬ ┬┌┬┐┌─┐ ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐
    ╠╣ ╠╩╗├─┤│ │ │ │ │ └─┐├─┤├─┤├┬┘├┤ ├┬┘
    ╚  ╚═╝┴ ┴└─┘ ┴ └─┘ └─┘┴ ┴┴ ┴┴└─└─┘┴└─
    """
    console.print(banner, style="bold cyan")

def print_line():
    console.print(SEPARATOR_LINE, style="bold green")

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
    key_text = Text("[", style="bold white")
    key_text.append(str(number), style="bold white")
    key_text.append("/", style="bold yellow")
    key_text.append(letter, style="bold white")
    key_text.append("]", style="bold white")

    if is_exit:
        desc_text = Text(f" {description}", style="bold red")
    else:
        desc_text = Text(f" {description}", style="bold green")

    console.print(key_text + desc_text)

def menu_section_animated():
    """
    Animates the menu with voice.
    """
    # Speak while showing menu
    speak("Please select an option from the menu.")
    
    options = [
        ("01", "A", "START AUTO SHARE", False),
        ("02", "B", "JOIN FB GROUP", False),
        ("03", "C", "JOIN FACEBOOK", False),
        ("04", "D", "FOLLOW GITHUB", False),
        ("00", "X", "BACK TO MAIN MENU", True),
    ]
    
    for num, let, desc, is_ex in options:
        menu_option(num, let, desc, is_exit=is_ex)
        time.sleep(0.08) # Slightly slower for dramatic effect
    
    print_line()

def animated_input(prompt_text_str, voice_msg=None):
    """
    1. Plays voice (if provided).
    2. Types out the prompt design.
    3. Waits for input.
    """
    if voice_msg:
        speak(voice_msg)

    # Manual construction of prompt "[➤] CHOICE ➤"
    console.print(" [", style="bold white", end="")
    time.sleep(0.05)
    console.print("➤", style="bold white", end="")
    time.sleep(0.05)
    console.print("]", style="bold white", end="")
    
    # Typing the word " CHOICE " or whatever is passed
    type_print(f" {prompt_text_str} ", style="bold cyan", delay=0.05)
    
    console.print("➤ ", style="bold white", end="")
    
    return input("").upper().strip()

def fake_loading_bar(task_name):
    """
    A cool progress bar loader using Rich.
    """
    speak(f"Processing {task_name}, please wait.")
    
    with Progress(
        SpinnerColumn(spinner_name="dots12"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=None, complete_style="green", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        task = progress.add_task(f"[bold white]{task_name}...", total=100)
        
        while not progress.finished:
            # Simulate work with random speed
            sleep_time = random.uniform(0.02, 0.08)
            time.sleep(sleep_time)
            progress.update(task, advance=random.randint(2, 5))

def main():
    clear()
    
    # Intro Voice
    speak("Welcome to F B Auto Sharer by Ken Drick.")
    
    # Fake startup loader
    fake_loading_bar("Loading Assets")
    
    while True:
        clear()
        print_banner()
        header_section()
        menu_section_animated()
        
        try:
            # Voice + Animation for Input
            choice = animated_input("CHOICE", voice_msg="Enter your choice now.")

            if choice in ['1', '01', 'A']:
                print()
                speak("You selected Auto Share.")
                
                # Ask for Cookie with voice
                cookie = animated_input("COOKIE", voice_msg="Please paste your Facebook cookie.")
                
                # Ask for Link with voice
                link = animated_input("POST LINK", voice_msg="Please enter the target post link.")
                
                print()
                fake_loading_bar("Authenticating Cookie")
                fake_loading_bar("Initializing Bot")
                
                console.print("\n [bold green][✓] Process Started Successfully![/]")
                speak("Process started successfully.")
                time.sleep(2)
                
            elif choice in ['0', '00', 'X']:
                print()
                speak("Exiting program. Goodbye.")
                console.print("\n [bold red][!] Exiting...[/]")
                time.sleep(1)
                sys.exit()
            else:
                speak("Invalid selection.")
                console.print("\n [bold red][!] Invalid Selection[/]")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print()
            speak("Force closing.")
            console.print("\n\n [bold red][!] Force Exit[/]")
            sys.exit()

if __name__ == "__main__":
    main()
