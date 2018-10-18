import os, sys, subprocess
import pandas as pd
import math
import glob
import configuration


def parse(path, output_path):
    full_path = os.path.join(os.getcwd(), path)
    print (os.listdir(full_path))
    devices = os.listdir(full_path)
    for d in devices:
        path = full_path + '/' + d
        if os.path.isdir(path):
            path += "/*.pcap"
            # only needed if we need test files.
            test_file = max(glob.glob(path), key = os.path.getmtime)

            # dns features
            columns_dns = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Length " \
                          "-e eth.src -e eth.src_resolved -e eth.dst -e eth.dst_resolved " \
                          "-e udp.port -e dns.a -e dns.aaaa -e dns.cname -e dns.count.answers " \
                          "-e dns.count.add_rr -e dns.count.auth_rr -e dns.count.labels -e dns.count.prerequisites " \
                          "-e dns.count.queries -e dns.count.updates -e dns.qry.name -e dns.qry.name.len" \
                          " -e dns.qry.class -e dns.qry.type -e dns.resp.name -e dns.resp.type -e dns.resp.class" \
                          " -e dns.resp.ttl -e dns.resp.len"
            genericParser(path, output_path, columns_dns, " -Y 'dns'", test_file, "dns", d, 100)

            # http features
            columns_http = "-e ip.src -e ip.dst -e _ws.col.Protocol -e _" \
                           "ws.col.Length -e eth.src -e eth.src_resolved -e eth.dst" \
                           " -e eth.dst_resolved -e tcp.port -e http.content_length -e http.content_type " \
                           "-e http.host -e http.request -e http.request.uri -e http.server -e http.time " \
                           "-e http.response.line"
            genericParser(path, output_path, columns_http, " -Y 'http'", test_file, "http", d, 100)

            # time delta and protocol features
            columns_general = "-e frame.protocols -e frame.time_delta"
            genericParser(path, output_path, columns_general, "", test_file, "general", d, 100)

            # port features
            columns_dstport = "-e tcp.dstport -e udp.dstport"
            genericParser(path, output_path, columns_dstport, "", test_file, "dstport", d, 100)

            # payload size features
            columns_dstport = "-e ip.len -e ip.hdr_len -e tcp.hdr_len"
            genericParser(path, output_path, columns_dstport, "", test_file, "payload", d, 100)



# @params:
# intput_path: input path
# output_path: output path
# columns: columns to parse
# fields: specify filter if any
# test_file: will generate test file if given a name
# name: customize the output file name
# device: device dir location
# shrink_count: 0 means output everything, otherwise shrink the output to the given number
def genericParser(intput_path, output_path, columns, fields, test_file, name, device, shrink_count=0):
    for f in glob.glob(intput_path):
        if f == test_file:
            output = ">>" + output_path + "/" + device.replace(':', '-') + "-test-" + name + ".csv"
        else:
            output = ">>" + output_path + "/" + device.replace(':', '-') + "-" + name + ".csv"
        command = "tshark -r " + f + fields + " -T fields -E header=y -E separator=/t, " + columns + output
        os.system(command)
    if shrink_count:
        shrink_output_size(output_path, name, device, shrink_count)

        # dns_file = "csvs/" + d.replace(':', '-') + "-dns.csv"
        # lines = []
        # line_count = 0
        # try:
        #     dns_f = open(dns_file)
        #     for line in dns_f:
        #         if line_count == 0 or "ip.src" not in line:
        #             if line_count < 180:
        #                 line_count += 1
        #                 lines.append(line)
        #             else:
        #                 dns_f.close()
        #                 break
        #     if line_count < 180:
        #         os.remove(dns_file)
        #         os.remove("csvs/" + d.replace(':', '-') + "-test-dns.csv")
        #     else:
        #         dns_f = open(dns_file, "w")
        #         for l in lines:
        #             dns_f.write(l)
        # except:
        #     print(dns_file, " error")

def shrink_output_size(output_path, name, device, line_limit):
    csvfile = output_path + "/" + device.replace(':', '-') + "-" + name + ".csv"
    lines = []
    line_count = 0
    try:
        f = open(csvfile)
        print(f)
        for line in f:
            if line_count == 0 or "ip.src" not in line:
                if line_count < line_limit:
                    line_count += 1
                    lines.append(line)
                else:
                    f.close()
                    break
        if line_count < line_limit:
            os.remove(csvfile)
            os.remove(output_path + "/" + device.replace(':', '-') + "-test-" + name +".csv")
        else:
            f = open(csvfile, "w")
            for l in lines:
                f.write(l)
    except:
        print(csvfile, " error")


if __name__ == "__main__":
    input_path = configuration.pcapfiles
    output_path = configuration.outputfiles
    parse(input_path, output_path)
