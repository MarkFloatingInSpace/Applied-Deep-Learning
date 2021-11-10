import win32gui
from inputs import get_gamepad
import math
import threading
import os
import re
import win32gui, win32ui, win32con
import numpy as np
import cv2
from PIL import Image


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        steering = self.LeftJoystickX
        accelerator = self.RightTrigger
        brake = self.LeftTrigger
        reset = self.B

        return [steering, accelerator, brake, reset]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state


class WindowCapture:
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name, run_replay_path):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 1
        titlebar_pixels = 10

        side_cutoff = 200
        top_cutoff = 250
        bottom_cutoff = 100

        self.w = self.w - border_pixels - 2 * side_cutoff
        self.h = self.h - titlebar_pixels - border_pixels - top_cutoff - bottom_cutoff
        self.cropped_x = border_pixels + side_cutoff
        self.cropped_y = titlebar_pixels + top_cutoff

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

        self.replay_path = run_replay_path
        self.capture_counter = 0

    def get_screenshot(self, save_method="bmp"):
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        if save_method == "bmp":
            dataBitMap.SaveBitmapFile(cDC, "{}/screenshots{}.bmp".format(self.replay_path, self.capture_counter))
        elif save_method == "rescaled_png":
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (self.h, self.w, 4)
            img = img[::2, ::2, :3]
            cv2.imwrite("{}/screenshots{}.bmp".format(self.replay_path, self.capture_counter), img)

        self.capture_counter += 1

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)


def postprocessing_bmp_screenshots(path):
    for filename in os.listdir(path):
        if filename.endswith(".bmp"):
            im = Image.open(os.path.join(path, filename)).convert('L')
            resized_im = im.resize((im.size[0] // 3, im.size[1] // 3))
            resized_im.save(os.path.join(path, filename.split(".")[0] + ".png"))



def create_replay_dir(base_path, track_name, player_name):
    if not os.path.isdir(os.path.join(base_path, track_name)):
        os.mkdir(os.path.join(base_path, track_name))

    if not os.path.isdir(os.path.join(base_path, track_name, player_name)):
        os.mkdir(os.path.join(base_path, track_name, player_name))

    individual_capture_path = os.path.join(base_path, track_name, player_name)
    run_dir_list = os.listdir(individual_capture_path)
    all_run_names = " ".join(run_dir_list)
    all_run_name_numbers = re.findall(r"run_(\d+)", all_run_names)

    if not all_run_name_numbers:
        run_name = "run_{}".format(1)
    else:
        max_run_number = max([int(i) for i in all_run_name_numbers])
        run_name = "run_{}".format(max_run_number + 1)

    run_path = os.path.join(individual_capture_path, run_name)
    os.mkdir(run_path)

    return run_path


if __name__ == "__main__":
    list_window_names()
