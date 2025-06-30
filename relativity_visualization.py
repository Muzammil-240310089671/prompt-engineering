# This script provides a 3D visualisation of a simplified relativity scenario
# using the vpython library. Planets can be added along the x-axis and are
# attached to the origin via a helical "string". The center of mass of all
# planets is tracked and displayed. Planets are constrained to move only along
# the x-axis (y=0 plane), demonstrating a simple 1D gravity well.

from vpython import canvas, sphere, vector, color, helix, label, rate

class Planet:
    def __init__(self, mass: float, x: float, radius: float = 0.5, body_color=color.blue):
        self.mass = mass
        self.position = vector(x, 0, 0)
        self.initial_x = x
        self.body = sphere(pos=self.position, radius=radius, color=body_color, make_trail=False)
        # Helical string anchored at the origin
        self.string = helix(pos=vector(0, 0, 0), axis=self.position,
                            radius=0.05, thickness=0.02, coils=20, color=color.white)

    def update(self):
        # keep the planet on the x-axis and update string
        self.position.y = 0
        self.body.pos = self.position
        self.string.axis = self.position

    @property
    def stretch(self) -> float:
        """Return the current stretch of the string from its initial length."""
        current_len = self.position.mag
        return current_len - abs(self.initial_x)


class RelativityVisualization:
    def __init__(self):
        self.scene = canvas(title="Einstein Relativity 3D Visualisation",
                            width=800, height=600, background=color.black)
        self.planets = []
        self.cm_label = label(pos=vector(0, 1, 0), text="Center of Mass: 0", box=False, color=color.yellow)
        self.scene.bind('keydown', self._on_keydown)

    def _on_keydown(self, evt):
        # Press 'n' to add a new planet via console input
        if evt.key == 'n':
            try:
                mass = float(input("Mass of new planet: "))
                x_pos = float(input("Initial x position: "))
                self.add_planet(mass, x_pos)
            except Exception:
                print("Invalid input. Planet not added.")

    def add_planet(self, mass: float, x: float, radius: float = 0.5, body_color=color.blue):
        planet = Planet(mass, x, radius, body_color)
        self.planets.append(planet)
        self.update_center_of_mass()

    def update_center_of_mass(self):
        total_mass = sum(p.mass for p in self.planets)
        if total_mass == 0:
            cm_x = 0
        else:
            cm_x = sum(p.mass * p.position.x for p in self.planets) / total_mass
        self.cm_label.pos = vector(cm_x, 1, 0)
        self.cm_label.text = f"Center of Mass (x-axis): {cm_x:.2f}"

    def run(self):
        # Example planets
        if not self.planets:
            self.add_planet(mass=5, x=3, radius=0.5, body_color=color.red)
            self.add_planet(mass=2, x=6, radius=0.3, body_color=color.green)

        while True:
            rate(60)
            for planet in self.planets:
                planet.update()
            self.update_center_of_mass()
            # Display stretch values for each planet
            for i, planet in enumerate(self.planets, start=1):
                print(f"Planet {i} stretch: {planet.stretch:.2f}", end='\r')


if __name__ == "__main__":
    visualisation = RelativityVisualization()
    visualisation.run()
