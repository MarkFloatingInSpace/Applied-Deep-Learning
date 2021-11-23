import cv2
import numpy as np
from utils import XboxController, create_replay_dir, WindowCapture, bmp_2_compresed_batch
import time
import os
import matplotlib.pyplot as plt


if __name__ == "__main__":
    player_name = "Markus"
    track_name = "Track_Supervised_Learning_1"
    capture_path = r"C:\Users\Markus\Documents\Uni\Applied-Deep-Learning\data_capturing\captured_data"

    myController = XboxController()

    recording_flag = False
    frame_number = 0

    while True:
        if not recording_flag:
            if myController.LeftBumper:
                recording_flag = True
                run_replay_path = create_replay_dir(capture_path, track_name, player_name)
                wincap = WindowCapture('Trackmania', run_replay_path)
                frame_number = 0
                print("Recording started.")
                start_time = time.time()
        else:
            if myController.RightBumper:
                recording_flag = False
                end_time = time.time()
                print("Stopped recording.")
                print("Avg FPS: {}".format(frame_number/(end_time-start_time)))
                # print("Converting to png...")
                # bmp_2_compresed_batch(run_replay_path)
                # print("Finished converting!")

            else:
                time_1 = time.time()
                # get an updated image of the game
                screenshot = wincap.get_screenshot(save_method="bmp")
                time_2 = time.time()
                # read controller input
                controller_input = myController.read()
                time_3 = time.time()

                with open(os.path.join(run_replay_path, 'inputs.txt'), 'a') as input_file_obj:
                    input_file_obj.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(frame_number, time_1, time_2, time_3,
                                                                               *controller_input[:3]))

                # debug the loop rate
                # print('FPS {}'.format(1 / (time.time() - time_1)))

                frame_number += 1