import os
import sys
import time
from rich.console import Console
from rich.text import Text

# Initialize Rich Console
console = Console()

# --- CONSTANTS ---
LABEL_WIDTH = 12 
SEPARATOR_LINE = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

def clear():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    """Prints a single menu option."""
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
    Prints menu options one by one with a small delay
    to create a 'loading' or 'waterfall' animation.
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
        time.sleep(0.05) # Small delay between lines appearing
    
    print_line()

def type_print(text, style, delay=0.03):
    """Helper to type out text char-by-char without newline."""
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)

def animated_input():
    """
    Manually types out the prompt: [➤] CHOICE ➤ 
    Then waits for input.
    """
    # 1. Type the first bracket part [➤]
    console.print(" [", style="bold white", end="")
    time.sleep(0.05)
    console.print("➤", style="bold white", end="")
    time.sleep(0.05)
    console.print("]", style="bold white", end="")
    
    # 2. Type " CHOICE "
    type_print(" CHOICE ", style="bold cyan", delay=0.05)
    
    # 3. Type the arrow ➤ 
    console.print("➤ ", style="bold white", end="")
    
    # 4. Actual input capture
    return input("").upper().strip()

def main():
    while True:
        clear()
        print_banner()
        header_section()
        
        # Animate the menu items appearing one by one
        menu_section_animated()
        
        try:
            # Use the custom typing input function
            choice = animated_input()

            if choice in ['1', '01', 'A']:
                console.print("\n [bold green][!] Starting Auto Share...[/]")
                
                # Example: If you need inputs inside here, use the same logic
                # console.print("\n [bold yellow]Enter Cookies:[/]", end=" ")
                # cookie = input() 
                
                time.sleep(2)
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
