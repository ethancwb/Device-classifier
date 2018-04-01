import pandas as pd
import glob
import numpy as np
import json
import statistics
import configuration

class data_feature_extractor:
    def __init__(self, df,df_http,df_general,df_dstport,df_payload):
        self.dataframe = df
        self.dataframe_http=df_http
        self.dataframe_general=df_general
        self.dataframe_dstport=df_dstport
        self.dataframe_payload=df_payload
        self.features = {}
        self.formatted = {
            "feature_strings": {},
            "feature_ips": {},
            "total_packets": {},
            'others':{}
        }
        self.totalPackets_dns = len(self.dataframe)
        self.totalPackets_http = len(self.dataframe_http)
        self.totalPackets_general = len(self.dataframe_general)
        self.totalPackets_dstport = len(self.dataframe_dstport)
        self.totalPackets_payload = len(self.dataframe_payload)

    def feature_eth_src(self):
        ethsrc = self.dataframe["eth.src_resolved"]
        counts = ethsrc.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != 'eth.src_resolved' and 'PcPartne_' not in name:
                if self.totalPackets_dns != 0:
                    self.formatted['feature_strings'][name.split("_")[0]] = float(counts[name] / self.totalPackets_dns)

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
            if self.totalPackets_dns != 0:
                self.formatted['feature_ips'][name] = float(counts[name] / self.totalPackets_dns)

    def cname(self):
        answer = self.dataframe["dns.cname"].dropna()

        counts = answer.value_counts()

        name_list = counts.index.tolist()
        for each in answer.unique():
            if each != 'dns.cname':
                for every in each.split(","):
                    if "_" in every:
                        self.features[every.split("_")[0]] = 1
                    elif "." in every:
                        str_list = every.split(".")
                        if len(str_list) > 2:
                            self.features[str_list[-2] + "." + str_list[-1]] = 1
                    else:
                        self.features[every] = 1
        for names in name_list:
            if names != 'dns.cname':
                for name in names.split(","):
                    if "_" in name:
                        if self.totalPackets_dns != 0:
                            self.formatted['feature_strings'][name.split("_")[0]] = float(counts[names] / self.totalPackets_dns)
                    elif "." in name:
                        str_list = name.split(".")
                        if len(str_list) > 2:
                            if self.totalPackets_dns != 0:
                                self.formatted['feature_strings'][str_list[-2] + "." + str_list[-1]] = float(counts[names] / self.totalPackets_dns)
                    else:
                        self.formatted['feature_strings'][name] = float(counts[names] / self.totalPackets_dns)

    def qname(self):
        answer = self.dataframe["dns.qry.name"].dropna()
        counts = answer.value_counts()

        name_list = counts.index.tolist()

        for each in answer.unique():
            if each != 'dns.qry.name':
                for every in each.split(","):
                    if "_" in every:
                        self.features[every.split("_")[0]] = 1
                    elif "." in every:
                        str_list = every.split(".")
                        if len(str_list) > 2:
                            self.features[str_list[-2] + "." + str_list[-1]] = 1
                    else:
                        self.features[every] = 1
        for names in name_list:
            if names != 'dns.qry.name':
                for name in names.split(","):
                    if "_" in name:
                        if self.totalPackets_dns != 0:
                            self.formatted['feature_strings'][name.split("_")[0]] = float(counts[names] / self.totalPackets_dns)
                    elif "." in name:
                        str_list = name.split(".")
                        if len(str_list) > 2:
                            if self.totalPackets_dns != 0:
                                self.formatted['feature_strings'][str_list[-2] + "." + str_list[-1]] = float(counts[names] / self.totalPackets_dns)
                    else:
                        if self.totalPackets_dns != 0:
                            self.formatted['feature_strings'][name] = float(counts[names] / self.totalPackets_dns)

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
        for names in counts:
            for name in names.split(","):
                if "_" in name:
                    if self.totalPackets_dns != 0:
                        self.formatted['feature_strings'][name.split("_")[0]] = float(counts[names] / self.totalPackets_dns)
                elif "." in name:
                    str_list = name.split(".")
                    if len(str_list) > 2:
                        self.formatted['feature_strings'][str_list[-2] + "." + str_list[-1]] = float(
                            counts[names] / self.totalPackets_dns)
                else:
                    if self.totalPackets_dns != 0:
                        self.formatted['feature_strings'][name] = float(counts[names] / self.totalPackets_dns)

    def protocol(self):
        answer = self.dataframe_general["frame.protocols"].dropna()

        counts = answer.value_counts()

        name_list = counts.index.tolist()
        for names in name_list:
            if names != 'frame.protocols':
                for name in names.split(","):
                    if "eth:ethertype:ip" in name:
                        if self.totalPackets_general != 0:
                            self.formatted['feature_strings'][name.split(":")[-1]] = float(counts[names] / self.totalPackets_general)
                    else:
                        if self.totalPackets_general != 0:
                            self.formatted['feature_strings'][name] = float(counts[names] / self.totalPackets_general)

    def dstport(self):
        answer_udp = self.dataframe_dstport["udp.dstport"].dropna()
        answer_tcp = self.dataframe_dstport["tcp.dstport"].dropna()

        counts_udp = answer_udp.value_counts()
        counts_tcp = answer_tcp.value_counts()

        name_list = counts_udp.index.tolist() + counts_tcp.index.tolist()
        count_known_ports = 0
        count_registered_ports = 0
        count_private_ports = 0

        for names in name_list:
            if names != 'udp.dstport' and names != 'tcp.dstport':
                port = int(names)
                if port in range(0, 1024):
                    count_known_ports += 1
                elif port in range(1024, 49152):
                    count_registered_ports += 1
                elif port >= 49152:
                    count_private_ports += 1

        self.formatted['others']['known_ports'] = count_known_ports / self.totalPackets_dstport
        self.formatted['others']['registered_ports'] = count_registered_ports / self.totalPackets_dstport
        self.formatted['others']['private_ports'] = count_private_ports / self.totalPackets_dstport

    def payload_size(self):
        parsed_df = self.dataframe_payload.fillna(0)
        payload_array = []
        for index, row in parsed_df.iterrows():
            ip_len = row[0]
            ip_hdr_len = row[1]
            tcp_hdr_len = row[2]
            if "," not in str(ip_len) or "," not in (ip_hdr_len):
                payload_array.append(float(ip_len) - float(ip_hdr_len) - float(tcp_hdr_len))
        payload_array = list(filter(lambda x : x != float(0.0), payload_array))
        self.formatted['others']['payload_max'] = max(payload_array)
        self.formatted['others']['payload_mean'] = np.mean(payload_array)
        self.formatted['others']['payload_min'] = min(payload_array)
        self.formatted['others']['payload_std'] = statistics.stdev(payload_array)

    def time_delta(self):
        answer = self.dataframe_general['frame.time_delta'].dropna()
        answer_list = list(filter(lambda x : "frame.time_delta" not in str(x), answer.tolist()))
        time_list = list(map(lambda x : float(x), answer_list))
        self.formatted['others']['time_max'] = max(time_list)
        self.formatted['others']['time_mean'] = np.mean(time_list)
        self.formatted['others']['time_min'] = min(time_list)
        self.formatted['others']['time_std'] = statistics.stdev(time_list)

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
                if "_" in name:
                    if self.totalPackets_http != 0:
                        self.formatted['feature_strings'][name.split("_")[0]] = float(counts[name] / self.totalPackets_http)
                elif "." in name:
                    str_list = name.split(".")
                    if len(str_list) > 2:
                        if self.totalPackets_http != 0:
                            self.formatted['feature_strings'][str_list[-2] + "." + str_list[-1]] = float(counts[name] / self.totalPackets_http)
                else:
                    if self.totalPackets_http != 0:
                        self.formatted['feature_strings'][name] = float(counts[name] / self.totalPackets_http)

    def feature_http_request_uri(self):
        uri = self.dataframe_http["http.request.uri"]
        counts = uri.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.request.uri":
                if self.totalPackets_http != 0:
                    self.formatted["feature_strings"][name.split("_")[0]] = float(counts[name] / self.totalPackets_http)

    def feature_http_server(self):
        server = self.dataframe_http["http.server"]
        counts = server.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.server":
                if self.totalPackets_http != 0:
                    self.formatted["feature_strings"][name.split("_")[0]] = float(counts[name] / self.totalPackets_http)

    def feature_http_response(self):
        res = self.dataframe_http["http.response.line"]
        counts = res.value_counts()
        name_list = counts.index.tolist()
        for name in name_list:
            if name != "http.response.line":
                if self.totalPackets_http != 0:
                    self.formatted['feature_strings'][name]=float(counts[name] / self.totalPackets_http)

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
        #self.feature_http_request_uri()
        #self.feature_http_response()
        self.feature_http_server()
        self.protocol()
        self.dstport()
        self.payload_size()
        self.time_delta()

        return self.formatted
# dev="18-b4-30-c8-d8-28"
# train_path=configuration.Train_loc
# f_dns = open(train_path+dev+'-dns.csv')
# f_http = open(train_path+dev+'-http.csv')
# f_general = open(train_path+dev+'-general.csv')
# f_dstport = open(train_path+dev+'-dstport.csv')
# f_payload = open(train_path+dev+'-payload.csv')
# df = pd.read_csv(f_dns, error_bad_lines=False, sep='\t')
#
# df_http = pd.read_csv(f_http, error_bad_lines=False, sep='\t')
# print("here")
# df_general = pd.read_csv(f_general,low_memory=False,error_bad_lines=False, sep='\t')
# print("here")
# df_dstport = pd.read_csv(f_dstport, low_memory=False,error_bad_lines=False, sep='\t')
# print("here")
# df_payload = pd.read_csv(f_payload, error_bad_lines=False, sep='\t')
# print('here')
#
# d = data_feature_extractor(df, df_http, df_general, df_dstport, df_payload)
# print(d.formatted_output())
