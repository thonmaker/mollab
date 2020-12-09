# author: Roy Kid

from emmm.core.atom import Atom
from emmm.core.adt import Item
from emmm.core.operate import Bioperate, Unioperate


class Molecule(Item):

    id = 0

    def __init__(self, label=None, type=None, parent=None, path=None, isAdhere=False):
        super().__init__(label=label, type=type, parent=parent, path=path)

        self.isAdhere = isAdhere
        self.id = Molecule.id
        Molecule.id += 1

    @property
    def coords(self):
        if not hasattr(self, 'coords'):
            Unioperate.calc_centroid(self)
        return self.coords

    def __repr__(self) -> str:
        return f'< molecule: {self.label} in {self.parent}>'

    def get_items(self):
        return self

    def add_items(self, *items):
        for item in items:
            if isinstance(item, Atom):
                item.parent = self.label
                self.append(item)

            elif isinstance(item, list):
                self.add_items(*item)

            elif isinstance(item, Molecule):
                self.append(item)

    def __getitem__(self, label):

        if isinstance(label, str):
            for item in self:
                if item.label == label:
                    return item
            
        elif isinstance(label, slice):
            raise TypeError('Not support slice yet')

   # def rm_item(self, label):
    
    def flatten(self, dir=None, isSelf=False):

        if dir is None:
            dir = [self.label]

        else:
            dir.append(self.label)
        atoms = list()
        for item in self:
            if isinstance(item, Atom):
                dir.append(item.label)
                item.path = '/'.join(dir)
                atoms.append(item)
                dir.pop()

            elif isinstance(item, Molecule) and isSelf:
                atoms.append(item)
                atoms.append(item.flatten(dir))
            elif isinstance(item, Molecule) and not isSelf:
                atoms.extend(item.flatten(dir))

        dir.pop()
        return atoms

    def rotate(self, theta, x, y, z, x0=0, y0=0, z0=0):
        Unioperate.rotate(self, theta, x, y, z, x0, y0, z0)