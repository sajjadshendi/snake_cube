from Interface import *
from sim import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# a class for drawing simulator
class GUI:
    def __init__(self):
        pass

    def draw(self, world_model):
        interface = Interface()
        #getting coordinates of our centers and make dataframe from that
        Coordinates = interface.cur_state(world_model)['Coordinates']
        x=[]
        y=[]
        z=[]
        for item in Coordinates:
            x.append(item[0])
            y.append(item[1])
            z.append(item[2])
        df = pd.DataFrame({"x": x, "y": y,
                           "z": z})
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        L = 1

        #for drawing each cube we need a loop
        for i in df.index:
            x, y, z = self.get_cube()

            # Change the centroid of the cube from zero to values in data frame
            x = x * L + df.x[i]
            y = y * L + df.y[i]
            z = z * L + df.z[i]
            ax.plot_surface(x, y, z)
            ax.set_zlabel("z")

        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    def get_cube(self):
        phi = np.arange(1, 10, 2) * np.pi / 4
        Phi, Theta = np.meshgrid(phi, phi)

        x = np.cos(Phi) * np.sin(Theta)
        y = np.sin(Phi) * np.sin(Theta)
        z = np.cos(Theta) / np.sqrt(2)
        return x, y, z

