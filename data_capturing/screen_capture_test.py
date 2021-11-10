import cv2
import numpy as np
from utils import XboxController, create_replay_dir, WindowCapture
import time
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    player_name = "Markus"
    track_name = "Track_01"
    capture_path = r"C:\Users\Markus\Documents\Uni\Applied-Deep-Learning\data_capturing\captured data"

    run_replay_path = create_replay_dir(capture_path, track_name, player_name)

    wincap = WindowCapture('Trackmania', run_replay_path)
    myController = XboxController()

    loop_time = time.time()
    # while True:
    time_array = np.zeros((1000, 3))

    for variation_idx in range(2):
        start_time = time.time()
        for frame_number in range(1000):
            # get an updated image of the game
            time_1 = time.time()

            if variation_idx == 0:
                screenshot = wincap.get_screenshot(save_method="bmp")
            elif variation_idx == 1:
                screenshot = wincap.get_screenshot(save_method="rescaled_png")

        end_time = time.time()
        print("Variation {}: {} FPS".format(variation_idx, frame_number / (end_time - start_time)))
