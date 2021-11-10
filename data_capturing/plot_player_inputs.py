import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = r"C:\Users\Markus\Documents\Uni\Applied-Deep-Learning\data_capturing\captured data\Track_01\Markus\run_22\inputs.txt"

input_df = pd.read_csv(path, delimiter="\t", names=["screenshot_number", "time", "steering", "throttle", "brake"])

print(input_df)

dt = input_df.time.diff()

plt.figure()
plt.plot(dt)

plt.figure()
plt.plot(input_df["steering"][:400])

plt.figure()
plt.plot(input_df["throttle"])
plt.plot(input_df["brake"])
plt.show()