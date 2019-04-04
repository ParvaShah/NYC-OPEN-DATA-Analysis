# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:58:35 2019

@author: Parva
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



neveredit = pd.read_csv("DOB_Permit_Issuance.csv")

neveredit2 = pd.read_csv("DOF__Condominium_comparable_rental_income___Manhattan_-_FY_2010_2011.csv")

neveredit.head()


data = neveredit.drop(columns=['Job doc. #','Self_Cert','Lot','Community Board','Special District 1',
                        'Special District 2','Oil Gas','Site Fill',"Permittee's First Name","Permittee's Last Name",
                        "Permittee's Business Name","Permittee's Phone #",
                        "Permittee's License Type","Permittee's License #",
                        "Act as Superintendent",
                        "Permittee's Other Title",
                        "HIC License",
                        "Site Safety Mgr's First Name",
                        "Site Safety Mgr's Last Name",
                        "Site Safety Mgr Business Name",
                        "Superintendent First & Last Name",
                        "Superintendent Business Name",
                        "Owner's Business Type",
                        "Non-Profit",
                        "Owner's Business Name",
                        "Owner's First Name",
                        "Owner's Last Name",
                        "Owner's House #",
                        "Owner's House Street Name",
                        "Owner's Phone #",
                        "DOBRunDate",
                        "PERMIT_SI_NO",
                        "Owner’s House City",
                        "Owner’s House State" ,       
                        "Owner’s House Zip Code",
                        "CENSUS_TRACT"           ,   
                        "NTA_NAME"
                        ],axis=1)

data_man = data[data["BOROUGH"]=="MANHATTAN"]
data_man = data_man.rename(index=str, columns={"Bin #": "BIN"})
data_man["BIN"] = pd.to_numeric(data_man["BIN"], errors='coerce')

print(data_man.dtypes)
print(neveredit2.dtypes)
neveredit2 =  neveredit2.drop(columns=["MANHATTAN CONDOMINIUM PROPERTY Boro-Block-Lot",            
                                    "MANHATTAN CONDOMINIUM PROPERTY Condo Section",
                                    " COMPARABLE RENTAL 1 Boro-Block-Lot",                     
                                    "COMPARABLE RENTAL 1 Address",                   
                                    "COMPARABLE RENTAL 1  Neighborhood",                   
                                    "COMPARABLE RENTAL 1  Building Classification",               
                                    "COMPARABLE RENTAL 1  Total Units",             
                                    "COMPARABLE RENTAL 1  Year Built" ,              
                                    "COMPARABLE RENTAL 1  Gross SqFt",            
                                    "COMPARABLE RENTAL 1  Est. Gross Income",            
                                    "COMPARABLE RENTAL 1  Gross Income per SqFt",         
                                    "COMPARABLE RENTAL 1 Full Market Value",          
                                    "COMPARABLE RENTAL 1  Market Value per SqFt",       
                                    "COMPARABLE RENTAL 1  Dist. from Coop in miles",      
                                    "COMPARABLE RENTAL 2  Boro-Block-Lot",     
                                    "COMPARABLE RENTAL 2  Address",    
                                    "COMPARABLE RENTAL 2  Neighborhood",   
                                    "COMPARABLE RENTAL 2  Building Classification" ,    
                                    "COMPARABLE RENTAL 2  Total Units",   
                                    "COMPARABLE RENTAL 2  Year Built",    
                                    "COMPARABLE RENTAL 2  Gross SqFt",    
                                    "COMPARABLE RENTAL 2  Est. Gross Income",   
                                    "COMPARABLE RENTAL 2  Gross Income per SqFt",  
                                    "COMPARABLE RENTAL 2  Full Market Value", 
                                    "COMPARABLE RENTAL 2  Market Value per SqFt",
                                    "COMPARABLE RENTAL 2  Dist. from Coop in miles"
                                    ],axis=1)



