import os
import numpy as np
import scipy.constants

epsilon_0 = 8.854187817e-12

class Particle:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge

origin_electron = Particle(np.array([0, 0, 0]), 1.60e-19)

def calc_E_field_at_point(r, particle:Particle):
    return (1/(4*np.pi*scipy.constants.epsilon_0)) * (particle.charge / (np.linalg.norm(particle.position - r) ** 3)) * (particle.position - r)

min_x = -50e-6
max_x = 50e-6
min_y = -50e-6
max_y = 50e-6
min_z = -50e-6
max_z = 50e-6

x = np.linspace(min_x, max_x, 101)
y = np.linspace(min_y, max_y, 101)
z = np.linspace(min_z, max_z, 101)

X, Y, Z = np.meshgrid(x, y, z)
Ex = np.zeros(len(X.flatten()))
Ey = np.zeros(len(X.flatten()))
Ez = np.zeros(len(X.flatten()))
field_points = np.array([X.flatten(), Y.flatten(), Z.flatten(), Ex, Ey, Ez]).T

for point in field_points:
    #point[3] = np.linalg.norm(point[0:3])
    E = calc_E_field_at_point([point[0], point[1], point[2]], origin_electron)
    point[3] = E[0]
    point[4] = E[1]
    point[5] = E[2]

# for point in field_points:
#     print(point)

BASE_DIR = os.path.dirname(__file__)
PATH = os.path.join(BASE_DIR, "data/E-field-from-charge.csv")
with open(PATH, "w") as f:
    f.write("x, y, z, Ex, Ey, Ez\n")
    for line in field_points:
        f.write(f"{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}\n")




