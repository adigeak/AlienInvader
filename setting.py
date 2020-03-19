class Setting():
    """A class to store the settings for Alien invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Setting the screen
        self.screen_width = 1500
        self.screen_height = 1000
        self.bg_color = (119,120,230)
        self.bg_image = "images/stars.bmp"

        # ship Setting
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        # self.bullet_color = 60,60,60
        self.bullet_color = 250,250,250
        self.bullet_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # score scale up
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that changes throughout the game."""
        self.ship_speed_factor = 2.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.2

        # Scoring
        self.alien_points= 10

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)