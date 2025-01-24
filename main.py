import shutil
import time
import os

def draw_border():
    columns, rows = shutil.get_terminal_size()
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen
    print("#" * columns)  # Top border
    for _ in range(rows - 2):
        print("#" + " " * (columns - 2) + "#")  # Side borders
    print("#" * columns)  # Bottom border

def monitor_terminal_size():
    prev_size = shutil.get_terminal_size()
    draw_border()  # Draw the initial border
    while True:
        time.sleep(0.5)  # Check terminal size every 0.5 seconds
        current_size = shutil.get_terminal_size()
        if current_size != prev_size:
            draw_border()  # Redraw border if size has changed
            prev_size = current_size

if __name__ == "__main__":
    monitor_terminal_size()
    