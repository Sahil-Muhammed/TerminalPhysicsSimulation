# import shutil
# import time
# import os
# import threading

# objects  = {}
# running = True

# def draw_border():
#     columns, rows = shutil.get_terminal_size()
#     os.system("cls" if os.name == "nt" else "clear")  # Clear screen
#     print("-" * columns)  # Top border
#     for _ in range(rows - 2):
#         print("|" + " " * (columns - 2) + "|")  # Side borders
#     print("-" * columns)  # Bottom border

# def monitor_terminal_size():
#     prev_size = shutil.get_terminal_size()
#     draw_border()  # Draw the initial border
#     while True:
#         time.sleep(0.5)  # Check terminal size every 0.5 seconds
#         current_size = shutil.get_terminal_size()
#         if current_size != prev_size:
#             draw_border()  # Redraw border if size has changed
#             prev_size = current_size

# def handle_user_input():
#     """Handles CLI commands for the program."""
#     global running, objects
#     while running:
#         command = input("@Makhachev$ ").strip()
#         if command.lower() in {"exit", "quit"}:
#             running = False  # Stop the program
#         elif command.startswith("spawn"):
#             try:
#                 # Example: spawn 10 5 O
#                 parts = command.split()
#                 if len(parts) == 4:
#                     x = int(parts[1])  # Column
#                     y = int(parts[2])  # Row
#                     char = parts[3]
#                     if y not in objects:
#                         objects[y] = {}
#                     objects[y][x] = char
#                     draw_border()
#                 else:
#                     print("Usage: spawn <x> <y> <char>")
#             except ValueError:
#                 print("Invalid coordinates. Use integers for <x> and <y>.")
#         else:
#             print("Unknown command. Available commands: exit, spawn <x> <y> <char>")

# def animate_colored_object():
#     for i in range(20):
#         os.system("cls" if os.name == "nt" else "clear")
#         print("\033[31m" + " " * i + "O" + "\033[0m")  # Red "O"
#         time.sleep(0.1)

# if __name__ == "__main__":
#     # Start the border drawing in a separate thread
#     border_thread = threading.Thread(target=monitor_terminal_size)
#     border_thread.daemon = True
#     border_thread.start()
#     animate_colored_object()
#     # Handle user input in the main thread
#     try:
#         handle_user_input()
#     except KeyboardInterrupt:
#         running = False  # Graceful exit on Ctrl+C

#     print("Exiting program...")
import shutil
import time
import os
import threading

# Shared variables
objects = []  # List to store all objects
running = True  # Global flag to control program termination

def draw_screen():
    """Draws the terminal border and objects."""
    columns, rows = shutil.get_terminal_size()
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen

    # Draw top border
    print("#" * columns)
    
    # Draw middle rows
    for row in range(1, rows - 1):
        line = [" "] * (columns - 2)  # Empty line for the row
        # Place objects in this row
        for obj in objects:
            if obj["y"] == row and 0 <= obj["x"] < columns - 2:
                line[obj["x"]] = obj["name"][0]  # Use the first letter of the object's name
        print("#" + "".join(line) + "#")  # Print the line with borders
    
    # Draw bottom border
    print("#" * columns)

def update_objects():
    """Updates object positions based on their velocity."""
    global running
    columns, _ = shutil.get_terminal_size()
    while running:
        for obj in objects:
            # Update position
            obj["x"] += obj["velocity"]
            # Bounce off walls
            if obj["x"] <= 0 or obj["x"] >= columns - 3:  # Adjust for border
                obj["velocity"] *= -1  # Reverse direction
        draw_screen()
        time.sleep(0.2)  # Update every 200ms

def handle_user_input():
    """Handles CLI commands for the program."""
    global running
    while running:
        command = input("> ").strip()
        if command.lower() in {"exit", "quit"}:
            running = False  # Stop the program
        elif command.startswith("add"):
            try:
                # Parse the command: add <object_name> <x> <y> <velocity>
                parts = command.split()
                if len(parts) == 5:
                    # Validate coordinates
                    columns, rows = shutil.get_terminal_size()
                    name = parts[1]
                    x = int(parts[2])
                    y = rows - int(parts[3]) - 1
                    velocity = int(parts[4])
                    if y <= 0 or y >= rows - 1:
                        print("Error: y-coordinate is out of bounds.")
                        continue
                    # Add object to the list
                    objects.append({"name": name, "x": x, "y": y, "velocity": velocity})
                    print(f"Added object '{name}' at ({parts[2]}, {parts[3]}) with velocity {parts[4]}.")
                else:
                    print("Usage: add <object_name> <x_position> <y_position> <horizontal_velocity>")
            except ValueError:
                print("Error: Invalid command format. Use integers for <x>, <y>, and <velocity>.")
        elif command.startswith("remove"):
            try:
                parts = command.split()
                flag = -1;
                if len(parts) != 2:
                    print("Incorrect syntax: need 2 arguments")
                else:
                    name = parts[1]
                    for obj in objects:
                        if obj["name"] == name:
                            objects.remove(obj)
                            flag = 1
                    if flag == -1:
                        print("Object not found")
                    else:
                        print(f"Object '{name}' removed successfully.")
            except ValueError:
                    print("Error: Invalid command format.")
        else:
            print("Unknown command. Available commands: exit, add <object_name> <x> <y> <velocity>")

if __name__ == "__main__":
    # Start the object updater in a separate thread
    updater_thread = threading.Thread(target=update_objects)
    updater_thread.daemon = True
    updater_thread.start()

    # Handle user input in the main thread
    try:
        handle_user_input()
    except KeyboardInterrupt:
        running = False  # Graceful exit on Ctrl+C

    print("Exiting program...")
