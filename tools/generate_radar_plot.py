#!/usr/bin/env python3
import json
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.join(
    os.path.dirname(__file__), "..")))

import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from math import pi


def generate_radar_chart(data: str, output_path: str):
    radar_data = {}
    radar_data["group"] = []
    label_count = len(data["labels"])
    for label, value in data["data"].items():
        radar_data["group"].append(label)
        radar_data[label] = [value for i in range(label_count)]

    df = pd.DataFrame(radar_data)
    categories = list(df)[1:]
    cat_count = len (categories)

    values = df.loc[0].drop("group").values.flatten().tolist()
    values += values[:1]

    angles = [n / float(cat_count) * 2 * pi for n in range(cat_count)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, color="#6f7274", size=6)

    for label, i in zip(ax.get_xticklabels(), range(0, len(angles))):
        angle_rad = angles[i]
        if angle_rad <= pi / 2:
            ha = "left"
            va = "bottom"
        elif pi/2 < angle_rad <= pi:
            ha = "right"
            va = "bottom"
        elif pi < angle_rad <= (3*pi/2):
            ha = "right"
            va = "top"
        else:
            ha = "right"
            va = "top"
        label.set_verticalalignment(va)
        label.set_horizontalalignment(ha)

    ax.set_rlabel_position(30)
    plt.yticks([5, 10, 15, 20], ["5", "10", "15", "20"], color="grey", size=7)
    plt.ylim(0, 20)

    ax.plot(angles, values, linewidth=1, linestyle="solid", color="#e30d29")
    ax.fill(angles, values, "#e30d29", alpha=0.1)

    if not os.path.exists(os.path.split(output_path)[0]):
        os.mkdir(os.path.split(output_path)[0])
    plt.savefig(output_path)
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", type=str)
    parser.add_argument("-o", "--output", type=str)

    args = parser.parse_args()
    data = json.loads(args.data)
    output_path = args.output

    generate_radar_chart(data, output_path)
