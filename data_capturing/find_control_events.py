from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
import itertools
import random

num_samples = 500
path = r"C:\Users\Markus\Documents\Uni\Applied-Deep-Learning\data_capturing\captured_data\Track_Supervised_Learning_1\Markus\run_4\inputs.txt"

input_df = pd.read_csv(path, delimiter="\t", names=["frame_id", "time_1", "time_2", "time_3", "steering", "throttle", "brake"])

input_df["rois_steering"] = np.abs(input_df["steering"]) > 0.03
input_df["rois_steering_change"] = np.abs(input_df["steering"].diff(3)) > 0.01
input_df["rois_throttle"] = input_df["throttle"] < 0.9
input_df["rois_throttle_change"] = np.abs(input_df["throttle"].diff(3)) > 0.01
input_df["rois_brake"] = input_df["brake"] > 0.1
input_df["rois_brake_change"] = np.abs(input_df["brake"].diff(3)) > 0.01

input_df["event_significance"] = np.sum(input_df.iloc[:, 7:13], axis=1) + 1
sample_idxs = random.choices(input_df.index, input_df["event_significance"], k=num_samples)

# -----

def get_start_stop_idx_rois(input_df, featur_name):
    start = np.argwhere(input_df[featur_name].to_numpy()[1:] > input_df[featur_name].to_numpy()[:-1])
    stop = np.argwhere(input_df[featur_name].to_numpy()[1:] < input_df[featur_name].to_numpy()[:-1])
    return start, stop

rois_steering_starts, rois_steering_stops = get_start_stop_idx_rois(input_df, "rois_steering")
rois_throttle_starts, rois_throttle_stops = get_start_stop_idx_rois(input_df, "rois_throttle")
rois_brake_starts, rois_brake_stops = get_start_stop_idx_rois(input_df, "rois_brake")

rois_steering_change_starts, rois_steering_change_stops = get_start_stop_idx_rois(input_df, "rois_steering_change")
rois_throttle_change_starts, rois_throttle_change_stops = get_start_stop_idx_rois(input_df, "rois_throttle_change")
rois_brake_change_starts, rois_brake_change_stops = get_start_stop_idx_rois(input_df, "rois_brake_change")

fig, axes = plt.subplots(5, 1)

# for (start, stop) in zip(rois_combined_starts, rois_combined_stops):
#     axes[0].axvspan(start, stop, facecolor='r', alpha=0.5)

for (start, stop) in zip(rois_steering_starts, rois_steering_stops):
    axes[0].axvspan(start, stop, facecolor='b', alpha=0.3)
for (start, stop) in zip(rois_steering_change_starts, rois_steering_change_stops):
    axes[0].axvspan(start, stop, facecolor='r', alpha=0.3)
axes[0].plot(input_df["steering"])

for (start, stop) in zip(rois_throttle_starts, rois_throttle_stops):
    axes[1].axvspan(start, stop, facecolor='b', alpha=0.3)
for (start, stop) in zip(rois_throttle_change_starts, rois_throttle_change_stops):
    axes[1].axvspan(start, stop, facecolor='r', alpha=0.3)
axes[1].plot(input_df["throttle"])

for (start, stop) in zip(rois_brake_starts, rois_brake_stops):
    axes[2].axvspan(start, stop, facecolor='b', alpha=0.3)
for (start, stop) in zip(rois_brake_change_starts, rois_brake_change_stops):
    axes[2].axvspan(start, stop, facecolor='r', alpha=0.3)
axes[2].plot(input_df["brake"])

axes[3].plot(input_df["event_significance"])
axes[4].plot(sample_idxs, np.zeros(len(sample_idxs)), 'o')
plt.show()

