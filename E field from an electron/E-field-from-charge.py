import os
import numpy as np
import scipy.constants
import pyvista as pv

class Particle:
    def __init__(self, position, charge):
        self.position = position
        self.charge = charge

electron_1 = Particle(np.array([0, 1e-5, 0]), 1.60e-19)
electron_2 = Particle(np.array([0, -1e-5, 0]), 1.60e-19)

my_particles = [electron_1, electron_2]

def calc_E_field_at_point(r, particles:Particle):
    field = np.array([0, 0, 0])
    
    for particle in particles:
        dist = np.linalg.norm(particle.position - r)
        if dist == 0:
            return np.array([0.0, 0.0, 0.0])
        
        field = np.add(field, (1/(4*np.pi*scipy.constants.epsilon_0)) * (particle.charge / (dist ** 3)) * (particle.position - r))

    return field

grid_size = 31
spacing = 1e-6

x = np.linspace(-spacing*grid_size/2, spacing*grid_size/2, grid_size)
y = np.linspace(-spacing*grid_size/2, spacing*grid_size/2, grid_size)
z = np.linspace(-spacing*grid_size/2, spacing*grid_size/2, grid_size)


X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])

E_vectors = np.array([calc_E_field_at_point(p, my_particles) for p in points])
magnitude = np.linalg.norm(E_vectors, axis=1)
magnitude[magnitude==0] = 1e-12
logE = np.log(magnitude)


grid = pv.StructuredGrid()
grid.points = points
grid.dimensions = (grid_size, grid_size, grid_size)
grid["E"] = E_vectors
grid["log(|E|)"] = logE



BASE_DIR = os.path.dirname(__file__)
PATH = os.path.join(BASE_DIR, "data/electric-field.vtk")
grid.save(PATH)



