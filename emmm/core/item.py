# author: Roy Kid
from copy import deepcopy

from numpy.lib.arraysetops import isin
import numpy as np 

class Item(list):

    def __init__(self, label=None, type=None, parent=None, path=None):
        super().__init__()

        self.label = label
        self.type = type
        self.parent = parent
        self.path = path

    @property
    def id(self):
        return self.id

    @property
    def coords(self):
        return self.coords
    @coords.setter
    def coords(self, value):
        if isinstance(value, list) and isinstance(value, tuple):
            value = np.array(value)
            self.coords = np.array(value)
        elif isinstance(value, np.ndarray):
            self.coords = value
        else:
            raise TypeError("type of coords is error")

        self.x = self.coords[0]
        self.y = self.coords[1]
        self.z = self.coords[2]

    @property
    def x(self):
        return self.x
    @x.setter
    def x(self, x):
        self.x = np.float64(x)
        self.coord[0] = x

    @property
    def y(self):
        return self.y
    @y.setter
    def y(self, y):
        self.y = np.float64(y)
        self.coord[1] = y
    
    @property
    def z(self):
        return self.z
    @z.setter
    def z(self, z):
        self.z = np.float64(z)
        self.coords[2] = z

    def move(self, x, y, z):
        """[In-place]

        Args:
            x (Float): vector in x
            y (Float): vector in y
            z (Float): vector in z
        """

        vec = np.array([x,y,z], dtype=float)
        self.coords += vec

    def randmove(self, length):
        """[In-place]

        Args:
            length (Float): length to random move in any orientation vector
        """
        vec = np.random.random([3,1])
        vec /= np.linalg.norm(vec)
        vec *= length
        self.coords += vec

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        """[summary]

        Args:
            theta (radian): theta:=theta*PI
            x (float): to
            y (float): to
            z (float): to
            x0 (float): from
            y0 (float): from
            z0 (float): from
        """
        # rotation axis
        x = float(x)
        y = float(y)
        z = float(z)
        x0= float(x0)
        y0= float(y0)
        z0= float(z0)
        disVec = np.array([x0, y0, z0])
        rotAxis = np.array([x, y, z])

        rotAxis = rotAxis/np.linalg.norm(rotAxis)
        rotAxisX, rotAxisY, rotAxisZ = rotAxis

        # half theta = theta/2
        htheta = np.pi*theta/2
        # sin theta = sin(htheta)
        stheta = np.sin(htheta)

        a = np.cos(htheta)
        b = stheta*rotAxisX
        c = stheta*rotAxisY
        d = stheta*rotAxisZ
        b2 = b**2
        c2 = c**2
        d2 = d**2
        ab = a*b
        ac = a*c
        ad = a*d
        bc = b*c
        bd = b*d
        cd = c*d

        # rotation matrix
        rotm = np.array([[1-2*(c2+d2), 2*(bc-ad), 2*(ac+bd)],
                         [2*(bc+ad), 1-2*(b2+d2), 2*(cd-ab)],
                         [2*(bd-ac), 2*(ab+cd), 1-2*(b2+c2)]])

        self.coords -= disVec
        self.coords = np.dot(rotm, self.coords)
        self.coords += disVec

    def rotate_orth(self, theta, x, y, z, xAxis, yAxis, zAxis):

        if (x,y,z)==(1,0,0) or\
           (x,y,z)==(0,1,0) or\
           (x,y,z)==(0,0,1):

            self.rotate(self, theta, x+xAxis, y+yAxis, z+zAxis, x, y, z)
        else:
            raise SyntaxError('only one of *Axis can be 1 to indicate the orientation of rotation axis')

    def seperate_with(self, targetItem, type, value):
        """ [Bioperate] to seperate two items in opposite direction: (rel)ative distance is move EACH item in a distance under system unit; (abs)olute distance is the time of current distance of two items, e.g.: item+=unit_orientation_vector*rel; item+=orientation_vector*abs.

        Args:
            targetItem (Item): Atom|Molecule
            type (str): rel|abs
            value (Float): distance
        """
        coords1 = self.coords
        coords2 = targetItem.coords

        # orientation vector
        oriVec = coords2 - coords1
        uniVec = oriVec/np.linalg.norm(oriVec)

        if type=='relative' or type=='rel':
            coords2 += uniVec*value
            coords1 -= uniVec*value
        if type=='abusolute' or type=='abs':
            coords2 += oriVec*value
            coords1 -= oriVec*value

        self.coords = coords1
        targetItem.coords = coords2        

    def distance_to(self, targetItem):
        """[Bioperate] return the distance to a target item

        Args:
            targetItem (Item): Atom|Molecule
        """
        coords1 = self.coords
        coords2 = targetItem.coords

        dist = np.linalg.norm(coords2-coords1)

        return dist