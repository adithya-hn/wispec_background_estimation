import numpy as np
import matplotlib.pyplot as plt



uc=1.65

uc_to_E=1.7*10e-11

E1=2 #in keV
E2=6
gamma=2 # our assumption
alpha=gamma-1
if alpha==1:
    Intgral_val=np.log(E2/E1)
    print(Intgral_val)
else:
    print('not written yet')


A=(uc*uc_to_E)/Intgral_val
print('Value of A',A)

E3=0.5 #in keV
E4=4






