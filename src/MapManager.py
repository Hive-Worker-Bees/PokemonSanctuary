from random import choice


class Background():
    """
    Manage background images
    """

    def __init__(self, name, image, pokemonSpawns, interesting_regions, disallowed_regions, danger_regions):
        self._name = name
        self._image = image
        self._pokemonSpawns = pokemonSpawns
        self._left = None
        self._left_bounds = None
        self._right = None
        self._right_bounds = None
        self._beneath = None
        self._beneath_bounds = None
        self._above = None
        self._above_bounds = None
        self._interesting_regions = interesting_regions
        self._disallowed_regions = disallowed_regions
        self._danger_regions = danger_regions

    def get_name(self):
        """
        Get zone name
        """
        return self._name

    def get_image(self):
        """
        Get file path to image PNG
        """
        return self._image

    def get_all_pokemon_spawns(self):
        """
        Get all coordinates deemed suitable for Pokemon spawns
        """
        return self._pokemonSpawns

    def get_random_pokemon_spawn(self):
        """
        Get a random set of coordinates deemed suitable for Pokemon spawns
        """
        return choice(self.get_all_pokemon_spawns())

    def set_left(self, left, lower, upper):
        """
        Set the zone which should appear when a player exits this zone to the left
        """
        self._left = left
        self._left_bounds = (lower, upper)

    def get_left(self):
        """
        Get the zone which will appear when a player exits this zone to the left

        Returns None if no zone is set
        """
        return self._left

    def get_left_bounds(self):
        """
        Get the region where a user can proceed to the next zone on the left

        Returns None if no zone is set
        """
        return self._left_bounds

    def set_right(self, right, lower, upper):
        """
        Set the zone which should appear when a player exits this zone to the right
        """
        self._right = right
        self._right_bounds = (lower, upper)

    def get_right(self):
        """
        Get the zone which will appear when a player exits this zone to the right

        Returns None if no zone is set
        """
        return self._right

    def get_right_bounds(self):
        """
        Get the region where a user can proceed to the next zone on the right

        Returns None if no zone is set
        """
        return self._right_bounds

    def set_beneath(self, beneath, lower, upper):
        """
        Set the zone which should appear when a player exits this zone at the bottom
        """
        self._beneath = beneath
        self._beneath_bounds = (lower, upper)

    def get_beneath(self):
        """
        Get the zone which will appear when a player exits this zone at the bottom

        Returns None if no zone is set
        """
        return self._beneath

    def get_beneath_bounds(self):
        """
        Get the region where a user can proceed to the next zone at the bottom

        Returns None if no zone is set
        """
        return self._beneath_bounds

    def set_above(self, above, lower, upper):
        """
        Set the zone which should appear when a player exits this zone at the top
        """
        self._above = above
        self._above_bounds = (lower, upper)

    def get_above(self):
        """
        Get the zone which will appear when a player exits this zone at the top

        Returns None if no zone is set
        """
        return self._above

    def get_above_bounds(self):
        """
        Get the region where a user can proceed to the next zone at the top

        Returns None if no zone is set
        """
        return self._above_bounds

    def is_interesting_region(self, x, y):
        """
        Checks if a player has clicked an interesting region of this zone

        Returns information about the zone if an interesting region was clicked. Otherwise, returns None.
        """
        for region in self._interesting_regions:
            start = region.get_start_coordinates()
            end = region.get_end_coordinates()
            if start[0] < x < end[0] and start[1] < y < end[1]:
                return region.get_information()
        return None

    def is_disallowed_region(self, x, y):
        """
        Checks if a player has entered a disallowed region of this zone

        Returns True if the player is in a disallowed region. Otherwise, returns False.
        """
        for region in self._disallowed_regions:
            if region[0] < x < region[2] and region[1] < y < region[3]:
                return True
        return False

    def is_danger_region(self, x, y):
        """
        Checks if a player has entered a dangerous region of this zone

        Returns True if the player is in a dangerous region. Otherwise, returns False.
        """
        for region in self._danger_regions:
            if region[0] < x < region[2] and region[1] < y < region[3]:
                return True
        return False


class InterestingRegion():
    """
    Manage an interesting region
    """
    def __init__(self, information, x1, y1, x2, y2):
        self._information = information
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def get_information(self):
        """
        Return the information associated with this region
        """
        return self._information

    def get_start_coordinates(self):
        """
        Return the coordinates at the upper left of this region
        """
        return [self._x1, self._y1]

    def get_end_coordinates(self):
        """
        Return the coordinates at the lower right of this region
        """
        return [self._x2, self._y2]


def get_maps():
    """
    Returns all zones which make up the map
    """
    return [forest, spawn, city, meadow, canyon]


def get_first_map():
    """
    Returns the spawn zone
    """
    return spawn


# Initialise all zones
forest = Background(
    "Forest",
    "assets/images/maps/forest.png",
    [
        [195, 155]
    ],
    [],
    [
        [120, 175, 190, 225],
        [210, 175, 280, 225],
        [120, 85, 185, 135],
        [210, 85, 275, 135],
        [125, 260, 400, 400],
        [0, 0, 90, 230],
        [0, 260, 90, 400],
        [305, 0, 400, 230],
        [90, 0, 260, 50]
    ],
    []
)
spawn = Background(
    "Spawn",
    "assets/images/maps/spawn.png",
    [
        [155, 205],
        [155, 290],
        [245, 290],
        [245, 205]
    ],
    [],
    [
        [160, 40, 240, 115],
        [190, 220, 225, 250]
    ],
    []
)
city = Background(
    "City",
    "assets/images/maps/city.png",
    [
        [160, 110]
    ],
    [],
    [
        [25, 40, 85, 120],
        [85, 5, 150, 120],
        [0, 185, 185, 235],
        [0, 260, 185, 400],
        [225, 195, 280, 400],
        [225, 0, 400, 165],
        [310, 315, 365, 365]
    ],
    []
)
meadow = Background(
    "Meadow",
    "assets/images/maps/meadow.png",
    [
        [95, 255]
    ],
    [],
    [],
    [
        [0, 325, 40, 380],
        [40, 335, 100, 390],
        [100, 325, 120, 380],
        [120, 315, 175, 370],
        [160, 310, 215, 360],
        [190, 295, 235, 335],
        [195, 280, 250, 310],
        [195, 200, 250, 230],
        [185, 160, 240, 200],
        [180, 125, 235, 160],
        [190, 85, 245, 125],
        [200, 50, 250, 85],
        [205, 15, 260, 50],
        [215, 0, 270, 15]
    ]
)
canyon = Background(
    "Canyon",
    "assets/images/maps/canyon.png",
    [
        [190, 220]
    ],
    [],
    [],
    [
        [250, 0, 355, 35],
        [245, 35, 350, 70],
        [240, 70, 345, 110],
        [245, 105, 350, 140],
        [240, 145, 345, 175],
        [235, 180, 340, 215],
        [230, 220, 335, 220],
        [230, 275, 340, 300],
        [235, 300, 345, 335],
        [240, 335, 350, 370],
        [245, 370, 355, 390],
        [250, 400, 360, 400]
    ]
)

forest.set_right(spawn, 235, 275)
forest.set_beneath(meadow, 95, 135)

spawn.set_left(forest, 235, 275)
spawn.set_beneath(canyon, 190, 230)
spawn.set_right(city, 235, 275)

city.set_left(spawn, 235, 275)

meadow.set_above(forest, 95, 135)
meadow.set_right(canyon, 235, 275)

canyon.set_left(meadow, 235, 275)
canyon.set_above(spawn, 190, 230)
