import pandas as pd
import glob
import numpy as np
from tabulate import tabulate

path = 'E:\\MonIOTr\\0%3Ae%3Af3%3A3b%3A85%3Ae5\\0-e-f3-3b-85-e5-dns.csv'
df = pd.read_csv(path,error_bad_lines=False,sep='\t')

class data_feature_extractor:
    def __init__(self, df):
        self.dataframe = df
        self.features = {}
        self.formatted = {
            "feature_strings": {},
            "feature_ips": {},
            "total_packets": {},
            'others':[]
        }
        self.totalPackets = len(self.dataframe)
    def feature_eth_src(self):
        ethsrc = self.dataframe["eth.src_resolved"]
        counts = ethsrc.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != 'eth.src_resolved':
                self.formatted['feature_strings'][name.split("_")[0]] = float(counts[name] / self.totalPackets)

    def pckt_length(self):
        pktlen = self.dataframe["_ws.col.Length"]
        print(pktlen)
        counts = pktlen.value_counts()
        name_list = counts.index.tolist()
        for each in pktlen.unique():
            if each != '_ws.col.Length':
                self.features[each] = 1
        for name in name_list:
            if name != '_ws.col.Length':
                self.formatted['others'].append(int(name))

    def dsn_answers_A(self):
        answer = self.dataframe["dns.a"].dropna().unique()
        #counts = answer.value_counts()
        #name_list = counts.index.tolist()
        temp=[]
        for each in answer:
            if each != 'dns.a':
                for every in each.split(","):
                    temp.append(every)
        counts={}
        for name in temp:
            counts[name]=temp.count(name)
        for name in counts:
                self.formatted['feature_ips'][name] = float(counts[name] / self.totalPackets)
    def cname(self):
        answer = self.dataframe["dns.cname"].dropna()

        counts = answer.value_counts()

        name_list = counts.index.tolist()
        for each in answer.unique():
            if each != 'dns.cname':
                for every in each.split(","):
                    self.features[every] = 1
        for name in name_list:
            if name != 'dns.cname':
                self.formatted['feature_strings'][name] = float(counts[name] / self.totalPackets)

    def qname(self):
        answer = self.dataframe["dns.qry.name"].dropna()
        counts = answer.value_counts()

        name_list = counts.index.tolist()
        for each in answer.unique():
            if each != 'dns.qry.name':
                for every in each.split(","):
                    self.features[every] = 1
        for name in name_list:
            if name != 'dns.qry.name':
                self.formatted['feature_strings'][name] = float(counts[name] / self.totalPackets)
    def rname(self):
        answer = self.dataframe["dns.resp.name"].dropna().unique()
        #counts = answer.value_counts()
        #name_list = counts.index.tolist()
        temp=[]
        for each in answer:
            if each != 'dns.resp.name':
                for every in each.split(","):
                    temp.append(every)
        counts={}
        for name in temp:
            counts[name]=temp.count(name)
        for name in counts:
            self.formatted['feature_strings'][name] = float(counts[name] / self.totalPackets)
    def formatted_output(self):
        self.feature_eth_src()
        self.pckt_length()
        self.dsn_answers_A()
        self.cname()
        self.qname()
        self.rname()
        totalCount = len(self.dataframe)
        self.formatted['total_packets'] = totalCount
        print (self.formatted)
        return self.formatted
fe_obj = data_feature_extractor(df)
fe_obj.formatted_output()