import time
import random
import sys
from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.panel import Panel

# Initialize Rich Console
console = Console()

# --- Configuration ---
TOOL_NAME = "RPW"
VERSION = "V/1.0"
OWNER = "YOUR_NAME_HERE"
WHATSAPP = "+1234567890"

def clear_screen():
    # Clears the terminal screen
    console.clear()

def print_banner():
    # Manually created blocky ASCII art for "RPW" to ensure it works without pyfiglet
    # You can change the color style here (e.g., "bold green", "bold cyan")
    ascii_art = """
[bold green]
██████╗ ██████╗ ██╗    ██╗
██╔══██╗██╔══██╗██║    ██║
██████╔╝██████╔╝██║ █╗ ██║
██╔══██╗██╔═══╝ ██║███╗██║
██║  ██║██║     ╚███╔███╔╝
╚═╝  ╚═╝╚═╝      ╚══╝╚══╝
[/bold green]"""
    
    # Print the Banner
    console.print(ascii_art, highlight=False)
    
    # Print the Version number floating to the right (simulated)
    console.print(f"[bold green]{' '*30}{VERSION}[/]")
    
    # Print the Green Divider Line
    console.print("[bold green]" + "_" * 50 + "[/]")

def print_info():
    # The Info Section (simulating the [≈] style)
    # Using simple f-strings with Rich markup for the exact terminal look
    
    # Define styles for the brackets and text
    bracket_style = "[bold red]"
    key_style = "[bold yellow]" 
    val_style = "[bold green]"
    
    # Layout matches the screenshot structure
    console.print(f"{bracket_style}[≈] OWNER      : {key_style}{OWNER}")
    console.print(f"{bracket_style}[≈] TOOL TYPE  : {val_style}RANDOM_FILE")
    console.print(f"{bracket_style}[≈] VERSION    : {style_text('PREMIUM', 'bold blue')}")
    console.print(f"{bracket_style}[≈] WHATSAPP   : {style_text(WHATSAPP, 'bold red')}")
    
    # Second Divider
    console.print("[bold green]" + "_" * 50 + "[/]")
    console.print() # Spacer

    # Status Section
    console.print(f"[bold green][=] SIM CODE   : 019")
    console.print(f"[bold green][=] TOTAL UID  : 9999")
    console.print(f"[bold green][=] TURN [ON/OFF] AIRPLANE MODE EVERY 3 MIN")
    console.print("[bold green]" + "_" * 50 + "[/]")
    console.print()

def style_text(text, style_name):
    return f"[{style_name}]{text}[/{style_name}]"

def simulate_process():
    """
    Simulates the scrolling log output seen in the screenshot.
    """
    ids = ["100076", "100082", "100093", "100012", "100045"]
    
    try:
        while True:
            # Generate random fake data to mimic the screenshot
            uid_prefix = random.choice(ids)
            uid = f"{uid_prefix}{random.randint(10000000, 99999999)}"
            
            # 20% chance of a "Hit/Success" (Green)
            # 80% chance of standard processing or waiting
            status = random.random()
            
            if status < 0.3:
                # SUCCESS / OK FORMAT
                console.print(f"[bold green][{TOOL_NAME}-OK] {uid} | M | ...[/]")
                console.print(f"[bold green][COOKIE] c_user={uid};xs=17:9Ngw2VXT2n...[/]")
                console.print(f"[bold white]UA: Mozilla/5.0 (Linux; Android 10)...[/]")
                console.print("[bold green]" + "-" * 50 + "[/]")
            
            elif status < 0.4:
                # CHECKPOINT / CP FORMAT (Yellow/Red)
                console.print(f"[bold yellow][{TOOL_NAME}-CP] {uid} | [bold red]CHECKPOINT[/]")
                console.print(f"[bold red][✘] Password Incorrect or Locked[/]")
            
            # Simple spacing or speed control
            time.sleep(0.1) 

    except KeyboardInterrupt:
        console.print("\n[bold red][!] Process Stopped by User[/]")

if __name__ == "__main__":
    clear_screen()
    print_banner()
    print_info()
    
    # Add a small delay before starting the "work"
    time.sleep(1)
    
    simulate_process()

