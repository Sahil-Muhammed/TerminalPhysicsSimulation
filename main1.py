import shutil
import time
import os
import threading
import math

# Shared variables
objects = []  
running = True  
gravity = 0.5  
elasticity = 1
direction = 1
# friction = 0

def draw_screen():
    """Draws the terminal border and objects."""
    columns, rows = shutil.get_terminal_size()
    os.system("cls" if os.name == "nt" else "clear")  

    print(f"Columns: {columns}, Rows: {rows}")
    print("\33[31m" + "#" * columns + "\33[0m")

    for row in range(2, rows - 1):
        line = [" "] * (columns - 2)  
        for obj in objects:
            if obj["y"] == row and 0 <= obj["x"] < columns - 2:
                line[int(obj["x"])] = obj["name"][0]  
        print("\33[31m" + "#" + "".join(line) + "#" + "\33[0m")  
    
    
    print("\33[31m" + "#" * columns + "\33[0m")

def update_objects():
    """Updates object positions based on their velocity, including gravity for vertical motion."""
    global running, gravity, direction
    columns, rows = shutil.get_terminal_size()
    ground_level = rows - 2  
    while running:
        for obj in objects:
            
            obj["velocity_y"] = direction*int(math.sqrt(2*gravity*obj["y"])) 

            obj["x"] += obj["velocity_x"]

            obj["y"] += obj["velocity_y"]

            # Bounce off the ground
            if obj["y"] >= ground_level:  
                obj["y"] = ground_level  
                direction *= -1
                obj["velocity_y"] *= elasticity*direction  # Reverse and apply elasticity to vertical velocity
                #gravity *= -1
                # obj["velocity_x"] *= friction

            # Bounce off walls (left and right)
            if obj["x"] <= 0 or obj["x"] >= columns - 3:  
                obj["velocity_x"] *= -1  # Reverse horizontal direction

        draw_screen()  
        time.sleep(0.1)  # Update every 100ms

def handle_user_input():
    """Handles CLI commands for the program."""
    global running, gravity
    while running:
        command = input("> ").strip()

        if command.lower() in {"exit", "quit"}:
            running = False  
        elif command.startswith("add"):
            try:
                # Parse the command: add <object_name> <x> <y> <velocity_x> <velocity_y>
                parts = command.split()
                if len(parts) == 6:
                    name = parts[1]
                    x = int(parts[2])
                    y = int(parts[3])
                    velocity_x = int(parts[4])  
                    velocity_y = 0  # Vertical velocity; ignoring vertical velocity for now
                elif len(parts) == 5:
                    columns, rows = os.get_terminal_size()
                    name = parts[1]
                    x = int(parts[2])
                    y = rows - int(parts[3]) - 1
                    velocity_x = int(parts[4])  
                    velocity_y = 0  
                else:
                    print("Usage: add <object_name> <x_position> <y_position> <velocity_x> <velocity_y>")
                    continue
                    
                objects.append({"name": name, "x": x, "y": y, "velocity_x": velocity_x, "velocity_y": velocity_y})
                print(f"Added object '{name}' at ({x}, {y}) with initial velocities (x: {velocity_x}, y: {velocity_y}).")
            except ValueError:
                print("Error: Invalid command format. Use integers for <x>, <y>, and velocities.")
        elif command.startswith("remove"):
            try:
                parts = command.split()
                if len(parts) != 2:
                    print("Incorrect syntax: need 2 arguments")
                else:
                    name = parts[1]
                    flag = -1
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
        elif command.startswith("set gravity"):
            try:
                parts = command.split()
                if len(parts) == 3:
                    gravity = int(parts[2])
                    print(f"Gravity set to {gravity}")
            except ValueError:
                print("Error: Invalid gravity value. Use an integer.")
        # elif command.startswith("set elasticity"): temporarily disabling elasticity
        #     try:
        #         parts = command.split()
        #         if len(parts) == 3:
        #             elasticity = float(parts[2])  # Set elasticity (0 to 1)
        #             print(f"Elasticity set to {elasticity}")
        #     except ValueError:
        #         print("Error: Invalid elasticity value. Use a float between 0 and 1.")
        else:
            print("Unknown command. Available commands: exit, add, remove, set gravity, set elasticity")

if __name__ == "__main__":
    updater_thread = threading.Thread(target=update_objects)
    updater_thread.daemon = True
    updater_thread.start()

    try:
        handle_user_input()
    except KeyboardInterrupt:
        running = False  # Graceful exit on Ctrl+C

    print("Exiting program...")
