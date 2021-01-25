# author: Roy Kid


from emmm.plugins.output.output_base import OutputBase


class OUTlmpdat(OutputBase):
    def __init__(self, world) -> None:
        super().__init__(world)


    def dump_data(self, file):
        fname = file
        with open(fname, 'w') as f:

            s = self.world
            w = f.write
            
            # comment line
            w('# generated by emmm\n\n')

            
            w(f'{s["atomNum"]}\tatoms\n')
            w(f'{s["bondNum"]}\tbonds\n')

            if 'angles' in s:
                w(f'{s["angleNum"]}\tangles\n')
            else: 
                w(f'0\tangles\n')

            if 'dihedrals' in s:
                w(f'{s["dihedralNum"]}\tdihedrals\n')
            else:
                w(f'0\tdihedrals\n')

            if 'impropers' in s:
                w(f'{s["improperNum"]}\timpropers\n')
            else:
                w(f'0\timpropers\n')

            w(f'{s["atomTypeNum"]}\tatom types\n')
            w(f'{s["bondTypeNum"]}\tbond types\n')

            if 'angle types' in s:
                w(f'{s["angleTypeNum"]}\tangle types\n')
            else: 
                w(f'{s["angleTypeNum"]}\tangle types\n')

            if 'dihedral types' in s:
                w(f'{s["dihedralTypeNum"]}\tdihedral types\n')
            else:
                w(f'0\tdihedral types\n')

            if 'improper types' in s:
                w(f'{s["improperTypeNum"]}\timpropers types\n\n')
            else:
                w(f'0\timproper types\n\n')            

            # box size section
            if 'xlo' and 'xhi' in s:
                w(f'{s["xlo"]}\t{s["xhi"]}\txlo\txhi\n')
            else:
                w(f'0.0000\t0.0000\txlo\txhi')

            if 'ylo' and 'yhi' in s:
                w(f'{s["ylo"]}\t{s["yhi"]}\tylo\tyhi\n')
            else:
                w(f'0.0000\t0.0000\tylo\tyhi')

            if 'zlo' and 'zhi' in s:
                w(f'{s["zlo"]}\t{s["zhi"]}\tzlo\tzhi\n')
            else:
                w(f'0.0000\t0.0000\tzlo\tzhi\n')

            w('\n\n\n')

            # Masses section
            w('Masses\n\n')

            for i in s['masses']:
                w(f'{i[0]}\t{i[1]}\n')

            w('\n\n\n')            

            w(f'Atoms # {s["atomStyle"]}\n\n')

            for i in s['atoms']:
                w(' '.join(i)+'\n')
                

            w('Bonds\n\n')

            for i in s['bonds']:
                w(' '.join(i)+'\n')
                

            if 'Angles' in s:
                w('Angles\n\n')

                for i in s['angles']:
                    w(' '.join(i)+'\n')



            if 'Dihedrals' in s:
                w('Dihedrals\n\n')

                for i in s['dihedrals']:
                    w(' '.join(i)+'\n')

            if 'Impropers' in s:
                w('Impropers\n\n')

                for i in s['impropers']:
                    w(' '.join(i)+'\n')
            

            # other sections   