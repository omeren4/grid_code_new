from axesInitializer import initialize_axes, axis_position
import time
import keyboard


class AxisController:
    """
    Manages the three axes for disc placement operations.
    Provides convenient access to individual axes and bulk operations.
    """

    def __init__(self):
        self.axes = initialize_axes()
        self.is_manual_mode = False

    @property
    def x_axis(self):
        """Returns the X-axis (axis1) """
        return self.axes[0]

    @property
    def y_axis(self):
        """Returns the Y-axis (axis2)"""
        return self.axes[1]

    @property
    def z_axis(self):
        """Returns the Z-axis (axis3)"""
        return self.axes[2]

    def open_all(self):
        """Opens all axis devices"""
        for axis in self.axes:
            axis.open_device()

    def close_all(self):
        """Closes all axis devices"""
        for axis in self.axes:
            axis.close_device()

    def print_all_positions(self):
        """Prints the current position of all axes"""
        print("\nX-axis position:")
        axis_position(self.x_axis)
        print("\nY-axis position:")
        axis_position(self.y_axis)
        print("\nZ-axis position:")
        axis_position(self.z_axis)

    def place_disc(self, coordinates):
        self.z_axis.command_move(coordinates.z_top_step, 0)
        self.z_axis.command_wait_for_stop(100)
        self.x_axis.command_move(coordinates.x_step, 0)
        self.y_axis.command_move(coordinates.y_step, 0)
        self.x_axis.command_wait_for_stop(100)
        self.y_axis.command_wait_for_stop(100)
        self.z_axis.command_move(coordinates.z_bottom_step, 0)
        self.z_axis.command_wait_for_stop(100)

    def disc_load_position(self, coordinates):
        self.z_axis.command_move(coordinates.z_top_step, 0)
        self.z_axis.command_wait_for_stop(100)
        self.x_axis.command_move(coordinates.x_disc_load_step, 0)
        self.y_axis.command_move(coordinates.y_disc_load_step, 0)
        self.x_axis.command_wait_for_stop(100)
        self.y_axis.command_wait_for_stop(100)
        self.z_axis.command_move(coordinates.z_disc_load_step, 0)
        self.z_axis.command_wait_for_stop(100)

    def home_xy(self):
        self.z_axis.command_movr(20*4000, 0)     # so end effector won't hit something
        self.z_axis.command_wait_for_stop(100)
        self.x_axis.command_home()
        self.y_axis.command_home()
        self.x_axis.command_wait_for_stop(100)
        self.y_axis.command_wait_for_stop(100)

    def home_z(self):
        self.z_axis.command_home()
        self.z_axis.command_wait_for_stop(100)

    def set_zero_x(self):
        self.x_axis.command_zero()
        self.x_axis.command_wait_for_stop(100)

    def set_zero_y(self):
        self.y_axis.command_zero()
        self.y_axis.command_wait_for_stop(100)

    def set_zero_z(self):
        self.z_axis.command_zero()
        self.z_axis.command_wait_for_stop(100)

    def start_manual_control(self):
        """Start keyboard control mode"""
        self.is_manual_mode = True
        print("Manual control activated!")
        print("  Controls:")
        print("  Left/Right arrows: X axis")
        print("  Up/Down arrows: Y axis")
        print("  +/-: Z axis")
        print("  ESC: Exit manual mode")
        print("  P: Print current positions")
        print()

        # Track which keys were pressed in the previous loop
        prev_keys = {
            'left': False, 'right': False, 'up': False, 'down': False,
            'plus': False, 'minus': False
        }
        relative_steps = -400000

        while self.is_manual_mode:
            try:
                # Current key states
                current_keys = {
                    'left': keyboard.is_pressed('left'),
                    'right': keyboard.is_pressed('right'),
                    'up': keyboard.is_pressed('up'),
                    'down': keyboard.is_pressed('down'),
                    'plus': keyboard.is_pressed('+') or keyboard.is_pressed('='),
                    'minus': keyboard.is_pressed('-')
                }

                # X-axis control
                if current_keys['left'] and not prev_keys['left']:
                    # Just started pressing left
                    self.x_axis.command_movr(relative_steps, 0)
                elif not current_keys['left'] and prev_keys['left']:
                    # Just released left
                    self.x_axis.command_sstp()

                if current_keys['right'] and not prev_keys['right']:
                    # Just started pressing right
                    self.x_axis.command_movr(-relative_steps, 0)
                elif not current_keys['right'] and prev_keys['right']:
                    # Just released right
                    self.x_axis.command_sstp()

                # Y-axis control
                if current_keys['up'] and not prev_keys['up']:
                    # Just started pressing up
                    self.y_axis.command_movr(-relative_steps, 0)
                elif not current_keys['up'] and prev_keys['up']:
                    # Just released up
                    self.y_axis.command_sstp()

                if current_keys['down'] and not prev_keys['down']:
                    # Just started pressing down
                    self.y_axis.command_movr(relative_steps, 0)
                elif not current_keys['down'] and prev_keys['down']:
                    # Just released down
                    self.y_axis.command_sstp()

                # Z-axis control
                if current_keys['plus'] and not prev_keys['plus']:
                    # Just started pressing +
                    self.z_axis.command_movr(-relative_steps, 0)
                elif not current_keys['plus'] and prev_keys['plus']:
                    # Just released +
                    self.z_axis.command_sstp()

                if current_keys['minus'] and not prev_keys['minus']:
                    # Just started pressing -
                    self.z_axis.command_movr(relative_steps, 0)
                elif not current_keys['minus'] and prev_keys['minus']:
                    # Just released -
                    self.z_axis.command_sstp()

                # Other controls
                if keyboard.is_pressed('p'):
                    self.print_all_positions()
                    time.sleep(0.3)  # Longer delay for position printing

                if keyboard.is_pressed('esc'):
                    self.stop_manual_control()

                # Update previous key states
                prev_keys = current_keys.copy()

                time.sleep(0.05)  # Small delay to prevent excessive CPU usage

            except KeyboardInterrupt:
                self.stop_manual_control()

    def stop_manual_control(self):
        """Stop keyboard control mode and stop all axes"""
        self.is_manual_mode = False
        # Stop all axes when exiting manual mode
        self.x_axis.command_sstp()
        self.y_axis.command_sstp()
        self.z_axis.command_sstp()
        print("\nManual control deactivated! All axes stopped.")
