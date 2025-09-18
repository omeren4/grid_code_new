class Coordinates:

    """
    Args:
        x (float): X coordinate in millimeters from grid selector
        y (float): Y coordinate in millimeters from grid selector
    """

    def __init__(self, x, y):
        # Convert mm to steps (X,Y 8000 steps per mm)
        self.x_step = -int(x * 8000)
        self.y_step = -int(y * 8000)
        #  (Z 4000 steps per mm)
        self.z_top_step = 60000
        self.z_bottom_step = -12400

        # Disc Loading Position parameters in steps
        self.x_disc_load_step = 296000
        self.y_disc_load_step = -184000
        self.z_disc_load_step = self.z_bottom_step + 2000