neveredit2 = neveredit2.rename(index=str, columns={"MANHATTAN CONDOMINIUM PROPERTY Neighborhood" : "Neighborhood", 
"MANHATTAN CONDOMINIUM PROPERTY Building Classification"  :  "Building Classification" ,
"MANHATTAN CONDOMINIUM PROPERTY Total Units"               :   "Total Units",
"MANHATTAN CONDOMINIUM PROPERTY Year Built"                :   "Year Built",
"MANHATTAN CONDOMINIUM PROPERTY Gross SqFt"                :   "Gross SqF",
"MANHATTAN CONDOMINIUM PROPERTY Est. Gross Income"         :   "Gross Income",
"MANHATTAN CONDOMINIUM PROPERTY Gross Income per SqFt" :"Gross Income per SqFt",
"MANHATTAN CONDOMINIUM PROPERTY Full Market Value" :"Full Market Value",
"MANHATTAN CONDOMINIUM PROPERTY Market Value per SqFt": "Market Value per SqFt" ,
"MANHATTAN CONDOMINIUM PROPERTY Address" : "Address"   })




merg = pd.merge(data_man, neveredit2, how='inner', on=["BIN"])





#         EDA on manhattan prices :

########### 'Market Value per SqFt VS Build Year' ---> Most of decents check with recessions in us

mvp = neveredit2
mvp = mvp.dropna(subset=['Year Built'])
mvp1 = mvp.groupby(['Year Built']).count()

year = mvp1.index.values.tolist()
count_ =  mvp1.BIN.values.tolist()

mvp = mvp.groupby(['Year Built']).sum()

sum_ = mvp['Market Value per SqFt'].values.tolist()

for i in range(len(sum_)):
    if count_[i] == 0:
        sum_[i] = 0
    else:
        sum_[i] = sum_[i]/count_[i]




plt.figure(figsize=(15,10))

plt.plot(year,sum_)
plt.title('Market Value per SqFt VS Build Year')
plt.show()




################  Development vs Years ----> downward slope between 2007 -2010 recession

mv_by = neveredit.loc[neveredit['BOROUGH'].isin(['MANHATTAN'])]

unq = mv_by['BOROUGH'].unique()
print(unq)

mv_by = mv_by.dropna(subset=['Filing Date'])
mv_by['Filing Date'] = mv_by['Filing Date'].str[6:10]
mv_by['Filing Date'] = pd.to_numeric(mv_by['Filing Date'])

mv_by = mv_by.loc[neveredit['Job Type'].isin(['NB','DM','A1'])]



mv_by = mv_by.groupby(['Filing Date']).count()

year = mv_by.index.values.tolist()

plt.figure(figsize=(15,10))

plt.plot(year,mv_by['Job Type'])


plt.title('Development VS Years')
plt.show()





import seaborn as sns


colormap = plt.cm.RdBu
plt.figure(figsize=(32,10))
plt.title('Pearson Correlation of Features Before', y=1.05, size=15)

sns.heatmap(neveredit2.corr(),linewidths=0.1,vmax=1.0, 
            square=True, cmap=colormap, linecolor='white', annot=True)



################## Pricing and permit


################# Look for New Building -----> Found range 204 - 222


s1 = pd.merge(data_man, neveredit2, how='inner', on=["BIN"])
print('columns with null values:\n', s1.isnull().sum())


s1 = s1.dropna(subset=['BIN']) # Less nan so dropna out use


    
s2 = s1.loc[s1['Job Type'].isin(['NB'])]

price = s2.groupby(["Market Value per SqFt"]).count()

mvps = price.index.values.tolist()

plt.figure(figsize=(20,10))
plt.plot(mvps,price['Job Type'])
#plt.xticks(mvps, price['Job Type'])
plt.title('New Buldings VS Market Value per SqFt')
plt.show()


####### Getting locations in Above price range

import gmplot

geo = s1.loc[s1['Market Value per SqFt'].isin(range(204,223))]

geo = geo.drop_duplicates(subset=['BIN'])

lat = geo["LATITUDE"]
lon = geo["LONGITUDE"]

print('Train columns with null values:\n', geo.isnull().sum())

gmap4 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap4.scatter( lat, lon, '# FF0000', 
                              size = 20, marker = False ) 

gmap4.draw( "mapex10.html" ) 







############## Areas with most development in recent years [last 10 years]

merg = merg.dropna(subset=['Filing Date'])
merg['Filing Date'] = merg['Filing Date'].str[6:10]
merg['Filing Date'] = pd.to_numeric(merg['Filing Date'])
merg = merg.loc[merg['Filing Date'].isin(range(2009,2020))]
merg = merg.loc[merg['Job Type'].isin(['NB','A1','DM'])]

merg1 = merg.groupby(["BIN"]).count()

unq_count = merg1['Job Type'].unique()


