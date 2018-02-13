#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 20:50:19 2017

@author: guptasoumya
"""
import numpy as np
import pandas as pd
import math
import sys


class DonationAnalytics():
    def __init__(self,file1,file2):
        #reads and converts the input into a dataframe
        raw_data=open(file2,encoding='utf-8',errors='ignore').readlines()
        self.percentile=int([line.rstrip() for line in raw_data][0])
        self.df= pd.read_table(file1,header=None, delimiter='|',converters={10:str})
     
    def preProcessing(self):
        #Rename columns for better understanding
        self.df = self.df.rename(columns={0:'CMTE_ID',7:'NAME',10:'ZIP_CODE',13:'TRANSACTION_DT',14:'TRANSACTION_AMT',15:'OTHER_ID'})
        df = self.df[['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']].copy()
        #Identify and remove OTHER IDs with some values
        df['OTHER_ID']=df['OTHER_ID'].fillna(0) 
        df= df[df['OTHER_ID']==0]
        df = df.drop(['OTHER_ID'],axis=1)
        # Identify and remove NAME empty 
        df['NAME']=df['NAME'].fillna(0) 
        df= df[df['NAME']!=0]
        # Identify and remove CMTE_ID empty 
        df['CMTE_ID']=df['CMTE_ID'].fillna(0) 
        df= df[df['CMTE_ID']!=0]
        # Identify and remove TRANSACTION_AMT empty 
        df['TRANSACTION_AMT']=df['TRANSACTION_AMT'].fillna(0) 
        df= df[df['TRANSACTION_AMT']!=0]
        # Identify and remove ZIP_CODE empty 
        df['ZIP_CODE']=df['ZIP_CODE'].fillna(0) 
        df= df[df['ZIP_CODE']!=0]
        # Identify and remove TRANSACTION_DT empty 
        df['TRANSACTION_DT']=df['TRANSACTION_DT'].fillna(0) 
        df= df[df['TRANSACTION_DT']!=0]
        # Identify year of donation
        df['YEAR'] = df['TRANSACTION_DT']%10000
        # Identify and remove ZIP_CODE less than 5
        zip_flag = df['ZIP_CODE'].map(lambda x: False if len(x)<5 else True)
        df = df.loc[zip_flag,:]
        # Only first five characters of a ZIP CODE
        df['ZIP_CODE'] = df['ZIP_CODE'].apply(lambda x:x[:5])
        # Identify duplicate/ return donors
        df1 = df[df.duplicated(subset={'NAME','ZIP_CODE'},keep='first')]
        # New column for cumulative donations
        df1['CUMSUM'] = df1['TRANSACTION_AMT'].cumsum()
        # Reset index
        df1.index = np.arange(1, len(df1) + 1)
        
        return(df1)
        
    def create_output(self,df1,output):
         file=open(output,"w")
         for idx, row in df1.iterrows():
             percentile_index=(math.ceil((self.percentile/100)*idx))-1
             file.write("{}|{}|{}|{}|{}|{}\n".\
                                format(row['CMTE_ID'],row['ZIP_CODE'],row['YEAR'],
                                       df1['TRANSACTION_AMT'].iloc[percentile_index],row['CUMSUM'],idx))
         file.close()   
         return(None)
         
    
if __name__ == "__main__":
    #take in first input as input file name 1
    file1=sys.argv[1]
    #take in first input as input file name 2
    file2=sys.argv[2]
    #third input as output file name 2
    output=sys.argv[3]
    political_donors=DonationAnalytics(file1,file2)
    #call the class FindPoliticalDonors and the functions to create the output files
    df=political_donors.preProcessing()
    political_donors.create_output(df,output)

        