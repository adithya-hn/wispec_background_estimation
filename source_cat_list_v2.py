import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygmt
from astropy import coordinates as coord
import math as mt
from astropy.coordinates import SkyCoord
from astropy import units as u
from scipy import integrate



#cat_data=(np.loadtxt('/home/adithya/Downloads/uhuru_ssm_format20160322.dat',usecols=(0,1,6))).transpose()
#print(cat_data)
#cols=["srcra", "srcdec", "srcname", "srcindex","maxint", "minint", "avgint", "lastint", "lastint_unc", "HR1", "HR2",  "lastMJD","srcact","altname" , "srctype"]
#df = pd.read_csv('/home/adithya/Downloads/uhuru_ssm_format20160322_1.dat',sep=r"\s+", names=cols, skiprows=4)
#df.to_csv('/home/adithya/Downloads/uhuru_ssm_format20160322_1.csv', index=False)
df=pd.read_csv('uhuru_ssm_format20160322_1.csv')

#df=pd.read_csv('simulated_data.csv')
#print(df.head())
#print(df['srcra'])


fov_ra= 6  #width along ra
fov_dec=6 #width along dec

grid= np.zeros((360,180))
gal_grid= np.zeros((360,180))
cat_ra =df['srcra'].tolist()  #np.array(cat_data[0])  #RA
cat_dec=df['srcdec'].tolist() #np.array(cat_data[1])  #DEC
cat_int=df['avgint'].tolist() #np.array(cat_data[2])  #Flux/Int

c=SkyCoord(ra=cat_ra*u.degree, dec=cat_dec*u.degree, frame='icrs')
cat_l=c.galactic.l.deg.tolist()
cat_b=c.galactic.b.deg.tolist()
check='no'
if check=='yes': # to check ra,dec to l,b conversion, will set to use RA, DEC not galactic
    cat_l=cat_ra
    cat_b=cat_dec
#print(cat_l)

print('---------')
#print(cat_b)

        
ref_ra=329  # Galactic coord correspond to 276, -65 (RA, DEC)
ref_dec=-21

#print('Center (l,b)=',ref_ra,ref_dec,k,m)

Intensity_threshold=0
num_sources=0
total_intensity=0


ra_min=ref_ra-(fov_ra/(2*np.cos(np.radians(ref_dec)))) #ra min
ra_max=ref_ra+(fov_ra/(2*np.cos(np.radians(ref_dec)))) #ra max
dec_min=ref_dec-fov_dec/2 #dec min
dec_max=ref_dec+fov_dec/2 # dec max

ra_max_=np.copy(ra_max)
ra_min_=np.copy(ra_min)

if ra_min<0:
    ra_min=360+ra_min #Ra min is negativ
    ra_max_=360
    ra_min_=0

if ra_max>360:
    ra_max=ra_max%360

if dec_min<-90:
    dec_min=-90 + (abs(dec_min)%90)

if dec_max>90:
    dec_max=90 - (dec_max%90)

#if dec_max<-90:
#    dec_max=-90 + (abs(dec_max)%90)

#print(a,b,c,d)
#print(cat_ra,cat_dec)


for i in range(len(cat_ra)):
    #print('Source',i+1,cat_ra[i],a,b)
    if cat_l[i]>=ra_min and cat_l[i]<= ra_max_ or cat_l[i]>=ra_min_ and cat_l[i]<= ra_max :
        #print('--',cat_dec[i],c,d)
        if cat_b[i]>= dec_min and cat_b[i]<=dec_max:

            print('Source in FOV :',cat_ra[i],'RA',cat_dec[i],'DEC',cat_l[i],'l',cat_b[i],'b')
            num_sources +=1
            total_intensity +=cat_int[i]




if num_sources>0:
    print('Total sourcecs',num_sources)
    

print('----------------------------------')


uc_to_E=1.7*10e-11
E1=2 #in keV
E2=6
gamma=2 # our assumption
alpha=gamma-1
if alpha==1:
    Intgral_val=np.log(E2/E1)
    print(Intgral_val)
else:
    (E2**(-alpha+1) - E1**(-alpha -1))/(-alpha+1)


A=(total_intensity*uc_to_E)/Intgral_val
print('Value of A=',A)

E3=0.5 #in keV
E4=4

qe_data=np.loadtxt('NON_OBF_line.txt') #eng in ev: qe
eng=np.array(qe_data[:,0]/1000) #eng * 1000 to make keV
qe=qe_data[:,1] #qe value

counts_s=0
eng_qe=[]
for j in range (len(eng)):
    eng_qe.append(A*1.6e9*(eng[j]**-gamma)*qe[j]*16) #16 is the detectpr area
#print(counts_s)

print(len(eng_qe),len(eng))

counts_cm2_s=integrate.simpson(eng_qe, x=eng)
print('---->',counts_cm2_s)

#plt.plot(eng,qe)
#plt.show()


'''fig = pygmt.Figure()
fig.coast(
    region="d",
    projection="Y12c",
    frame="afg",
    land="gray80",
    water="steelblue",
)
plt.imshow(grid.T, origin='lower', extent=[0,360,-90,90], cmap='viridis')
plt.colorbar(label='Total sources in FOV')
plt.xlabel('Right Ascension (degrees)')
plt.ylabel('Declination (degrees)')
plt.title('Sky Map of Total total source per FOV')
plt.grid(False)
plt.show()
print('With the intensity threshold',Intensity_threshold)
print('Number of sources in FOV:',num_sources)
print('Total of averaged intensity:',total_intensity)'''
