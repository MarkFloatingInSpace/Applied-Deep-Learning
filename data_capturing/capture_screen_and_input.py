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
    for frame_number in range(1000):
        # get an updated image of the game
        time_1 = time.time()
        screenshot = wincap.get_screenshot()
        time_2 = time.time()
        controller_input = myController.read()
        time_3 = time.time()

        time_array[frame_number, :] = [time_1, time_2, time_3]

        with open(os.path.join(run_replay_path, 'inputs.txt'), 'a') as input_file_obj:
            input_file_obj.write("{}\t{}\t{}\t{}\t{}\n".format(frame_number, time_2, *controller_input[:3]))

        # debug the loop rate
        print('FPS {}'.format(1 / (time.time() - loop_time)))
        loop_time = time.time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

    loop_dt = np.diff(time_array[:, 0])
    step_dt = np.diff(time_array, 1, axis=1)

    plt.figure()
    plt.plot(loop_dt)
    plt.show()
