import sys
from pathlib import Path
import natsort
import re
import json
import datetime
import math
import csv


def _preprocess_gps_data(src_path: str, dst_path: str) -> int:
    pathlist = Path(src_path).glob('**/*.json')
    list1 = []
    list2 = []
    for path in pathlist:
        path_in_str = str(path)
        list1.append(path_in_str)

    list2 = natsort.natsorted(list1)

    with open(dst_path, 'w', newline='') as file_out:
        csv_out = csv.writer(file_out)
        csv_out.writerow(["year", "month", "day", "hour", "minute", "second", "lat", "lon", "alt", "speed", "heading",
                          "altHAE", "eps", "ept", "epv", "epx", "epy", "datetime"])

        row = 0

        for path in list2:
            timestamp_str = re.findall(r'\d+', path)
            try:
                year = timestamp_str[0]
                month = timestamp_str[1]
                day = timestamp_str[2]
                hour = timestamp_str[3]
                minutes = timestamp_str[4]
                seconds = timestamp_str[5]
            except IndexError:
                pass
            else:
                with open(path) as f:
                    try:
                        data = json.load(f)
                    except ValueError:
                        pass
                        # print('JSON error: %s' % path)
                    else:
                        lon = data['coordinates'][0]
                        if math.isnan(lon):
                            lon = 0
                        lat = data['coordinates'][1]
                        if math.isnan(lat):
                            lat = 0
                        alt = float(data.get('altitude', 0))
                        if math.isnan(alt):
                            alt = 0
                        speed = data.get('speed', 0)
                        if math.isnan(speed):
                            speed = 0
                        heading = data.get('heading', 0)
                        if math.isnan(heading):
                            heading = 0
                        altHAE = data.get('altHEA', 0)
                        if math.isnan(altHAE):
                            altHAE = 0
                        eps = data.get('eps', 0)
                        if math.isnan(eps):
                            eps = 0
                        ept = data.get('ept', 0)
                        if math.isnan(ept):
                            ept = 0
                        epv = data.get('epv', 0)
                        if math.isnan(epv):
                            epv = 0
                        epx = data.get('epx', 0)
                        if math.isnan(epx):
                            epx = 0
                        epy = data.get('epy', 0)
                        if math.isnan(epy):
                            epy = 0
                        try:
                            time_str = data.get('time', "").replace("Z", " ").replace("T", " ").replace(".000Z", "").replace(
                                ".000 ", "")
                            time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            time_obj = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds))

                        csv_out.writerow(
                            [year, month, day, hour, minutes, seconds, lat, lon, alt, speed, heading, altHAE, eps, ept, epv, epx,
                             epy, time_obj])
                        row += 1

    return row


if __name__ == '__main__':
    if sys.argv == 1:
        print("Num positions: ", _preprocess_gps_data("/mnt/smb/gps", "/mnt/gps.csv"))
    else:
        print("Src:", sys.argv[1], " Dst:", sys.argv[2], " Num positions:",
              _preprocess_gps_data(sys.argv[1], sys.argv[2]))
