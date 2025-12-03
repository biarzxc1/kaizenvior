import os
import sys
import time
from rich.console import Console
from rich.text import Text

# Initialize Rich Console
console = Console()

# --- CONSTANTS & CONFIG ---
# Alignment spacing for the labels (to make arrows align vertically)
LABEL_WIDTH = 12 
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

def clear():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the cyan ASCII banner."""
    banner = """
    ╔═╗╔╗ ┌─┐┬ ┬┌┬┐┌─┐ ┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐
    ╠╣ ╠╩╗├─┤│ │ │ │ │ └─┐├─┤├─┤├┬┘├┤ ├┬┘
    ╚  ╚═╝┴ ┴└─┘ ┴ └─┘ └─┘┴ ┴┴ ┴┴└─└─┘┴└─
    """
    console.print(banner, style="bold cyan")

def print_line():
    """Prints the green separator line."""
    console.print(SEPARATOR_LINE, style="bold green")

def print_info_row(label, value, is_highlighted=False):
    """
    Helper function to print a single row in the info section.
    Matches format: [•] LABEL      ➤ VALUE
    """
    # 1. The Bullet [•]
    bullet = Text("[", style="bold white")
    bullet.append("•", style="bold white")
    bullet.append("] ", style="bold white")

    # 2. The Label (Yellow) padded for alignment
    label_text = Text(f"{label:<{LABEL_WIDTH}}", style="bold yellow")

    # 3. The Arrow (White)
    arrow = Text("➤ ", style="bold white")

    # 4. The Value (Green or Highlighted)
    if is_highlighted:
        # Red brackets, White text on Red Background
        val_text = Text("[ ", style="bold red")
        val_text.append(value, style="bold white on red")
        val_text.append(" ]", style="bold red")
    else:
        val_text = Text(value, style="bold green")

    # Combine and print
    final_text = bullet + label_text + arrow + val_text
    console.print(final_text)

def header_section():
    print_line()
    
    # Use the helper to print rows aligned perfectly
    print_info_row("DEVELOPER", "KEN DRICK")
    print_info_row("GITHUB", "RYO GRAHHH")
    print_info_row("VERSION", "1.0.0")
    print_info_row("FACEBOOK", "facebook.com/ryoevisu")
    print_info_row("TOOL'S NAME", "FB AUTO SHARER", is_highlighted=True)
    
    print_line()

def menu_option(number, letter, description, is_exit=False):
    """
    Helper to print menu options accurately.
    Format: [01/A] DESCRIPTION
    """
    # Create the key part: [01/A]
    # Brackets/Nums = White, Slash = Yellow (as per your code request), Letter = White
    key_text = Text("[", style="bold white")
    key_text.append(str(number), style="bold white")
    key_text.append("/", style="bold yellow") # Kept yellow per your previous code
    key_text.append(letter, style="bold white")
    key_text.append("]", style="bold white")

    # Description part
    if is_exit:
        desc_text = Text(f" {description}", style="bold red")
    else:
        desc_text = Text(f" {description}", style="bold green")

    console.print(key_text + desc_text)

def menu_section():
    menu_option("01", "A", "START AUTO SHARE")
    menu_option("02", "B", "JOIN FB GROUP")
    menu_option("03", "C", "JOIN FACEBOOK")
    menu_option("04", "D", "FOLLOW GITHUB")
    menu_option("00", "X", "BACK TO MAIN MENU", is_exit=True)
    
    print_line()

def main():
    while True:
        clear()
        print_banner()
        header_section()
        menu_section()
        
        # Input Prompt: [➤] CHOICE ➤ 
        # Using rich to construct the prompt styling
        prompt_text = Text("[", style="bold white")
        prompt_text.append("➤", style="bold white")
        prompt_text.append("]", style="bold white")
        prompt_text.append(" CHOICE ", style="bold cyan")
        prompt_text.append("➤ ", style="bold white")
        
        try:
            # explicit end="" so input matches the style
            choice = console.input(prompt_text).upper().strip()

            if choice in ['1', '01', 'A']:
                console.print("\n [bold green][!] Starting Auto Share...[/]")
                time.sleep(1)
            elif choice in ['0', '00', 'X']:
                console.print("\n [bold red][!] Exiting...[/]")
                sys.exit()
            else:
                console.print("\n [bold red][!] Invalid Selection[/]")
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            console.print("\n\n [bold red][!] Force Exit[/]")
            sys.exit()

if __name__ == "__main__":
    main()
