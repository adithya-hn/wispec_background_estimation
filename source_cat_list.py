import numpy as np
import pandas as pd

#cat_data=(np.loadtxt('/home/adithya/Downloads/uhuru_ssm_format20160322.dat',usecols=(0,1,6))).transpose()
#print(cat_data)


#cols=["srcra", "srcdec", "srcname", "srcindex","maxint", "minint", "avgint", "lastint", "lastint_unc", "HR1", "HR2",  "lastMJD","srcact","altname" , "srctype"]
#df = pd.read_csv('/home/adithya/Downloads/uhuru_ssm_format20160322_1.dat',sep=r"\s+", names=cols, skiprows=4)
#df.to_csv('/home/adithya/Downloads/uhuru_ssm_format20160322_1.csv', index=False)

#df=pd.read_csv('uhuru_ssm_format20160322_1.csv')
df=pd.read_csv('simulated_data.csv')
#print(df.head())
#print(df['srcra'])


ref_ra=5
ref_dec=82
fov_ra= 20 #width along ra
fov_dec=20 #width along dec
Intensity_threshold=0


cat_ra =df['srcra'].tolist()  #np.array(cat_data[0])  #RA
cat_dec=df['srcdec'].tolist() #np.array(cat_data[1])  #DEC
cat_int=df['avgint'].tolist() #np.array(cat_data[2])  #Flux/Int

num_sources=0
total_intensity=0


a=ref_ra-fov_ra/2
b=ref_ra+fov_ra/2
c=ref_dec-fov_dec/2
d=ref_dec+fov_dec/2

e=b
f=a
if a<0:
    a=360+a
    e=360
    f=0

if b>360:
    b=b%360

if c>90:
    c=90 - (c%90)

if c<-90:
    c=-90 + (abs(c)%90)

if d>90:
    d=90 - (d%90)

if d<-90:
    d=-90 + (abs(d)%90)

print(a,b,c,d)
print(cat_ra,cat_dec)

for i in range(len(cat_ra)):
    #print('Source',i+1,cat_ra[i],a,b)
    if cat_ra[i]>=a and cat_ra[i]<= e or cat_ra[i]>=f and cat_ra[i]<= b :
        #print('--',cat_dec[i],c,d)
        if cat_dec[i]>= c and cat_dec[i]<=d:

            print('Source in FOV',cat_ra[i],cat_dec[i])
            num_sources +=1
            total_intensity +=cat_int[i]

print('----------------------------------')

print('With the intensity threshold',Intensity_threshold)
print('Number of sources in FOV:',num_sources)
print('Total of averaged intensity:',total_intensity)
  