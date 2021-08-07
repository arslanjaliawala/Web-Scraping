import pandas as pd
import os
import numpy as np
import datetime as dt


def getFilePath(filename):
    currentDir = os.getcwd()
    fullPath = os.path.join(currentDir,filename)
    return fullPath


def currentAge(dob):
    return (2021 - dob)

#1
df = pd.read_csv(getFilePath("police.csv"))
#2
#print(df.head())
#3
#print(df.shape)
#4
#print(df.info())
#5
df['stop_date'] = pd.to_datetime(df['stop_date'])
df['stop_time'] = pd.to_datetime(df['stop_time'])
#print(df.info())
#6
#print(df.isnull().sum())
#7
#print(df.head())
df.drop(['country_name'],axis=1, inplace=True)
#8
#print(df.describe())
#9
#print(df['search_type'].value_counts())
#10
#print(df['driver_gender'].isnull().sum())
df['driver_gender'].fillna(df['driver_gender'].mode,inplace=True)
#print(df['driver_gender'].isnull().sum())
#11
#print(df.sample(2))
#12
#print(df['driver_race'].nunique())
#13
#print(df.columns)
#14
#print(df.nsmallest(3,'driver_age'))
#print(df.nlargest(3,'driver_age'))
#15
#print(df.groupby('driver_race').agg(np.mean))
#16
#print(df.groupby('driver_race').get_group('Asian').agg(np.mean))
#print(df.groupby('driver_race').driver_age.describe())
#17
#print(df.loc[:5,['driver_gender','violation']])
#print(df.loc[(df.driver_age < 16) & (df.violation == 'Speeding')])
#print(df.iloc[:5,:5])
#18
#print(df[['stop_date','driver_age','driver_race','violation','stop_outcome']].sort_values(by='driver_age'))
#19
#print(df.query('45 < driver_age < 50').head())
#print(df.query('driver_gender == "F" and violation == "Speeding"').head())
#20
#print(df.set_index('stop_date').head(3))
#21
#print(df.duplicated().sum())
df.drop_duplicates(inplace=True)
#print(df.duplicated().sum())
#22
newdf = pd.get_dummies(df.driver_race,prefix='driver_race_').iloc[:,0:]
#print(newdf.head(10))
#23
numerical_df = df.select_dtypes(include = [np.number])
#print(numerical_df.head())
categorical_df = df.select_dtypes(include = [object])
#print(categorical_df.head())
#24
comb_df = pd.concat([numerical_df,categorical_df],axis =1 )
#print(comb_df.head(4))
#25
df['driver_current_age'] = df['driver_age_raw'].apply(currentAge)
#print(df['driver_current_age'].head())
#26
df['driver_age_qcut_bins'] = pd.qcut(df['driver_age'],q=5)
#print(df['driver_age_qcut_bins'].value_counts())
df['driver_age_cut_bins']=pd.cut(df['driver_age'],bins=3,labels=['1-21','22-60','61-100'])
print(df['driver_age_cut_bins'].value_counts())
#27
comb_df.to_csv('output.csv',index=False)