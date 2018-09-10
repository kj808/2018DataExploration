#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Import the first dataset (Massachusetts high school)
mshs=pd.read_csv('../data/external/MA_Public_Schools_2017.csv')

#Import the second dataset (University data)
univ=pd.read_json('../data/external/schoolInfo.json')

#Cleaning MA high school data

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

#Dropping additional columns based on name based on findings and reevaluations. 
#The additional dropping due to irrelevant information and not following certain exploratory paths.
#One example is using ZIP codes in MA to determine if certain areas present better education

mshsFinal=mshsFinal.drop(columns=['School Code','Function','Contact Name','Address 1','Address 2','Phone','Fax','Grade','PK_Enrollment','K_Enrollment', '1_Enrollment',
                                  '2_Enrollment','3_Enrollment','4_Enrollment','5_Enrollment','6_Enrollment',
                                  '7_Enrollment', '8_Enrollment','9_Enrollment','10_Enrollment','11_Enrollment',
                                  'Accountability and Assistance Description','District_Accountability and Assistance Level',
                                  'District_Accountability and Assistance Description','Progress and Performance Index (PPI) - High Needs Students',
                                  'District_Progress and Performance Index (PPI) - High Needs Students','District Name','District Code',
                                 'SP_Enrollment','School Type', 'Town','Average Class Size', 'Number of Students', 
                                  'SAT_Tests Taken','Average SAT_Writing','School Accountability Percentile (1-99)',
                                  'Progress and Performance Index (PPI) - All Students','District_Progress and Performance Index (PPI) - All Students',])


##Remove all non high schools or nonenrollment of seniors
mshsFinal=mshsFinal[mshsFinal['12_Enrollment'] > 0]

#Drop the column
mshsFinal=mshsFinal.drop(columns=['12_Enrollment'])

##Remove all rows without district performance progress
mshsFinal=mshsFinal.dropna(subset=['Accountability and Assistance Level'])

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
                        'rankingDisplayScore','rankingSortRank','tuition','city','region'])

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

##----------------Plot the different average SAT scores of high schools in MA vs Universities----------------
#Plot average SAT scores 1 line is high school and 1 line is university
#export the sat-avg and School Type
SATforType=result[['sat-avg','schoolType']].copy()

#categorize school type
SATforType['schoolType']=SATforType['schoolType'].astype("category")

#Sample about 100 data points
SATforType=SATforType.sample(n=300)

##----------------Plot the different average SAT scores of MA high schools in MA universities----------------
#Copy dataframe consisting of only avg SAT scores, school type and state
SATMA=result[['sat-avg','schoolType','State']].copy()

#Ensure only viewing institutions in MA
SATMA=SATMA.loc[SATMA['State']=='MA']

#Sepearate high schools from universities
HSSAT=SATMA.loc[SATMA['schoolType'] == 'high-school'].copy()
USAT=SATMA.loc[SATMA['schoolType'] == 'national-universities'].copy()

#Create new Dataframe as High School and University are separated with average SAT for easy plotting
SATforType=pd.DataFrame(data={'High School SAT':HSSAT['sat-avg'], 'University SAT':USAT['sat-avg']})

#Sample SAT from high schools as high schools contain 321 values as only 16 values of universities exist in MA.
SATforType['High School SAT']=SATforType['High School SAT'].sample(n=209)
SATforType.plot.box()


#plot based on school type
SATforType.boxplot(by='schoolType')

#Format graph
plt.title("HS vs University Average SAT")
plt.suptitle("")
plt.ylabel("SAT Scores")
plt.xlabel("Institution Type")

##----------------Plot the different average SAT scores of MA high schools in MA universities----------------
#Copy dataframe consisting of only avg SAT scores, school type and state
SATMA=result[['sat-avg','schoolType','State']].copy()

#Ensure only viewing institutions in MA
SATMA=SATMA.loc[SATMA['State']=='MA']

#Sepearate high schools from universities
HSSAT=SATMA.loc[SATMA['schoolType'] == 'high-school'].copy()
USAT=SATMA.loc[SATMA['schoolType'] == 'national-universities'].copy()

#Create new Dataframe as High School and University are separated with average SAT for easy plotting
SATforType=pd.DataFrame(data={'High School SAT':HSSAT['sat-avg'], 'University SAT':USAT['sat-avg']})

#Sample SAT from high schools as high schools contain 321 values as only 16 values of universities exist in MA.
SATforType['High School SAT']=SATforType['High School SAT'].sample(n=209)
SATforType.plot.box()

##----------------Plot PPI vs SAT----------------
#Copy dataframe consisting of only avg SAT scores, school type and state
SATMA=result[['sat-avg','schoolType','State', 'Accountability and Assistance Level']].copy()

#Ensure only viewing institutions in MA
SATMA=SATMA.loc[SATMA['State']=='MA']

#Set all universities Account/Assis level to 'University' for easy plotting
SATMA['Accountability and Assistance Level'] = np.where(SATMA['schoolType']=='national-universities','University',SATMA['Accountability and Assistance Level'])

#Categorize the account/assis level for plotting
SATMA['Accountability and Assistance Level']=SATMA['Accountability and Assistance Level'].astype("category")

#Separate the different levels due to difference in amount of data then sample level 1, level 2 and level 3 to provide better sample
#HS Level 1 =109 rows
#HS L2=149 rows 
#HS L3=59 rows
#HS L4=8 rows
#Univ=16 rows

HSL1=SATMA.loc[SATMA['Accountability and Assistance Level'] == 'Level 1'].copy().sample(92)
HSL2=SATMA.loc[SATMA['Accountability and Assistance Level'] == 'Level 2'].copy().sample(129)
HSL3=SATMA.loc[SATMA['Accountability and Assistance Level'] == 'Level 3'].copy().sample(54)
HSL4=SATMA.loc[SATMA['Accountability and Assistance Level'] == 'Level 4'].copy()
Univ=SATMA.loc[SATMA['Accountability and Assistance Level'] == 'University'].copy()

#Remerge the dataset
HSL1=pd.concat([HSL1,HSL2],axis=0,sort=False )
HSL1=pd.concat([HSL1,HSL3],axis=0,sort=False )
HSL1=pd.concat([HSL1,HSL4],axis=0,sort=False )
HSL1=pd.concat([HSL1,Univ],axis=0,sort=False )

#Plot the results
HSL1.boxplot(by='Accountability and Assistance Level')

#Format graph
plt.title("HS Act/Assis Levels SAT vs University")
plt.suptitle("")
plt.ylabel("SAT Scores")
plt.xlabel("Levels of Institutions")




