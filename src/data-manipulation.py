#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Import the first dataset (Massachusetts high school)
mshs=pd.read_csv('../data/external/MA_Public_Schools_2017.csv')

#Import the second dataset (University data)
univ=pd.read_json('../data/external/schoolInfo.json')

#Cleaning up MA high school data

#------------Dropping Columns------------
#Drop columns regarding MCAS scores
mshsFirst=mshs.iloc[:,0:31].copy()

mshsSecond=mshs.iloc[:,93:97].copy()

mshsLast=mshs.iloc[:,293:302].copy()

#also drop all demographics of students.
mshsdemo=mshs.iloc[:,51:53].copy()


#merge the tables
mshsFinal=mshsFirst.join(mshsdemo, how='outer')
mshsFinal=mshsFinal.join(mshsSecond, how='outer')
mshsFinal=mshsFinal.join(mshsLast, how='outer')

#Dropping...
#Contact name: column 5--- not irrelevant in detecting acceptance to universities
#Address 1 & 2: column 6,7---also not irrelevant. Can generalize by state.
#Phone and Fax:col 10,11---also not irrelevant

mshsFinal=mshsFinal.drop(columns=['School Code','Function','Contact Name','Address 1','Address 2','Phone','Fax','Grade','PK_Enrollment','K_Enrollment', '1_Enrollment',
                                  '2_Enrollment','3_Enrollment','4_Enrollment','5_Enrollment','6_Enrollment',
                                  '7_Enrollment', '8_Enrollment','9_Enrollment','10_Enrollment','11_Enrollment',
                                  'Accountability and Assistance Description','District_Accountability and Assistance Level',
                                  'District_Accountability and Assistance Description','Progress and Performance Index (PPI) - High Needs Students',
                                  'District_Progress and Performance Index (PPI) - High Needs Students','District Name','District Code',
                                 'SP_Enrollment','School Type', 'Town'])


##Remove all non high schools or nonenrollment of seniors
mshsFinal=mshsFinal[mshsFinal['12_Enrollment'] > 0]

#Drop the column
mshsFinal=mshsFinal.drop(columns=['12_Enrollment'])

##Remove all rows without SAT data and district performance progress
mshsFinal=mshsFinal.dropna(subset=['School Accountability Percentile (1-99)'])

#Remove all rows without average SAT reading and SAT Math
mshsFinal=mshsFinal[mshsFinal['Average SAT_Reading']>0]
mshsFinal=mshsFinal[mshsFinal['Average SAT_Math']>0]
##-----------------------------------------------------------------------------------------
#Cleaning up university data

#----------Dropping columns----------
#Not relevant
univ=univ.drop(columns=['primaryKey','act-avg','aliasNames','businessRepScore','sortName',
                        'primaryPhoto','primaryPhotoThumb','rankingType','rankingMaxPossibleScore',
                        'rankingDisplayName','rankingNoteText','rankingNoteCharacter','sortName',
                        'urlName','xwalkId','nonResponder','nonResponderText','rankingIsTied',
                        'rankingRankStatus','engineeringRepScore','isPublic','cost-after-aid', 
                        'hs-gpa-avg', 'overallRank','percent-receiving-aid', 'rankingDisplayRank', 
                        'rankingDisplayScore','rankingSortRank','tuition','city'])

#remove NaN entries in sat-avg
univ=univ.dropna(subset=['sat-avg'])

#----------Transforming High School Data----------
#Transform high school public to boolean
#The data on school type is public OR charter school.
#charter schools seen as public from federal education department
mshsFinal['Institutional Control']=True

#Change TOTAL Enrollment to Enrollment
mshsFinal.rename(columns={'TOTAL_Enrollment':'Enrollment'},inplace=True)

#Add column categorizing high schools vs universities (will help with merge)
mshsFinal.loc[:,'schoolType']=pd.Series('high-school', index=mshsFinal.index, dtype="category")

#Adding column and calculating average SAT scores
mshsFinal.loc[:,'sat-avg']=mshsFinal['Average SAT_Reading']+mshsFinal['Average SAT_Math']

#----------Transforming University Data----------
#Change column for university name, city, zip, enrollment, and private/public institution for merge
univ.rename(columns={'displayName':'School Name', 'city':'City','zip':'Zip', 
                     'state':'State','enrollment':'Enrollment',
                     'institutionalControl':'Institutional Control'}, inplace=True)
                     
#----------Merge datasets----------
result=pd.concat([mshsFinal,univ],axis=0,sort=False )

#----------------Randomize data----------------
result=result.sample(frac=1)

