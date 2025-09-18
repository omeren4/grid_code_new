import tkinter as tk
from tkinter import messagebox, Canvas

# Constants
diameter_mm = 35
circle_radius = diameter_mm * 1000 / 2  # Convert mm to µm
line_thickness = 800  # µm
spacing = 2200  # µm
circle_global_coordinates = [23 * 10 ** 3, 23 * 10 ** 3]  # Needs to change to actual


def get_coordinates(row, col):
    # Function to calculate Cartesian coordinates of a square
    x = ((col - 1) if col >= 0 else col) * (spacing + line_thickness) + abs(line_thickness / 2)
    y = ((row - 1) if row >= 0 else row) * (spacing + line_thickness) + abs(line_thickness / 2)
    return x, y


def get_grid_square_from_markings(x_markings, x_shape, y_markings, y_shape):
    # Function to determine the square based on axis markings.
    col = x_markings if x_shape == "square" else -x_markings
    row = y_markings if y_shape == "square" else -y_markings
    return row, col


# Function to handle square selection
def select_grid_square():
    try:
        x_markings = int(x_markings_var.get())
        y_markings = int(y_markings_var.get())
        x_shape = x_shape_var.get()
        y_shape = y_shape_var.get()
        delta_x = int(delta_x_entry.get())
        delta_y = int(delta_y_entry.get())

        if x_shape not in ["square", "circle"] or y_shape not in ["square", "circle"]:
            raise ValueError("Invalid shape selection")

        # Check if deltas are in a grid square
        if delta_x > (spacing + line_thickness) or delta_y > (spacing + line_thickness):
            raise ValueError("Delta out of scope!")

        row, col = get_grid_square_from_markings(x_markings, x_shape, y_markings, y_shape)
        x, y = get_coordinates(row, col)

        # Check if the bottom-left corner is inside the circle
        if x ** 2 + y ** 2 <= circle_radius ** 2:
            # Desired placement coordinates on grid
            x_tag = x + delta_x
            y_tag = y + delta_y
            [x_global, y_global] = [circle_global_coordinates[0] + x_tag, circle_global_coordinates[1] + y_tag]

            messagebox.showinfo("Grid Square Selected",
                                f"Selected grid square:\nRow: {row}, Column: {col}\n\n"
                                f"Global coordinates of point on grid: \nX: {x_global * 10 ** -3: .3f} [mm]\nY: "
                                f" {y_global * 10 ** -3: .3f} [mm]")
        else:
            messagebox.showwarning("Out of Bounds", "The selected grid square is outside the circle!")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")


# Function to draw the grid square and markings
def draw_grid(grid_canvas):
    grid_canvas.delete("all")
    canvas_width = 200
    canvas_height = 200

    # Draw the grid square
    grid_canvas.create_rectangle(50, 50, canvas_width + 50, canvas_height + 50, fill="lightblue", outline="black")

    # Draw markings on the X-axis
    x_markings = int(x_markings_var.get())
    x_shape = x_shape_var.get()
    if x_markings > 0:
        spacing_x = canvas_width / (x_markings + 1)
        for i in range(1, x_markings + 1):
            x_pos = 50 + i * spacing_x
            if x_shape == "square":
                grid_canvas.create_rectangle(x_pos - 8, 242, x_pos + 8, 258, fill="black")
            elif x_shape == "circle":
                grid_canvas.create_oval(x_pos - 8, 242, x_pos + 8, 258, fill="black")

    # Draw markings on the Y-axis
    y_markings = int(y_markings_var.get())
    y_shape = y_shape_var.get()
    if y_markings > 0:
        spacing_y = canvas_height / (y_markings + 1)
        for i in range(1, y_markings + 1):
            y_pos = 250 - i * spacing_y
            if y_shape == "square":
                grid_canvas.create_rectangle(42, y_pos - 8, 58, y_pos + 8, fill="black")
            elif y_shape == "circle":
                grid_canvas.create_oval(42, y_pos - 8, 58, y_pos + 8, fill="black")


# GUI setup

root = tk.Tk()

root.title("Grid Selector")

# Input fields and labels
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="X-axis mark shape:").grid(row=0, column=0, padx=5, pady=5)
x_shape_var = tk.StringVar(value="square")
x_shape_menu = tk.OptionMenu(input_frame, x_shape_var, "square", "circle")
x_shape_menu.grid(row=0, column=1, padx=5, pady=5)

x_markings_var = tk.StringVar(value="1")
tk.Label(input_frame, text="Number of marks on X:").grid(row=1, column=0, padx=5, pady=5)
x_markings_menu = tk.OptionMenu(input_frame, x_markings_var, *[str(i) for i in range(1, 7)])
x_markings_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Y-axis mark shape:").grid(row=3, column=0, padx=5, pady=5)
y_shape_var = tk.StringVar(value="square")
y_shape_menu = tk.OptionMenu(input_frame, y_shape_var, "square", "circle")
y_shape_menu.grid(row=3, column=1, padx=5, pady=5)

y_markings_var = tk.StringVar(value="1")
tk.Label(input_frame, text="Number of marks on Y:").grid(row=4, column=0, padx=5, pady=5)
y_markings_menu = tk.OptionMenu(input_frame, y_markings_var, *[str(i) for i in range(1, 7)])
y_markings_menu.grid(row=4, column=1, padx=5, pady=5)

delta_x_var = tk.StringVar(value="0")  # Set the default value to "0"
tk.Label(input_frame, text="Input delta X:").grid(row=6, column=0, padx=5, pady=5)
delta_x_entry = tk.Entry(input_frame, textvariable=delta_x_var)
delta_x_entry.grid(row=6, column=1, padx=5, pady=5)

delta_y_var = tk.StringVar(value="0")  # Set the default value to "0"
tk.Label(input_frame, text="Input delta Y:").grid(row=7, column=0, padx=5, pady=5)
delta_y_entry = tk.Entry(input_frame, textvariable=delta_y_var)  # Bind the StringVar to the Entry
delta_y_entry.grid(row=7, column=1, padx=5, pady=5)

# Canvas for grid visualization
canvas_frame = tk.Frame(root)

canvas_frame.pack(pady=10)
canvas = Canvas(canvas_frame, width=300, height=300, bg="white")
canvas.pack()

# Submit button
submit_button = tk.Button(root, text="Select Grid Square", command=select_grid_square)
submit_button.pack(pady=10)


# Update grid drawing when inputs change
def update_grid(*args):
    draw_grid(canvas)


x_markings_var.trace("w", update_grid)
y_markings_var.trace("w", update_grid)
x_shape_var.trace("w", update_grid)
y_shape_var.trace("w", update_grid)

# Initial grid drawing
draw_grid(canvas)

root.mainloop()
