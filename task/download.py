#!/usr/bin/env python3

import sys
from pathlib import Path

from gwpy.timeseries import TimeSeries, TimeSeriesDict


# ====================== 配置 ======================
start = 1378402219
duration  = 3072
FRAMETYPE = "H1_R"
end  = start + duration
frequency = 120
FRAMETYPE_strain = 'H1_HOFT_C00_AR'

strain_channel = "H1:GDS-CALIB_STRAIN_CLEAN_AR"

channel_file = f"/home/yuchen.liu/deepclean/channels/{frequency}hz_aux_channel.txt"

TARGET_RATE = 4096
OUTPUT_FILE = f"/home/yuchen.liu/deepclean/data/{start}_{duration}_{frequency}.hdf5"
# ===============================================================


def read_channel(path):
    channels = []
    with open(path) as f:
        for line in f:
            line = line.strip('",').strip()
            if not line or line.startswith("#"):
                continue
            channels.append(line)
    return channels




def to_hdf5(data, output_path, target_rate=None):

    data = data.resample(target_rate)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.write(str(output_path), format="hdf5", overwrite=True)



def main():
    witness = read_channel(channel_file)
    data = TimeSeriesDict()
    strain = TimeSeries.get(strain_channel, start, end, frametype=FRAMETYPE_strain)
    data[strain_channel] = strain
    for ch in witness:
        data[ch] = TimeSeries.get(ch, start, end, frametype=FRAMETYPE)
    to_hdf5(data, OUTPUT_FILE, target_rate=TARGET_RATE)


if __name__ == "__main__":
    main()
