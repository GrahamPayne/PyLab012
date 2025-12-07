import math

# Simple color codes
COLOR_CODES = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
RESET_COLOR = "\033[0m"


class UniversalGravity:
    def __init__(self, G=0.1):
        self.G = float(G)


U = UniversalGravity()


class Sun:
    def __init__(self, name, radius, mass, temp, x=0.0, y=0.0):
        self.name = name
        self.radius = float(radius)
        self.mass = float(mass)
        self.temp = float(temp)
        self.x = float(x)
        self.y = float(y)

    def get_mass(self):
        return self.mass

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def __str__(self):
        return (
            f"Sun {self.name}: "
            f"pos=({self.x:.2f}, {self.y:.2f}), "
            f"mass={self.mass}, radius={self.radius}"
        )


class Planet:
    def __init__(
        self,
        name,
        radius,
        mass,
        distance,
        x,
        y,
        color="white",
        vel_x=0.0,
        vel_y=0.0,
    ):
        self.name = name
        self.radius = float(radius)
        self.mass = float(mass)
        self.distance = float(distance)
        self.x = float(x)
        self.y = float(y)
        self.vel_x = float(vel_x)
        self.vel_y = float(vel_y)
        self.color = color

    def get_mass(self):
        return self.mass

    def get_distance(self):
        return self.distance

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def get_x_vel(self):
        return self.vel_x

    def get_y_vel(self):
        return self.vel_y

    def set_x_vel(self, new_x_vel):
        self.vel_x = float(new_x_vel)

    def set_y_vel(self, new_y_vel):
        self.vel_y = float(new_y_vel)

    def move_to(self, new_x, new_y):
        self.x = float(new_x)
        self.y = float(new_y)

    def __str__(self):
        code = COLOR_CODES.get(self.color.lower(), "")
        reset = RESET_COLOR if code else ""
        return (
            f"{code}Planet {self.name}: "
            f"pos=({self.x:.2f}, {self.y:.2f}), "
            f"vel=({self.vel_x:.3f}, {self.vel_y:.3f}), "
            f"dist={self.distance:.2f}{reset}"
        )


class SolarSystem:
    def __init__(self):
        self.the_sun = None
        self.planets = []

    def add_sun(self, the_sun):
        self.the_sun = the_sun

    def add_planet(self, new_planet):
        self.planets.append(new_planet)

    def show_planets(self):
        print("Current planet positions:")
        for planet in self.planets:
            print("  ", planet)
        print()

    def move_planets(self):
        if self.the_sun is None:
            return

        dt = 0.001

        for planet in self.planets:
            planet.move_to(
                planet.get_x_pos() + dt * planet.get_x_vel(),
                planet.get_y_pos() + dt * planet.get_y_vel(),
            )

            dist_x = self.the_sun.get_x_pos() - planet.get_x_pos()
            dist_y = self.the_sun.get_y_pos() - planet.get_y_pos()
            new_distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

            if new_distance == 0:
                continue

            acc_x = U.G * self.the_sun.get_mass() * dist_x / new_distance ** 3
            acc_y = U.G * self.the_sun.get_mass() * dist_y / new_distance ** 3

            planet.set_x_vel(planet.get_x_vel() + dt * acc_x)
            planet.set_y_vel(planet.get_y_vel() + dt * acc_y)

            planet.distance = new_distance


class Simulation:
    def __init__(self, solar_system, width, height, num_periods):
        self.solar_system = solar_system
        self.width = int(width)
        self.height = int(height)
        self.num_periods = int(num_periods)

    def run(self):
        print("Starting simulation...\n")

        for step in range(self.num_periods):
            self.solar_system.move_planets()

            if step % 100 == 0:
                print(f"Step {step}")
                self.solar_system.show_planets()

        print("Simulation complete.")


if __name__ == "__main__":
    solar_system = SolarSystem()

    the_sun = Sun("SOL", 5000, 10_000_000, 5800)
    solar_system.add_sun(the_sun)

    earth = Planet("EARTH", 47.5, 1, 25, 5.0, 200.0, "green")
    solar_system.add_planet(earth)

    mars = Planet("MARS", 40.5, 0.1, 62, 10.0, 125.0, "red")
    solar_system.add_planet(mars)

    simulation = Simulation(solar_system, 500, 500, 2000)
    simulation.run()
