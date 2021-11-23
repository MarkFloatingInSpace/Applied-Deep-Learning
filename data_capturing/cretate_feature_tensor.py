import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
import itertools
import random


def find_sample_indices(run_path, input_df, selection_percent=0.25):
    num_samples = int(input_df.index.__len__() * selection_percent)

    input_df["rois_steering"] = np.abs(input_df["steering"]) > 0.03
    input_df["rois_steering_change"] = np.abs(input_df["steering"].diff(3)) > 0.01
    input_df["rois_throttle"] = input_df["throttle"] < 0.9
    input_df["rois_throttle_change"] = np.abs(input_df["throttle"].diff(3)) > 0.01
    input_df["rois_brake"] = input_df["brake"] > 0.1
    input_df["rois_brake_change"] = np.abs(input_df["brake"].diff(3)) > 0.01

    input_df["event_significance"] = np.sum(input_df.iloc[:, 7:13], axis=1) + 1
    sample_indices = random.choices(input_df.index, input_df["event_significance"], k=num_samples)
    return sample_indices


def image_preparation(img_path, img_size, bw=True):
    img = Image.open(img_path)
    img_rescaled = img.resize(img_size, Image.LANCZOS)

    if bw:
        img_rescaled = ImageOps.grayscale(img_rescaled)

    return np.asarray(img_rescaled) / 255


def create_run_feature_tensor(run_path, selection_percent=0.25, img_size=(383, 189)):
    inputs_path = os.path.join(run_path, "inputs.txt")
    input_df = pd.read_csv(inputs_path, delimiter="\t",
                           names=["frame_id", "time_1", "time_2", "time_3", "steering", "throttle", "brake"])
    sample_indices = find_sample_indices(run_path, input_df, selection_percent=selection_percent)

    file_name_list = os.listdir(path)
    img_name_list = [i for i in file_name_list if i.endswith(".png")]
    img_indices = [int(i[11:-4]) for i in img_name_list]

    sample_indices_available = np.intersect1d(sample_indices, img_indices)
    num_used_samples = len(sample_indices_available)

    feature_tensor = np.zeros((num_used_samples, img_size[1], img_size[0]))
    for idx, sample_idx in enumerate(sample_indices_available):
        sample_path = os.path.join(run_path, f"screenshots{sample_idx}.png")

        img = image_preparation(sample_path, img_size)
        feature_tensor[idx, :, :] = img

        if (idx * 100 / num_used_samples) % 10 == 0:
            print(f"{idx * 100 / num_used_samples}%")

    target_matrix = input_df.loc[sample_indices_available, ["steering", "throttle", "brake"]]
    return feature_tensor, target_matrix


if __name__ == "__main__":
    path = r"C:\Users\Markus\Documents\Uni\Applied-Deep-Learning\data_capturing\captured_data\Track_Supervised_Learning_1\Markus\run_4"
    run_name = os.path.split(path)[-1]
    save_path = os.path.join(path, f"{run_name}_feature_target.npz")

    feature_tensor, target_matrix = create_run_feature_tensor(path)
    np.savez(save_path, name1=feature_tensor, name2=target_matrix)