import numpy as np
import pandas as pd
from astropy.table import Table
import numpy.ma as ma
from scipy import integrate

import warnings
warnings.simplefilter('ignore')

table = Table.read("/home/adithya/Downloads/cat2rxs.fits")
#print(table)
g_lon=table['LII']                    #galactic longitude
g_lat=table['BII']                    #galactic latitude
flux =table['FLUX_p']                 #Flux, Absorption corrected flux of PL-fit
gamma=table['GAMMA_p']                #Photon index (GAMMA_p)
gamma_er=table['GAMMA_err_p']         #Error of GAMMA_p (GAMMA_err_p)
Norm_const=table['NORM_p']            #Photon index
Norm_const_er=table['NORM_err_p']     #Photon index error

qe_data=np.loadtxt('NON_OBF_line.txt') #eng in ev: qe

counts=[]
eng=np.array(qe_data[:,0]/1000) #eng * 1000 to make keV
qe=qe_data[:,1] #qe value


fov_ra= 6  #width along ra
fov_dec=6  #width along dec

grid= np.zeros((360,180))
gal_grid= np.zeros((360,180))

cat_l=g_lon
cat_b=g_lat

no_flux=0  #count of sources which dont have flux measurments

print('---------')
  
ref_ra=329      # ra, dec = gal_long, gal_lat
ref_dec=-21

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


for i in range(len(cat_l)):
    if cat_l[i]>=ra_min and cat_l[i]<= ra_max_ or cat_l[i]>=ra_min_ and cat_l[i]<= ra_max :
        #print('--',cat_dec[i],c,d)
        if cat_b[i]>= dec_min and cat_b[i]<=dec_max:
            num_sources +=1
            
            if not isinstance(gamma[i], ma.core.MaskedConstant): #to check for masked values, where we dont have proper measurmenst
                
                eng_qe=[]
                for j in range (len(eng)):
                    eng_qe.append(Norm_const[i]*(eng[j]**-gamma[i])*qe[j]*16*0.6) #16 is the detectpr area
                print(integrate.simpson(eng_qe, x=eng))
                counts+=integrate.simpson(eng_qe, x=eng)
            

            else:
                no_flux+=1
print('---->',counts)


if num_sources>0:
    print('Total sourcecs',num_sources)
    print('Total intensity',total_intensity)
    

print('----------------------------------')

