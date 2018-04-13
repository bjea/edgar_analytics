#!/usr/bin/env python

import collections
import csv
from datetime import datetime, timedelta
import sys


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
            if row and row[0][0].isalpha():
                continue
            elif not row:
                continue
            else:
                date_curr = row[1]
                time_curr = row[2]
                ip = row[0]
                DATE_FORMAT = '%Y-%m-%d'
                TIME_FORMAT = '%H:%M:%S'
                for k, v in dict_log.items():
                    if date_curr != v[2]:
                        d_delta = datetime.strptime(date_curr, DATE_FORMAT) - \
                                  datetime.strptime(v[2], DATE_FORMAT)
                        t_delta = datetime.strptime(time_curr, TIME_FORMAT) - \
                                  datetime.strptime(v[3], TIME_FORMAT)
                        if d_delta.days > 1 or (d_delta.days == 1 and t_delta.days == 0):
                            duration = datetime.strptime(v[3], TIME_FORMAT) - \
                                       datetime.strptime(v[1], TIME_FORMAT)
                            if duration.days < 0:
                                duration_new = timedelta(days=0, seconds=t_delta.seconds,
                                                         microseconds=t_delta.microseconds)

                                duration_secs = duration_new.total_seconds() - 1

                            else:
                                duration_secs = duration.total_seconds() + 1

                            if duration.days == 0 and ((datetime.strptime(v[2], DATE_FORMAT) -
                                                        datetime.strptime(v[0], DATE_FORMAT)).days == 1):
                                duration_secs = duration_secs + 86400
                            with open(out_filename, mode='a+') as outfile:
                                outfile.write(k + "," + v[0] + " " + v[1] + "," + v[2] + " " + v[3] + ","
                                              + str(int(duration_secs)) + "," + str(dict_count[k]))
                                outfile.write("\n")

                            del dict_log[k]
                            del dict_count[k]
                        elif d_delta.days == 1 and t_delta.days < 0:
                            t_delta = timedelta(days=0, seconds=t_delta.seconds, microseconds=t_delta.microseconds)

                            if t_delta.total_seconds() > inactive_time:
                                duration = datetime.strptime(v[3], TIME_FORMAT) - \
                                           datetime.strptime(v[1], TIME_FORMAT)
                                if duration.days < 0:
                                    duration_new = timedelta(days=0, seconds=t_delta.seconds,
                                                             microseconds=t_delta.microseconds)
                                    duration_secs = duration_new.total_seconds() + 1
                                else:
                                    duration_secs = duration.total_seconds() + 1

                                if duration.days == 0 and ((datetime.strptime(v[2], DATE_FORMAT) -
                                                                datetime.strptime(v[0], DATE_FORMAT)).days == 1):
                                    duration_secs = duration_secs + 86400

                                with open(out_filename, mode='a+') as outfile:
                                    outfile.write(k + "," + v[0] + " " + v[1] + "," + v[2] + " " + v[3] + ","
                                                  + str(int(duration_secs)) + "," + str(dict_count[k]))
                                    outfile.write("\n")

                                del dict_log[k]
                                del dict_count[k]

                    else:
                        t_delta = datetime.strptime(time_curr, TIME_FORMAT) - \
                                  datetime.strptime(v[3], TIME_FORMAT)
                        if t_delta.total_seconds() > inactive_time:
                            duration = datetime.strptime(v[3], TIME_FORMAT) - \
                                       datetime.strptime(v[1], TIME_FORMAT)
                            if duration.days < 0:
                                duration_new = timedelta(days=0, seconds=t_delta.seconds,
                                                         microseconds=t_delta.microseconds)
                                duration_secs = duration_new.total_seconds() + 1
                            else:
                                duration_secs = duration.total_seconds() + 1

                            if duration.days == 0 and ((datetime.strptime(v[2], DATE_FORMAT) -
                                                            datetime.strptime(v[0], DATE_FORMAT)).days == 1):
                                duration_secs = duration_secs + 86400

                            with open(out_filename, mode='a+') as outfile:
                                outfile.write(k + "," + v[0] + " " + v[1] + "," + v[2] + " " + v[3] + ","
                                              + str(int(duration_secs)) + "," + str(dict_count[k]))
                                outfile.write("\n")

                            del dict_log[k]
                            del dict_count[k]

                if ip in dict_log:
                    li_prev_entry = dict_log.get(row[0])

                    if date_curr == li_prev_entry[2]:
                        t_delta = datetime.strptime(time_curr, TIME_FORMAT) - \
                                  datetime.strptime(li_prev_entry[3], TIME_FORMAT)
                        if t_delta.total_seconds() < inactive_time + 1:
                            dict_count[ip] += 1
                            dict_log.update({ip: [li_prev_entry[0], li_prev_entry[1], date_curr, time_curr]})
                    else:
                        d_delta = datetime.strptime(date_curr, DATE_FORMAT) - \
                                  datetime.strptime(li_prev_entry[2], DATE_FORMAT)
                        t_delta = datetime.strptime(time_curr, TIME_FORMAT) - \
                                  datetime.strptime(li_prev_entry[3], TIME_FORMAT)
                        if d_delta.days == 1 and t_delta.days < 0:
                            t_delta = timedelta(days=0, seconds=t_delta.seconds, microseconds=t_delta.microseconds)
                            if t_delta.total_seconds() < inactive_time + 1:
                                dict_count[ip] += 1
                                dict_log.update({ip: [li_prev_entry[0], li_prev_entry[1], date_curr, time_curr]})

                else:
                    dict_log.update({ip: [row[1], row[2], date_curr, time_curr]})
                    dict_count[ip] = 1

    for k, v in dict_log.items():
        duration = datetime.strptime(v[3], TIME_FORMAT) - \
                   datetime.strptime(v[1], TIME_FORMAT)
        if duration.days < 0:
            duration_new = timedelta(days=0, seconds=t_delta.seconds,
                                     microseconds=t_delta.microseconds)
            duration_secs = duration_new.total_seconds() + 1
        else:
            duration_secs = duration.total_seconds() + 1

        if duration.days == 0 and ((datetime.strptime(v[2], DATE_FORMAT) -
                                        datetime.strptime(v[0], DATE_FORMAT)).days == 1):
            duration_secs = duration_secs + 86400

        with open(out_filename, mode='a+') as outfile:
            outfile.write(k + "," + v[0] + " " + v[1] + "," + v[2] + " " + v[3] + ","
                          + str(int(duration_secs)) + "," + str(dict_count[k]))
            outfile.write("\n")

        del dict_log[k]
        del dict_count[k]

    return


if __name__ == '__main__':
    input_file = sys.argv[1]
    inactivity_file = sys.argv[2]
    out_filename = sys.argv[3]

    inactive_time = get_inactivity_period(inactivity_file)
    inactive_time = int(inactive_time)

    process_input(input_file, out_filename, inactive_time)
