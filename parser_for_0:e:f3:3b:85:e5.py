import os, sys, subprocess
import pandas as pd
import glob


def parse(path):

    full_path = os.path.join(os.getcwd(), path)
    full_path = full_path + "/*.pcap"

    columns = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Length -e eth.src -e eth.src_resolved -e eth.dst -e eth.dst_resolved -e udp.port -e dns.a -e dns.aaaa -e dns.cname -e dns.count.answers -e dns.count.add_rr -e dns.count.auth_rr -e dns.count.labels -e dns.count.prerequisites -e dns.count.queries -e dns.count.updates -e dns.qry.name -e dns.qry.name.len -e dns.qry.class -e dns.qry.type -e dns.resp.name -e dns.resp.type -e dns.resp.class -e dns.resp.ttl -e dns.resp.len"
    output_name = ">> output.csv"
    file = open("output.csv", "w+")
    for f in glob.glob(full_path):
        command = "tshark -r " + f + " -Y 'dns' -T fields -E header=y -E separator=/t, " + columns + output_name
        # k = subprocess.Popen(command, shell=True)
        os.system(command)
        # file.write('\n')
    # col = ["src", "dest"]
    df = pd.read_csv("output.csv", sep='\t')
    print df.head


if __name__ == "__main__":
    path = sys.argv[1]
    parse(path)