unq_count1 = np.unique(unq_count)

length = len(unq_count1)

incr = int(length/5)
x = []
i=0
while i<(length):
    
    x.append(unq_count1[i])
    
    i = i + incr
    print(i)
x.append(unq_count1[-1]+1)


dev1 = merg1.loc[merg1['Job Type'].isin(range(x[0],x[1]))]
dev1_bin = dev1.index.values.tolist()
dev1 = merg.loc[merg['BIN'].isin(dev1_bin)]
gmap1 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap1.scatter( dev1['Latitude'], dev1['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap1.draw( "mapdev1.html" ) 




dev1 = merg1.loc[merg1['Job Type'].isin(range(x[1],x[2]))]
dev1_bin = dev1.index.values.tolist()
dev1 = merg.loc[merg['BIN'].isin(dev1_bin)]
gmap1 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap1.scatter( dev1['Latitude'], dev1['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap1.draw( "mapdev2.html" ) 

dev1 = merg1.loc[merg1['Job Type'].isin(range(x[2],x[3]))]
dev1_bin = dev1.index.values.tolist()
dev1 = merg.loc[merg['BIN'].isin(dev1_bin)]
gmap1 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap1.scatter( dev1['Latitude'], dev1['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap1.draw( "mapdev3.html" ) 

dev1 = merg1.loc[merg1['Job Type'].isin(range(x[3],x[4]))]
dev1_bin = dev1.index.values.tolist()
dev1 = merg.loc[merg['BIN'].isin(dev1_bin)]
gmap1 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap1.scatter( dev1['Latitude'], dev1['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap1.draw( "mapdev4.html" ) 

dev1 = merg1.loc[merg1['Job Type'].isin(range(x[4],x[5]))]
dev1_bin = dev1.index.values.tolist()
dev1 = merg.loc[merg['BIN'].isin(dev1_bin)]
gmap1 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap1.scatter( dev1['Latitude'], dev1['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap1.draw( "mapdev5.html" ) 


#1000830,149

x1  = neveredit2.loc[neveredit2['BIN'].isin([1000830])]
                         
print(neveredit2.dtypes)

# FUN FACT
#20 Exchange Place-CIBC Building, 20 Exchange Pl, New York, NY 10005
# Building with most permits 
                         
                         
                         
################################## Subway  ######################


sub = data

sub = sub.dropna(subset=['Filing Date'])
sub['Filing Date'] = sub['Filing Date'].str[6:10]
sub['Filing Date'] = pd.to_numeric(sub['Filing Date'])

unq = sub['Zip Code'].unique()


zips = (10065, 10021, 10075, 10028, 10128, 10029, 10035)

sub_fin = sub.loc[sub['Zip Code'].isin(zips)]



######### Phase 1


## Left Side 

left_1 = [i for i in range(1423,1434)]
left11 = [i for i in range(1525,1542)]
left = [left_1,left11]
left_1 =  [item for sublist in left for item in sublist]
left_1.append(1646)



left_2 = [i for i in range(1403,1414)]
left2 = [i for i in range(1508,1525)]
left = [left_2,left2]
left_2 =  [item for sublist in left for item in sublist]
left_2.append(1624)


left_3 = [i for i in range(1383,1394)]
left3 = [i for i in range(1491,1507)]
left = [left_3,left3]
left_3 =  [item for sublist in left for item in sublist]
left_3.append(1602)



year = [i for i in range(2001,2018)]
      

sub_fin_left_1 = sub_fin.loc[sub_fin['Block'].isin(left_1) & sub_fin['Filing Date'].isin(year)]

sub_fin_left_2 = sub_fin.loc[sub_fin['Block'].isin(left_2) & sub_fin['Filing Date'].isin(year)]

sub_fin_left_3 = sub_fin.loc[sub_fin['Block'].isin(left_3) & sub_fin['Filing Date'].isin(year)]






permit_left_1 = sub_fin_left_1.groupby(["Filing Date"]).count()
permit_left_2 = sub_fin_left_2.groupby(["Filing Date"]).count()
permit_left_3 = sub_fin_left_3.groupby(["Filing Date"]).count()


plt.figure(figsize=(15,10))
plt.plot(year, permit_left_1["Job Type"], label='Block 1 plot')
plt.plot(year, permit_left_2["Job Type"], label='Block 2-3 plot')
plt.plot(year, permit_left_3["Job Type"], label='Block 4-5 plot')
plt.legend()
plt.title('Building Permit VS Distance from Second Avenue')




## Right Side 

left_1 = [i for i in range(1443,1454)]
left11 = [i for i in range(1542,1558)]
left = [left_1,left11]
left_1 =  [item for sublist in left for item in sublist]
left_1.append(1668)



left_2 = [i for i in range(1463,1473)]
left2 = [i for i in range(1559,1571)]
left = [left_2,left2]
left_2 =  [item for sublist in left for item in sublist]
left_2.append(1690)


left_3 = [i for i in range(1380,1390)]
left3 = [i for i in range(1491,1507)]
left = [left_3,left3]
left_3 =  [item for sublist in left for item in sublist]
left_3.append(1602)



year = [i for i in range(2001,2018)]
      

sub_fin_left_1 = sub_fin.loc[sub_fin['Block'].isin(left_1) & sub_fin['Filing Date'].isin(year)]

sub_fin_left_2 = sub_fin.loc[sub_fin['Block'].isin(left_2) & sub_fin['Filing Date'].isin(year)]

sub_fin_left_3 = sub_fin.loc[sub_fin['Block'].isin(left_3) & sub_fin['Filing Date'].isin(year)]






permit_left_1 = sub_fin_left_1.groupby(["Filing Date"]).count()
permit_left_2 = sub_fin_left_2.groupby(["Filing Date"]).count()
permit_left_3 = sub_fin_left_3.groupby(["Filing Date"]).count()


plt.figure(figsize=(15,10))
plt.plot(year, permit_left_1["Job Type"], label='Block 1 plot')
plt.plot(year, permit_left_2["Job Type"], label='Block 2-3 plot')
plt.plot(year, permit_left_3["Job Type"], label='Block 4-5 plot')
plt.legend()
plt.title('Building Permit VS Distance from Second Avenue')



####  Phase 2

nodups = data.drop_duplicates(subset=['Block'])
nodups = nodups.loc[nodups['BOROUGH'].isin(['MANHATTAN'])]
nodups = nodups.dropna(subset=['Block','LATITUDE','LONGITUDE' ])
print('columns with null values:\n', nodups.isnull().sum())



rig = nodups['Block'].values
rig = rig.astype(int)

lat = nodups['LATITUDE'].values
lon = nodups['LONGITUDE'].values




#coordinates of planned phase 2 106 station: 40.790526 / -73.942509
#40.788051, -73.944323
#coordinates of planned phase 2 116 station: 40.797087 / -73.938084
#40.796026, -73.935446
#coordinates of planned phase 2 125 station: 40.8041855 / -73.933735
#40.803719, -73.935817

import math
print(math.pow(40.789658-40.790622,2) + math.pow(-73.940019+73.942445,2))

# Distance calculation

distance_1 = []
distance_2 = []
distance_3 = []

length = len(lat)
for i in range(length):
    print(i)
    distance_1.append((math.pow(lat[i]-40.790526,2) + math.pow(lon[i]+73.942509,2)))
    distance_2.append((math.pow(lat[i]-40.797087,2) + math.pow(lon[i]+73.938084,2)))
    distance_3.append((math.pow(lat[i]-40.8041855,2) + math.pow(lon[i]+73.933735,2)))
    


#1 block square distance (in coordinates diff. square): 0.00000129545
    #9.416220999970073e-06
#1-2 blocks square distance (in coordinates diff. square): 0.00000259091
    #8.084765000024125e-06
#2-3 blocks square distance (in coordinates diff. square): 0.00000388636
    #2.595386250003433e-06
    
stat_1 = 0.00000129545
stat_2 = 0.00000259091
stat_3 = 0.00000388636

stat_1_bl =[]
stat_2_bl =[]
stat_3_bl =[]

temp = []

for i in range(length):
    if distance_1[i] <= stat_1:
        stat_1_bl.append(i)
        temp.append(i)
    
    if distance_2[i] <= stat_1:
        stat_1_bl.append(i)
        temp.append(i)
    
    if distance_3[i] <= stat_1:
        stat_1_bl.append(i)
        temp.append(i)
    

### 2 block away

for i in range(length):
    if distance_1[i] <= stat_2:
        stat_2_bl.append(i)
        temp.append(i)
    
    if distance_2[i] <= stat_2:
        stat_2_bl.append(i)
        temp.append(i)
    
    if distance_3[i] <= stat_2:
        stat_2_bl.append(i)
        temp.append(i)


### 3 block away

for i in range(length):
    if distance_1[i] <= stat_3:
        stat_3_bl.append(i)
        temp.append(i)
    
    if distance_2[i] <= stat_3:
        stat_3_bl.append(i)
        temp.append(i)
    
    if distance_3[i] <= stat_3:
        stat_3_bl.append(i)
        temp.append(i)



stat_3_bl = list(set(stat_3_bl) - set(stat_2_bl))
stat_2_bl = list(set(stat_2_bl) - set(stat_1_bl))


ph = [stat_1_bl,stat_2_bl,stat_3_bl]

ph =  [item for sublist in ph for item in sublist]

indexes = []
for i in range(len(rig)):

    if rig[i] in ph:
        indexes.append(i) 



year = [i for i in range(1989,2020)]

phase2_1 = sub.loc[sub['Block'].isin(stat_1_bl)]
phase2_2 = sub.loc[sub['Block'].isin(stat_2_bl)]
phase2_3 = sub.loc[sub['Block'].isin(stat_3_bl)]

phase2_1 = phase2_1.groupby(['Filing Date']).count()
phase2_2 = phase2_2.groupby(['Filing Date']).count()
phase2_3 = phase2_3.groupby(['Filing Date']).count()


plt.figure(figsize=(15,10))
plt.plot(year, phase2_1["Job Type"], label='Block 1 plot')
plt.plot(year, phase2_2["Job Type"], label='Block 2-3 plot')
plt.plot(year, phase2_3["Job Type"], label='Block 4-5 plot')
plt.legend()
plt.title('Building Permit VS Distance from Second Avenue')


### Ploting

latitude_list = []
longitude_list = []

length = len(indexes)

for i in range(length):
    print(lat[indexes[i]])
    latitude_list.append(lat[indexes[i]])
    longitude_list.append(lon[indexes[i]])


gmap3 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap3.scatter( latitude_list, longitude_list, '# FF0000', 
                              size = 20, marker = False ) 
gmap3.scatter( lat, lon, '# FF0000', 
                              size = 20, marker = False ) 
gmap3.draw( "map11.html" ) 

   


############ Most expensive


neveredit2.dtypes

expensive = neveredit2.drop_duplicates(subset=['BIN'])

expensive = expensive.dropna(subset=['Latitude'])

lc = expensive.groupby(['Market Value per SqFt']).count()

pr_tot = lc.index.values.tolist()
pc_tot = lc.BIN.values.tolist()




plt.figure(figsize=(15,10))
plt.plot(pr_tot, pc_tot, label='Block 1 plot')

plt.legend()
plt.title('Number of Condos VS Market Value per SqFt')






ex1 = neveredit2.loc[neveredit2['Market Value per SqFt'].isin(range(0,125))]
ex1 = ex1.dropna(subset=['Latitude'])
ex2 = neveredit2.loc[neveredit2['Market Value per SqFt'].isin(range(125,180))]
ex2 = ex2.dropna(subset=['Latitude'])
ex3 = neveredit2.loc[neveredit2['Market Value per SqFt'].isin(range(180,225))]
ex3 = ex3.dropna(subset=['Latitude'])
ex4 = neveredit2.loc[neveredit2['Market Value per SqFt'].isin(range(225,350))]
ex4 = ex4.dropna(subset=['Latitude'])

gmap1 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap1.scatter( ex1['Latitude'], ex1['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 
gmap1.draw( "mapex1.html" ) 


gmap2 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap2.scatter( ex2['Latitude'], ex2['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 
gmap2.draw( "mapex2.html" ) 


gmap3 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap3.scatter( ex3['Latitude'], ex3['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 
gmap3.draw( "mapex3.html" ) 


gmap4 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap4.scatter( ex4['Latitude'], ex4['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap4.draw( "mapex4.html" ) 

gmap5 = gmplot.GoogleMapPlotter(40.790526, -73.942509, 13) 
gmap5.scatter( expensive['Latitude'], expensive['Longitude'], '# FF0000', 
                              size = 20, marker = False ) 

gmap5.draw( "mapex5.html" ) 

print('Train columns with null values:\n', ex1.isnull().sum())


####### Done






