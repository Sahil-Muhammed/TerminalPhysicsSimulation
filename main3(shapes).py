import shutil
import time
import os
import threading

# Shared variables
objects = []  
running = True  

gravity = 0.5  
elasticity = 1
friction = 1  

def draw_screen():
    """Draws the terminal border and objects."""
    columns, rows = shutil.get_terminal_size()
    os.system("cls" if os.name == "nt" else "clear") 

    print("\33[31m" + "#" * columns + "\33[0m")
    for row in range(2, rows - 1):
        line = [" "] * (columns - 2)  
        for obj in objects:
            if obj["y"] <= row < obj["y"] + obj["size"]:
                shape = obj["shape_func"](obj) 
                for dx, char in enumerate(shape[row - obj["y"]]):
                    if 0 <= obj["x"] + dx < columns - 2:
                        line[obj["x"] + dx] = char
        print("\33[31m" + "#" + "".join(line) + "#" + "\33[0m")  
    print("\33[31m" + "#" * columns + "\33[0m")

def generate_circle(obj):
    """Generate a circle representation as a list of strings."""
    radius = obj["size"]
    result = []
    for y in range(-radius, radius + 1):
        row = []
        for x in range(-radius, radius + 1):
            if x**2 + y**2 <= radius**2:
                row.append(obj["name"][0])
            else:
                row.append(" ")
        result.append("".join(row))
    return result

def generate_square(obj):
    """Generate a square representation as a list of strings."""
    size = obj["size"]
    return [obj["name"][0] * size for _ in range(size)]

def generate_ascii(obj):
    """Generate a single ASCII character."""
    return [obj["name"]]

SHAPE_FUNCTIONS = {
    "circle": generate_circle,
    "square": generate_square,
    "ascii": generate_ascii,
}

def update_objects():
    """Updates object positions based on their velocity and gravity."""
    global running
    columns, rows = shutil.get_terminal_size()
    ground_level = rows - 2  

    while running:
        for obj in objects:
            obj["y"] += gravity

            obj["x"] += obj["velocity_x"]

            if obj["y"] + obj["size"] >= ground_level:
                obj["y"] = ground_level - obj["size"]  
                obj["velocity_x"] *= friction

            if obj["x"] <= 0 or obj["x"] + obj["size"] >= columns - 2:
                obj["velocity_x"] *= -1  # Reverse horizontal direction
                obj["x"] = max(0, min(obj["x"], columns - 2 - obj["size"]))

        draw_screen()  
        time.sleep(0.1)  # Update every 100ms

def handle_user_input():
    """Handles CLI commands for the program."""
    global running
    while running:
        try:
            command = input("> ").strip()

            if command.lower() in {"exit", "quit"}:
                running = False  # Stop the program
            elif command.startswith("add"):
                # Parse the command: add <object_name> <x> <y> <velocity_x> <size> <shape>
                parts = command.split()
                if len(parts) == 7:
                    name = parts[1]
                    x = int(parts[2])
                    y = int(parts[3])
                    velocity_x = int(parts[4])
                    size = int(parts[5])
                    shape = parts[6].lower()
                    if shape not in SHAPE_FUNCTIONS:
                        print(f"Error: Unsupported shape '{shape}'. Use one of: {', '.join(SHAPE_FUNCTIONS.keys())}")
                        continue

                    # Add object to the list
                    objects.append({
                        "name": name,
                        "x": x,
                        "y": y,
                        "velocity_x": velocity_x,
                        "size": size,
                        "shape": shape,
                        "shape_func": SHAPE_FUNCTIONS[shape],
                    })
                    print(f"Added object '{name}' ({shape}) at ({x}, {y}) with size {size} and velocity ({velocity_x}).")
                else:
                    print("Usage: add <object_name> <x> <y> <velocity_x> <size> <shape>")
            elif command.startswith("remove"):
                parts = command.split()
                if len(parts) == 2:
                    name = parts[1]
                    objects[:] = [obj for obj in objects if obj["name"] != name]
                    print(f"Object '{name}' removed.")
                else:
                    print("Usage: remove <object_name>")
            else:
                print("Unknown command. Available commands: exit, add, remove")
        except ValueError:
            print("Error: Invalid command format.")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    updater_thread = threading.Thread(target=update_objects)
    updater_thread.daemon = True
    updater_thread.start()

    try:
        handle_user_input()
    except KeyboardInterrupt:
        running = False  # Graceful exit on Ctrl+C

    print("Exiting program...")
