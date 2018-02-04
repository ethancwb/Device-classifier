import os, sys, subprocess
import pandas as pd
from tabulate import tabulate
import glob


def parse(path):

    full_path = os.path.join(os.getcwd(), path)
    full_path = full_path + "/*.pcap"

    columns_dns = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Length -e eth.src -e eth.src_resolved -e eth.dst -e eth.dst_resolved -e udp.port -e dns.a -e dns.aaaa -e dns.cname -e dns.count.answers -e dns.count.add_rr -e dns.count.auth_rr -e dns.count.labels -e dns.count.prerequisites -e dns.count.queries -e dns.count.updates -e dns.qry.name -e dns.qry.name.len -e dns.qry.class -e dns.qry.type -e dns.resp.name -e dns.resp.type -e dns.resp.class -e dns.resp.ttl -e dns.resp.len"
    output_name_dns = ">> 0:e:f3:3b:85:e5-dns.csv"
    for f in glob.glob(full_path):
        command = "tshark -r " + f + " -Y 'dns' -T fields -E header=y -E separator=/t, " + columns_dns + output_name_dns
        os.system(command)
    df = pd.read_csv("0:e:f3:3b:85:e5-dns.csv", sep='\t')
    print tabulate(df, headers='keys', tablefmt='psql')
    # print df.head

    columns_http = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Length -e eth.src -e eth.src_resolved -e eth.dst -e eth.dst_resolved -e tcp.port -e http.content_length -e http.content_type -e http.host -e http.request -e http.request.uri -e http.server -e http.time -e http.response.line"
    output_name_http = ">> 0:e:f3:3b:85:e5-http.csv"
    for f in glob.glob(full_path):
        command = "tshark -r " + f + " -Y 'http' -T fields -E header=y -E separator=/t, " + columns_http + output_name_http
        os.system(command)
    df = pd.read_csv("0:e:f3:3b:85:e5-http.csv", sep='\t')
    print tabulate(df, headers='keys', tablefmt='psql')
    # print df.head

if __name__ == "__main__":
    path = sys.argv[1]
    parse(path)