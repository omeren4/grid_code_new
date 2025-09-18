import tkinter as tk


class ModeSelector:
    def __init__(self, parent=None):
        self.selection = None
        if parent is None:
            self.root = tk.Tk()
        else:
            self.root = tk.Toplevel(parent)
        self.root.title("Select Operation Mode")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        tk.Label(self.root, text="Choose a mode:", font=("Helvetica", 14)).pack(padx=35, pady=15)

        tk.Button(self.root, text="Input Placement Coordinates", width=25, height=2,
                  command=lambda: self.select("placement coordinates")).pack(pady=5)

        tk.Button(self.root, text="Go to Loading Station", width=25, height=2,
                  command=lambda: self.select("loading position")).pack(pady=5)

        tk.Button(self.root, text="Manual Control", width=25, height=2,
                  command=lambda: self.select("manual control")).pack(pady=5)

        home_frame = tk.Frame(self.root)
        home_frame.pack(pady=5)

        tk.Button(home_frame, text="XY Home Calibration", width=19, height=2,
                  command=lambda: self.select("XY home")).pack(side="left", padx=1)

        tk.Button(home_frame, text="Z Home Calibration", width=19, height=2,
                  command=lambda: self.select("Z home")).pack(side="left", padx=1)

        zero_frame = tk.Frame(self.root)
        zero_frame.pack(pady=5, padx=5)

        tk.Button(zero_frame, text="Zero X & Y Positions", width=19, height=2,
                  command=lambda: self.select("zero XY")).pack(side="left", padx=1)

        tk.Button(zero_frame, text="Zero Z Position", width=19, height=2,
                  command=lambda: self.select("zero Z")).pack(side="left", padx=1)

        tk.Button(self.root, text="EXIT", width=5, height=1,
                  command=lambda: self.select("exit")).pack(pady=10)

    def select(self, mode):
        self.selection = mode
        self.root.quit()

    def get_selection(self):
        # if self.root.winfo_exists():  # Check if window still exists
        self.root.mainloop()
        self.root.destroy()
        return self.selection

    def _on_close(self):
        """User clicked the ✕ button"""
        self.selection = None
        self.root.quit()


# For standalone testing
if __name__ == "__main__":
    selector = ModeSelector()
    choice = selector.get_selection()
    print("You selected:", choice)
