# author: Roy Kid
# contact: lijichen365@126.com
# date: 2021-01-25
# version: 0.0.1

from emmm.core.potential.bond_base import BondBase


class BondHarmonic(BondBase):
    def __init__(self, coeffs) -> None:
        super().__init__()
        if not isinstance(coeffs, dict):
            raise TypeError(f'coeffs 应为dict类型而不是{type(coeffs)}')
        self.k = coeffs['k']
        self.r0 = coeffs['r0']
        self.cutoff = coeffs['cutoff']


    def energy(self, r):
        """ get the energy when bond length=r

        Args:
            r (float): bond length

        Returns:
            energy: bond energy
        """
        return self.k*(r - self.r0)**2

    def force(self, r):
        """ get the force when bond length=r

        Args:
            r (float): bond length

        Returns:
            force: bond force
        """
        return 2*self.k*(r - self.r0)