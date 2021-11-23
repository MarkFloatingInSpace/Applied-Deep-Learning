from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

path = r"C:\Users\Markus\Documents\Uni\Applied-Deep-Learning\data_capturing\captured_data\Track_Supervised_Learning_1\Markus\run_4\screenshots148.png"

img = Image.open(path)
img_size = np.array(img.size)
img_size_samller = (img_size / 4).astype(int)
img_res_closest = img.resize(img_size_samller)
img_res_bilinear = img.resize(img_size_samller, Image.BILINEAR)
img_res_bicubic = img.resize(img_size_samller, Image.BICUBIC)
img_res_lanczos = img.resize(img_size_samller, Image.LANCZOS)

fig, axes = plt.subplots(2,2)
# axes[0, 0].imshow(img)
# axes[0, 0].set_title("original")
axes[0, 1].imshow(img_res_closest)
axes[0, 1].set_title("img_res closest")
axes[1, 0].imshow(img_res_bilinear)
axes[1, 0].set_title("img_res linear")
axes[1, 1].imshow(img_res_bicubic)
axes[1, 1].set_title("img_res cubic")
axes[0, 0].imshow(img_res_lanczos)
axes[0, 0].set_title("img_res img_res_lanczos")

img_orig_gray = ImageOps.grayscale(img)
img_closest_gray = ImageOps.grayscale(img_res_closest)
img_bilinear_gray = ImageOps.grayscale(img_res_bilinear)
img_bicubic_gray = ImageOps.grayscale(img_res_bicubic)
img_lanczos_gray = ImageOps.grayscale(img_res_lanczos)

fig, axes = plt.subplots(2,2)
# axes[0, 0].imshow(img_orig_gray)
# axes[0, 0].set_title("original")
axes[0, 1].imshow(img_closest_gray, cmap="gray")
axes[0, 1].set_title("img_res closest")
axes[1, 0].imshow(img_bilinear_gray, cmap="gray")
axes[1, 0].set_title("img_res linear")
axes[1, 1].imshow(img_bicubic_gray, cmap="gray")
axes[1, 1].set_title("img_res cubic")
axes[0, 0].imshow(img_lanczos_gray, cmap="gray")
axes[0, 0].set_title("img_res img_res_lanczos")


plt.show()
