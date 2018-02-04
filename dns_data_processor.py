import pandas as pd
import glob
import numpy as np
from tabulate import tabulate

path = 'E:\\MonIOTr\\0%3Ae%3Af3%3A3b%3A85%3Ae5\\0-e-f3-3b-85-e5-dns.csv'
df = pd.read_csv(path,error_bad_lines=False,sep='\t')
        

class data_feature_extractor:
    def __init__(self,df):
        self.dataframe=df
        self.features={}
        
    def feature_eth_src(self):
        ethsrc=self.dataframe["eth.src_resolved"]
        unique_list=ethsrc.unique()      
        for each in  unique_list:
            if each !='eth.src_resolved': 
                self.features[each.split("_")[0]]=1
                    
    def pckt_length(self):
        pktlen=self.dataframe["_ws.col.Length"].unique()
        
        for each in  pktlen:
            if each !='_ws.col.Length': 
                self.features[each]=1
            
    def dsn_answers_A(self):
        answer=self.dataframe["dns.a"].dropna().unique()
        for each in  answer:
            if each !='dns.a': 
                
                for every in each.split(","):
                    self.features[every]=1
        
                  
        
        
        
fe_obj=data_feature_extractor(df)

fe_obj.feature_eth_src()
fe_obj.pckt_length()
fe_obj.dsn_answers_A()