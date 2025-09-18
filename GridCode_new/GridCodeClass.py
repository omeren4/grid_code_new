import tkinter as tk
from tkinter import messagebox, Canvas

# Constants
diameter_mm = 35
circle_radius = diameter_mm * 1000 / 2  # Convert mm to µm
line_thickness = 800  # µm
spacing = 2200  # µm
circle_global_coordinates = [23 * 10 ** 3, 23 * 10 ** 3]  # Needs to change to actual


def get_coordinates(row, col):
    """Calculate Cartesian coordinates of a square"""
    x = ((col - 1) if col >= 0 else col) * (spacing + line_thickness) + abs(line_thickness / 2)
    y = ((row - 1) if row >= 0 else row) * (spacing + line_thickness) + abs(line_thickness / 2)
    return x, y


def get_grid_square_from_markings(x_markings, x_shape, y_markings, y_shape):
    """Determine the square based on axis markings """
    col = x_markings if x_shape == "square" else -x_markings
    row = y_markings if y_shape == "square" else -y_markings
    return row, col


class GridSelector:
    def __init__(self, callback_function=None, parent=None):
        self.callback_function = callback_function
        self.parent = parent
        self.x_global = None
        self.y_global = None
        self.root = None
        self.x_shape_var = None
        self.y_shape_var = None
        self.x_markings_var = None
        self.y_markings_var = None
        self.delta_x_var = None
        self.delta_x_entry = None
        self.delta_y_var = None
        self.delta_y_entry = None
        self.canvas = None
        self.setup_gui()
        self.was_closed = False

    def select_grid_square(self):
        """Handle square selection and coordinate calculation"""
        try:
            x_markings = int(self.x_markings_var.get())
            y_markings = int(self.y_markings_var.get())
            x_shape = self.x_shape_var.get()
            y_shape = self.y_shape_var.get()
            delta_x = int(self.delta_x_entry.get())
            delta_y = int(self.delta_y_entry.get())

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
                self.x_global = circle_global_coordinates[0] + x_tag
                self.y_global = circle_global_coordinates[1] + y_tag

                messagebox.showinfo("Grid Square Selected",
                                    f"Selected grid square:\nRow: {row}, Column: {col}\n\n"
                                    f"Coordinates of desired point: \nX: {self.x_global * 10 ** -3: .3f} [mm]\nY: "
                                    f" {self.y_global * 10 ** -3: .3f} [mm]")

                # Call the callback function if provided
                if self.callback_function:
                    self.callback_function(self.x_global, self.y_global)

                self.cleanup()

            else:
                messagebox.showwarning("Out of Bounds", "The selected grid square is outside the circle!")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def draw_grid(self):
        """Draw the grid square and markings"""
        self.canvas.delete("all")
        canvas_width = 200
        canvas_height = 200

        # Draw the grid square
        self.canvas.create_rectangle(50, 50, canvas_width + 50, canvas_height + 50, fill="lightblue", outline="black")

        # Draw markings on the X-axis
        x_markings = int(self.x_markings_var.get())
        x_shape = self.x_shape_var.get()
        if x_markings > 0:
            spacing_x = canvas_width / (x_markings + 1)
            for i in range(1, x_markings + 1):
                x_pos = 50 + i * spacing_x
                if x_shape == "square":
                    self.canvas.create_rectangle(x_pos - 8, 242, x_pos + 8, 258, fill="black")
                elif x_shape == "circle":
                    self.canvas.create_oval(x_pos - 8, 242, x_pos + 8, 258, fill="black")

        # Draw markings on the Y-axis
        y_markings = int(self.y_markings_var.get())
        y_shape = self.y_shape_var.get()
        if y_markings > 0:
            spacing_y = canvas_height / (y_markings + 1)
            for i in range(1, y_markings + 1):
                y_pos = 250 - i * spacing_y
                if y_shape == "square":
                    self.canvas.create_rectangle(42, y_pos - 8, 58, y_pos + 8, fill="black")
                elif y_shape == "circle":
                    self.canvas.create_oval(42, y_pos - 8, 58, y_pos + 8, fill="black")

        # ---------- draw the point on square ---------------------------------
        try:
            delta_x_val = int(self.delta_x_var.get())
            delta_y_val = int(self.delta_y_var.get())
        except ValueError:
            # ignore until the user types a valid integer
            return

        # Only draw if the deltas are within the current square
        if 0 <= delta_x_val <= spacing and 0 <= delta_y_val <= spacing:
            # convert µm → canvas pixels (200 px maps to spacing µm)
            x_ratio = delta_x_val / spacing
            y_ratio = delta_y_val / spacing

            # canvas coords: left = 50, right = 250 ; top = 50, bottom = 250
            x_px = 50 + x_ratio * 200
            y_px = 250 - y_ratio * 200  # invert Y (canvas grows downward)

            # a small red cross
            self.canvas.create_line(x_px - 5, y_px, x_px + 5, y_px,
                                    fill="red", width=2)
            self.canvas.create_line(x_px, y_px - 5, x_px, y_px + 5,
                                    fill="red", width=2)

    def setup_gui(self):
        """Set up the GUI components"""
        if self.parent is None:
            self.root = tk.Tk()
        else:
            self.root = tk.Toplevel(self.parent)

        self.root.title("Grid Selector")
        self.root.protocol("WM_DELETE_WINDOW", self.x_button_pressed)

        # Input fields and labels
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="X-axis mark shape:").grid(row=0, column=0, padx=5, pady=5)
        self.x_shape_var = tk.StringVar(master=self.root, value="square")
        x_shape_menu = tk.OptionMenu(input_frame, self.x_shape_var, "square", "circle")
        x_shape_menu.grid(row=0, column=1, padx=5, pady=5)

        self.x_markings_var = tk.StringVar(master=self.root, value="1")
        tk.Label(input_frame, text="Number of marks on X:").grid(row=1, column=0, padx=5, pady=5)
        x_markings_menu = tk.OptionMenu(input_frame, self.x_markings_var, *[str(i) for i in range(1, 7)])
        x_markings_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Y-axis mark shape:").grid(row=3, column=0, padx=5, pady=5)
        self.y_shape_var = tk.StringVar(master=self.root, value="square")
        y_shape_menu = tk.OptionMenu(input_frame, self.y_shape_var, "square", "circle")
        y_shape_menu.grid(row=3, column=1, padx=5, pady=5)

        self.y_markings_var = tk.StringVar(master=self.root, value="1")
        tk.Label(input_frame, text="Number of marks on Y:").grid(row=4, column=0, padx=5, pady=5)
        y_markings_menu = tk.OptionMenu(input_frame, self.y_markings_var, *[str(i) for i in range(1, 7)])
        y_markings_menu.grid(row=4, column=1, padx=5, pady=5)

        self.delta_x_var = tk.StringVar(master=self.root, value="0")
        tk.Label(input_frame, text="Input delta X:").grid(row=6, column=0, padx=5, pady=5)
        self.delta_x_entry = tk.Entry(input_frame, textvariable=self.delta_x_var)
        self.delta_x_entry.grid(row=6, column=1, padx=5, pady=5)

        self.delta_y_var = tk.StringVar(master=self.root, value="0")
        tk.Label(input_frame, text="Input delta Y:").grid(row=7, column=0, padx=5, pady=5)
        self.delta_y_entry = tk.Entry(input_frame, textvariable=self.delta_y_var)
        self.delta_y_entry.grid(row=7, column=1, padx=5, pady=5)

        # Canvas for grid visualization
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(pady=10)
        self.canvas = Canvas(canvas_frame, width=300, height=300, bg="white")
        self.canvas.pack()

        # Submit button
        submit_button = tk.Button(self.root, text="Select Grid Square", command=self.select_grid_square)
        submit_button.pack(pady=10)

        # Update grid drawing when inputs change
        def update_grid(*args):
            self.draw_grid()

        self.x_markings_var.trace("w", update_grid)
        self.y_markings_var.trace("w", update_grid)
        self.x_shape_var.trace("w", update_grid)
        self.y_shape_var.trace("w", update_grid)

        self.delta_x_var.trace("w", update_grid)
        self.delta_y_var.trace("w", update_grid)

        # Initial grid drawing
        self.draw_grid()

    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()

    def get_final_coordinates_mm(self):
        """Return the current global coordinates in mm"""
        x = self.x_global/10**3
        y = self.y_global / 10 ** 3
        return x, y

    def x_button_pressed(self):
        self.was_closed = True
        self.cleanup()

    def cleanup(self):
        """Properly cleanup the GUI"""
        if self.root and self.root.winfo_exists():
            self.root.quit()
            self.root.destroy()
        self.root = None


# For backward compatibility and standalone running
if __name__ == "__main__":
    grid_selector = GridSelector()
    grid_selector.run()
