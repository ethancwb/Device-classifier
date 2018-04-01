import os, sys, subprocess
import pandas as pd
import math
import glob
import configuration



def parse(path):
    full_path = os.path.join(os.getcwd(), path)
    print (os.listdir(full_path))
    devices = os.listdir(full_path)
    for d in devices:
        path = full_path + '/' + d
        if os.path.isdir(path):
            path += "/*.pcap"
            test_file = max(glob.glob(path), key = os.path.getmtime)
            # part 1, dns features
            columns_dns = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Length -e eth.src -e eth.src_resolved -e eth.dst -e eth.dst_resolved -e udp.port -e dns.a -e dns.aaaa -e dns.cname -e dns.count.answers -e dns.count.add_rr -e dns.count.auth_rr -e dns.count.labels -e dns.count.prerequisites -e dns.count.queries -e dns.count.updates -e dns.qry.name -e dns.qry.name.len -e dns.qry.class -e dns.qry.type -e dns.resp.name -e dns.resp.type -e dns.resp.class -e dns.resp.ttl -e dns.resp.len"
            output_name_dns = ""
            for f in glob.glob(path):
                if f == test_file:
                    output_name_dns = ">> csvs/" + d.replace(':', '-') + "-test-dns.csv"
                else:
                    output_name_dns = ">> csvs/" + d.replace(':', '-') + "-dns.csv"
                command = "tshark -r " + f + " -Y 'dns' -T fields -E header=y -E separator=/t, " + columns_dns + output_name_dns
                os.system(command)
            dns_file = "csvs/" + d.replace(':', '-') + "-dns.csv"
            lines = []
            line_count = 0
            try:
                dns_f = open(dns_file)
                for line in dns_f:
                    if line_count == 0 or "ip.src" not in line:
                        if line_count < 180:
                            line_count += 1
                            lines.append(line)
                        else:
                            dns_f.close()
                            break
                if line_count < 180:
                    os.remove(dns_file)
                    os.remove("csvs/" + d.replace(':', '-') + "-test-dns.csv")
                else:
                    dns_f = open(dns_file, "w")
                    for l in lines:
                        dns_f.write(l)
            except:
                print(dns_file, " error")
            # part 2, http features
            columns_http = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Length -e eth.src -e eth.src_resolved -e eth.dst -e eth.dst_resolved -e tcp.port -e http.content_length -e http.content_type -e http.host -e http.request -e http.request.uri -e http.server -e http.time -e http.response.line"
            output_name_http = ""
            for f in glob.glob(path):
                if f == test_file:
                    output_name_http = ">> csvs/" + d.replace(':', '-') + "-test-http.csv"
                else:
                    output_name_http = ">> csvs/" + d.replace(':', '-') + "-http.csv"
                command = "tshark -r " + f + " -Y 'http' -T fields -E header=y -E separator=/t, " + columns_http + output_name_http
                os.system(command)
            http_file = "csvs/" + d.replace(':', '-') + "-http.csv"
            lines = []
            line_count = 0
            try:
                http_f = open(http_file)
                for line in http_f:
                    if line_count == 0 or "ip.src" not in line:
                        if line_count < 40:
                            line_count += 1
                            lines.append(line)
                        else:
                            http_f.close()
                            break
                if line_count < 40:
                    os.remove(http_file)
                    os.remove("csvs/" + d.replace(':', '-') + "-test-http.csv")
                else:
                    http_f = open(http_file, "w")
                    for l in lines:
                        http_f.write(l)
            except:
                print(http_file, " error")
            # part 3, protocol features
            columns_general = "-e frame.protocols -e frame.time_delta"
            output_name_general = ""
            for f in glob.glob(path):
                if f == test_file:
                    output_name_general = ">> csvs/" + d.replace(':', '-') + "-test-general.csv"
                else:
                    output_name_general = ">> csvs/" + d.replace(':', '-') + "-general.csv"
                command = "tshark -r " + f + " -T fields -E header=y -E separator=/t, " + columns_general + output_name_general
                os.system(command)
            # part 4, destination port features
            columns_dstport = "-e tcp.dstport -e udp.dstport"
            output_name_dstport = ""
            for f in glob.glob(path):
                if f == test_file:
                    output_name_dstport = ">> csvs/" + d.replace(':', '-') + "-test-dstport.csv"
                else:
                    output_name_dstport = ">> csvs/" + d.replace(':', '-') + "-dstport.csv"
                command = "tshark -r " + f + " -T fields -E header=y -E separator=/t, " + columns_dstport + output_name_dstport
                os.system(command)
            # part 5, payload features
            columns_payload = "-e ip.len -e ip.hdr_len -e tcp.hdr_len"
            output_name_payload = ""
            for f in glob.glob(path):
                if f == test_file:
                    output_name_payload = ">> csvs/" + d.replace(':', '-') + "-test-payload.csv"
                else:
                    output_name_payload = ">> csvs/" + d.replace(':', '-') + "-payload.csv"
                command = "tshark -r " + f + " -T fields -E header=y -E separator=/t, " + columns_payload + output_name_payload
                os.system(command)
            payload_file = "csvs/" + d.replace(':', '-') + "-payload.csv"
            lines = []
            line_count = 0
            try:
                payload_f = open(payload_file)
                for line in payload_f:
                    if line_count == 0 or "ip.len" not in line:
                        if line_count < 400:
                            line_count += 1
                            lines.append(line)
                        else:
                            payload_f.close()
                            break
                if line_count < 400:
                    os.remove(payload_file)
                else:
                    payload_f = open(payload_file, "w")
                    for l in lines:
                        payload_f.write(l)
            except:
                print(payload_file, " error")
if __name__ == "__main__":
    path = configuration.pcapfiles
    parse(path)