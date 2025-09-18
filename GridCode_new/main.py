from GridCodeClass import GridSelector
from CoordinateClass import Coordinates
from axis_controller import AxisController
from mode_selector import ModeSelector
import tkinter as tk
import tkinter.messagebox as msgbox


def main():

    main_root = tk.Tk()  # Create a main root for all others
    main_root.withdraw()  # Hide the main root window

    # Step 1: Initialize motors
    # AxisController initializes the axes and offers functions to operate them
    control = AxisController()
    control.open_all()

    while True:

        mode_selector = ModeSelector(parent=main_root)
        mode = mode_selector.get_selection()

        """"clean up to allow proper loop"""
        del mode_selector

        if mode == "placement coordinates":
            # Get coordinates from user
            grid = GridSelector(parent=main_root)
            grid.run()
            if grid.was_closed:
                del grid
                continue
            x, y = grid.get_final_coordinates_mm()
            coordinates = Coordinates(x, y)

            """"clean up to allow proper loop"""
            del grid

            # # control the stage to place disc in desired coordinates
            control.place_disc(coordinates)
            control.print_all_positions()

        elif mode == "manual control":
            # ***************************** #
            # *******MANUAL CONTROL******** #

            control.start_manual_control()

            # ***************************** #

        elif mode == "loading position":

            # Move to loading area coordinates
            dummy = Coordinates(0, 0)
            control.disc_load_position(dummy)

        elif mode == "XY home":
            control.home_xy()

        elif mode == "Z home":
            control.home_z()

        elif mode == "zero XY":
            control.set_zero_x()
            control.set_zero_y()
            control.print_all_positions()

        elif mode == "zero Z":
            control.set_zero_z()
            control.print_all_positions()

        elif mode is None or mode == "exit":
            break

        # Step 3: Ask whether to repeat or exit
        result = msgbox.askquestion(
            "Operation Complete",
            f"Mode '{mode}' completed.\n\nWould you like to return to the main menu?"
        )

        if result != 'yes':
            main_root.destroy()
            break  # Exit loop

    # Final Step: close all axes
    control.close_all()
    print("Program Exited.")


if __name__ == "__main__":
    main()
