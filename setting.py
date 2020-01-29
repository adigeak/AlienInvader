class Setting():
    """A class to store the settings for Alien invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Setting the screen
        self.screen_width = 1500
        self.screen_height = 1000
        self.bg_color = (119,120,230)
        self.bg_image = "images/stars.bmp"
        # speed of ship
        self.ship_speed_factor = 2.5
        # Bullet settings
        self.bullet_speed_factor = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        # self.bullet_color = 60,60,60
        self.bullet_color = 250,250,250
        self.bullet_allowed = 5
        # Alien settings
        self.alien_speed_factor = 1.2
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1