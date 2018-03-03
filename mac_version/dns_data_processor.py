import pandas as pd
import glob
import numpy as np
import json

class data_feature_extractor:
    def __init__(self, df,df_http):
        self.dataframe = df
        self.dataframe_http=df_http
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
            if name != 'eth.src_resolved' and 'PcPartne_' not in name:
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

    def content_length(self):
        print(self.dataframe_http)
        conLen = self.dataframe_http["http.content_length"]
        counts = conLen.value_counts()
        name_list = counts.index.tolist()
        for each in conLen.unique():
            if each != 'http.content_length':
                self.features[each] = 1
        for name in name_list:
            if name != 'http.content_length':
                self.formatted['others'].append(int(name))

    def content_type(self):
        conType = self.dataframe_http["http.content_type"]
        counts = conType.value_counts()
        name_list = counts.index.tolist()
        for each in conType.unique():
            if each != 'http.content_type':
                self.features[each] = 1
        for name in name_list:
            if name != 'http.content_type':
                self.formatted['others'].append(name)
    def feature_http_host(self):
        host = self.dataframe_http["http.host"]
        counts = host.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.host":
                self.formatted["feature_strings"][name.split("_")[0]] = float(counts[name] / self.totalPackets)
    def feature_http_request_uri(self):
        uri = self.dataframe_http["http.request.uri"]
        counts = uri.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.request.uri":
                self.formatted["feature_strings"][name.split("_")[0]] = float(counts[name] / self.totalPackets)
    def feature_http_server(self):
        server = self.dataframe_http["http.server"]
        counts = server.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.server":
                self.formatted["feature_strings"][name.split("_")[0]] = float(counts[name] / self.totalPackets)
    def feature_http_response(self):
        res = self.dataframe_http["http.response.line"]
        counts = res.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.response.line":
                self.formatted['feature_strings'][name]=float(counts[name] / self.totalPackets)
    def formatted_output(self):
        self.feature_eth_src()
        #self.pckt_length()
        #self.dsn_answers_A()
        self.cname()
        self.qname()
        self.rname()
        #self.content_length()
        #self.content_type()

        self.feature_http_host()
        self.feature_http_request_uri()
        #self.feature_http_response()
        self.feature_http_server()
        totalCount = len(self.dataframe)
        self.formatted['total_packets'] = totalCount

        return self.formatted



