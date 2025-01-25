import shutil
import time
import os
import threading

object  = {}
running = True

def draw_border():
    columns, rows = shutil.get_terminal_size()
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen
    print("-" * columns)  # Top border
    for _ in range(rows - 2):
        print("|" + " " * (columns - 2) + "|")  # Side borders
    print("-" * columns)  # Bottom border

def monitor_terminal_size():
    prev_size = shutil.get_terminal_size()
    draw_border()  # Draw the initial border
    while True:
        time.sleep(0.5)  # Check terminal size every 0.5 seconds
        current_size = shutil.get_terminal_size()
        if current_size != prev_size:
            draw_border()  # Redraw border if size has changed
            prev_size = current_size

def handle_user_input():
    """Handles CLI commands for the program."""
    global running, objects
    while running:
        command = input("> ").strip()
        if command.lower() in {"exit", "quit"}:
            running = False  # Stop the program
        elif command.startswith("spawn"):
            try:
                # Example: spawn 10 5 O
                parts = command.split()
                if len(parts) == 4:
                    x = int(parts[1])  # Column
                    y = int(parts[2])  # Row
                    char = parts[3]
                    if y not in objects:
                        objects[y] = {}
                    objects[y][x] = char
                    draw_border()
                else:
                    print("Usage: spawn <x> <y> <char>")
            except ValueError:
                print("Invalid coordinates. Use integers for <x> and <y>.")
        else:
            print("Unknown command. Available commands: exit, spawn <x> <y> <char>")

if __name__ == "__main__":
    # Start the border drawing in a separate thread
    border_thread = threading.Thread(target=monitor_terminal_size)
    border_thread.daemon = True
    border_thread.start()

    # Handle user input in the main thread
    try:
        handle_user_input()
    except KeyboardInterrupt:
        running = False  # Graceful exit on Ctrl+C

    print("Exiting program...")
    