#!/usr/bin/env python

import csv
import collections
from datetime import datetime


def get_inactivity_period(filename):
    with open(filename, mode='r') as myfile:
        inactive_time = myfile.read()

    return inactive_time


def process_input(in_filename, out_filename, inactive_time):
    dict_log = collections.OrderedDict()
    dict_count = {}
    with open(in_filename, newline='') as infile:
        log = csv.reader(infile)

        for row in log:
            if row[0] == 'ip':
                continue
            else:
                date_curr = row[1]
                time_curr = row[2]
                ip = row[0]
                TIME_FORMAT = '%H:%M:%S'
                for k, v in dict_log.items():
                    if date_curr == v[2]:
                        t_delta = datetime.strptime(time_curr, TIME_FORMAT) - \
                              datetime.strptime(v[3], TIME_FORMAT)
                        if t_delta.total_seconds() > inactive_time:
                            duration = (datetime.strptime(v[3], TIME_FORMAT) - \
                              datetime.strptime(v[1], TIME_FORMAT)).total_seconds() + 1
                            with open(out_filename, mode='a+') as outfile:
                                outfile.write(k + "," + v[0] + " " + v[1] + "," + v[2] + " " + v[3] + ","
                                              + str(int(duration)) + "," + str(dict_count[k]))
                                outfile.write("\n")

                            del dict_log[k]
                            del dict_count[k]

                if ip in dict_log:
                    li_prev_entry = [ip] + dict_log.get(row[0])

                    if date_curr == li_prev_entry[3]:
                        t_delta = datetime.strptime(time_curr, TIME_FORMAT) - \
                                  datetime.strptime(li_prev_entry[4], TIME_FORMAT)
                        if t_delta.total_seconds() < inactive_time + 1:
                            dict_count[ip] += 1
                            dict_log.update({ip: [li_prev_entry[1], li_prev_entry[2], date_curr, time_curr]})

                else:
                    dict_log.update({ip: [row[1], row[2], date_curr, time_curr]})
                    dict_count[ip] = 1

    for k, v in dict_log.items():
        duration = (datetime.strptime(v[3], TIME_FORMAT) - \
                    datetime.strptime(v[1], TIME_FORMAT)).total_seconds() + 1
        with open(out_filename, mode='a+') as outfile:
            outfile.write(k + "," + v[0] + " " + v[1] + "," + v[2] + " " + v[3] + ","
                          + str(int(duration)) + "," + str(dict_count[k]))
            outfile.write("\n")

        del dict_log[k]
        del dict_count[k]

    return


if __name__ == '__main__':

    input_file = "../input/log.csv"
    inactivity_file = "../input/inactivity_period.txt"
    out_filename = "../output/sessionization.txt"

    inactive_time = get_inactivity_period(inactivity_file)
    inactive_time = int(inactive_time)

    process_input(input_file, out_filename, inactive_time)
