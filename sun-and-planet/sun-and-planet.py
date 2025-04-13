import numpy as np
import os

G = 6.674e-11

time = 0
dt = 3600
num_updates = 5000

sun_position = np.array([0, 0, 0])
sun_mass = 1.98892e30

earth_mass = 9722e24
earth_position = np.array([1.499e11, 0, 0])
earth_velocity = np.array([0, 0, 0])
earth_acceleration = np.array([0, 0, 0])


def calc_gravitational_force(m1, m2, d):
    abs_d = np.linalg.norm(d)
    return (G * m1 * m2 / (abs_d**3)) * d

def calc_acceleration(mass, *forces):
    net_force = np.sum(forces, axis=0)
    return net_force / mass

def calc_velocity(acceleration, current_velocity, dt):
    return current_velocity + acceleration * dt

def calc_position(velocity, current_position, dt):
    return current_position + velocity * dt


class Planet:
    def __init__(self, mass, position, velocity, acceleration):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def update(self):
        gravitational_force = calc_gravitational_force(self.mass, sun_mass, sun_position - self.position)
        #print(gravitational_force)

        self.acceleration = calc_acceleration(self.mass, gravitational_force)
        self.velocity = calc_velocity(self.acceleration, self.velocity, dt)
        self.position = calc_position(self.velocity, self.position, dt)



Earth = Planet(earth_mass, earth_position, earth_velocity, earth_acceleration)


data = []
for i in range(num_updates):
    data.append([time, Earth.position, Earth.velocity, Earth.acceleration])
    Earth.update()
    time += dt


print(data[1])
print(data[1][1])
BASE_DIR = os.path.dirname(__file__)
PATH = os.path.join(BASE_DIR, "data/sun-and-planet-data.csv")
with open(PATH, "w") as f:
    f.write("time, planet_x, planet_y, planet_z, planetv_x, planetv_y, planetv_z, planeta_x, planeta_y, planeta_z\n")
    for line in data:
        f.write(f"{line[0]}, {line[1][0]}, {line[1][1]}, {line[1][2]}, {line[2][0]}, {line[2][1]}, {line[2][2]}, {line[3][0]}, {line[3][1]}, {line[3][2]}\n")




